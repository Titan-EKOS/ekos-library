---
id: TANGERINE-009
title: OneDrive project folders - confirm files are local and avoid duplicate copies
type: skill
function: project-setup
trigger: Starting AI or script work on a project folder that lives in OneDrive
steps:
- Check the folder holds real files (not only desktop.ini or cloud placeholders);
  set Always keep on this device or download first
- Copy to the work area with robocopy /S /E /MT:8 /R:1 /W:1 and log it; verify count
  and bytes, spot-check SHA-256
- Record in the project notes that the copy is complete so later runs do not start
  a second download
- After any bulk upload, check the folder for a nested copy of itself and for size
  growth before work starts
gotchas:
- The Tangerine folder showed only desktop.ini until a manual download; the run stalled
  about 1 hr
- The October upload created a full nested duplicate of the project folder inside
  itself (about 2,258 files, 50 GB), taking about 3 hr to sync
- OneDrive resets file timestamps to the sync time, so file dates cannot be used to
  estimate work history; keep a dated log
jurisdiction: any
tools_versions: OneDrive, robocopy
evidence:
- C:\Ekos\projects\tangerine\README.md
- C:\Ekos\projects\tangerine\qa\download_copy.log
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\AZ State Land Tangerine
  Corridor
hours_lost: 4.0
recurrence: 2
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:08+00:00'
schema_version: 1
---
