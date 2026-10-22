---
id: TANGERINE-003
title: Run existing and proposed 2D models on a common mesh before no-adverse-impact
  claims
type: qc_rule
function: hydraulics-model-run
trigger: Any report text says the proposed condition maintains existing flow distribution,
  depths or downstream discharge
steps:
- Build existing and proposed geometries from the same 2D flow area perimeter, cell
  size and breaklines; change only terrain and roughness
- Produce cell-by-cell difference maps for depth, WSE, velocity and shear
- Tabulate existing vs proposed peak Q, volume, timing, WSE, depth and velocity at
  upstream inflows, property boundaries, roadway crossings and downstream constraints
  (railroad and freeway embankments)
- Only then state no adverse impact; otherwise label the comparison distributional
  and qualitative
gotchas:
- The concept report compared meshes of different extent and resolution and still
  drew strong conclusions; three reviewer comments (T1-6, T1-11, R-1) asked for a
  common-mesh re-run, now deferred to the master drainage report
jurisdiction: Town of Marana; Pima County RFCD
tools_versions: HEC-RAS 6.6 / 7.0 2D unsteady
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Comments\Internal\Comments
  B.docx
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Comment_Response_Report.docx
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Psomas Hydraulic Modeling\WorkingMAM-RAS\ASL_Marana.prj
hours_lost: 4.0
recurrence: 3
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:06+00:00'
schema_version: 1
---
