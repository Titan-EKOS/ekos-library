---
id: EKOS-LOCAL-023
title: Reference library intake - copy, hash, extract, selective OCR, human review
  queue
type: skill
function: data-gathering
trigger: Bringing a folder of legacy reference documents into the shared library
steps:
- Copy without altering source; compare SHA-256 before marking verified; keep original
  names and paths
- Inventory executables but never run them
- Extract PDFs with page provenance; OCR only zero-text or low-text PDFs into separate
  derived files
- Leave encrypted PDFs pending; do not bypass protection
- Diagnose timeouts individually before longer retries
- Put human decisions in a separate sheet; never approve numbers from OCR alone
gotchas:
- 715-file intake ran 5.3 h; 220 of 264 PDFs verified, 16 timeouts, 18 page-label
  failures, 8 zero-text
- A stdout warning on a successful extraction confused the orchestrator into marking
  failure
- OCR of map pages misread labels
- 'Recurrence note: 1 intake, 42 PDFs needing rework'
jurisdiction: Arizona (ADWR reference set)
tools_versions: Docling, OCRmyPDF (Ubuntu WSL), Tesseract 5.4.0
evidence:
- C:\Ekos\docs\ADWR_INTAKE_QA_POLICY.md
- C:\Ekos\docs\ADWR_OCR_GRAPH_REVIEW_HANDOFF.md
- C:\Ekos\logs\adwr-intake.stdout.log
hours_lost: 2.0
recurrence: 1
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:22+00:00'
schema_version: 1
---
