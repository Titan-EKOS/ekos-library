---
id: SILVERBELL-012
title: Review package assembly with checksum verification
type: skill
function: compile-pdf
trigger: Delivering a multi-GB review folder of CAD, models, PDFs and renderings.
steps:
- Stage in the work folder, then copy to the delivery folder.
- Write START_HERE.md, a manifest and a sheet index; verify every SHA256 source vs
  delivery.
- Run PDF verification on plan compilation, hydraulic review and render PDFs before
  copying.
gotchas:
- Late additions (source model 00, re-rendered views) forced re-copies; finish content
  before the final copy.
- Copying while a RAS run is writing risks partial HDFs; copy finished results only.
jurisdiction: n/a
tools_versions: Python
evidence:
- C:\Ekos\projects\silverbell\v4\package_current_review.py
- C:\Ekos\projects\silverbell\v4\deliver_current_review.py
- C:\Ekos\projects\silverbell\Current_Review_Package_2026-09-13\Verification
hours_lost: 1.5
recurrence: 3
confidence: high
project: SILVERBELL
source_ai: claude
timestamp: '2026-10-22T23:32:26+00:00'
schema_version: 1
---
