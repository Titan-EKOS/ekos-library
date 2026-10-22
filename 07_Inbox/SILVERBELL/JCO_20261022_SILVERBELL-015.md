---
id: SILVERBELL-015
title: User-defined arch section geometry for HY-8
type: skill
function: hydraulics-model-run
trigger: Arch or non-standard barrel shape must be entered in HY-8 as user-defined
  coordinates.
steps:
- Define crown radius, haunch radius, span and rise; solve springline height and tangent
  point.
- Integrate exact opening area; generate about 19 paired coordinates and check polygon
  area within 0.3 pct.
- Save coordinates to JSON beside the model; edit the .hy8 text file from a seed crossing
  for repeat cases.
- Run analysis and Create Report natively; keep the exported native report as output.
gotchas:
- HY-8 GUI automation through dialogs was slow and fragile; text editing of a seed
  .hy8 file was faster.
- Inlet relationships for user-defined shapes are generic; note no manufacturer inlet
  data.
- LibreOffice was not available for docx rendering; Word export used for page QA.
jurisdiction: n/a
tools_versions: HY-8 8.00, scipy
evidence:
- C:\Users\Titan\OneDrive\Silverbell -Goret to Camino del Cerro\JCO_20261007_Culvert_Comparison\section_geometry.json
- C:\Users\Titan\OneDrive\Silverbell -Goret to Camino del Cerro\JCO_20261007_Culvert_Comparison\Silverbell_BC4_Arch_Comparison.hy8
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Silverbell_Goret_to_Camino_del_Cerro\2026-10-07_d19152bc879c.txt
  (from Codex session 2026-10-07)
hours_lost: 0.5
recurrence: 2
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:27+00:00'
schema_version: 1
---
