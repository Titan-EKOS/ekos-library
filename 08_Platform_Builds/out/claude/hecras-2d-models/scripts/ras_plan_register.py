"""HEC-RAS plan / geometry / flow register and hygiene check (HYD-C13, DSO-C16). Pure Python, read-only.

  D:\\EKOS\\envs\\gis\\.venv\\Scripts\\python.exe ras_plan_register.py <project.prj> [--out plan_register.csv]

Reads the .prj and every .p## as text (never opens RAS, so nothing is rewritten). Writes the register CSV
beside the project (or --out) and prints findings as JSON. Exit 1 when any FLAG is raised.

Register columns: plan, registered, title, short_id, geom, flow, program_version, comp_interval,
                  result_hdf_bytes, flags
Flags raised
  - plan file on disk but not registered in the .prj / registered but missing on disk
  - two or more plans share one flow file (e.g. 100-yr and 10-yr plans both on u02)
  - placeholder names (Plan 12, Plan 37, '1', New Geometry, Retry, Copy of ...) or empty short ID
  - mixed Program Version across plans in one project
  - auto-duplicate plans: same geom + flow pair as another plan
  - stray result copies: *.tmp.hdf, renamed *.p##*.hdf, snapshot / backup / conflict copies
"""
import argparse
import csv
import glob
import json
import os
import re
import sys

PLACEHOLDER = re.compile(r"^\s*(plan\s*\d+|\d+|new\s+geometry|unsteady\s*flow\s*\d*|copy\s+of.*|.*retry\d*.*)\s*$", re.I)


def read_keys(path):
    out = {}
    with open(path, "r", errors="replace") as f:
        for line in f:
            if "=" in line:
                k, v = line.rstrip("\r\n").split("=", 1)
                out.setdefault(k.strip(), []).append(v.strip())
    return out


def first(d, k):
    v = d.get(k)
    return v[0] if v else ""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prj")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    folder = os.path.dirname(os.path.abspath(a.prj))
    base = os.path.splitext(os.path.basename(a.prj))[0]
    prj = read_keys(a.prj)
    reg_plans = set(prj.get("Plan File", []))
    reg_geoms = set(prj.get("Geom File", []))
    reg_flows = set(prj.get("Unsteady File", []) + prj.get("Flow File", []))
    findings = {"project": a.prj, "as_received_current_plan": first(prj, "Current Plan"), "flags": []}

    disk_plans = {}
    for p in glob.glob(os.path.join(folder, base + ".p[0-9][0-9]")):
        disk_plans[p[-3:]] = p
    rows, pair_seen, flow_users, versions = [], {}, {}, set()
    for pid in sorted(set(disk_plans) | reg_plans):
        flags = []
        path = disk_plans.get(pid)
        if pid not in reg_plans:
            flags.append("not registered in .prj")
        if not path:
            flags.append("registered but file missing")
            rows.append({"plan": pid, "registered": pid in reg_plans, "flags": "; ".join(flags)})
            continue
        d = read_keys(path)
        title, sid = first(d, "Plan Title"), first(d, "Short Identifier")
        geom, flow = first(d, "Geom File"), first(d, "Flow File")
        ver = first(d, "Program Version")
        if ver:
            versions.add(ver)
        if PLACEHOLDER.match(title or "1") or not sid:
            flags.append("placeholder title or empty short ID")
        if geom and geom not in reg_geoms:
            flags.append(f"geometry {geom} not registered")
        if flow and flow not in reg_flows:
            flags.append(f"flow {flow} not registered")
        flow_users.setdefault(flow, []).append(pid)
        pair = (geom, flow)
        if pair in pair_seen:
            flags.append(f"same geom+flow as {pair_seen[pair]} (auto-duplicate?)")
        else:
            pair_seen[pair] = pid
        hdf = os.path.join(folder, f"{base}.{pid}.hdf")
        rows.append({"plan": pid, "registered": pid in reg_plans, "title": title, "short_id": sid,
                     "geom": geom, "flow": flow, "program_version": ver,
                     "comp_interval": first(d, "Computation Interval"),
                     "result_hdf_bytes": os.path.getsize(hdf) if os.path.exists(hdf) else 0,
                     "flags": "; ".join(flags)})
    for flow, users in flow_users.items():
        if flow and len(users) > 1:
            for r in rows:
                if r["plan"] in users:
                    r["flags"] = "; ".join(filter(None, [r.get("flags", ""), f"flow file {flow} shared by {','.join(users)}"]))
    if len(versions) > 1:
        findings["flags"].append({"flag": "mixed Program Version in one project", "versions": sorted(versions)})
    strays = []
    for p in glob.glob(os.path.join(folder, "*.hdf")):
        n = os.path.basename(p)
        if re.fullmatch(re.escape(base) + r"\.(p|g|u)\d\d\.hdf", n, re.I):
            continue
        if re.fullmatch(re.escape(base) + r"\.(g|u)\d\d\.hdf", n, re.I):
            continue
        strays.append(n)
    for g in ["Backup*", "*conflict*", "*Snapshot*", "*.tmp.hdf"]:
        strays += [os.path.basename(p) for p in glob.glob(os.path.join(folder, g))]
    if strays:
        findings["flags"].append({"flag": "stray or non-standard result copies (never treat as results)",
                                  "files": sorted(set(strays))[:100]})
    for r in rows:
        if r.get("flags"):
            findings["flags"].append({"plan": r["plan"], "flag": r["flags"]})

    out = a.out or os.path.join(folder, "plan_register.csv")
    cols = ["plan", "registered", "title", "short_id", "geom", "flow", "program_version", "comp_interval",
            "result_hdf_bytes", "flags"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    findings["register"] = out
    print(json.dumps(findings, indent=2))
    return 1 if findings["flags"] else 0


if __name__ == "__main__":
    sys.exit(main())
