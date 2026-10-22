"""Command-line access to the same library functions the MCP server exposes.

For AIs without MCP (Ollama, ChatGPT web, Gemini web) and for manual card drops.

  python library_cli.py list-skills [--filter "jurisdiction=pima"]
  python library_cli.py get-skill drainage-report-build
  python library_cli.py list-agents
  python library_cli.py get-agent qc-reviewer
  python library_cli.py qc-rules [--scope pima]
  python library_cli.py add-card card.yaml --source-ai chatgpt --project 7PSO010100
  python library_cli.py log-lesson --project 7PSO010100 --source-ai local:laguna-s-2.1 \
        --text "..." --evidence "path1" --evidence "path2"

add-card accepts a YAML or JSON file holding one card or a list of cards.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from library_server.core import Library, LibraryError, parse_frontmatter  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="EKOS Library CLI")
    ap.add_argument("--root", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list-skills"); p.add_argument("--filter", default="")
    p = sub.add_parser("get-skill"); p.add_argument("name")
    sub.add_parser("list-agents")
    p = sub.add_parser("get-agent"); p.add_argument("name")
    p = sub.add_parser("qc-rules"); p.add_argument("--scope", default="all")
    p = sub.add_parser("add-card"); p.add_argument("file")
    p.add_argument("--source-ai", required=True); p.add_argument("--project", required=True)
    p = sub.add_parser("log-lesson"); p.add_argument("--project", required=True)
    p.add_argument("--source-ai", required=True); p.add_argument("--text", required=True)
    p.add_argument("--evidence", action="append", default=[])
    a = ap.parse_args(argv)

    lib = Library(a.root)
    try:
        if a.cmd == "list-skills":
            out = lib.list_skills(a.filter or None)
        elif a.cmd == "get-skill":
            out = lib.get_skill(a.name)["content"]
        elif a.cmd == "list-agents":
            out = lib.list_agents()
        elif a.cmd == "get-agent":
            out = lib.get_agent(a.name)["content"]
        elif a.cmd == "qc-rules":
            out = lib.get_qc_rules(a.scope)
        elif a.cmd == "add-card":
            raw = Path(a.file).read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(raw)
            data = meta or yaml.safe_load(raw)
            cards = data if isinstance(data, list) else [data]
            out = [lib.add_card(c, a.source_ai, a.project) for c in cards]
        else:
            out = lib.log_lesson(a.project, a.text, a.evidence, a.source_ai)
    except LibraryError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    print(out if isinstance(out, str) else json.dumps(out, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
