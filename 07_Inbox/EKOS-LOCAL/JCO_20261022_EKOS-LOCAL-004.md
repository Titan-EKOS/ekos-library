---
id: EKOS-LOCAL-004
title: Shared knowledge base lesson lifecycle for local models
type: skill
function: other
trigger: Before a local worker retries a known problem, and after any investigated
  failure
steps:
- Look up verified lessons through knowledge.py before each local model request (gateway
  injects up to 3 matching procedures)
- For a novel issue the supervisor investigates, solves, then records topic, applicability,
  steps, validation evidence and limits with knowledge.put
- Mark a lesson verified only after the local worker replays it through its own tools;
  otherwise record knowledge.issue as open or blocked
- Keep draft, blocked, retired and verified states distinct; retire superseded lessons
  with a pointer to the replacement
- Keep project facts, owner assumptions and approvals out of lessons; a lesson never
  grants approval
- Group lessons by topic folders (local-models, gis-records, hydrology, hydraulics,
  orchestration); sqlite is authoritative, md/json are mirrors
gotchas:
- Retrieval is keyword matching; relevance can be poor, include error strings and
  software names in lesson titles
- Standalone LM Studio and Ollama chats do not see the knowledge base; direct integration
  was still not done after 4 weekly reminders
- A successfully proposed repair is not proof of local replay
- Changed or missing evidence files must drop a lesson from automatic retrieval
- 'Recurrence note: 45 lessons recorded in 1.5 days; LM Studio/Ollama gap open 4 weeks'
jurisdiction: General
tools_versions: knowledge.py, knowledge.sqlite 2026-09-27, LM Studio 0.4.21
evidence:
- D:\LocalAI_Test\AGENTS.md
- D:\LocalAI_Test\EKOS_Knowledge\README.md
- D:\LocalAI_Test\EKOS_Knowledge\INDEX.md
- D:\LocalAI_Test\EKOS_Knowledge\CONNECTIONS_TODO.md
hours_lost: 2.0
recurrence: 4
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:12+00:00'
schema_version: 1
---
