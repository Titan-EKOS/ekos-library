# EKOS Library server

Local MCP server for the shared skills library. Runs on EKOS only. Stdio by default; `--http` binds 127.0.0.1.

## Setup
    powershell -ExecutionPolicy Bypass -File D:\EKOS\Library\09_Server\setup.ps1

## Run
MCP clients start it themselves with:

    command: D:\EKOS\Library\09_Server\.venv\Scripts\python.exe
    args:    D:\EKOS\Library\09_Server\run_server.py

By hand: `.\start_server.ps1` (stdio) or `.\start_server.ps1 -Http` (http://127.0.0.1:8765/mcp).

## Tools
| Tool | Does |
|---|---|
| list_skills(filter) | Active skills. Filter by free text or `key=value` (e.g. `jurisdiction=pima`). |
| get_skill(name) | Full SKILL.md, metadata, resource list. |
| list_agents() | Active agents and the skills they call. |
| get_agent(name) | Full AGENT.md. |
| add_card(card, source_ai, project) | New card file in 07_Inbox, one git commit. |
| log_lesson(project, text, evidence, source_ai) | New lesson file in 07_Inbox, one git commit. |
| get_qc_rules(scope) | Rules from 05_QC_Rules by jurisdiction, function or tag. |

## Write rules
- add_card and log_lesson only create new files under `07_Inbox\<job no>\`. Nothing overwrites. No tool edits skills, agents or rules.
- Stamped on every write: source_ai, UTC timestamp, project, schema_version, and the MCP client name (`client_reported`).
- Every write is one local git commit. Pushing happens in the weekly task.
- Data guard rejects: emails, phone numbers, APN/SSN patterns, street addresses, any field over 4000 chars, and terms in `00_Inventory\_local\client_terms.txt`. Evidence paths pass through `00_Inventory\_local\path_aliases.csv` first (client name to job number). Both files stay local (gitignored).
- Pre-commit hook: 07_Inbox append-only, data guard on staged cards, generated files must match masters.

## Without MCP
`library_cli.py` has the same functions: `list-skills`, `get-skill`, `list-agents`, `get-agent`, `qc-rules`, `add-card <file>`, `log-lesson`.

## Test
    .venv\Scripts\python.exe -m pytest -q tests

Covers every tool over a real stdio MCP session, append-only, commit per write, data-guard rejections, no writes outside 07_Inbox, build drift detection and the hook.
