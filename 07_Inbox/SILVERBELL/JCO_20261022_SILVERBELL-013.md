---
id: SILVERBELL-013
title: Effective FEMA reference layers from NFHL into CAD, Mapper, renders
type: skill
function: data-gathering
trigger: Exhibits or models need effective 1-pct, 0.2-pct and floodway linework.
steps:
- Download zones, boundaries, panels, LOMRs, XS, BFE lines from NFHL for the project
  extent.
- Save native CAD reference drawing, RAS Mapper layers and render overlays from the
  same set.
- List LOMRs and compare to the hydraulic baseline before any regulatory statement.
gotchas:
- Display-clipped polygons must not feed hydraulic encroachment logic (see SILVERBELL-002).
- The supplied updated local model plus mapped lines is a screening, not a duplicate-effective
  model.
jurisdiction: FEMA
tools_versions: FEMA NFHL REST, Python
evidence:
- C:\Ekos\projects\silverbell\hydraulics\fetch_effective_fema.py
- C:\Ekos\projects\silverbell\hydraulics\export_fema_references.py
- C:\Ekos\projects\silverbell\hydraulics\effective_fema
hours_lost: 1.0
recurrence: 2
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:26+00:00'
schema_version: 1
---
