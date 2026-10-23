#!/usr/bin/env python3
"""
exhibit_kit.py  (scripted-exhibit-sheets v1.0.0)
================================================
Shared helpers for scripted exhibit sheets: one sheet template, the library
depth / difference ramps, the standing map checklist items (north arrow,
graphic scale bar, datum note, credit line, legend), empty-layer guards,
register-driven labels with callouts, never-overwrite versioned output, and
FLO-2D output readers for result mapping.

Import from a per-project exhibit script:
    import sys; sys.path.insert(0, r"<library>\\03_Skills\\scripted-exhibit-sheets\\scripts")
    import exhibit_kit as ek

Self-test (no project data needed):
    python exhibit_kit.py --selftest <outdir>

Only numpy and matplotlib are required. geopandas / rasterio are used by the
calling script for its layers; this module does not import them.
"""
import copy
import csv
import json
import math
import os
import re
import textwrap
import warnings

import numpy as np

__version__ = "1.0.0"

# ------------------------------------------------------------------ ramps ---
# D31 / D32 / D33. Bounds are continuous, upper bound exclusive.
# "hidden" classes are not drawn (display cutoff = bottom of the first shown class).
RAMPS = {
    "local": {
        "title": "Max Depth (ft), local classes",
        "bounds": [0.2, 0.5, 1.0, 2.0, 3.0, math.inf],
        "colors": ["#FFFF00", "#00FFFF", "#0050FF", "#FF8C00", "#FF0000"],
        "labels": ["0.2 - 0.5", "0.5 - 1.0", "1.0 - 2.0", "2.0 - 3.0", "> 3.0"],
    },
    "deep-flow": {  # colors default, to confirm
        "title": "Max Depth (ft), deep-flow classes",
        "bounds": [0.0, 3.0, 5.0, 10.0, math.inf],
        "colors": ["#FFFF00", "#0050FF", "#FF8C00", "#FF0000"],
        "labels": ["0 - 3", "3 - 5", "5 - 10", "> 10"],
    },
    "difference": {  # increases only; |d| < 0.10 ft hidden unless agency threshold differs
        "title": "WSE Increase (ft), proposed minus existing",
        "bounds": [0.10, 0.25, 0.50, 1.0, 2.0, math.inf],
        "colors": ["#00FFFF", "#00B050", "#0050FF", "#FF8C00", "#FF0000"],
        "labels": ["0.10 - 0.25", "0.25 - 0.50", "0.50 - 1.0", "1.0 - 2.0", "> 2.0"],
    },
}
RESULT_ALPHA = 0.60   # D40: raster 60 % over a full-strength aerial
MIN_TEXT_PT = 9.0     # D34: new text
SHEETS_IN = {"11x17": (17.0, 11.0), "8.5x11": (11.0, 8.5), "22x34": (34.0, 22.0), "30x42": (42.0, 30.0)}
ENG_SCALES = [10, 20, 30, 40, 50, 60, 100, 200, 300, 400, 500, 600, 1000, 2000, 2500, 5000, 10000]


def difference_ramp(threshold=0.10):
    """Difference ramp with an agency threshold other than 0.10 ft (D33)."""
    r = copy.deepcopy(RAMPS["difference"])
    if threshold < 0.10:
        r["bounds"] = [threshold] + r["bounds"]
        r["colors"] = ["#FFFF00"] + r["colors"]
        r["labels"] = [f"{threshold:.2f} - 0.10"] + r["labels"]
    elif threshold > 0.10:
        keep = [i for i, b in enumerate(r["bounds"][:-1]) if r["bounds"][i + 1] > threshold]
        r["bounds"] = [threshold] + [r["bounds"][i + 1] for i in keep]
        r["colors"] = [r["colors"][i] for i in keep]
        r["labels"] = [f"{threshold:.2f} - {r['bounds'][1]:g}"] + [r["labels"][i] for i in keep[1:]]
    return r


def classify(arr, ramp):
    """Class index per cell (0..n-1); -1 = hidden (below cutoff, NaN or nodata)."""
    r = RAMPS[ramp] if isinstance(ramp, str) else ramp
    a = np.asarray(arr, dtype=float)
    b = np.asarray(r["bounds"], dtype=float)
    out = np.full(a.shape, -1, dtype=int)
    ok = np.isfinite(a) & (a >= b[0])
    idx = np.searchsorted(b, a[ok], side="right") - 1   # upper bound exclusive
    out[ok] = np.clip(idx, 0, len(b) - 2)
    return out


def ramp_cmap(ramp):
    """(ListedColormap, BoundaryNorm) for imshow of classify() output."""
    from matplotlib.colors import ListedColormap, BoundaryNorm
    r = RAMPS[ramp] if isinstance(ramp, str) else ramp
    n = len(r["colors"])
    return ListedColormap(r["colors"]), BoundaryNorm(np.arange(-0.5, n + 0.5, 1), n)


def class_areas(arr, ramp, cell_area_sqft):
    """Acres per displayed class, for the report table (same breaks as the map)."""
    r = RAMPS[ramp] if isinstance(ramp, str) else ramp
    c = classify(arr, r)
    return {lab: float((c == i).sum() * cell_area_sqft / 43560.0) for i, lab in enumerate(r["labels"])}


# ---------------------------------------------------------- empty layers ---
class EmptyLayerError(RuntimeError):
    pass


def require_nonempty(layer, name, strict=True):
    """Stop (strict) or warn when a filtered layer is empty (EXH-C04).

    Returns True when the layer has features. A warning return means the legend
    entry must be dropped or replaced with "none mapped".
    """
    n = 0 if layer is None else (len(layer) if hasattr(layer, "__len__") else int(bool(layer)))
    if n == 0:
        msg = f"EMPTY LAYER: '{name}' has no features in the frame"
        if strict:
            raise EmptyLayerError(msg)
        warnings.warn(msg + "; drop its legend entry or state 'none mapped'")
        return False
    return True


# --------------------------------------------------------- sheet template ---
def engineering_scale(extent_ft, map_in):
    """Smallest engineering scale (ft per in) that fits extent_ft in map_in inches."""
    need = extent_ft / float(map_in)
    for s in ENG_SCALES:
        if s >= need:
            return s
    return int(math.ceil(need / 1000.0) * 1000)


def sheet(size="11x17", orientation="landscape", margin_in=0.5, title_h_in=1.1, legend_w_in=3.2):
    """Figure with the map frame, a right-margin legend panel and a bottom title block.

    Returns (fig, axes) with axes keys: map, legend, title.
    """
    import matplotlib.pyplot as plt
    w, h = SHEETS_IN[size]
    if orientation == "portrait":
        w, h = h, w
    fig = plt.figure(figsize=(w, h))
    m = margin_in
    ax_map = fig.add_axes([m / w, (m + title_h_in) / h, (w - 2 * m - legend_w_in) / w,
                           (h - 2 * m - title_h_in) / h])
    ax_leg = fig.add_axes([(w - m - legend_w_in) / w, (m + title_h_in) / h, legend_w_in / w,
                           (h - 2 * m - title_h_in) / h])
    ax_tb = fig.add_axes([m / w, m / h, (w - 2 * m) / w, title_h_in / h])
    for a in (ax_leg, ax_tb):
        a.set_xticks([]); a.set_yticks([])
    ax_map.set_xticks([]); ax_map.set_yticks([])
    ax_map.set_aspect("equal")
    fig._ek = {"size": size, "orientation": orientation, "w": w, "h": h}
    return fig, {"map": ax_map, "legend": ax_leg, "title": ax_tb}


def set_extent_to_scale(ax, cx, cy, scale_ft_per_in):
    """Set map limits so the plotted sheet reads at exactly 1 in = scale ft.

    Call AFTER all layers are drawn (imshow and plot reset the limits), then check
    measured_scale(ax) == scale before saving.
    """
    fig = ax.figure
    bb = ax.get_position(original=True)
    w_in = bb.width * fig.get_figwidth()
    h_in = bb.height * fig.get_figheight()
    hw, hh = w_in * scale_ft_per_in / 2.0, h_in * scale_ft_per_in / 2.0
    ax.set_xlim(cx - hw, cx + hw)
    ax.set_ylim(cy - hh, cy + hh)
    return w_in, h_in


def measured_scale(ax):
    """ft per plotted inch, from the axis limits (QC: must equal the stated scale)."""
    fig = ax.figure
    bb = ax.get_position(original=True)
    w_in = bb.width * fig.get_figwidth()
    x0, x1 = ax.get_xlim()
    return (x1 - x0) / w_in


def north_arrow(ax, x=0.5, y=0.93, size=0.06, rotation_deg=0.0):
    """North arrow in axes-fraction coordinates; rotate the arrow, never the layout."""
    t = math.radians(rotation_deg)
    dx, dy = -math.sin(t) * size, math.cos(t) * size
    ax.annotate("", xy=(x + dx / 2, y + dy / 2), xytext=(x - dx / 2, y - dy / 2),
                xycoords="axes fraction", arrowprops=dict(arrowstyle="-|>", lw=2, color="k"))
    ax.text(x + dx * 0.75, y + dy * 0.75, "N", transform=ax.transAxes, ha="center", va="center",
            fontsize=12, fontweight="bold")


def scale_bar(ax, scale_ft_per_in, x=0.08, y=0.25, inches=2.0, fontsize=MIN_TEXT_PT):
    """Graphic scale bar drawn in the legend/margin axes, `inches` long at the stated scale."""
    from matplotlib.patches import Rectangle
    fig = ax.figure
    bb = ax.get_position()
    frac = inches / (bb.width * fig.get_figwidth())
    n = 4
    for i in range(n):
        ax.add_patch(Rectangle(
            (x + i * frac / n, y), frac / n, 0.008, transform=ax.transAxes,
            facecolor="k" if i % 2 == 0 else "w", edgecolor="k", lw=0.8))
    for i in (0, n // 2, n):
        ax.text(x + i * frac / n, y - 0.012, f"{int(i * scale_ft_per_in * inches / n)}",
                transform=ax.transAxes, ha="center", va="top", fontsize=fontsize)
    ax.text(x + frac / 2, y + 0.018, f"SCALE: 1 in = {scale_ft_per_in:g} ft (feet)",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=fontsize)
    return frac


def datum_note(ax, horizontal, vertical, crs_note="", y=0.15, fontsize=MIN_TEXT_PT, width=42):
    lines = [f"HORIZONTAL DATUM: {horizontal}", f"VERTICAL DATUM: {vertical}"]
    if crs_note:
        lines.append(crs_note)
    txt = "\n".join(textwrap.fill(t, width) for t in lines)
    ax.text(0.05, y, txt, transform=ax.transAxes, ha="left", va="top", fontsize=fontsize)


def credit_line(ax, text, y=0.04, fontsize=MIN_TEXT_PT):
    ax.text(0.05, y, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=fontsize,
            wrap=True)


def title_block(ax, fig_id, title, project_no, scale_text, storm="", condition="",
                firm="PSOMAS", drawn="JCO", checked="", source=""):
    """Bottom title block. No dates (a date in every title block forces replotting the set)."""
    ax.axvline(0.70, color="k", lw=0.8)
    ax.axvline(0.85, color="k", lw=0.8)
    sub = " | ".join(s for s in (condition, storm) if s)
    ax.text(0.01, 0.62, title.upper(), fontsize=16, fontweight="bold", va="center")
    if sub:
        ax.text(0.01, 0.25, sub, fontsize=11, va="center")
    ax.text(0.715, 0.70, firm, fontsize=14, fontweight="bold", va="center", color="#0C3350")
    ax.text(0.715, 0.35, f"Project No. {project_no}\nDrawn: {drawn}  Checked: {checked}",
            fontsize=MIN_TEXT_PT, va="center")
    ax.text(0.925, 0.62, fig_id, fontsize=18, fontweight="bold", ha="center", va="center")
    ax.text(0.925, 0.25, scale_text, fontsize=MIN_TEXT_PT, ha="center", va="center")
    if source:
        ax.text(0.01, 0.05, f"Source: {source}", fontsize=7.5, va="bottom", color="#555555")


def legend_patches(ax, entries, title="LEGEND", y0=0.97, fontsize=MIN_TEXT_PT):
    """Legend with graphic samples. entries: list of dict(kind=fill|line|marker, label, **style).

    Only pass entries for symbols present on the sheet (EXH-C04).
    """
    from matplotlib.patches import Rectangle
    from matplotlib.lines import Line2D
    ax.text(0.05, y0, title, transform=ax.transAxes, fontsize=fontsize + 2, fontweight="bold",
            va="top")
    y = y0 - 0.045
    for e in entries:
        k = e.get("kind", "fill")
        if k == "fill":
            ax.add_patch(Rectangle((0.05, y - 0.012), 0.12, 0.022, transform=ax.transAxes,
                                   facecolor=e.get("color", "none"), edgecolor=e.get("edge", "k"),
                                   alpha=e.get("alpha", 1.0), hatch=e.get("hatch"), lw=0.6))
        elif k == "line":
            ax.add_line(Line2D([0.05, 0.17], [y, y], transform=ax.transAxes, color=e.get("color", "k"),
                               lw=e.get("lw", 1.5), ls=e.get("ls", "-")))
        else:
            ax.plot([0.11], [y], transform=ax.transAxes, marker=e.get("marker", "o"),
                    color=e.get("color", "k"), ms=e.get("ms", 7), ls="none")
        ax.text(0.21, y, e["label"], transform=ax.transAxes, va="center", fontsize=fontsize)
        y -= 0.04
    return y


def ramp_legend_entries(ramp, alpha=RESULT_ALPHA):
    r = RAMPS[ramp] if isinstance(ramp, str) else ramp
    return [dict(kind="fill", color=c, alpha=alpha, label=lab) for c, lab in zip(r["colors"], r["labels"])]


# ------------------------------------------------- labels from a register ---
def load_register(path, key="id"):
    """Read a register CSV (inflow register, storage register, CP table) keyed by `key`."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    reg = {}
    for r in rows:
        k = r.get(key, "").strip()
        if not k:
            continue
        if k in reg:
            raise ValueError(f"duplicate register key {k} in {path}")
        reg[k] = r
    return reg


def compare_register(register, report_rows, key, fields, tol=0.0):
    """Every exhibit value must match the report table (EXH-C11). Returns list of mismatches."""
    bad = []
    rep = {r[key]: r for r in report_rows}
    for k, r in register.items():
        if k not in rep:
            bad.append((k, "<missing in report table>", "", ""))
            continue
        for fld in fields:
            a, b = r.get(fld, ""), rep[k].get(fld, "")
            try:
                if abs(float(a) - float(b)) > tol:
                    bad.append((k, fld, a, b))
            except ValueError:
                if str(a).strip() != str(b).strip():
                    bad.append((k, fld, a, b))
    return bad


def callouts(ax, pts, labels, min_sep_ft=None, offset_ft=None, fontsize=MIN_TEXT_PT, box=True):
    """Place labels with leader lines, staggering offsets so labels keep a minimum spacing.

    pts: list of (x, y) in map units. Returns list of label positions.
    """
    x0, x1 = ax.get_xlim()
    span = x1 - x0
    off = offset_ft or span * 0.04
    sep = min_sep_ft or span * 0.03
    dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1.4), (0, -1.4), (1.4, 0), (-1.4, 0)]
    placed = []
    for (x, y), lab in zip(pts, labels):
        best = None
        for ring in (1, 2, 3):
            for dx, dy in dirs:
                cx, cy = x + dx * off * ring, y + dy * off * ring
                if all(math.hypot(cx - px, cy - py) >= sep for px, py in placed):
                    best = (cx, cy)
                    break
            if best:
                break
        best = best or (x + off, y + off)
        placed.append(best)
        ax.annotate(lab, xy=(x, y), xytext=best, fontsize=fontsize, ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color="k"),
                    bbox=dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.5) if box else None)
    return placed


# ---------------------------------------------------------------- output ---
def next_version_path(folder, stem, ext=".pdf"):
    """<stem>_v1.pdf, _v2 ... ; never overwrites an existing file."""
    os.makedirs(folder, exist_ok=True)
    pat = re.compile(re.escape(stem) + r"_v(\d+)" + re.escape(ext) + "$", re.I)
    vs = [int(m.group(1)) for f in os.listdir(folder) for m in [pat.match(f)] if m]
    return os.path.join(folder, f"{stem}_v{(max(vs) + 1) if vs else 1}{ext}")


def save_sheet(fig, folder, stem, meta, dpi=200):
    """Write PDF + PNG (margins visible in both) + the source/extent JSON for the sheet."""
    pdf = next_version_path(folder, stem, ".pdf")
    ver = re.search(r"_v(\d+)\.pdf$", pdf).group(1)
    png = pdf[:-4] + ".png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=dpi)
    meta = dict(meta, version=f"v{ver}", pdf=os.path.basename(pdf), png=os.path.basename(png),
                kit=f"exhibit_kit {__version__}")
    with open(pdf[:-4] + ".json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, default=str)
    return pdf, png


# ------------------------------------------------------ FLO-2D readers ---
def read_flo2d_xyz(path, value_col=-1):
    """Read TOPO.DAT / DEPTH.OUT / MAXWSELEV.OUT style text.

    3 numeric columns -> x, y, value; 4+ -> grid, x, y, value (value_col picks the column).
    Returns dict(grid, x, y, v) as numpy arrays (grid = 1..n when absent).
    """
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            parts = line.split()
            try:
                nums = [float(p) for p in parts]
            except ValueError:
                continue
            if len(nums) >= 3:
                rows.append(nums)
    if not rows:
        raise ValueError(f"no numeric rows in {path}")
    ncol = min(len(r) for r in rows)
    a = np.array([r[:ncol] for r in rows])
    if ncol == 3:
        return dict(grid=np.arange(1, len(a) + 1), x=a[:, 0], y=a[:, 1], v=a[:, 2])
    return dict(grid=a[:, 0].astype(int), x=a[:, 1], y=a[:, 2], v=a[:, value_col])


def assert_cells_match(*sets, tol=0.01):
    """Cell coordinates of TOPO / DEPTH / MAXWSELEV must agree (EXH-C09)."""
    ref = sets[0]
    for s in sets[1:]:
        if len(s["x"]) != len(ref["x"]):
            raise ValueError(f"cell count differs: {len(ref['x'])} vs {len(s['x'])}")
        dx = np.max(np.abs(s["x"] - ref["x"]))
        dy = np.max(np.abs(s["y"] - ref["y"]))
        if dx > tol or dy > tol:
            raise ValueError(f"cell coordinates differ (max dx {dx:.3f}, dy {dy:.3f})")
    return True


def grid_cells(x, y, v, cellsize, bounds=None, nodata=np.nan):
    """Grid FLO-2D cell values on the model cell size. bounds=(xmin,ymin,xmax,ymax) from a
    correctly tagged reference raster when available. Returns (array, (xmin, ymax, cellsize))."""
    if bounds is None:
        xmin, ymin = x.min() - cellsize / 2, y.min() - cellsize / 2
        xmax, ymax = x.max() + cellsize / 2, y.max() + cellsize / 2
    else:
        xmin, ymin, xmax, ymax = bounds
    ncol = int(round((xmax - xmin) / cellsize))
    nrow = int(round((ymax - ymin) / cellsize))
    arr = np.full((nrow, ncol), nodata, dtype=float)
    c = np.floor((x - xmin) / cellsize).astype(int)
    r = np.floor((ymax - y) / cellsize).astype(int)
    ok = (c >= 0) & (c < ncol) & (r >= 0) & (r < nrow)
    arr[r[ok], c[ok]] = v[ok]
    return arr, (xmin, ymax, cellsize)


def flo2d_wet_masks(depth, wse, display_cutoff):
    """Dry cells have WSE coded 0; hide depths below the display cutoff (ramp bottom)."""
    wet = np.isfinite(wse) & (wse != 0) & np.isfinite(depth) & (depth > 0)
    shown = wet & (depth >= display_cutoff)
    return wet, shown


def wse_residuals(topo, depth, wse, wet):
    """WSE - terrain - depth on wet cells only (dry zero cells give false residuals)."""
    res = np.full(np.shape(depth), np.nan)
    res[wet] = wse[wet] - topo[wet] - depth[wet]
    return res


def same_array_different_crs(a, b, crs_a, crs_b):
    """Flag supplied 'twin' rasters: identical arrays with different CRS tags (EXH-C09)."""
    a, b = np.asarray(a), np.asarray(b)
    same = a.shape == b.shape and np.allclose(a, b, equal_nan=True)
    return bool(same and str(crs_a) != str(crs_b))


# Depth-to-zone table of the source case (STARVALLEY-009). Always replace with the
# effective study's table for the reach; never reuse across studies unchecked.
ZONE_TABLE_SOURCE_CASE = [(0.0, 1.0, "X"), (1.0, 1.5, "AO(1)"), (1.5, 2.5, "AO(2)"),
                          (2.5, 3.0, "AO(3)"), (3.0, math.inf, "AE")]


def depth_to_zone(depth, table, ae_mask=None):
    """Zone label per cell from a depth table; ae_mask (channels, connected corridor, basins) forces AE."""
    d = np.asarray(depth, dtype=float)
    z = np.full(d.shape, "", dtype=object)
    for lo, hi, lab in table:
        z[np.isfinite(d) & (d >= lo) & (d < hi)] = lab
    if ae_mask is not None:
        z[np.asarray(ae_mask, bool)] = "AE"
    return z


# --------------------------------------------------------------- selftest ---
def _selftest(outdir):
    import matplotlib
    matplotlib.use("Agg")
    os.makedirs(outdir, exist_ok=True)
    d = np.array([0.0, 0.1, 0.2, 0.49, 0.5, 1.0, 2.99, 3.0, 12.0, np.nan])
    c = classify(d, "local")
    assert c.tolist() == [-1, -1, 0, 0, 1, 2, 3, 4, 4, -1], c
    assert classify([2.9, 3.0, 10.0], "deep-flow").tolist() == [0, 1, 3]
    assert classify([0.05, 0.10, -0.5], "difference").tolist() == [-1, 0, -1]
    assert difference_ramp(0.05)["bounds"][0] == 0.05
    assert engineering_scale(3000, 12.0) == 300
    try:
        require_nonempty([], "BC lines")
        raise AssertionError("empty layer not caught")
    except EmptyLayerError:
        pass
    # FLO-2D synthetic: 10 x 10 cells of 100 ft
    xs, ys = np.meshgrid(np.arange(10) * 100.0 + 50, np.arange(10) * 100.0 + 50)
    x, y = xs.ravel(), ys.ravel()
    topo = 100 + 0.01 * x
    depth = np.clip(1.5 - 0.002 * x, 0, None)
    wse = np.where(depth > 0, topo + depth, 0.0)
    T = dict(grid=np.arange(1, 101), x=x, y=y, v=topo)
    D = dict(T, v=depth)
    W = dict(T, v=wse)
    assert_cells_match(T, D, W)
    gd, tr = grid_cells(x, y, depth, 100.0)
    gt, _ = grid_cells(x, y, topo, 100.0)
    gw, _ = grid_cells(x, y, wse, 100.0)
    wet, shown = flo2d_wet_masks(gd, gw, 0.2)
    res = wse_residuals(gt, gd, gw, wet)
    assert np.nanmax(np.abs(res)) < 1e-9
    z = depth_to_zone(gd, ZONE_TABLE_SOURCE_CASE)
    assert set(z[wet].tolist()) <= {"X", "AO(1)"}
    assert same_array_different_crs(gd, gd.copy(), "EPSG:3498", "EPSG:2223")
    # sample sheet
    fig, ax = sheet("11x17")
    scale = engineering_scale(1000, ax["map"].get_position().height * fig.get_figheight())
    cmap, norm = ramp_cmap("local")
    cls = classify(gd, "local").astype(float)
    cls[cls < 0] = np.nan
    ax["map"].imshow(cls, extent=(0, 1000, 0, 1000), cmap=cmap, norm=norm, alpha=RESULT_ALPHA,
                     interpolation="nearest")
    callouts(ax["map"], [(150, 150), (160, 170), (800, 800)], ["A\nQ100 = 45 cfs", "B\nQ100 = 12 cfs",
                                                                "C\nQ100 = 3 cfs"])
    set_extent_to_scale(ax["map"], 500, 500, scale)   # after drawing layers
    assert abs(measured_scale(ax["map"]) - scale) < 1e-6
    y = legend_patches(ax["legend"], ramp_legend_entries("local") +
                       [dict(kind="line", color="#E6007E", lw=3, label="Watershed boundary"),
                        dict(kind="line", color="#00B7EB", lw=1.5, ls="--", label="Flowline")],
                       title="LEGEND - " + RAMPS["local"]["title"])
    north_arrow(ax["legend"], y=0.30)
    scale_bar(ax["legend"], scale, y=0.22)
    datum_note(ax["legend"], "NAD83(HARN) Arizona Central, intl ft (EPSG:2868)", "NAVD88")
    credit_line(ax["legend"], "Aerial: (source, year). Model: synthetic test.")
    title_block(ax["title"], "Figure 4-1", "Existing Conditions 100-Year Max Depth", "0000.00",
                f"1 in = {scale} ft", storm="100-Year", condition="Existing")
    pdf, png = save_sheet(fig, outdir, "F4-1_EX_100yr_Depth", dict(fig_id="Figure 4-1", ramp="local",
                                                                   scale=scale))
    print("selftest ok:", pdf, png)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--selftest":
        _selftest(sys.argv[2])
    else:
        print(__doc__)
