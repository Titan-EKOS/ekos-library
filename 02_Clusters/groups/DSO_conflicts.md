# DSO conflicts

Real disagreements between cards, or between a card and an existing skill. Jurisdiction differences and project facts are excluded (see DSO.md add-ons and DSO_open_items.md).

1. 3DEP tile / lidar vintage selection rule (DSO-C04)
   - Side A: pick the newest 1 m project per tile (CALFIRE-004 step 2), while also filtering by project date to avoid mixed vintages (CALFIRE-004 gotcha).
   - Side B: select by named collection/year, not by newest publication date; newest-published logic picked an older 2018 collection published 2025 and forced a DEM rebuild (RKN-002).
   - Side C: composite keeps the older lidar as base and uses the newer lidar only where it is bare earth and the ground changed, logged in the assumption log (SAH-020).
   - Why it matters: different terrain surfaces change subbasin areas, Tc paths and depression storage; RKN-002 shows "newest" is ambiguous (publication vs acquisition). Library rule should be: choose by acquisition collection, document the choice, and difference vintages where both exist.

2. DEM output cell sizes (DSO-C04)
   - CALFIRE-004: site DEM 3 ft, basin DEM 30 ft.
   - RKN-002: 3 ft for hydraulics/grading, 10 ft for hydrology.
   - DLR-007: reproject 1 m to 3.28 ft to keep native resolution (implies not resampling to 3 ft).
   - SAH-018: PAG 2015 10 ft lidar as hydrology terrain.
   - Why it matters: hydrology parameters (slope, length) and RAS terrain detail depend on cell size; reruns across projects are not comparable without a stated default and a rule for when to coarsen.

3. Arizona Central State Plane realization (DSO-C04, DSO-C05)
   - RKN-002 and DLR-007: NAD83(HARN) AZ Central, intl ft (EPSG:2868); DLR-007 says Pima County GIS data is HARN.
   - STARVALLEY-014: NAD83 AZ Central intl ft, with files declaring EPSG:2223 (NAD83, not HARN).
   - Why it matters: HARN vs NAD83(1986) realizations differ by up to about 1 m; silent mixing shifts linework against terrain. The library needs one default per jurisdiction and a rule to record the realization in every data log.

4. HEC-HMS version (DSO-C14 vs existing skill)
   - drainage-report-build sec 3: HEC-HMS 4.12 headless.
   - CALFIRE-018 and SAH-018: HEC-HMS 4.13.
   - Why it matters: the headless command, template project and results can differ by build; the skill and rerun kit must pin the same version.

5. HEC-RAS version pinning (DSO-C14, DSO-C16)
   - CALFIRE-018, SAH-018: HEC-RAS 6.6 pinned in the rerun kit.
   - ELTORO-005: project carried 6.6 and 7.0 plans together; DLR-007 lists 6.x/7.x.
   - Existing skills: no HEC-RAS version stated.
   - Why it matters: 7.0 upgrades plan/geometry files one way; results fed to a report must cite one version. Library should pin a version and require a pre-upgrade copy.

6. Python interpreter / environment rule (DSO-C23, DSO-C25, existing skills)
   - EKOS-LOCAL-021: use locked uv environments (uv run --project <env>); never bare pip or global Python.
   - SAH-015: call Python312\python.exe by full path in every .cmd; streams were rewritten with Python 3.12 first on PATH. CALFIRE-018 scripts were tied to Python 3.12 site-packages.
   - hecras-result-rasters and pchydro-hydrographs "Dependencies": pip install --break-system-packages.
   - Why it matters: three different environment models; long jobs failed at import after restart (SAH-015). One rule needed: long-job .cmd files call the uv env interpreter by full path; skill dependency lines name the env, not a global pip install (container-only skills can keep pip).

7. PowerShell scripts for detached launch (DSO-C23 vs DSO-C25)
   - EKOS-LOCAL-021: .ps1 execution is disabled; do not change policy; run Python or inline commands.
   - SAH-015: long jobs started through launch_detached.ps1 (Win32_Process Create via CIM). SILVERBELL-009 and CAMPBELL-023 also used PowerShell.
   - Why it matters: the detached-launch procedure in the model-run-supervisor must work under the EKOS policy; implement it as an inline command or Python (e.g. CIM call via subprocess) rather than a .ps1 file.

8. Standard project folder structure (DSO-C14, DSO-C31, existing skills)
   - CALFIRE-018: folders 00-10 plus 99_Working.
   - RKN-019: package folders 01 Scopes .. 09 QC.
   - Existing skills: 40_QC\T3_EOR_Review and 10_Record.
   - SAH project used 30_Data, 50_GIS, 90_Report (SAH-018, SAH-020 evidence); NORTHLOOP-001 used Review_<date>\Standards.
   - Why it matters: agents and scripts locate inputs/outputs by folder; Standard v0.3 should define one folder map (working tree and delivery package) and the rerun kit should read it.

9. Date format in folder/file names (DSO-C31, existing skills)
   - Existing skills: <Initials>_<date>_<topic> (format not stated).
   - CALFIRE-018 evidence names: JO_20261006 (YYYYMMDD).
   - RKN-019 and CAMPBELL-023: JO_YYYY-MM-DD.
   - Why it matters: sorting and the File Steward naming check need one format; pick one and state it in the skill.

10. Which local model drafts narrative and cited answers (DSO-C26, DSO-C30, DSO-C09)
    - EKOS-LOCAL-001: supervisor and report drafting on Qwen3.5-9B; EKOS-LOCAL-013 uses Qwen3.5-9B for selection.
    - EKOS-LOCAL-005: Qwen invented a hydraulic standard and misbound a stage value; 9B role limited to recovery and extraction; Mistral Small 3.2 passed 10/10 cited answers. EKOS-LOCAL-022 uses Mistral Small 3.2 as the RAG generator.
    - Why it matters: narrative with criteria citations should go to the model that passed the cited-answer test; model roles need one table in the gateway skill.

11. Execution split: who runs model computes (DSO-C15 vs DSO-C14/C25/C28)
    - ELTORO-022: AI preps terrain, geometry and flow inputs and post-processes; the engineer runs the compute.
    - CALFIRE-018, SAH-018, SAH-015: the AI session launches HEC-RAS/FLO-2D/HMS runs itself; existing skills: run every model natively (by the agent).
    - EKOS-LOCAL-003: local AI does the calcs; cloud only plans, teaches and reviews.
    - Why it matters: the model-run-supervisor scope and the continuation file template depend on this; record the split per job, with a library default.

12. Cloud model doing data retrieval itself (DSO-C28 vs DSO-C01/C03)
    - EKOS-LOCAL-003: owner correction; cloud must not fetch source data or compute; it teaches the local worker the procedure.
    - CALFIRE-001, CALFIRE-003, CALFIRE-005, NORTHLOOP-002: the cloud session ran the due-diligence crawl and API harvest directly (and the planned due-diligence-researcher agent assumes this).
    - Why it matters: decide whether due-diligence-researcher runs on cloud or on the local worker for EKOS-LOCAL jobs; if local, C01/C03 procedures must be written as replayable scripts.
