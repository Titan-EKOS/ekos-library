---
id: STARVALLEY-019
title: Unattended FLO-2D run harness on Windows
type: skill
function: hydraulics-model-run
trigger: Running several FLO-2D models in parallel or overnight from scripts
steps:
- 'run_model.ps1: delete old *.OUT/*.TMP/*.CHK, set OMP_NUM_THREADS, start FLOPRO.exe
  minimized in the model folder, append PID and threads to a run log'
- Run a dialog watcher that clicks Close on the end-of-run summary dialog so the run
  finishes and TMP files clear
- Check for duplicate FLOPRO processes in the same folder and kill strays before restarting
- Archive each version of outputs to a scratch folder (v3, v4, v5...) before rebuilding
- Declare success only on exit code 0, native termination, complete outputs and no
  TMP files; never infer completion from simulation time
gotchas:
- A stray script launched duplicate Interim runs in the same folder
- Windows AppHang closed two runs at sim hour 7.7; restarts with fewer threads were
  needed
- Runs left going at session end were not monitored; status must be re-read before
  results are used
jurisdiction: FEMA CLOMR (any FLO-2D model)
tools_versions: FLO-2D Pro Build 26.02.25, PowerShell 5.1
evidence:
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\run_model.ps1
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\09 QC\tools\dialog_watcher.ps1
- D:\Star Valley CLOMR\4th Submittal - New Case (Sep 2026)\01 Models\_run_log.txt
- D:\SV-BLIND-CLOMR\_WORK\00_Admin\JCO_20261011_Closeout_and_Resume.txt
hours_lost: 4.0
recurrence: 37
confidence: high
project: STARVALLEY
source_ai: claude
timestamp: '2026-10-22T23:33:14+00:00'
schema_version: 1
---
