---
id: TANGERINE-006
title: Concept report exhibit set from 2D results over aerial (11x17, versioned)
type: skill
function: exhibits
trigger: Producing figures for a concept drainage report from HEC-RAS or FLO-2D result
  rasters
steps:
- Confirm with the PM whether figures must be editable; if so build them in QGIS or
  CAD from the start, not as scripted images
- Use one CRS for all layers (NAD83 AZ Central ft intl for this project) and check
  every .prj sidecar
- Draw over current aerial with semi-transparent depth classes; use the same scale,
  classes and legend for existing and proposed sheets
- Show protected areas (Preserve), property boundary, parcels, roads, easements and
  named washes on every map sheet
- Add large-scale insets or typical cross-sections where text cites a corridor width
- Export full-size 11x17 sheets, add PDF bookmarks per figure, and increment the filename
  suffix (v2, v3) instead of overwriting
gotchas:
- Three exhibit versions were exported within about 2.3 hr on the submittal morning
  (v1, v2 adding Figure 12, v3 16 min later); finish the figure list before export
- Scripted matplotlib PDFs could not be edited by the user, who later asked for the
  figures to be recreated in QGIS or CAD
- Reviewers found report-scale figures too dense and the Preserve boundary missing;
  full-size sheets and the Preserve polygon on every map closed B-1, P2-7, P2-8
- A DRAFT date in every title block forces replotting the set when the date changes
jurisdiction: Town of Marana
tools_versions: matplotlib 3.10.9, rasterio, geopandas; QGIS requested for edits
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Exhibits_11x17.pdf
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Exhibits_11x17_v2.pdf
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Exhibits_11x17_v3.pdf
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_AZ_State_Land_Tangerine_Corridor\2026-10-13_615c5525ad67.txt
  (from Codex session 2026-10-13)
hours_lost: 2.3
recurrence: 4
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:07+00:00'
schema_version: 1
---
