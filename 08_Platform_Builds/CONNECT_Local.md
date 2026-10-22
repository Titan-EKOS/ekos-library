# Connect local models (LM Studio, Ollama, EKOS agent system)

## LM Studio (MCP)
Program tab > Install > Edit `mcp.json` (`%USERPROFILE%\.lmstudio\mcp.json`), add under `mcpServers`:
```json
"ekos-library": {
  "command": "D:\\EKOS\\Library\\09_Server\\.venv\\Scripts\\python.exe",
  "args": ["D:\\EKOS\\Library\\09_Server\\run_server.py"]
}
```
Use `source_ai: local:<model>` (e.g. `local:laguna-s-2.1`).
System prompt: paste `out\local\_library.txt`, or the agent prompt `out\local\<agent>.txt`.

## Ollama (no MCP)
- System prompts: `out\local\<agent>.txt`. Set `build.local_base_model` in `library.yaml` to an Ollama tag and the build also writes `out\local\<agent>.Modelfile`; then `ollama create <agent> -f <agent>.Modelfile`.
- Lessons: the harness (or the model through a shell tool) runs
```powershell
D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py log-lesson --project <job no> --source-ai local:<model> --text "..." --evidence "<path>"
```

## EKOS drainage agent system
Point each agent at the MCP server (stdio command above) or at `library_cli.py`. Agents read `get_agent` / `get_skill` at start and call `log_lesson` at the end of every run.

## Standing instruction
> **Standing instruction:** Read the relevant skill before the work; write a lesson card at the end of any project task.
