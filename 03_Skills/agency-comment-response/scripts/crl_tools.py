"""Comment-response log tools (skill agency-comment-response).

extract : PDF review annotations -> CSV (page, author, subject, subtype, contents); links, popups, empty text-box
          labels and plain shapes without text are dropped.
new-log : build the editable log workbook from one or more sources (CSV from extract, agency xlsx with any number of
          tabs, or a plain CSV with a 'comment' column). Original text, numbers and prior responses are kept unchanged.
check   : pre-issue checks on a filled log: ID counts vs sources, duplicates, blanks, "will" wording, placeholders,
          status/disposition vocabulary (D45), cited section/table/figure numbers present in the current build PDF.

Usage:
  python crl_tools.py extract --pdf marked.pdf --csv out.csv [--prefix R]
  python crl_tools.py new-log --out <Job>_<ReportID>_CommentResponse_<YYYYMMDD>.xlsx --source R=rfcd.xlsx --source J=jco.csv
  python crl_tools.py check --log <log.xlsx> [--pdf <current build.pdf>] [--issue] [--json out.json]
Exit codes: 0 clean, 1 findings, 2 usage error.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

STATUS = ["Addressed", "Partial", "Assumed", "Not Addressed", "Cannot Determine", "Stale"]
DISPOSITION = ["incorporated", "superseded", "no change"]
CATEGORY = ["missing content", "technical error", "engineering content", "exhibits", "formatting", "methodology",
            "editorial"]
TYPES = ["substantive", "copyedit"]
COLUMNS = ["CommentID", "Source", "Reviewer / division", "Document", "Page / sheet", "Original comment",
           "Prior response", "Discipline", "Category", "Type", "Priority", "Response", "Revised location", "Action",
           "Completed by", "Check by", "Status", "Disposition", "Evidence (file + page)", "Decision ref"]
SKIP_SUBTYPES = {"/Link", "/Popup", "/Widget"}
SHAPES = {"/Square", "/Circle", "/Line", "/Polygon", "/PolyLine", "/Ink"}
PLACEHOLDER = re.compile(r"\?|\bTBD\b|\bTBC\b|\bTO BE CONFIRMED\b|\bXX+\b|\[\s*\]|\{[^}]*\}")
WILL = re.compile(r"\bwill\b|\bshall be (?:provided|revised|added)\b", re.I)
REF = re.compile(r"\b(Section|Table|Figure|Exhibit|Appendix)\s+([A-Z]?\d+(?:[.-]\d+)*|[A-Z])\b")


def cmd_extract(a):
    from pypdf import PdfReader
    r = PdfReader(str(a.pdf))
    rows, n = [], 0
    for i, page in enumerate(r.pages, start=1):
        for ref in (page.get("/Annots") or []):
            an = ref.get_object()
            st = an.get("/Subtype")
            text = str(an.get("/Contents") or "").strip()
            if st in SKIP_SUBTYPES:
                continue
            if st in SHAPES and not text:
                continue
            if st == "/FreeText" and not text:
                continue
            if not text and st not in ("/Highlight", "/StrikeOut", "/Underline", "/Caret"):
                continue
            n += 1
            rows.append({"id": f"{a.prefix}-{n:02d}", "page": i, "author": str(an.get("/T") or ""),
                         "subject": str(an.get("/Subj") or ""), "subtype": str(st), "comment": text})
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "page", "author", "subject", "subtype", "comment"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} comments extracted from {a.pdf} -> {a.csv}")
    return 0


def _read_source(path):
    """Yield dicts with keys id, page, author, document, comment, prior from csv or every tab of an xlsx."""
    p = Path(path)
    if p.suffix.lower() == ".csv":
        with open(p, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                yield {k.lower().strip(): (v or "").strip() for k, v in row.items() if k}
        return
    from openpyxl import load_workbook
    wb = load_workbook(p, data_only=True, read_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        hdr_i = next((i for i, r in enumerate(rows[:15]) if any(isinstance(c, str) and "comment" in c.lower() for c in r)), None)
        if hdr_i is None:
            continue
        hdr = [str(c or "").strip().lower() for c in rows[hdr_i]]
        for r in rows[hdr_i + 1:]:
            d = {hdr[j]: ("" if v is None else str(v).strip()) for j, v in enumerate(r) if j < len(hdr) and hdr[j]}
            d["_tab"] = ws.title
            yield d


def _pick(d, *keys):
    for k in d:
        for want in keys:
            if want in k:
                if d[k]:
                    return d[k]
    return ""


def cmd_new_log(a):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    wb = Workbook()
    ws = wb.active
    ws.title = "Log"
    ws.append(COLUMNS)
    thin = Side(style="thin")
    src_rows = []
    for spec in a.source:
        if "=" not in spec:
            print(f"--source must be PREFIX=path: {spec}", file=sys.stderr)
            return 2
        prefix, path = spec.split("=", 1)
        count = 0
        for d in _read_source(path):
            comment = _pick(d, "comment", "contents", "remark")
            if not comment:
                continue
            count += 1
            orig_id = _pick(d, "id", "no", "number", "#")
            tab = f"{d['_tab'][:3].upper()}-" if d.get("_tab") else ""
            if orig_id.startswith(f"{prefix}-"):
                cid = orig_id
            else:
                cid = f"{prefix}-{tab}{orig_id}" if orig_id else f"{prefix}-{tab}{count:02d}"
            ws.append([cid, Path(path).name + (f" [{d['_tab']}]" if d.get("_tab") else ""),
                       _pick(d, "author", "reviewer", "division", "agency") or d.get("_tab", ""),
                       _pick(d, "document", "file"), _pick(d, "page", "sheet"), comment,
                       _pick(d, "prior", "previous response", "response"), "", "", "", "", "", "", "", "", "", "", "",
                       "", ""])
        src_rows.append([prefix, str(path), count])
    n = ws.max_row
    for col, values in (("Q", STATUS), ("R", DISPOSITION), ("I", CATEGORY), ("J", TYPES),
                        ("H", ["drainage", "other discipline"])):
        dv = DataValidation(type="list", formula1='"' + ",".join(values) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col}2:{col}{max(n, 2) + 200}")
    for c in ws[1]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=1, max_row=n):
        for c in row:
            c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
            c.alignment = Alignment(wrap_text=True, vertical="top")
    widths = [10, 18, 16, 14, 8, 60, 30, 12, 16, 12, 8, 60, 18, 18, 10, 10, 14, 13, 24, 10]
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "B2"
    s = wb.create_sheet("Sources")
    s.append(["Prefix", "Source file", "Comment count at import"])
    for r in src_rows:
        s.append(r)
    dsh = wb.create_sheet("Decisions")
    dsh.append(["Decision ref", "Comment IDs", "Agency direction or conflict", "JCO decision", "Date", "Effect"])
    lst = wb.create_sheet("Lists")
    lst.append(["Status", "Disposition", "Category"])
    for i in range(max(len(STATUS), len(CATEGORY))):
        lst.append([STATUS[i] if i < len(STATUS) else None, DISPOSITION[i] if i < len(DISPOSITION) else None,
                    CATEGORY[i] if i < len(CATEGORY) else None])
    wb.save(a.out)
    print(f"log written: {a.out} ({n - 1} comments; " + ", ".join(f"{p}={c}" for p, _, c in src_rows) + ")")
    return 0


def cmd_check(a):
    from openpyxl import load_workbook
    wb = load_workbook(a.log, data_only=True)
    ws = wb["Log"]
    hdr = [c.value for c in ws[1]]
    idx = {h: i for i, h in enumerate(hdr)}
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if any(v not in (None, "") for v in r)]
    f = {"count_mismatch": [], "duplicates": [], "blank": [], "will": [], "placeholders": [], "vocabulary": [],
         "unresolved_refs": [], "addressed_without_response": []}
    ids = [str(r[idx["CommentID"]]) for r in rows]
    seen = set()
    for i in ids:
        if i in seen:
            f["duplicates"].append(i)
        seen.add(i)
    if "Sources" in wb.sheetnames:
        for pre, path, cnt in wb["Sources"].iter_rows(min_row=2, values_only=True):
            if pre is None:
                continue
            got = sum(1 for i in ids if i.startswith(f"{pre}-"))
            if cnt is not None and got != int(cnt):
                f["count_mismatch"].append(f"{pre}: {got} rows vs {cnt} in source {path}")
    build_text = ""
    if a.pdf:
        from pypdf import PdfReader
        build_text = " ".join((p.extract_text() or "") for p in PdfReader(str(a.pdf)).pages)
        build_text = re.sub(r"\s+", " ", build_text)
    required = ["Response", "Status", "Disposition"] + (["Completed by", "Check by", "Revised location"] if a.issue else [])
    for r in rows:
        cid = r[idx["CommentID"]]
        if str(r[idx.get("Discipline", 0)] or "").lower() == "other discipline":
            continue
        for col in required:
            if r[idx[col]] in (None, ""):
                if col == "Revised location" and str(r[idx["Disposition"]] or "") == "no change":
                    continue
                f["blank"].append(f"{cid}: {col}")
        resp = str(r[idx["Response"]] or "")
        if WILL.search(resp):
            f["will"].append(f"{cid}: {WILL.search(resp).group(0)}")
        for col in ("Response", "Revised location"):
            v = str(r[idx[col]] or "")
            m = PLACEHOLDER.search(v)
            if m:
                f["placeholders"].append(f"{cid} {col}: '{m.group(0)}'")
        st, di = r[idx["Status"]], r[idx["Disposition"]]
        if st not in (None, "") and st not in STATUS:
            f["vocabulary"].append(f"{cid}: status '{st}'")
        if di not in (None, "") and di not in DISPOSITION:
            f["vocabulary"].append(f"{cid}: disposition '{di}'")
        if st == "Addressed" and not resp.strip():
            f["addressed_without_response"].append(str(cid))
        if build_text:
            for kind, num in REF.findall(resp + " " + str(r[idx["Revised location"]] or "")):
                pat = rf"\b{re.escape(num)}\b" if kind == "Section" else rf"\b{kind}\s+{re.escape(num)}\b"
                if not re.search(pat, build_text, re.I):
                    f["unresolved_refs"].append(f"{cid}: {kind} {num} not found in current build")
    total = sum(len(v) for v in f.values())
    if a.json:
        Path(a.json).write_text(json.dumps(f, indent=1), encoding="utf-8")
    print(f"{len(rows)} rows | " + " | ".join(f"{k} {len(v)}" for k, v in f.items()) + f" -> {'CLEAN' if not total else 'FINDINGS'}")
    for k, v in f.items():
        for x in v[:50]:
            print(f"  [{k}] {x}")
    return 0 if not total else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--pdf", required=True, type=Path)
    e.add_argument("--csv", required=True, type=Path)
    e.add_argument("--prefix", default="C")
    n = sub.add_parser("new-log")
    n.add_argument("--out", required=True, type=Path)
    n.add_argument("--source", action="append", required=True, help="PREFIX=path (.csv or .xlsx)")
    c = sub.add_parser("check")
    c.add_argument("--log", required=True, type=Path)
    c.add_argument("--pdf", type=Path, help="current build PDF for displayed-number checks")
    c.add_argument("--issue", action="store_true", help="also require Completed by, Check by, Revised location")
    c.add_argument("--json", type=Path)
    a = ap.parse_args(argv)
    return {"extract": cmd_extract, "new-log": cmd_new_log, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
