---
id: NORTHLOOP-013
title: PC-Hydro graded ground keeps the program 20% default
type: qc_rule
function: hydrology
trigger: Onsite PC-Hydro runs with graded (developed pad) ground
steps:
- Keep PC-Hydro 20% default for graded ground; no blanket 5% Desert Brush override
- Use the native runoff parameters for the selected cover and soil group; do not carry
  a fixed CN 86
- Tc is the program value, 5 min minimum
gotchas:
- Saved standards still had the old 5% rule; the EOR correction overrides it, update
  the shared skill
jurisdiction: Pima County / Town of Marana
tools_versions: PC-Hydro 7.4
evidence:
- C:\Users\Titan\OneDrive\Northloop\AGENTS.md (section 3)
- C:\Users\Titan\OneDrive\Northloop\40_QC\T3_EOR_Review\JCO_2026-09-30_Instruction_Comparison.txt
  (EOR update - PC-Hydro)
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30, EOR correction)
hours_lost: 0.5
recurrence: 2
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:30+00:00'
schema_version: 1
---
