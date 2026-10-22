---
id: SILVERBELL-018
title: Long-run monitor agent for queued RAS computations
type: agent
function: hydraulics-model-run
trigger: Several multi-hour 2D runs must run in sequence with checks between them.
steps:
- Queue runs with a status JSON; gate each next run on duration, roughness and volume
  error (for example 0.5 pct or less).
- Gate geometry-dependent runs on a review marker created only after an actual geometry
  check.
- Heartbeat every 15 min; skip if a healthy run is active; never open a writing HDF.
- Pause the heartbeat after delivery or user freeze.
gotchas:
- Old queue sessions and obsolete diagnostic runs had to be stopped to avoid duplicate
  computes.
- Generator scripts that rebuild all inputs must not run while cases compute; use
  targeted edits.
jurisdiction: n/a
tools_versions: HEC-RAS, Python
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md (QUEUE V2, Automatic follow-up)
- C:\Ekos\projects\silverbell\hydraulics\models\03_2D_Review\queue_v2.log
- C:\Ekos\projects\silverbell\hydraulics\run_2d_queue.py
hours_lost: 1.5
recurrence: 2
confidence: medium
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:28+00:00'
schema_version: 1
---
