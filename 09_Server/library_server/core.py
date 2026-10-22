"""EKOS Library core logic. No MCP dependency, so the server, CLI and hook share it.

Write rules enforced here:
  - Only add_card and log_lesson write, and only new files under 07_Inbox.
  - Every write is its own git commit.
  - The data guard rejects anything that looks like client data.
"""
from __future__ import annotations

import csv
import datetime as dt
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

import yaml

INBOX = "07_Inbox"
SKILLS = "03_Skills"
AGENTS = "04_Agents"
QC_RULES = "05_QC_Rules/rules.md"

_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)
_SLUG_RE = re.compile(r"[^A-Za-z0-9_.-]+")


class LibraryError(ValueError):
    """Raised for rejected writes and bad requests. Message is safe to show the caller."""


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    if not isinstance(meta, dict):
        return {}, text
    return meta, m.group(2)


def slug(value: str, maxlen: int = 60) -> str:
    s = _SLUG_RE.sub("-", str(value).strip()).strip("-.")
    return (s or "x")[:maxlen]


class Library:
    def __init__(self, root: str | os.PathLike | None = None, *, commit: bool = True):
        if root is None:
            root = os.environ.get("LIBRARY_ROOT") or Path(__file__).resolve().parents[2]
        self.root = Path(root).resolve()
        cfg_path = self.root / "library.yaml"
        if not cfg_path.exists():
            raise LibraryError(f"library.yaml not found under {self.root}")
        self.cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        self.commit_enabled = commit
        self._lock = threading.Lock()
        self._patterns = {
            k: re.compile(v) for k, v in self.cfg["data_guard"]["patterns"].items()
        }

    # ------------------------------------------------------------------ reads
    def _masters(self, folder: str, filename: str) -> list[tuple[Path, dict, str]]:
        out = []
        base = self.root / folder
        if not base.exists():
            return out
        for d in sorted(base.iterdir()):
            f = d / filename
            if d.is_dir() and not d.name.startswith("_") and f.exists():
                meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
                out.append((d, meta, body))
        return out

    @staticmethod
    def _matches(meta: dict, flt: str | None) -> bool:
        if not flt:
            return True
        for term in flt.split():
            if "=" in term:
                k, v = term.split("=", 1)
                val = meta.get(k)
                vals = val if isinstance(val, list) else [val]
                if not any(v.lower() in str(x).lower() for x in vals if x is not None):
                    return False
            else:
                hay = " ".join(
                    str(meta.get(k, "")) for k in
                    ("name", "description", "jurisdiction", "function", "tools_versions", "status")
                ).lower()
                if term.lower() not in hay:
                    return False
        return True

    @staticmethod
    def _summary(meta: dict) -> dict:
        keys = ("name", "description", "version", "status", "function", "jurisdiction",
                "tools_versions", "owner", "replaces", "skills")
        return {k: meta[k] for k in keys if k in meta}

    def list_skills(self, filter: str | None = None) -> list[dict]:
        return [self._summary(m) for _, m, _ in self._masters(SKILLS, "SKILL.md")
                if m.get("status") != "retired" and self._matches(m, filter)]

    def get_skill(self, name: str) -> dict:
        return self._get(SKILLS, "SKILL.md", name)

    def list_agents(self) -> list[dict]:
        return [self._summary(m) for _, m, _ in self._masters(AGENTS, "AGENT.md")
                if m.get("status") != "retired"]

    def get_agent(self, name: str) -> dict:
        return self._get(AGENTS, "AGENT.md", name)

    def _get(self, folder: str, filename: str, name: str) -> dict:
        for d, meta, _ in self._masters(folder, filename):
            if meta.get("name") == name or d.name == name:
                files = sorted(
                    str(p.relative_to(d)).replace("\\", "/")
                    for p in d.rglob("*") if p.is_file() and p.name != filename
                )
                return {"name": meta.get("name", d.name), "meta": meta,
                        "content": (d / filename).read_text(encoding="utf-8"),
                        "resources": files, "path": str(d.relative_to(self.root))}
        raise LibraryError(f"No {folder[3:].rstrip('s').lower()} named '{name}'")

    def get_qc_rules(self, scope: str | None = "all") -> list[dict]:
        """Rules live in 05_QC_Rules/rules.md as '## QC-nnnn title' + a ```yaml block."""
        path = self.root / QC_RULES
        if not path.exists():
            return []
        text = path.read_text(encoding="utf-8")
        rules = []
        for m in re.finditer(r"^## +(QC-\d+)[^\n]*\n.*?```yaml\n(.*?)```", text, re.S | re.M):
            data = yaml.safe_load(m.group(2)) or {}
            data.setdefault("id", m.group(1))
            rules.append(data)
        if not scope or scope.lower() == "all":
            return rules
        s = scope.lower()

        def hit(r: dict) -> bool:
            fields = []
            for k in ("scope", "function", "jurisdiction", "tags", "id"):
                v = r.get(k)
                fields += v if isinstance(v, list) else [v]
            return any(s in str(f).lower() for f in fields if f is not None) or \
                any(str(f).lower() in ("all", "*") for f in fields if f is not None)
        return [r for r in rules if hit(r)]

    # ------------------------------------------------------------- data guard
    def _local_lines(self, key: str) -> list[str]:
        p = self.root / self.cfg["data_guard"][key]
        if not p.exists():
            return []
        return [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")]

    def apply_path_aliases(self, text: str) -> str:
        p = self.root / self.cfg["data_guard"]["path_aliases_file"]
        if not p.exists():
            return text
        with p.open(encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh):
                if len(row) >= 2 and row[0].strip() and not row[0].startswith("#"):
                    text = re.sub(re.escape(row[0].strip()), row[1].strip(), text,
                                  flags=re.I)
        return text

    def guard(self, obj: Any, where: str = "card") -> None:
        """Raise LibraryError naming the first field and pattern that looks like client data."""
        limit = int(self.cfg["data_guard"]["max_field_chars"])
        terms = [t.lower() for t in self._local_lines("client_terms_file")]
        for path, value in _walk(obj, where):
            if not isinstance(value, str):
                continue
            if len(value) > limit:
                raise LibraryError(
                    f"Rejected: {path} is {len(value)} chars (limit {limit}). "
                    "Cards hold lessons and paths, not pasted documents.")
            for name, rx in self._patterns.items():
                if rx.search(value):
                    raise LibraryError(
                        f"Rejected: {path} matches data-guard pattern '{name}'. "
                        "Remove client data and resubmit.")
            low = value.lower()
            for t in terms:
                if t and t in low:
                    raise LibraryError(
                        f"Rejected: {path} contains a listed client term. "
                        "Use the job number instead.")

    # ------------------------------------------------------------------ writes
    def _check_source_ai(self, source_ai: str) -> str:
        s = (source_ai or "").strip().lower()
        if not s or not any(s == p or s.startswith(p + ":") or s.startswith(p + "-")
                            for p in self.cfg["card"]["source_ai_prefixes"]):
            raise LibraryError(
                "source_ai is required and must start with one of "
                f"{self.cfg['card']['source_ai_prefixes']} (e.g. 'claude', 'local:laguna-s-2.1').")
        return s

    def _inbox_path(self, project: str, stem: str) -> Path:
        inbox = (self.root / INBOX).resolve()
        folder = (inbox / slug(project)).resolve()
        if inbox not in folder.parents:
            raise LibraryError("Write outside 07_Inbox refused.")
        folder.mkdir(parents=True, exist_ok=True)
        cand = folder / f"{stem}.md"
        n = 2
        while cand.exists():
            cand = folder / f"{stem}_{n}.md"
            n += 1
        return cand

    def _write_new(self, path: Path, text: str, message: str, source_ai: str) -> str:
        inbox = (self.root / INBOX).resolve()
        rp = path.resolve()
        if inbox not in rp.parents:
            raise LibraryError("Write outside 07_Inbox refused.")
        with self._lock, _FileLock(self.root / ".git" / "library_server.lock"):
            with open(rp, "x", encoding="utf-8", newline="\n") as fh:   # never overwrite
                fh.write(text)
            if self.commit_enabled:
                self._commit(rp, message, source_ai)
        return str(rp.relative_to(self.root)).replace("\\", "/")

    def _commit(self, path: Path, message: str, source_ai: str) -> None:
        rel = str(path.relative_to(self.root))
        env = dict(os.environ,
                   LIBRARY_PYTHON=os.environ.get("LIBRARY_PYTHON", sys.executable),
                   GIT_AUTHOR_NAME=f"library-server ({source_ai})",
                   GIT_AUTHOR_EMAIL="library-server@ekos.local",
                   GIT_COMMITTER_NAME="library-server",
                   GIT_COMMITTER_EMAIL="library-server@ekos.local")
        for cmd in (["git", "add", "--", rel],
                    ["git", "commit", "-q", "-m", message, "--", rel]):
            r = subprocess.run(cmd, cwd=self.root, env=env, capture_output=True, text=True,
                               stdin=subprocess.DEVNULL, timeout=60)
            if r.returncode != 0:
                raise LibraryError(f"git failed ({' '.join(cmd[:2])}): {r.stderr.strip()[:400]}")

    def add_card(self, card: dict, source_ai: str, project: str,
                 client_reported: str | None = None) -> dict:
        if not isinstance(card, dict):
            raise LibraryError("card must be an object")
        if not project or not str(project).strip():
            raise LibraryError("project is required (use the job number)")
        src = self._check_source_ai(source_ai)
        c = self.cfg["card"]
        card = {k: v for k, v in card.items() if v is not None}
        missing = [k for k in c["required"] if k not in card or card[k] in ("", [], {})]
        if missing:
            raise LibraryError(f"Missing required card fields: {missing}")
        for key, allowed in (("type", c["types"]), ("function", c["functions"]),
                             ("confidence", c["confidence"])):
            if str(card[key]).lower() not in allowed:
                raise LibraryError(f"{key} must be one of {allowed}")
            card[key] = str(card[key]).lower()
        for key in ("hours_lost", "recurrence"):
            if key in card:
                try:
                    card[key] = float(card[key]) if key == "hours_lost" else int(card[key])
                except (TypeError, ValueError):
                    raise LibraryError(f"{key} must be a number")
                if card[key] < 0:
                    raise LibraryError(f"{key} must be >= 0")
        for key in ("steps", "gotchas", "evidence"):
            if key in card and isinstance(card[key], str):
                card[key] = [card[key]]
        card["evidence"] = [self.apply_path_aliases(str(e)) for e in card["evidence"]]
        self.guard(card, "card")
        self.guard(project, "project")

        now = dt.datetime.now(dt.timezone.utc)
        stamped = dict(card)
        stamped.update({
            "project": str(project).strip(),
            "source_ai": src,
            "timestamp": now.isoformat(timespec="seconds"),
            "schema_version": self.cfg["schema_version"],
        })
        if client_reported:
            stamped["client_reported"] = client_reported
        stem = f"{self.cfg['initials']}_{now:%Y%m%d}_{slug(card['id'], 50)}"
        path = self._inbox_path(project, stem)
        text = "---\n" + yaml.safe_dump(stamped, sort_keys=False, allow_unicode=True) + "---\n"
        rel = self._write_new(path, text,
                              f"inbox: {card['type']} card {card['id']} [{project}] via {src}", src)
        return {"status": "accepted", "path": rel, "timestamp": stamped["timestamp"]}

    def log_lesson(self, project: str, text: str, evidence: Any, source_ai: str,
                   client_reported: str | None = None) -> dict:
        if not project or not str(project).strip():
            raise LibraryError("project is required (use the job number)")
        if not text or not str(text).strip():
            raise LibraryError("text is required")
        src = self._check_source_ai(source_ai)
        ev = evidence if isinstance(evidence, list) else ([evidence] if evidence else [])
        ev = [self.apply_path_aliases(str(e)) for e in ev]
        rec = {"type": "lesson", "project": str(project).strip(), "text": str(text).strip(),
               "evidence": ev}
        self.guard(rec, "lesson")
        now = dt.datetime.now(dt.timezone.utc)
        rec.update({"source_ai": src, "timestamp": now.isoformat(timespec="seconds"),
                    "schema_version": self.cfg["schema_version"]})
        if client_reported:
            rec["client_reported"] = client_reported
        stem = f"{self.cfg['initials']}_{now:%Y%m%d}_lesson"
        path = self._inbox_path(project, stem)
        body = "---\n" + yaml.safe_dump(rec, sort_keys=False, allow_unicode=True) + "---\n"
        rel = self._write_new(path, body, f"inbox: lesson [{project}] via {src}", src)
        return {"status": "accepted", "path": rel, "timestamp": rec["timestamp"]}


def _walk(obj: Any, path: str):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _walk(v, f"{path}[{i}]")
    else:
        yield path, obj


class _FileLock:
    """Cross-process lock via exclusive create. Stale locks (>120 s) are cleared."""

    def __init__(self, path: Path, timeout: float = 30.0):
        self.path, self.timeout = Path(path), timeout

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        start = time.time()
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - self.path.stat().st_mtime > 120:
                        self.path.unlink(missing_ok=True)
                        continue
                except FileNotFoundError:
                    continue
                if time.time() - start > self.timeout:
                    raise LibraryError("Library is busy (lock timeout). Try again.")
                time.sleep(0.1)

    def __exit__(self, *exc):
        self.path.unlink(missing_ok=True)
