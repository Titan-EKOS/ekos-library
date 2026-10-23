"""HEC-RAS model-set register for received or archived models (skill project-intake, HYD-C13).

Reads the .prj as text (registered geometry, unsteady/steady flow and plan files, as-received Current Plan), each
.p## (Plan Title, Short Identifier, Geom File, Flow File, Program Version, Computation Interval), the .rasmap
projection, and the files on disk; writes a plan-geometry-flow register and flags:
  unregistered plans, registered entries without files, stray copies (.tmp.hdf, renamed result HDFs, Backup files,
  snapshot HDFs, sync conflict copies), plans sharing one flow file under different titles, generic plan titles.
Read-only: never open the project in RAS for this step (opening rewrites plan and geometry files).

Usage: python ras_plan_register.py --prj <model.prj> --out <register.csv> [--json <findings.json>]
Exit codes: 0 no findings, 1 findings, 2 usage error.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

GENERIC = re.compile(r"^\s*(plan\s*\d+|unsteady\s*\d*|new plan|test|copy of .*)\s*$", re.I)


def read_kv(path):
    out = {}
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out.setdefault(k.strip(), []).append(v.strip())
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prj", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    prj = Path(a.prj)
    if not prj.exists():
        print(f"missing {prj}", file=sys.stderr)
        return 2
    stem, folder = prj.stem, prj.parent
    kv = read_kv(prj)
    reg = {"plan": kv.get("Plan File", []), "geom": kv.get("Geom File", []),
           "unsteady": kv.get("Unsteady File", []), "flow": kv.get("Flow File", [])}
    current = (kv.get("Current Plan") or [""])[0]
    findings = {"as_received_current_plan": current, "unregistered_plans": [], "registered_missing": [],
                "stray_files": [], "shared_flow_file": [], "generic_titles": [], "flow_title_check": []}
    rows = []
    disk_plans = sorted(p.suffix[1:] for p in folder.glob(f"{stem}.p[0-9][0-9]"))
    findings["unregistered_plans"] = [p for p in disk_plans if p not in reg["plan"]]
    for kind, ids in reg.items():
        for i in ids:
            if not (folder / f"{stem}.{i}").exists():
                findings["registered_missing"].append(f"{stem}.{i}")
    for p in sorted(set(reg["plan"]) | set(disk_plans)):
        f = folder / f"{stem}.{p}"
        if not f.exists():
            continue
        pk = read_kv(f)
        title = (pk.get("Plan Title") or [""])[0]
        geom = (pk.get("Geom File") or [""])[0]
        flow = (pk.get("Flow File") or [""])[0]
        hdf = folder / f"{stem}.{p}.hdf"
        rows.append({"plan": p, "registered": "yes" if p in reg["plan"] else "no", "title": title,
                     "short_id": (pk.get("Short Identifier") or [""])[0], "geom": geom, "flow": flow,
                     "program_version": (pk.get("Program Version") or [""])[0],
                     "computation_interval": (pk.get("Computation Interval") or [""])[0],
                     "result_hdf_mb": round(hdf.stat().st_size / 1e6, 1) if hdf.exists() else "",
                     "condition": "", "terrain": "", "status": ""})
        if GENERIC.match(title or "plan"):
            findings["generic_titles"].append(f"{p}: '{title}'")
    by_flow = {}
    for r in rows:
        by_flow.setdefault(r["flow"], []).append(r)
    for flow, rs in by_flow.items():
        if flow and len(rs) > 1 and len({r["title"] for r in rs}) > 1:
            findings["shared_flow_file"].append(f"{flow}: " + ", ".join(f"{r['plan']} '{r['title']}'" for r in rs))
    for r in rows:
        ev = re.findall(r"(\d{1,3})\s*-?\s*(?:yr|year)", r["title"], re.I)
        if ev and r["flow"]:
            ff = folder / f"{stem}.{r['flow']}"
            ftitle = (read_kv(ff).get("Flow Title") or [""])[0] if ff.exists() else ""
            fev = re.findall(r"(\d{1,3})\s*-?\s*(?:yr|year)", ftitle, re.I)
            if fev and set(ev) != set(fev):
                findings["flow_title_check"].append(f"{r['plan']} '{r['title']}' uses {r['flow']} '{ftitle}'")
    known = {f"{stem}.{i}" for ids in reg.values() for i in ids} | {f"{stem}.{i}.hdf" for ids in reg.values() for i in ids}
    known |= {f"{stem}.prj", f"{stem}.rasmap"}
    for f in folder.iterdir():
        n = f.name
        low = n.lower()
        if (low.endswith(".tmp.hdf") or "backup" in low or "snapshot" in low or "conflict" in low
                or re.search(r"-[A-Za-z0-9]+-\d+\.", n)  # OneDrive conflict copies: name-PCNAME-2.ext
                or (n.startswith(stem + ".") and re.match(rf"{re.escape(stem)}\.[pgu]\d\d\w+\.hdf$", n))):
            findings["stray_files"].append(n)
    rasmap = folder / f"{stem}.rasmap"
    if rasmap.exists():
        m = re.search(r'<RASProjectionFilename Filename="([^"]+)"', rasmap.read_text(encoding="utf-8", errors="replace"))
        findings["rasmap_projection"] = m.group(1) if m else "(not set)"
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["plan"])
        w.writeheader()
        w.writerows(rows)
    if a.json:
        Path(a.json).write_text(json.dumps(findings, indent=1), encoding="utf-8")
    print(json.dumps(findings, indent=1))
    n = sum(len(v) for k, v in findings.items() if isinstance(v, list))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
