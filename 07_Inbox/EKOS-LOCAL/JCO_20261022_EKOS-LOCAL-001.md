---
id: EKOS-LOCAL-001
title: Unattended local supervisor agent - stop conditions, current-state manifest
  and completion gates
type: agent
function: other
trigger: Any unattended local-model run that plans steps, calls tools and drafts a
  drainage report without cloud supervision
steps:
- Give the supervisor a compact current-state manifest (completed milestones, open
  blockers, accepted inputs) generated from structured outputs; never feed it the
  append-only checkpoint or history log as a source for drafting
- Read JSON evidence as parsed structured objects or targeted keys, not fixed 50-line
  text windows
- Fingerprint repeated work on action plus target file (ignore offset and window arguments);
  after 2 repeats force a different action or end the branch
- Cap native retries at 2 identical attempts and at most 2 materially different recoveries,
  then log the issue and move to an independent branch
- Gate completion on required native artifacts (fresh output files, numeric checks,
  provenance), not on the count of filled report sections
- On exit write a terminal heartbeat and reconcile state, queue and actual process
  existence before sending any notification
- Use distinct end states (completed, partial, blocked, failed); a draft with unresolved
  modeling is partial and the alert must say so
- Honor an owner STOP_REQUESTED file and a single-instance lock
gotchas:
- Continuation run ended after 8 steps (about 20 s) with LOCAL_DRAFT_READY_WITH_UNRESOLVED_MODELING
  after re-reading the same summary.json 3 times in 50-line windows; no hydraulic
  work was attempted
- Sections drafted from EXECUTION_CHECKPOINT.md repeated superseded statements (supervisor
  not implemented, stale pending tasks) and misread a task label as a project name;
  fix is drafting only from a curated current manifest and structured result tables
- One section failed on an unterminated JSON string from the local model after 2 bounded
  attempts; section was left Unresolved (correct behavior, keep it)
- Heartbeat stayed LOCAL_REASONING after the run terminated; add a final heartbeat
  write in a finally block
- Exact-match loop detection is evaded by small argument changes (start or line offsets)
- Fourteen filled report headings looked complete while all RAS 1D/2D, HY-8 and 100-yr
  routing were missing
- 'Recurrence note: 3 autonomous pilots (001, 002 replay, continuation 003), all ended
  without hydraulic progress'
jurisdiction: General (tested on Pima County RFCD drainage report)
tools_versions: LM Studio 0.4.21 local server, Qwen3.5-9B alias ekos-evidence-worker,
  Python 3.12, autonomous_supervisor.py 2026-09-22
evidence:
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\50_Deliverables\Autonomous_Review\state.json
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\50_Deliverables\Autonomous_Review\step_0007.json
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\50_Deliverables\Autonomous_Review\heartbeat.json
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\50_Deliverables\Autonomous_Review\decisions_and_questions.jsonl
- D:\LocalAI_Test\EKOS_ORCHESTRATION_REVIEW.md
- D:\LocalAI_Test\EKOS_Runtime\autonomous_supervisor.py
hours_lost: 6.0
recurrence: 3
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:07+00:00'
schema_version: 1
---
