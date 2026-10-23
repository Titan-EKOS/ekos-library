"""File-based run checks for model-run-supervisor (FLO-2D and HEC-RAS).

Read-only on model folders. Writes JSON results only where --out points (use 40_QC or the run folder log).

  python run_checks.py preflight-flo2d <folder> [--compare <folder> ...] [--end-hr 24] [--out preflight.json]
  python run_checks.py complete-flo2d <folder> [--require MAXWSELEV.OUT DEPTH.OUT] [--max-vol-err 0.1]
  python run_checks.py complete-ras <plan.pNN.hdf> [--max-vol-err 0.1]
  python run_checks.py status <run_register.csv> [--out-md run_status.md] [--out-json run_status.json]

Exit code 0 = pass, 1 = fail, 2 = usage or read error. Every result is also printed as JSON.
On EKOS call it with the gis env interpreter (%GIS_PY%, h5py) by full path (D11), e.g.
  "%GIS_PY%" run_checks.py complete-flo2d D:\\Jobs\\<job>\\20_Working\\FLO2D\\EX_100yr_3hr
Decisions applied: D04 (FLO-2D completion), D09 (volume error), D08 (status file).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

TEXT_INPUT_EXT = {".DAT", ".RGH"}
BINARY_INPUTS = {"NEIGHBORS.DAT"}
SHARED_FILES = ["CADPTS.DAT", "CONT.DAT", "TOLER.DAT", "INFLOW.DAT", "OUTFLOW.DAT", "FPXSEC.DAT", "RAIN.DAT"]
CFS_HR_TO_ACFT = 3600.0 / 43560.0


def _upper_map(folder: Path) -> dict[str, Path]:
    return {p.name.upper(): p for p in folder.iterdir() if p.is_file()}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bare_lf_count(path: Path) -> int:
    data = path.read_bytes()
    return data.count(b"\n") - data.count(b"\r\n")


def parse_inflow(path: Path) -> dict[str, list[tuple[float, float]]]:
    """Group H (time, Q) lines under the preceding F/C node line of INFLOW.DAT."""
    series: dict[str, list[tuple[float, float]]] = {}
    node = None
    for line in path.read_text(errors="replace").splitlines():
        tok = line.split()
        if not tok:
            continue
        tag = tok[0].upper()
        if tag in ("F", "C") and len(tok) >= 3:
            node = tok[-1]
            series.setdefault(node, [])
        elif tag == "H" and node is not None and len(tok) >= 3:
            try:
                series[node].append((float(tok[1]), float(tok[2])))
            except ValueError:
                pass
    return series


def inflow_stats(series: dict[str, list[tuple[float, float]]]) -> dict:
    nodes, bad, total_vol, last_t = [], [], 0.0, 0.0
    for node, pts in series.items():
        times = [t for t, _ in pts]
        problems = [i for i in range(1, len(times)) if times[i] <= times[i - 1]]
        vol = sum((pts[i][0] - pts[i - 1][0]) * (pts[i][1] + pts[i - 1][1]) / 2.0
                  for i in range(1, len(pts)) if pts[i][0] > pts[i - 1][0]) * CFS_HR_TO_ACFT
        peak = max((q for _, q in pts), default=0.0)
        end = max(times, default=0.0)
        last_t = max(last_t, end)
        total_vol += vol
        rec = {"node": node, "points": len(pts), "peak_cfs": round(peak, 2),
               "volume_acft": round(vol, 3), "last_time_hr": end,
               "non_increasing_at": problems[:10], "chronology_ok": not problems}
        nodes.append(rec)
        if problems:
            bad.append(node)
    return {"nodes": nodes, "bad_nodes": bad, "total_volume_acft": round(total_vol, 3),
            "last_inflow_hr": last_t}


def cont_simul_hr(path: Path) -> float | None:
    for line in path.read_text(errors="replace").splitlines():
        tok = line.split()
        if tok:
            try:
                return float(tok[0])
            except ValueError:
                return None
    return None


def cmd_preflight_flo2d(a) -> dict:
    folder = Path(a.folder)
    files = _upper_map(folder)
    res: dict = {"check": "preflight-flo2d", "folder": str(folder), "issues": []}
    lf = {}
    for name, p in files.items():
        if p.suffix.upper() in TEXT_INPUT_EXT and name not in BINARY_INPUTS:
            n = bare_lf_count(p)
            if n:
                lf[name] = n
    res["bare_lf_files"] = lf
    if lf:
        res["issues"].append(f"bare LF line endings in {sorted(lf)} (write CRLF; HYD-C03 step 5)")
    stale = sorted(n for n in files if n.endswith((".TMP", ".OUT", ".CHK")))
    res["stale_outputs_present"] = stale
    if stale:
        res["issues"].append(f"{len(stale)} old .OUT/.TMP/.CHK files in folder; archive and clear before launch")
    if "INFLOW.DAT" in files:
        st = inflow_stats(parse_inflow(files["INFLOW.DAT"]))
        res["inflow"] = st
        if st["bad_nodes"]:
            res["issues"].append(f"inflow chronology fails at nodes {st['bad_nodes'][:10]}")
        end = a.end_hr if a.end_hr is not None else (
            cont_simul_hr(files["CONT.DAT"]) if "CONT.DAT" in files else None)
        res["simulation_end_hr"] = end
        if end is not None and st["last_inflow_hr"] > end:
            res["issues"].append(
                f"inflow lasts to {st['last_inflow_hr']} hr but run ends at {end} hr; extend the run")
    else:
        res["inflow"] = None
    hashes = {n: sha256(files[n]) for n in SHARED_FILES if n in files}
    res["shared_hashes"] = {k: v[:12] for k, v in hashes.items()}
    mism = []
    for other in a.compare or []:
        of = _upper_map(Path(other))
        for n, h in hashes.items():
            if n in of and sha256(of[n]) != h:
                mism.append(f"{n} differs from {other}")
            elif n not in of:
                mism.append(f"{n} missing in {other}")
    res["compare_mismatches"] = mism
    if mism:
        res["issues"].append("shared input files differ across compared scenarios")
    res["preflight_pass"] = not res["issues"]
    res["note"] = ("Volume error 0.0% in SUMMARY.OUT does not validate inflow chronology; compare inflow "
                   "volume with the source workbook by hand (total_volume_acft).")
    return res


VOL_RE = re.compile(r"(?:VOLUME|CONSERVATION)[^\n]*?(-?\d+\.\d+)\s*%", re.I)


def cmd_complete_flo2d(a) -> dict:
    folder = Path(a.folder)
    files = _upper_map(folder)
    res: dict = {"check": "complete-flo2d", "folder": str(folder), "issues": []}
    summ = files.get("SUMMARY.OUT")
    text = summ.read_text(errors="replace") if summ else ""
    res["termination_line"] = "COMPUTER RUN TIME" in text.upper()
    if not res["termination_line"]:
        res["issues"].append("SUMMARY.OUT has no termination line (COMPUTER RUN TIME)")
    tmp = sorted(n for n in files if n.endswith(".TMP"))
    res["tmp_files"] = tmp
    if tmp:
        res["issues"].append(f"{len(tmp)} TMP files present")
    req = [r.upper() for r in (a.require or ["MAXWSELEV.OUT"])]
    empty = [r for r in req if r not in files or files[r].stat().st_size == 0]
    res["missing_or_empty_outputs"] = empty
    if empty:
        res["issues"].append(f"required outputs missing or empty: {empty}")
    outs = [p for n, p in files.items() if n.endswith(".OUT")]
    ins = [p for n, p in files.items() if n.endswith(".DAT") and n not in BINARY_INPUTS]
    if outs and ins:
        oldest_out = min(p.stat().st_mtime for p in outs)
        newest_in = max(p.stat().st_mtime for p in ins)
        res["outputs_newer_than_inputs"] = oldest_out >= newest_in
        if not res["outputs_newer_than_inputs"]:
            res["issues"].append("an output is older than the newest input (stale output)")
    m = VOL_RE.findall(text)
    res["volume_error_pct"] = float(m[-1]) if m else None
    if res["volume_error_pct"] is None:
        res["issues"].append("volume error not parsed from SUMMARY.OUT; read it by hand")
    elif abs(res["volume_error_pct"]) > a.max_vol_err:
        res["issues"].append(f"volume error {res['volume_error_pct']}% > {a.max_vol_err}% (D09)")
    chk = files.get("ERROR.CHK")
    if chk:
        lines = chk.read_text(errors="replace").upper().splitlines()
        res["error_chk"] = {"errors": sum("ERROR" in l for l in lines),
                            "warnings": sum("WARNING" in l for l in lines)}
        if res["error_chk"]["errors"]:
            res["issues"].append("ERROR.CHK lists errors; disposition each before reporting")
    res["complete"] = not res["issues"]
    return res


def _walk_hdf(h5, msgs: list, vols: list):
    def visit(name, obj):
        for k, v in obj.attrs.items():
            kl = k.lower()
            if "error" in kl and ("percent" in kl or "%" in kl):
                try:
                    vols.append((name, k, float(v)))
                except (TypeError, ValueError):
                    pass
        if "compute messages" in name.lower() and hasattr(obj, "shape"):
            try:
                raw = obj[()]
                if hasattr(raw, "tobytes"):
                    raw = raw.tobytes()
                msgs.append(raw.decode(errors="replace") if isinstance(raw, bytes) else str(raw))
            except Exception:  # noqa: BLE001
                pass
    h5.visititems(visit)


def cmd_complete_ras(a) -> dict:
    res: dict = {"check": "complete-ras", "hdf": a.hdf, "issues": []}
    p = Path(a.hdf)
    if p.name.lower().endswith(".tmp.hdf"):
        res["issues"].append("this is a live .tmp.hdf; never read it during a run")
        res["complete"] = False
        return res
    try:
        import h5py  # noqa: PLC0415
    except ImportError:
        res["issues"].append("h5py not installed in this environment (D11: use the env interpreter)")
        res["complete"] = False
        return res
    msgs: list = []
    vols: list = []
    with h5py.File(p, "r") as h5:
        _walk_hdf(h5, msgs, vols)
    text = "\n".join(msgs)
    res["finished_message"] = bool(re.search(r"Finished Unsteady Flow Simulation|"
                                             r"Unsteady Finished Successfully", text, re.I))
    if not res["finished_message"]:
        res["issues"].append("no 'Finished Unsteady Flow Simulation' in compute messages")
    res["volume_error_attrs"] = [{"path": n, "attr": k, "value": v} for n, k, v in vols]
    if not vols:
        res["issues"].append("volume accounting error not found; read Volume Accounting by hand")
    else:
        worst = max(abs(v) for _, _, v in vols)
        res["volume_error_pct_max"] = worst
        if worst > a.max_vol_err:
            res["issues"].append(f"volume error {worst}% > {a.max_vol_err}% (D09)")
    res["note"] = "Also check max WSEL residual and iteration warnings in the compute log (D09)."
    res["complete"] = not res["issues"]
    return res


def cmd_status(a) -> dict:
    rows = list(csv.DictReader(open(a.register, newline="", encoding="utf-8")))
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.get("status", "")] = counts.get(r.get("status", ""), 0) + 1
    out = {"check": "status", "updated": now, "counts": counts, "jobs": rows}
    if a.out_md:
        cols = [c for c in ("job_id", "engine", "folder_or_plan", "status", "progress_hr", "end_hr", "eta",
                            "last_check", "note") if rows and c in rows[0]]
        lines = [f"# Run status (updated {now})", "",
                 "Status comes from files and processes only. Queued is not done.", "",
                 "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        lines += ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows]
        lines += ["", "Counts: " + ", ".join(f"{k or 'blank'} {v}" for k, v in sorted(counts.items()))]
        Path(a.out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    if a.out_json:
        Path(a.out_json).write_text(json.dumps(out, indent=1), encoding="utf-8")
    out["complete"] = True
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preflight-flo2d"); p.add_argument("folder")
    p.add_argument("--compare", nargs="*"); p.add_argument("--end-hr", type=float); p.add_argument("--out")
    p = sub.add_parser("complete-flo2d"); p.add_argument("folder"); p.add_argument("--require", nargs="*")
    p.add_argument("--max-vol-err", type=float, default=0.1); p.add_argument("--out")
    p = sub.add_parser("complete-ras"); p.add_argument("hdf")
    p.add_argument("--max-vol-err", type=float, default=0.1); p.add_argument("--out")
    p = sub.add_parser("status"); p.add_argument("register")
    p.add_argument("--out-md"); p.add_argument("--out-json"); p.set_defaults(out=None)
    a = ap.parse_args(argv)
    try:
        res = {"preflight-flo2d": cmd_preflight_flo2d, "complete-flo2d": cmd_complete_flo2d,
               "complete-ras": cmd_complete_ras, "status": cmd_status}[a.cmd](a)
    except (OSError, ValueError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    txt = json.dumps(res, indent=1, default=str)
    if getattr(a, "out", None):
        Path(a.out).write_text(txt, encoding="utf-8")
    print(txt)
    ok = res.get("preflight_pass", res.get("complete", False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
