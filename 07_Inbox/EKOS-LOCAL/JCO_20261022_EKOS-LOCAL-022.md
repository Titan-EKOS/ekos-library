---
id: EKOS-LOCAL-022
title: Local RAG over reference manuals with page citations
type: skill
function: data-gathering
trigger: Answering method or criteria questions from local reference PDFs with a local
  model
steps:
- Extract each PDF to page-aware JSON (documents env); record PDF and artifact SHA-256
- Chunk by actual tokenizer length; freeze the embedding profile and fingerprint it
- Version the whole Qdrant collection by artifact hash plus chunking and embedding
  profile; write only to pilot_ or versioned collections
- Evaluate retrieval (hit@1, hit@5, MRR) before generation
- Generator cites short evidence labels mapped by code to chunk IDs; reject unknown
  labels; require abstention when unanswerable
- Keep edition, adoption and project applicability as separate registry fields; unknown
  stays unknown
gotchas:
- Qdrant 1.15.3 accepted but did not return collection metadata; verify fingerprint
  in point payloads instead
- LM Studio rejected json_object response format (HTTP 400)
- Only a synthetic 5-page test passed; real manuals not yet qualified
- 'Recurrence note: 3 failures fixed'
jurisdiction: General
tools_versions: Docling, MiniLM-L6-v2 embeddings, Qdrant 1.15.3, LM Studio Mistral
  Small 3.2
evidence:
- C:\Ekos\docs\RAG_PILOT_RECONCILED_DECISION.md
- C:\Ekos\docs\RAG_PILOT_END_TO_END_REPORT.md
- C:\Ekos\rag\ekos_rag\index.py
hours_lost: 2.0
recurrence: 3
confidence: medium
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:22+00:00'
schema_version: 1
---
