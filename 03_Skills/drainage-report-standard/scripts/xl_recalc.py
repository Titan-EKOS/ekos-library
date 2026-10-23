"""Native Excel recalculation and semantic compare for the Standard workbook (decision D51).

recalc : private Excel instance (DispatchEx), hidden, events/macros/link updates off,
         CalculateFullRebuild, save, close only that instance. Windows + Excel + pywin32.
compare: semantic compare of a workbook before and after recalc (openpyxl): formulas unchanged,
         input values unchanged, defined names, merged ranges, validation count, new formula errors.

Usage (EKOS, documents venv by full path):
  "%DOCS_PY%" xl_recalc.py recalc  --workbook <wb.xlsx> [--keep-copy <before.xlsx>] [--json <out.json>]
  "%DOCS_PY%" xl_recalc.py compare --before <before.xlsx> --after <after.xlsx> [--json <out.json>]
recalc with --keep-copy saves the pre-recalc copy and runs compare automatically.
Exit codes: 0 ok, 1 compare found problems, 2 usage / environment error.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ERRORS = ("#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#NULL!", "#SPILL!", "#CALC!")


def recalc(path: Path) -> None:
    try:
        import win32com.client  # type: ignore
    except ImportError:
        sys.exit("pywin32 not available: recalc needs Windows, Excel and pywin32 in this environment")
    xl = win32com.client.DispatchEx("Excel.Application")  # private instance, never the user's session
    try:
        xl.Visible = False
        xl.DisplayAlerts = False
        xl.ScreenUpdating = False
        xl.EnableEvents = False
        xl.AskToUpdateLinks = False
        try:
            xl.AutomationSecurity = 3  # msoAutomationSecurityForceDisable: macros off
        except Exception:
            pass
        wb = xl.Workbooks.Open(str(path.resolve()), UpdateLinks=0, ReadOnly=False)
        try:
            xl.CalculateFullRebuild()
            wb.Save()
        finally:
            wb.Close(SaveChanges=False)
    finally:
        xl.Quit()


def _load(path: Path, data_only: bool):
    from openpyxl import load_workbook
    return load_workbook(path, data_only=data_only)


def compare(before: Path, after: Path) -> dict:
    fb, fa = _load(before, False), _load(after, False)
    vb, va = _load(before, True), _load(after, True)
    out = {"before": str(before), "after": str(after), "formula_changes": [], "input_changes": [],
           "new_errors": [], "sheets_added": [], "sheets_removed": [], "names_added": [], "names_removed": [],
           "merged_changes": [], "validation_count": {}}
    sb, sa = set(fb.sheetnames), set(fa.sheetnames)
    out["sheets_added"], out["sheets_removed"] = sorted(sa - sb), sorted(sb - sa)
    nb, na = set(fb.defined_names.keys()), set(fa.defined_names.keys())
    out["names_added"], out["names_removed"] = sorted(na - nb), sorted(nb - na)
    for name in sorted(sb & sa):
        wsb, wsa = fb[name], fa[name]
        mb = {str(r) for r in wsb.merged_cells.ranges}
        ma = {str(r) for r in wsa.merged_cells.ranges}
        if mb != ma:
            out["merged_changes"].append({"sheet": name, "added": sorted(ma - mb), "removed": sorted(mb - ma)})
        # Excel merges adjacent validation ranges, so compare the count of validation rules only as information.
        out["validation_count"][name] = [len(wsb.data_validations.dataValidation),
                                         len(wsa.data_validations.dataValidation)]
        max_r = max(wsb.max_row, wsa.max_row)
        max_c = max(wsb.max_column, wsa.max_column)
        for row in range(1, max_r + 1):
            for col in range(1, max_c + 1):
                cb, ca = wsb.cell(row, col).value, wsa.cell(row, col).value
                is_fb = isinstance(cb, str) and cb.startswith("=")
                is_fa = isinstance(ca, str) and ca.startswith("=")
                ref = f"{name}!{wsa.cell(row, col).coordinate}"
                if is_fb or is_fa:
                    if cb != ca:
                        out["formula_changes"].append({"cell": ref, "before": cb, "after": ca})
                    valb = vb[name].cell(row, col).value
                    vala = va[name].cell(row, col).value
                    if isinstance(vala, str) and vala in ERRORS and not (isinstance(valb, str) and valb in ERRORS):
                        out["new_errors"].append({"cell": ref, "value": vala})
                elif cb != ca:
                    out["input_changes"].append({"cell": ref, "before": cb, "after": ca})
    out["ok"] = not (out["formula_changes"] or out["input_changes"] or out["new_errors"]
                     or out["sheets_added"] or out["sheets_removed"] or out["names_removed"] or out["merged_changes"])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("recalc")
    r.add_argument("--workbook", required=True, type=Path)
    r.add_argument("--keep-copy", type=Path, help="save the pre-recalc copy here and compare after")
    r.add_argument("--json", type=Path)
    c = sub.add_parser("compare")
    c.add_argument("--before", required=True, type=Path)
    c.add_argument("--after", required=True, type=Path)
    c.add_argument("--json", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "recalc":
        if not a.workbook.exists():
            print(f"missing workbook: {a.workbook}", file=sys.stderr)
            return 2
        if a.keep_copy:
            shutil.copy2(a.workbook, a.keep_copy)
        recalc(a.workbook)
        print(f"recalculated (CalculateFullRebuild, private instance): {a.workbook}")
        if not a.keep_copy:
            return 0
        res = compare(a.keep_copy, a.workbook)
    else:
        res = compare(a.before, a.after)
    if a.json:
        a.json.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(f"formula changes {len(res['formula_changes'])} | input changes {len(res['input_changes'])} | "
          f"new errors {len(res['new_errors'])} | merged changes {len(res['merged_changes'])} | "
          f"names removed {len(res['names_removed'])} -> {'OK' if res['ok'] else 'CHECK'}")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
