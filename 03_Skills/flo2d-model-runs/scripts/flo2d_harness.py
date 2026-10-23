"""FLO-2D Pro run harness: preflight, launch, status, finish.

Environment: hydraulics env, %HYDRAULICS_PY% (numpy not needed; psutil required for launch/status/finish).
Run with the env interpreter by full path, e.g.
  "%HYDRAULICS_PY%" flo2d_harness.py preflight D:\\Jobs\\1234\\FLO\\EX_100yr_24hr

Subcommands
  preflight <folder> [--source SRC] [--compare F2 ...] [--fix-crlf] [--simul HOURS]
      CRLF scan, stale-output scan, file size/hash vs source copy, shared-input hash
      equality across scenarios, INFLOW.DAT chronology/volume, run window vs last inflow.
      Writes <folder>/preflight.json; exit 1 when preflight_pass is false.
  launch <folder> --threads 8 --mask 0xFF00 [--exe PATH] [--max-solvers 2] [--archive]
      Refuses a folder already run (unless --archive moves old outputs to _archive/vN),
      refuses a duplicate FLOPRO in the folder and more than --max-solvers FLOPRO at once,
      sets OMP_NUM_THREADS and CPU affinity, starts detached, writes Running.json.
  status <folder> [--base-hours H] [--end-hours H]
      Reads closed summary files only. Writes <folder>/status.json.
  finish <folder> [--grace 120]
      If the run is complete (termination line + outputs + no TMP) and FLOPRO is still
      open, verifies PID + creation time and terminates it. Exit code is logged only (D04).

Completion rule (decision D04): SUMMARY.OUT has the termination line, key outputs are
non-empty and no *.TMP files remain. The process exit code is recorded, never required.
"""
import argparse
import csv
import datetime as dt
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

TERMINATION = "COMPUTER RUN TIME"
SHARED_INPUTS = ["CADPTS.DAT", "CONT.DAT", "TOLER.DAT", "INFLOW.DAT", "OUTFLOW.DAT"]
KEY_OUTPUTS = ["DEPFP.OUT", "MAXWSELEV.OUT", "VELFP.OUT", "FINALDEP.OUT", "VELDIREC.OUT"]
BINARY_INPUTS = {"NEIGHBORS.DAT"}
TEXT_EXT = (".DAT", ".RGH")
OUTPUT_GLOBS = ["*.OUT", "*.TMP", "*.CHK"]


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def sha256(path, block=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            h.update(chunk)
    return h.hexdigest()


def find_ci(folder, name):
    """Case-insensitive file lookup in folder."""
    target = name.upper()
    for f in os.listdir(folder):
        if f.upper() == target:
            return os.path.join(folder, f)
    return None


def write_json(path, data):
    tmp = path + ".tmp_write"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


# ---------------------------------------------------------------- preflight
def scan_line_endings(folder):
    """Return list of text inputs containing a bare LF (no preceding CR)."""
    bad = []
    for f in sorted(os.listdir(folder)):
        up = f.upper()
        if not up.endswith(TEXT_EXT) or up in BINARY_INPUTS:
            continue
        data = open(os.path.join(folder, f), "rb").read()
        bare = len(re.findall(rb"(?<!\r)\n", data))
        no_trailing = len(data) > 0 and not data.endswith(b"\r\n")
        if bare or no_trailing:
            bad.append({"file": f, "bare_lf": bare, "missing_trailing_crlf": no_trailing})
    return bad


def fix_crlf(folder, files):
    """Rewrite listed files with CRLF via temp file + rename. Content otherwise unchanged."""
    for f in files:
        p = os.path.join(folder, f)
        data = open(p, "rb").read()
        data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        if not data.endswith(b"\r\n"):
            data += b"\r\n"
        tmp = p + ".crlf_tmp"
        with open(tmp, "wb") as fh:
            fh.write(data)
        os.replace(tmp, p)


def compare_to_source(folder, source):
    """Byte size + hash of every file in source vs the copy."""
    issues = []
    for f in sorted(os.listdir(source)):
        sp = os.path.join(source, f)
        if not os.path.isfile(sp):
            continue
        cp = os.path.join(folder, f)
        if not os.path.exists(cp):
            issues.append({"file": f, "issue": "missing in copy"})
            continue
        if os.path.getsize(sp) != os.path.getsize(cp):
            issues.append({"file": f, "issue": "size differs",
                           "source_bytes": os.path.getsize(sp), "copy_bytes": os.path.getsize(cp)})
        elif sha256(sp) != sha256(cp):
            issues.append({"file": f, "issue": "hash differs"})
    return issues


def shared_hashes(folder):
    out = {}
    for name in SHARED_INPUTS:
        p = find_ci(folder, name)
        out[name] = sha256(p) if p else None
    return out


def parse_inflow(path):
    """Parse INFLOW.DAT node series. Lines starting F or C open a node (last token = node);
    lines starting H carry time (hr) and discharge (cfs). Returns {node: [(t, q), ...]}."""
    series, node = {}, None
    with open(path, "r", errors="replace") as f:
        for line in f:
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


def check_inflow(series):
    nodes, total_af, last_t = [], 0.0, 0.0
    for node, pts in series.items():
        times = [t for t, _ in pts]
        bad = [i for i in range(1, len(times)) if times[i] <= times[i - 1]]
        vol_cf = sum((pts[i][0] - pts[i - 1][0]) * 3600.0 * (pts[i][1] + pts[i - 1][1]) / 2.0
                     for i in range(1, len(pts)) if pts[i][0] > pts[i - 1][0])
        steps = sorted({round(times[i] - times[i - 1], 6) for i in range(1, len(times))})
        nodes.append({"node": node, "points": len(pts),
                      "non_increasing_at": bad[:10], "n_non_increasing": len(bad),
                      "peak_cfs": max((q for _, q in pts), default=0.0),
                      "volume_af": round(vol_cf / 43560.0, 3),
                      "last_time_hr": times[-1] if times else None,
                      "time_steps_hr": steps[:5]})
        total_af += vol_cf / 43560.0
        if times:
            last_t = max(last_t, times[-1])
    return nodes, round(total_af, 3), last_t


def read_simul(folder):
    """First token on line 1 of CONT.DAT is SIMUL (hr) in FLO-2D Pro. Verify by eye."""
    p = find_ci(folder, "CONT.DAT")
    if not p:
        return None
    first = open(p, "r", errors="replace").readline().split()
    try:
        return float(first[0])
    except (IndexError, ValueError):
        return None


def cmd_preflight(a):
    folder = a.folder
    rep = {"folder": folder, "time": now(), "checks": {}}
    ok = True

    if a.fix_crlf:
        bad = scan_line_endings(folder)
        fix_crlf(folder, [b["file"] for b in bad])
        rep["checks"]["crlf_fixed"] = [b["file"] for b in bad]
    bad = scan_line_endings(folder)
    rep["checks"]["line_endings"] = {"pass": not bad, "files": bad}
    ok &= not bad

    stale = sorted({os.path.basename(p) for g in OUTPUT_GLOBS for p in glob.glob(os.path.join(folder, g))})
    rep["checks"]["stale_outputs"] = {"pass": not stale, "files": stale[:50],
                                      "note": "archive with launch --archive before running"}
    ok &= not stale

    if a.source:
        issues = compare_to_source(folder, a.source)
        rep["checks"]["copy_integrity"] = {"pass": not issues, "issues": issues}
        ok &= not issues

    exe = find_ci(folder, "FLOPRO.exe")
    if exe:
        dlls = len(glob.glob(os.path.join(folder, "*.dll")))
        rep["checks"]["engine"] = {"exe_bytes": os.path.getsize(exe), "exe_sha256": sha256(exe), "dll_count": dlls}

    hashes = shared_hashes(folder)
    rep["checks"]["shared_input_hashes"] = hashes
    if a.compare:
        mism = []
        for other in a.compare:
            oh = shared_hashes(other)
            for k, v in hashes.items():
                if oh.get(k) != v:
                    mism.append({"file": k, "other": other})
        rep["checks"]["shared_hash_equality"] = {"pass": not mism, "mismatches": mism}
        ok &= not mism

    inflow = find_ci(folder, "INFLOW.DAT")
    if inflow:
        nodes, total_af, last_t = check_inflow(parse_inflow(inflow))
        chron_bad = [n["node"] for n in nodes if n["n_non_increasing"]]
        rep["checks"]["inflow"] = {"pass": not chron_bad, "nodes": len(nodes), "total_volume_af": total_af,
                                   "last_inflow_hr": last_t, "nodes_with_bad_chronology": chron_bad[:50],
                                   "detail": nodes}
        ok &= not chron_bad
        simul = a.simul if a.simul is not None else read_simul(folder)
        win_ok = simul is not None and simul >= last_t
        rep["checks"]["run_window"] = {"pass": win_ok, "simul_hr": simul, "last_inflow_hr": last_t,
                                       "note": "run must also cover the recession (reference-run test)"}
        ok &= win_ok

    rep["preflight_pass"] = bool(ok)
    write_json(os.path.join(folder, "preflight.json"), rep)
    print(json.dumps({"preflight_pass": rep["preflight_pass"],
                      "failed": [k for k, v in rep["checks"].items() if isinstance(v, dict) and v.get("pass") is False]}))
    return 0 if ok else 1


# ---------------------------------------------------------------- process helpers
def flopro_procs():
    import psutil
    out = []
    for p in psutil.process_iter(["pid", "name", "create_time"]):
        try:
            if (p.info["name"] or "").upper().startswith("FLOPRO"):
                try:
                    cwd = p.cwd()
                except Exception:
                    cwd = None
                out.append({"pid": p.info["pid"], "create_time": p.info["create_time"], "cwd": cwd})
        except Exception:
            continue
    return out


def same_path(a, b):
    return a and b and os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def verified_process(man):
    """Return psutil.Process only if PID, name and creation time match the manifest (PIDs are reused)."""
    import psutil
    try:
        p = psutil.Process(man["pid"])
        if not (p.name() or "").upper().startswith("FLOPRO"):
            return None
        if abs(p.create_time() - man["create_time"]) > 1.0:
            return None
        return p
    except Exception:
        return None


def archive_outputs(folder):
    arch = os.path.join(folder, "_archive")
    os.makedirs(arch, exist_ok=True)
    n = 1
    while os.path.exists(os.path.join(arch, f"v{n}")):
        n += 1
    dest = os.path.join(arch, f"v{n}")
    os.makedirs(dest)
    moved = []
    for g in OUTPUT_GLOBS + ["Running.json", "status.json"]:
        for p in glob.glob(os.path.join(folder, g)):
            shutil.move(p, os.path.join(dest, os.path.basename(p)))
            moved.append(os.path.basename(p))
    return dest, moved


def cmd_launch(a):
    folder = os.path.abspath(a.folder)
    man_path = os.path.join(folder, "Running.json")
    already = os.path.exists(man_path) or find_ci(folder, "SUMMARY.OUT")
    if already and not a.archive:
        print("REFUSED: folder already run (Running.json or SUMMARY.OUT present). Use --archive.")
        return 2
    procs = flopro_procs()
    if any(same_path(p["cwd"], folder) for p in procs):
        print("REFUSED: a FLOPRO process is already open in this folder; stop it first.")
        return 2
    if len(procs) >= a.max_solvers:
        print(f"REFUSED: {len(procs)} FLOPRO solvers running; limit {a.max_solvers} (decision D06).")
        return 3
    pf = os.path.join(folder, "preflight.json")
    if not a.skip_preflight_check:
        if not os.path.exists(pf) or not json.load(open(pf)).get("preflight_pass"):
            print("REFUSED: preflight.json missing or preflight_pass false.")
            return 4
    archived = None
    if a.archive:
        archived = archive_outputs(folder)
    exe = a.exe or find_ci(folder, "FLOPRO.exe")
    if not exe or not os.path.exists(exe):
        print("REFUSED: FLOPRO.exe not found (copy the Run for Project Folder package into the folder).")
        return 5
    env = dict(os.environ, OMP_NUM_THREADS=str(a.threads))
    flags = 0
    if os.name == "nt":
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    proc = subprocess.Popen([exe], cwd=folder, env=env, creationflags=flags,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import psutil
    p = psutil.Process(proc.pid)
    cores = [i for i in range(psutil.cpu_count()) if (int(a.mask, 16) >> i) & 1]
    try:
        p.cpu_affinity(cores)
    except Exception as e:
        print(f"WARNING: affinity not set: {e}")
    man = {"status": "running", "folder": folder, "cmd": [exe], "pid": proc.pid,
           "create_time": p.create_time(), "threads": a.threads, "mask": a.mask, "cores": cores,
           "exe_sha256": sha256(exe), "started": now(), "archived_previous": archived}
    write_json(man_path, man)
    log = os.path.join(folder, "run_log.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "event", "pid", "threads", "mask", "note"])
        w.writerow([now(), "launch", proc.pid, a.threads, a.mask, ""])
    print(json.dumps({"launched": True, "pid": proc.pid, "cores": cores}))
    return 0


# ---------------------------------------------------------------- status / finish
VOL_RE = re.compile(r"(VOLUME|CONSERVATION).*?(-?\d+\.\d+(?:E[-+]?\d+)?)\s*(%|PERCENT)", re.I)


def run_state(folder, end_hours=None):
    st = {"folder": folder, "time": now()}
    summ = find_ci(folder, "SUMMARY.OUT")
    text = open(summ, "r", errors="replace").read() if summ else ""
    st["termination_line"] = TERMINATION in text.upper()
    vol_lines = [ln.strip() for ln in text.splitlines() if VOL_RE.search(ln)]
    st["volume_lines"] = vol_lines[:5]
    vals = []
    for ln in vol_lines:
        m = VOL_RE.search(ln)
        try:
            vals.append(abs(float(m.group(2))))
        except (TypeError, ValueError):
            pass
    st["volume_error_pct"] = max(vals) if vals else None
    st["tmp_files"] = [os.path.basename(p) for p in glob.glob(os.path.join(folder, "*.TMP"))]
    outs = {}
    for k in KEY_OUTPUTS:
        p = find_ci(folder, k)
        outs[k] = os.path.getsize(p) if p else 0
    st["key_outputs_bytes"] = outs
    st["outputs_ok"] = all(v > 0 for v in outs.values())
    st["complete"] = bool(st["termination_line"] and st["outputs_ok"] and not st["tmp_files"])
    if st["complete"] and st["volume_error_pct"] is None:
        st["note"] = "volume error line not parsed; read SUMMARY.OUT and record it by hand"
    return st


def cmd_status(a):
    folder = os.path.abspath(a.folder)
    st = run_state(folder, a.end_hours)
    man_path = os.path.join(folder, "Running.json")
    if os.path.exists(man_path):
        man = json.load(open(man_path))
        p = verified_process(man)
        st["process_open"] = p is not None
        started = dt.datetime.fromisoformat(man["started"])
        st["wall_hours"] = round((dt.datetime.now() - started).total_seconds() / 3600.0, 2)
        if a.base_hours and not st["complete"] and st["wall_hours"] > 4.0 * a.base_hours:
            st["stall_suspect"] = True
            st["note"] = ("wall time over 4x base run (rate under 25 pct); read TIME.OUT for the "
                          "controlling element and stop per the stall procedure")
    write_json(os.path.join(folder, "status.json"), st)
    print(json.dumps({k: st.get(k) for k in ("complete", "termination_line", "outputs_ok", "tmp_files",
                                             "volume_error_pct", "process_open", "wall_hours", "stall_suspect")}))
    return 0


def cmd_finish(a):
    folder = os.path.abspath(a.folder)
    st = run_state(folder)
    man_path = os.path.join(folder, "Running.json")
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    if not st["complete"]:
        print("NOT COMPLETE: termination line, outputs or TMP check failed; no action taken.")
        return 1
    exit_code = None
    if man:
        p = verified_process(man)
        if p is not None:
            try:
                exit_code = p.wait(timeout=a.grace)
            except Exception:
                p.terminate()
                try:
                    exit_code = p.wait(timeout=30)
                except Exception:
                    p.kill()
                    exit_code = "killed"
        man.update({"status": "complete", "finished": now(), "exit_code_logged": exit_code,
                    "volume_error_pct": st["volume_error_pct"]})
        write_json(man_path, man)
    with open(os.path.join(folder, "run_log.csv"), "a", newline="") as f:
        csv.writer(f).writerow([now(), "finish", man.get("pid"), "", "", f"exit={exit_code}"])
    print(json.dumps({"complete": True, "exit_code_logged": exit_code, "volume_error_pct": st["volume_error_pct"]}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preflight"); p.add_argument("folder"); p.add_argument("--source")
    p.add_argument("--compare", nargs="*"); p.add_argument("--fix-crlf", action="store_true")
    p.add_argument("--simul", type=float)
    p = sub.add_parser("launch"); p.add_argument("folder"); p.add_argument("--threads", type=int, default=8)
    p.add_argument("--mask", default="0xFF"); p.add_argument("--exe"); p.add_argument("--max-solvers", type=int, default=2)
    p.add_argument("--archive", action="store_true"); p.add_argument("--skip-preflight-check", action="store_true")
    p = sub.add_parser("status"); p.add_argument("folder"); p.add_argument("--base-hours", type=float)
    p.add_argument("--end-hours", type=float)
    p = sub.add_parser("finish"); p.add_argument("folder"); p.add_argument("--grace", type=float, default=120)
    a = ap.parse_args(argv)
    return {"preflight": cmd_preflight, "launch": cmd_launch, "status": cmd_status, "finish": cmd_finish}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
