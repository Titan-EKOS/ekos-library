---
id: STARVALLEY-020
title: Scripted CLOMR model build and post-processing chain
type: skill
function: report-assembly
trigger: Producing a FEMA CLOMR package (duplicate effective, existing, proposed models,
  results, GIS, exhibits, report tables) that will go through several rebuilds
steps:
- build_models.py regenerates every derived input from source surfaces, centerline
  and design data; log cell counts and surface sources
- Keep a shared helper module for grid, TOPO, LandXML and transform readers; drive
  package variants by environment variables
- 'postchain: postprocess results, structure flows, dWSE location tables, zones, model
  shapefiles, Appendix D warnings, QGIS exhibits, report writer, package QC'
- 'Appendix D: tabulate every ERROR.CHK and runtime-warning message per model, mark
  those also in the duplicate-effective run as inherited, give a disposition'
- Write a README for the package and build zips (ZIP64) at the end; compile a review
  PDF of all exhibits and documents
gotchas:
- Report text generated from code leaked a template fragment into the TDN draft (a
  Python conditional string appears in section 4.8.3); scan generated docx for code
  fragments before release
- Keep backups of each script version (v3bak, v4bak) so a regression can be traced
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: Python 3.12, QGIS 3.44.12 (python-qgis-ltr), python-docx, FLO-2D Pro
  Build 26.02.25
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\build_models.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\postchain.ps1
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\appendix_d_warnings.py
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\06 Report\SV-CLOMR_TDN_Narrative_4th-Submittal_DRAFT.docx
hours_lost: 3.0
recurrence: 6
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:14+00:00'
schema_version: 1
---
