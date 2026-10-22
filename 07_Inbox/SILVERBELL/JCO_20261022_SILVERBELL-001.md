---
id: SILVERBELL-001
title: Rapid proposal-stage hydraulic screening from existing studies
type: agent
function: hydraulics-model-run
trigger: Proposal or interview needs a corridor drainage screening in 24-48 hr using
  only supplied DCR, existing HEC-RAS models and public data.
steps:
- Inventory supplied studies, DCR pages and models; record which are effective FEMA
  vs later local updates.
- Reproduce the supplied source model exactly (all profiles, all XS) before any edits;
  save as model 00.
- Expand terrain from public USGS 1 m lidar, reproject to project state plane ft,
  clip to a set buffer.
- Build existing and proposed tributary reaches; iterate receiving-stream tailwaters
  until converged.
- Run paired existing/proposed Q100, map depth and WSEL change, publish a short screening
  review PDF.
- Keep a running scope/checkpoint file with what is provisional, what failed, and
  what must not be claimed.
gotchas:
- Local-peak tributary runs with iterated tailwaters are not a connected mass-conserving
  junction network; label results as screening.
- Source local model differed from FEMA effective; no no-rise or CLOMR finding can
  be drawn from it.
- Long autonomous runs need a checkpoint file that supersedes older status text, or
  later sessions act on stale state.
jurisdiction: Pima County RFCD / FEMA
tools_versions: HEC-RAS (native COM and RasMapper), Python, USGS 1 m 3DEP
evidence:
- C:\Ekos\projects\silverbell\ACTIVE_SCOPE.md
- C:\Ekos\projects\silverbell\REVIEW_STATUS.md
- D:\Silverbell Proposal\Review_2026-09-13\SVB-Hydraulic-Screening-Review.pdf
- C:\Ekos\projects\silverbell\hydraulics\models\00_Source_Reproduction
hours_lost: 8.0
recurrence: 1
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:22+00:00'
schema_version: 1
---
