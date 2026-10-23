"""Manifest-driven compiled report PDF with bookmarks, link check, annotation policy, size gate and QA JSON.

Library helper for the Standard v0.3 chain until compile_report.py ships in the package (v0.4 change spec CS-09).
Decisions applied: D48 (annotations), D50 (placeholder pages only for named items), D52 (bookmarks, size).

build : python compile_pdf.py build --manifest compile_manifest.json [--split]
check : python compile_pdf.py check --pdf <file.pdf> [--require "^Cover$" --require "Table of Contents"] [--limit-mb 50]

Manifest (JSON):
{
  "output": "<...>/30_Report/Issued/<YYYYMMDD>_<Milestone>/<Job>_<ReportID>_<Milestone>_<YYYYMMDD>.pdf",
  "qa_json": "<...>/40_QC/<Job>_<ReportID>_compile_QA_<YYYYMMDD>.json",       (optional; default beside output)
  "size_limit_mb": 50,                     (D52: 50 MB or the agency limit if lower)
  "required_bookmarks": ["^Cover$", "^Table of Contents$", "^1\\.0", "^Appendix A"],   (regex list, optional)
  "entries": [
    {"file": "body.pdf", "pages": "1-18", "import_outline": true},
    {"file": "Fig4-1_Proposed_Drainage_20261022.pdf", "bookmark": "Figure 4-1 Proposed Conditions Drainage Map", "level": 1},
    {"file": "body.pdf", "pages": "19-40", "import_outline": true},
    {"file": "PCHydro_CP1.pdf", "bookmark": "CP-1 PC-Hydro Output", "level": 1, "annotations": "must-be-flat"},
    {"file": "PlanSheets_marked.pdf", "bookmark": "Appendix K Plan Sheets", "level": 0, "annotations": "remove-clouds"},
    {"placeholder": "Appendix L - Agency comment forms (named item)", "bookmark": "Appendix L Correspondence", "level": 0}
  ]
}
"pages" is 1-based inclusive ("3", "1-5", "1-3,7"); omitted = all pages. "rotate" (90/180/270) optional.
"annotations": "report" (default, inventory only) | "must-be-flat" (fail if markups remain; flatten in the PDF
reader first, originals kept) | "remove-clouds" (drop inherited revision clouds) | "strip-markups" (drop all markups).
Exit codes: 0 pass, 1 checks failed, 2 usage error.
"""
import argparse
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, NameObject

MARKUP_SKIP = {"/Link", "/Widget", "/Popup"}


def parse_pages(spec, n):
    if not spec:
        return list(range(n))
    out = []
    for part in str(spec).split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a) - 1, int(b)))
        else:
            out.append(int(part) - 1)
    bad = [p + 1 for p in out if p < 0 or p >= n]
    if bad:
        raise ValueError(f"pages {bad} outside 1-{n}")
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_cloud(annot):
    be = annot.get("/BE")
    if be is not None and be.get_object().get("/S") == "/C":
        return True
    return annot.get("/IT") in ("/PolygonCloud",)


def annot_policy(page, policy):
    """Apply policy to one page; return (inventory dict, removed count, remaining markups)."""
    inv, removed, remaining = {}, 0, 0
    annots = page.get("/Annots")
    if annots is None:
        return inv, 0, 0
    annots = annots.get_object()
    keep = ArrayObject()
    for ref in annots:
        a = ref.get_object()
        st = a.get("/Subtype", "/Unknown")
        inv[st] = inv.get(st, 0) + 1
        markup = st not in MARKUP_SKIP
        drop = (policy == "remove-clouds" and is_cloud(a)) or (policy == "strip-markups" and markup)
        if drop:
            removed += 1
            continue
        if markup:
            remaining += 1
        keep.append(ref)
    page[NameObject("/Annots")] = keep
    return inv, removed, remaining


def placeholder_page(label):
    if not label or not label.strip():
        raise ValueError("placeholder pages need a label naming the item that follows (D50)")
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(letter[0] / 2, letter[1] / 2, label.strip())
    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf)


def flatten_outline(reader, items=None, depth=0):
    out = []
    items = reader.outline if items is None else items
    last = None
    for it in items:
        if isinstance(it, list):
            if last is not None:
                out += flatten_outline(reader, it, depth + 1)
            continue
        try:
            pg = reader.get_destination_page_number(it)
        except Exception:
            pg = None
        out.append((depth, pg, str(it.title)))
        last = it
    return out


def build_tree(nodes):
    """nodes: list of (level, out_page, title). Attach each node to the latest node one level up whose page <= its
    page, then sort siblings by page (fixes appendix order by page, CALFIRE-014)."""
    nodes = sorted(nodes, key=lambda n: (n[1], n[0]))
    roots, stack_by_level = [], {}
    for lvl, pg, title in nodes:
        node = {"title": title, "page": pg, "children": []}
        parent = None
        for up in range(lvl - 1, -1, -1):
            if up in stack_by_level:
                parent = stack_by_level[up]
                break
        (parent["children"] if parent else roots).append(node)
        stack_by_level[lvl] = node
        for deeper in [k for k in stack_by_level if k > lvl]:
            del stack_by_level[deeper]

    def srt(lst):
        lst.sort(key=lambda n: n["page"])
        for n in lst:
            srt(n["children"])
    srt(roots)
    return roots


def add_tree(writer, tree, parent=None):
    for n in tree:
        ref = writer.add_outline_item(n["title"], n["page"], parent=parent)
        add_tree(writer, n["children"], ref)


def page_text_hash(page):
    try:
        t = re.sub(r"\s+", " ", page.extract_text() or "").strip()
    except Exception:
        t = ""
    return hashlib.md5(t.encode("utf-8", "ignore")).hexdigest(), len(t)


def check_pdf(path, required=(), limit_mb=None):
    r = PdfReader(str(path))
    res = {"pdf": str(path), "pages": len(r.pages), "size_mb": round(Path(path).stat().st_size / 1e6, 2),
           "bookmarks": [], "order_issues": [], "missing_required": [], "links_checked": 0, "broken_links": [],
           "uri_links": 0, "annotations": {}}
    flat = flatten_outline(r)
    res["bookmarks"] = [{"level": d, "page": (p + 1 if p is not None else None), "title": t} for d, p, t in flat]
    for d, p, t in flat:
        if p is None:
            res["broken_links"].append(f"bookmark without target: {t}")
    # siblings sorted by page
    last_at_level = {}
    for d, p, t in flat:
        for k in [k for k in last_at_level if k > d]:
            del last_at_level[k]
        if p is not None and d in last_at_level and last_at_level[d][0] is not None and p < last_at_level[d][0]:
            res["order_issues"].append(f"'{t}' (p {p + 1}) listed after '{last_at_level[d][1]}' (p {last_at_level[d][0] + 1})")
        last_at_level[d] = (p, t)
    titles = [t for _, _, t in flat]
    for rx in required:
        if not any(re.search(rx, t) for t in titles):
            res["missing_required"].append(rx)
    page_ids = {pg.indirect_reference.idnum for pg in r.pages if pg.indirect_reference is not None}
    named = r.named_destinations
    for i, pg in enumerate(r.pages):
        for ref in (pg.get("/Annots") or []):
            a = ref.get_object()
            st = a.get("/Subtype", "/Unknown")
            res["annotations"][st] = res["annotations"].get(st, 0) + 1
            if st != "/Link":
                continue
            dest = a.get("/Dest")
            act = a.get("/A")
            if act is not None:
                act = act.get_object()
                if act.get("/S") == "/URI":
                    res["uri_links"] += 1
                    continue
                if act.get("/S") == "/GoTo":
                    dest = act.get("/D")
                elif act.get("/S") is not None:
                    continue
            if dest is None:
                continue
            res["links_checked"] += 1
            dest = dest.get_object() if isinstance(dest, IndirectObject) else dest
            ok = False
            if isinstance(dest, (str,)) or hasattr(dest, "original_bytes"):
                ok = str(dest) in named
            elif isinstance(dest, ArrayObject) and len(dest):
                tgt = dest[0]
                ok = isinstance(tgt, IndirectObject) and tgt.idnum in page_ids
            elif isinstance(dest, NameObject):
                ok = str(dest) in named
            if not ok:
                res["broken_links"].append(f"page {i + 1}: link target does not resolve ({dest!r:.60})")
    res["size_ok"] = limit_mb is None or res["size_mb"] <= limit_mb
    res["ok"] = not (res["order_issues"] or res["missing_required"] or res["broken_links"]) and res["size_ok"]
    return res


def build(manifest_path, split=False):
    m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    base = Path(manifest_path).parent
    out = Path(m["output"])
    out = out if out.is_absolute() else base / out
    qa_path = Path(m.get("qa_json") or out.with_suffix(".qa.json"))
    qa_path = qa_path if qa_path.is_absolute() else base / qa_path
    limit = float(m.get("size_limit_mb", 50))
    w = PdfWriter()
    nodes, qa_entries, fail = [], [], []
    for k, e in enumerate(m["entries"], start=1):
        start = len(w.pages)
        if "placeholder" in e:
            rd, src, used = placeholder_page(e["placeholder"]), "(placeholder)", [0]
            digest = None
        else:
            src = Path(e["file"])
            src = src if src.is_absolute() else base / src
            rd = PdfReader(str(src))
            used = parse_pages(e.get("pages"), len(rd.pages))
            digest = sha256(src)
        w.append(rd, pages=used, import_outline=False)
        policy = e.get("annotations", "report")
        ent = {"n": k, "source": str(src), "sha256": digest, "source_pages": [p + 1 for p in used],
               "output_pages": [start + 1, len(w.pages)], "annotation_policy": policy, "annotations": {},
               "removed_annotations": 0, "page_checks": []}
        for j, sp in enumerate(used):
            op = w.pages[start + j]
            if e.get("rotate"):
                op.rotate(int(e["rotate"]))
            inv, removed, remaining = annot_policy(op, policy)
            for kk, vv in inv.items():
                ent["annotations"][kk] = ent["annotations"].get(kk, 0) + vv
            ent["removed_annotations"] += removed
            if policy == "must-be-flat" and remaining:
                fail.append(f"entry {k} page {sp + 1}: {remaining} markup annotation(s) not flattened")
            s_page = rd.pages[sp]
            s_links = sum(1 for x in (s_page.get("/Annots") or []) if x.get_object().get("/Subtype") == "/Link")
            o_links = sum(1 for x in (op.get("/Annots") or []) if x.get_object().get("/Subtype") == "/Link")
            if o_links < s_links:
                fail.append(f"entry {k} page {sp + 1}: {s_links - o_links} link(s) dropped (target page not in the compile)")
            sh, sl = page_text_hash(s_page)
            oh, ol = page_text_hash(op)
            sbox = [round(float(x), 1) for x in s_page.mediabox]
            obox = [round(float(x), 1) for x in op.mediabox]
            same = sh == oh and sbox == obox
            ent["page_checks"].append({"src": sp + 1, "out": start + j + 1, "text_chars": [sl, ol],
                                       "mediabox_same": sbox == obox, "text_same": sh == oh})
            if not same:
                fail.append(f"entry {k} page {sp + 1}: output page differs from source")
        if e.get("bookmark"):
            nodes.append((int(e.get("level", 0)), start, e["bookmark"]))
        if e.get("import_outline") and "file" in e:
            pos = {p: start + j for j, p in enumerate(used)}
            base_lvl = int(e.get("level", 0))
            for d, pg, title in flatten_outline(rd):
                if pg in pos:
                    nodes.append((base_lvl + d, pos[pg], title))
        qa_entries.append(ent)
    add_tree(w, build_tree(nodes))
    for pg in w.pages:
        try:
            pg.compress_content_streams()
        except Exception:
            pass
    try:
        w.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    except Exception:
        pass
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        w.write(f)
    chk = check_pdf(out, m.get("required_bookmarks", []), limit)
    parts = []
    if not chk["size_ok"] and split:
        parts = split_pdf(out, limit)
    qa = {"manifest": str(manifest_path), "output": str(out), "entries": qa_entries, "check": chk,
          "split_parts": parts, "failures": fail}
    qa_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.write_text(json.dumps(qa, indent=1), encoding="utf-8")
    ok = chk["ok"] and not fail
    print(f"{out}: {chk['pages']} pages, {len(chk['bookmarks'])} bookmarks, {chk['size_mb']} MB (limit {limit}), "
          f"links {chk['links_checked']} broken {len(chk['broken_links'])}, order issues {len(chk['order_issues'])}, "
          f"missing required {len(chk['missing_required'])}, page failures {len(fail)} -> {'PASS' if ok else 'CHECK'}")
    if parts:
        print("split into: " + ", ".join(parts))
    print(f"QA JSON: {qa_path}")
    return 0 if ok or (parts and not fail and not chk["broken_links"] and not chk["order_issues"]) else 1


def split_pdf(path, limit_mb):
    """Split at top-level bookmarks into parts under the size limit."""
    r = PdfReader(str(path))
    tops = sorted({r.get_destination_page_number(it) for it in r.outline if not isinstance(it, list)})
    if not tops or tops[0] != 0:
        tops = [0] + tops
    bounds = tops + [len(r.pages)]
    segs = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1) if bounds[i] < bounds[i + 1]]
    parts, cur = [], []

    def size_of(pages):
        w = PdfWriter()
        for p in pages:
            w.add_page(r.pages[p])
        b = io.BytesIO()
        w.write(b)
        return len(b.getvalue()) / 1e6

    for a, b in segs:
        trial = cur + list(range(a, b))
        if cur and size_of(trial) > limit_mb:
            parts.append(cur)
            cur = list(range(a, b))
        else:
            cur = trial
    if cur:
        parts.append(cur)
    names = []
    for i, pages in enumerate(parts, start=1):
        w = PdfWriter()
        w.append(r, pages=pages, import_outline=False)
        flat = [(d, pg, t) for d, pg, t in flatten_outline(r) if pg in pages]
        pos = {p: j for j, p in enumerate(pages)}
        add_tree(w, build_tree([(d, pos[pg], t) for d, pg, t in flat]))
        name = path.with_name(f"{path.stem}_Part{i}{path.suffix}")
        with open(name, "wb") as f:
            w.write(f)
        names.append(str(name))
    return names


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--manifest", required=True, type=Path)
    b.add_argument("--split", action="store_true", help="split at top-level bookmarks when over the size limit")
    c = sub.add_parser("check")
    c.add_argument("--pdf", required=True, type=Path)
    c.add_argument("--require", action="append", default=[])
    c.add_argument("--limit-mb", type=float)
    c.add_argument("--json", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "build":
        return build(a.manifest, a.split)
    res = check_pdf(a.pdf, a.require, a.limit_mb)
    if a.json:
        a.json.write_text(json.dumps(res, indent=1), encoding="utf-8")
    for b_ in res["bookmarks"]:
        print(f"{'  ' * b_['level']}{b_['title']}  (p {b_['page']})")
    print(f"pages {res['pages']} | {res['size_mb']} MB | links {res['links_checked']} broken {len(res['broken_links'])} | "
          f"order issues {len(res['order_issues'])} | missing required {len(res['missing_required'])} | "
          f"annotations {res['annotations']} -> {'PASS' if res['ok'] else 'CHECK'}")
    for x in res["order_issues"] + res["broken_links"] + [f"missing bookmark /{r}/" for r in res["missing_required"]]:
        print("  " + x)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
