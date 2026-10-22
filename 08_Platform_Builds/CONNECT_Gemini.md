# Connect Gemini

## Gemini CLI
1. Add to `%USERPROFILE%\.gemini\settings.json`:
```json
{
  "mcpServers": {
    "ekos-library": {
      "command": "D:\\EKOS\\Library\\09_Server\\.venv\\Scripts\\python.exe",
      "args": ["D:\\EKOS\\Library\\09_Server\\run_server.py"]
    }
  }
}
```
   (merge into the existing file if there is one)
2. `python D:\EKOS\Library\08_Platform_Builds\build.py --install` writes `out\GEMINI.md` to `%USERPROFILE%\.gemini\GEMINI.md`.
3. Check: run `gemini`, then `/mcp`. `ekos-library` lists seven tools.

## Gemini web / app
Read-only, same as ChatGPT web: make a Gem whose instructions are `out\GEMINI.md`; lessons come back as card files you submit with
`library_cli.py add-card <file> --source-ai gemini --project <job no>`.

## Standing instruction
> **Standing instruction:** Read the relevant skill before the work; write a lesson card at the end of any project task.
> source_ai `gemini`, project = job number.
