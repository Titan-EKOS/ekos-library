---
id: STARVALLEY-013
title: Model development effects in FLO-2D without building footprints
type: skill
function: hydraulics-model-run
trigger: Proposed residential development must be represented in FLO-2D (FEMA asks
  for ARF, IRAINBUILDING, n and infiltration updates) but lot layouts or footprints
  are not final
steps:
- Measure building coverage on a comparable built block from county building footprints
  (count buildings and lots, coverage ratio)
- Apply ARF = WRF = measured ratio (0.35 here) on lot cells in ARF.DAT; set IWRFS
  = 1 in CONT.DAT and IRAINBUILDING = 1 in RAIN.DAT
- 'Classify cells from transformed lot and ROW linework: lots n 0.040, paved streets
  n 0.016'
- 'Compute CN on the unblocked-area basis so roof runoff is not double counted: non-roof
  impervious = (lot imperv - ARF)/(1 - ARF)'
- Keep FPLAIN.DAT n and elevation columns in sync with MANNINGS_N.DAT and TOPO.DAT
- Document every edit in a change memo and the build log
gotchas:
- Earlier submittal carried full-imperviousness CN 93.7-95.3 plus no ARF; replaced
  by an ARF-compatible set
- Open space lumped with ROW gives a conservatively high CN; refine if mapping is
  available
jurisdiction: FEMA Region IX / Pima County RFCD
tools_versions: FLO-2D Pro Build 23.10.25 and 26.02.25, TR-55
evidence:
- D:\Star Valley CLOMR\Comment 4 - Development Effects\Revised Inputs\CHANGE-MEMO.txt
- D:\Star Valley CLOMR\Comment 4 - Development Effects\Block18-Building-Coverage-Measurement.txt
hours_lost: 4.0
recurrence: 1
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:11+00:00'
schema_version: 1
---
