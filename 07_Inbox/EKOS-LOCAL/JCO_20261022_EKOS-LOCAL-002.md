---
id: EKOS-LOCAL-002
title: Persistent local queue worker - dependency refresh, failure capture and idle
  detection
type: agent
function: other
trigger: Running registered local scripts (GIS, PC-Hydro, HMS, RAS, report build)
  overnight from a task plan
steps:
- Keep tasks in a plan file (overnight_plan.json) that maps only to registered actions
  in approved_actions.json; adding a task ID needs no restart
- Use strict dependencies for calculations and after_settled dependencies for progress
  packaging so a failed evidence job does not block the review package
- Retry only adapters marked resume_safe, with a finite attempt limit; preserve failed
  attempts and continue independent tasks
- Hold one OS-level worker lock; confirm a fresh RUNNING heartbeat, child PID and
  an advancing task log before claiming work is delegated
- When a task is replaced (e.g. 001 failed, 005 succeeds), explicitly cancel or re-point
  dependents of the failed ID
- Store stderr tail and exit reason with every failed task in the supervisor inbox
- Write a deduplicated supervisor inbox when ready work is exhausted
gotchas:
- Queue policy only adds new IDs and never refreshes dependencies of existing pending
  tasks; 3 obsolete tasks stayed pending forever on failed predecessors
- 22 of 140 tasks ended NEEDS_REVIEW, and the inbox recorded every one as error null
  with exit_code 1, so each failure had to be re-investigated from logs; capture the
  error text
- Worker in WAITING_FOR_SUPERVISOR showed 0 GPU use while the owner expected work;
  waiting is not engineering progress
- GIS venv lacked jsonschema; keep GIS calculation and local-model schema validation
  in separate qualified environments (KB-020)
- Registering a new action in worker code requires a controlled restart (RESTART_REQUESTED
  marker); the approved_actions catalog avoids that
- 'Recurrence note: 22 failed tasks of 140; 3 stuck pending'
jurisdiction: General
tools_versions: local_queue_worker.py and queue_policy.py 2026-09-21, Python 3.12
evidence:
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\queue.json
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\Local_Queue\supervisor_inbox.json
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-015.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-020.md
- D:\LocalAI_Test\EKOS_Runtime\LOCAL_WORKER.md
- D:\EKOS\Library\00_Inventory\_local\codex_text\D_LocalAI_Test\2026-09-21_d92e6073ab48.txt
  (from Codex session 2026-09-21, GPU at 0 exchange)
hours_lost: 4.0
recurrence: 22
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:11+00:00'
schema_version: 1
---
