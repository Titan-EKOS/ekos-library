---
id: TANGERINE-007
title: Load official boundary GIS before any land-budget or riparian overlap numbers
type: qc_rule
function: data-gathering
trigger: A report quantifies acreage of development, preserve, riparian habitat or
  swap land
steps:
- Obtain the official property, preserve and parcel GIS from the client team before
  computing any acreage
- Record source, date and CRS of each layer in a data log
- Compute overlaps (riparian in parcels, dry non-riparian land outside corridors)
  with a script so numbers can be rerun when layers change
- After any layer update, rerun and push numbers to text, tables and figures in one
  pass
gotchas:
- After the official boundary and preserve GIS arrived, swap land dropped from about
  1,197 ac to 673 ac and baseline riparian preservation changed from about 55% to
  73%; text, tables 8-1 and 8-2 and Figures 10-11 all had to be redone
jurisdiction: Pima County riparian classification
tools_versions: geopandas, shapely
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Comment_Response_Report.docx
  (Sec 1.0)
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Exhibits\GIS_v2
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Exhibits\GIS_v3
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Exhibits\GIS_Optimized
hours_lost: 2.0
recurrence: 1
confidence: medium
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:08+00:00'
schema_version: 1
---
