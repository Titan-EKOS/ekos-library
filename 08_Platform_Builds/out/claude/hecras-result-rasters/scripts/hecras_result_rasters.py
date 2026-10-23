#!/usr/bin/env python3
"""
hecras_result_rasters.py  (v2.0.0)
==================================
Generate Max Depth, Max Velocity and Max Water-Surface-Elevation rasters from a
HEC-RAS 2D plan results HDF, on a regular grid, optionally clipped to a polygon.
Also builds proposed-minus-existing difference rasters from two exported sets.

Auto-detects:
  * the 2D flow area name(s) in the HDF,
  * the model's native projection (HDF "Projection" attribute),
  * the scenario terrain the plan's geometry names ("Terrain Filename"),
    resolved BY BASENAME to a .vrt / .tif in the Terrain folder.

Pre-checks (v2.0.0):
  * Volume accounting: reads the plan HDF volume error (Volume Accounting
    attributes, else the compute messages). Above the limit (0.1 % final,
    0.5 % with --screening) the export is REFUSED (exit code 2) unless
    --vol-warn-only is given, in which case the rasters are written and the
    flag VOL_ERROR_OVER_LIMIT is recorded in the raster dictionary.
  * Terrain modifications: warns when the geometry or the terrain HDF holds
    terrain modifications. The script reads the base .vrt/.tif only, so depth
    does not include them. Pass --terrain with a RAS Mapper export of the
    modified terrain to fix this.

Naming (v2.0.0):
  --naming d43  (default)  <scenario>_<event>_<variable>_<units>_<cell>ft.tif
                           e.g. EX_100yr_Depth_ft_10ft.tif
  --naming plan (legacy)   <tag>_MaxDepth_ft_<cell>ft.tif, tag = plan number
  Every run appends rows to raster_dictionary.csv in --outdir (file, scenario,
  event, variable, units, cell size, plan number, plan title, HDF, terrain,
  tool, volume error, flags). Difference rasters go to <outdir>/Differences.

Method:
  Depth    = max WSE (flat per cell) - terrain on the output grid.
  Velocity = per-cell max of |Maximum Face Velocity| over the cell's faces
             (proxy; runs higher than RAS Mapper cell velocity).
  One data mask (depth > 0.01 ft) applied to all three rasters. This is the
  data mask, not the display cutoff; exhibits set the display cutoff.

Usage:
  python hecras_result_rasters.py --hdf PLAN.p14.hdf --scenario EX --event 100yr
        [--clip CLIP.shp] [--cellsize 10] [--epsg 2868] [--area NAME]
        [--terrain MODIFIED_TERRAIN.tif] [--outdir DIR]
        [--screening] [--vol-max 0.1] [--vol-warn-only]
  python hecras_result_rasters.py --hdf PLAN.p14.hdf --naming plan --tag p14
  python hecras_result_rasters.py --diff-base EX_100yr_WSE_ft_10ft.tif
        --diff-new PR_100yr_WSE_ft_10ft.tif --variable wse --outdir DIR

Exit codes: 0 done, 1 error, 2 refused by the volume pre-check.
"""
import argparse
import csv
import datetime
import os
import re
import shutil
import sys
import tempfile

import numpy as np

__version__ = "2.0.0"
TOOL_TAG = f"hecras_result_rasters.py {__version__}"

NODATA = -9999.0
WET = 0.01            # ft: data mask (D33). Display cutoff is set on the exhibit.
VOL_MAX_FINAL = 0.1   # percent (D09)
VOL_MAX_SCREEN = 0.5  # percent, screening runs only (D09)
DIFF_DISPLAY = 0.10   # ft: default display threshold for difference maps (D33)

SUMMARY = ("Results/Unsteady/Output/Output Blocks/Base Output/"
           "Summary Output/2D Flow Areas")
VOL_ACCT_PATHS = ("Results/Unsteady/Summary/Volume Accounting",
                  "Results/Summary/Volume Accounting")
MSG_PATHS = ("Results/Unsteady/Summary/Compute Messages (text)",
             "Results/Summary/Compute Messages (text)",
             "Results/Unsteady/Compute Messages (text)")

# key -> (file token, units, legacy name)
VARIABLES = {
    "depth":    ("Depth",    "ft",  "MaxDepth_ft"),
    "velocity": ("Velocity", "fps", "MaxVelocity_fps"),
    "wse":      ("WSE",      "ft",  "MaxWSE_ft"),
}

DICT_FIELDS = ["file", "folder", "scenario", "event", "variable", "units",
               "cellsize_ft", "plan_number", "plan_title", "plan_hdf",
               "terrain", "tool", "volume_error_pct", "volume_limit_pct",
               "flags", "created"]

_ERR_KEY = re.compile(r"(error.*(percent|%|pct))|((percent|%|pct).*error)", re.I)
_MSG_PCT = re.compile(
    r"volume\s+accounting\s+error\s+as\s+(a\s+)?percentage\s*[:=]?\s*"
    r"(-?\d+(\.\d+)?([eE][-+]?\d+)?)", re.I)
_MSG_PCT2 = re.compile(
    r"percent\s+error\s*[:=]?\s*(-?\d+(\.\d+)?([eE][-+]?\d+)?)", re.I)


def log(*a):
    print(*a, flush=True)


def _s(v):
    """Decode HDF bytes / numpy scalars to str."""
    if isinstance(v, (bytes, np.bytes_)):
        return v.decode(errors="replace")
    if isinstance(v, np.ndarray) and v.size == 1:
        return _s(v.reshape(-1)[0])
    return str(v)


def _f(v):
    try:
        if isinstance(v, np.ndarray):
            v = v.reshape(-1)[0]
        return float(_s(v)) if isinstance(v, (bytes, np.bytes_, str)) else float(v)
    except Exception:
        return None


# ----------------------------------------------------------------- naming ---
def clean_token(s):
    """File-name token: no spaces, no underscores (underscore separates tokens)."""
    t = re.sub(r"[^A-Za-z0-9.\-]+", "-", str(s).strip()).strip("-")
    return t


def fmt_cell(cs):
    cs = float(cs)
    if abs(cs - round(cs)) < 1e-9:
        return str(int(round(cs)))
    return ("%g" % cs).replace(".", "p")


def d43_name(scenario, event, var_key, cellsize):
    tok, units, _ = VARIABLES[var_key]
    return f"{clean_token(scenario)}_{clean_token(event)}_{tok}_{units}_{fmt_cell(cellsize)}ft.tif"


def plan_name(tag, var_key, cellsize):
    """Legacy v1 naming kept as an option (--naming plan)."""
    return f"{tag}_{VARIABLES[var_key][2]}_{int(round(float(cellsize)))}ft.tif"


def diff_name(new_scn, base_scn, event, var_key, cellsize):
    tok, units, _ = VARIABLES[var_key]
    return (f"{clean_token(new_scn)}-minus-{clean_token(base_scn)}_{clean_token(event)}_"
            f"{tok}_{units}_{fmt_cell(cellsize)}ft_Difference.tif")


def parse_d43(fname):
    """Return dict of tokens from a D43 file name, or None."""
    m = re.match(r"^([^_]+)_([^_]+)_(Depth|WSE|Velocity)_(ft|fps)_([0-9p]+)ft\.tif$",
                 os.path.basename(fname))
    if not m:
        return None
    return dict(scenario=m.group(1), event=m.group(2), token=m.group(3),
                units=m.group(4), cell=m.group(5))


# -------------------------------------------------------------- plan info ---
def plan_info(f, hdf_path):
    m = re.search(r"\.(p\d{2})\.hdf$", os.path.basename(hdf_path), re.I)
    info = {"plan_number": m.group(1).lower() if m else "", "plan_title": "",
            "geometry_title": "", "flow_title": ""}
    g = f.get("Plan Data/Plan Information")
    if g is not None:
        for k, key in (("plan_title", "Plan Title"), ("geometry_title", "Geometry Title"),
                       ("flow_title", "Flow Title")):
            if key in g.attrs:
                info[k] = _s(g.attrs[key]).strip()
    return info


# ------------------------------------------------------ volume pre-check ---
def read_volume_error(f):
    """Read percent volume error from a plan HDF.

    Returns dict(global_pct, regional={path: pct}, source) or None when the
    HDF holds no volume accounting the script can find.
    """
    out = {"global_pct": None, "regional": {}, "source": None}
    for p in VOL_ACCT_PATHS:
        g = f.get(p)
        if g is None:
            continue
        for k, v in g.attrs.items():
            if _ERR_KEY.search(k):
                val = _f(v)
                if val is not None and out["global_pct"] is None:
                    out["global_pct"] = val
                    out["source"] = f"{p} attr '{k}'"

        def visit(name, obj, base=p):
            full = f"{base}/{name}"
            for k, v in obj.attrs.items():
                if _ERR_KEY.search(k):
                    val = _f(v)
                    if val is not None:
                        out["regional"][f"{full} attr '{k}'"] = val
            if hasattr(obj, "dtype") and obj.dtype.names:
                names = obj.dtype.names
                errf = [n for n in names if _ERR_KEY.search(n)]
                labf = [n for n in names if re.search(r"name|area|region", n, re.I)]
                if errf:
                    data = obj[()]
                    data = np.atleast_1d(data)
                    for i, row in enumerate(data):
                        lab = _s(row[labf[0]]).strip() if labf else str(i)
                        for e in errf:
                            val = _f(row[e])
                            if val is not None:
                                out["regional"][f"{full}[{lab}].{e}"] = val
        g.visititems(visit)
        if out["global_pct"] is None and out["regional"]:
            # one value only -> treat it as the global number
            if len(out["regional"]) == 1:
                k, v = out["regional"].popitem()
                out["global_pct"], out["source"] = v, k
        break
    if out["global_pct"] is None:
        for p in MSG_PATHS:
            d = f.get(p)
            if d is None:
                continue
            raw = d[()]
            if isinstance(raw, np.ndarray):
                text = "\n".join(_s(x) for x in raw.reshape(-1))
            else:
                text = _s(raw)
            hits = _MSG_PCT.findall(text)
            if hits:
                out["global_pct"] = float(hits[-1][1])
                out["source"] = f"{p} (compute messages)"
                break
            hits = _MSG_PCT2.findall(text)
            if hits:
                out["global_pct"] = float(hits[-1][0])
                out["source"] = f"{p} (compute messages, 'percent error')"
                break
    if out["global_pct"] is None and not out["regional"]:
        return None
    return out


def volume_gate(vol, limit, warn_only=False):
    """Decide whether to export. Returns (ok, flags, messages)."""
    flags, msgs = [], []
    if vol is None or vol["global_pct"] is None:
        flags.append("VOL_NOT_FOUND")
        msgs.append("WARN: no volume accounting found in the plan HDF. Read the global and "
                    "per-area Volume Accounting in HEC-RAS before using these rasters (QC-C21).")
        return True, flags, msgs
    g = vol["global_pct"]
    msgs.append(f"Volume error {g:.4f} % (limit {limit} %) from {vol['source']}")
    for k, v in vol["regional"].items():
        if abs(v) > limit:
            flags.append("REGIONAL_VOL_ERROR_OVER_LIMIT")
            msgs.append(f"WARN: regional volume error {v:.4f} % at {k}; opposing regional errors "
                        f"can cancel in the global number (QC-C21).")
            break
    if abs(g) > limit:
        flags.append("VOL_ERROR_OVER_LIMIT")
        if warn_only:
            msgs.append(f"WARN: volume error {g:.4f} % exceeds {limit} %. Exporting because "
                        f"--vol-warn-only was given; rasters are flagged and are not for reporting.")
            return True, flags, msgs
        msgs.append(f"REFUSED: volume error {g:.4f} % exceeds {limit} %. Fix the run (QC-C21) or "
                    f"rerun with --vol-warn-only for a flagged diagnostic export.")
        return False, flags, msgs
    return True, flags, msgs


# --------------------------------------------- terrain resolution / mods ---
def _terrain_names(f, area):
    names = []
    for key in (f"Geometry/2D Flow Areas/{area}", "Geometry"):
        g = f.get(key)
        if g is None:
            continue
        for attr in ("Terrain Filename", "Terrain File Name"):
            tf = g.attrs.get(attr)
            if tf is not None:
                names.append(_s(tf).replace("\\", "/"))
    return names


def resolve_terrain(hdf_path, f, area):
    """Find the raster terrain the plan's geometry names (basename match only)."""
    proj_dir = os.path.dirname(os.path.abspath(hdf_path))
    for tf in _terrain_names(f, area):
        stem = os.path.splitext(os.path.basename(tf))[0]
        for sub in ("Terrain", "."):
            for ext in (".vrt", ".tif", ".tiff"):
                hit = os.path.join(proj_dir, sub, stem + ext)
                if os.path.exists(hit):
                    return hit
    return None


def _find_mod_paths(h):
    hits = []

    def visit(name, obj):
        if re.search(r"modif", name.split("/")[-1], re.I):
            hits.append(name)
        else:
            for k in obj.attrs.keys():
                if re.search(r"modif", k, re.I):
                    hits.append(f"{name} attr '{k}'")
                    break
    h.visititems(visit)
    return hits


def terrain_mod_warnings(hdf_path, f, area, terrain_path, terrain_override=False):
    """Warn when terrain modifications exist that the base raster does not carry."""
    import h5py
    warns = []
    if terrain_override:
        warns.append("NOTE: --terrain override used; confirm it is the RAS Mapper export of the "
                     "terrain (with modifications) the plan's geometry uses.")
        return warns
    geo = f.get("Geometry")
    if geo is not None:
        hits = _find_mod_paths(geo)
        if hits:
            warns.append("WARN: the plan geometry holds terrain modification data "
                         f"({hits[0]}{' ...' if len(hits) > 1 else ''}). Depth here is computed on the "
                         "base terrain raster and does NOT include these modifications. Export the "
                         "modified terrain from RAS Mapper and pass it with --terrain.")
    proj_dir = os.path.dirname(os.path.abspath(hdf_path))
    cands = []
    for tf in _terrain_names(f, area):
        stem = os.path.splitext(os.path.basename(tf))[0]
        for sub in ("Terrain", "."):
            cands.append(os.path.join(proj_dir, sub, stem + ".hdf"))
    if terrain_path:
        cands.append(os.path.splitext(terrain_path)[0] + ".hdf")
    seen = set()
    for c in cands:
        c = os.path.normpath(c)
        if c in seen or not os.path.exists(c):
            continue
        seen.add(c)
        try:
            with h5py.File(c, "r") as t:
                hits = _find_mod_paths(t)
        except Exception as e:  # unreadable terrain HDF
            warns.append(f"WARN: terrain HDF {os.path.basename(c)} could not be read ({e}); check "
                         "for terrain modifications in RAS Mapper before using depth.")
            continue
        if hits:
            warns.append(f"WARN: terrain HDF {os.path.basename(c)} holds modifications "
                         f"({hits[0]}). The script reads the base .vrt/.tif, so depth does NOT "
                         "include them. Export the modified terrain from RAS Mapper and pass --terrain.")
    if terrain_path is None:
        warns.append("WARN: no terrain raster resolved; depth falls back to cell minimum "
                     "elevation (blocky, cell-resolution depth).")
    else:
        warns.append("NOTE: terrain resolved by basename only "
                     f"({os.path.basename(terrain_path)}); confirm it matches the geometry's "
                     "terrain in RAS Mapper.")
    return warns


# ---------------------------------------------------------- array helpers ---
def cell_velocity(face_cell, face_vel, ncell):
    """Per-cell max |face velocity| over the faces bounding each cell."""
    cellvel = np.zeros(ncell)
    av = np.abs(np.asarray(face_vel, dtype=float))
    for col in (0, 1):
        ci = face_cell[:, col]
        m = (ci >= 0) & (ci < ncell)
        np.maximum.at(cellvel, ci[m], av[m])
    return cellvel


def depth_from(wse, terr, wet=WET, nodata=NODATA):
    depth = np.full(wse.shape, nodata, "float32")
    valid = (wse != nodata) & (terr != nodata)
    d = wse - terr
    m = valid & (d > wet)
    depth[m] = d[m]
    return depth


def difference(new, base, var_key, nodata=NODATA):
    """new - base. WSE: only where both wet. Depth/velocity: dry counts as 0."""
    new = np.asarray(new, dtype="float32")
    base = np.asarray(base, dtype="float32")
    out = np.full(new.shape, nodata, "float32")
    nw, bw = new != nodata, base != nodata
    if var_key == "wse":
        m = nw & bw
        out[m] = new[m] - base[m]
    else:
        m = nw | bw
        n0 = np.where(nw, new, 0.0)
        b0 = np.where(bw, base, 0.0)
        out[m] = (n0 - b0)[m]
    return out


def spot_points(depth, transform, n=10, nodata=NODATA):
    """Pick up to n wet pixels spread across the depth distribution."""
    rr, cc = np.nonzero(depth != nodata)
    if rr.size == 0:
        return []
    order = np.argsort(depth[rr, cc])
    idx = np.unique(np.linspace(0, order.size - 1, min(n, order.size)).astype(int))
    pts = []
    for i in order[idx]:
        r, c = int(rr[i]), int(cc[i])
        x = transform.c + (c + 0.5) * transform.a
        y = transform.f + (r + 0.5) * transform.e
        pts.append((r, c, x, y))
    return pts


def append_dictionary(outdir, rows):
    path = os.path.join(outdir, "raster_dictionary.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=DICT_FIELDS)
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in DICT_FIELDS})
    return path


def _copy_out(src, dest):
    # truncate-copy works even where delete is blocked
    with open(src, "rb") as s, open(dest, "wb") as o:
        o.write(s.read())


# ----------------------------------------------------------------- export ---
def export(a):
    import h5py
    import rasterio
    from rasterio.transform import from_origin
    from rasterio.features import rasterize, geometry_mask
    from rasterio.warp import reproject, Resampling, calculate_default_transform
    from shapely.geometry import Polygon
    from pyproj import CRS

    if a.naming == "d43" and not (a.scenario and a.event):
        log("ERROR: --naming d43 needs --scenario and --event (e.g. --scenario EX --event 100yr), "
            "or use --naming plan for the legacy plan-number names.")
        return 1
    os.makedirs(a.outdir, exist_ok=True)
    limit = a.vol_max if a.vol_max is not None else (VOL_MAX_SCREEN if a.screening else VOL_MAX_FINAL)

    f = h5py.File(a.hdf, "r")
    pinfo = plan_info(f, a.hdf)
    log(f"Plan: {pinfo['plan_number'] or '?'}  '{pinfo['plan_title']}'  ({os.path.basename(a.hdf)})")

    # 1. volume pre-check before anything else
    vol = read_volume_error(f)
    ok, flags, msgs = volume_gate(vol, limit, a.vol_warn_only)
    for m in msgs:
        log(m)
    if not ok:
        f.close()
        return 2

    wkt = f.attrs.get("Projection")
    ncrs = None
    if wkt is not None:
        try:
            ncrs = CRS.from_wkt(_s(wkt))
        except Exception:
            ncrs = None
    if ncrs is None:
        log("WARN: no readable Projection in HDF; assuming inputs already in target CRS")
    nat_epsg = (ncrs.to_epsg() if ncrs else None) or a.epsg
    tgt_epsg = a.epsg or nat_epsg
    if tgt_epsg is None:
        f.close()
        log("ERROR: could not determine a CRS; pass --epsg")
        return 1

    grp = f["Geometry/2D Flow Areas"]
    areas = [k for k in grp.keys() if isinstance(grp[k], h5py.Group)]
    if not areas:
        f.close()
        log("ERROR: no 2D flow areas in HDF")
        return 1
    area = a.area or areas[0]
    if len(areas) > 1 and not a.area:
        log(f"WARN: {len(areas)} 2D areas {areas}; using '{area}'. Pass --area to choose.")
    log(f"2D area: {area}   native EPSG: {nat_epsg}   target EPSG: {tgt_epsg}")
    tag = a.tag or pinfo["plan_number"] or os.path.basename(a.hdf).split('.')[-2]

    g = f[f"Geometry/2D Flow Areas/{area}"]
    res = f[f"{SUMMARY}/{area}"]
    cc = g["Cells Center Coordinate"][:]
    fp_idx = g["Cells FacePoint Indexes"][:]
    fp_xy = g["FacePoints Coordinate"][:]
    cmin = g["Cells Minimum Elevation"][:]
    face_cell = g["Faces Cell Indexes"][:]
    wse_max = res["Maximum Water Surface"][0, :]
    fvel = res["Maximum Face Velocity"][0, :]

    # 2. terrain and terrain-modification warning
    if a.terrain:
        terrain = a.terrain
    else:
        terrain = resolve_terrain(a.hdf, f, area)
    for w in terrain_mod_warnings(a.hdf, f, area, terrain, terrain_override=bool(a.terrain)):
        log(w)
        if w.startswith("WARN: the plan geometry") or "holds modifications" in w:
            if "TERRAIN_MODS_NOT_APPLIED" not in flags:
                flags.append("TERRAIN_MODS_NOT_APPLIED")
    f.close()
    if terrain is None:
        flags.append("BLOCKY_DEPTH_NO_TERRAIN")
    log(f"Terrain: {terrain if terrain else 'NONE -> cell min elevation (blocky depth)'}")

    ncell = cc.shape[0]
    wse_max = wse_max[:ncell]
    cellvel = cell_velocity(face_cell, fvel, ncell)

    work_crs = f"EPSG:{nat_epsg}"
    if a.clip:
        import geopandas as gpd
        clip = gpd.read_file(a.clip).to_crs(epsg=nat_epsg)
        clip_geom = clip.union_all() if hasattr(clip, "union_all") else clip.unary_union
        xmin, ymin, xmax, ymax = clip.total_bounds
    else:
        clip_geom = None
        # mesh extent from cell face points (v1 used cell centers and cut half a cell)
        used = np.unique(fp_idx[fp_idx >= 0])
        used = used[used < fp_xy.shape[0]]
        ext = fp_xy[used] if used.size else cc
        xmin, ymin = ext[:, 0].min(), ext[:, 1].min()
        xmax, ymax = ext[:, 0].max(), ext[:, 1].max()
    cs = a.cellsize
    xmin = np.floor(xmin / cs) * cs
    ymin = np.floor(ymin / cs) * cs
    xmax = np.ceil(xmax / cs) * cs
    ymax = np.ceil(ymax / cs) * cs
    ncol = int(round((xmax - xmin) / cs))
    nrow = int(round((ymax - ymin) / cs))
    transform = from_origin(xmin, ymax, cs, cs)
    log(f"Grid: {ncol} x {nrow} px @ {cs}")

    pad = max(cs * 5, 100.0)
    sel = ((cc[:, 0] >= xmin - pad) & (cc[:, 0] <= xmax + pad) &
           (cc[:, 1] >= ymin - pad) & (cc[:, 1] <= ymax + pad))
    shapes_wse, shapes_vel, shapes_zmin = [], [], []
    for i in np.nonzero(sel)[0]:
        pts = fp_idx[i]
        pts = pts[pts >= 0]
        if pts.size < 3 or not np.isfinite(wse_max[i]):
            continue
        xy = fp_xy[pts]
        cx, cy = xy[:, 0].mean(), xy[:, 1].mean()
        xy = xy[np.argsort(np.arctan2(xy[:, 1] - cy, xy[:, 0] - cx))]
        poly = Polygon(xy)
        if not poly.is_valid or poly.area == 0:
            continue
        shapes_wse.append((poly, float(wse_max[i])))
        shapes_vel.append((poly, float(cellvel[i])))
        shapes_zmin.append((poly, float(cmin[i])))
    log(f"Polygons: {len(shapes_wse)}")
    if not shapes_wse:
        log("ERROR: no mesh cells inside the grid window (check --clip CRS and extent)")
        return 1

    def burn(s):
        return rasterize(s, out_shape=(nrow, ncol), transform=transform,
                         fill=NODATA, dtype="float32")
    wse_all = burn(shapes_wse)
    vel_all = burn(shapes_vel)

    if terrain:
        terr = np.full((nrow, ncol), NODATA, "float32")
        with rasterio.open(terrain) as t:
            reproject(rasterio.band(t, 1), terr, src_transform=t.transform, src_crs=t.crs,
                      dst_transform=transform, dst_crs=work_crs,
                      resampling=Resampling.bilinear, src_nodata=t.nodata, dst_nodata=NODATA)
    else:
        terr = burn(shapes_zmin)

    depth = depth_from(wse_all, terr, a.wet)
    wet = depth != NODATA
    wse_out = np.where(wet, wse_all, NODATA).astype("float32")
    vel_out = np.where(wet, vel_all, NODATA).astype("float32")

    if clip_geom is not None:
        outside = geometry_mask([clip_geom], out_shape=(nrow, ncol), transform=transform, invert=False)
        for arr in (depth, wse_out, vel_out):
            arr[outside] = NODATA

    prof = dict(driver="GTiff", height=nrow, width=ncol, count=1, dtype="float32",
                crs=work_crs, transform=transform, nodata=NODATA,
                compress="lzw", tiled=True, blockxsize=256, blockysize=256)
    layers = {"depth": depth, "velocity": vel_out, "wse": wse_out}
    if a.terrain_out:
        layers_terr = np.where(terr != NODATA, terr, NODATA).astype("float32")
    tmp = tempfile.mkdtemp()
    written, rows = [], []
    now = datetime.datetime.now().strftime("%Y%m%d %H:%M")
    vol_pct = "" if (vol is None or vol["global_pct"] is None) else f"{vol['global_pct']:.4f}"
    for key, arr in layers.items():
        nm = (d43_name(a.scenario, a.event, key, cs) if a.naming == "d43"
              else plan_name(tag, key, cs))
        path = os.path.join(tmp, nm)
        with rasterio.open(path, "w", **prof) as dst:
            dst.write(arr, 1)
            dst.update_tags(tool=TOOL_TAG, plan=pinfo["plan_number"], plan_title=pinfo["plan_title"],
                            flags=";".join(flags), volume_error_pct=vol_pct)
        final_local = path
        if tgt_epsg != nat_epsg:
            wpath = os.path.join(tmp, nm.replace(".tif", f"_epsg{tgt_epsg}.tif"))
            with rasterio.open(path) as src:
                dt, dw, dh = calculate_default_transform(src.crs, f"EPSG:{tgt_epsg}",
                                                         src.width, src.height, *src.bounds)
                kw = src.meta.copy()
                kw.update(crs=f"EPSG:{tgt_epsg}", transform=dt, width=dw, height=dh)
                with rasterio.open(wpath, "w", **kw) as dst:
                    reproject(rasterio.band(src, 1), rasterio.band(dst, 1),
                              resampling=Resampling.bilinear)
            final_local = wpath
        dest = os.path.join(a.outdir, os.path.basename(final_local))
        _copy_out(final_local, dest)
        with rasterio.open(dest) as chk:
            v = chk.read(1)
            vv = v[v != NODATA]
            if vv.size:
                log(f"WROTE {os.path.basename(dest):45s} valid={vv.size:>8d} "
                    f"min={vv.min():.3f} max={vv.max():.3f} mean={vv.mean():.3f}")
            else:
                log(f"WROTE {os.path.basename(dest):45s} valid=0 (no wet cells)")
        written.append(dest)
        rows.append(dict(file=os.path.basename(dest), folder="", scenario=a.scenario or "",
                         event=a.event or "", variable=VARIABLES[key][0], units=VARIABLES[key][1],
                         cellsize_ft=fmt_cell(cs).replace("p", "."),
                         plan_number=pinfo["plan_number"], plan_title=pinfo["plan_title"],
                         plan_hdf=os.path.basename(a.hdf),
                         terrain=os.path.basename(terrain) if terrain else "cell-min-elevation",
                         tool=TOOL_TAG, volume_error_pct=vol_pct, volume_limit_pct=limit,
                         flags=";".join(flags), created=now))
    if a.terrain_out:
        tname = (f"{clean_token(a.scenario)}_Terrain_ft_{fmt_cell(cs)}ft.tif" if a.naming == "d43"
                 else f"{tag}_Terrain_ft_{int(round(cs))}ft.tif")
        tpath = os.path.join(a.outdir, tname)
        with rasterio.open(tpath, "w", **prof) as dst:
            dst.write(layers_terr, 1)
        written.append(tpath)
        rows.append(dict(file=tname, scenario=a.scenario or "", event="", variable="Terrain",
                         units="ft", cellsize_ft=fmt_cell(cs).replace("p", "."),
                         plan_number=pinfo["plan_number"], plan_title=pinfo["plan_title"],
                         plan_hdf=os.path.basename(a.hdf),
                         terrain=os.path.basename(terrain) if terrain else "cell-min-elevation",
                         tool=TOOL_TAG, flags=";".join(flags), created=now))
        log(f"WROTE {tname} (terrain used for depth)")
    shutil.rmtree(tmp, ignore_errors=True)
    dpath = append_dictionary(a.outdir, rows)
    log(f"Dictionary: {dpath}")

    # spot-check template for the mandatory RAS Mapper comparison (D57)
    pts = spot_points(depth, transform, n=10)
    stem = (f"{clean_token(a.scenario)}_{clean_token(a.event)}" if a.naming == "d43" else tag)
    spath = os.path.join(a.outdir, f"spotcheck_{stem}.csv")
    with open(spath, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["pt", "x", "y", "script_depth_ft", "script_wse_ft", "script_vel_fps",
                    "rasmapper_depth_ft", "rasmapper_wse_ft", "rasmapper_vel_fps", "note"])
        for k, (r, c, x, y) in enumerate(pts, 1):
            w.writerow([k, f"{x:.2f}", f"{y:.2f}", f"{depth[r, c]:.3f}", f"{wse_out[r, c]:.3f}",
                        f"{vel_out[r, c]:.3f}", "", "", "", ""])
    log(f"Spot-check sheet: {spath}  (fill RAS Mapper values for the same plan and terrain; required)")
    if flags:
        log("FLAGS: " + ";".join(flags))
    log("DONE: " + "; ".join(os.path.basename(w) for w in written))
    return 0


# ------------------------------------------------------------- difference ---
def run_diff(a):
    import rasterio
    var = a.variable
    if var not in VARIABLES:
        log("ERROR: --variable must be depth, wse or velocity")
        return 1
    with rasterio.open(a.diff_base) as b, rasterio.open(a.diff_new) as n:
        if (b.crs != n.crs or b.transform != n.transform or b.shape != n.shape):
            log("ERROR: base and new rasters differ in CRS, grid or extent; export both on the same "
                "grid (same --clip and --cellsize) first.")
            return 1
        base = b.read(1)
        new = n.read(1)
        bnd = b.nodata if b.nodata is not None else NODATA
        nnd = n.nodata if n.nodata is not None else NODATA
        base = np.where(base == bnd, NODATA, base).astype("float32")
        new = np.where(new == nnd, NODATA, new).astype("float32")
        prof = b.profile.copy()
        prof.update(nodata=NODATA, dtype="float32")
        cs = abs(b.transform.a)
    d = difference(new, base, var)
    pb, pn = parse_d43(a.diff_base), parse_d43(a.diff_new)
    base_scn = a.base_scenario or (pb["scenario"] if pb else "BASE")
    new_scn = a.new_scenario or (pn["scenario"] if pn else "NEW")
    event = a.event or (pn["event"] if pn else (pb["event"] if pb else "event"))
    outdir = os.path.join(a.outdir, "Differences")
    os.makedirs(outdir, exist_ok=True)
    nm = diff_name(new_scn, base_scn, event, var, cs)
    dest = os.path.join(outdir, nm)
    rule = ("WSE difference only where both scenarios are wet" if var == "wse"
            else "dry cells counted as 0")
    with rasterio.open(dest, "w", **prof) as dst:
        dst.write(d, 1)
        dst.update_tags(tool=TOOL_TAG, sign=f"{new_scn} minus {base_scn}; positive = increase",
                        wet_dry_rule=rule, display_threshold_ft=str(a.display_threshold))
    vv = d[d != NODATA]
    over = int((vv >= a.display_threshold).sum()) if vv.size else 0
    log(f"WROTE Differences/{nm} valid={vv.size} "
        f"min={vv.min() if vv.size else 0:.3f} max={vv.max() if vv.size else 0:.3f} "
        f"cells >= +{a.display_threshold} ft: {over}")
    log(f"Sign: {new_scn} minus {base_scn} (positive = increase). Rule: {rule}. "
        f"Display threshold for exhibits: |d| < {a.display_threshold} ft hidden (data kept).")
    append_dictionary(a.outdir, [dict(
        file=nm, folder="Differences", scenario=f"{new_scn}-minus-{base_scn}", event=event,
        variable=f"{VARIABLES[var][0]} Difference", units=VARIABLES[var][1],
        cellsize_ft=fmt_cell(cs).replace("p", "."), plan_hdf="", terrain="",
        tool=TOOL_TAG, flags=rule,
        created=datetime.datetime.now().strftime("%Y%m%d %H:%M"))])
    return 0


# ------------------------------------------------------------------- CLI ---
def build_parser():
    ap = argparse.ArgumentParser(description="HEC-RAS 2D max result rasters (v%s)" % __version__)
    ap.add_argument("--hdf", help="plan results HDF (*.p##.hdf)")
    ap.add_argument("--clip", help="polygon shapefile/GeoPackage to clip to")
    ap.add_argument("--cellsize", type=float, default=10.0)
    ap.add_argument("--epsg", type=int, default=None, help="only for a non-native output CRS")
    ap.add_argument("--area", default=None, help="2D flow area name if more than one")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--naming", choices=["d43", "plan"], default="d43",
                    help="d43: <scenario>_<event>_<var>_<units>_<cell>ft.tif (default); "
                         "plan: legacy <tag>_MaxDepth_ft_<cell>ft.tif")
    ap.add_argument("--scenario", help="scenario token, e.g. EX, PR, PR-Mitigated")
    ap.add_argument("--event", help="event token, e.g. 100yr, 10yr, 500yr")
    ap.add_argument("--tag", default=None, help="legacy naming tag (default plan number, e.g. p14)")
    ap.add_argument("--terrain", help="terrain raster to use instead of the basename match "
                                      "(e.g. RAS Mapper export with modifications)")
    ap.add_argument("--terrain-out", action="store_true",
                    help="also write the terrain used for depth on the output grid")
    ap.add_argument("--wet", type=float, default=WET, help="data mask depth, ft (default 0.01)")
    ap.add_argument("--screening", action="store_true", help="screening run: volume limit 0.5 %%")
    ap.add_argument("--vol-max", type=float, default=None, help="override volume limit, percent")
    ap.add_argument("--vol-warn-only", action="store_true",
                    help="export even above the volume limit; outputs are flagged")
    ap.add_argument("--diff-base", help="difference mode: base raster (e.g. EX)")
    ap.add_argument("--diff-new", help="difference mode: new raster (e.g. PR)")
    ap.add_argument("--variable", default=None, help="difference mode: depth | wse | velocity")
    ap.add_argument("--base-scenario")
    ap.add_argument("--new-scenario")
    ap.add_argument("--display-threshold", type=float, default=DIFF_DISPLAY)
    ap.add_argument("--version", action="version", version=TOOL_TAG)
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    if a.diff_base or a.diff_new:
        if not (a.diff_base and a.diff_new and a.variable):
            log("ERROR: difference mode needs --diff-base, --diff-new and --variable")
            return 1
        return run_diff(a)
    if not a.hdf:
        log("ERROR: --hdf is required")
        return 1
    return export(a)


if __name__ == "__main__":
    sys.exit(main())
