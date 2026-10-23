#!/usr/bin/env python3
"""
package_qc.py -- pre-upload QC gate for a FEMA CLOMR/LOMR FLO-2D model package
(fema-clomr-lomr v1, RPT-C13; checks from STARVALLEY-004, STARVALLEY-001, STARVALLEY-020).

FAIL on any check = do not zip, do not upload, do not state the item complete in a letter.

Per model folder:
  B1 build strings agree: FLOPRO.exe build = CONT.DAT line 1 build = SUMMARY.OUT build
  B2 DLL set present and identical to the reference folder (first model given)
  F1 required inputs/outputs present (channel files when CHAN.DAT is present or --ichannel)
  F2 zero *.TMP files
  F3 oldest output newer than newest input
  F4 SUMMARY.OUT shows a completed run and a volume conservation line
  F5 every text .DAT/.RGH uses CRLF line endings (NEIGHBORS.DAT skipped)
Across models:
  X1 shared boundary files identical by SHA-256 (CADPTS, INFLOW, OUTFLOW, FPXSEC, TOLER, RAIN)
Package level:
  G1 flood zone and BFE contour shapefiles present for every condition (--gis)
  D1 no placeholders or code fragments in DOCX/XLSX/TXT/MD documents (--docs)
Manual (listed in the report, not automated): HYSTRUC rating tables = HY-8 export.

Usage (EKOS, venv python by full path):
  "%DOCS_PY%" package_qc.py ^
     --model DUPEFF=D:\\...\\DupEff --model EXIST=D:\\...\\Existing --model PROP=D:\\...\\Proposed ^
     --gis D:\\...\\GIS --docs D:\\...\\Report --out package_QC_report.txt
Exit code: 0 = PASS, 1 = FAIL.
"""
import argparse
import glob
import hashlib
import os
import re
import sys
import zipfile

BUILD_RE = re.compile(rb"(\d{2}\.\d{2}\.\d{2})")
INPUT_NAMES = {"CONT.DAT", "TOPO.DAT", "MANNINGS_N.DAT", "FPLAIN.DAT", "CADPTS.DAT", "INFLOW.DAT",
               "OUTFLOW.DAT", "TOLER.DAT", "RAIN.DAT", "FPXSEC.DAT", "HYSTRUC.DAT", "CHAN.DAT",
               "CHANBANK.DAT", "XSEC.DAT", "ARF.DAT", "INFIL.DAT", "NEIGHBORS.DAT"}
REQ_OUT = ["MAXWSELEV.OUT", "DEPTH.OUT", "SUMMARY.OUT", "ERROR.CHK"]
REQ_OUT_CHAN = ["CHANMAX.OUT", "CROSSMAX.OUT"]
REQ_IN_CHAN = ["CHAN.DAT", "CHANBANK.DAT", "XSEC.DAT"]
SHARED = ["CADPTS.DAT", "INFLOW.DAT", "OUTFLOW.DAT", "FPXSEC.DAT", "TOLER.DAT", "RAIN.DAT"]
PLACEHOLDER_RE = re.compile(
    r"\[(?:DATE|TBD|TO BE CONFIRMED|TO BE DETERMINED|INSERT[^\]]*|XX+|PLACEHOLDER[^\]]*|NOTE[^\]]*)\]"
    r"|\bTBD\b|\bTO BE CONFIRMED\b|\{\{.*?\}\}|\{[a-z_]+\}"
    r"|\bif\s+[\w.\[\]']+\s*(?:==|!=|>=|<=|>|<|is not|is|not in|in)\s*\S+\s+else\b|(?-i:\bnan\b)|Traceback|\bdef \w+\(",
    re.I)


def fpath(folder, name):
    """Case-insensitive file lookup."""
    for f in os.listdir(folder):
        if f.upper() == name.upper():
            return os.path.join(folder, f)
    return None


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def first_build(p, nbytes=None, first_line=False):
    if not p:
        return None
    with open(p, "rb") as fh:
        data = fh.readline() if first_line else fh.read(nbytes or -1)
    m = BUILD_RE.search(data)
    return m.group(1).decode() if m else None


def exe_build(p):
    """Find a build string near the word 'Build' in the executable; else the first dd.dd.dd."""
    if not p:
        return None
    with open(p, "rb") as fh:
        data = fh.read()
    m = re.search(rb"[Bb]uild[^0-9]{0,12}(\d{2}\.\d{2}\.\d{2})", data)
    if m:
        return m.group(1).decode()
    m = BUILD_RE.search(data)
    return m.group(1).decode() if m else None


class Report:
    def __init__(self):
        self.lines, self.fail = [], 0

    def add(self, ok, code, where, msg):
        status = "PASS" if ok else "FAIL"
        if not ok:
            self.fail += 1
        self.lines.append(f"{status}  {code:<3} {where:<12} {msg}")

    def note(self, text):
        self.lines.append(text)


def check_model(name, folder, rep, ref_dlls, force_chan):
    files = os.listdir(folder)
    up = {f.upper(): f for f in files}
    # B1 build strings
    exe = fpath(folder, "FLOPRO.exe")
    b_exe = exe_build(exe)
    b_cont = first_build(fpath(folder, "CONT.DAT"), first_line=True)
    b_sum = first_build(fpath(folder, "SUMMARY.OUT"), nbytes=4096)
    ok = None not in (b_exe, b_cont, b_sum) and b_exe == b_cont == b_sum
    rep.add(ok, "B1", name, f"build exe={b_exe} CONT.DAT={b_cont} SUMMARY.OUT={b_sum}")
    # B2 DLLs
    dlls = sorted(f.upper() for f in files if f.upper().endswith(".DLL"))
    if ref_dlls is None:
        rep.add(bool(dlls), "B2", name, f"{len(dlls)} DLL(s) (reference set)")
    else:
        missing = sorted(set(ref_dlls) - set(dlls))
        rep.add(not missing and bool(dlls), "B2", name,
                f"{len(dlls)} DLL(s)" + (f"; missing {missing}" if missing else ""))
    # F1 required files
    chan = force_chan or "CHAN.DAT" in up
    req = REQ_OUT + (REQ_OUT_CHAN + REQ_IN_CHAN if chan else [])
    hy = "HYSTRUC.DAT" in up
    if hy:
        req = req + ["HYDROSTRUCT.OUT"]
    missing = [r for r in req if r not in up]
    rep.add(not missing, "F1", name, "required files present" if not missing else f"missing {missing}")
    # F2 TMP
    tmps = [f for f in files if f.upper().endswith(".TMP")]
    rep.add(not tmps, "F2", name, f"{len(tmps)} TMP file(s)" + (f": {tmps[:5]}" if tmps else ""))
    # F3 chronology
    ins = [os.path.join(folder, up[n]) for n in INPUT_NAMES if n in up]
    outs = [os.path.join(folder, f) for f in files if f.upper().endswith(".OUT") or f.upper() == "ERROR.CHK"]
    if ins and outs:
        newest_in = max(ins, key=os.path.getmtime)
        oldest_out = min(outs, key=os.path.getmtime)
        ok = os.path.getmtime(oldest_out) > os.path.getmtime(newest_in)
        rep.add(ok, "F3", name, f"oldest output {os.path.basename(oldest_out)} vs newest input "
                                f"{os.path.basename(newest_in)}")
    else:
        rep.add(False, "F3", name, "no outputs" if ins else "no inputs found")
    # F4 SUMMARY.OUT completion and volume conservation
    sp = fpath(folder, "SUMMARY.OUT")
    txt = open(sp, errors="ignore").read() if sp else ""
    done = bool(re.search(r"normal\s+termination|simulation\s+(?:is\s+)?complete|completed", txt, re.I))
    vol = re.search(r"volume\s+conservation[^\n]*", txt, re.I)
    rep.add(done and bool(vol), "F4", name,
            f"completed={done}; " + (vol.group(0).strip()[:80] if vol else "no volume conservation line"))
    # F5 CRLF
    bad = []
    for f in files:
        u = f.upper()
        if (u.endswith(".DAT") or u.endswith(".RGH")) and u != "NEIGHBORS.DAT":
            data = open(os.path.join(folder, f), "rb").read()
            if re.search(rb"(?<!\r)\n", data):
                bad.append(f)
    rep.add(not bad, "F5", name, "CRLF line endings" if not bad else f"bare LF in {bad[:6]}")
    return dlls


def check_shared(models, rep):
    for fn in SHARED:
        hashes = {}
        for name, folder in models:
            p = fpath(folder, fn)
            hashes[name] = sha256(p)[:12] if p else None
        present = {k: v for k, v in hashes.items() if v}
        if not present:
            rep.note(f"INFO  X1  {fn:<12} not present in any model")
            continue
        ok = len(present) == len(models) and len(set(present.values())) == 1
        rep.add(ok, "X1", fn, " ".join(f"{k}={v}" for k, v in hashes.items()))


def check_gis(gis, conditions, rep):
    shps = [os.path.basename(p).upper() for p in glob.glob(os.path.join(gis, "**", "*.shp"), recursive=True)]
    for cond in conditions:
        c = cond.upper()
        zone = any(c in s and "ZONE" in s for s in shps)
        bfe = any(c in s and "BFE" in s for s in shps)
        rep.add(zone and bfe, "G1", cond, f"zone shapefile={zone} BFE contour shapefile={bfe}")


def doc_text(p):
    ext = os.path.splitext(p)[1].lower()
    try:
        if ext in (".docx", ".xlsx"):
            with zipfile.ZipFile(p) as z:
                parts = [n for n in z.namelist() if n.endswith(".xml") and
                         (n.startswith("word/") or n.startswith("xl/sharedStrings") or n.startswith("xl/worksheets"))]
                xml = " ".join(z.read(n).decode("utf8", "ignore") for n in parts)
            # join runs: drop tags, keep text
            return re.sub(r"<[^>]+>", "", re.sub(r"</w:p>|</si>|</row>", "\n", xml))
        if ext in (".txt", ".md", ".csv"):
            return open(p, errors="ignore").read()
    except (zipfile.BadZipFile, OSError) as e:
        return f"__UNREADABLE__ {e}"
    return ""


def check_docs(docs, rep):
    files = [p for p in glob.glob(os.path.join(docs, "**", "*"), recursive=True)
             if os.path.splitext(p)[1].lower() in (".docx", ".xlsx", ".txt", ".md")
             and not os.path.basename(p).startswith("~$")
             and os.path.basename(p).lower() != "package_qc_report.txt"]
    for p in files:
        txt = doc_text(p)
        hits = sorted({m.group(0)[:40] for m in PLACEHOLDER_RE.finditer(txt)})
        rep.add(not hits and not txt.startswith("__UNREADABLE__"), "D1",
                os.path.basename(p)[:12], "clean" if not hits else f"found {hits[:6]} ({os.path.basename(p)})")


def main(argv=None):
    ap = argparse.ArgumentParser(description="FEMA CLOMR/LOMR FLO-2D package QC gate")
    ap.add_argument("--model", action="append", required=True, metavar="NAME=FOLDER",
                    help="model folder; first one is the DLL reference (use duplicate effective)")
    ap.add_argument("--ichannel", action="store_true", help="require channel files in every model")
    ap.add_argument("--gis", help="GIS package folder (zone and BFE shapefiles named with condition)")
    ap.add_argument("--docs", help="report/matrix/letter folder to scan for placeholders")
    ap.add_argument("--out", default="package_QC_report.txt")
    a = ap.parse_args(argv)

    models = []
    for m in a.model:
        name, _, folder = m.partition("=")
        if not folder or not os.path.isdir(folder):
            sys.exit(f"bad --model {m}")
        models.append((name, folder))

    rep = Report()
    rep.note("FEMA CLOMR/LOMR package QC report")
    rep.note("Models: " + "; ".join(f"{n} = {f}" for n, f in models))
    rep.note("")
    ref = None
    for name, folder in models:
        d = check_model(name, folder, rep, ref, a.ichannel)
        ref = d if ref is None else ref
    check_shared(models, rep)
    if a.gis:
        check_gis(a.gis, [n for n, _ in models], rep)
    else:
        rep.note("SKIP  G1  no --gis folder given")
    if a.docs:
        check_docs(a.docs, rep)
    else:
        rep.note("SKIP  D1  no --docs folder given")
    rep.note("")
    rep.note("MANUAL  HYSTRUC rating tables equal the HY-8 export (names, discharge pairs, headwater "
             "reference offset): record result here")
    rep.note("")
    rep.note(f"RESULT: {'PASS' if rep.fail == 0 else 'FAIL'} ({rep.fail} failed check(s))")
    with open(a.out, "w", newline="\r\n") as fh:
        fh.write("\n".join(rep.lines) + "\n")
    print("\n".join(rep.lines))
    print("WROTE", a.out)
    return 0 if rep.fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
