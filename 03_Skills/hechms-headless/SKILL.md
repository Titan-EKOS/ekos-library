---
name: "hechms-headless"
description: "Build, compute, rerun and read HEC-HMS 4.13 models without the GUI (text-file project build from a parameter table, Jython compute via HEC-HMS.cmd -s, results and DSS extraction, reproduction of archived HMS work, depression bracketing, CN calibration); use whenever a drainage job needs HMS results for watersheds over 1 sq mi, many storms or variants, detention routing of external inflow hydrographs, or a check of archived HMS output before reuse."
version: "1.0.0"
status: "active"
function: "hydrology"
jurisdiction: "all (add-ons: pima-county-rfcd, caltrans-california)"
tools_versions: "HEC-HMS 4.13 (bundled Jython); hecdss / pydsstools for DSS; WhiteboxTools for depressions"
owner: "JCO"
replaces: "HEC-HMS bullet in drainage-report-build v1 Sec. 3 (4.12, Specified Average met model)"
---
# HEC-HMS Headless Runs (4.13)

## When to use
- Watershed systems over 1 sq mi where the governing method is HEC-HMS (Pima County TECH-018; Caltrans HDM 819.2 above
  about 320 ac), or any study needing many storms, durations or areal-reduction variants.
- Detention / reservoir routing of external inflow hydrographs (PC-Hydro DSS) without hand building in the GUI.
- Reproducing archived HMS results before a report update reuses them.
- Closed depressions that must be bracketed contributing vs non-contributing.
- Not for subbasins under 1 sq mi in Pima County (pchydro-hydrographs), and not for 2D rain-on-grid (hecras-2d-models,
  flo2d-model-runs).

Long or queued runs go through the model-run-supervisor agent (status file, rerun-all gate). Report text that quotes HMS
results follows drainage-report-build (values trace to native output).

## Inputs
- Parameter table (CSV) per subbasin: id, area (sq mi), loss parameters (CN, initial abstraction or % impervious), transform
  (lag in min, or Tc and R), downstream element; reach routing table; reservoir stage-storage-outflow tables.
- Rainfall: governing source and statistic from the jurisdiction add-on of drainage-report-build (for example Atlas 14
  upper 90% at the system centroid in Pima County); storm durations; areal reduction factors where required.
- External inflow hydrographs (DSS, INST-VAL, CFS, 1Minute) when routing gage flow.
- For reproduction work: the archived project, its results and the report tables to compare against.
- Governing version: HEC-HMS 4.13 (D01). Interpreter for helper scripts: `%HYDRO_PY%` = `C:\EKOS\hydrology\.venv\Scripts\python.exe` (D11).

## Steps

### A. Set up the working copy
1. Work in `20_Working\HMS\<model>_413\` (D56 job layout). Close HMS before copying any project (file locks, WinError 32).
   Archive old `results\` and `.log` files into `_archive_YYYYMMDD\` before the first compute.
2. Opening a 4.12 project in 4.13 upgrades it one way. Never open the record copy; open only the working copy and keep
   the original in `10_Record` untouched (D01).
3. Record in the run log: HMS build string, project path, date, and that the version is 4.13. The same version is stated
   in the report text and appears on the native printouts (D01).

### B. Build the project from text files
4. Start from the minimal template project in `reference/hms_file_patterns.md` (blocks copied from files saved by HMS 4.13).
   Do not learn file syntax from scattered sample projects; if a block is missing, save it once from the HMS GUI on EKOS
   and add it to the reference.
5. Write `.hms`, `.basin`, `.met`, `.gage`, `.control`, `.run` (and `.pdata` for paired data) from the parameter table.
   Add basins or runs by appending blocks. Write paired data (storage-outflow, rating) with hecdss.
6. Subbasin delineation for TECH-018 style models: outlets just above junctions where both branches exceed the threshold
   area; check the DEM-derived total area against any published (FIS) area before use.
7. External inflow (gage-flow routing), the default pattern (D01):
   - Source element with method GAGE_FLOW pointing to a Flow gage on the external DSS.
   - A zero meteorology component named `No Precipitation` with evapotranspiration `No Evapotranspiration`. Do not name it
     `None` (Undefined controller errors).
   - Alternate pattern (document when used): Specified Average met model with Use Basin Model lines.
8. DSS inputs: canonical interval names (`1Minute`, `1Hour`), data type INST-VAL, units CFS. Write, close, reopen and
   compare every ordinate before running (pchydro-hydrographs `build_dss.py` writes these records).
9. Reservoirs:
   - Translate every elevation and every stage-storage x value by one documented basin-bottom offset (relative datum);
     keep the absolute source values in the parameter table.
   - Circular outlets with Diameter, Chart, Scale, End Conduit; overflow with coefficient, top length, top elevation,
     taken from native examples.
   - Controlled Outflow (culvert outlet) or Modified Puls storage-outflow as the design requires.
   - Check the implied area of the stage-storage curve (dS/dz) against the basin footprint; flag jumps from
     connected-component masks (a flooded saddle). Use the dominant connected minimum of the DEM only as a floor candidate.
10. Check that every input path named in the project exists before starting the chain.

### C. Compute headless
11. Write the Jython script and launcher:
    ```
    "%HYDRO_PY%" scripts\make_hms_run_script.py ^
        --project-file "<job>\20_Working\HMS\<model>_413\<model>.hms" ^
        --runs-file runs.txt --out-dir "<job>\20_Working\HMS\_run" ^
        --hms-dir "C:\Program Files\HEC\HEC-HMS\4.13"
    ```
    The script opens the project, computes each run inside its own try/except (per-case failures kept), writes a status
    file and shuts the engine down. `--api legacy` writes the older OpenProject / Compute / Exit form.
12. Delete the previous results CSV for the runs being computed. Run `run_compute.cmd`; it calls `HEC-HMS.cmd -s` from the
    HMS install folder, logs console output and writes a `.done` file for the next chained step.
13. Run each scenario that changes geometry or reservoirs in an isolated project copy; keep failures per case.
14. Chain build, compute and read in one launcher when the job has many runs; the `.done` file is the hand-off.

### D. Judge the run and read results
15. Judge success by files, never by console text:
    ```
    "%HYDRO_PY%" scripts\check_hms_results.py --project-dir <model dir> ^
        --runs-file runs.txt --status <out>\compute_status.txt --input-dss <inflows.dss> ^
        --min-elements <n> --out <out>\check
    ```
    It checks results file present, newer than every input (stale test), element count, ERROR lines in the run log,
    unit hydrograph volume notes = 1.0000, and the status file. Exit code 1 means at least one run failed.
16. Read peaks, volumes and hydrographs only for the paths needed (HecDss in the same Jython session, or hecdss Python).
    Lower the DSS message level or redirect output; large variant sets make very large DSS files.
17. Continuity: compute from DSS storage endpoints for reservoir runs; report it with the run.
18. Critical storm: per the jurisdiction add-on (Pima County: max of 3-hr and 24-hr).
19. Native output for the report appendix: print the HMS summary and results tables from the program. If values had to be
    extracted from XML or DSS, title that PDF "extracted summary" and keep the program files in the record (D38).

### E. Failure handling
20. Native error 40253 (stage above storage curve): stop. Do not extrapolate the storage table, add street areas to storage
    or tune weir width to force a pass. Re-running sensitivities without new geometry does not change the result; report
    the failure and ask for geometry.
21. A run that never executed in an archived project (for example ERROR 23430, missing basin depths) is reported as
    missing. Do not fill it.
22. A Source element with ZERO_FLOW and no downstream link throws ClassCastException at every step; remove it in a
    documented copy and say so in the log.

### F. Reproducing archived HMS work
23. Copy the archived project to a native working folder (Step A), compute, then compare every element peak and volume to
    the archived values; list items not recomputed and why.
24. Check that RAS or FLO-2D inflow hydrographs match the HMS DSS series they claim to come from.
25. Any departure from the governing HMS version or archived setup is a JCO decision item in the QC open-items document.

### G. Closed depressions (bracketing)
26. Fill depressions on the DEM (WhiteboxTools); keep those over the volume threshold (20 af used); compute volume, area,
    catchment; state the terrain vintage used.
27. Run HMS twice: depressions filled (contributing) and catchments removed (non-contributing); compare peaks at the key
    CPs. Run the same non-contributing variant in the PC-Hydro routing model. For FLO-2D, a filled-terrain variant only
    after checking cells at the fill edges (flo2d-model-runs).
28. Non-contributing treatment is a methodology-meeting item; record the agency position in writing.

### H. CN models without calibration data
29. On HSG C/D foothill basins (or any CN model with no local check), compare uncalibrated Q100 with an independent
    estimate (FIS, regression) before use; follow `addons/caltrans-california.md` for the calibration sweep.

## Jurisdiction add-ons
| Add-on | Load when |
|---|---|
| `addons/pima-county-rfcd.md` | Pima County, City of Tucson, Marana or Sahuarita work over 1 sq mi (TECH-018 parameters) |
| `addons/caltrans-california.md` | California / Caltrans R/W; CN calibration to FIS and regression |
Load with `get_skill("hechms-headless", resource="addons/<file>.md")`. Jurisdiction criteria for the report itself are in
the drainage-report-build add-ons.

## Gotchas
- Opening a 4.12 project in 4.13 upgrades it; work on copies (CAMPBELL-012, claude session).
- 4.12 was the old standard but was not installed; 4.13 was used and logged as a decision item; 4.13 is now the standard
  per D01 (RKN-006, claude session).
- A Source element with ZERO_FLOW and no downstream link caused ClassCastException at every step; remove it in a documented
  copy (CAMPBELL-012, claude session).
- A 24-hr run never executed in the original (missing basin depths, ERROR 23430); report as missing, do not fill
  (CAMPBELL-012, claude session).
- Every -s run prints an XML/JAXB "Premature end of file" exception; harmless; confirm results exist rather than trusting
  the console (RKN-006, SAH-008; claude session).
- hecdss prints every zread to stdout (log reached 1.7 MB); redirect or lower the DSS message level (SAH-008, claude session).
- 50 runs (5 RP x 2 durations x 5 areal-reduction variants) gave a 492 MB DSS with 152,759 records; read only needed paths
  (SAH-008, claude session).
- First chain failed on a hard-coded input path that did not exist (hand-drawn berm file); check inputs before the chain
  (SAH-008, claude session).
- Copying an HMS project while HMS had it open failed with WinError 32 (SAH-008, claude session).
- File syntax was learned from a folder of 145 sample files; ship a minimal template in the library instead
  (CALFIRE-008, claude session).
- Check each run log for unit hydrograph volume 1.0000 in notes and errors (CALFIRE-008, claude session).
- Absolute elevation 2687.90658 was saved as 2687.9, below the storage table minimum, causing an initial-pool error;
  relative datum fixed it (EKOS-LOCAL-009, claude session).
- Generic meteorology name None produced Undefined controller errors (EKOS-LOCAL-009, claude session).
- All 100-yr cases failed with native error 40253; do not extrapolate the table, enlarge storage with street areas or tune
  weir width to force a pass (EKOS-LOCAL-009, claude session).
- Connected-component stage-storage jumped where a saddle flooded (implied 3,181 m2 vs 846 m2 footprint)
  (EKOS-LOCAL-009, claude session).
- Lowest DEM cell was an isolated 4-cell depression; use the dominant connected minimum as a floor candidate only
  (EKOS-LOCAL-009, claude session).
- Repeating inlet-location sensitivity did not change the 4 failures; stop re-running without new geometry
  (EKOS-LOCAL-009, claude session).
- Recurrence: 3 native HMS runs, 4 of 6 cases failed each time; 3 failed setup tasks (EKOS-LOCAL-009, claude session).
- Mine areas changed 30 to 80 ft between 2015 and 2021 terrain; terrain vintage controls depression volumes
  (SAH-016, claude session).
- Non-contributing treatment of pits and impoundments was based on public disclosures and permits; needs agency agreement
  at the methodology meeting (SAH-016, claude session).
- Uncalibrated HMS Q100 was about 1.9x FIS on a 9 sq mi creek and 2.5x regression on a 0.79 sq mi tributary
  (CALFIRE-007, claude session).

## QC checks
- Pull `get_qc_rules('hydrology')` and `get_qc_rules('model-runs')`; add the jurisdiction tag (`pima-rfcd`, `caltrans`).
- HMS version recorded in the run log, report text and printouts; any departure from 4.13 is a JCO decision item.
- `check_hms_results.py` passes for every run reported: results present, newer than inputs, element count as built, no
  ERROR lines, unit hydrograph volume 1.0000.
- DSS input round-trip verified ordinate by ordinate before compute.
- Reservoir runs: stage-storage implied area checked against footprint; continuity reported; no extrapolated tables.
- Reproduction: element-by-element peak and volume comparison table, with items not recomputed listed.
- Depression bracketing: both runs reported with terrain vintage.
- Native-output appendix pages are HMS printouts or titled "extracted summary" (D38).

## Change log
- 1.0.0 2026-10-22: built from clusters HYD-C19, HJR-C05, HJR-C06, HJR-C18; decisions D01 (4.13 standard, upgraded
  copies, version stated, No Precipitation zero-met default, Specified Average as alternate), D11, D38, D56. Scripts
  make_hms_run_script.py and check_hms_results.py added (run on synthetic data; results-XML statistic parsing to be
  confirmed against one GUI-opened run on EKOS, to confirm). Template blocks in reference/hms_file_patterns.md to be
  replaced by files saved by HMS 4.13 on EKOS (to confirm).
