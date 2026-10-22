---
id: EKOS-LOCAL-019
title: Do not adopt imperviousness from model-labeled imagery without independent
  labels
type: qc_rule
function: hydrology
trigger: Estimating percent impervious or vegetative cover from NAIP imagery with
  local AI labels
steps:
- Use dated native-resolution imagery with locked raster IDs and receipts
- Build training and holdout labels independently of the model being tested; check
  shadow and tree occlusion
- Report agreement as diagnostic only; set a minimum acceptance before using percentages
- If the classifier fails, run explicitly labeled cover scenarios (S1/S2/S3) instead
gotchas:
- Classifier on 128 model-labeled points reached 68.75 percent agreement (67 percent
  balanced) with 60 percent of the main catchment unknown; failed and was not used
- Model labeled a shadow as vegetation; labels are not field truth
- First imagery set did not cover the north reach; check coverage of the full hydraulic
  extent separately from the watershed
- 'Recurrence note: 2 classification attempts'
jurisdiction: Pima County RFCD
tools_versions: USGS NAIP 2023 0.3 m 4-band, rasterio 1.5, Qwen3.5 vision
evidence:
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\audited-imagery-classifier-001.log
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-022.md
- D:\LocalAI_Test\EKOS_Runtime\EXECUTION_CHECKPOINT.md
hours_lost: 2.0
recurrence: 2
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:21+00:00'
schema_version: 1
---
