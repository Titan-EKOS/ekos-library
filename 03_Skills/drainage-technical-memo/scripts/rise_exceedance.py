"""WSEL rise exceedance durations at common-wet 2D cells (crossing rise memo, RPT-C15).

Reads the cell water-surface time series of an existing and a proposed HEC-RAS plan HDF (same mesh), finds cells wet
in both (depth > wet threshold at any time), and reports for each rise threshold the number of common-wet cells that
exceed it and the maximum time above it. Native cell counts are reported as counts, never as raster areas.

Thresholds come from the governing agency or stakeholder for the project (D29); pass them with --thresholds.

Usage:
  python rise_exceedance.py --ex <existing.p01.hdf> --pr <proposed.p02.hdf> --area "<2D area name>" \
      --thresholds 0.1 0.5 1.0 [--wet 0.01] [--csv cells.csv] [--json summary.json]
Dataset paths default to the HEC-RAS 6.x layout; confirm with h5ls on the plan HDF and override with --wse-path,
--time-path and --minelev-path if the layout differs. Exit codes: 0 ok, 2 input error.
"""
import argparse
import csv
import json
import sys

import h5py
import numpy as np

TS = "/Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series"
WSE = TS + "/2D Flow Areas/{area}/Water Surface"
TIME = TS + "/Time"
MINEL = "/Geometry/2D Flow Areas/{area}/Cells Minimum Elevation"


def load(path, area, wse_path, time_path, minel_path):
    with h5py.File(path, "r") as h:
        wse = h[wse_path.format(area=area)][()]          # [time, cell]
        t_days = h[time_path][()]                          # days
        zmin = h[minel_path.format(area=area)][()]         # [cell]
    n = min(wse.shape[1], zmin.shape[0])                   # WSE may include face-point ghost cells at the end
    return wse[:, :n], np.asarray(t_days, dtype=float) * 24.0, zmin[:n]


def max_run_hours(mask, t_hours):
    """Longest continuous time (h) each column of mask stays True."""
    dt = np.diff(t_hours, prepend=t_hours[0])
    best = np.zeros(mask.shape[1])
    cur = np.zeros(mask.shape[1])
    for k in range(mask.shape[0]):
        cur = np.where(mask[k], cur + dt[k], 0.0)
        best = np.maximum(best, cur)
    return best


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ex", required=True)
    ap.add_argument("--pr", required=True)
    ap.add_argument("--area", required=True)
    ap.add_argument("--thresholds", type=float, nargs="+", required=True)
    ap.add_argument("--wet", type=float, default=0.01)
    ap.add_argument("--wse-path", default=WSE)
    ap.add_argument("--time-path", default=TIME)
    ap.add_argument("--minelev-path", default=MINEL)
    ap.add_argument("--csv")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    we, te, ze = load(a.ex, a.area, a.wse_path, a.time_path, a.minelev_path)
    wp, tp, zp = load(a.pr, a.area, a.wse_path, a.time_path, a.minelev_path)
    if we.shape != wp.shape or not np.allclose(te, tp):
        print(f"plans differ in mesh or output times: {we.shape} vs {wp.shape}; use a common mesh and output interval",
              file=sys.stderr)
        return 2
    de, dp = we - ze, wp - zp
    common = (np.nanmax(de, axis=0) > a.wet) & (np.nanmax(dp, axis=0) > a.wet)
    rise = np.where((de > a.wet) & (dp > a.wet), wp - we, np.nan)
    out = {"existing": a.ex, "proposed": a.pr, "area": a.area, "common_wet_cells": int(common.sum()),
           "max_rise_ft": float(np.nanmax(rise[:, common])) if common.any() else None, "thresholds": []}
    per_cell = {}
    for thr in a.thresholds:
        mask = np.nan_to_num(rise, nan=-1e9) > thr
        hrs = max_run_hours(mask, te)
        hrs[~common] = 0.0
        exceed = hrs > 0
        cell = int(np.argmax(hrs)) if exceed.any() else None
        out["thresholds"].append({"rise_ft": thr, "cells_exceeding": int(exceed.sum()),
                                  "max_hours_above": float(hrs.max()) if exceed.any() else 0.0,
                                  "cell_of_max": cell})
        per_cell[thr] = hrs
    out["note"] = "maxima for different thresholds can occur at different cells; counts are native cells, not areas"
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["cell", "max_rise_ft"] + [f"hours_above_{t}" for t in a.thresholds])
            mr = np.nanmax(np.nan_to_num(rise, nan=-1e9), axis=0)
            for c in np.where(common)[0]:
                w.writerow([int(c), round(float(mr[c]), 3)] + [round(float(per_cell[t][c]), 3) for t in a.thresholds])
    if a.json:
        with open(a.json, "w") as f:
            json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
