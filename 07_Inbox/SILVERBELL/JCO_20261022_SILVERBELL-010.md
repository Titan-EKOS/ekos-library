---
id: SILVERBELL-010
title: Blender crossing renderings from CAD and RAS geometry
type: skill
function: exhibits
trigger: Proposal or public exhibit needs 3D views of culvert and bridge crossings
  with modeled water.
steps:
- Use native CAD sections, barrel endpoints, project terrain and current model water
  surface; sample display terrain at about 10 ft.
- Two cameras per crossing - aerial looking upstream from downstream side, and pedestrian
  view through the barrel.
- Semi-transparent water, ground-draped FEMA lines, wide views showing both ties.
- Plot each view to PDF plus a combined PDF; label water source and concept status
  on each.
gotchas:
- Fill display closed over open barrels at C21, C22, C23, C45 and C01; a separate
  fill-closure pass was needed after each rebuild.
- Bridge views needed natural ground restored under the deck and pavement finishing
  passes.
- Renderings kept showing provisional 1D water after design changes; note the water
  basis on each sheet.
- Thumbnail and OptiX cache write warnings are harmless.
jurisdiction: n/a
tools_versions: Blender 5.2 Cycles, Python
evidence:
- C:\Ekos\projects\silverbell\renderings\README.md
- C:\Ekos\projects\silverbell\renderings\C22_render.log
- C:\Ekos\projects\silverbell\v4\restore_culvert_fill_display.py
- D:\Silverbell Proposal\Review_2026-09-13\Current_Review_Package\Renderings
hours_lost: 4.0
recurrence: 5
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:25+00:00'
schema_version: 1
---
