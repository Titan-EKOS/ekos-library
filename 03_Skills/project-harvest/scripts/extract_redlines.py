"""Extract PDF markup annotations (redlines) to CSV for harvest evidence. Read-only on the PDF.

Usage:
  python extract_redlines.py <file.pdf> <out.csv> [--author JCO]

Columns: file, page (1-based), comment_no (per page, in annotation order), subtype, subject, author, contents.
Popups and links are skipped.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from pypdf import PdfReader

SKIP = {"/Popup", "/Link"}


def _s(v) -> str:
    return str(v).replace("\r", " ").replace("\n", " ").strip() if v is not None else ""


def extract(pdf: Path, author: str | None = None) -> list[dict]:
    rows = []
    reader = PdfReader(str(pdf))
    for pno, page in enumerate(reader.pages, start=1):
        annots = page.get("/Annots")
        if not annots:
            continue
        n = 0
        for ref in annots.get_object() if hasattr(annots, "get_object") else annots:
            a = ref.get_object()
            sub = _s(a.get("/Subtype"))
            if sub in SKIP:
                continue
            n += 1
            who = _s(a.get("/T"))
            if author and author.lower() not in who.lower():
                continue
            rows.append({"file": str(pdf), "page": pno, "comment_no": n, "subtype": sub,
                         "subject": _s(a.get("/Subj")), "author": who,
                         "contents": _s(a.get("/Contents"))})
    return rows


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:]]
    author = None
    if "--author" in args:
        i = args.index("--author")
        author = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    if len(args) != 2:
        print(__doc__)
        return 2
    pdf, out = Path(args[0]), Path(args[1])
    rows = extract(pdf, author)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "page", "comment_no", "subtype", "subject",
                                           "author", "contents"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} annotations -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
