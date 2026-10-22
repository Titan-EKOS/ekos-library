---
id: NORTHLOOP-002
title: Jurisdiction standards harvester agent (download, register, flag gaps)
type: agent
function: data-gathering
trigger: Start of any drainage report or update where the jurisdiction has released
  new standards since the last study
steps:
- Confirm jurisdiction from the city/town limits and jurisdiction GIS layers at the
  parcel; save the REST responses as evidence
- Crawl the agency drainage, engineering and development-plan pages; download every
  linked manual, checklist, standard detail set and code chapter
- 'Write Standards_Register.txt: document, edition, URL, local path, current or historical,
  key sections used'
- Extract text of each PDF for search; flag requirements that change the prior study
  (software build, event, freeboard, critical-facility criteria)
- List what could not be archived and how it was reviewed instead
gotchas:
- About 155 town PDFs downloaded, but bulk download of the online code was blocked;
  current code chapters had to be saved as web extracts and older code PDFs marked
  historical
- 'Runs as a separate context: long web crawl, independent of model work, about 1-2
  h'
jurisdiction: Town of Marana
tools_versions: Python 3 requests, pypdf
evidence:
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\Standards_Register.txt
- C:\Users\Titan\OneDrive\Northloop\Review_2026-09-30\download.py
- C:\Users\Titan\OneDrive\Northloop\Model_Update_2026-09-30\audit\jurisdiction_layer_3.json
- D:\EKOS\Library\00_Inventory\_local\codex_text\C_Users_Titan_OneDrive_Northloop\2026-09-30_c8a5a041bb76.txt
  (from Codex session 2026-09-30)
hours_lost: 1.0
recurrence: 1
confidence: medium
project: NORTHLOOP
source_ai: claude
timestamp: '2026-10-22T23:33:26+00:00'
schema_version: 1
---
