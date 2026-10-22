---
id: TANGERINE-002
title: Comment-response matrix with Incorporated / Partial / Deferred disposition
type: skill
function: report-assembly
trigger: Review comments (agency, internal or mock) must be answered alongside a revised
  report
steps:
- List every comment ID from every source file first; count them and keep the count
  in the memo header
- Disposition each as Incorporated (done in this revision), Partial (concept level
  now, balance to the next phase) or Deferred (needs new calcs, data or model runs)
- For each row give where it is addressed (section, table, figure) or the remaining
  action
- Add a summary-of-revisions list keyed to comment IDs and a remaining-items table
  grouped by workstream (hydrology, 2D documentation, common mesh, roughness, detention,
  sediment, crossings, environmental, floodplain, cost, exhibits)
- Before issue, diff the ID list in the matrix against the source ID list and search
  the memo for placeholders
gotchas:
- The matrix dispositioned A-, T1-, B- and P2- comments but omitted the Town (M-1..M-4),
  landowner-agency (A-1..A-4), county flood control (R-1..R-4) and public (N-1..N-5)
  items from the second review set; diff IDs before issue
- A placeholder reference (T1-?) was left in the remaining-items table; search for
  ?, TBD and XX before issue
- Memo date read June 2026 while later files are October; set the memo date at issue,
  not at generation
jurisdiction: Town of Marana; Pima County RFCD
tools_versions: python-docx generated memo, Word
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\ASLD_Tangerine_Comment_Response_Report.docx
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Comments\Internal\Comments
  B.docx
hours_lost: 1.5
recurrence: 1
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:05+00:00'
schema_version: 1
---
