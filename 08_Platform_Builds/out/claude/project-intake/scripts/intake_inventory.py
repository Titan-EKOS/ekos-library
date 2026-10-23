r"""Project folder intake: inventory, cloud-placeholder and nested-copy checks, ZIP contents, snapshot delta, copy
verification (skill project-intake, DSO-C13).

inventory : python intake_inventory.py inventory --root <project folder> --out <work>\Intake_<YYYYMMDD>\inventory_<YYYYMMDD_HHMM>.csv
            [--previous <earlier inventory.csv>]   writes the CSV, a ZIP-contents CSV, a summary JSON and (with
            --previous) a delta CSV. Outputs must sit outside the source job folder.
verify    : python intake_inventory.py verify --src <source> --dst <copy> [--sample 50]
            compares file count and bytes and SHA-256 of a sample (after robocopy).
Exit codes: 0 ok, 1 findings (placeholders, nested copy, unreadable files, copy mismatch), 2 usage error.
"""
import argparse
import csv
import hashlib
import json
import os
import random
import stat
import sys
import zipfile
from datetime import datetime
from pathlib import Path

RECALL = 0x00400000      # FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS (cloud-only, OneDrive)
OFFLINE = 0x00001000
PINNED = 0x00080000


def sha256(path, limit=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk(root):
    for dirpath, dirs, files in os.walk(root):
        for n in files:
            yield Path(dirpath) / n


def cmd_inventory(a):
    root, out = Path(a.root).resolve(), Path(a.out).resolve()
    if root in out.parents:
        print("STOP: write the inventory outside the source job folder", file=sys.stderr)
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    rows, zips, cloud, unreadable = [], [], 0, 0
    names_only_desktop_ini = True
    for p in walk(root):
        rel = p.relative_to(root).as_posix()
        try:
            st = p.stat()
            attrs = getattr(st, "st_file_attributes", 0)
            is_cloud = bool(attrs & (RECALL | OFFLINE))
            readable = os.access(p, os.R_OK)
        except OSError:
            st, attrs, is_cloud, readable = None, 0, False, False
        if p.name.lower() != "desktop.ini":
            names_only_desktop_ini = False
        cloud += is_cloud
        unreadable += not readable
        rows.append({"path": rel, "bytes": st.st_size if st else "", "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y%m%d %H:%M") if st else "",
                     "readable": "yes" if readable else "no", "cloud_only": "yes" if is_cloud else "no",
                     "ext": p.suffix.lower()})
        if p.suffix.lower() == ".zip" and readable and not is_cloud:
            try:
                with zipfile.ZipFile(p) as z:
                    for i in z.infolist():
                        zips.append({"zip": rel, "member": i.filename, "bytes": i.file_size,
                                     "modified": "%04d%02d%02d" % i.date_time[:3]})
            except zipfile.BadZipFile:
                zips.append({"zip": rel, "member": "(unreadable zip)", "bytes": "", "modified": ""})
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["path", "bytes", "modified", "readable", "cloud_only", "ext"])
        w.writeheader()
        w.writerows(rows)
    zout = out.with_name(out.stem + "_zip_contents.csv")
    with open(zout, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["zip", "member", "bytes", "modified"])
        w.writeheader()
        w.writerows(zips)
    # nested copy: the root folder name repeated below itself, or a subfolder whose file list mirrors the root
    top = root.name.lower()
    nested = sorted({r["path"].split("/")[0] for r in rows if top in [s.lower() for s in r["path"].split("/")[:-1]]})
    summary = {"root": str(root), "files": len(rows), "bytes": sum(r["bytes"] or 0 for r in rows),
               "cloud_only_files": cloud, "unreadable_files": unreadable,
               "only_desktop_ini": names_only_desktop_ini and len(rows) > 0, "empty": len(rows) == 0,
               "nested_copy_suspects": nested, "zip_members": len(zips), "inventory": str(out), "zip_contents": str(zout),
               "taken": datetime.now().strftime("%Y%m%d %H:%M")}
    if a.previous:
        prev = {r["path"]: r for r in csv.DictReader(open(a.previous, encoding="utf-8"))}
        cur = {r["path"]: r for r in rows}
        delta = [{"change": "added", "path": p} for p in cur if p not in prev]
        delta += [{"change": "removed", "path": p} for p in prev if p not in cur]
        delta += [{"change": "size", "path": p} for p in cur if p in prev and str(cur[p]["bytes"]) != str(prev[p]["bytes"])]
        dout = out.with_name(out.stem + "_delta.csv")
        with open(dout, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["change", "path"])
            w.writeheader()
            w.writerows(delta)
        summary["delta"] = {"added": sum(d["change"] == "added" for d in delta),
                            "removed": sum(d["change"] == "removed" for d in delta),
                            "size_changed": sum(d["change"] == "size" for d in delta), "file": str(dout)}
        summary["final"] = not delta
    out.with_name(out.stem + "_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    bad = summary["empty"] or summary["only_desktop_ini"] or cloud or unreadable or nested
    return 1 if bad else 0


def cmd_verify(a):
    src, dst = Path(a.src), Path(a.dst)
    s_files = {p.relative_to(src).as_posix(): p.stat().st_size for p in walk(src)}
    d_files = {p.relative_to(dst).as_posix(): p.stat().st_size for p in walk(dst)}
    missing = sorted(set(s_files) - set(d_files))
    size_diff = sorted(k for k in s_files if k in d_files and s_files[k] != d_files[k])
    sample = random.Random(0).sample(sorted(set(s_files) & set(d_files)), min(a.sample, len(set(s_files) & set(d_files))))
    hash_diff = [k for k in sample if sha256(src / k) != sha256(dst / k)]
    res = {"src_files": len(s_files), "dst_files": len(d_files), "src_bytes": sum(s_files.values()),
           "dst_bytes": sum(d_files.values()), "missing_in_copy": missing[:50], "size_differs": size_diff[:50],
           "hash_sample": len(sample), "hash_differs": hash_diff, "checked": datetime.now().strftime("%Y%m%d %H:%M")}
    res["ok"] = not (missing or size_diff or hash_diff)
    print(json.dumps(res, indent=1))
    return 0 if res["ok"] else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inventory")
    i.add_argument("--root", required=True)
    i.add_argument("--out", required=True)
    i.add_argument("--previous")
    v = sub.add_parser("verify")
    v.add_argument("--src", required=True)
    v.add_argument("--dst", required=True)
    v.add_argument("--sample", type=int, default=50)
    a = ap.parse_args(argv)
    return cmd_inventory(a) if a.cmd == "inventory" else cmd_verify(a)


if __name__ == "__main__":
    sys.exit(main())
