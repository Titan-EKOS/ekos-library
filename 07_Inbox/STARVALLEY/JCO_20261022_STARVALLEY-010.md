---
id: STARVALLEY-010
title: Diagnose a FLO-2D run stall by file-swap bisection
type: skill
function: hydraulics-model-run
trigger: A FLO-2D model hangs or stalls at a fixed simulation time with no fatal error
steps:
- Start from a known-good model folder and create variants swapping groups of files
  from the failing model (terrain set, roughness, infiltration, structures, controls)
- Run all variants in parallel to a fixed simulation time and record pass or stall
- Narrow to the single file group, then test the same inputs on a newer engine build
- Record the test in the report issues section and adopt one engine build for all
  models
gotchas:
- Build 23.10.25 stalled at sim hour 1.2 with the effective terrain plus effective
  n or infiltration; Build 26.02.25 ran the same files to completion and was adopted
  for all models
- Legacy 2009 executable runs only in limited demo mode without a license and exits
  without results; plan on converting to the current Pro build
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 23.10.25, 26.02.25
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\bisect_hang.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\06 Report\SV-CLOMR_TDN_Narrative_4th-Submittal_DRAFT.docx
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_SV_BLIND_CLOMR\2026-10-11_dc0c3a768069.txt
  (from Codex session 2026-10-11)
hours_lost: 5.0
recurrence: 2
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:10+00:00'
schema_version: 1
---
