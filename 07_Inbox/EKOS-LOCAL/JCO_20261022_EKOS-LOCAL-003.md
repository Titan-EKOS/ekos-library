---
id: EKOS-LOCAL-003
title: Cloud supervisor budget - one planning handoff, one consolidated exception
  packet, one final QA
type: agent
function: other
trigger: Using a paid cloud model (Codex, Claude, GPT) to supervise local models on
  an engineering job
steps:
- Cloud writes the plan and task list once, then stops; local worker executes
- Local agents make reversible choices and owner-authorized preliminary assumptions,
  log them with source, rationale and affected outputs
- Batch unresolved questions into one review packet (completed milestones, decisions
  to review, failed attempts with evidence paths, grouped questions); omit routine
  status and unchanged files
- Cloud answers come back as structured decisions plus draft lessons; local replay
  is required before a lesson is marked verified
- Schedule at most one daily cloud check; never a 15 or 30 minute heartbeat
- When the cloud solves a novel issue it records the procedure with knowledge.put
  and has the local worker replay it, instead of computing results itself
gotchas:
- Cloud supervision with 15-30 minute heartbeats, incremental connector development,
  repeated image reviews and 24 review-package refreshes used about 50 percent of
  the weekly cloud quota in about 1.5 days; owner judged it more than doing the job
  directly
- Cloud agent kept ending its turn with a final response, so nothing ran between owner
  prompts; progress updates must not end the work turn
- Cloud started doing calculations itself; owner correction - the local AI must do
  the calcs, cloud only plans, teaches and reviews
- Cloud fetched source data itself; owner correction - teach the local worker the
  retrieval procedure so it can repeat it
- 'Recurrence note: about 20 scheduled cloud heartbeats overnight plus 4 owner corrections'
jurisdiction: General
tools_versions: Codex desktop with automations, LM Studio local models
evidence:
- D:\EKOS\Library\00_Inventory\_local\codex_text\D_LocalAI_Test\2026-09-21_d92e6073ab48.txt
  (from Codex session 2026-09-21, owner prompts U13, U14, U34, U40)
- D:\LocalAI_Test\EKOS_Runtime\LOW_USAGE_ORCHESTRATION_PLAN.md
- D:\LocalAI_Test\EKOS_INDEPENDENT_REVIEW_PROMPT.md
- D:\LocalAI_Test\EKOS_ORCHESTRATION_REVIEW.md
hours_lost: 10.0
recurrence: 20
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:11+00:00'
schema_version: 1
---
