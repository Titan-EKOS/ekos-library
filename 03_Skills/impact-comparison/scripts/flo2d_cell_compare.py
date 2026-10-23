"""Cell-by-cell existing vs proposed comparison for matched FLO-2D models (HYD-C08). Environment: gis env (numpy).

  "%GIS_PY%" flo2d_cell_compare.py --base EX=<ex_folder>
      --scenario PR=<pr_folder> [--scenario ALT1=<alt_folder> ...] --threshold 0.10 --threshold-source "<agency, doc, section>"
      [--wet 0.1] [--fema] [--list-above 1.00] [--outdir <40_QC or 20_Working folder>]

Reads MAXWSELEV.OUT and DEPTH.OUT (override with --wse-file / --depth-file) and TOPO.DAT from each folder.
Stops if cell ids or XY differ between base and scenario (models must share one grid: CADPTS identical).
For each scenario writes <outdir>/<base>_vs_<name>_cells.csv (cells beyond threshold, new wet, new dry) and
merges a summary into <outdir>/impact_register.json (never overwrites other scenarios' entries).

dWSE = proposed max WSE - existing max WSE, on cells wet (depth >= --wet) in both conditions.
--threshold has no default (decision D29): cite the governing agency value with --threshold-source.
--fema (44 CFR 65.12 add-on): rises evaluated where max depth >= 1.0 ft in both conditions (SFHA) and
reported separately from any-depth counts; new SFHA cells (pr >= 1.0, ex < 1.0) and removed SFHA cells;
--list-above lists every cell above that rise with ground change and depth change.
Ground change = proposed TOPO - existing TOPO; cells with |ground change| > 0.1 ft are tagged so extreme
dWSE at fills and basins is reviewed before quoting.
"""
import argparse
import csv
import json
import os
import sys

import numpy as np


def find_ci(folder, name):
    for f in os.listdir(folder):
        if f.upper() == name.upper():
            return os.path.join(folder, f)
    raise FileNotFoundError(f"{name} not in {folder}")


def read_out(path):
    """Rows of 'cell x y value'. Returns ids, xy (n,2), values."""
    ids, xy, val = [], [], []
    for line in open(path, errors="replace"):
        t = line.split()
        if len(t) < 4:
            continue
        try:
            nums = [float(x) for x in t[:4]]
        except ValueError:
            continue
        ids.append(int(nums[0]))
        xy.append(nums[1:3])
        val.append(float(t[-1]))
    order = np.argsort(ids)
    return np.array(ids)[order], np.array(xy)[order], np.array(val)[order]


def read_topo(path):
    xy, z = [], []
    for line in open(path, errors="replace"):
        t = line.split()
        if len(t) < 3:
            continue
        try:
            a, b, c = float(t[0]), float(t[1]), float(t[2])
        except ValueError:
            continue
        xy.append((a, b))
        z.append(c)
    return np.array(xy), np.array(z)


def load(folder, a):
    ids, xy, wse = read_out(find_ci(folder, a.wse_file))
    ids2, xy2, dep = read_out(find_ci(folder, a.depth_file))
    if not (np.array_equal(ids, ids2) and np.allclose(xy, xy2)):
        raise SystemExit(f"{folder}: WSE and depth files do not share cells")
    topo = None
    try:
        txy, tz = read_topo(find_ci(folder, "TOPO.DAT"))
        if len(tz) == len(ids):
            topo = tz
    except FileNotFoundError:
        pass
    return {"ids": ids, "xy": xy, "wse": wse, "dep": dep, "topo": topo}


def compare(b, s, a):
    if not (np.array_equal(b["ids"], s["ids"]) and np.allclose(b["xy"], s["xy"], atol=1e-3)):
        raise SystemExit("STOP: grids differ (cell ids or XY). Build all conditions on one grid (CADPTS identical).")
    wet_b, wet_s = b["dep"] >= a.wet, s["dep"] >= a.wet
    both = wet_b & wet_s
    d = np.where(both, s["wse"] - b["wse"], np.nan)
    gchg = (s["topo"] - b["topo"]) if (b["topo"] is not None and s["topo"] is not None) else np.full(len(d), np.nan)
    summ = {"cells": int(len(d)), "wet_both": int(both.sum()),
            "new_wet": int((wet_s & ~wet_b).sum()), "new_dry": int((wet_b & ~wet_s).sum()),
            "threshold_ft": a.threshold, "threshold_source": a.threshold_source,
            "rise_cells_any_depth": int((d > a.threshold).sum()), "fall_cells_any_depth": int((d < -a.threshold).sum()),
            "max_rise_ft": round(float(np.nanmax(d)), 3) if both.any() else None,
            "max_fall_ft": round(float(np.nanmin(d)), 3) if both.any() else None,
            "rise_cells_with_ground_change": int(((d > a.threshold) & (np.abs(gchg) > 0.1)).sum())}
    rows = []
    sel = (np.abs(np.nan_to_num(d)) > a.threshold) | (wet_s & ~wet_b) | (wet_b & ~wet_s)
    if a.fema:
        sf_b, sf_s = b["dep"] >= 1.0, s["dep"] >= 1.0
        sfha = sf_b & sf_s
        summ.update({"fema_rise_cells_sfha": int((sfha & (d > a.threshold)).sum()),
                     "fema_new_sfha_cells": int((sf_s & ~sf_b).sum()),
                     "fema_removed_sfha_cells": int((sf_b & ~sf_s).sum())})
        if a.list_above is not None:
            summ["fema_cells_above_list"] = int((d > a.list_above).sum())
            sel |= np.nan_to_num(d) > a.list_above
    for i in np.where(sel)[0]:
        cls = "new wet" if wet_s[i] and not wet_b[i] else "new dry" if wet_b[i] and not wet_s[i] else "change"
        rows.append({"cell": int(b["ids"][i]), "x": b["xy"][i, 0], "y": b["xy"][i, 1], "class": cls,
                     "wse_ex": round(float(b["wse"][i]), 3), "wse_pr": round(float(s["wse"][i]), 3),
                     "dwse_ft": None if np.isnan(d[i]) else round(float(d[i]), 3),
                     "depth_ex": round(float(b["dep"][i]), 3), "depth_pr": round(float(s["dep"][i]), 3),
                     "depth_change_ft": round(float(s["dep"][i] - b["dep"][i]), 3),
                     "ground_change_ft": None if np.isnan(gchg[i]) else round(float(gchg[i]), 3),
                     "ownership_or_grading": ""})
    return summ, rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="NAME=folder")
    ap.add_argument("--scenario", action="append", required=True, help="NAME=folder (repeat; list all together)")
    ap.add_argument("--threshold", type=float, required=True)
    ap.add_argument("--threshold-source", required=True)
    ap.add_argument("--wet", type=float, default=0.1)
    ap.add_argument("--fema", action="store_true")
    ap.add_argument("--list-above", type=float)
    ap.add_argument("--wse-file", default="MAXWSELEV.OUT")
    ap.add_argument("--depth-file", default="DEPTH.OUT")
    ap.add_argument("--outdir", default=".")
    a = ap.parse_args(argv)
    bname, bfolder = a.base.split("=", 1)
    base = load(bfolder, a)
    os.makedirs(a.outdir, exist_ok=True)
    regp = os.path.join(a.outdir, "impact_register.json")
    reg = json.load(open(regp)) if os.path.exists(regp) else {}
    for sc in a.scenario:
        name, folder = sc.split("=", 1)
        summ, rows = compare(base, load(folder, a), a)
        summ.update({"base": f"{bname}={bfolder}", "scenario": f"{name}={folder}"})
        reg[f"{bname}_vs_{name}"] = summ
        cp = os.path.join(a.outdir, f"{bname}_vs_{name}_cells.csv")
        with open(cp, "w", newline="") as f:
            cols = ["cell", "x", "y", "class", "wse_ex", "wse_pr", "dwse_ft", "depth_ex", "depth_pr",
                    "depth_change_ft", "ground_change_ft", "ownership_or_grading"]
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(json.dumps({f"{bname}_vs_{name}": summ}))
    with open(regp, "w") as f:
        json.dump(reg, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
