---
name: project-harvest
description: Use at project closeout or after a major submittal to harvest one project's lessons into the EKOS Library as cards (skill, agent or qc_rule), submitted through the ekos-library server (add_card / log_lesson) or library_cli.py add-card, by whichever AI runs it.
version: 1.0.0
status: active
function: other
jurisdiction: all
tools_versions: "EKOS Library server schema_version 1; library_cli.py; Python with pypdf, python-docx, openpyxl, PyYAML"
owner: JCO
replaces: "Phase 2 harvest brief (one-off instructions), rewritten as a standing procedure"
---
# Project Harvest (closeout lessons to the EKOS Library)

## When to use
- At project closeout (final submittal accepted or job closed).
- After a major submittal (DR/TM issued, agency comment round answered, CLOMR/LOMR package uploaded).
- Not during routine work: single lessons found mid-task go in at once with `log_lesson`; this skill is the full pass.

Any AI may run it (Claude, ChatGPT, Codex, Gemini, a local model). Set `source_ai` to the AI actually running the harvest
(`claude`, `chatgpt`, `codex`, `gemini`, `local:<model>`). Set `project` to the job number.

## Inputs
- Job number and the project folder root(s) (Standard v0.3 tree, D56; older jobs may use the pre-v0.3 tree).
- Harvest scope: the whole job (closeout) or evidence dated since the last harvest (after a submittal). Find the last harvest date from the newest card timestamp in `D:\EKOS\Library\07_Inbox\<job>\` (read only).
- Access to the ekos-library MCP server, or a shell on EKOS for `library_cli.py`.
- Scratch folder: `D:\EKOS\Library\00_Inventory\_local\harvest\<job>\` (helper scripts, extracted text, `cards.yaml`). Nothing else is written.

## Rules (read before starting)
1. Harvest only this project's evidence. Do not read other jobs' folders, even when a file points to them.
2. Read-only on every project file. Do not open models, rasters, HDF or DSS contents beyond listing; keep command output short.
3. Never edit, rename or delete anything in `07_Inbox`. It is append-only and the pre-commit hook enforces it. To correct an accepted card, submit a new card (next id) with `corrects: <old id>` and the fix in its steps or gotchas.
4. Cards hold lessons and file paths only: no client documents, no client data, no copied paragraphs, no people's names, no emails, phone numbers, parcel numbers or street addresses. Use the job number in place of owner/client names; place and road names are fine. The data guard rejects violations and the card is not written.
5. Plain technical language, units abbreviated (cfs, fps, ac, sq mi, ft, in/hr). No AI wording in any step meant for a deliverable.
6. Prefer 8-25 strong cards per project over many weak ones; merge duplicates within the project before submitting.

## Skip list
Do not open: contracts, professional services agreements, scope and fee or fee proposals, invoices, Outlook .msg correspondence,
and anything in folders named INTERNAL, Opposition, Personal or StampAndSeal.

## Steps
1. **Set up.** Create the scratch folder. Confirm the server is reachable (`list_skills()`), or the CLI runs:
   `D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py list-skills`.
   Web AIs without EKOS access stay read-only: they write `cards.yaml` and hand it to JCO to submit with the CLI (step 9).
2. **Inventory.** List the project folders (names, dates, sizes; top levels only for model folders). Note dated work folders (`<Initials>_<YYYYMMDD>_*`, `Review_*`, `*_Update_*`), reruns and submittal dates. Apply the skip list.
3. **Read evidence in this order:**
   1. AI notes: AGENTS.md, CLAUDE.md, `*Continuation*.md`, `*Handoff*`, `*PROMPT*.md`, work plans, logs folders.
   2. Session transcripts already extracted to text (e.g. `D:\EKOS\Library\00_Inventory\_local\codex_text\<folder>\`), only those for this job.
   3. Markups and redlines: extract PDF annotations (`/Contents`, `/Subj`, `/T`, page) with
      `D:\EKOS\Library\09_Server\.venv\Scripts\python.exe <skill>\scripts\extract_redlines.py <pdf> <scratch>\redlines_<name>.csv`.
   4. Comment-response matrices and letters (xlsx, docx, md, csv): agency comments and what had to change.
   5. Scripts folders, run logs, dated work folders: what was repeated, rerun or fixed.
   6. Deliverables (report docx/pdf): skim structure only, to see what the work produced.
4. **Answer the five questions** in scratch notes, with evidence paths:
   1. Which tasks repeated or cost the most time, and how many hours? Estimate from file timestamps, dated folders, rerun counts, log durations and session start/end times; state the method.
   2. Which should be a skill (a procedure) and which an agent (separate context, long-running, or independent judgment)?
   3. What would each make easier or faster, and how?
   4. Which gotchas, failures and fixes were learned?
   5. What did JCO's redlines correct?
5. **JCO redlines become qc_rule cards.** One qc_rule card per distinct correction (merge repeats of the same correction and count them in `recurrence`). Evidence = file path + page + comment number/author, e.g. `<path>\Draft_DR.pdf p.14 comment 7 (JCO)`. The trigger states when the rule applies; steps state the check in testable terms. Agency comments that forced a change also become qc_rule cards (evidence: matrix path + comment number).
6. **Check the library first.** For each candidate, read the matching master (`get_skill`, `get_qc_rules('<tag>')`). Skip a lesson the master already states; card only what is new, different or contradicts the master (say so in a gotcha).
7. **Write cards** to `<scratch>\cards.yaml` as a YAML list using `templates/card_template.yaml`. Ids are `<job>-001`, `<job>-002`, ... continuing after the highest id already in `07_Inbox\<job>\`. Required fields: id, title, type, function, trigger, steps, evidence, confidence. Cards whose lesson came from a session transcript keep `source_ai` = the harvesting AI and say "from <tool> session <YYYY-MM-DD>" in the evidence.
8. **Self-check before submitting:** run the data-guard terms mentally against every field (names, emails, phones, addresses, parcel numbers, client names in text); replace client names in paths with the job number (the server also applies `path_aliases.csv`, but do not rely on it); each field under 4000 chars; no pasted paragraphs.
9. **Submit.**
   - MCP: call `add_card(card, source_ai, project)` once per card; `log_lesson(project, text, evidence, source_ai)` for short lessons that are not procedures.
   - CLI: `D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py add-card D:\EKOS\Library\00_Inventory\_local\harvest\<job>\cards.yaml --source-ai <ai> --project <job>`
   - Each accepted card is one new file in `07_Inbox\<job>\` and one git commit. The CLI stops at the first rejected card; cards before it are already accepted. Fix or drop the rejected card and resubmit only the cards not yet accepted.
   - Resubmitting an identical card (same id and content) is refused as a duplicate and nothing is written, so a rerun is safe; a changed card with an already-used id is written as a second file, so give real corrections a new id (Rule 3).
10. **Report back** (under 300 words): cards accepted by type, any rejected and why; top 5 cards by hours_lost x recurrence (id, title, hours, recurrence); total estimated hours lost and the method; evidence not readable; items for JCO to decide.
11. **End with a lesson** about the harvest itself if anything failed: `log_lesson(project, text, evidence, source_ai)`.

## Card fields
| Field | Content |
|---|---|
| id | `<job>-NNN`, sequential |
| title | short |
| type | skill, agent or qc_rule |
| function | data-gathering, hydrology, hydraulics-model-run, exhibits, report-assembly, compile-pdf, qc, jurisdiction-rules, project-setup, other |
| trigger | when the lesson applies |
| steps | list of concrete steps or checks |
| gotchas | list: what failed and the fix |
| jurisdiction | e.g. Pima County RFCD, City of Tucson, Placer County |
| tools_versions | e.g. HEC-RAS 6.6, PC-Hydro 7.4 |
| evidence | list: full file paths, path + page + comment, transcript path |
| hours_lost | number, estimate |
| recurrence | times it came up in this project |
| confidence | high, medium, low |

The server stamps project, source_ai, timestamp, schema_version and client name; do not add them to the card.

## Gotchas
- The data guard rejects a card for one street address or phone number anywhere, including inside an evidence path; the card is lost until resubmitted clean. (Phase 2 harvest brief)
- Client names in folder paths are swapped for job numbers only when listed in `path_aliases.csv`; write the job number yourself. (Phase 2 harvest brief)
- A changed card resubmitted under the same id is not a duplicate; it lands as a second inbox file. Use a new id with `corrects:`. (server behavior, add_card)
- Large model folders (100+ GB) make full listings slow and noisy; list top levels and use counts. (Phase 2 harvest brief)
- Many weak cards dilute clustering; merge within the project and aim for 8-25. (Phase 2 harvest brief)

## QC checks
- Pull rules: none required; the card itself is the output.
- Every qc_rule card from a redline has page + comment evidence; every card has at least one evidence path.
- No card restates a master unchanged; contradictions with a master are stated.
- All cards accepted or listed as rejected with reason; nothing written outside the scratch folder and `07_Inbox` (via server/CLI only).

## Change log
- 1.0.0 2026-10-22: built from the Phase 2 harvest brief (evidence order, five questions, card format, data rules, skip list) as a standing procedure; submission through add_card / log_lesson or library_cli.py add-card; source_ai = running AI, project = job number. Since-last-harvest scope, `corrects:` field and id continuation are defaults, to confirm.
