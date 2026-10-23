"""EKOS Library MCP server.

Run:  python run_server.py            (stdio, for Claude Desktop / Claude Code / Codex / Gemini CLI / LM Studio)
      python run_server.py --http     (streamable HTTP on 127.0.0.1 only)
"""
from __future__ import annotations

import argparse
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from .core import Library, LibraryError

INSTRUCTIONS = (
    "EKOS Library: shared skills, agents and QC rules for drainage, H&H and civil work. "
    "Before a task, call list_skills/get_skill (and get_qc_rules) and follow the skill. "
    "At the end of any project task, call add_card or log_lesson with your source_ai and the "
    "job number as project. Cards hold lessons and file paths only - never client documents "
    "or client data. Skills and agents are read-only here."
)

lib: Library | None = None
mcp = FastMCP("ekos-library", instructions=INSTRUCTIONS)


def _lib() -> Library:
    global lib
    if lib is None:
        lib = Library()
    return lib


def _client_name(ctx: Context | None) -> str | None:
    try:
        info = ctx.session.client_params.clientInfo  # type: ignore[union-attr]
        return f"{info.name} {info.version}".strip()
    except Exception:
        return None


def _wrap(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except LibraryError as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def list_skills(filter: str = "") -> Any:
    """List active skills. filter: free text, or key=value terms (e.g. 'jurisdiction=pima function=hydrology')."""
    return _wrap(_lib().list_skills, filter or None)


@mcp.tool()
def get_skill(name: str, resource: str = "") -> Any:
    """Full SKILL.md text, metadata and resource file list for one skill.
    resource: optional relative path of one resource (e.g. 'addons/pima-county-rfcd.md') to read instead."""
    return _wrap(_lib().get_skill, name, resource or None)


@mcp.tool()
def list_agents() -> Any:
    """List active agents with the skills each one calls."""
    return _wrap(_lib().list_agents)


@mcp.tool()
def get_agent(name: str, resource: str = "") -> Any:
    """Full AGENT.md text and metadata for one agent (or one resource file of it)."""
    return _wrap(_lib().get_agent, name, resource or None)


@mcp.tool()
def add_card(card: dict, source_ai: str, project: str, ctx: Context | None = None) -> Any:
    """Append a lesson card to 07_Inbox (append-only, one git commit).

    card fields: id, title, type (skill|agent|qc_rule), function (data-gathering|hydrology|
    hydraulics-model-run|exhibits|report-assembly|compile-pdf|qc|jurisdiction-rules|
    project-setup|other), trigger, steps[], gotchas[], jurisdiction, tools_versions,
    evidence[] (paths, chat links, markup pages), hours_lost, recurrence,
    confidence (high|medium|low).
    source_ai: claude | chatgpt | codex | gemini | local:<model>.  project: job number.
    No client documents or client data; the data guard rejects them.
    """
    return _wrap(_lib().add_card, card, source_ai, project, _client_name(ctx))


@mcp.tool()
def log_lesson(project: str, text: str, evidence: list[str] | str, source_ai: str,
               ctx: Context | None = None) -> Any:
    """Append a short free-text lesson to 07_Inbox (append-only, one git commit).
    project: job number. evidence: paths, chat links or markup pages. source_ai as in add_card."""
    return _wrap(_lib().log_lesson, project, text, evidence, source_ai, _client_name(ctx))


@mcp.tool()
def get_qc_rules(scope: str = "all") -> Any:
    """QC rules from 05_QC_Rules, each tied to the redline it came from.
    scope: 'all', a jurisdiction (e.g. 'pima'), a function (e.g. 'exhibits') or a tag."""
    return _wrap(_lib().get_qc_rules, scope)


def main() -> None:
    ap = argparse.ArgumentParser(description="EKOS Library MCP server")
    ap.add_argument("--http", action="store_true", help="streamable HTTP on 127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--root", default=None, help="library root (default: repo containing this file)")
    args = ap.parse_args()
    global lib
    lib = Library(args.root)
    if args.http:
        mcp.settings.host = "127.0.0.1"   # never bind to other interfaces
        mcp.settings.port = args.port
        mcp.run("streamable-http")
    else:
        mcp.run("stdio")


if __name__ == "__main__":
    main()
