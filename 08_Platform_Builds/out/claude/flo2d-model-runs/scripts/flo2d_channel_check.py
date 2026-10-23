"""FLO-2D natural-section 1D channel validity checks (HYD-C05). Pure Python.

  D:\\EKOS\\envs\\gis\\.venv\\Scripts\\python.exe flo2d_channel_check.py <model_folder> [--min-relief 0.5]

Reads XSEC.DAT, CHAN.DAT and CHANBANK.DAT (case-insensitive names) and writes
<model_folder>/channel_check.json. Exit 1 on any FAIL.

Assumed layouts (check against the build's Data Input Manual if a parse looks wrong):
  XSEC.DAT     'X <num> <name>' header, then 'station elevation' rows.
  CHAN.DAT     element rows start with N/R/T/V; token 2 = grid element; for N rows the last
               token = cross-section number. A segment = a contiguous block of element rows.
  CHANBANK.DAT 'channel_element bank_element' per row.

Checks
  FAIL  section numbers not consecutive from 1 / gaps / referenced but missing / used twice
  FAIL  section with >= 33 points; duplicate stations; thalweg at a section end point
  WARN  section with more than 25 points; relief (lower end minus thalweg) under --min-relief
  FAIL  bank cell that is also a channel element; grid element in more than one segment
  WARN  segment of 2 cells or less (stub reach)
"""
import argparse
import json
import os
import sys

ELEM_TAGS = {"N", "R", "T", "V"}


def find_ci(folder, name):
    for f in os.listdir(folder):
        if f.upper() == name.upper():
            return os.path.join(folder, f)
    return None


def parse_xsec(path):
    secs, cur = {}, None
    for line in open(path, errors="replace"):
        t = line.split()
        if not t:
            continue
        if t[0].upper() == "X" and len(t) >= 2:
            cur = int(float(t[1]))
            if cur in secs:
                secs[cur]["dup_header"] = True
            secs.setdefault(cur, {"pts": [], "name": " ".join(t[2:])})
        elif cur is not None:
            try:
                secs[cur]["pts"].append((float(t[0]), float(t[1])))
            except (ValueError, IndexError):
                pass
    return secs


def parse_chan(path):
    segments, cur, xs_refs = [], [], []
    for line in open(path, errors="replace"):
        t = line.split()
        if t and t[0].upper() in ELEM_TAGS and len(t) >= 2:
            try:
                cur.append(int(float(t[1])))
            except ValueError:
                continue
            if t[0].upper() == "N":
                try:
                    xs_refs.append(int(float(t[-1])))
                except ValueError:
                    pass
        else:
            if cur:
                segments.append(cur)
                cur = []
    if cur:
        segments.append(cur)
    return segments, xs_refs


def parse_bank(path):
    pairs = []
    for line in open(path, errors="replace"):
        t = line.split()
        if len(t) >= 2:
            try:
                pairs.append((int(float(t[0])), int(float(t[1]))))
            except ValueError:
                pass
    return pairs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--min-relief", type=float, default=0.5)
    a = ap.parse_args(argv)
    fails, warns = [], []

    xp = find_ci(a.folder, "XSEC.DAT")
    secs = parse_xsec(xp) if xp else {}
    if secs:
        nums = sorted(secs)
        if nums[0] != 1 or nums != list(range(1, len(nums) + 1)):
            gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
            fails.append({"check": "xsec numbering not consecutive from 1", "gaps": gaps[:50]})
        for n, s in secs.items():
            pts = s["pts"]
            if s.get("dup_header"):
                fails.append({"check": "xsec number defined twice", "xsec": n})
            if len(pts) >= 33:
                fails.append({"check": "xsec >= 33 points", "xsec": n, "points": len(pts)})
            elif len(pts) > 25:
                warns.append({"check": "xsec > 25 points (target 20-25)", "xsec": n, "points": len(pts)})
            stations = [p[0] for p in pts]
            if len(set(stations)) != len(stations):
                fails.append({"check": "duplicate stations", "xsec": n})
            if len(pts) >= 3:
                elev = [p[1] for p in pts]
                zmin = min(elev)
                imin = elev.index(zmin)
                if imin in (0, len(elev) - 1):
                    fails.append({"check": "thalweg at section end point", "xsec": n})
                relief = min(elev[0], elev[-1]) - zmin
                if relief < a.min_relief:
                    warns.append({"check": f"relief under {a.min_relief} ft", "xsec": n, "relief_ft": round(relief, 2)})
            else:
                fails.append({"check": "section with fewer than 3 points", "xsec": n})

    cp = find_ci(a.folder, "CHAN.DAT")
    segments, xs_refs = parse_chan(cp) if cp else ([], [])
    chan_cells = [c for s in segments for c in s]
    dup_cells = sorted({c for c in chan_cells if chan_cells.count(c) > 1})
    if dup_cells:
        fails.append({"check": "grid element in more than one segment / repeated", "cells": dup_cells[:50]})
    for i, s in enumerate(segments, 1):
        if len(s) <= 2:
            warns.append({"check": "stub reach (2 cells or less)", "segment": i, "cells": s})
    if xs_refs:
        dup_refs = sorted({x for x in xs_refs if xs_refs.count(x) > 1})
        if dup_refs:
            fails.append({"check": "xsec used by more than one channel element", "xsec": dup_refs[:50]})
        missing = sorted(set(xs_refs) - set(secs))
        if missing and secs:
            fails.append({"check": "xsec referenced in CHAN.DAT but not in XSEC.DAT", "xsec": missing[:50]})

    bp = find_ci(a.folder, "CHANBANK.DAT")
    if bp:
        cset = set(chan_cells)
        bad = [(c, b) for c, b in parse_bank(bp) if b != 0 and b in cset]
        if bad:
            fails.append({"check": "bank cell is a channel element", "pairs": bad[:50]})

    rep = {"folder": a.folder, "files": {"XSEC": bool(xp), "CHAN": bool(cp), "CHANBANK": bool(bp)},
           "n_sections": len(secs), "n_segments": len(segments), "fail": fails, "warn": warns,
           "pass": not fails}
    with open(os.path.join(a.folder, "channel_check.json"), "w") as f:
        json.dump(rep, f, indent=2)
    print(json.dumps({"pass": rep["pass"], "fails": len(fails), "warns": len(warns)}))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
