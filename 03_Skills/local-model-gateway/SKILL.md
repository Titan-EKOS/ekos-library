---
name: local-model-gateway
description: Use whenever an agent or script on the EKOS workstation sends work to a local model (LM Studio / Ollama), runs Python, GIS or install commands there, records or retrieves a knowledge lesson for local workers, or installs and validates engineering software; covers model roles, context budget, structured output, environment rules, lesson lifecycle and install validation.
version: 1.0.0
status: active
function: other
jurisdiction: all
tools_versions: "LM Studio 0.4.21 (native API); Laguna S 2.1; Mistral Small 3.2 24B Q4_K_M; Qwen3.5-4B/9B Q4_K_M; Python 3.12 uv environments; QGIS 3.44 LTR; Qdrant 1.15.3; Windows 11 Pro"
owner: JCO
replaces: "none (new; folds in proposed ekos-environment-rules, knowledge-lesson-lifecycle and software-install-validation)"
---
# Local Model Gateway and EKOS Environment Rules

## When to use
- Any request to a local model on EKOS: evidence selection, OCR reading, extraction, cited criteria answers, narrative drafting, routing.
- Any agent running Python, GIS, model or install commands on EKOS (load this skill in every EKOS agent, including ekos-local-supervisor and model-run-supervisor).
- Before a local worker retries a known problem, and after any investigated failure (lesson lifecycle).
- New workstation, software upgrade, missing plugin/toolbar, or new GPU/CFD engine install (Section E).

## Inputs
- Task type (see role table), evidence rows or files with stable IDs, the output JSON schema.
- Loaded context length of the target model (LM Studio model info).
- Job number (for attempt logs and lessons).

## A. Model roles (D15)
| Role | Model | Use for | Never use for |
|---|---|---|---|
| Reasoning / planning | Laguna S 2.1 | task plans, decomposition, review of local results, exception packets | final numbers not taken from checked rows |
| Cited narrative and criteria answers | Mistral Small 3.2 24B | report narrative from checked rows, method/criteria answers with page citations (RAG generator) | inventing criteria, numbers not in the input rows |
| Extraction and recovery | Qwen3.5-9B | field extraction to schema, OCR excerpt selection, recovery after a failed attempt | narrative, criteria citations, supervisor drafting |
| First-pass crop reading | Qwen3.5-4B | reading cropped image regions, first-pass labels | numbers accepted without check |
| Dispatcher | 4B model | routing a request to a role | any number or engineering value |
| Excluded | Nemotron Nano 4B (numbers), Gemma 4 12B (cited answers) | - | see gotchas |

Role table is a default, to confirm (D15). Inference concurrency 2. (EKOS-LOCAL-005)

## B. Gateway procedure (every local call)
1. Route the call through the gateway module, never a direct chat; the gateway does the knowledge lookup and attempt logging. Standalone LM Studio or Ollama chats do not see the knowledge base. (EKOS-LOCAL-005, EKOS-LOCAL-004)
2. Look up verified lessons for the task (keywords: software, error string, task); inject at most 3 matching procedures. (EKOS-LOCAL-004)
3. Budget prompt plus expected output inside the loaded context (8k for 4B/9B). Pre-filter rows and shortlist links or files by script before inference; never send a full catalog. (EKOS-LOCAL-005, EKOS-LOCAL-013)
4. Call the LM Studio native API with reasoning off for small models and `response_format` = `json_schema` (strict). Do not use `json_object` (HTTP 400). Use the OpenAI-compatible endpoint only for short calls. (EKOS-LOCAL-005, EKOS-LOCAL-022)
5. The model selects only observed IDs (record IDs, OCR excerpt IDs, URLs, evidence labels). Reject any unknown ID; resolve quotes deterministically from the source text by ID, never from model output. (EKOS-LOCAL-005, EKOS-LOCAL-013, EKOS-LOCAL-022)
6. Write numeric wording from checked structured rows by code; never accept a number written by the model. (EKOS-LOCAL-005)
7. Validate output: schema, ID membership, citation labels map to chunk IDs, abstention allowed when the evidence does not answer. Schema-valid is not factual: a check against source rows is required before use. (EKOS-LOCAL-005, EKOS-LOCAL-022)
8. Log each attempt: job, role, model, prompt size, outcome, failure reason, stderr tail if any.
9. On failure, retry once with the extraction/recovery role and a smaller shortlist (2 bounded attempts total); then mark the item Unresolved and add it to the exception packet for the supervisor. (EKOS-LOCAL-001)

## C. EKOS environment rules
1. Python: use the locked uv environments (`uv run --project <env>` for interactive work); never bare pip or the global Python 3.14. (EKOS-LOCAL-021)
2. Long jobs and every .cmd launcher call the environment interpreter by full path, set as user variables `%GIS_PY%`, `%DOCS_PY%`, `%HYDRO_PY%`, `%HYDRAULICS_PY%`, `%ACQ_PY%`, `%LIBRARY_PY%` (table in `08_Platform_Builds/ENVIRONMENTS.md`), e.g. `"%GIS_PY%\" script.py`; never `python` from PATH. Skill dependency lines name the environment; pip install only for container-only skills. (D11, SAH-015)
3. GIS environment for rasterio/geopandas; documents environment for local-model schema validation (jsonschema); keep the two separate. (EKOS-LOCAL-021, EKOS-LOCAL-002)
4. Keep QGIS GDAL/PROJ off PATH; use the QGIS shell wrapper or the conda PDAL environment when those tools are needed. (EKOS-LOCAL-021)
5. PowerShell .ps1 execution is disabled; do not change the policy. Launch with Python or inline commands; setup scripts only may use `-ExecutionPolicy Bypass`. (D12, EKOS-LOCAL-021)
6. Open every text file with explicit `encoding="utf-8"` (Windows default is cp1252). (EKOS-LOCAL-021, EKOS-LOCAL-013)
7. Qdrant data in a Docker named volume, not a Windows bind mount. (EKOS-LOCAL-021)
8. Write validation scratch and temp files to workspace paths, not user TEMP. (EKOS-LOCAL-021)
9. Before a chain starts, check that every input path exists and that no input is locked by another program. (SAH-015)

## D. Lesson lifecycle (local knowledge base and library)
1. States: draft, blocked, verified, retired; keep them distinct. Retire a superseded lesson with a pointer to its replacement. (EKOS-LOCAL-004)
2. For a novel issue the supervisor investigates and solves it, then records topic, applicability, steps, validation evidence and limits. (EKOS-LOCAL-004)
3. A lesson becomes verified only after the local worker replays it through its own tools; a proposed repair is not proof. Otherwise record it as open or blocked. (EKOS-LOCAL-004, EKOS-LOCAL-003)
4. No project facts, owner assumptions or approvals in a lesson; a lesson never grants approval. (EKOS-LOCAL-004)
5. Title every lesson with the software name and the exact error string (retrieval is keyword matching). (EKOS-LOCAL-004)
6. Topic folders: local-models, gis-records, hydrology, hydraulics, orchestration. The sqlite store is authoritative; md/json files are mirrors. (EKOS-LOCAL-004)
7. Drop a lesson from automatic retrieval when its evidence files change or go missing. (EKOS-LOCAL-004)
8. Library sync: lessons that apply beyond EKOS go to the shared library with `log_lesson(project, text, evidence, source_ai)` (MCP server ekos-library) or `D:\EKOS\Library\09_Server\.venv\Scripts\python.exe D:\EKOS\Library\09_Server\library_cli.py log-lesson --project <job> --source-ai local:<model> --text "..." --evidence <path>`. Fields align with the library card: no client data, paths and lessons only; the data guard rejects anything else. Procedure-sized lessons go as cards (see project-harvest).

## E. Software install and validation (short form)
1. Check what is installed first (engine folder vs plugin; installed QGIS LTR version); back up QGIS settings. (EKOS-LOCAL-024, SAH-005)
2. If a compatible QGIS is present, skip the bundled QGIS; install the matching FLO-2D plugin (2.2.0 "Gila" for QGIS 3.44) into the existing profile plugins folder, enable it, set the engine path. (EKOS-LOCAL-024, SAH-005)
3. Run the license activator from its own folder; confirm activation by running a model. (SAH-005)
4. Validate every install with a real example end to end; FLO-2D: SUMMARY.OUT shows full simulation and volume conservation, ERROR.CHK has no fatal errors. (EKOS-LOCAL-024, SAH-005)
5. Close finished runs before rerunning in the same folder. (EKOS-LOCAL-024)
6. WSL: source the OpenFOAM bashrc from the profile; build LIGGGHTS STUBS before `make serial`. (EKOS-LOCAL-024)
7. GPU: RTX 5090 (SM 12.0) needs CUDA 12.8 PyTorch builds. (EKOS-LOCAL-024)
8. Save a short ready-to-run note and the plugin dependency check (h5py, netCDF4, engine path); record account-bound or interactive steps as unresolved, not done. (SAH-005, EKOS-LOCAL-024)

## Gotchas
- Sending 131 scan links into an 8k context caused HTTP 500; shortlist first. (EKOS-LOCAL-005)
- Long reviews through the OpenAI-compatible endpoint spent the output budget on reasoning; native API with reasoning off fixed it. (EKOS-LOCAL-005)
- LM Studio rejected `response_format` json_object with HTTP 400; use json_schema or text. (EKOS-LOCAL-005, EKOS-LOCAL-022)
- Gemma 4 12B passed only 5/10 cited answers (token budget spent in reasoning); Mistral Small 3.2 passed 10/10 on the same synthetic test. (EKOS-LOCAL-005)
- Nemotron Nano 4B rounded 11/12 ft too coarsely; do not use it for numbers. (EKOS-LOCAL-005)
- Local Qwen invented a hydraulic standard and misbound a stage value to the wrong area result; schema-valid output is not factual. (EKOS-LOCAL-005)
- Supervisor and report drafting had been on Qwen3.5-9B; given the failures above, narrative and cited answers move to Mistral Small 3.2 and planning to Laguna S 2.1 (D15). (EKOS-LOCAL-001, EKOS-LOCAL-005)
- A section failed on an unterminated JSON string from the local model after 2 bounded attempts and was left Unresolved; that is the correct end state, keep attempts bounded. (EKOS-LOCAL-001)
- Free-form model quotes: only 40 of 137 matched the source exactly; quote by excerpt ID from the original. (EKOS-LOCAL-013)
- Default cp1252 decoding failed on utf-8 OCR text. (EKOS-LOCAL-013)
- Only a synthetic 5-page RAG test passed; real manuals are not yet qualified for cited answers. (EKOS-LOCAL-022)
- Qdrant 1.15.3 accepted but did not return collection metadata; verify the fingerprint in point payloads. (EKOS-LOCAL-022)
- install-wsl-admin.ps1 failed: running scripts is disabled. (EKOS-LOCAL-021)
- Qdrant rejected the Windows bind mount for durability; moved to a named volume. (EKOS-LOCAL-021)
- Hugging Face cache cannot symlink without Developer Mode (extra disk use only). (EKOS-LOCAL-021)
- Sandbox validations could not write to user TEMP. (EKOS-LOCAL-021)
- GIS venv lacked jsonschema; keep GIS calculation and schema validation in separate qualified environments. (EKOS-LOCAL-002)
- After a session restart, python on PATH lacked numpy and h5py; jobs failed at import. (SAH-015)
- Retrieval is keyword matching; relevance can be poor without error strings and software names in titles. (EKOS-LOCAL-004)
- Standalone LM Studio and Ollama chats do not see the knowledge base; integration was still not done after 4 weekly reminders. (EKOS-LOCAL-004)
- 45 lessons were recorded in 1.5 days; without states and retirement the store fills with unverified repairs. (EKOS-LOCAL-004)
- FLO-2D installer said QGIS was not part of the install; the real gap was the missing plugin in the existing QGIS profile. (EKOS-LOCAL-024, SAH-005)
- Second FLO-2D test run hit a file lock from an open test process. (EKOS-LOCAL-024)
- CUDA 12.4 kernels failed on SM 12.0. (EKOS-LOCAL-024)
- The FLO-2D activator window closes by itself on success with no message; confirm by running a model. (SAH-005)

## QC checks
- Pull rules: `get_qc_rules('model-runs')`.
- Every local call logged with role and model; no model outside its role row.
- No number in any output that does not trace to a checked structured row; all IDs and citation labels observed in the input.
- Long-job launchers use a full interpreter path; no .ps1 dependency; utf-8 explicit.
- Lessons: state recorded; verified only with local replay evidence; no project facts or approvals.
- Installs: example run evidence filed (SUMMARY.OUT / ERROR.CHK or equivalent); unresolved steps listed.

## Change log
- 1.0.0 2026-10-22: built from clusters DSO-C30, DSO-C23, DSO-C29, DSO-C24 (with SAH-015 from DSO-C25); decisions D15 (role table, default, to confirm), D11, D12; conflicts 6, 7 and 10 resolved per those decisions. Retry-once rule (B9) and attempt-log fields (B8) are defaults, to confirm.
