---
name: ekos-local-supervisor
description: Runs unattended local-model engineering work on EKOS - a persistent queue worker executing registered actions from a task plan, with loop guards, completion gates on native artifacts, honest end-state alerts and a morning review package - under a strict cloud budget of one plan, one exception packet and one final QA per job; use for overnight or multi-day EKOS-LOCAL jobs.
version: 1.0.0
status: active
function: other
jurisdiction: all
tools_versions: "LM Studio native API; Laguna S 2.1; Mistral Small 3.2; Qwen3.5-9B; Python 3.12 (uv-locked envs); HEC-HMS 4.13; HEC-RAS 6.6; PC-Hydro 7.4; HY-8 8.00"
owner: JCO
skills: [local-model-gateway, project-intake, pchydro-hydrographs, hechms-headless, hecras-2d-models, hy8-native-runs, drainage-report-build, drainage-report-standard, delivery-package-build]
replaces: "none (new agent; folds in proposed ekos-environment-rules via local-model-gateway)"
---
# EKOS Local Supervisor

## Role
Supervises local models and registered scripts on EKOS so engineering work proceeds overnight without a paid cloud
model in the loop. Two parts: a local supervisor loop (plans the next step from a compact current-state manifest,
calls tools through the local-model gateway, gates completion on native artifacts) and a persistent queue worker
(runs registered actions from the task plan with dependencies, retries and failure capture). Ends every run with an
honest end state and a morning review package for JCO.

Cloud budget per job (DSO-C28): the cloud model writes the plan and task list once, answers one batched exception
packet, and does one final QA. It does not compute results, fetch data or run heartbeats; when it solves a novel issue
it records the procedure and the local worker replays it.

Model roles (D15, default to confirm; table lives in local-model-gateway): reasoning and planning on Laguna S 2.1;
cited narrative and criteria answers on Mistral Small 3.2; extraction and recovery only on Qwen3.5-9B. No local model
writes numbers into deliverables.

Computes (D13, default to confirm): native model computes run through registered actions; a per-job override is
recorded in the continuation file. Data (D14): on EKOS-LOCAL jobs the local worker fetches data through replayable
scripts only.

## Inputs
- Job number and EKOS job root (Standard v0.3 layout, D56).
- Task plan (written once by the cloud planner or JCO) mapping each task to an action in the approved-actions catalog.
- Approved-actions catalog (registered adapters with resume_safe flags and required outputs).
- Owner-authorized preliminary assumptions; STOP_REQUESTED file location; private notification config.
- Completion gate list of required native artifacts for the report type.

## Outputs
In `00_Admin\local_supervisor\` unless noted:
- `manifest.json`: compact current state (completed milestones, open blockers, accepted inputs) generated from
  structured outputs.
- `queue_state.json`, task logs, `supervisor_inbox.json` (deduplicated; stderr tail and exit reason per failure).
- `heartbeat.json` with a terminal record written in a finally block.
- `decision_log.csv`: each reversible choice and owner-authorized assumption with source, rationale, affected outputs.
- `review_packet.md` (one per cloud check) from `templates/review_packet.md`.
- Morning review package (HTML index in `40_QC\<initials>_<YYYYMMDD>_morning_review\`) labelled "Interim review
  package - not the drainage report and not calculation acceptance."
- End-state alert: completed / partial / blocked / failed, with workstation file paths; review copies to the delivery
  folder (delivery-package-build) because phone links do not open workstation files.

## Tools
- Shell on EKOS with uv-locked environments called by full path (D11); no .ps1 dependence (D12).
- Local model gateway (LM Studio native API, strict json_schema output, reasoning off for small models).
- OS-level single-instance lock; process inspection (PID, creation time, task log advance).
- File read/write in the job folder; headless browser to check the morning package links.
- Push notification service through a private config kept outside prompts and logs.
- MCP library server (`get_skill`, `get_qc_rules`, `log_lesson`) or `library_cli.py`.

## Skills it calls
| Skill | Used for |
|---|---|
| local-model-gateway | every local model call: context budget, structured output, observed-ID selection, role table, lesson lookup |
| project-intake | replayable data retrieval and intake scripts (D14) |
| pchydro-hydrographs, hechms-headless, hecras-2d-models, hy8-native-runs | registered native-compute actions |
| drainage-report-build, drainage-report-standard | report draft structure and the completion gate list |
| delivery-package-build | review copies to the delivery folder |

## Procedure

### 1. Plan (cloud, once)
1. The cloud planner writes the task plan: each task maps to a registered action; strict dependencies for
   calculations; after_settled dependencies for progress packaging. Then it stops.
2. JCO approves the plan and any preliminary assumptions; approvals go in the continuation file, never in lessons.

### 2. Queue worker (DSO-C27)
1. Hold one OS-level worker lock. A task ID added to the plan needs no restart; a new action type needs the catalog
   entry (not a code change). A code change needs a controlled restart (RESTART_REQUESTED marker).
2. Run ready tasks; retry only adapters marked resume_safe, with a finite attempt limit; preserve failed attempts;
   continue independent tasks.
3. When a task is replaced, explicitly cancel or re-point dependents of the failed ID; refresh dependencies of every
   existing pending task on each plan load.
4. Store stderr tail and exit reason with every failed task in the supervisor inbox; never record error null.
5. Before claiming work is delegated, confirm a fresh RUNNING heartbeat, a child PID and an advancing task log.
6. When ready work is exhausted, write the deduplicated supervisor inbox and stop; waiting is not progress.

### 3. Supervisor loop (DSO-C26)
1. Build the manifest from structured outputs; never draft from the append-only checkpoint or history log.
2. Read JSON evidence as parsed objects or targeted keys, never fixed 50-line text windows.
3. Before each local model request, the gateway injects up to 3 verified lessons matching the task.
4. Loop guard: fingerprint repeated work on action plus target file (ignore offsets and windows); after 2 repeats
   force a different action or end the branch.
5. Native retries: at most 2 identical attempts and at most 2 materially different recoveries; then log and move to an
   independent branch.
6. Local agents make reversible choices and use owner-authorized preliminary assumptions; log each in
   `decision_log.csv`.
7. Honor STOP_REQUESTED at every step.

### 4. Completion gate and end state
1. "Completed" only when every required native artifact exists, is fresh, passes its numeric checks and has
   provenance (PC-Hydro printouts, HMS/RAS/HY-8 outputs per the gate list). Filled report sections never count.
2. A draft with unresolved modeling is partial, and the alert says so. Distinct end states: completed, partial,
   blocked, failed.
3. On exit (finally block): write the terminal heartbeat; reconcile state, queue and actual process existence before
   notifying.

### 5. Notification
1. Server and topic in a private config outside prompts and logs; test once per setup.
2. Persist send intent before posting; distinguish server-accepted from owner-confirmed receipt; investigate
   delivery_unknown before resending; clear intent and receipt per run ID.
3. Message: end state, what is missing, workstation paths of the morning package and logs.

### 6. Morning review package and exception packet
1. Build the morning package with after_settled dependencies (builds even when evidence tasks failed): candidate
   geography, sourced evidence, assumptions, failed or missing calculations, links to native files. Check every link,
   image and table row headlessly; render one preview image. Refresh only when evidence changes, batched.
2. Batch unresolved questions into one `review_packet.md`: completed milestones, decisions to review, failed attempts
   with evidence paths, grouped questions. Omit routine status and unchanged files.
3. At most one cloud check per day; never a 15- or 30-minute cloud heartbeat. A progress update must not end the
   cloud work turn while work is pending.
4. Cloud answers come back as structured decisions plus draft lessons. A lesson is marked verified only after the
   local worker replays it through its own tools; otherwise it stays draft or blocked. Lessons hold procedures, never
   project facts, owner assumptions or approvals.

## Gotchas
- A continuation run ended after 8 steps (about 20 s) as draft-ready with unresolved modeling after re-reading the
  same summary.json 3 times in 50-line windows; no hydraulic work was attempted (EKOS-LOCAL-001).
- Sections drafted from the checkpoint log repeated superseded statements and misread a task label as a project name
  (EKOS-LOCAL-001).
- One section failed on an unterminated JSON string after 2 bounded attempts and was left Unresolved; that is correct
  behavior, keep it (EKOS-LOCAL-001).
- Heartbeat stayed LOCAL_REASONING after the run terminated (EKOS-LOCAL-001).
- Exact-match loop detection is evaded by small argument changes (start or line offsets) (EKOS-LOCAL-001).
- Fourteen filled report headings looked complete while all RAS 1D/2D, HY-8 and 100-yr routing were missing; three
  autonomous pilots ended without hydraulic progress (EKOS-LOCAL-001).
- The alert said draft ready while hydraulics were missing (EKOS-LOCAL-020, EKOS-LOCAL-001).
- A leftover intent or receipt can suppress the next alert (EKOS-LOCAL-020).
- Paths sent to a phone do not give remote file access; deliver review copies to the delivery folder (EKOS-LOCAL-020).
- Queue policy only added new IDs and never refreshed dependencies of existing pending tasks; 3 obsolete tasks stayed
  pending forever on failed predecessors (EKOS-LOCAL-002).
- 22 of 140 tasks ended NEEDS_REVIEW and the inbox recorded every one as error null with exit code 1, so each was
  re-investigated from logs (EKOS-LOCAL-002).
- A worker in WAITING_FOR_SUPERVISOR showed 0 GPU use while the owner expected work (EKOS-LOCAL-002).
- Registering a new action in worker code required a controlled restart; the approved-actions catalog avoids that
  (EKOS-LOCAL-002).
- The GIS environment lacked jsonschema; environment checks belong to setup (EKOS-LOCAL-002).
- 15-30 min heartbeats, incremental connector development, repeated image reviews and 24 package refreshes used about
  50 pct of the weekly cloud quota in about 1.5 days; the owner judged it more than doing the job directly
  (EKOS-LOCAL-003).
- The cloud agent kept ending its turn with a final response, so nothing ran between owner prompts (EKOS-LOCAL-003).
- The cloud started doing calculations itself; owner correction: the local AI does the calcs, the cloud only plans,
  teaches and reviews (EKOS-LOCAL-003).
- The cloud fetched source data itself; owner correction: teach the local worker the retrieval procedure so it can
  repeat it (EKOS-LOCAL-003).
- About 20 scheduled cloud heartbeats ran overnight plus 4 owner corrections (EKOS-LOCAL-003).
- The morning package refreshed 24 times overnight; package existence was nearly reported as report completion
  (EKOS-LOCAL-017).
- A successfully proposed repair is not proof of local replay; 45 lessons were recorded in 1.5 days (EKOS-LOCAL-004).
- A local model invented a hydraulic standard and misbound a stage value; schema-valid output is not factual
  (EKOS-LOCAL-005).

## Stop conditions
- STOP_REQUESTED present: finish the current atomic step, write the terminal heartbeat, notify, stop.
- Loop guard or retry cap reached on a branch: end the branch, log, continue independent branches.
- Ready work exhausted: write the supervisor inbox and stop (do not idle-wait claiming progress).
- A step needs an approval that is not recorded: put it in the review packet; do not assume it.
- Second instance detected (lock held): exit without changes.

## Escalation (to JCO)
- The one daily review packet: decisions to review, failed attempts with evidence, grouped questions.
- Any owner assumption that becomes a design basis; any approval request (PC-Hydro terms, D17, are recorded once
  per project).
- Changes to model roles (D15), execution split (D13) or retrieval rule (D14).
- End states partial, blocked or failed, with what is missing.

## Learning log
End every run with `log_lesson(project='<job no>', text='<procedure, applicability, validation evidence, limits; replayed: yes/no>',
evidence=['<task log or replay output>'], source_ai='local:<model>')`, or on EKOS:
`D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py log-lesson --project <job no> --source-ai local:<model> --text "..." --evidence "<path>"`.
Put error strings and software names in the lesson text so keyword retrieval finds it.

## Change log
- 1.0.0 2026-10-22: built from clusters DSO-C26, DSO-C27, DSO-C28 (with lesson rules from DSO-C29 and gateway rules
  from DSO-C30, RPT-C04 package rules); decisions D11-D15, D17, D56. Items marked "default, to confirm": D13
  (computes run natively by the agent), D15 (model role table).
