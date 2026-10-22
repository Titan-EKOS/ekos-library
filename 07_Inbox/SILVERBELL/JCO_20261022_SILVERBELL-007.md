---
id: SILVERBELL-007
title: Civil 3D reconstruction from DCR PDF and GIS linework
type: skill
function: project-setup
trigger: Only a PDF DCR and GIS linework exist and a native Civil 3D base, corridor
  and plan set is needed.
steps:
- Extract construction baseline from PDF vector strokes; georeference to the supplied
  GIS; keep a CAD-to-plan station crosswalk.
- Build EG TIN from clipped lidar; trace proposed profile from plotted line at about
  5 ft spacing.
- Build corridor regions at source transition stations; record every schematic assumption
  on a decisions sheet.
- Produce individual sheets plus combined PDF; package with checksums per revision.
gotchas:
- Recovered chainage drifted 32.7 ft over the corridor; keep it in the crosswalk,
  do not hide it with a coordinate shift.
- Printed vertical-curve labels conflicted with the plotted line; trace follows plotted
  geometry and the conflict is flagged.
- DCR vertical datum unknown; EG vs FG differences are not earthwork depths.
- Keep the .mms companion file beside each DWG or the large surface is lost.
jurisdiction: n/a
tools_versions: Civil 3D 2026 .NET API, Python
evidence:
- C:\Ekos\projects\silverbell\README.md
- C:\Ekos\projects\silverbell\cad\build_log.txt
- C:\Ekos\projects\silverbell\sheets_v3.py
hours_lost: 4.0
recurrence: 4
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:24+00:00'
schema_version: 1
---
