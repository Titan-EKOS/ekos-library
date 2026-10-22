---
id: EKOS-LOCAL-012
title: HY-8 8.00 file authoring and GUI run - units, catalog codes and session contamination
type: skill
function: hydraulics-model-run
trigger: Generating or running HY-8 crossings by file edit or GUI automation
steps:
- Start from a native saved example; take catalog codes (IRREGSIZE etc.) from it,
  never infer
- Serialize barrel data and geometry lengths in ft even when the UI shows inches
- Match exact field keys with whitespace boundaries (INLETEDGETYPE vs INLETEDGETYPE71);
  normalize CRLF only in derived text; check ENDPROJECTFILE
- Before Open, create an empty project (Ctrl+N, No) and confirm only intended crossings
  are loaded
- On welcome screen Return opens chooser; Alt+n to filename, verify caret visually,
  type path; Run Analysis; Create Report, Shift+End selects all crossings
- Parse the exported report and check total = barrel + roadway flow; record solver
  mode actually used
gotchas:
- Opening a file appended its crossing to the prior benchmark session; never save
  a contaminated session
- Accessibility focus and cached modal element indexes went stale; refresh screenshot
  before every action
- HY-8 closing without a report is a failed run
- Native summary showed Full Flow mode despite profile toolbar; do not call it a matched
  RAS profile comparison
- Unattended local HY-8 run was never achieved; only supervisor GUI runs worked
- 'Recurrence note: 4 (2 modal failures, 2 key-matching failures)'
jurisdiction: General
tools_versions: HY-8 8.00.2
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-010.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-036.md
- C:\Ekos\docs\CLAUDE_COMPUTER_SOFTWARE_LESSONS.md
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\hy8-synthetic-input-exact-002.log
hours_lost: 4.0
recurrence: 4
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:18+00:00'
schema_version: 1
---
