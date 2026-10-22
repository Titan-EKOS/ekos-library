---
id: EKOS-LOCAL-013
title: Record plan and field-book retrieval with OCR provenance (City of Tucson Maps
  and Records)
type: skill
function: data-gathering
trigger: Locating as-built plans, crossing details and benchmark datum records for
  a drainage study
steps:
- Use the public catalog with description queries by words and plan queries by plan
  ID; offer the model only observed action links
- For field books, use a cookie session and CSRF token, follow next-page links with
  a page budget, shortlist matching filenames before model selection
- Save every download with SHA-256, check PDF/TIFF magic bytes, keep receipts
- Run Tesseract per page with orientation detection; make a rotated derivative, keep
  the original
- Read OCR files with explicit strict utf-8 on Windows
- Have the model pick source-offset excerpt IDs; quote text deterministically from
  the original; verify the page image before using any number
gotchas:
- First field-book search stopped at page 1 and called the target missing
- Sideways scans gave zero OCR hits on all 26 pages until orientation was corrected
- Default cp1252 decoding failed on utf-8 OCR text
- Free-form model quotes - only 40 of 137 matched the source exactly
- OCR misread 2698.20 as 2696.20 on one record; two monuments with the same elevation
  were different points
- Plan titles naming roads do not geolocate a structure; candidate crossing details
  stayed unaccepted until spatially anchored
- 'Recurrence note: 8 datum/crossing retrieval tasks, 5 failed or empty'
jurisdiction: City of Tucson / Pima County
tools_versions: Tesseract 5.4.0, Python requests, Qwen3.5-9B
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-007.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-028.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-030.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-031.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-029.md
hours_lost: 3.0
recurrence: 5
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:19+00:00'
schema_version: 1
---
