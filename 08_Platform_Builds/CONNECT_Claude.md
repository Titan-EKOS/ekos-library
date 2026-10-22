# Connect Claude

## Claude desktop app (also reaches cloud sessions linked to EKOS)
1. Open `%APPDATA%\Claude\claude_desktop_config.json` (Settings > Developer > Edit Config).
2. Add under `mcpServers`:
```json
"ekos-library": {
  "command": "D:\\EKOS\\Library\\09_Server\\.venv\\Scripts\\python.exe",
  "args": ["D:\\EKOS\\Library\\09_Server\\run_server.py"]
}
```
3. Restart the app. The seven `ekos-library` tools show in the tools list.

## Claude Code
```powershell
claude mcp add --scope user ekos-library -- "D:\EKOS\Library\09_Server\.venv\Scripts\python.exe" "D:\EKOS\Library\09_Server\run_server.py"
python D:\EKOS\Library\08_Platform_Builds\build.py --install   # copies skills to %USERPROFILE%\.claude\skills
```
`--install` skips any hand-made skill folder with the same name unless you add `--force` (a dated backup is kept).

## claude.ai (web, mobile, desktop chats not on EKOS)
No live server. Skills reach your account through the skill review cards Claude shows after each build (save each card). Lessons from those chats: ask Claude for a card in the `01_Cards\_TEMPLATE_card.yaml` format, save it, then run
`library_cli.py add-card <file> --source-ai claude --project <job no>`.

## Project instruction (paste into the Claude Project or CLAUDE.md)
> **Standing instruction:** Read the relevant skill before the work; write a lesson card at the end of any project task.
> Use the `ekos-library` tools: `get_skill` before the work, `add_card` or `log_lesson` (source_ai `claude`, project = job number) at the end. Lessons and file paths only, no client data.
