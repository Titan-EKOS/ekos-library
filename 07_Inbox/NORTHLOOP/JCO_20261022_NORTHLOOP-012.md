---
id: NORTHLOOP-012
title: GIS exhibit legends use graphic samples, not text descriptions
type: qc_rule
function: exhibits
trigger: Any GIS or model exhibit with a legend
steps:
- 'Each legend entry shows the real mapped symbol: color, line weight and style, arrow,
  fill and hatch'
- Concise feature label beside each sample; include only symbols present on the sheet
- Apply to report figures and to viewer/dashboard legends too
gotchas:
- Legends describing symbology in words were rejected by the EOR and replaced
jurisdiction: any
tools_versions: QGIS / matplotlib
evidence:
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30, EOR correction)
- C:\Users\Titan\OneDrive\Northloop\40_QC\T3_EOR_Review\JCO_2026-09-30_Instruction_Comparison.txt
  (EOR update - GIS legends)
hours_lost: 1.0
recurrence: 1
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:29+00:00'
schema_version: 1
---
