---
id: NORTHLOOP-008
title: FLO-2D engine build choice and legacy startup failure (War30.bac)
type: skill
function: hydraulics-model-run
trigger: A FLO-2D run fails at startup with access denied on War30.bac, or a jurisdiction
  names a specific engine build
steps:
- Test the engine on a copied vendor example under the normal user account using the
  Run for Project Folder package
- If only the archived build fails, do not change folder permissions or UAC; choose
  between a vendor repair of the legacy build or the installed build
- If the build changes, rerun all scenarios (existing, proposed, mitigation) on the
  same build; never compare a new-build result with old-build baselines
- Record engine SHA256, build number and vendor revision notes in the model basis;
  ask the agency to accept the build if it differs from the manual
gotchas:
- Build 17.08.17 reproduced the War30.bac error on a vendor example; build 26.02.25
  ran without admin prompts. The admin prompt could only be approved at the desktop,
  not from a phone
- The Town manual names 17.08.17, so moving to 26.02.25 is an open agency-acceptance
  item
jurisdiction: Town of Marana
tools_versions: FLO-2D Pro 17.08.17, 26.02.25
evidence:
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\startup_investigation_20261019\JCO_2026-10-19_FLO2D_Startup_Findings.txt
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\startup_investigation_20261019\test_results.json
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30, Oct 19 turns)
hours_lost: 2.5
recurrence: 1
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:28+00:00'
schema_version: 1
---
