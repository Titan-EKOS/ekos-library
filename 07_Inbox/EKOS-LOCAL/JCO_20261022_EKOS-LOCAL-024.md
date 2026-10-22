---
id: EKOS-LOCAL-024
title: Install and validate engineering and simulation software on the workstation
type: skill
function: project-setup
trigger: Installing FLO-2D, CFD/DEM engines or GIS plugins on EKOS
steps:
- Check what is already installed first (engine vs QGIS plugin); back up QGIS settings
- For FLO-2D, the engine was present; install the FLO-2D QGIS plugin into the existing
  QGIS profile, set engine path, run a bundled example from the toolbar
- Validate each install by running a real example end to end, not just version output
- In WSL, source OpenFOAM bashrc from the profile; build LIGGGHTS STUBS before make
  serial
- Record account-bound or interactive steps as unresolved instead of claiming done
gotchas:
- FLO-2D installer complained QGIS was not part of the install; the real gap was the
  missing plugin
- Second FLO-2D run hit a file lock from an open test process; close finished runs
  before rerunning the same folder
- RTX 5090 needs CUDA 12.8 PyTorch builds; CUDA 12.4 kernels failed on SM 12.0
- 'Recurrence note: 2 install sessions'
jurisdiction: General
tools_versions: FLO-2D Pro Build 25 (26.02.25), FLO-2D plugin 2.2.0, QGIS 3.44.12,
  OpenFOAM, LIGGGHTS, DualSPHysics
evidence:
- C:\Flo2d\FLO-2D Ready to Run.txt
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Flo2d\2026-09-18_8f710667f879.txt
  (from Codex session 2026-09-18)
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\engineering_suite_windows_wsl_20260927.md
hours_lost: 2.0
recurrence: 2
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:23+00:00'
schema_version: 1
---
