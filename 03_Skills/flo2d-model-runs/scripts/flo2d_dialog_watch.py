"""FLO-2D Pro dialog watcher (decision D07). Windows only; Environment: gis env with pywinauto.

Polls top-level windows owned by FLOPRO processes. For each dialog it logs title and text to
<logdir>/dialog_log.csv. Text that matches an entry in known_benign_warnings.json is answered
(button named in the entry, else Enter) and logged as auto-answered. Any other dialog is left
open, a STOP_<pid>.json file is written for the supervisor, and the watcher keeps logging.
The supervisor notifies JCO; the run waits until someone decides.

  D:\\EKOS\\envs\\gis\\.venv\\Scripts\\python.exe flo2d_dialog_watch.py --logdir D:\\Jobs\\1234\\FLO\\EX_100yr
      [--benign ..\\reference\\known_benign_warnings.json] [--poll 5] [--once]

Add an entry to the benign list only after JCO has reviewed the logged text from a real run.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time


def load_benign(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rules = []
    for e in data.get("entries", []):
        rules.append({"id": e["id"], "title": re.compile(e.get("title_regex", ".*"), re.I),
                      "text": re.compile(e["text_regex"], re.I | re.S), "button": e.get("button")})
    return rules


def flopro_pids():
    import psutil
    return {p.pid for p in psutil.process_iter(["name"]) if (p.info["name"] or "").upper().startswith("FLOPRO")}


def dialog_text(win):
    parts = []
    try:
        for c in win.descendants():
            try:
                t = c.window_text()
                if t:
                    parts.append(t)
            except Exception:
                pass
    except Exception:
        pass
    return " | ".join(parts)


def log_row(logdir, row):
    path = os.path.join(logdir, "dialog_log.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "pid", "title", "text", "action", "rule"])
        w.writerow(row)


def answer(win, button):
    if button:
        try:
            win.child_window(title=button, control_type="Button").invoke()
            return f"clicked {button}"
        except Exception:
            pass
    win.set_focus()
    win.type_keys("{ENTER}")
    return "sent Enter"


def poll_once(rules, logdir, seen):
    from pywinauto import Desktop
    pids = flopro_pids()
    if not pids:
        return 0
    n = 0
    for win in Desktop(backend="uia").windows():
        try:
            pid = win.process_id()
        except Exception:
            continue
        if pid not in pids:
            continue
        title = win.window_text() or ""
        text = dialog_text(win)
        # The main solver window is not a dialog; only act on small modal windows with buttons.
        try:
            has_button = any(c.element_info.control_type == "Button" for c in win.descendants())
        except Exception:
            has_button = False
        if not has_button:
            continue
        key = (pid, title, text)
        stamp = dt.datetime.now().isoformat(timespec="seconds")
        rule = next((r for r in rules if r["title"].search(title) and r["text"].search(text)), None)
        if rule:
            action = answer(win, rule["button"])
            log_row(logdir, [stamp, pid, title, text, action, rule["id"]])
            n += 1
        elif key not in seen:
            seen.add(key)
            log_row(logdir, [stamp, pid, title, text, "LEFT OPEN - not on benign list", ""])
            stop = {"time": stamp, "pid": pid, "title": title, "text": text,
                    "action_needed": "JCO decision: answer, or stop the run and fix inputs"}
            with open(os.path.join(logdir, f"STOP_{pid}.json"), "w", encoding="utf-8") as f:
                json.dump(stop, f, indent=2)
    return n


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--logdir", required=True)
    ap.add_argument("--benign", default=os.path.join(here, "..", "reference", "known_benign_warnings.json"))
    ap.add_argument("--poll", type=float, default=5.0)
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args(argv)
    if os.name != "nt":
        print("Windows only.")
        return 1
    rules = load_benign(a.benign)
    seen = set()
    while True:
        poll_once(rules, a.logdir, seen)
        if a.once:
            return 0
        if not flopro_pids():
            time.sleep(a.poll * 6)
            if not flopro_pids():
                return 0
        time.sleep(a.poll)


if __name__ == "__main__":
    sys.exit(main())
