---
id: SILVERBELL-009
title: CAD helper NETLOAD blocked by modal dialogs
type: skill
function: other
trigger: Agent loads compiled .NET helpers into a running Civil 3D session.
steps:
- Pre-trust a single helper folder or batch helpers into one DLL so the user approves
  once.
- Verify the exact target drawing FullName before SendCommand; guard ActiveDocument
  changes.
- Write a completion marker file per helper and never repeat NETLOAD for a helper
  already logged complete.
gotchas:
- Choose Assembly and Load Once dialogs blocked COM; computer-use could not reach
  off-monitor dialogs; user had to click for helpers 15, 21, 22, 23.
- A generic assembly error left helper 24 unapplied; native grading finished only
  with a later helper.
- Native CAD COM needs an elevated shell.
jurisdiction: n/a
tools_versions: Civil 3D 2026, PowerShell COM
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md
- C:\Ekos\projects\silverbell\v4\CURRENT_STATUS_2026-09-13.md
- C:\Ekos\projects\silverbell\v4\CHECKPOINT_1348.md
hours_lost: 2.0
recurrence: 5
confidence: medium
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:24+00:00'
schema_version: 1
---
