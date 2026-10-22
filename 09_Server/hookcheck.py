"""Pre-commit checks, called from .githooks/pre-commit.

1. 07_Inbox is append-only: staged modifications, deletions or renames are refused
   unless LIBRARY_INBOX_MAINTENANCE=1 (set only by the approved weekly merge).
2. Data guard runs on every staged card or lesson file in 01_Cards and 07_Inbox.
3. Generated platform files match the masters (build.py --check).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from library_server.core import Library, LibraryError, parse_frontmatter  # noqa: E402


def staged(filter_: str) -> list[str]:
    r = subprocess.run(["git", "diff", "--cached", "--name-only", f"--diff-filter={filter_}"],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def main() -> int:
    errors: list[str] = []

    if os.environ.get("LIBRARY_INBOX_MAINTENANCE") != "1":
        for f in staged("MDR"):
            if f.startswith("07_Inbox/") and not f.endswith(".gitkeep"):
                errors.append(f"07_Inbox is append-only; refused change to {f}")

    lib = Library(ROOT, commit=False)
    for f in staged("AM"):
        if f.startswith(("07_Inbox/", "01_Cards/")) and f.endswith((".md", ".yaml", ".yml")):
            p = ROOT / f
            if not p.exists():
                continue
            meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
            try:
                lib.guard({"meta": meta, "body": body}, f)
            except LibraryError as e:
                errors.append(str(e))

    build = ROOT / "08_Platform_Builds" / "build.py"
    r = subprocess.run([sys.executable, str(build), "--check"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        errors.append("Generated files out of date or hand-edited:\n" + (r.stdout + r.stderr).strip())

    if errors:
        print("pre-commit: commit blocked\n  - " + "\n  - ".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
