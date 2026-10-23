"""Build and verify a delivery / review package: stage with exclusions, firm document properties, inventory,
SHA256SUMS, one ZIP64 zip, member-by-member verification (skill delivery-package-build).

build  : python build_package.py build --src <finished folder> --stage <dedicated staging folder, recreated each run>
                --out-dir <delivery folder>
                --name <Initials>_<YYYYMMDD>_<CODE>_<description> [--creator "Psomas (JCO)"] [--busy-minutes 10]
                [--exclude <glob>]... [--pointer-in <old work folder>]
verify : python build_package.py verify --zip <package.zip>       (or --dir <extracted folder>)
Exit codes: 0 pass, 1 check failed, 2 usage error.
"""
import argparse
import csv
import fnmatch
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path

EXCLUDE = ["_run0*", "*.tmp.hdf", "*.tmp", "*_body_*", "compute_stdout*", "_*", "*.bck", "*.sol", "node_modules",
           "__pycache__", ".git", "*.pyc", "~$*", "*.zip.part", "desktop.ini", "Thumbs.db", "*.lock", "*.ldb",
           "Backup.p*", "*.p??.hdf.bak"]
KEEP_UNDERSCORE = {"__init__.py"}
REQUIRED_DOCS = ["PACKAGE_README.md", "REBUILD_GUIDE.md"]
FOLDER_SET = ["01_Reports", "02_Exhibits", "03_GIS", "04_CAD", "05_Models", "06_Calculations", "07_Scripts", "08_QC"]
NAME_RX = re.compile(r"^[A-Z]{2,4}_\d{8}_[A-Za-z0-9-]+_[A-Za-z0-9_-]+$")
OFFICE = {".docx", ".xlsx", ".pptx", ".docm", ".xlsm"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def excluded(rel_parts, patterns):
    for part in rel_parts:
        if part in KEEP_UNDERSCORE:
            continue
        for p in patterns:
            if fnmatch.fnmatch(part, p):
                return p
    return None


def set_office_creator(path, creator):
    """Rewrite dc:creator and cp:lastModifiedBy in an OOXML file; returns True if changed."""
    with zipfile.ZipFile(path) as z:
        if "docProps/core.xml" not in z.namelist():
            return False
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    changed = False
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zw:
        for info, data in items:
            if info.filename == "docProps/core.xml":
                s = data.decode("utf-8")
                s2 = re.sub(r"(<dc:creator>)(.*?)(</dc:creator>)", rf"\g<1>{creator}\g<3>", s, flags=re.S)
                s2 = re.sub(r"(<cp:lastModifiedBy>)(.*?)(</cp:lastModifiedBy>)", rf"\g<1>{creator}\g<3>", s2, flags=re.S)
                if "<cp:lastModifiedBy>" not in s2 and "</cp:coreProperties>" in s2:
                    s2 = s2.replace("</cp:coreProperties>", f"<cp:lastModifiedBy>{creator}</cp:lastModifiedBy></cp:coreProperties>")
                if "<dc:creator>" not in s2 and "</cp:coreProperties>" in s2 and "xmlns:dc=" in s2:
                    s2 = s2.replace("</cp:coreProperties>", f"<dc:creator>{creator}</dc:creator></cp:coreProperties>")
                changed = s2 != s
                data = s2.encode("utf-8")
            zw.writestr(info, data)
    if changed:
        Path(path).write_bytes(out.getvalue())
    return changed


def office_creator(path):
    try:
        with zipfile.ZipFile(path) as z:
            s = z.read("docProps/core.xml").decode("utf-8", "ignore")
    except Exception:
        return None
    c = re.search(r"<dc:creator>(.*?)</dc:creator>", s, re.S)
    m = re.search(r"<cp:lastModifiedBy>(.*?)</cp:lastModifiedBy>", s, re.S)
    return (c.group(1) if c else ""), (m.group(1) if m else "")


def build(a):
    src, stage, out_dir = Path(a.src), Path(a.stage), Path(a.out_dir)
    problems, warnings = [], []
    if not NAME_RX.match(a.name):
        problems.append(f"name '{a.name}' is not <Initials>_<YYYYMMDD>_<CODE>_<description>")
    patterns = EXCLUDE + (a.exclude or [])
    now = time.time()
    files, skipped, busy = [], [], []
    for root, dirs, names in os.walk(src):
        rel_root = Path(root).relative_to(src)
        keep_dirs = []
        for d in dirs:
            hit = excluded((rel_root / d).parts, patterns)
            (skipped.append((str(rel_root / d) + "/", hit)) if hit else keep_dirs.append(d))
        dirs[:] = keep_dirs
        for n in names:
            rel = rel_root / n
            hit = excluded(rel.parts, patterns)
            if hit:
                skipped.append((str(rel), hit))
                continue
            p = Path(root) / n
            if now - p.stat().st_mtime < a.busy_minutes * 60:
                busy.append(str(rel))
            files.append(rel)
    if busy:
        problems.append(f"{len(busy)} file(s) modified in the last {a.busy_minutes} min (a run may still be writing): "
                        + ", ".join(busy[:5]))
    for d in FOLDER_SET:
        if not (src / d).exists():
            warnings.append(f"standard folder missing: {d}")
    for doc in REQUIRED_DOCS:
        if not (src / doc).exists():
            problems.append(f"missing {doc} in the source folder (template: reference/PACKAGE_README_template.md)")
        elif re.search(r"<fill[^>]*>", (src / doc).read_text(encoding="utf-8", errors="ignore")):
            problems.append(f"{doc} still has <fill> fields")
    if problems:
        for p in problems:
            print("STOP: " + p)
        return 1

    rs, rt = src.resolve(), stage.resolve()
    if rt == rs or rs in rt.parents or rt in rs.parents or rt == rt.anchor or len(rt.parts) < 3:
        print(f"STOP: staging folder {stage} overlaps the source or is too shallow; use a dedicated empty folder")
        return 1
    if stage.exists():
        shutil.rmtree(stage)
    pkg = stage / a.name
    creators_fixed, pdf_bad = 0, []
    for rel in files:
        dst = pkg / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / rel, dst)
        if dst.suffix.lower() in OFFICE and a.creator:
            try:
                creators_fixed += set_office_creator(dst, a.creator)
            except zipfile.BadZipFile:
                warnings.append(f"not a valid OOXML file: {rel}")
        if dst.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader
                if len(PdfReader(str(dst)).pages) == 0:
                    pdf_bad.append(str(rel))
            except Exception as e:  # noqa: BLE001
                pdf_bad.append(f"{rel} ({type(e).__name__})")
    if pdf_bad:
        print("STOP: PDF(s) do not open: " + ", ".join(pdf_bad))
        return 1
    # package documents
    (pkg / "EXCLUSIONS.txt").write_text("Excluded patterns:\n" + "\n".join(patterns) + "\n\nExcluded items:\n"
                                        + "\n".join(f"{p}  [{why}]" for p, why in skipped) + "\n", encoding="utf-8")
    shutil.copy2(Path(__file__), pkg / "verify_package.py")
    rows = []
    for p in sorted(pkg.rglob("*")):
        if p.is_file():
            rel = p.relative_to(pkg).as_posix()
            rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha256(p),
                         "modified": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y%m%d %H:%M"), "purpose": ""})
    with open(pkg / "FILE_INVENTORY.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "sha256", "modified", "purpose"])
        w.writeheader()
        w.writerows(rows)
    with open(pkg / "SHA256SUMS", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(f"{r['sha256']}  {r['path']}\n")
        f.write(f"{sha256(pkg / 'FILE_INVENTORY.csv')}  FILE_INVENTORY.csv\n")
    # zip
    out_dir.mkdir(parents=True, exist_ok=True)
    zpath = out_dir / f"{a.name}.zip"
    tmp = out_dir / f"{a.name}.zip.part"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        for p in sorted(pkg.rglob("*")):
            if p.is_file():
                z.write(p, f"{a.name}/{p.relative_to(pkg).as_posix()}")
    os.replace(tmp, zpath)
    res = verify_zip(zpath)
    others = [p.name for p in out_dir.iterdir() if p.is_file() and p.name != zpath.name
              and (p.suffix.lower() in (".zip", ".part", ".tmp") or p.name.startswith("~$"))]
    if others:
        res["ok"] = False
        res["problems"].append("other zip/temp files in the delivery folder: " + ", ".join(others))
    if a.pointer_in:
        Path(a.pointer_in).mkdir(parents=True, exist_ok=True)
        (Path(a.pointer_in) / "Delivery_Location.txt").write_text(
            f"Delivered {datetime.now():%Y%m%d}: {zpath}\nDo not redistribute copies from this folder.\n", encoding="utf-8")
    unz = sum(r["bytes"] for r in rows)
    summary = {"zip": str(zpath), "files": len(rows), "unzipped_mb": round(unz / 1e6, 1),
               "zipped_mb": round(zpath.stat().st_size / 1e6, 1), "excluded_items": len(skipped),
               "creator_fixed": creators_fixed, "warnings": warnings, **res}
    (out_dir / f"{a.name}_build_log.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "mismatches"}, indent=1))
    return 0 if res["ok"] else 1


def verify_zip(zpath):
    problems, mism = [], []
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        sums_name = next((n for n in names if n.endswith("/SHA256SUMS") or n == "SHA256SUMS"), None)
        if not sums_name:
            return {"ok": False, "problems": ["SHA256SUMS not in zip"], "mismatches": []}
        root = sums_name[: -len("SHA256SUMS")]
        expected = {}
        for line in z.read(sums_name).decode("utf-8").splitlines():
            if line.strip():
                h, rel = line.split("  ", 1)
                expected[rel] = h
        for rel, h in expected.items():
            name = root + rel
            if name not in names:
                mism.append(f"missing in zip: {rel}")
                continue
            got = hashlib.sha256(z.read(name)).hexdigest()
            if got != h:
                mism.append(f"hash mismatch: {rel}")
        extra = [n for n in names if not n.endswith("/") and n[len(root):] not in expected and n != sums_name]
        if extra:
            mism.append(f"{len(extra)} member(s) not listed in SHA256SUMS")
    if mism:
        problems.append(f"{len(mism)} verification problem(s)")
    return {"ok": not problems, "problems": problems, "mismatches": mism, "members_checked": len(expected)}


def verify_dir(d):
    d = Path(d)
    mism = []
    lines = (d / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    for line in lines:
        if not line.strip():
            continue
        h, rel = line.split("  ", 1)
        p = d / rel
        if not p.exists():
            mism.append(f"missing: {rel}")
        elif sha256(p) != h:
            mism.append(f"hash mismatch: {rel}")
    return {"ok": not mism, "problems": [], "mismatches": mism, "members_checked": len(lines)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--src", required=True)
    b.add_argument("--stage", required=True)
    b.add_argument("--out-dir", required=True)
    b.add_argument("--name", required=True)
    b.add_argument("--creator", default="Psomas")
    b.add_argument("--busy-minutes", type=float, default=10)
    b.add_argument("--exclude", action="append")
    b.add_argument("--pointer-in")
    v = sub.add_parser("verify")
    g = v.add_mutually_exclusive_group(required=True)
    g.add_argument("--zip")
    g.add_argument("--dir")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        return build(a)
    res = verify_zip(a.zip) if a.zip else verify_dir(a.dir)
    print(json.dumps(res, indent=1))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
