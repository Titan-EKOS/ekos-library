---
id: NORTHLOOP-019
title: Confirm survey vertical datum before setting pad elevation
type: qc_rule
function: data-gathering
trigger: Setting a pad or floor elevation against a modeled WSE using new survey and
  older model terrain
steps:
- Find the datum and benchmark note in the survey; if absent, request it
- Compare the new survey surface with the model grid; list differences over 2 ft
- Reconcile units (metric survey vs feet plans) before any grid update
- Update the grid from the original survey triangles, not a new triangulation
gotchas:
- Survey CAD had no datum or benchmark statement; pad elevation and WSE remain provisional
- An early Delaunay terrain was replaced by exact LandXML triangles (26,507 cells
  updated)
jurisdiction: any
tools_versions: Civil 3D LandXML; Python 3
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\survey_cad_text.json
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F13)
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\CONTINUATION_NOTES.txt
hours_lost: 1.0
recurrence: 2
confidence: medium
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:32+00:00'
schema_version: 1
---
