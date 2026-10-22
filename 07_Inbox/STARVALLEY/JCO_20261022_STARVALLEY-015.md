---
id: STARVALLEY-015
title: Scan proposed TOPO for placeholder surfaces before comparison
type: qc_rule
function: qc
trigger: Any proposed-conditions FLO-2D TOPO.DAT received from others or edited for
  grading
steps:
- Search for large patches of cells at one constant elevation
- Compare proposed TOPO to the design TIN and to existing ground inside the grading
  limits (mean, median, std, percent within 0.5 ft)
- Check maximum step between adjacent cells at the regrade boundary and smooth artificial
  steps
gotchas:
- 3,072 Interim cells sat at one elevation (2555.77 ft), 6-30 ft above ground; this
  drove a 34.6 ac over-1-ft dWSE cluster
- Regrade-boundary steps up to 7 ft were reduced to 2.5 ft and 185 residual placeholder
  cells replaced
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 23.10.25, Python 3.12
evidence:
- D:\Star Valley CLOMR\Comment 4 - Development Effects\Revised Inputs\CHANGE-MEMO.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\topo_vs_survey.py
hours_lost: 4.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:12+00:00'
schema_version: 1
---
