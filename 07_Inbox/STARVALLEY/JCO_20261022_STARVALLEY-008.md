---
id: STARVALLEY-008
title: dWSE and 44 CFR 65.12 rise analysis from FLO-2D outputs
type: skill
function: hydraulics-model-run
trigger: Showing whether a proposed project raises base flood elevations more than
  1.00 ft against existing conditions (FLO-2D, shallow flooding)
steps:
- Confirm both models share the same grid cell by cell (CADPTS identical) so differences
  are exact
- Read MAXWSELEV.OUT and DEPTH.OUT; compute dWSE = proposed minus existing
- Evaluate rises where the cell is in the SFHA (max depth at least 1.0 ft) in both
  conditions; report any-depth counts separately
- Map new SFHA cells (at least 1 ft proposed, under 1 ft existing) and removed SFHA
  cells
- List every cell over 1.00 ft with ground change, depth change, and whether it lies
  on applicant land, inside approved grading, or in the channel prism
- Write rasters, over-1-ft polygons, summary json and an exhibit; quote values from
  these files in the report
- For cells on other ownership prepare alternatives, notices on the CLOMR template
  and PE certification
gotchas:
- Extreme dWSE values at fill slopes and excavated basins come from ground change,
  not flood change; review before quoting min/max
- A 34.6 ac over-1-ft cluster came from a placeholder flat surface in the proposed
  TOPO, not real grading
- Property-boundary linework is needed to classify edge cells; request it early
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FLO-2D Pro Build 26.02.25, Python 3.12, numpy, geopandas, rasterio
evidence:
- D:\Star Valley CLOMR\WSEL Comparison\README-Methodology.txt
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\dwse_where.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\dwse_where_INT.txt
hours_lost: 8.0
recurrence: 3
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:10+00:00'
schema_version: 1
---
