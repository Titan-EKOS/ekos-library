# Connect ChatGPT (web and desktop app)

ChatGPT web cannot reach a server on EKOS without exposing EKOS to the internet. Per the Phase 0 decision, it stays read-only:

1. Create a ChatGPT Project "EKOS Library". Paste `08_Platform_Builds\out\AGENTS.md` into the project instructions (or upload it as a project file). Re-paste after each build; the weekly report says when it changed.
2. For a full skill, upload `out\claude\<skill>\SKILL.md` to the chat or project.
3. Lessons: at the end of a project task, ask ChatGPT for a card in the format of `01_Cards\_TEMPLATE_card.yaml`. Save it anywhere outside the library (e.g. Downloads), then run:
```powershell
D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py add-card <file> --source-ai chatgpt --project <job no>
```
The CLI runs the same validation and data guard as the server. For computer-use sessions on EKOS, ChatGPT can run that command itself.

For Codex inside ChatGPT, use CONNECT_Codex.md.

## Standing instruction (paste into the project)
> **Standing instruction:** Read the relevant skill before the work; write a lesson card at the end of any project task.
> End each project task with a lesson card in the EKOS card format (lessons and file paths only, job number instead of client names).
