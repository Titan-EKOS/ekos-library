---
id: NORTHLOOP-015
title: Collector channel depth - combined flow, freeboard and bend superelevation
type: qc_rule
function: hydraulics-model-run
trigger: Channel routes flow around a raised site, picking up more than one upstream
  flow path
steps:
- Size for the combined flow of all intercepted paths, not each reach alone
- Required depth = normal depth + 2 ft freeboard; check superelevation at each bend
  from the radius of curvature
- Screen bank height with a conservative case (2 x normal depth or summed peaks) and
  compare with the provided bank
- Check transitions, lateral inflow capture and basin backwater; normal depth plus
  freeboard alone may not satisfy collector channel criteria
gotchas:
- Candidate 8-ft north bank was below the 8.71-ft depth from the conservative summed
  500-yr flow; bank height had to be revisited
- 'EOR callout: flow all around to the north at about 1,945 cfs, 49 in depth + 2 ft
  freeboard, verify superelevation by radius'
jurisdiction: Town of Marana; City of Tucson collector channel provisions where adopted
tools_versions: Manning normal depth screen (Python)
evidence:
- C:\Users\Titan\OneDrive\Northloop\40_QC\T3_EOR_Review\NorthLoop_Concept1_Historical_2026-09-30_DRAFT_EOR-Markup.pdf
  p.1 callout (EOR 2021, combined flow)
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\channel_sizing_screen.json
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt (F09)
hours_lost: 1.0
recurrence: 3
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:30+00:00'
schema_version: 1
---
