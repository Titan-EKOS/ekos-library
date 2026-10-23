"""Word export for the Standard chain: update fields twice, TOC and tables of figures, save, export PDF
with heading bookmarks, optional reduced on-screen copy for email.

Runs in a separate Word instance (DispatchEx), never the user's open Word. Windows + Word + pywin32.

Usage:
  "%DOCS_PY%" word_export.py --docx <draft.docx> --pdf <out.pdf> [--email-pdf <out_email.pdf>]
Exit codes: 0 ok, 2 environment error.
"""
import argparse
import sys
from pathlib import Path

WD_EXPORT_PDF = 17
WD_OPTIMIZE_PRINT = 0
WD_OPTIMIZE_SCREEN = 1
WD_BOOKMARKS_HEADINGS = 1


def export(docx: Path, pdf: Path, email_pdf: Path | None) -> None:
    try:
        import win32com.client  # type: ignore
    except ImportError:
        sys.exit("pywin32 not available: word_export needs Windows, Word and pywin32")
    wd = win32com.client.DispatchEx("Word.Application")
    try:
        wd.Visible = False
        wd.DisplayAlerts = 0
        doc = wd.Documents.Open(str(docx.resolve()), ConfirmConversions=False, ReadOnly=False, AddToRecentFiles=False)
        try:
            for _ in range(2):  # twice: chapter-dash captions and REF fields settle on the second pass
                doc.Fields.Update()
                for i in range(1, doc.TablesOfContents.Count + 1):
                    doc.TablesOfContents(i).Update()
                for i in range(1, doc.TablesOfFigures.Count + 1):
                    doc.TablesOfFigures(i).Update()
                for s in range(1, doc.Sections.Count + 1):
                    sec = doc.Sections(s)
                    for coll in (sec.Headers, sec.Footers):
                        for k in (1, 2, 3):
                            try:
                                coll(k).Range.Fields.Update()
                            except Exception:
                                pass
            doc.Save()
            doc.ExportAsFixedFormat(OutputFileName=str(pdf.resolve()), ExportFormat=WD_EXPORT_PDF,
                                    OpenAfterExport=False, OptimizeFor=WD_OPTIMIZE_PRINT,
                                    CreateBookmarks=WD_BOOKMARKS_HEADINGS, DocStructureTags=True,
                                    BitmapMissingFonts=True, UseISO19005_1=False)
            if email_pdf:
                doc.ExportAsFixedFormat(OutputFileName=str(email_pdf.resolve()), ExportFormat=WD_EXPORT_PDF,
                                        OpenAfterExport=False, OptimizeFor=WD_OPTIMIZE_SCREEN,
                                        CreateBookmarks=WD_BOOKMARKS_HEADINGS, DocStructureTags=True)
        finally:
            doc.Close(SaveChanges=False)
    finally:
        wd.Quit()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docx", required=True, type=Path)
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--email-pdf", type=Path)
    a = ap.parse_args(argv)
    if not a.docx.exists():
        print(f"missing docx: {a.docx}", file=sys.stderr)
        return 2
    export(a.docx, a.pdf, a.email_pdf)
    print(f"exported {a.pdf}" + (f" and {a.email_pdf}" if a.email_pdf else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
