"""SHA-256 manifest of a source folder, to prove automated CAD reads changed nothing.

Usage:
  python hash_manifest.py make  <source_folder> <manifest.json>
  python hash_manifest.py check <source_folder> <manifest.json>

check exits 0 when every file is unchanged and none is missing, 1 otherwise
(new files are reported but do not fail the check).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def scan(folder: Path) -> dict[str, dict]:
    out = {}
    for p in sorted(folder.rglob("*")):
        if p.is_file():
            st = p.stat()
            out[p.relative_to(folder).as_posix()] = {
                "sha256": sha256(p), "bytes": st.st_size, "mtime": st.st_mtime}
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] not in ("make", "check"):
        print(__doc__)
        return 2
    folder, manifest = Path(argv[2]), Path(argv[3])
    if not folder.is_dir():
        print(f"ERROR: not a folder: {folder}")
        return 2
    if argv[1] == "make":
        data = scan(folder)
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({"folder": str(folder), "files": data}, indent=1),
                            encoding="utf-8")
        print(f"manifest: {len(data)} files -> {manifest}")
        return 0
    before = json.loads(manifest.read_text(encoding="utf-8"))["files"]
    after = scan(folder)
    changed = [k for k in before if k in after and after[k]["sha256"] != before[k]["sha256"]]
    missing = [k for k in before if k not in after]
    new = [k for k in after if k not in before]
    for label, items in (("CHANGED", changed), ("MISSING", missing), ("NEW", new)):
        for k in items:
            print(f"{label}: {k}")
    ok = not changed and not missing
    print(f"{'OK' if ok else 'FAIL'}: {len(before)} checked, {len(changed)} changed, "
          f"{len(missing)} missing, {len(new)} new")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
