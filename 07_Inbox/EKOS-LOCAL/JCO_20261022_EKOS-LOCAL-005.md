---
id: EKOS-LOCAL-005
title: Local model gateway - context budget, structured output and model roles
type: skill
function: other
trigger: Sending evidence, OCR or catalog data to a local LM Studio model for selection,
  reading or narrative
steps:
- Budget prompt plus output inside the loaded context (8k for 4B/9B); pre-filter rows
  or shortlist links before inference
- Use the LM Studio native API with reasoning off for small models, and a strict json_schema
  response format
- Let the model select only observed IDs (records, OCR excerpt IDs, URLs); reject
  unknown IDs and resolve quotes deterministically from source
- Generate numeric wording directly from checked structured rows; never accept numbers
  written by the model
- Use 4B for first-pass crop reading, 9B for recovery and extraction, a 4B dispatcher
  only for routing (not numbers); keep inference concurrency at 2
- Route every local call through the gateway so knowledge lookup and attempt logging
  happen
gotchas:
- Sending 131 scan links into an 8k context caused HTTP 500; shortlist first
- Long reviews through the OpenAI-compatible endpoint exhausted output budget on reasoning;
  native API reasoning off fixed it
- LM Studio rejected response_format json_object with HTTP 400; use json_schema or
  text
- Gemma 4 12B passed only 5/10 cited answers (token budget spent in reasoning); Mistral
  Small 3.2 passed 10/10 on the same synthetic test
- Nemotron Nano 4B rounded 11/12 ft too coarsely; do not use it for numbers
- Local Qwen invented a hydraulic standard and misbound a stage value to the wrong
  area result; schema-valid output is not factual
- 'Recurrence note: 6 distinct model failures'
jurisdiction: General
tools_versions: LM Studio 0.4.21, Qwen3.5-4B and 9B Q4_K_M, Nemotron 3 Nano 4B, Mistral
  Small 3.2 24B Q4_K_M
evidence:
- D:\LocalAI_Test\EKOS_Runtime\MODEL_SELECTION.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-004.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB040.md
- D:\LocalAI_Test\EKOS_Knowledge\topics\gis-records\KB-030.md
- C:\Ekos\docs\RAG_PILOT_END_TO_END_REPORT.md
hours_lost: 3.0
recurrence: 6
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:12+00:00'
schema_version: 1
---
