---
id: TANGERINE-016
title: Rillito Substation report - PDF bookmarks on every report and exhibit PDF
type: qc_rule
function: compile-pdf
trigger: Any report or exhibit PDF issued for review or submittal
steps:
- Add bookmarks at minimum for cover, table of contents, each main section, each figure
  and each main appendix
- Generate them by script from headings and figure captions rather than by hand
- Open the PDF and confirm the bookmark tree before issue
gotchas:
- JCO general comment on the Rillito Substation draft; the Tangerine 96-page report
  PDF and all three exhibit PDFs also had none
jurisdiction: any
tools_versions: Bluebeam Revu, pypdf
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Rillito Substation-Drainage
  Report-DRAFT1 - QAQC_JCO.pdf p.1 comment 2 (JCO)
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Exhibits_11x17_v3.pdf
hours_lost: 0.5
recurrence: 3
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:11+00:00'
schema_version: 1
---
