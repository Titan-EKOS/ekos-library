---
id: STARVALLEY-012
title: FLO-2D hydraulic structure setup checks (zero-flow culverts)
type: qc_rule
function: hydraulics-model-run
trigger: Adding culverts or basin structures to HYSTRUC.DAT, or HYDROSTRUCT.OUT shows
  zero flow where flow is expected
steps:
- Inlet and outlet cells must not be channel-interior cells (between a channel element
  and its bank cell); use the channel element or a true floodplain cell
- Set IFPORCHAN to match the actual inlet/outlet cell types
- For rating tables set ICURVTABLE = 1 (table), not 0 (curve)
- With HEADREFEL 0 re-reference HY-8 headwater from culvert invert to inlet-cell bed
  and record the offset
- Export tables from one HY-8 project with matching names; discharge range covers
  the model peak with no extrapolation
- After each run read per-structure peak and volume (struct_flows.py) and stop if
  any wet-inlet structure shows zero flow
gotchas:
- 'Four rebuilds (v5, v5a, v5b, ALT-A) passed zero flow before the cause was found:
  inlets on channel-interior cells (DEPFP=0); ICURVTABLE 0 was a second, separate
  bug'
- June basin structures had inlets on 1D channel elements declared as floodplain and
  a table assuming full-basin tailwater; FEMA noted zero flow and HY-8 name/range
  mismatch
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 26.02.25, HY-8 8.0
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\01 Models\_run_log.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\alt_a_outlets.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\struct_flows.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\07 Response Matrix and
  Cover Letter\Response_Matrix_AD02_and_Closure.xlsx
hours_lost: 8.0
recurrence: 5
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:11+00:00'
schema_version: 1
---
