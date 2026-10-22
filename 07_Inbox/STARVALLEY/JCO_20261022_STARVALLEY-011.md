---
id: STARVALLEY-011
title: Convert a legacy effective FLO-2D model and document the duplicate-effective
  basis
type: skill
function: hydraulics-model-run
trigger: The effective FLO-2D model is in an old build (e.g. 2009) and FEMA requires
  current-build duplicate effective, existing and proposed models
steps:
- Preserve the effective package unchanged; work on copies and hash the copy
- Split FPLAIN into TOPO/MANNINGS_N/FPLAIN, remove obsolete TOLER fields, add floodplain
  and channel Courant fields, set storm-drain and IRAINBUILDING switches off
- Shorten structure names over 30 characters without changing hydraulic numbers; log
  every name change
- Remove stale .RGH outputs copied with the effective package
- Run upstream and detailed models; compare depths and hydrographs to the effective
  results by footprint
- Run Courant sensitivity (e.g. 0.6, 0.4, 0.2) and compare peak flows in sensitive
  clusters
- Record version differences from the vendor revision history; get EOR acceptance
  of the current-build baseline in writing
gotchas:
- 'Current build did not reproduce legacy results exactly (up to 1.57 ft upstream,
  0.59 ft detailed); legacy exe could not run without a license; EOR directed: document
  differences and use the Pro baseline'
- Do not adjust terrain, inflows or ratings to force a match
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D 2009.06, FLO-2D Pro Build 23.10.25 and 26.02.25
evidence:
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\judgment_register.json
- D:\SV-BLIND-CLOMR\_WORK\10_Record\pro_conversion_reconciliation.json
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_SV_BLIND_CLOMR\2026-10-11_dc0c3a768069.txt
  (from Codex session 2026-10-11)
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\01 Models\_run_log.txt
hours_lost: 8.0
recurrence: 2
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:11+00:00'
schema_version: 1
---
