"""Headless HEC-RAS 6.6 plan compute with the decision-D05 fallback order. Windows only.

Environment: gis env (psutil; pywinauto for the dialog log; pywin32 only for the COM fallback).
  D:\\EKOS\\envs\\gis\\.venv\\Scripts\\python.exe ras_headless.py <project.prj> p03
      [--ras-exe "C:\\Program Files (x86)\\HEC\\HEC-RAS\\6.6\\Ras.exe"]
      [--timeout-hours 12] [--no-com] [--unsteady-args "{tmp} x{num}"]

Order (D05):
  1. Ras.exe -c <prj> <plan file> -hideCompute, with a dialog logger running.
  2. If no plan HDF but <prj>.p##.tmp.hdf remains: wait until no RasUnsteady.exe is open in the folder,
     then run RasUnsteady.exe on the temp HDF and rename it to p##.hdf on success.
     The argument pattern is configurable (--unsteady-args); confirm it on the EKOS 6.6 install from the
     command line of a GUI-started RasUnsteady.exe before relying on it.
  3. COM controller (RAS66.HECRASController): open, set plan, compute, always QuitRas.
Success is judged only by the closed plan HDF and ras_result_check.py, never by a return code.
Writes <prj folder>/<plan>_headless_log.json. One project copy per plan for parallel runs.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def procs_named(name, folder=None):
    import psutil
    out = []
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if (p.info["name"] or "").lower() != name.lower():
                continue
            cmd = " ".join(p.info["cmdline"] or [])
            if "-embedding" in cmd.lower():
                continue  # Ras -Embedding is a COM server, not a compute
            if folder and os.path.normcase(folder) not in os.path.normcase(cmd + " " + (p.cwd() or "")):
                continue
            out.append(p)
        except Exception:
            continue
    return out


def dialog_logger(stop, log):
    """Log any Ras.exe / RasUnsteady.exe dialog text. Does not answer dialogs (D07 pattern: notify)."""
    try:
        from pywinauto import Desktop
    except Exception:
        log.append({"time": now(), "note": "pywinauto missing; dialogs not logged"})
        return
    seen = set()
    while not stop.is_set():
        try:
            pids = {p.pid for p in procs_named("Ras.exe") + procs_named("RasUnsteady.exe")}
            for w in Desktop(backend="uia").windows():
                try:
                    if w.process_id() not in pids:
                        continue
                    text = " | ".join(c.window_text() for c in w.descendants() if c.window_text())
                    key = (w.window_text(), text)
                    if key not in seen:
                        seen.add(key)
                        log.append({"time": now(), "dialog_title": w.window_text(), "text": text[:2000]})
                except Exception:
                    pass
        except Exception:
            pass
        stop.wait(10)


def result_check(hdf):
    r = subprocess.run([sys.executable, os.path.join(HERE, "ras_result_check.py"), hdf],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def wait_no_unsteady(folder, timeout_s):
    t0 = time.time()
    while procs_named("RasUnsteady.exe", folder):
        if time.time() - t0 > timeout_s:
            return False
        time.sleep(30)
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prj")
    ap.add_argument("plan", help="plan id, e.g. p03")
    ap.add_argument("--ras-exe", default=r"C:\Program Files (x86)\HEC\HEC-RAS\6.6\Ras.exe")
    ap.add_argument("--timeout-hours", type=float, default=12.0)
    ap.add_argument("--no-com", action="store_true")
    ap.add_argument("--unsteady-args", default="{tmp} x{num}")
    a = ap.parse_args(argv)
    if os.name != "nt":
        print("Windows only.")
        return 1
    prj = os.path.abspath(a.prj)
    folder = os.path.dirname(prj)
    base = os.path.splitext(prj)[0]
    plan_file = f"{base}.{a.plan}"
    hdf, tmp = plan_file + ".hdf", plan_file + ".tmp.hdf"
    log = {"prj": prj, "plan": a.plan, "attempts": [], "dialogs": []}
    logpath = os.path.join(folder, f"{a.plan}_headless_log.json")
    timeout_s = a.timeout_hours * 3600

    def save():
        with open(logpath, "w") as f:
            json.dump(log, f, indent=2, default=str)

    if procs_named("RasUnsteady.exe", folder) or os.path.exists(tmp):
        log["refused"] = "a compute is open in this folder or a temp HDF exists; do not start another"
        save()
        print(log["refused"])
        return 2
    if os.path.exists(hdf):
        os.replace(hdf, hdf + f".prev_{dt.datetime.now():%Y%m%d%H%M}")

    stop = threading.Event()
    th = threading.Thread(target=dialog_logger, args=(stop, log["dialogs"]), daemon=True)
    th.start()
    try:
        # 1. Ras.exe -c
        t0 = time.time()
        p = subprocess.Popen([a.ras_exe, "-c", prj, plan_file, "-hideCompute"], cwd=folder)
        while p.poll() is None and time.time() - t0 < timeout_s:
            time.sleep(30)
        if p.poll() is None:
            p.kill()
        log["attempts"].append({"method": "Ras.exe -c -hideCompute", "start": t0, "minutes": round((time.time() - t0) / 60, 1),
                                "return_code_logged": p.returncode})
        if not os.path.exists(hdf) and os.path.exists(tmp):
            # 2. RasUnsteady direct on the temp HDF
            if wait_no_unsteady(folder, timeout_s):
                unsteady = os.path.join(os.path.dirname(a.ras_exe), "RasUnsteady.exe")
                args = a.unsteady_args.format(tmp=os.path.basename(tmp), num=a.plan[1:]).split()
                t1 = time.time()
                r = subprocess.run([unsteady] + args, cwd=folder, capture_output=True, text=True, timeout=timeout_s)
                log["attempts"].append({"method": "RasUnsteady direct", "args": args, "minutes": round((time.time() - t1) / 60, 1),
                                        "stdout_tail": r.stdout[-3000:], "return_code_logged": r.returncode})
                if os.path.exists(tmp) and not procs_named("RasUnsteady.exe", folder):
                    os.replace(tmp, hdf)
        if not os.path.exists(hdf) and not a.no_com:
            # 3. COM controller
            t2 = time.time()
            rc = None
            try:
                import win32com.client
                ras = win32com.client.Dispatch("RAS66.HECRASController")
                try:
                    ras.Project_Open(prj)
                    titles = ras.Plan_Names(None, None, False)
                    rc = {"plan_names": str(titles)}
                    # Set the current plan by title read from the plan file.
                    title = next((ln.split("=", 1)[1].strip() for ln in open(plan_file, errors="replace")
                                  if ln.startswith("Plan Title=")), None)
                    if title:
                        ras.Plan_SetCurrent(title)
                    res = ras.Compute_CurrentPlan(None, None, True)
                    rc["compute_return"] = str(res)
                finally:
                    ras.QuitRas()
            except Exception as e:
                rc = {"error": str(e)}
            log["attempts"].append({"method": "COM RAS66.HECRASController", "minutes": round((time.time() - t2) / 60, 1),
                                    "detail": rc, "note": "COM may reset core count to automatic; verify the plan setting"})
    finally:
        stop.set()
    if os.path.exists(hdf):
        code, out = result_check(hdf)
        log["result_check"] = out
        log["success"] = code == 0
    else:
        log["success"] = False
        log["note"] = ("no plan HDF: check geometry errors in compute messages (e.g. BC lines share the same face), "
                       "then retry up to 3 times before logging not complete")
    log["finished"] = now()
    save()
    print(json.dumps({"success": log["success"], "log": logpath}))
    return 0 if log["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
