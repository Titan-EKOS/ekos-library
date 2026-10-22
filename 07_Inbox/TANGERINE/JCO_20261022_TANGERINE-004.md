---
id: TANGERINE-004
title: Name HEC-RAS plans meaningfully and cite plan ID and geometry from the plan
  file headers
type: qc_rule
function: hydraulics-model-run
trigger: Report text, figure captions or tables cite a HEC-RAS plan as existing or
  proposed
steps:
- Read Plan Title, Short Identifier and Geom File from each .pXX header and Current
  Plan from the .prj
- Rename plans with generic titles (Plan 01, Plan 03, Plan 12) to condition-specific
  names before results are reported
- Keep a plan register (plan, short ID, geometry, terrain, condition, status superseded
  or live) in the model folder
- Cite plan file, short ID and geometry in every caption and table that uses results
gotchas:
- Report and figure captions cite existing conditions as Plan 12 / EX_JCO_LG, but
  p12 is titled Plan 12 with no short ID (geometry g08), and the project notes name
  p09 EX_JCO as existing; no plan file carries EX_JCO_LG
- 12 plans and 8 geometries in one project with superseded iterations p01-p08 make
  the wrong HDF easy to read; confirm the plan before exporting rasters
jurisdiction: any
tools_versions: HEC-RAS 6.6 / 7.0
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Psomas Hydraulic Modeling\WorkingMAM-RAS\ASL_Marana.p12
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Psomas Hydraulic Modeling\WorkingMAM-RAS\ASL_Marana.p09
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\CLAUDE.md
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Drainage_Concept_Report_DRAFT.docx
  (Sec 5.7, Figure 2 caption)
hours_lost: 0.5
recurrence: 2
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:06+00:00'
schema_version: 1
---
