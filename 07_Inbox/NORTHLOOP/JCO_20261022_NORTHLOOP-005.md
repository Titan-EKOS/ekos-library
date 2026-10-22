---
id: NORTHLOOP-005
title: Check historical model run duration covers the full inflow hydrographs
type: qc_rule
function: hydraulics-model-run
trigger: Reusing an archived FLO-2D model as the existing-condition baseline
steps:
- Compare CONT.DAT simulation time with the last inflow hydrograph time
- Compute the inflow volume beyond the simulation window; extend the run to cover
  the recession
- State the change in the model notes when comparing with the old results
gotchas:
- Old model stopped at 24 hr while inflows ran to 50 hr, leaving about 18% of the
  inflow volume unsimulated
jurisdiction: any
tools_versions: FLO-2D Pro
evidence:
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F16)
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30)
hours_lost: 1.0
recurrence: 1
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:27+00:00'
schema_version: 1
---
