---
id: EKOS-LOCAL-007
title: PC-Hydro hydrograph must use 1-minute steps and an audited peak adjustment
type: qc_rule
function: hydrology
trigger: Any PC-Hydro hydrograph passed to HEC-HMS, HEC-RAS or a report table
steps:
- Confirm actual sample spacing in the export is 60 s, not only the UI setting
- Compare the sampled hydrograph maximum to the PC-Hydro reported peak; they will
  differ
- Make a separate peak-adjusted copy that replaces the maximum ordinate with the reported
  peak; keep the native export unchanged and log the added volume
- Report equation-based runoff volume, integrated hydrograph volume and adjustment
  volume separately; do not reject an export because they differ
- Close a nonzero tail with one extra minute to zero and log the added volume before
  DSS transfer
- Verify the adjusted series through DSS write and reopen (every ordinate, interval,
  units, volume)
gotchas:
- Owner correction during the run - not at 1-minute steps the peak never matches and
  has to be manually adjusted
- An invented 1 percent volume equality gate wrongly flagged the export as corrupt;
  the county manual defines the hydrograph integral as an approximation
- 'Recurrence note: 4 catchment scenario sets (benchmark, Basin B, road crossing,
  HMS inflows)'
jurisdiction: Pima County RFCD
tools_versions: PC-Hydro 7.4, HEC-HMS 4.13 DSS (bundled Jython)
evidence:
- D:\EKOS\Library\00_Inventory\_local\codex_text\D_LocalAI_Test\2026-09-21_d92e6073ab48.txt
  (from Codex session 2026-09-21, owner prompt U30)
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-012.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\KB-018.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\hydrology\ISSUE-PC-VOLUME.md
hours_lost: 2.0
recurrence: 4
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:13+00:00'
schema_version: 1
---
