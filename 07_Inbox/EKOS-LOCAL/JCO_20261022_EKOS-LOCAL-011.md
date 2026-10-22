---
id: EKOS-LOCAL-011
title: Connector development and recovery agent - isolated patch, regression, rollback
type: agent
function: qc
trigger: A native-application connector (PC-Hydro, HMS, RAS, HY-8, Excel) fails or
  a new capability is needed
steps:
- Work only on isolated copies; hash originals and confirm unchanged at the end
- Qualify against retained benchmark evidence first (HMS samples 28 statistics, RAS
  1D 316 WSE and flow, RAS 2D 36,862 cells) before any project use
- Make one patch at a time; rerun the regression set; keep failed patches and roll
  back on any regression
- Record what was qualified and what was not (e.g. solver replay does not qualify
  new geometry authoring)
- Activate the connector in approved_actions only after tests pass; record a lesson
  and local replay
gotchas:
- Cloud built most connectors interactively (high quota); the local recovery loop
  was never implemented
- Repeating already-passed benchmarks was used as visible progress; do not rerun unchanged
  benchmarks
- Archive readback (HY-8) was briefly treated as fresh calculation; it is not
- 'Recurrence note: 6 connectors'
jurisdiction: General
tools_versions: HEC-HMS 4.13, HEC-RAS 6.6, HY-8 8.00.2, PC-Hydro 7.4, connector_validation.py
evidence:
- D:\LocalAI_Test\EKOS_Runtime\CONNECTOR_RESULTS.md
- D:\LocalAI_Test\EKOS_Runtime\CONNECTOR_DEVELOPMENT_PLAN.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydraulics\KB-006.md
- D:\LocalAI_Test\EKOS_ORCHESTRATION_REVIEW.md
hours_lost: 4.0
recurrence: 6
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:18+00:00'
schema_version: 1
---
