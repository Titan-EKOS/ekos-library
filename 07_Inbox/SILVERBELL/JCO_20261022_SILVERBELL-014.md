---
id: SILVERBELL-014
title: Contractor culvert substitution check in HY-8
type: skill
function: hydraulics-model-run
trigger: Contractor proposes a modified culvert shape or size and asks if headwater
  still meets the approved design.
steps:
- Locate the approved calculation in the drainage report; confirm the analyzed shape
  matches the current plan.
- If no approved model exists for the plan shape, rebuild a baseline from plan dimensions
  with stated assumptions.
- Model baseline and revised shape with identical flow, slope, n, length and fixed
  tailwater from the report model.
- Bracket unknown entrance (Ke 0.2 bevel and 0.5 square) and add a high-tailwater
  and full-flow stress case.
- Compare HW to the report existing-condition HW; write a 1-page memo with native
  output and report excerpts.
gotchas:
- Report analyzed six 12x8 ft boxes; later plan shows three 24x8 ft arches. Plan HW
  note repeated the old box result.
- Request said drainage area reduction; it was opening area per cell (about 10 sq
  ft each, 29-30 sq ft total).
- Original flow split between two openings; also test full crossing flow through one
  structure.
- Recomputed arch area loss (10.00 sq ft) differed from contractor value (9.58); report
  the difference.
- Result was HW rise 0.45-0.50 ft, still at least 2.6 ft below existing HW.
jurisdiction: City of Tucson
tools_versions: HY-8 8.00, Python
evidence:
- C:\Users\Titan\OneDrive\Silverbell -Goret to Camino del Cerro\JCO_20261007_Culvert_Comparison\Source_Review_and_Required_Inputs.txt
- C:\Users\Titan\OneDrive\Silverbell -Goret to Camino del Cerro\JCO_20261007_Culvert_Comparison\Silverbell_BC4_Technical_Memo.pdf
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Silverbell_Goret_to_Camino_del_Cerro\2026-10-07_d19152bc879c.txt
  (from Codex session 2026-10-07)
hours_lost: 1.0
recurrence: 1
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:26+00:00'
schema_version: 1
---
