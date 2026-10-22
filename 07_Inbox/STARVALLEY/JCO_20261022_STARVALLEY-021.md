---
id: STARVALLEY-021
title: Blind rebuild agent as an independent CLOMR check
type: agent
function: qc
trigger: High-stakes CLOMR where the main model has been through several rebuilds
  and an independent from-sources check is wanted before submittal
steps:
- Give the agent only a source list (effective model and TDN, survey, approved plans,
  O&M, ESA) and forbid prior CLOMR products
- 'Scope it to checks that matter: duplicate effective reproduction, terrain and coordinate
  checks, structure ratings by native HY-8, basin storage, rise analysis'
- Time-box it (one session) and require a continuation state file, judgment register
  and decision records
- Agent asks the EOR only for real decisions and explains what a missing item is (model
  type, role) in the question
- Compare its findings with the main package and log differences for EOR decision
gotchas:
- One Codex session ran about 9.5 hr and used 47 percent of the weekly allowance without
  producing the notebook or rise analysis; full rebuild is too large for one pass
- 'It found items the main package had not flagged: effective 24 hr storm model files
  absent (only 3 hr supplied), basin grading storage 15.71 ac-ft vs 18.10 ac-ft approved,
  Culvert 5 headwater 0.02 ft over allowable, storm-drain outlet loss'
- Three runs were left running unmonitored at session end
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: Codex desktop, FLO-2D Pro, HY-8, QGIS 3.44
evidence:
- D:\Star Valley CLOMR\_BLIND REBUILD PROMPT.md
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\JCO_20261011_Closeout_and_Resume.txt
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\judgment_register.json
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_SV_BLIND_CLOMR\2026-10-11_dc0c3a768069.txt
  (from Codex session 2026-10-11)
hours_lost: 10.0
recurrence: 1
confidence: medium
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:14+00:00'
schema_version: 1
---
