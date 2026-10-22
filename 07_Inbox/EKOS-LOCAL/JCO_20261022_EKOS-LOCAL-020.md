---
id: EKOS-LOCAL-020
title: Run-end phone notification with honest status (ntfy)
type: skill
function: other
trigger: Alerting the owner when an unattended local run ends
steps:
- Keep server and topic in a private config file outside prompts and logs
- Test once; distinguish server accepted from owner-confirmed receipt
- Persist send intent before posting; investigate delivery_unknown before resending
- Message states completed, partial, blocked or failed and gives file paths on the
  workstation
gotchas:
- A leftover intent or receipt can suppress the next alert; clear per run ID
- Paths sent to a phone do not give remote file access
- Alert said draft ready while hydraulics were missing
- 'Recurrence note: 2'
jurisdiction: General
tools_versions: ntfy Android, notifications.py
evidence:
- D:\LocalAI_Test\EKOS_Knowledge\topics\orchestration\KB-011.md
- D:\LocalAI_Test\Projects\EKOS-GUILLERMO\ENGR\DOCS\Drainage Report\DR-01_Guillermo-Golf-Links\00_Admin\PHONE_NOTIFICATION_STATUS.json
hours_lost: 1.0
recurrence: 2
confidence: high
project: EKOS-LOCAL
source_ai: claude
timestamp: '2026-10-22T23:35:21+00:00'
schema_version: 1
---
