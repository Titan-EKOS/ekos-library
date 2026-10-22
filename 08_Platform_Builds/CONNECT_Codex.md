# Connect Codex (CLI and IDE extension)

1. Add to `%USERPROFILE%\.codex\config.toml`:
```toml
[mcp_servers.ekos-library]
command = 'D:\EKOS\Library\09_Server\.venv\Scripts\python.exe'
args = ['D:\EKOS\Library\09_Server\run_server.py']
```
   (or: `codex mcp add ekos-library -- "D:\EKOS\Library\09_Server\.venv\Scripts\python.exe" "D:\EKOS\Library\09_Server\run_server.py"`)
2. Standing instructions: `python D:\EKOS\Library\08_Platform_Builds\build.py --install` writes `out\AGENTS.md` to `%USERPROFILE%\.codex\AGENTS.md` (an existing hand-made file is backed up first).
3. Check: run `codex`, then `/mcp`. `ekos-library` lists seven tools.

AGENTS.md stays under the 32 KiB Codex project-doc limit; it holds the index, and Codex pulls full skills through `get_skill`.

## Standing instruction
> **Standing instruction:** Read the relevant skill before the work; write a lesson card at the end of any project task.
> source_ai `codex`, project = job number.
