---
id: SILVERBELL-008
title: Civil 3D assembly offset sign is opposite section data
type: skill
function: qc
trigger: Building corridor assemblies from scripted section data.
steps:
- Mirror assembly X when converting section offsets; positive Civil 3D offset is opposite
  the section data sign.
- Add an explicit outer boundary to the corridor surface; do not trust the automatic
  dynamic boundary.
- Export the surface and check footprint overlap against restricted parcels before
  using it for hydraulics.
gotchas:
- First TIN overlapped the restricted parcel by 36,430 sq ft from a side flip and
  invalid boundary; rebuilt as a fixed corridor.
- Stale exported FG CSV was nearly used for hydraulics; mark superseded exports explicitly.
- Wall solid extrusion along 3D paths threw eNonPlanarEntity; use planar profiles
  per segment.
jurisdiction: n/a
tools_versions: Civil 3D 2026
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md (CRITICAL CAD QA)
- C:\Ekos\projects\silverbell\v4\road_finish17_error.txt
- C:\Ekos\projects\silverbell\Current_Review_Package_2026-09-13\Verification\native_surface_parcel_qa.json
hours_lost: 2.0
recurrence: 2
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:24+00:00'
schema_version: 1
---
