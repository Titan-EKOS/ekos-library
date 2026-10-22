---
id: EKOS-LOCAL-014
title: Plan reading - keep WSEL, crest, invert, banktop and apron dimensions separate
type: qc_rule
function: qc
trigger: Reading detention basin, channel or outlet sections from record plans for
  model inputs
steps:
- Identify dimension-arrow endpoints on the image before assigning meaning
- Subtract labeled WSEL and invert in the same datum and compare with any claimed
  depth
- Store WSEL, banktop, crest, apron size and utility inverts as separate fields
- Never take weir width from slab width or scale an NTS section
- Do not treat a historical 100-yr WSEL as an overflow crest, and do not treat a DEM
  minimax path as a weir length
- Keep historical datum offsets (e.g. +2.21 ft candidate) as unadopted until a common
  monument tie is verified
gotchas:
- Local model read a 10 ft arrow to banktop as 10 ft water depth; WSEL minus invert
  was 7.7 ft
- Model conflated WSEL with a datum and with the crest
- An 8-inch adjacent utility was nearly taken as the basin outlet
- 'Recurrence note: 3 misreadings corrected by supervisor'
jurisdiction: Pima County RFCD / City of Tucson
tools_versions: Qwen3.5-9B vision, Python Decimal checks
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB041.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-021.md
- D:\LocalAI_Test\EKOS_Runtime\EXECUTION_CHECKPOINT.md
hours_lost: 2.0
recurrence: 3
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:19+00:00'
schema_version: 1
---
