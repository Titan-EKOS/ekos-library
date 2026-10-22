---
id: NORTHLOOP-001
title: Drainage study update intake - inventory, standards, deficiency review, one-page
  scope
type: skill
function: project-setup
trigger: An earlier preliminary drainage study must be updated to current jurisdiction
  standards for a development plan, and a short scope is needed for a larger proposal
steps:
- Inventory the whole project folder (path, size, mtime, readable yes/no) to CSV;
  inventory ZIP contents separately; keep the inventory and all generated work outside
  the source job folder
- If an upload is still running, save dated snapshots and a delta file; rerun the
  inventory when the upload is complete before final findings
- Identify the prior report, native model folders, current site plan/CAD, survey,
  geotech report and correspondence; record which layout the prior report actually
  adopted
- Download all current jurisdiction drainage and development standards into Review_<date>\Standards
  with a register (title, edition date, URL, current or historical)
- Write numbered findings (F01...) with severity, evidence locator (report page, model
  file) and action
- Write the scope as plain text, one page target and two pages max, no subtasks, with
  assumptions and exclusions; list conditional services (FEMA map revision, regional
  model rebuild, easement-driven redesign) separately instead of omitting them
gotchas:
- Upload grew from 1,726 to 2,653 files during the review; findings issued from the
  first snapshot had to be revised. Mark findings provisional until the inventory
  is final
- Correspondence did not show prior agency approval of the old report, which decides
  addendum vs full replacement report; check this early
- Prior report carried conflicting dates and tables (Q500 basis stated two ways);
  do not reuse tables without tracing to calcs
jurisdiction: Town of Marana
tools_versions: Python 3 (pypdf, PyMuPDF), ripgrep
evidence:
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Review.txt
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Drainage_Update_Scope.txt
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\inventory_delta.txt
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\archive_summary.json
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30, opening prompt)
hours_lost: 1.5
recurrence: 3
confidence: high
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:26+00:00'
schema_version: 1
---
