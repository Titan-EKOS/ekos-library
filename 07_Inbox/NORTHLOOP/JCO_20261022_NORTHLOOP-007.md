---
id: NORTHLOOP-007
title: FLO-2D headless run supervisor agent (launch, monitor, validate, hand back)
type: agent
function: hydraulics-model-run
trigger: One or more native FLO-2D scenarios must run for hours in the background
  and feed results, GIS and report steps
steps:
- Prepare each run in its own folder with a manifest (status, engine build, input
  hashes); refuse to launch into a folder already run
- Run at most two solvers at once, 8 threads each on separate core sets; set the display
  option off for unattended runs
- 'Every few minutes read SUMMARY.OUT: simulated hour, finite values, volume error
  <= 0.1%; write a status JSON'
- Treat a run as complete only when the termination line is present, simulated hour
  >= end time and key outputs (DEPFP, MAXWSELEV, VELFP, FINALDEP, VELDIREC) are non-empty
- After completion, close the solver process if it stays open; never block on process
  exit
- On any stop, preserve the folder, log the reason and notify; do not report queued
  steps as done
- When all runs pass, run the comparison, outlet, GIS and report builders in order
gotchas:
- Build 26.02.25 run finished in about 2 hr but the solver kept running after termination;
  proc.wait(timeout=30) raised TimeoutExpired and the coordinator crashed, so scenario
  03 never launched. Poll and terminate instead of waiting
- An unattended collector run stopped at 33 of 50 hr with no restart file; the chat
  said the queue would finish on its own and the project sat 18 days before a status
  check found it. Status must come from files and processes, not from the plan
- Empty .OUT files during a run are not results; read SUMMARY.OUT and the status JSON
- Low CPU use (about 12% each on a 16-core CPU) is normal; FLO-2D does not use the
  GPU and more threads give diminishing returns. Benchmark threads later, do not restart
  live runs
jurisdiction: any
tools_versions: FLO-2D Pro 17.08.17 and 26.02.25; Python 3 psutil; Windows 11
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\scripts\run_installed_engine_study.py
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\installed_engine_pipeline_error.txt
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\corrected_study_pipeline_status.json
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\interrupted_collector_2026-10-01\SUMMARY.OUT
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\scripts\monitor_runs.py
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30, status turns Oct 2026)
hours_lost: 8.0
recurrence: 3
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:28+00:00'
schema_version: 1
---
