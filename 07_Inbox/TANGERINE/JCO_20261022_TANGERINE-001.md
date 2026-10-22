---
id: TANGERINE-001
title: Mock agency and public review of a concept drainage report before issue
type: agent
function: qc
trigger: A concept-level or rezoning drainage report is drafted and will face agency
  review and a skeptical public before formal submittal
steps:
- Give the agent the draft report PDF, the governing manuals list and the review roles
  (Town reviewer, county flood control reviewer, landowner agency reviewer, public
  or opposition reader)
- Run the same review prompt on two AI platforms independently (Comments A and Comments
  B) so findings can be cross-checked
- Require each comment to carry a unique source-prefixed ID, a report location (section,
  page, table or figure), what is missing and the expected revision
- 'Merge the two sets: collapse duplicates, keep the stricter wording, and log which
  source raised each item'
- Hand the merged list to the comment-response matrix step (TANGERINE-002) and sort
  into fix now vs carry to the master drainage report
gotchas:
- Both review sets independently flagged the same core items (uniform Manning n, non-common
  mesh comparison, unsized detention, crossing language, Preserve not on maps), which
  confirmed priority; use overlap as the priority signal
- 'ID collision: set A used A-1..A-3 for agency comments while set B used A-1..A-4
  for the landowner-agency reviewer; prefix IDs by source set before merging'
- Review prompts written from a public or opposition view produce politically framed
  text; keep it internal and never paste it into a deliverable
jurisdiction: Town of Marana; Pima County RFCD
tools_versions: ChatGPT, Claude, Gemini (same prompt on two platforms)
evidence:
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Comments\Internal\Comments
  A.docx
- C:\Users\Titan\OneDrive\AZ State Land Tangerine Corridor\Comments\Internal\Comments
  B.docx
hours_lost: 1.0
recurrence: 2
confidence: high
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:05+00:00'
schema_version: 1
---
