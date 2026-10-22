# HYD clusters - hydraulics model build and run (HEC-RAS 1D/2D, FLO-2D, HY-8, culverts, storm drain, SWMM/SSA, run supervision)

Source group: group_hydraulics-model-run.json (78 cards). 28 clusters. Score = sum(hours_lost x recurrence).
Scoring notes: HYD-C02 score is driven by STARVALLEY-019 (recurrence 37 run launches); HYD-C01 + HYD-C02 together (model-run-supervisor agent plus FLO-2D harness) score 293. QC-rule recurrence for BARNETT-011 and SAHPARK-012/013 counts individual review/redline comments. Conflicts: HYD_conflicts.md (HYD-CF-nn).
Gotcha tags: (card id, source). All cards source_ai = claude; 'via Codex session' where the evidence is a Codex session transcript.

### HYD-C01 Long-running model run supervision (HEC-RAS and FLO-2D queues, status, hand-back)
agent | agent model-run-supervisor (core); engine add-ons in HYD-C02 (FLO-2D) and HYD-C11/C10 (HEC-RAS launch) | score 142.0 | hours 20.5 | cards 5 | projects 4 (CAMPBELL, NORTHLOOP, SAH, SILVERBELL) | confidence mixed (SILVERBELL-018 medium; rest high)

Trigger: One or more native HEC-RAS 2D or FLO-2D runs must run for hours, overnight or in sequence on a shared workstation while other work continues.

Steps (merged):
1. Keep one job table / run register (project, plan or folder, engine build, start, end, run hours, status, input hashes); skip jobs already complete (RAS: HDF Compute Messages contain Finished Unsteady Flow Simulation; FLO-2D: SUMMARY.OUT has COMPUTER RUN TIME). Do not hand-write a new queue file for every re-plan.
2. Prepare each run in its own folder with a manifest / Running.json: exact command line, PID, process creation time, plan/geometry, controls, engine build, source hashes. Refuse to launch into a folder that has already been run.
3. Before each launch check that no other Ras/RasUnsteady/FLOPRO job is using the cores (exclude Ras -Embedding); wait on folder status or a lock file, not a hard-coded PID.
4. Assign cores explicitly: fixed affinity streams (start /affinity mask) with OMP_NUM_THREADS matched to the mask; FLO-2D at most two solvers at once at 8 threads each unless benchmarked otherwise; benchmark RAS cores once per model.
5. Poll only stdout, process state and closed summary files (SUMMARY.OUT, status JSON); never open a live pNN.tmp.hdf or an HDF being written. Before any action on a process verify name, command line and creation time (PIDs are reused).
6. Give every job a time limit; on a hang, failure or stop preserve the folder, log the reason, notify once, and move to the next job. Retry RAS plans up to 3 times, then log not complete.
7. Gate dependent runs: next run starts only after the previous passes duration, roughness and volume-error checks; geometry-dependent runs wait for a review marker written only after an actual geometry check.
8. Declare complete only from files: RAS - closed HDF with end time reached, Unsteady Finished Successfully, volume accounting, max residual, actual timestep controls; FLO-2D - termination line, simulated hour >= end time, key outputs non-empty, volume error <= 0.1%.
9. After completion run the prepared read-only comparison / results / GIS / report builders in order, write results JSON, notify the user once with values.
10. Keep one status file (progress hours, ETA, last check) the user can open; stay quiet while unchanged; heartbeat (15-30 min) skips when a healthy run is active and pauses after delivery or a user freeze.
11. Never duplicate or restart a healthy run; stop old queue sessions and obsolete diagnostic runs; do not run input generator scripts that rebuild all inputs while cases compute (use targeted edits).
12. Record each user authorization and hold in AGENTS.md; keep a checkpoint file that supersedes older status text.

Gotchas:
- Low CPU use during a headless run is normal (RAS about 8 pct seen; FLO-2D about 12 pct per solver on a 16-core CPU, no GPU use, diminishing returns from more threads); explain headless runs and core counts to the user up front, benchmark threads later, do not restart live runs (CAMPBELL-005, claude via Codex session; NORTHLOOP-007, claude via Codex session)
- About 100 half-hour heartbeats ran 2026-10-19 to 10-21 and the user still asked for status about 15 times; post progress hours and ETA in one status file the user can open (CAMPBELL-005, claude via Codex session)
- Worker scripts failed on the optional Max Courant dataset, absent under fixed stepping; recover results from the closed HDF instead of rerunning (CAMPBELL-005, claude via Codex session)
- Concurrent FLO-2D jobs by the user took all CPUs; run time is then not a benchmark (CAMPBELL-005, claude via Codex session)
- Do not duplicate or restart a healthy run; record each user authorization and hold in AGENTS.md (CAMPBELL-005, claude via Codex session)
- Build 26.02.25 run finished in about 2 hr but the solver kept running after termination; proc.wait(timeout=30) raised TimeoutExpired and the coordinator crashed, so scenario 03 never launched. Poll and terminate instead of waiting (NORTHLOOP-007, claude via Codex session)
- An unattended collector run stopped at 33 of 50 hr with no restart file; the chat said the queue would finish on its own and the project sat 18 days before a status check found it. Status must come from files and processes, not from the plan (NORTHLOOP-007, claude via Codex session)
- Empty .OUT files during a run are not results; read SUMMARY.OUT and the status JSON (NORTHLOOP-007, claude via Codex session)
- Thirteen queue/stream files were written in 20 h (flo_queue..queue4, streamA/A2/A3/B/C/C2/P6b/P7/P8) because each re-plan or crash needed a new hand-edited list. A queue that reads a job table and skips completed runs (SUMMARY.OUT has COMPUTER RUN TIME) would replace all of them (SAH-001, claude session)
- Waiting on a hard-coded PID breaks after any restart; wait on folder status or a lock file instead (SAH-001, claude session)
- A stream that hangs (see SAH-003) blocks every job after it; give each job a time limit (SAH-001, claude session)
- Other projects ran HEC-RAS on the same machine; the stream B wrapper polled Win32_Process command lines and only started after those jobs ended (SAH-001, claude session)
- First compute attempt through ras-commander compute_plan on 10-06 did not produce a result; the base 100-yr plan did not finish until 10:08 next day (SAH-009, claude session)
- ras_try.py (drop the SA/2D connection named in an error and retry) crashed because the plan HDF did not exist yet; check for the file before reading messages (SAH-009, claude session)
- ras_queue3 crashed on import (h5py missing) after the job restart used a different Python; see SAH-015 (SAH-009, claude session)
- Old queue sessions and obsolete diagnostic runs had to be stopped to avoid duplicate computes (SILVERBELL-018, claude session)
- Generator scripts that rebuild all inputs must not run while cases compute; use targeted edits (SILVERBELL-018, claude session)

QC checks:
- Run reported complete only with closed-file evidence (HYD-C01 step 8).
- Queued steps never reported as done; status in chat must match the status file.

Source cards: CAMPBELL-005, NORTHLOOP-007, SAH-001, SAH-009, SILVERBELL-018
Tool versions cited: CAMPBELL-005: HEC-RAS 6.6, Python, PowerShell | NORTHLOOP-007: FLO-2D Pro 17.08.17 and 26.02.25; Python 3 psutil; Windows 11 | SAH-001: FLO-2D Pro Build 26.02.25, Windows 11, Ryzen 9950X 32 threads | SAH-009: HEC-RAS 6.6, ras-commander 0.103.0, h5py | SILVERBELL-018: HEC-RAS, Python

### HYD-C02 FLO-2D Pro unattended run harness on Windows (dialogs, locks, stale output, duplicates)
skill | new skill flo2d-run-harness (used by agent model-run-supervisor) | score 151.0 | hours 5.0 | cards 2 | projects 2 (SAH, STARVALLEY) | confidence mixed (SAH-004 medium; rest high)

Trigger: Running FLOPRO.exe from scripts (not the QGIS plugin), in parallel or overnight.

Steps (merged):
1. Run FLOPRO.exe from the model folder using the Run for Project Folder install: cd /d <folder>; start "" /wait /affinity <MASK> FLOPRO.exe (or run_model.ps1 starting it minimized); set OMP_NUM_THREADS; append PID and thread count to the run log.
2. Before each run delete old *.OUT, *.TMP and *.CHK in the folder so a finished-check never reads old results; archive each prior output version to a scratch folder (v3, v4, v5 ...) before rebuilding.
3. Check for duplicate FLOPRO processes in the same folder and kill strays before (re)starting; confirm the previous FLOPRO process has exited (it keeps result files open) before starting another run in that folder.
4. Run a dialog watcher (UI Automation) that logs the text of any FLOPRO Warning window and the end-of-run summary dialog, then answers/closes it so the run finishes and TMP files clear; review the logged warning text after the run.
5. Set the display option off for unattended runs.
6. Declare success only on native termination (SUMMARY.OUT has COMPUTER RUN TIME), complete outputs and no TMP files; never infer completion from simulation time. See HYD-CF-05 on exit code vs solver that stays open.

Gotchas:
- FLOPRO keeps result files open after the simulation ends; a second run in the same folder was blocked until the old process was stopped (from Codex session 2026-09-18) (SAH-004, claude via Codex session)
- Warning dialogs stop an unattended run until answered; flo_dialog_watch.ps1 posts Enter and logs the message text for review (SAH-004, claude via Codex session)
- A stray script launched duplicate Interim runs in the same folder (STARVALLEY-019, claude session)
- Windows AppHang closed two runs at sim hour 7.7; restarts with fewer threads were needed (STARVALLEY-019, claude session)
- Runs left going at session end were not monitored; status must be re-read before results are used (STARVALLEY-019, claude session)

Source cards: SAH-004, STARVALLEY-019
Tool versions cited: SAH-004: FLO-2D Pro Build 26.02.25 | STARVALLEY-019: FLO-2D Pro Build 26.02.25, PowerShell 5.1

### HYD-C03 Model run preflight: inflow chronology, run duration, double-counted inflows, line endings and file integrity
qc_rule | QC rule (05_QC_Rules) - preflight gate run by agent model-run-supervisor before every launch | score 29.0 | hours 15.0 | cards 5 | projects 3 (CAMPBELL, NORTHLOOP, STARVALLEY) | confidence high

Trigger: Before launching any FLO-2D or HEC-RAS 2D production run, especially one that reuses inherited inputs, script-written inputs, or files copied through OneDrive or a time-limited shell.

Steps (merged):
1. Inflow chronology: parse every inflow node series; times strictly increasing and at the source calc interval (e.g. 0.5 hr, 0-50 hr); RAS hydrograph interval units match the source workbook (1MIN vs 1HOUR).
2. Inflow volume: integrate volume and peak per node and in total; compare with the source workbook before and after any scaling. If a series fails, repair timestamps from the source calcs only, keep every discharge value, log each change to CSV.
3. Double counts: check for inflows double counted where sub-basins lie inside a larger basin (see HYD-C12).
4. Duration: find when the last inflow hydrograph ends and when cell peaks occur; run a 24 hr reference and pick the shortest end time with < 0.01 ft later rise. For an archived model compare CONT.DAT simulation time with the last inflow time, compute inflow volume beyond the window, extend the run and note the change.
5. Line endings: write FLO-2D .DAT/.RGH with explicit CRLF and trailing CRLF; scan all text inputs for bare LF before every run (leave binary NEIGHBORS.DAT untouched); when patching, detect and preserve the existing style, write via temp file and rename.
6. File integrity after copy: compare byte size and hash of every file against the source; NEIGHBORS.DAT size equals the expected value for the grid; FLOPRO.exe size, build string and DLL count checked in every model folder.
7. Hash shared input files (CADPTS, CONT, TOLER, INFLOW, OUTFLOW) and require equal hashes across scenarios being compared.
8. Save face flow output in RAS plans (runs without it cannot give transect flows later).
9. Block launch unless preflight_pass is true; add the line-ending and hash checks to the package QC script so they fail the build.

Gotchas:
- 41 of 185 inherited hydrographs had repeated integer-hour times and a jump back from hr 9 to hr 1; two 8-hr native runs used them and were rejected after completion (NORTHLOOP-004, claude session)
- Volume error 0.0% in SUMMARY.OUT does not validate boundary chronology (NORTHLOOP-004, claude session)
- An input-volume comparison computed with the bad times (2.3% discrepancy) was invalid and had to be withdrawn (NORTHLOOP-004, claude session)
- Old model stopped at 24 hr while inflows ran to 50 hr, leaving about 18% of the inflow volume unsimulated (NORTHLOOP-005, claude via Codex session)
- 12 hr was too short; inflow lasted to 15.5 hr; 20 hr chosen (CAMPBELL-010, claude session)
- Double-counted B-1/B-2 inflows were found by the audit (CAMPBELL-010, claude session)
- LF-only CHAN/CHANBANK/CHAN.RGH/XSEC files gave error while creating channel segments and subscript out of range; content fixes (banks, dup cells, point counts) did not clear it until CRLF conversion (STARVALLEY-001, claude session)
- The same LF problem was present in the Build 23 converted existing-conditions model (TOPO, MANNINGS_N, FPLAIN, CONT, RAIN, HYSTRUC, INFLOW) (STARVALLEY-001, claude session)
- A copy cut off by a 45 s shell timeout left Interim NEIGHBORS.DAT at 733 KB instead of 5.9 MB; FLO-2D reported a misleading MANNINGS_N mismatched grid element / TOLER.DAT error (STARVALLEY-003, claude session)

Jurisdiction add-ons:
- FEMA (CLOMR): line-ending and hash checks are part of the submittal package QC (STARVALLEY-001, STARVALLEY-003).

QC checks:
- preflight_pass = chronology OK + volume match + duration covers recession + no double counts + CRLF + hashes equal.
- Volume error 0.0% in SUMMARY.OUT is not evidence of valid inflow chronology.

Source cards: NORTHLOOP-004, NORTHLOOP-005, CAMPBELL-010, STARVALLEY-001, STARVALLEY-003
Tool versions cited: NORTHLOOP-004: FLO-2D Pro 17.08.17; Python 3 | NORTHLOOP-005: FLO-2D Pro | CAMPBELL-010: HEC-RAS 6.6 | STARVALLEY-001: FLO-2D Pro Build 23.10.25 and 26.02.25, Python 3.12 | STARVALLEY-003: FLO-2D Pro Build 23.10.25

### HYD-C04 FLO-2D engine build selection, stall bisection and legacy effective model conversion
skill | new skill flo2d-engine-build-and-legacy-conversion; add-on flo2d-engine-build-and-legacy-conversion/FEMA and /town-of-marana | score 28.5 | hours 15.5 | cards 3 | projects 2 (NORTHLOOP, STARVALLEY) | confidence high

Trigger: A FLO-2D run fails at startup (War30.bac access denied), stalls at a fixed simulation time with no error, a jurisdiction names an engine build, or the effective model is in an old build (e.g. 2009) and current-build duplicate effective / existing / proposed models are needed.

Steps (merged):
1. Preserve the effective / archived package unchanged; work on copies and hash the copy.
2. Test the engine on a copied vendor example under the normal user account (Run for Project Folder package). If only the archived build fails, do not change folder permissions or UAC; choose between a vendor repair of the legacy build or the installed build.
3. For a stall: start from a known-good model folder, make variants swapping file groups from the failing model (terrain, roughness, infiltration, structures, controls), run all variants in parallel to a fixed simulation time, narrow to one file group, then test the same inputs on a newer build.
4. Legacy conversion: split FPLAIN into TOPO/MANNINGS_N/FPLAIN, remove obsolete TOLER fields, add floodplain and channel Courant fields, set storm-drain and IRAINBUILDING switches off; shorten structure names over 30 characters without changing hydraulic numbers and log each change; remove stale .RGH outputs copied with the package.
5. Run upstream and detailed models; compare depths and hydrographs to effective results by footprint; run Courant sensitivity (e.g. 0.6, 0.4, 0.2) and compare peak flows in sensitive clusters.
6. Adopt one engine build for all conditions; if the build changes, rerun every scenario (existing, proposed, mitigation) on it; never compare new-build results with old-build baselines.
7. Record engine SHA256, build number and vendor revision notes in the model basis and the report issues section; get EOR acceptance of the current-build baseline in writing and ask the agency to accept a build that differs from its manual.

Gotchas:
- Build 17.08.17 reproduced the War30.bac error on a vendor example; build 26.02.25 ran without admin prompts. The admin prompt could only be approved at the desktop, not from a phone (NORTHLOOP-008, claude via Codex session)
- The Town manual names 17.08.17, so moving to 26.02.25 is an open agency-acceptance item (NORTHLOOP-008, claude via Codex session)
- Build 23.10.25 stalled at sim hour 1.2 with the effective terrain plus effective n or infiltration; Build 26.02.25 ran the same files to completion and was adopted for all models (STARVALLEY-010, claude via Codex session)
- Legacy 2009 executable runs only in limited demo mode without a license and exits without results; plan on converting to the current Pro build (STARVALLEY-010, claude via Codex session)
- Current build did not reproduce legacy results exactly (up to 1.57 ft upstream, 0.59 ft detailed); legacy exe could not run without a license; EOR directed: document differences and use the Pro baseline (STARVALLEY-011, claude via Codex session; EOR direction)
- Do not adjust terrain, inflows or ratings to force a match (STARVALLEY-011, claude via Codex session; EOR direction)

Jurisdiction add-ons:
- FEMA: current build is the duplicate-effective basis; document differences from legacy results rather than forcing a match (STARVALLEY-011).
- Town of Marana: the manual names build 17.08.17; any other build is an agency-acceptance item (NORTHLOOP-008).

Source cards: NORTHLOOP-008, STARVALLEY-010, STARVALLEY-011
Tool versions cited: NORTHLOOP-008: FLO-2D Pro 17.08.17, 26.02.25 | STARVALLEY-010: FLO-2D Pro Build 23.10.25, 26.02.25 | STARVALLEY-011: FLO-2D 2009.06, FLO-2D Pro Build 23.10.25 and 26.02.25

### HYD-C05 FLO-2D natural-section 1D channel build and validity checks
qc_rule | QC rule (05_QC_Rules) + new skill flo2d-channel-build (procedure); FEMA add-on | score 101.0 | hours 11.0 | cards 2 | projects 1 (STARVALLEY) | confidence high

Trigger: Building or rebuilding a FLO-2D 1D channel (CHAN.DAT, CHANBANK.DAT, XSEC.DAT) from a centerline and terrain or survey.

Steps (merged):
1. Bank cell = first non-channel (floodplain) cell perpendicular to flow; never another channel cell.
2. Each grid cell belongs to exactly one segment; drop stub reaches of 2 cells or less.
3. XSEC.DAT: 20-25 station points per section (hard limit near 33); thalweg interior with ground rising both sides; relief >= 0.5 ft; no duplicate stations.
4. Number natural cross sections consecutively with no gaps; one XSEC per channel element.
5. Treat abrupt invert drops in constructed channels as grade-control structures unless the EOR says otherwise; do not smooth them out; list each drop (location, height) for EOR review and decide if a structure rating is needed.
6. Do not model onsite drainage channels as dead-end 1D reaches without their outlet culverts.
7. Build CHANBANK only after the final section cut.
8. Write xsec_adjustments_*.csv listing every section with synthetic banks or relief adjustment for engineer review; consider leaving flat tails as 2D.
9. Plot plan, profile and section QC exhibits before the first run; write inputs CRLF (HYD-C03).

Gotchas:
- Channel rebuild took 8 fix iterations in one day (v1-v8): bank-is-channel cells, duplicate cells, stub reach, 61-point sections, LF line endings, thalweg at section endpoint and flat sections giving Error 11 division by zero (STARVALLEY-002, claude session)
- Non-consecutive cross-section numbering let a 30 hr run finish integration then fail writing output (Intel Fortran EOF at CHMAX2.TMP); only consecutive renumbering fixed it (STARVALLEY-002, claude session)
- CHANBANK written before sections were re-cut produced a fatal mismatch; build banks after the final section cut (STARVALLEY-002, claude session)
- 65 flat-terrain sections needed synthetic banks (thalweg + 1.5 ft); consider leaving flat tails as 2D instead (STARVALLEY-002, claude session)
- EOR correction: steps up to 5.9 ft in the constructed channels are real rip-rap grade controls and must be kept in the section geometry (STARVALLEY-016, claude session; EOR correction)

Source cards: STARVALLEY-002, STARVALLEY-016
Tool versions cited: STARVALLEY-002: FLO-2D Pro Build 23.10.25 and 26.02.25 | STARVALLEY-016: FLO-2D Pro Build 23.10.25

### HYD-C06 FLO-2D hydraulic structure setup (zero-flow culverts, HY-8 rating tables)
qc_rule | QC rule (05_QC_Rules) + section in new skill flo2d-channel-build | score 40.0 | hours 8.0 | cards 1 | projects 1 (STARVALLEY) | confidence high

Trigger: Adding culverts or basin structures to HYSTRUC.DAT, or HYDROSTRUCT.OUT shows zero flow where flow is expected.

Steps (merged):
1. Inlet and outlet cells are never channel-interior cells (between a channel element and its bank cell); use the channel element or a true floodplain cell; set IFPORCHAN to match.
2. Rating tables: ICURVTABLE = 1 (table), not 0.
3. With HEADREFEL 0, re-reference HY-8 headwater from culvert invert to inlet-cell bed and record the offset.
4. Export all tables from one HY-8 project with matching names; discharge range covers the model peak with no extrapolation; tailwater assumption in the table matches the model.
5. After each run read per-structure peak and volume (struct_flows.py) and stop if any wet-inlet structure shows zero flow.

Gotchas:
- Four rebuilds (v5, v5a, v5b, ALT-A) passed zero flow before the cause was found: inlets on channel-interior cells (DEPFP=0); ICURVTABLE 0 was a second, separate bug (STARVALLEY-012, claude session; FEMA review comment)
- June basin structures had inlets on 1D channel elements declared as floodplain and a table assuming full-basin tailwater; FEMA noted zero flow and HY-8 name/range mismatch (STARVALLEY-012, claude session; FEMA review comment)

Source cards: STARVALLEY-012
Tool versions cited: STARVALLEY-012: FLO-2D Pro Build 26.02.25, HY-8 8.0

### HYD-C07 FLO-2D nested grid handoff (upper outflow to lower inflow)
skill | new skill flo2d-nested-grids; add-on /pima-county-rfcd (TECH-033 Amendment A) | score 9.0 | hours 4.5 | cards 1 | projects 1 (SAH) | confidence high

Trigger: A coarse UPPER FLO-2D grid (e.g. 40 ft) feeds a fine LOWER grid (e.g. 20 ft) through Inflow1_DS.DAT.

Steps (merged):
1. Build LOWER first so CADPTS.DAT exists; copy it into UPPER as CADPTS_DS1.DAT; delete UPPER *.OUT; run UPPER.
2. Copy UPPER Inflow1_DS.DAT to LOWER INFLOW.DAT.
3. Run the nested inflow fix on LOWER: keep INFLOW_raw.DAT, sum all inflow nodes on each grid row into the downstream-most inflow column, check total volume unchanged (log node count before/after).
4. Delete LOWER *.OUT and run LOWER; check FINALDEP.OUT / DEPTH.OUT along the overlap strip for ponding before using results.
5. Use one parameterized pair script (build LOWER, build UPPER, handoff, fix, run) with folder naming UPPER_|LOWER_<storm>_<RP>yr<_options>; always use the version that includes the fix.

Gotchas:
- FLO-2D maps UPPER boundary outflow to several LOWER cell columns in the overlap strip. Inflow nodes do not accept flow from neighbours, so hydrographs on the western columns were trapped. First LOWER 3-hr and 24-hr 100-yr runs were wasted and rerun LOWER-only (0.82 h + 2.91 h run time plus diagnosis) (SAH-002, claude session)
- flo_pair.cmd (first version) lacked the fix; flo_pair2.cmd and flo_lower2.cmd include it. Always use the fixed version (SAH-002, claude session)

Jurisdiction add-ons:
- Pima County RFCD: TECH-033 Amendment A - upstream outflow = downstream inflow.

Source cards: SAH-002
Tool versions cited: SAH-002: FLO-2D Pro Build 26.02.25

### HYD-C08 Existing vs proposed impact comparison on matched models (common mesh/grid, control cases, dWSE)
skill | new skill impact-comparison (core) + QC rule; jurisdiction add-on impact-comparison/FEMA (44 CFR 65.12) | score 108.0 | hours 37.0 | cards 6 | projects 5 (CAMPBELL, ELTORO, NORTHLOOP, STARVALLEY, TANGERINE) | confidence mixed (NORTHLOOP-009 medium, ELTORO-017 medium; rest high)

Trigger: Any report claim of no adverse impact, maintained flow distribution, pad clearance or BFE rise; grading or berm sensitivity tests; CLOMR existing/proposed comparison.

Steps (merged):
1. Build all conditions from one model set: same 2D perimeter / grid (CADPTS identical), cell size, breaklines, 1D channel network, FPXSEC, INFLOW, OUTFLOW, TOLER, RAIN, controls and engine build; only terrain (inside approved grading surfaces) and roughness / development differ. Hash-check shared files in package QC.
2. Use the effective grid elevations as base terrain in every model; check effective grid vs new survey (mean, std dev) before deciding to resample.
3. Run the existing-condition model at the same vintage and include its outputs.
4. For grading tests build a control plan with the same modifier geometry raised out of the ground so processing matches; confirm control equals base (e.g. within 0.0003 ft). Direct grading effect = test - control; impact = test - existing.
5. Join cells by verified ID and XY (or containing cell by physical location when meshes differ, and say the result includes mesh changes); compare depth, WSE, velocity (and shear) for cells wet above 0.1 ft; report new wet areas separately.
6. Produce cell-by-cell difference maps / RAS Mapper calculated difference layers with NoData handled (-9999); report changes beyond the ROW / parcel and at structures with a fixed threshold (e.g. 0.10 ft); split changes near boundaries where CAD and GIS lines disagree.
7. Tabulate existing vs proposed peak Q, volume, timing, WSE, depth, velocity at upstream inflows, property boundaries, road crossings, downstream constraints; outlet hydrograph split by domain exit (synchronized 0.5-hr series from final OUTNQ.OUT).
8. Pad clearance = max wet-cell WSE within 100 ft of the pad with 30/50/100/200 ft reference values; label screening, not a certified floor elevation.
9. Set a stop limit with the user for sensitivity series (e.g. opening lowering capped at 4.00 ft) and stop when no case meets targets; never change approved physical grading to fix numerical behavior.
10. Run the results script with all scenario folders together so the register is complete; only then state no adverse impact, else label the comparison distributional/qualitative.

Gotchas:
- June models: existing and Interim carried only an 18-cell eastern trapezoid while Ultimate carried a 567-cell western channel; offsite dWSE over 1 ft (157 cells) was an artifact of that mismatch (STARVALLEY-007, claude session)
- Interim and Ultimate used re-sampled terrain differing from the effective grid by up to 11 ft across the 3,060 ac domain; effective grid matched the 2025 survey to 0.15 ft mean (STARVALLEY-007, claude session)
- The concept report compared meshes of different extent and resolution and still drew strong conclusions; three reviewer comments (T1-6, T1-11, R-1) asked for a common-mesh re-run, now deferred to the master drainage report (TANGERINE-003, claude session; agency review comments)
- Running the comparison with only two folders overwrote the three-case results register (NORTHLOOP-009, claude session)
- FLO-2D lowers outlet-cell elevations internally, so WSE minus ground there does not equal max depth; interior cells reconcile within 0.0002 ft (NORTHLOOP-009, claude session)
- Partial outlet review from an incomplete run window is not usable; wait for the final file (NORTHLOOP-009, claude session)
- The 10 ft grid run produced a 934 MB post-processing HDF; keep fine-grid runs out of synced folders (ELTORO-017, claude session)
- North-bank 1 ft cut moved about 348 cfs north but worsened local rail rise (0.44 to 0.94 ft) (CAMPBELL-008, claude session)
- Opening lowering through 4.00 ft left about 1.5 ft rise; no target met (CAMPBELL-008, claude session)
- Proposed rail surface flow stayed about 700-900 cfs above existing in all tests; the issue is flow redistribution at the crossing (CAMPBELL-008, claude session)
- Extreme dWSE values at fill slopes and excavated basins come from ground change, not flood change; review before quoting min/max (STARVALLEY-008, claude session)
- A 34.6 ac over-1-ft cluster came from a placeholder flat surface in the proposed TOPO, not real grading (STARVALLEY-008, claude session)
- Property-boundary linework is needed to classify edge cells; request it early (STARVALLEY-008, claude session)

Jurisdiction add-ons:
- FEMA (44 CFR 65.12, Region IX): dWSE = proposed MAXWSELEV - existing; evaluate rises where max depth >= 1.0 ft in both conditions (SFHA), any-depth counts separately; map new and removed SFHA cells; list every cell > 1.00 ft with ground change, depth change and location (applicant land, approved grading, channel prism); write rasters, > 1 ft polygons, summary JSON and exhibit and quote report values from them; for cells on other ownership prepare alternatives, notices on the CLOMR template and PE certification (STARVALLEY-008).
- Town of Marana / Pima County RFCD: reviewers require common-mesh existing/proposed runs before no-adverse-impact text (TANGERINE-003).

QC checks:
- No-adverse-impact wording only with matched-model difference maps and tables.
- Shared input hashes equal across compared conditions.

Source cards: STARVALLEY-007, TANGERINE-003, NORTHLOOP-009, ELTORO-017, CAMPBELL-008, STARVALLEY-008
Tool versions cited: STARVALLEY-007: FLO-2D Pro Build 26.02.25 | TANGERINE-003: HEC-RAS 6.6 / 7.0 2D unsteady | NORTHLOOP-009: FLO-2D Pro; Python 3 numpy | ELTORO-017: HEC-RAS 7.0 RAS Mapper calculated layers | CAMPBELL-008: HEC-RAS 6.6 | STARVALLEY-008: FLO-2D Pro Build 26.02.25, Python 3.12, numpy, geopandas, rasterio

### HYD-C09 HEC-RAS 2D numerical stability: SWE wetting-front triage and mesh-induced velocity spikes
skill | new skill hecras-2d-stability-triage | score 58.0 | hours 14.0 | cards 2 | projects 1 (CAMPBELL) | confidence high

Trigger: A diffusion-wave 2D model must be rerun with SWE-ELM/SWE-EM (embankment, abrupt flow interruption) and crashes or shows large residuals, or a mesh is refined along an embankment/berm/railroad.

Steps (merged):
1. Keep the accepted DWE pair untouched; build trials in a new dated folder with new plan numbers.
2. Read the native compute log for the first residual cells and map them (steep terrain in small partly wet cells; roadway wetting fronts).
3. Try SWE-ELM before SWE-EM; keep Courant target below 1 for SWE-EM per HEC troubleshooting documents (not web posts).
4. Enlarge or realign cells at the failing front rather than refining; use wash-aligned cells, breaklines along banks, broader transitions; avoid very short faces along embankments; fix grid-transition cells that fail the max-side-count check before running.
5. Retest the first 1-6 hr window before a full event.
6. After every run extract max face velocity and its location (not just volume error); velocities far above physical (hundreds of fps) are numerical spikes - label the run diagnostic; check saved velocity series before accepting a peak.
7. For a timestep check use fixed step (adaptive off), e.g. 1 s base with 20 slices = 0.05 s local, on an identical-geometry existing/proposed pair; do not claim timestep convergence from one pair.
8. Accept only when native volume error, max cell WSEL residual, max face velocity and full end time are checked; report peak WSEL change vs DWE by location. Numerical tests are not mitigation.

Gotchas:
- Advice copied from web posts (Courant 3) conflicted with HEC guidance for SWE-EM; follow the HEC troubleshooting documents (CAMPBELL-001, claude via Codex session)
- Changing the momentum solver alone did not fix wetting-front errors; the mesh at the road front had to change (CAMPBELL-001, claude via Codex session)
- Fixed 0.05 s SWE-ELM pair finished with volume error near 0.07 pct but localized peak WSEL shifted up to 1.5 ft vs adaptive runs; do not claim timestep convergence (CAMPBELL-001, claude via Codex session)
- A smaller timestep did not remove the railroad increase (1.33 ft vs 1.06 ft); numerical tests are not a mitigation (CAMPBELL-001, claude via Codex session)
- Two refinement levels (54,036 and 68,273 points) gave 438-588 fps spikes on short railroad faces and did not converge (CAMPBELL-003, claude via Codex session)
- Wash-aligned refinement removed the spikes (max about 24 fps, volume error 0.006 pct) (CAMPBELL-003, claude via Codex session)
- A brief sub-minute native velocity peak (93 fps vs 3 fps saved 60 s max) remained unresolved later; do not accept peak velocity without checking saved series (CAMPBELL-003, claude via Codex session)
- Mesh generation can fail the max-side-count check at a grid transition; fix the transition cell before running (CAMPBELL-003, claude via Codex session)

Source cards: CAMPBELL-001, CAMPBELL-003
Tool versions cited: CAMPBELL-001: HEC-RAS 6.6 (2D DWE, SWE-ELM, SWE-EM) | CAMPBELL-003: HEC-RAS 6.6

### HYD-C10 HEC-RAS native automation API (text/HDF edits, RasProcess, COM, RasMapperLib terrain)
skill | new skill hecras-native-automation (shared library module); referenced by HYD-C11 | score 43.5 | hours 9.0 | cards 3 | projects 3 (CAMPBELL, EKOS-LOCAL, SILVERBELL) | confidence mixed (SILVERBELL-006 medium; rest high)

Trigger: Creating terrain, geometry, 2D mesh, 1D sections, culverts, roughness overrides or new plans, or running RAS, without the GUI.

Steps (merged):
1. Copy the project to a new work folder; never edit source plans; run COM/CLI on isolated copies and always quit the controller.
2. Write .prj/.g/.p/.u/.rasmap with CRLF line endings.
3. HDF string attributes: delete and recreate (h5py attrs.modify keeps the old fixed length and truncates paths/names); create new datasets chunked and gzip compressed like native ones.
4. Terrain: RasProcess CreateTerrain on the source grid (no resample), explicit ESRI projection and units, read back every pixel; or RasMapperLib with native GDAL initialized and a console progress display, NaN for the unused tile-write parameter, raster statistics then overviews before import. Verify terrain HDF exists, extent and dataset count. Place rasters in the project Terrain folder (hard link if needed); absolute raster paths in the terrain HDF are not resolved.
5. Geometry: CreateGeometry GeometryFilename=... UnitSystem=..., GenerateMesh with perimeter shapefile and cell size, CompleteGeometry GeomFilename=... RasMapFilename=...; count only the first Cell Count polygons as real cells (rest are ghost centers); check no gaps/overlaps.
6. 1D blocks: station-elevation in strict 8-character fixed width with Decimal values; read native HDF back for every ordinate, bank, length, roughness. Reject culvert names longer than 12 ASCII bytes.
7. Roughness: associate through native RasProcess geometry association (default NoData n; channel polygons first, first polygon wins); HDF-only patches do not persist.
8. Run: COM preprocess, confirm property tables recomputed, set core count in tmp.hdf (COM may reset it to automatic), launch RasUnsteady and check stdout; discover outputs with Output_Variables / Output_GetNodes; treat 3.4e38 as unavailable.
9. Diff new geometry tables against the source (cell centers, faces, structures, n) to prove only intended changes; keep project units explicit and record conversions.
10. Check the RasMapperLib command inventory before scripting (several commands not implemented).

Gotchas:
- LF files were read as empty: RAS created default g01/p01 and started a steady run (CAMPBELL-004, claude session)
- Truncated raster path gave terrain does not cover the 2D Flow Area (CAMPBELL-004, claude session)
- Contiguous datasets gave H5Pget_chunk not a chunked storage layout (CAMPBELL-004, claude session)
- A truncated flow-area name (Perimete) made table generation build an empty mesh (CAMPBELL-004, claude session)
- COM may reset core count to automatic; verify the native setting (CAMPBELL-004, claude session)
- Command-line runs gave no output within 90 s; COM fallback worked for 1D (EKOS-LOCAL-010, claude session)
- PowerShell script execution is disabled on this host; exact CLI arguments came from passive .NET metadata (dnfile, dncil), no policy bypass (EKOS-LOCAL-010, claude session)
- CreateGeometry uses GeometryFilename but CompleteGeometry uses GeomFilename (EKOS-LOCAL-010, claude session)
- Culvert names longer than 12 ASCII bytes are silently truncated in the HDF; reject before running (EKOS-LOCAL-010, claude session)
- pywin32 GetTypeAttr function count is index 6; index 8 gave a false empty output inventory (EKOS-LOCAL-010, claude session)
- CompleteGeometry warned Geometry/Structures not found; do not add fake structures to silence it (EKOS-LOCAL-010, claude session)
- Synthetic reach and culvert tests passed but the project 1D/2D model was never completed; synthetic success is not a project result (EKOS-LOCAL-010, claude session)
- Recurrence note: about 25 RAS tasks, 4 failures, project model not reached (EKOS-LOCAL-010, claude session)
- Eight helper builds over about 30 min returned No target dataset specified until NaN and stats/overview order were fixed (SILVERBELL-006, claude session)
- Several RasMapperLib scripting commands (GenerateMesh, SetGeometryAssociation XMLSave) are not implemented; check the inventory before scripting (SILVERBELL-006, claude session)

Source cards: CAMPBELL-004, EKOS-LOCAL-010, SILVERBELL-006
Tool versions cited: CAMPBELL-004: HEC-RAS 6.6, h5py, RAS COM | EKOS-LOCAL-010: HEC-RAS 6.6 (RasProcess.exe, RAS66 COM), pywin32, dnfile 0.18.0, h5py | SILVERBELL-006: HEC-RAS RasMapperLib .NET API

### HYD-C11 HEC-RAS 2D model build by script (rain-on-grid / inflow), alternatives and headless runs
skill | new skill hecras-2d-model-build; add-ons hecras-2d-model-build/pima-county-rfcd (TECH-018, TECH-033) and /town-of-marana (alluvial fan) | score 68.0 | hours 20.5 | cards 6 | projects 6 (CALFIRE, ELTORO, RKN, SAH, SILVERBELL, TANGERINE) | confidence mixed (SAH-010 medium; rest high)

Trigger: Building existing and proposed 2D HEC-RAS models from GIS/lidar (rain-on-grid, offsite inflows, culverts as SA/2D connections), extending an accepted model, or a screening/review 2D model.

Steps (merged):
1. Copy any accepted model to a new working copy; never edit it in place; keep Manning n and other accepted parameters unless the change is documented (see HYD-CF-08).
2. Terrain: merge DEM (e.g. USGS 1 m or 3 ft) + survey at crossings into one GeoTIFF in the model CRS/vertical datum; check the seam; proposed grading as a stacked raster/modification, not re-copied tiles.
3. Domain: cover the full contributing basin edge (check slivers) or project buffer; extend outflow BC at least 5 cells past the area of interest; trim BC line ends so no two BC lines share a face.
4. Mesh: cell size by zone (e.g. 10 ft tributary/near road, 20-30 ft corridor, 60-100 ft upper piedmont); breaklines on road crown, wash, curbs, path; overbank cells <= 100 ft where depths are 0.5-2 ft or run a grid-independence check.
5. Land cover: spatially varied n (active wash about 0.030-0.040, desert scrub 0.035-0.050, roads, pads, basins) and CN raster (burn pavement/path CN 99, include roads); uniform n only for feasibility or to match an accepted model.
6. Structures: SA/2D connections along road crests with weir profile stations from terrain over the full line (length within 1 ft of centerline); culvert inverts and barrel length set explicitly (survey/lidar), not from GIS line length; bridge type 32 (rating curves) under DWE, type 33 needs SWE.
7. Boundary conditions: rain-on-grid hyetographs to DSS (e.g. NOAA Atlas 14 upper bound, 5-min) and/or offsite inflow hydrographs only for areas outside the mesh (register per HYD-C12); synthetic hydrographs labelled not calibrated.
8. Plans: one plan and one unsteady flow file per event / condition, meaningful names (HYD-C13); run windows cover the recession (HYD-C03).
9. Build order (scripted): geometry -> mesh -> BC lines (rewrite after mesh changes) -> land cover -> mesh layers -> unsteady flow and plans; rebuild script runs all steps in order. Alternatives: copy base, stack grading raster, add culverts, regenerate mesh.
10. Run a 1 hr diagnostic first, then full events headless (Ras.exe -c <prj> <plan> -hideCompute; one project copy per plan for parallel runs; copy HDF and compute messages back) or as a separate supervised job (HYD-C01).
11. Judge success by plan HDF existence and compute messages (volume error, iteration warnings, hydrographs, wet boundary), not the launcher return code; if the launcher reports failure while a temp HDF remains, a watchdog may run RasUnsteady on p##.tmp.hdf and rename it.
12. Check plan HDF exists before StoreAllMaps / result extraction; store WSE, depth, velocity maps per plan; extract culvert flow, HW/TW, flow out each boundary and road overtopping to a results CSV.
13. Set PYTHONIOENCODING=utf-8 for library logs; split work so input prep is scripted and long computes run on the desktop.

Gotchas:
- RasProcess CreateTerrain reports stderr warnings but completes; check the terrain HDF (dataset count) instead of the warning stream (RKN-007, claude session; SAH-010, claude session)
- compute_plan reported FAILED / could not confirm solver quiescence on 3 of 4 plans while the temp HDF remained; fix was a watchdog that polls RasUnsteady.exe, then runs RasUnsteady.exe directly on p##.tmp.hdf and renames it (CALFIRE-009, claude session)
- StoreAllMaps returned 0 files when the plan HDF was missing; check the HDF exists before mapping (CALFIRE-009, claude session)
- Data error: weir profile length 1 vs GIS centerline 900 ft (must match within 1 ft); set the connection profile stations from terrain along the full line (CALFIRE-009, claude session)
- Culvert barrel length from the GIS line differed from the lidar measured 110 ft; set length explicitly (CALFIRE-009, claude session)
- One late rerun of plan 01 forced a second figure and PDF compile (about 35 min) (CALFIRE-009, claude session)
- Plan returned rc=0 after 0.1 min with no HDF - geometry error 'BC lines share the same face'. Fix - trim 100 ft off the BC line end nearest the other line and recheck (22c_fix_bc_overlaps.py); needed for EX and PR (RKN-007, claude session)
- Each 2D plan ran 19-32 min; one Alt2 plan had to be rerun alone (RKN-007, claude session)
- RFCD acceptance of the 2D approach is an open approval item (RKN-007, claude session)
- ras_rebuild.cmd must run all four steps in order; BC lines were rewritten after mesh changes (replaced=2) (SAH-010, claude session)
- Set PYTHONIOENCODING=utf-8; library banners use non-ASCII characters and broke logs (SAH-010, claude session)
- Opening an HDF while RAS was writing caused a write failure; the mesh was discarded and rebuilt. Never read active .tmp.hdf (SILVERBELL-005, claude session)
- Direct HDF-only roughness patches did not persist; use the native association (SILVERBELL-005, claude session)
- Proposed run had 3,520 iteration warnings and 17.1 ft max WSEL error at 0.25 pct volume error; not accepted. Existing run 517,161 cells, 1 hr 39 min, 0.000136 pct (SILVERBELL-005, claude session)
- Ambiguous duration from the user (3 6 hours) was interpreted and logged; confirm such inputs early (SILVERBELL-005, claude session)
- Basin sliver extended about 1,000 ft west of the perimeter NW corner; perimeter was widened to capture it (ELTORO-004, claude session)
- Roads omitted from the CN layer are slightly non-conservative locally; burn them from plans or county land use (ELTORO-004, claude session)
- Adjacent accepted study used FLO-2D with SCS Type II 3-hr on a 10 ft grid; moving the model from 1-hr to 3-hr aligned better with precedent (ELTORO-004, claude session)
- Manning n kept uniform 0.035 to match the accepted model; changing it breaks comparability with the accepted results (ELTORO-004, claude session)
- Every one of these items was raised by reviewers on the concept model and carried as deferred work (A-1, A-3, T1-4, T1-5, T1-7, T1-8); doing them in the first model build avoids a second model cycle (TANGERINE-005, claude session; agency review comments)
- Contracted scope assumed 1D HEC-RAS; the 2D approach needed a scope note in the report; flag scope mismatch to the PM early (TANGERINE-005, claude session; agency review comments)

Jurisdiction add-ons:
- Pima County RFCD: TECH-033 2D rain-on-grid for existing and each alternative (plans 100/2/10/500-yr); compare 1-hr IDF storm vs SCS Type II 3-hr and use the critical storm per TECH-018; CN from PC-Hydro User Guide table (HSG A desert brush treated as B, 20% density = CN 83); RFCD acceptance of a 2D approach is an approval item (RKN-007, ELTORO-004, SAH-010).
- Town of Marana / Pima County RFCD alluvial fan (Town of Marana Drainage Manual 2024, ADWR SS4-95/SS5-96, FEMA alluvial fan guidance): DWE for broad fan flow then test SWE at road crossings, pinch points, berms and high-velocity cells; appendix documenting terrain, breaklines, boundary hydrographs, timestep, Courant, volume balance and instability locations; 200-yr or increased-rainfall stress run; node-to-node volume ledger; velocities in erodible soils approaching 16-20 fps need bank protection or erosion-hazard setbacks; flag 1D-vs-2D scope mismatch to the PM (TANGERINE-005).
- FEMA 2D guidance referenced for rain-on-mesh builds (SAH-010).

Source cards: CALFIRE-009, RKN-007, SAH-010, SILVERBELL-005, ELTORO-004, TANGERINE-005
Tool versions cited: CALFIRE-009: HEC-RAS 6.6; ras_commander (Python 3.12) | RKN-007: HEC-RAS 6.6, ras_commander | SAH-010: HEC-RAS 6.6, ras-commander 0.103.0 | SILVERBELL-005: HEC-RAS 2D diffusion wave, 8 cores, 5 s fixed step | ELTORO-004: HEC-RAS 6.6; NOAA Atlas 14 Vol 1; Python rasterio/geopandas | TANGERINE-005: HEC-RAS 6.6 / 7.0 2D unsteady

### HYD-C12 Boundary inflow register for hybrid rain-on-grid plus inflow 2D models
skill | section in new skill hecras-2d-model-build (procedure) + QC rule (inflow reconciliation) | score 18.0 | hours 6.0 | cards 1 | projects 1 (ELTORO) | confidence high

Trigger: A 2D model combines direct rainfall on the mesh with hydrographs from prior drainage reports or master plans.

Steps (merged):
1. List every candidate inflow from the source reports: CP id, area (ac), Q2/Q10/Q100 (cfs), report page, condition (existing/developed).
2. Overlay each CP watershed on the 2D perimeter; keep a BC inflow only where the contributing area lies outside the mesh.
3. Build a map-based CP concordance across studies; use one value for the same watershed under two names; remove the upstream CP whenever its downstream CP is entered.
4. Export the BC list from the .u0x (name, peak) and reconcile line by line against the register; record condition basis for each.
5. Place each inflow BC where the culvert or wash discharges into the mesh; tag with coordinates.
6. Volume check: precipitation volume + inflow volume = outflow + storage + infiltration.

Gotchas:
- The accepted MUP model carried CP-13 twice (BC lines CP-13 and CP13, both 43 cfs); a straight double count that survived into the extended model until the inflow rebuild (ELTORO-001, claude session)
- Project notes listed WS10, B4, WS13 and CP-13 at 967/667/95/717 cfs while the report developed values are 2/40/3/43 cfs; treat note values as suspect until checked against the .u0x (ELTORO-001, claude session)
- Rebuilding inflows on the extended model replaced CP-W1 (2,254 cfs) with CP-10 (1,412 cfs) plus the South Outfall CPs; confirm the upstream CP is removed whenever its downstream CP is entered (ELTORO-001, claude session)
- CP numbering is not consistent across the 1999, 2005/2006, 2008 and 2021 studies; build a map-based concordance before transferring any value (ELTORO-001, claude session)

Source cards: ELTORO-001
Tool versions cited: ELTORO-001: HEC-RAS 6.6 and 7.0; PC-Hydro 5.4.3 (source report)

### HYD-C13 Model set intake, plan/folder register and storage housekeeping (received or archived models)
skill | new skill model-set-intake-register + QC rule (plan citation in report); used by due-diligence-researcher and report-writer | score 24.0 | hours 11.0 | cards 6 | projects 4 (DLR, NORTHLOOP, SAHPARK, TANGERINE) | confidence mixed (DLR-001 medium, DLR-002 medium, DLR-003 medium, SAHPARK-016 medium; rest high)

Trigger: A HEC-RAS or FLO-2D model set is received or reused from an archive; report text cites plans; a multi-plan corridor model is built in a synced project folder.

Steps (merged):
1. Keep the delivered zip / archive untouched as record copy; work on an extracted copy. Budget disk at 2-3x zip size; never open multi-GB tif/HDF in a viewer - read .vrt and .rasmap text.
2. Read the .prj as text; list registered Geom, Unsteady, Plan files and the as-received Current Plan (record before editing).
3. For each .p## read Plan Title, Short Identifier, Geom File, Flow File, Program Version, Computation Interval; build a plan-geometry-flow-terrain-condition register (status live/superseded) and keep it in the model folder.
4. Compare register with files on disk: flag unregistered plans, entries without files, stray copies (renamed .hdf, .tmp.hdf, snapshot HDFs, Backup.p##); never treat them as results.
5. Confirm each plan's flow file matches its title/storm; separate titles or clearly named plans for existing vs proposed; rename generic plan titles to condition-specific names before results are reported.
6. FLO-2D archives: register every native folder (build, grid, run time, terrain changes vs base, levee/barrier records); diff each alternative grid against base; match folder to report figures; never select by folder name or newest timestamp; separate artificial levee barriers from real proposed grading.
7. Terrain packages: list Terrain folder sizes and each scenario .vrt source/cell size; scenario modifications live in terrain HDF or geometry, not the tif; identify duplicate source tiles; check stored maps' Terrain name and StoredFilename and regenerate missing maps.
8. CRS: read RASProjectionFilename in .rasmap, SRS in each .vrt and each delivered .prj; confirm same horizontal datum realization and units (e.g. EPSG 2230 vs 6426) and vertical datum; record CRS of each layer before any reprojection.
9. Open in the same or newer RAS version on a copy only (opening rewrites plan and geometry files); record versions.
10. Run and store models on a local non-synced drive; copy only final plan results to the synced share; delete .tmp.hdf and unused plan results before archiving.
11. Cite plan file, short ID and geometry in every caption and table that uses results.

Gotchas:
- Plan p01 (floodwall, existing event) existed on disk with a 1.5 GB result HDF and was cited in the delivered data dictionary, but was not registered in the .prj, so it did not appear in the RAS plan list. Fix - add the plan back through the .prj or open the .p01 directly (DLR-001, claude session)
- A stray renamed copy of a plan result HDF (p02 with extra letters appended) was the same size as the real one; easy to map the wrong file (DLR-001, claude session)
- RAS Mapper listed a 91 percent snapshot HDF as a results layer next to the completed run; check the layer name for Snapshot before mapping (DLR-001, claude session)
- One geometry HDF appeared twice in RAS Mapper under two different names, and a stub geometry HDF (0 MB) was referenced but not in the .prj (DLR-001, claude session)
- Plans mixed 30 s and 1 s computation intervals and RAS 6.70 / 7.00 / 7.01 files; a test plan created after receipt changed the project Current Plan. Record the as-received Current Plan before editing (DLR-001, claude session)
- The .rasmap projection was set from a feature shapefile .prj under Features rather than the Terrain Projection.prj; it matched here, but this is fragile when features are replaced (DLR-002, claude session)
- Delivered spot elevation points were in NAD83(2011) CA zone 6 ftUS (EPSG 6426) while all sampled rasters were NAD83 CA zone 6 ftUS (EPSG 2230); a silent datum-realization mismatch of up to a few ft if transformed by a GIS on the fly (DLR-002, claude session)
- Base terrain was one 53 GB tif at 0.615 ft cells (about 430,000 px square) plus a 2.2 GB terrain HDF; the three scenario terrains were VRTs over that same tif (DLR-003, claude session)
- Stored depth maps referenced terrain clone names that were not delivered and output folders that did not exist, so they would not display until recomputed (DLR-003, claude session)
- The same USGS and county DEM tiles were delivered twice in two Terrain subfolders, including two 6.8 GB county DEM copies (DLR-003, claude session)
- Report and figure captions cite existing conditions as Plan 12 / EX_<init>_LG, but p12 is titled Plan 12 with no short ID (geometry g08), and the project notes name p09 EX_<init> as existing; no plan file carries EX_<init>_LG (TANGERINE-004, claude session)
- 12 plans and 8 geometries in one project with superseded iterations p01-p08 make the wrong HDF easy to read; confirm the plan before exporting rasters (TANGERINE-004, claude session)
- Plans p05 (100-yr) and p06 (10-yr) both point to the same flow file u02 - the 10-yr run either used 100-yr flows or the file was overwritten between runs; matches the mislabeled-storm comment on the draft (SAHPARK-016, claude session)
- OneDrive sync created a conflict copy of the g04 geometry .hdf (225 MB) (SAHPARK-016, claude session)
- Same 8 USGS tiles copied into three terrain folders (SAHPARK-016, claude session)
- About 40 geometry saves (g02, Jun 18-29) and 19 saves (g04, Jul 9-10) in Backup show heavy iteration on berm and road terrain (SAHPARK-016, claude session)
- Folder named Alt1 had an eastern channel and 2120-ft artificial barriers, while the report preferred alternative left the east natural (NORTHLOOP-006, claude session)
- Both named 500-yr folders were empty; the old 500-yr used a 1.75 x Q100 multiplier, not a saved run (NORTHLOOP-006, claude session)

Jurisdiction add-ons:
- California (received model set, CA zone 6): NAD83 realization check EPSG 2230 vs 6426 (DLR-002).

QC checks:
- Every cited plan exists, is registered, carries a condition-specific title and matches the caption.
- Plan flow file matches plan title/storm.

Source cards: DLR-001, DLR-002, DLR-003, TANGERINE-004, SAHPARK-016, NORTHLOOP-006
Tool versions cited: DLR-001: HEC-RAS 7.00 / 7.01, flow files 6.70 | DLR-002: HEC-RAS 7.0 RAS Mapper, GDAL VRT | DLR-003: HEC-RAS 7.0 RAS Mapper | TANGERINE-004: HEC-RAS 6.6 / 7.0 | SAHPARK-016: HEC-RAS 7.00 | NORTHLOOP-006: FLO-2D Pro; Python 3 numpy

### HYD-C14 2D result rasters, floodplain polygons and verification against RAS Mapper
skill | update skill hecras-result-rasters | score 1.25 | hours 0.75 | cards 2 | projects 2 (DLR, RKN) | confidence mixed (RKN-009 medium, DLR-006 medium; rest high)

Trigger: After each 2D plan finishes, or before using result rasters made by script instead of RAS Mapper stored maps.

Steps (merged):
1. Export max depth, WSE and velocity rasters (cell WSE on terrain) at the requested grid (e.g. 3 ft or the 10 ft default).
2. Floodplain polygons at depth >= 0.5 ft and area >= 0.25 ac (project criterion); proposed-minus-existing WSE with graded blocks masked.
3. Report BC peak flows, volume accounting and compute messages; flag BC lines with no results instead of reporting NaN peaks.
4. Record which tool made each raster (tag in name/README); spot-check depth, WSE and velocity at 5-10 points against a RAS Mapper max map of the same plan and terrain.
5. Confirm the terrain used for depth: the script resolves the geometry terrain name to a .vrt/.tif by basename and does not see terrain-HDF-only modifications.
6. State in deliverables that velocity is a max-face-velocity proxy; screen single-cell spikes before quoting peak velocity.
7. Use GDAL driver 'MEM' (not 'Memory', deprecated in GDAL 3.11).
8. Check deliverables for internal scripts / skill packages before release.

Gotchas:
- BC lines with no results give all-NaN slices; flag them instead of reporting NaN peaks (RKN-009, claude session)
- GDAL 3.11 deprecates the 'Memory' driver; use 'MEM' (RKN-009, claude session)
- The script burns one max WSE per cell polygon (flat per cell), not the sloped RAS Mapper surface, so depth shows steps at cell edges and differences can be noisy at wet-dry edges (DLR-006, claude session)
- Velocity is the max of face velocities around each cell and runs higher than RAS Mapper cell velocity (DLR-006, claude session)
- Depth uses the base .vrt; terrain modifications stored only in a terrain HDF are not seen. Here mitigations were in geometry so all plans used one terrain, but this must be checked each time (DLR-006, claude session)
- Output was regenerated at 10 ft cells from 0.6 ft terrain; spot values are sampled from the coarse grid, not source values (DLR-006, claude session)
- The script and its .skill package were shipped inside the delivered model folder; check deliverables for internal tools before release (DLR-006, claude session)

Source cards: RKN-009, DLR-006
Tool versions cited: RKN-009: HEC-RAS 6.6, h5py, rasterio | DLR-006: Python h5py/rasterio, HEC-RAS 7.0 plan HDF

### HYD-C15 Flow-section accounting from 2D/1D face output at railroads, breakouts and structures
qc_rule | QC rule (05_QC_Rules) | score 4.0 | hours 1.0 | cards 1 | projects 1 (CAMPBELL) | confidence high

Trigger: Reporting flows over or under a railroad, at breakouts, or at structures from 2D face output or 1D results.

Steps (merged):
1. Report railroad surface flow, bridge opening flow and culvert barrel flow separately.
2. Total crossing flow = peak of the simultaneous combined series, not the sum of separate peaks.
3. Do not add serial breakout sections (not a closed balance).
4. Label flow beneath the tracks only when bridge HW/TW stay below deck; else split opening vs overtopping.
5. Ignore near-zero-flow headwater spikes; compare stages at peak structure flow.

Gotchas:
- Terminal 1D reach flow is not bridge opening flow; extract Bridge Variables Flow (CAMPBELL-009, claude session)
- Some 1D FV velocity series are all zero; use max velocity flow distribution for mapping (CAMPBELL-009, claude session)

Source cards: CAMPBELL-009
Tool versions cited: CAMPBELL-009: HEC-RAS 6.6, h5py

### HYD-C16 Screening models vs FEMA effective (lidar 1D, fixed-map floodway, proposal-stage screening)
agent | agent due-diligence-researcher (screening mode) + QC rule (screening labels); add-on /FEMA | score 12.3 | hours 10.3 | cards 3 | projects 2 (CALFIRE, SILVERBELL) | confidence high

Trigger: Proposal-stage or concept screening of a FEMA-studied stream without the effective model, as-builts or a duplicate-effective baseline.

Steps (merged):
1. Inventory supplied studies, DCR pages and models; record effective FEMA vs later local updates.
2. Reproduce the supplied source model exactly (all profiles, all XS) before edits; save as model 00.
3. Expand terrain from public USGS 1 m lidar, reproject to project state plane ft, clip to a buffer.
4. Place XS at FEMA lettered/unlettered stations; tabulate model WSEL vs effective 1% WSEL.
5. Floodway screening: set encroachment stations from effective mapped floodway lines (Method 1) on existing; hold the same stations in proposed; restrict to project reach plus approaches; derive boundaries from full polygons, clip only display linework.
6. Flag bridge low chord (road crest less assumed slab) and pier width as assumptions; use the NBI record for span, length, deck width, channel rating; request DOT as-builts / bridge hydraulic file and the effective model before Zone A/AE work.
7. Run paired existing/proposed Q100, map depth and WSEL change, publish a short screening review.
8. Keep a running scope/checkpoint file (provisional items, failures, what must not be claimed) that supersedes older status; state in the result basis that it is screening, not certification; do not block modeling on the effective model.

Gotchas:
- Lidar under water and bridge decks gives no channel bottom or low chord; expect high bias in WSEL (CALFIRE-011, claude session)
- Agent initially wanted a duplicate-effective baseline first; EOR clarified the fixed-map intent (SILVERBELL-002, claude session; EOR direction)
- First trial over all 100 intersecting XS reported a spurious 23.7 ft surcharge from disconnected polygon pieces; limiting to the project reach gave about 4 ft existing surcharge and 0.16 ft max project rise (SILVERBELL-002, claude session; EOR direction)
- Clipping FEMA floodway polygons for display before deriving boundaries broke the hydraulic areas; derive boundaries from full polygons, clip only the display linework (SILVERBELL-002, claude session; EOR direction)
- Local-peak tributary runs with iterated tailwaters are not a connected mass-conserving junction network; label results as screening (SILVERBELL-001, claude session)
- Source local model differed from FEMA effective; no no-rise or CLOMR finding can be drawn from it (SILVERBELL-001, claude session)
- Long autonomous runs need a checkpoint file that supersedes older status text, or later sessions act on stale state (SILVERBELL-001, claude session)

Jurisdiction add-ons:
- FEMA: duplicate-effective required for any Zone A/AE, no-rise or CLOMR finding (CALFIRE-011, SILVERBELL-001, SILVERBELL-002).
- Caltrans/California: bridge data from DOT as-builts and NBI record (CALFIRE-011).

QC checks:
- Lidar / local / iterated-tailwater models labelled screening; no no-rise or CLOMR finding drawn from a non-effective model.

Source cards: CALFIRE-011, SILVERBELL-002, SILVERBELL-001
Tool versions cited: CALFIRE-011: HEC-RAS 6.6 | SILVERBELL-002: HEC-RAS 1D steady, FEMA NFHL download | SILVERBELL-001: HEC-RAS (native COM and RasMapper), Python, USGS 1 m 3DEP

### HYD-C17 1D HEC-RAS networks: auto-generated regulatory wash floodplains and 1D-with-breakouts to mimic 2D
skill | new skill hecras-1d-network-build; add-on /pima-county-rfcd (Q100 >= 100 cfs regulatory washes) | score 4.5 | hours 3.75 | cards 2 | projects 2 (CAMPBELL, RKN) | confidence mixed (RKN-008 medium, CAMPBELL-007 medium; rest high)

Trigger: Floodplain mapping for every wash with Q100 >= 100 cfs on/along a project, or a 1D existing/proposed pair whose breakouts approximate a completed 2D run.

Steps (merged):
1. Confirm reach scope first (main wash only or all washes); ask before building.
2. Streams = D8 cells with contributing area giving Q100 >= 100 cfs (PC-Hydro Q-area fit); longest-path decomposition; XS every 200 ft perpendicular to smoothed centerline, width scaled to Q100; or cut XS from 2D terrain at lines where 2D face flows/stages are extracted as targets.
3. Defaults (project-specific, confirm): n 0.035 channel / 0.045 overbank; 0.3/0.1 expansion/contraction; normal-depth BCs. Bank stations at actual station/elevation points (insert interpolated points and round).
4. Extend the domain through offsite reaches where a wash leaves and re-enters so the floodplain is continuous.
5. Run headless; map Q2/Q10/Q100/Q500 by interpolating WSE between XS, keeping only inundation connected to the centerline.
6. Proposed: re-cut XS on proposed terrain, drop XS inside graded blocks or ROW, update flows from re-run CPs.
7. Breakout fitting: check corridor flows for side inflow/reentry and revise extents before fitting weir coefficients; calibrate existing only and carry coefficients to proposed; account for every lateral/storage outflow in native mass balance and report residual mismatch; compare to the last submitted scenario by structure and section, keeping floodplain cell stages separate from structure headwater.

Gotchas:
- Bank stations must be actual station/elevation points; insert interpolated points and round (RKN-008, claude session)
- Floodplain broke where a wash leaves the project and re-enters; extend the 1D domain through the offsite reach so the floodplain is continuous (existing_ext case), rerun EX and PR (RKN-008, claude session)
- Out-of-system lateral weirs cannot return flow; return flow cannot be forced without prescribing internal hydrographs (CAMPBELL-007, claude via Codex session)
- Summed negative lateral volume double counts repeated crossings; it is not a breakout volume (CAMPBELL-007, claude via Codex session)
- Native input checks needed culvert node type, deck row format, duplicate zero-volume storage rows and FV upstream energy slope (CAMPBELL-007, claude via Codex session)
- Small 1D proposed-minus-existing deltas with existing stages several ft above the 2D are not lower impacts (CAMPBELL-007, claude via Codex session)

Source cards: RKN-008, CAMPBELL-007
Tool versions cited: RKN-008: HEC-RAS 6.6 | CAMPBELL-007: HEC-RAS 6.6 1D unsteady (finite volume)

### HYD-C18 HEC-RAS 2025 beta GPU conversion limits
qc_rule | QC rule (05_QC_Rules) + note in hecras-2d-model-build tool-version table | score 20.0 | hours 5.0 | cards 1 | projects 1 (CAMPBELL) | confidence high

Trigger: Request to run an existing HEC-RAS 6.x 2D model on the GPU with the HEC-RAS 2025 beta.

Steps (merged):
1. Before converting, list structures (culverts, bridges, SA/2D connections) and inflow types (internal vs perimeter).
2. After import audit cells, terrain tables, structures, BCs, CRS; an incomplete import is not an equivalent model.
3. Run native plan preparation first (it states unsupported features); verify support there before telling the user a feature works.
4. Run a short test and confirm nonzero depths before any calibration.
5. Ask before replacing structures with culverts or terrain openings; record dimensions and losses as approximations; apply terrain changes as raster cuts and check cell minima changed.

Gotchas:
- Importer dropped bridge, culverts and boundary conditions (CAMPBELL-006, claude via Codex session)
- GPU solver rejected culvert hydraulics (5 barrels), so bridge-as-culvert also failed (CAMPBELL-006, claude via Codex session)
- Legacy terrain modifications were stored but not applied to hydraulic tables; use raster cuts and check cell minima changed (CAMPBELL-006, claude via Codex session)
- Raster sampling precedence was the reverse of the CLI help (later inputs override) (CAMPBELL-006, claude via Codex session)
- GPU initialization ignored internal inflow boundaries: 20 hr run ended OK with all depths zero (CAMPBELL-006, claude via Codex session)
- Earlier general answer that the beta supports culverts was wrong for the GPU engine; verify with native preparation before telling the user (CAMPBELL-006, claude via Codex session)

Source cards: CAMPBELL-006
Tool versions cited: CAMPBELL-006: HEC-RAS 2025 beta 0.1.0.5048-dev (GPU explicit SWE), RTX 5090

### HYD-C19 HEC-HMS scripted project build, detention routing and headless compute
skill | update skill drainage-report-build section 3 (HMS headless) + new skill hec-hms-scripted (template project + scripts); see HYD-CF-01 | score 15.6 | hours 5.3 | cards 2 | projects 2 (CALFIRE, EKOS-LOCAL) | confidence mixed (CALFIRE-008 medium; rest high)

Trigger: An HMS model (subbasins or reservoir routing of PC-Hydro DSS inflows) is needed without hand building in the GUI.

Steps (merged):
1. Start from a minimal template project shipped in the library; write .hms, .basin, .met, .gage, .control, .run text files from a parameter CSV (area, CN, lag) or stage-storage table; add basins/runs by appending blocks.
2. External inflow: GAGE_FLOW source with a Flow gage on external DSS; zero meteorology component named No Precipitation / No Evapotranspiration (generic name None gives Undefined controller errors).
3. DSS: canonical interval names (1Minute, 1Hour), INST-VAL; write, close, reopen and compare every ordinate before running.
4. Reservoir: translate all elevations and stage-storage x values by one documented basin-bottom offset (relative datum), keep absolute source values; circular outlets with Diameter, Chart, Scale, End Conduit; overflow with coefficient, top length, top elevation from native examples.
5. Check stage-storage implied area (dS/dz) against the footprint; flag jumps from connected-component masks; use the dominant connected minimum as a floor candidate only.
6. Run headless: HEC-HMS.cmd -s <script> (Project.open, computeRun, Hms.shutdownEngine); each case in an isolated project; keep per-case failures.
7. Parse results\RUN_<name>.results XML (Outflow Maximum, volume, excess); write summary and hydrograph CSVs; check each run log for unit hydrograph volume 1.0000; compute continuity from DSS storage endpoints.
8. On native error 40253 (stage above storage curve) do not extrapolate the table or enlarge storage / tune weirs to force a pass; stop re-running without new geometry.

Gotchas:
- File syntax was learned from a folder of sample projects (145 files copied to 99_Working\hms_samples); ship a minimal template project in the library instead (CALFIRE-008, claude session)
- Check each run log for unit hydrograph volume 1.0000 in notes and errors (CALFIRE-008, claude session)
- Absolute elevation 2687.90658 was saved as 2687.9, below the storage table minimum, causing an initial-pool error; relative datum fixed it (EKOS-LOCAL-009, claude session)
- Generic meteorology name None produced Undefined controller errors (EKOS-LOCAL-009, claude session)
- All 100-yr cases failed with native error 40253 (stage above storage curve); do not extrapolate the table, enlarge storage with street areas or tune weir width to force a pass (EKOS-LOCAL-009, claude session)
- Connected-component stage-storage jumped where a saddle flooded (implied 3181 m2 vs 846 m2 footprint) (EKOS-LOCAL-009, claude session)
- Lowest DEM cell was an isolated 4-cell depression; use the dominant connected minimum as a floor candidate only (EKOS-LOCAL-009, claude session)
- Repeating inlet-location sensitivity did not change the 4 failures; stop re-running without new geometry (EKOS-LOCAL-009, claude session)
- Recurrence note: 3 native HMS runs, 4 of 6 cases failed each time; 3 failed setup tasks (EKOS-LOCAL-009, claude session)

Jurisdiction add-ons:
- Pima County RFCD: inflows from PC-Hydro DSS (see skill pchydro-hydrographs).

Source cards: CALFIRE-008, EKOS-LOCAL-009
Tool versions cited: CALFIRE-008: HEC-HMS 4.13 | EKOS-LOCAL-009: HEC-HMS 4.13 (bundled Java/Jython), hms_project_diagnostic.py

### HYD-C20 HY-8 native culvert runs: file authoring, session hygiene, report export and independent check
skill | new skill hy8-native-runs (importable .hy8 writer + template + report export); update drainage-report-build section 3; add-on /caltrans (HDM Table 808.1) | score 40.5 | hours 11.5 | cards 6 | projects 5 (CALFIRE, CAMPBELL, EKOS-LOCAL, SILVERBELL, VALENCIA) | confidence high

Trigger: Report needs HY-8 native culvert output (HW, control, outlet velocity, overtopping); reproducing CulvertMaster/HY-8 cases; contractor substitution check; user-defined arch shapes.

Steps (merged):
1. Take barrel count, size, length, inverts from plan profile stations/elevations or survey (not callout text); confirm the approved analysis matches the current plan shape; ask the EOR on conflicts; rebuild a baseline with stated assumptions if none exists.
2. Compute an independent HDS-5 inlet/outlet control check (Python) first; keep it internal and labelled (see HYD-CF-07).
3. Generate INPUT .hy8 from a template saved by HY-8 itself (importable library module, not a borrowed script): catalog codes (e.g. IRREGSIZE) and material enums from the native example, never inferred; barrel data and geometry serialized in ft even when the UI shows inches; exact field keys with whitespace boundaries; CRLF; check ENDPROJECTFILE.
4. User-defined arches: solve springline and tangent point from crown/haunch radius, span, rise; integrate exact area; ~19 coordinate pairs within 0.3% area; save coordinates JSON beside the model; edit a seed crossing for repeats; note generic inlet relationships.
5. Session: kill HY864.exe before each start; File New (Ctrl+N, No) to an empty project before Open; confirm only intended crossings loaded; never save a contaminated session; keep INPUT, WORKING and NATIVE files.
6. Check every tab (tailwater type, roadway crest, inlet edge, n); Run Analysis; save the project before exporting; Create Report (Shift+End selects all crossings) to Word, then PDF, one crossing at a time if export fails; reopen NATIVE in a fresh project to confirm inputs.
7. Parse the exported report: total = barrel + roadway flow; record solver mode actually used; check cover for each alternative against the road profile.
8. Stop and reconcile if native and independent differ by more than 0.2 ft HW or 0.5 fps; compare to archived output field by field and keep differences - never adjust inputs to force a match.
9. Substitution checks: identical flow, slope, n, length, fixed tailwater from the report model; bracket entrance loss (Ke 0.2 bevel, 0.5 square); high-tailwater and full-flow (all flow through one structure) stress cases; compare HW to report existing HW; 1-page memo with native output.
10. Barrel-only checks: an artificial high road crest suppresses overtopping and does not prove zero overflow; state it.

Gotchas:
- Opening a file into a non-empty HY-8 project appends/merges its crossings into the current tree (e.g. into a prior benchmark session), producing a combined model; never save a contaminated session (CAMPBELL-013, claude session; EKOS-LOCAL-012, claude session; VALENCIA-003, claude via Codex session)
- HY-8 closing (e.g. during report export) without producing a DOCX is a failed run; retry one crossing at a time (CAMPBELL-013, claude session; EKOS-LOCAL-012, claude session)
- The .hy8 writer was borrowed from another project by exec of split source text with a hard path; move it into the library as an importable module (CALFIRE-012, claude session)
- HY-8 has no command line report; GUI automation took 9 probe scripts and about 25 min; kill HY864.exe before each start and run button invokes on threads because dialogs block (CALFIRE-012, claude session)
- Barrel dims are stored in ft even if the UI shows in (CAMPBELL-013, claude session)
- HY-8 cannot model 25 deg skew on a box inlet; note it (CAMPBELL-013, claude session)
- The 2026-09-20 agent team left HY-8 pending; native runs happened 2026-10-01 (CAMPBELL-013, claude session)
- Accessibility focus and cached modal element indexes went stale; refresh screenshot before every action (EKOS-LOCAL-012, claude session)
- Native summary showed Full Flow mode despite profile toolbar; do not call it a matched RAS profile comparison (EKOS-LOCAL-012, claude session)
- Unattended local HY-8 run was never achieved; only supervisor GUI runs worked (EKOS-LOCAL-012, claude session)
- Recurrence note: 4 (2 modal failures, 2 key-matching failures) (EKOS-LOCAL-012, claude session)
- Arch dimensions show in inches in the UI but BARRELDATA/BARRELGEOMETRY are saved in feet; first 8 concrete-arch runs were wrong and VOIDed (VALENCIA-003, claude via Codex session)
- Corrugated steel arch 50x31 in needed IRREGSIZE 1 1 1, not the code derived from the HDF; the steel-arch report run closed HY-8 with no output until fixed (VALENCIA-003, claude via Codex session)
- Material enum set wrong in a generated file (4 instead of concrete 1); corrected in UI before run (VALENCIA-003, claude via Codex session)
- HY-8 window disappeared during Word export before the post-analysis save; save the project before exporting (VALENCIA-003, claude via Codex session)
- Archive printed 4.0 ft rise while the saved model had 3.5 ft; check printed inputs vs saved model before calling a mismatch (VALENCIA-003, claude via Codex session)
- Word locks an open export DOCX; rename fails until closed, so use a VOID sidecar note (VALENCIA-003, claude via Codex session)
- Report analyzed six 12x8 ft boxes; later plan shows three 24x8 ft arches. Plan HW note repeated the old box result (SILVERBELL-014, claude via Codex session)
- Request said drainage area reduction; it was opening area per cell (about 10 sq ft each, 29-30 sq ft total) (SILVERBELL-014, claude via Codex session)
- Original flow split between two openings; also test full crossing flow through one structure (SILVERBELL-014, claude via Codex session)
- Recomputed arch area loss (10.00 sq ft) differed from contractor value (9.58); report the difference (SILVERBELL-014, claude via Codex session)
- Result was HW rise 0.45-0.50 ft, still at least 2.6 ft below existing HW (SILVERBELL-014, claude via Codex session)
- HY-8 GUI automation through dialogs was slow and fragile; text editing of a seed .hy8 file was faster (SILVERBELL-015, claude via Codex session)
- Inlet relationships for user-defined shapes are generic; note no manufacturer inlet data (SILVERBELL-015, claude via Codex session)
- LibreOffice was not available for docx rendering; Word export used for page QA (SILVERBELL-015, claude via Codex session)

Jurisdiction add-ons:
- Caltrans (HDM Table 808.1): alternatives and sensitivity flow list per HDM (CALFIRE-012).
- City of Tucson: contractor substitution memo against the approved report HW (SILVERBELL-014).

QC checks:
- HY-8 closed without a report = failed run.
- Native vs independent HDS-5 within 0.2 ft HW / 0.5 fps.

Source cards: CALFIRE-012, CAMPBELL-013, EKOS-LOCAL-012, VALENCIA-003, SILVERBELL-014, SILVERBELL-015
Tool versions cited: CALFIRE-012: HY-8 8.00; pywinauto uia backend | CAMPBELL-013: HY-8 8.00.2, Word COM | EKOS-LOCAL-012: HY-8 8.00.2 | VALENCIA-003: HY-8 8.00 | SILVERBELL-014: HY-8 8.00, Python | SILVERBELL-015: HY-8 8.00, scipy

### HYD-C21 Legacy calc reproduction: FHWA Hydraulic Toolbox inlets, Hydraflow Storm Sewers, inlet bypass routing
agent | new agent legacy-calc-reproduction (proposed; separate context, 6-10 h) + new skill legacy-calc-native-rerun (Toolbox, Hydraflow, bypass graph procedures) | score 48.5 | hours 17.0 | cards 4 | projects 1 (VALENCIA) | confidence high

Trigger: Project calcs were done in software no longer licensed (FlowMaster, CulvertMaster) or legacy .stm networks, and must be reproduced natively before revision.

Steps (merged):
1. Inventory native sources (.fm8.sqlite, .cvm, .stm, .hy8) and workbook tabs; register each case input with provenance; reproduce signed-sealed and later workbooks separately.
2. Inlets (FHWA Hydraulic Toolbox 5.5): write a generated INPUT .hyd (CURBCALC blocks) and keep it uncomputed; clear the project with New/No; open each calculation, click Compute / Compute Inlet Data, OK, Save As a separate NATIVE .hyd; enter values by individual key presses or single-value paste; Tab does not refresh results.
3. Bypass chains: read bypass links from workbook formulas (not only the summary); build a graph, sort upstream to downstream, run in that order; apply local runoff plus upstream bypass only (confined pairs: full flow to the first inlet, bypass plus verified local to the next); check flow balance at each node through to pipes/channels.
4. Storm drain (Hydraflow Storm Sewers): launch from inside Civil 3D (HHApps); copy the .stm and zero result fields in the working input; compute, save, print Inventory/Summary/HGL to PDF and export the Summary grid to text; diff source vs native line by line; record outfall tailwater per line and do not substitute earlier tailwaters without evidence.
5. Parse saved native results and compare to source values at native precision; write a comparison workbook (formulas) and native/editable file index; report invalid results (e.g. -nan capture) as INVALID, never zero, and do not invent geometry.
6. Export native reports raw; build compact one-page sheets from saved native values; record source, scenario, version, inputs, run date and differences per case.
7. Only after reproduction, copy cases and update per current plans and redlines; label superseded working copies VOID_ only when a verified replacement exists; keep independent spreadsheet checks labelled preliminary and separate.
8. Keep a continuation checklist and work-status log; do not touch HEC-RAS when scope is inlets, culverts and storm drain.

Gotchas:
- Bulk text entry into a numeric field did not change it; individual key presses or single-value paste worked (VALENCIA-001, claude via Codex session)
- Tab commits a value but does not refresh results; click Compute or the results are stale (VALENCIA-001, claude via Codex session)
- A file that loads with changed inputs is not a run; only a computed and saved native file counts (VALENCIA-001, claude via Codex session)
- Clear the project with New/No before loading another; never save computed results back over the INPUT file (VALENCIA-001, claude via Codex session)
- Zero local-depression width returned -nan(ind) capture (element 207); report INVALID, never zero, and do not invent geometry (VALENCIA-001, claude via Codex session)
- Native orifice results matched g=32.16 ft/s2 with Cd 0.67; an independent check using 32.2 differs slightly, so report the native values (VALENCIA-001, claude via Codex session)
- No CLI or API: launching with a filename argument did not load inputs; UI automation needs screenshot-based targeting of modal dialogs (VALENCIA-001, claude via Codex session)
- On reopen the Summary flow shows 0.00 and COMPUTE appears; reopening is not a rerun (VALENCIA-004, claude session)
- Program warns flow/area/C missing when Known Q is used; record it, reconcile the intended Known Q method (VALENCIA-004, claude session)
- Printed PDF is image-only; keep the Summary text export for values or OCR the PDF (VALENCIA-004, claude session)
- Inherited outlet tailwaters were much higher than outfall inverts (e.g. 2504.42 vs 2472.59 ft); flag, do not zero all tailwaters (VALENCIA-004, claude session)
- Three generated V1-V3 inputs failed before V4; keep them as VOID_ (VALENCIA-004, claude session)
- Run takes 6-10 h of agent time; needs its own context and a written continuation checklist and work status log (VALENCIA-005, claude via Codex session)
- Signed-sealed revision workbook and 100% workbook differ; reproduce each separately (VALENCIA-005, claude via Codex session)
- Saved values in a source file are not a rerun (VALENCIA-005, claude via Codex session)
- Do not touch HEC-RAS when the scope is inlets, culverts and storm drain (VALENCIA-005, claude via Codex session)
- First 72 native runs missed bypass links found later in workbook J/K formulas; all VOIDed and rerun (VALENCIA-013, claude via Codex session)
- Duplicating full flow at a downstream inlet overstated Q; use bypass only (VALENCIA-013, claude via Codex session)

Jurisdiction add-ons:
- Pima County RFCD / Pima County DOT: pavement drainage (spread, capture) reproduced in FHWA Hydraulic Toolbox (VALENCIA-001).

Source cards: VALENCIA-001, VALENCIA-004, VALENCIA-005, VALENCIA-013
Tool versions cited: VALENCIA-001: FHWA Hydraulic Toolbox 5.5 (project header 55.3) | VALENCIA-004: Hydraflow Storm Sewers (Civil 3D 2026) | VALENCIA-005: FHWA Hydraulic Toolbox 5.5; HY-8 8.00; Hydraflow Storm Sewers; Python | VALENCIA-013: FHWA Hydraulic Toolbox 5.5; Python

### HYD-C22 EPA SWMM / Autodesk SSA hydrograph models calibrated to county peak methods
skill | new skill swmm-ssa-storm-drain + jurisdiction add-on swmm-ssa-storm-drain/placer-county-ca; see HYD-CF-04 | score 121.0 | hours 13.0 | cards 2 | projects 1 (HOMEWOOD) | confidence high

Trigger: Storage, peak control or HGL must be shown with a hydrograph model while the agency peak method is rational-type (e.g. Placer County Small Watershed), and/or scripted SWMM models are handed to an engineer in SSA.

Steps (merged):
1. Compute target peaks per area for each design storm with the county method.
2. Set constant-rate infiltration (Horton f0 = fc = agency table rate), no depression storage.
3. For each storm bisect subcatchment width in log space (about 26 iterations) on a runoff-only model until the modeled peak matches target; use the geometric mean of storm-specific widths; report fit (target within 10%); calibrate pre-condition catchments separately; carry widths into all routed scenarios; plot a calibration figure.
4. Write .inp in SWMM 5.1 syntax, one file per scenario named <code>-<side>-<run>-<storm>-<condition>.
5. Import in SSA (File > Import > EPA SWMM v5.x); save each as .spf with its text report; set storage node exfiltration in Project Options and re-enter gallery/trench infiltration by hand; keep Hydrodynamic routing; set surcharge elevation and sag-inlet ponded area deliberately (Warnings 108, 139).
6. Parse SSA .rpt (Node Depth, Outfall Loading, Storage Node, continuity); compare HGL and outfall peaks with SWMM on identical inputs; report continuity with exfiltration added back; use the more conservative surcharge result.

Gotchas:
- Switching SSA hydrology between TR-55 and TR-20 never matched county peaks (50-yr 0.13 vs 0.90 cfs); calibration of width is what closes the gap (HOMEWOOD-003, claude session)
- Calibrate pre-condition catchment separately with its own target (HOMEWOOD-003, claude session)
- SSA does not transfer storage exfiltration on import; peak-control and WQ runs were wrong until set manually (HOMEWOOD-004, claude session)
- SSA routing continuity omits exfiltrated volume, so a run shows 19-48% continuity error equal to exfiltration; report it with exfiltration added back (HOMEWOOD-004, claude session)
- SSA uses older SWMM 5.1 surcharge algorithm; surcharged nodes ran 0.3-2.1 ft higher than SWMM 5.2; use the more conservative result (HOMEWOOD-004, claude session)
- Original SSA export raised Warning 108 (surcharge elev below max) and 139 (zero ponded area on sag inlets); set these deliberately (HOMEWOOD-004, claude session)

Jurisdiction add-ons:
- Placer County CA / East Placer (Lake Tahoe Basin) / TRPA: Small Watershed method targets for 10/25/100-yr; Table 5-3 infiltration rates; calibration achieved +/-4% and +/-8% (HOMEWOOD-003, HOMEWOOD-004).

Source cards: HOMEWOOD-003, HOMEWOOD-004
Tool versions cited: HOMEWOOD-003: EPA SWMM 5.2.4 via swmm-toolkit; Autodesk SSA 2024.1 | HOMEWOOD-004: Autodesk SSA 2024.1; EPA SWMM 5.2.4

### HYD-C23 Storm drain tailwater and receiving-system capacity must be defensible
qc_rule | QC rule (05_QC_Rules); jurisdiction notes Placer County CA, City of Tucson | score 4.0 | hours 3.0 | cards 2 | projects 2 (HOMEWOOD, TANGERINE) | confidence high

Trigger: A storm drain ties into a public main/street structure and HGL freeboard is checked, or a report chooses retention instead of discharging to an alley, street or storm drain.

Steps (merged):
1. Get rim, invert and HGL of the receiving structure from the agency or as-builts.
2. Run fixed tailwater and free outfall cases; report both; model and memo must state the same boundary.
3. Compare assumed tailwater with the lowest onsite rims and gallery crowns before any site runoff arrives.
4. Compare proposed peaks with receiving storm drain capacity and HGL; explain why each discharge alternative was or was not used; coordinate connection feasibility with the site designer.
5. Verify report claims (e.g. impervious area removed) against the site plan.

Gotchas:
- Tailwater set 6 in below the Fawn St grate was only 0.52-0.55 ft below the lowest onsite rims, so the lower system failed the 0.5-ft criterion before site runoff; free outfall passed (HOMEWOOD-010, claude session)
- Original model used a free outfall while the memo claimed tailwater (HOMEWOOD-010, claude session)
- Draft asserted retention without checking the storm drain and claimed impervious removal that the plan did not show (TANGERINE-025, claude session)

Jurisdiction add-ons:
- Placer County CA: 0.5-ft HGL freeboard criterion (HOMEWOOD-010).
- City of Tucson: justify retention vs discharge with storm drain capacity and HGL (TANGERINE-025).

Source cards: HOMEWOOD-010, TANGERINE-025
Tool versions cited: HOMEWOOD-010: EPA SWMM 5.2.4; SSA 2024.1

### HYD-C24 FLO-2D development effects without building footprints (ARF, IRAINBUILDING, n, CN)
skill | jurisdiction add-on flo2d-channel-build/FEMA (or section of new skill flo2d-model-build) | score 4.0 | hours 4.0 | cards 1 | projects 1 (STARVALLEY) | confidence high

Trigger: Proposed residential development must be represented in FLO-2D (FEMA asks for ARF, IRAINBUILDING, n and infiltration updates) but lot layouts are not final.

Steps (merged):
1. Measure building coverage on a comparable built block from county building footprints (buildings, lots, coverage ratio).
2. Apply ARF = WRF = measured ratio on lot cells in ARF.DAT; IWRFS = 1 in CONT.DAT; IRAINBUILDING = 1 in RAIN.DAT.
3. Classify cells from transformed lot and ROW linework (e.g. lots n 0.040, paved streets n 0.016).
4. CN on unblocked-area basis: non-roof impervious = (lot imperv - ARF)/(1 - ARF) so roof runoff is not double counted.
5. Keep FPLAIN.DAT n and elevation columns in sync with MANNINGS_N.DAT and TOPO.DAT; document every edit in a change memo and build log.

Gotchas:
- Earlier submittal carried full-imperviousness CN 93.7-95.3 plus no ARF; replaced by an ARF-compatible set (STARVALLEY-013, claude session; FEMA review comment)
- Open space lumped with ROW gives a conservatively high CN; refine if mapping is available (STARVALLEY-013, claude session; FEMA review comment)

Jurisdiction add-ons:
- FEMA Region IX / Pima County RFCD (STARVALLEY-013).

Source cards: STARVALLEY-013
Tool versions cited: STARVALLEY-013: FLO-2D Pro Build 23.10.25 and 26.02.25, TR-55

### HYD-C25 Collector channels, outlets and culverts in sediment-laden piedmont / alluvial areas
qc_rule | QC rules (05_QC_Rules); jurisdiction add-on drainage-report-build/town-of-marana and /town-of-sahuarita | score 7.0 | hours 4.0 | cards 4 | projects 2 (NORTHLOOP, SAHPARK) | confidence mixed (NORTHLOOP-014 medium, NORTHLOOP-016 medium, SAHPARK-020 medium; rest high)

Trigger: Sizing a collector/diversion channel around a pad or a new culvert crossing in an alluvial sheet-flow / distributary piedmont area.

Steps (merged):
1. Size the collector for the combined flow of all intercepted paths; required depth = normal depth + freeboard; check superelevation at each bend from radius; screen bank height with a conservative case (2 x normal depth or summed peaks); check transitions, lateral inflow capture and basin backwater.
2. Lining: do not default to riprap where sediment load is high; evaluate concrete/shotcrete; state lining in the channel table (earthen n = 0.025 only if unlined); include sediment maintenance access and cleanout.
3. Outlet: level spreader basin where a collector returns flow to natural ground; compare existing vs proposed outlet hydrograph split by domain exit.
4. Culverts: outlet velocity and outlet protection per HEC-14 (at 9-13 fps a dumped riprap apron alone is not enough); inlet/outlet channel inverts at or below the box invert; note sediment risk for perpendicular alignments; cutoff walls for 100-yr scour plus long-term degradation; plan HEC-18/HEC-20 scour for final design; state overtopping vs 100-yr depth criterion with margin and check sensitivity to weir length.
5. Use survey or as-built culvert sizes, not concept markup sizes.

Gotchas:
- EOR callout on the 2021 concept: riprap may not suit the sediment load, consider concrete or shotcrete; later plans used 6 in shotcrete (NORTHLOOP-014, claude session; EOR redline)
- Candidate 8-ft north bank was below the 8.71-ft depth from the conservative summed 500-yr flow; bank height had to be revisited (NORTHLOOP-015, claude session; EOR redline)
- EOR callout: flow all around to the north at about 1,945 cfs, 49 in depth + 2 ft freeboard, verify superelevation by radius (NORTHLOOP-015, claude session; EOR redline)
- EOR markup called for a level spreader basin; the response log kept it open pending disposition (NORTHLOOP-016, claude session; EOR redline)
- Draft had no outlet protection or scour content; 100-yr overtopping criterion was met with no margin (SAHPARK-020, claude session; EOR redline)
- Shortest culvert alignment was perpendicular to flow - sediment maintenance may cancel the cost saving (SAHPARK-020, claude session; EOR redline)

Jurisdiction add-ons:
- Town of Marana: collector channel freeboard 2 ft; EOR callouts on lining and level spreader (NORTHLOOP-014, -015, -016); City of Tucson collector channel provisions where adopted (NORTHLOOP-015).
- Town of Sahuarita / Pima County RFCD: cutoff walls per local Development Criteria (SAHPARK-020).

Source cards: NORTHLOOP-014, NORTHLOOP-015, NORTHLOOP-016, SAHPARK-020
Tool versions cited: NORTHLOOP-015: Manning normal depth screen (Python) | NORTHLOOP-016: FLO-2D Pro | SAHPARK-020: CulvertMaster 10.3, FHWA HDS-5, HEC-14

### HYD-C26 Hydraulic calc deliverables: native program output for the selected design, standard software, one-page printouts
qc_rule | Standard v0.3 change (appendix rules) + QC rule; see HYD-CF-06/07 | score 6.0 | hours 4.0 | cards 2 | projects 1 (SAHPARK) | confidence high

Trigger: Culvert, channel or routine hydraulic calcs go into a report appendix.

Steps (merged):
1. Once plans show a selected design, run that design (size, count, inverts, length from plans, project datum inverts - not an arbitrary 100 ft datum) and insert the native output sheets; drop option-comparison tables. If options are still open, include calc sheets for each option, not only a summary.
2. Use standard hydraulic software (FlowMaster or Civil 3D hydraulic tools for normal depth; CulvertMaster or HY-8 for culverts; HEC-RAS for the system) or a named existing office spreadsheet; do not create a new spreadsheet the reviewer must check.
3. Set print areas so every output sheet plots on one page.

Gotchas:
- Draft appendix had only an options summary table on an arbitrary datum while the plans already showed a 3 - 10x4 ft RCBC (SAHPARK-012, claude session; EOR redline)
- Custom normal depth spreadsheets with an undocumented geometry sketch added review time and were removed (SAHPARK-013, claude session; EOR redline)

Note: Recurrence for these cards counts individual redline comments.

Source cards: SAHPARK-012, SAHPARK-013
Tool versions cited: SAHPARK-012: CulvertMaster 10.3, HY-8 | SAHPARK-013: FlowMaster, CulvertMaster 10.3, HY-8, HEC-RAS 7.00

### HYD-C27 Concept drainage report framing: crossings, path continuity, alternatives and client decisions up front
qc_rule | agent report-writer checklist + Standard v0.3 change (concept report intro); add-ons Town of Marana, Town of Sahuarita | score 19.0 | hours 3.0 | cards 2 | projects 2 (BARNETT, PHXZOO) | confidence mixed (PHXZOO-005 medium; rest high)

Trigger: Concept reports for channels with multi-use paths crossing roads/freeways/railroads, or conceptual drainage for a site crossed by a large offsite wash.

Steps (merged):
1. State in the introduction whether a path is continuous under major crossings (freeway, railroad) or ends at them, and the crossing type at each road (at grade, under, con-arch).
2. For each existing crossing structure state whether it stays, is adequate or is replaced.
3. Lay out offsite conveyance alternatives and count road crossings for each; prefer one consolidated crossing; compare culvert cells for 10-yr vs 100-yr capacity.
4. In alternatives note bank-protection options (e.g. geosynthetics on 4:1 vegetated slopes), precast vs cast-in-place culvert extensions, basin or spreader options at overchutes; terraced channel option (10-yr low-flow channel, 100-yr terrace outside sensitive areas).
5. Describe flow paths in downstream order.
6. Get written client decisions on level of protection (100-yr vs 500-yr), onsite containment requirements and acceptance of controlled flooding; a designed overflow onto the site needs agency buy-in.
7. Check grates/bar racks at fence crossings for headloss and debris; list next deliverables after decisions.

Gotchas:
- Reviewer read 41 of 48 pages before learning the path was claimed continuous under I-10 and UPRR; Development Engineering asked for the trail to stop at I-10 or explain the crossing (BARNETT-011, claude session; agency review comments + redlines)
- A designed overflow onto the site creates a second floodplain path and conflicts with matching existing peak Q and floodplain at the property boundary; needs Town and PCRFCD buy-in (PHXZOO-005, claude session)
- Double chain-link fencing passes stormwater freely, which removed the pipe-escape concern only because no pipes leave the enclosures (PHXZOO-005, claude session)

Jurisdiction add-ons:
- Town of Marana: Development Engineering asks for trail termination or crossing explanation at I-10/UPRR (BARNETT-011).
- Town of Sahuarita / Pima County RFCD: overflow onto site conflicts with matching existing peak Q and floodplain at the property boundary (PHXZOO-005).

Note: BARNETT-011 recurrence (9) counts individual reviewer/redline comments.

Source cards: BARNETT-011, PHXZOO-005
Tool versions cited: PHXZOO-005: HY-8, CulvertMaster, FlowMaster, optional HEC-RAS 1D/2D

### HYD-C28 FLO-2D road drainage alternative screening loop
agent | agent model-run-supervisor (screening-loop mode) + new skill flo2d-alternative-screening; add-on /town-of-sahuarita | score 24.0 | hours 3.0 | cards 1 | projects 1 (SAH) | confidence high

Trigger: Several culvert, collector and berm-removal layouts must be compared against existing 100-yr road depths.

Steps (merged):
1. Draw alternative elements in one layout file (collector, outlet channel, culvert, berm removal, sag fill) and summarize them.
2. Size culverts from screening flows into a sizing CSV per trial.
3. Build a LOWER-only proposed model from the existing LOWER folder (same nested inflow): lower cells to graded inverts, add HYSTRUC box culverts, remove levee directions near removed berms.
4. Run LOWER-only (0.75-1.5 h each at 8 threads) through a job table, not hand-written stream files.
5. Report max lane depth, 500-ft reaches over 1 ft and 0.5 ft, buildings with depth > 0.5 ft and with increase > 0.1 ft.
6. Pick the next trial from hot spots; repeat; carry the selected run into tables and exhibits; test every design storm (3-hr and 24-hr) on the recommended layout.

Gotchas:
- Eight alternatives (P1 to P8) and four sizing trials were run in about 12 h; each was a new hand-written stream file (SAH-011, claude session)
- P4 and P5 at 4 threads took 1.5 h each versus 0.8 h at 8 threads (SAH-011, claude session)
- Only the 3-hr 100-yr storm was tested; the 24-hr storm was not checked for the recommended layout (SAH-011, claude session)

Jurisdiction add-ons:
- Town of Sahuarita: 12 in all-weather access; Pima County Roadway Design Manual: 1 ft in paved section (SAH-011).

Source cards: SAH-011
Tool versions cited: SAH-011: FLO-2D Pro Build 26.02.25
