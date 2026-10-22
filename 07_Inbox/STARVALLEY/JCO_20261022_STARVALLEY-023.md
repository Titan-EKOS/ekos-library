---
id: STARVALLEY-023
title: Check approved-plan numbers against native recalculation and document differences
type: qc_rule
function: qc
trigger: Using approved-plan geometry (basin grading, culverts, storm drain) in a
  FEMA model where as-builts do not exist
steps:
- Recompute basin stage-storage from the supplied grading surface and compare to the
  approved report
- Rerun culvert and storm-drain checks in HY-8 or by hand at the county design flow
  and compare headwater to allowable
- Keep approved geometry; record each difference with numbers in the judgment memo
  after EOR decision
gotchas:
- Supplied basin surface gave 15.71 ac-ft at 2548.69 ft vs 18.10 ac-ft reported; storm-drain
  inlet water level rose from 2544.09 to 2545.00 ft when full outlet loss was included,
  above inlet ground
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: HY-8 8.0, Python 3.12
evidence:
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\basin_surface_user_decision.json
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\culvert5_design_decision.json
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\storm_drain_loss_user_decision.json
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_SV_BLIND_CLOMR\2026-10-11_dc0c3a768069.txt
  (from Codex session 2026-10-11)
hours_lost: 3.0
recurrence: 3
confidence: medium
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:15+00:00'
schema_version: 1
---
