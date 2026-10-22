---
id: EKOS-LOCAL-021
title: EKOS workstation environment rules for scripts and agents
type: skill
function: project-setup
trigger: Any agent running Python, GIS or install commands on the EKOS workstation
steps:
- Use the locked uv environments (uv run --project <env>); never bare pip or global
  Python 3.14
- Keep QGIS GDAL/PROJ off PATH; use the QGIS shell wrapper or conda PDAL env
- PowerShell .ps1 execution is disabled; run Python or inline commands, do not change
  policy
- Open text with explicit encoding utf-8 (Windows default is cp1252)
- Use the GIS venv for rasterio/geopandas and the documents venv for model schema
  validation
- Use a Docker named volume for Qdrant data, not a Windows bind mount
gotchas:
- install-wsl-admin.ps1 failed - running scripts is disabled
- Qdrant rejected the Windows bind mount for durability; moved to named volume
- Hugging Face cache cannot symlink without Developer Mode (extra disk only)
- Sandbox validations could not write to user TEMP; use workspace paths
- 'Recurrence note: 5'
jurisdiction: General
tools_versions: Windows 11 Pro, Python 3.12.10 uv envs, QGIS 3.44.12, Docker Desktop,
  WSL2 Ubuntu 24.04
evidence:
- C:\Ekos\EKOS_CURRENT_INVENTORY_2026-09-12.md
- C:\Ekos\EKOS_INSTALLATION_REPORT.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-020.md
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Ekos\2026-08-09_652d67e3fc81.txt
  (from Codex session 2026-08-09)
hours_lost: 3.0
recurrence: 5
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:22+00:00'
schema_version: 1
---
