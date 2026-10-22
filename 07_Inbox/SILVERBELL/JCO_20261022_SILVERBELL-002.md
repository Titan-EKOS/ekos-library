---
id: SILVERBELL-002
title: Fixed-map floodway screening holds existing encroachment stations
type: qc_rule
function: hydraulics-model-run
trigger: Floodway impact screening when no duplicate-effective model is available.
steps:
- Use effective mapped floodway lines to set encroachment stations (Method 1) on the
  existing-condition model.
- Hold the same stations unchanged in the proposed model and compare floodway WSEL
  to isolate project impact.
- Restrict encroachment to the project reach plus approaches; do not apply to far
  upstream/downstream polygon pieces.
- State in the result basis that this is screening, not certification; do not block
  the modeling on the effective model.
gotchas:
- Agent initially wanted a duplicate-effective baseline first; JCO clarified the fixed-map
  intent.
- First trial over all 100 intersecting XS reported a spurious 23.7 ft surcharge from
  disconnected polygon pieces; limiting to the project reach gave about 4 ft existing
  surcharge and 0.16 ft max project rise.
- Clipping FEMA floodway polygons for display before deriving boundaries broke the
  hydraulic areas; derive boundaries from full polygons, clip only the display linework.
jurisdiction: FEMA / Pima County RFCD
tools_versions: HEC-RAS 1D steady, FEMA NFHL download
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md (revision 4 floodway clarification,
  08:30 continuation)
- C:\Ekos\projects\silverbell\hydraulics\build_mapped_floodway.py
- C:\Ekos\projects\silverbell\hydraulics\check_mapped_floodway.py
- C:\Ekos\projects\silverbell\hydraulics\models\07_Revision4_Floodway
hours_lost: 2.0
recurrence: 2
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:22+00:00'
schema_version: 1
---
