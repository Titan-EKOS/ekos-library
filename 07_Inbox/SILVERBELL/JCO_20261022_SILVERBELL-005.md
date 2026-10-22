---
id: SILVERBELL-005
title: Native 2D HEC-RAS review model with synthetic hydrographs
type: skill
function: hydraulics-model-run
trigger: Need existing/proposed/alternative 2D runs for a corridor crossing screening.
steps:
- Clip domain to a set distance past the project ends; refine cells (10 ft tributary,
  25 ft main river, 100 ft elsewhere).
- Synthetic Q100 hydrograph 3 hr rise, 6 hr peak hold, 3 hr recession; state it is
  not a calibrated event.
- Run a 1 hr diagnostic first; then full event; check volume error, iteration warnings,
  hydrographs, wet boundary.
- Associate roughness through native RasProcess geometry association with a default
  NoData n; channel polygons first (first polygon wins).
- Use bridge type 32 (rating curves) under diffusion wave; type 33 needs full SWE.
gotchas:
- Opening an HDF while RAS was writing caused a write failure; the mesh was discarded
  and rebuilt. Never read active .tmp.hdf.
- Direct HDF-only roughness patches did not persist; use the native association.
- Proposed run had 3,520 iteration warnings and 17.1 ft max WSEL error at 0.25 pct
  volume error; not accepted. Existing run 517,161 cells, 1 hr 39 min, 0.000136 pct.
- Ambiguous duration from the user (3 6 hours) was interpreted and logged; confirm
  such inputs early.
jurisdiction: Pima County RFCD
tools_versions: HEC-RAS 2D diffusion wave, 8 cores, 5 s fixed step
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md
- C:\Ekos\projects\silverbell\hydraulics\models\03_2D_Review\RUN_STATUS.json
- C:\Ekos\projects\silverbell\v4\CHECKPOINT_1348.md
- C:\Ekos\projects\silverbell\hydraulics\run_2d_queue.py
hours_lost: 5.0
recurrence: 3
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:23+00:00'
schema_version: 1
---
