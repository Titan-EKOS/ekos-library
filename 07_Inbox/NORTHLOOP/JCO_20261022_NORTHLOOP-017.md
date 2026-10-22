---
id: NORTHLOOP-017
title: Trial grading QA - easements, slope tie-ins, fill depth vs geotech
type: qc_rule
function: qc
trigger: Building trial proposed grading on a model grid (raised pad, new channel)
steps:
- Overlay recorded permanent and temporary easements; report cut/fill area and max
  depth inside each
- Screen adjacent cell pairs for newly steepened slopes beyond 3:1 (about 35.3%),
  especially where an inherited channel is clipped
- Compare max fill depth with the geotech settlement basis; compare infiltration test
  locations with basin locations
- Report earthwork as screening quantities (no shrink, swell or stripping)
gotchas:
- Carried-forward north channel cut about 0.10 ac of permanent water easement (up
  to 2.7 ft)
- Clipping the old channel left 7 cell pairs up to 0.87 ft/ft slope; scenario 02 results
  mixed pad and bad tie-in effects
- Pad needed about 12.7 ft fill while geotech covered about 12 in; infiltration tests
  were not at the basin
jurisdiction: any
tools_versions: Python 3 numpy, shapely
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\easement_overlap_screen.json
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\grading_slope_screen.json
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F19, F21,
  F22)
hours_lost: 2.0
recurrence: 3
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:31+00:00'
schema_version: 1
---
