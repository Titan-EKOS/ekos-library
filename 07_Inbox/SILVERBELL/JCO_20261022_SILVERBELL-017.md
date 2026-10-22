---
id: SILVERBELL-017
title: Presentation exhibit maps with FEMA overlay on aerial
type: skill
function: exhibits
trigger: Interview or public meeting needs location exhibits (FEMA overview, floodway
  crossing, historic crossing).
steps:
- Pull aerial basemap and effective FEMA layers for each exhibit extent; save source
  and location JSON.
- Render PNG plus combined PDF; inspect preview and PDF QA images before delivery.
- Keep editable slides with native tables; detailed discussion in presenter notes.
gotchas:
- Image date can differ from lidar date; credit imagery source on each exhibit.
jurisdiction: n/a
tools_versions: Python, matplotlib, Esri imagery
evidence:
- C:\Ekos\projects\silverbell\make_presentation_maps.py
- D:\Silverbell Proposal\Presentation Graphics\2026-09-14\Silverbell_Presentation_Exhibits.pdf
hours_lost: 0.5
recurrence: 2
confidence: medium
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:27+00:00'
schema_version: 1
---
