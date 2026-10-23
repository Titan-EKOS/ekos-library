#!/usr/bin/env python3
"""
check_hms_results.py - judge a headless HEC-HMS compute by its files, not its console.

For each run name it checks:
  1. results\\RUN_<name>.results exists (spaces tried as-is and as underscores);
  2. the results file is newer than every model input (.hms .basin .met .control
     .gage .run .pdata .grid and any --input-dss files) -> otherwise STALE;
  3. element count in the results is not below --min-elements (if given);
  4. the run log (<name>.log, RUN_<name>.log or the project .log) has no ERROR lines;
     ERROR codes are listed (e.g. 23430 missing basin depths, 40253 stage above
     storage curve); unit hydrograph volume notes other than 1.0000 are flagged;
  5. optional --status file from make_hms_run_script.py: any FAILED run is reported.

Writes <out>_peaks.csv (run, element, statistic, value, units) and <out>_check.json.
Exit code 0 = all runs pass, 1 = at least one run failed a check.

The results XML layout is read tolerantly: any element carrying a name attribute
that holds Statistic* children with a type/name and a value attribute is recorded.
Confirm the parsed statistics against one run opened in the HMS GUI the first
time this is used on a new HMS build.

Usage:
  python check_hms_results.py --project-dir <dir with .hms> --runs "EX 100yr 3hr" ^
      --status <out_dir>\\compute_status.txt --input-dss <inflows.dss> --out <out_dir>\\check
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

INPUT_EXT = (".hms", ".basin", ".met", ".control", ".gage", ".run", ".pdata", ".grid", ".sqlite")
ERR_RE = re.compile(r"\bERROR\b\s*(\d+)?[:\s]*(.*)", re.IGNORECASE)
UH_RE = re.compile(r"unit hydrograph volume[^0-9]*([0-9.]+)", re.IGNORECASE)


def find_results(project_dir, run):
    cands = []
    for nm in {run, run.replace(" ", "_")}:
        cands.append(os.path.join(project_dir, "results", "RUN_" + nm + ".results"))
    for c in cands:
        if os.path.exists(c):
            return c
    hits = glob.glob(os.path.join(project_dir, "results", "*.results"))
    key = re.sub(r"[^a-z0-9]", "", run.lower())
    for h in hits:
        if re.sub(r"[^a-z0-9]", "", os.path.basename(h).lower()).endswith(key + "results"):
            return h
    return None


def parse_results(path):
    """Return list of (element, statistic, value, units)."""
    out = []
    tree = ET.parse(path)

    def walk(node, owner):
        name = node.attrib.get("name")
        tag = node.tag.split("}")[-1]
        if name and "statistic" not in tag.lower():
            owner = name
        if "statistic" in tag.lower():
            stype = node.attrib.get("type") or node.attrib.get("name")
            val = node.attrib.get("value")
            if stype and val is not None:
                out.append((owner or "", stype, val, node.attrib.get("units", "")))
        for ch in node:
            walk(ch, owner)

    walk(tree.getroot(), None)
    return out


def newest_input(project_dir, extra):
    newest, which = 0.0, None
    for fn in os.listdir(project_dir):
        if fn.lower().endswith(INPUT_EXT):
            t = os.path.getmtime(os.path.join(project_dir, fn))
            if t > newest:
                newest, which = t, fn
    for p in extra or []:
        if os.path.exists(p) and os.path.getmtime(p) > newest:
            newest, which = os.path.getmtime(p), p
    return newest, which


def scan_log(project_dir, run):
    names = [run + ".log", run.replace(" ", "_") + ".log", "RUN_" + run.replace(" ", "_") + ".log"]
    logs = [os.path.join(project_dir, n) for n in names]
    logs += [os.path.join(project_dir, "results", n) for n in names]
    errors, uh = [], []
    used = None
    for lp in logs:
        if os.path.exists(lp):
            used = lp
            with open(lp, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    m = ERR_RE.search(line)
                    if m and "premature end of file" not in line.lower():
                        errors.append(line.strip()[:300])
                    u = UH_RE.search(line)
                    if u:
                        uh.append(u.group(1))
            break
    return used, errors, uh


def read_status(path):
    res = {}
    if path and os.path.exists(path):
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh.read().splitlines()[1:]:
                parts = line.split("|")
                if len(parts) >= 2:
                    res[parts[0]] = (parts[1], parts[3] if len(parts) > 3 else "")
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-dir", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--runs", nargs="+")
    g.add_argument("--runs-file")
    ap.add_argument("--status", help="status file written by the generated Jython script")
    ap.add_argument("--input-dss", nargs="*", default=[], help="external inflow DSS files (count as inputs)")
    ap.add_argument("--min-elements", type=int, default=0)
    ap.add_argument("--out", required=True, help="output stem")
    a = ap.parse_args()

    runs = a.runs
    if a.runs_file:
        with open(a.runs_file, encoding="utf-8") as fh:
            runs = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]

    t_in, in_file = newest_input(a.project_dir, a.input_dss)
    status = read_status(a.status)
    rows, report, ok_all = [], [], True
    for run in runs:
        r = {"run": run, "problems": []}
        st = status.get(run)
        if st and st[0] != "COMPUTED":
            r["problems"].append("status " + st[0] + " " + st[1])
        res = find_results(a.project_dir, run)
        r["results_file"] = res
        if not res:
            r["problems"].append("no results file")
        else:
            if os.path.getmtime(res) < t_in:
                r["problems"].append("STALE: results older than input %s" % in_file)
            try:
                stats = parse_results(res)
            except ET.ParseError as e:
                stats = []
                r["problems"].append("results XML unreadable: %s" % e)
            elems = sorted({s[0] for s in stats})
            r["elements"] = len(elems)
            if a.min_elements and len(elems) < a.min_elements:
                r["problems"].append("only %d elements (expected >= %d)" % (len(elems), a.min_elements))
            if not stats:
                r["problems"].append("no statistics parsed")
            for s in stats:
                rows.append([run] + list(s))
        log, errs, uh = scan_log(a.project_dir, run)
        r["log"] = log
        r["log_errors"] = errs
        bad_uh = [v for v in uh if abs(float(v) - 1.0) > 0.00005] if uh else []
        r["uh_volume_notes"] = uh
        if errs:
            r["problems"].append("%d ERROR lines in log" % len(errs))
        if bad_uh:
            r["problems"].append("unit hydrograph volume not 1.0000: " + ", ".join(bad_uh))
        r["pass"] = not r["problems"]
        ok_all = ok_all and r["pass"]
        report.append(r)
        print(("PASS " if r["pass"] else "FAIL ") + run + ("" if r["pass"] else "  -> " + "; ".join(r["problems"])))

    with open(a.out + "_peaks.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["run", "element", "statistic", "value", "units"])
        w.writerows(rows)
    with open(a.out + "_check.json", "w", encoding="utf-8") as fh:
        json.dump({"newest_input": in_file, "runs": report, "all_pass": ok_all}, fh, indent=1)
    print("WROTE", a.out + "_peaks.csv", "and", a.out + "_check.json")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
