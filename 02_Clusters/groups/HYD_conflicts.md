# HYD conflicts (hydraulics model build and run)

Real disagreements between cards, or between cards and existing skills. Jurisdiction differences are handled as add-ons in HYD.md and are not listed here.

1. **HYD-CF-01 HEC-HMS version and meteorology for gage-flow inflows** (HYD-C19)
   - Side A: drainage-report-build section 3 - "HEC-HMS 4.12 headless ... Source Flow Method GAGE_FLOW from DSS; met model Specified Average with Use Basin Model lines".
   - Side B: CALFIRE-008, EKOS-LOCAL-009 - HEC-HMS 4.13; EKOS-LOCAL-009 uses GAGE_FLOW with a zero meteorology component named No Precipitation / No Evapotranspiration (a generic name None gave Undefined controller errors).
   - Why it matters: the skill pins an older version and a different met setup; scripts written to one may fail on the other. Decide the library HMS version and which met-model pattern is standard for external-inflow routing.

2. **HYD-CF-02 Can HY-8 be run unattended by UI automation?** (HYD-C20)
   - Side A: drainage-report-build section 3 - "HY-8 8.00: drive with Windows UI automation (Run Analysis -> Export Report -> Word)". CALFIRE-012 - report export via pywinauto worked (after 9 probe scripts, about 25 min).
   - Side B: EKOS-LOCAL-012 - "Unattended local HY-8 run was never achieved; only supervisor GUI runs worked"; stale accessibility focus and modal indexes. SILVERBELL-015 - GUI automation slow and fragile; text editing a seed .hy8 was faster. CAMPBELL-013 / VALENCIA-003 - export can close HY-8 with no DOCX.
   - Why it matters: decides whether HY-8 runs belong to an unattended agent or require a supervised (human-visible) step, and how much time to budget.

3. **HYD-CF-03 How to author .hy8 input files** (HYD-C20)
   - Side A: CALFIRE-012 - write the .hy8 text file (CRLF) directly with a writer script (borrowed from another project).
   - Side B: EKOS-LOCAL-012, VALENCIA-003 - start from a file saved by HY-8 itself; take catalog codes (IRREGSIZE etc.) and material enums from it, never infer (wrong codes / units gave 8 VOIDed arch runs and a crash).
   - Why it matters: the library writer must be template-driven; a from-scratch writer reproduces the unit and catalog-code failures.

4. **HYD-CF-04 Role of EPA SWMM** (HYD-C22)
   - Side A: drainage-report-build section 3 and drainage-report-exhibit-standards section 4 - "EPA SWMM as an independent check only".
   - Side B: HOMEWOOD-003, HOMEWOOD-004, HOMEWOOD-010 - SWMM (handed to Autodesk SSA) is the primary hydrograph / HGL model for storage, peak control and freeboard, calibrated to the county peak method.
   - Why it matters: the existing skill text reads as library-wide. Scope it to AZ jurisdictions (PC-Hydro/HMS primary) and put SWMM/SSA-primary practice in the Placer County CA add-on.

5. **HYD-CF-05 FLO-2D run completion criterion** (HYD-C01, HYD-C02)
   - Side A: STARVALLEY-019 - "Declare success only on exit code 0, native termination, complete outputs and no TMP files".
   - Side B: NORTHLOOP-007 - with build 26.02.25 the solver kept running after termination; the supervisor must poll and terminate it ("never block on process exit"); SAH-004 - complete when SUMMARY.OUT has COMPUTER RUN TIME, then confirm the process exited; FLOPRO keeps result files open.
   - Why it matters: a terminated process returns a non-zero code, so the exit-code rule would mark good runs as failed (or the supervisor waits forever). Standard should be: termination line + outputs + no TMP; exit code recorded but not required.

6. **HYD-CF-06 Which software to use for routine channel/culvert calcs** (HYD-C26, HYD-C21)
   - Side A: SAHPARK-013 (EOR redline) - use FlowMaster (or Civil 3D hydraulic tools) for normal depth, CulvertMaster or HY-8 for culverts.
   - Side B: VALENCIA-005 / VALENCIA-001 - FlowMaster and CulvertMaster are no longer licensed; legacy calcs are reproduced in FHWA Hydraulic Toolbox and HY-8.
   - Why it matters: the deliverable rule names tools that may not be available. Standard v0.3 should list the currently licensed set (FHWA Hydraulic Toolbox, HY-8, Civil 3D hydraulic tools, HEC-RAS) and treat FlowMaster/CulvertMaster as legacy.

7. **HYD-CF-07 Independent spreadsheet/Python checks vs "no new spreadsheet"** (HYD-C20, HYD-C26)
   - Side A: SAHPARK-013 - do not build a new spreadsheet the reviewer must check; custom normal-depth spreadsheets were removed.
   - Side B: CALFIRE-012, CAMPBELL-013 - run an independent HDS-5 check in a spreadsheet / Python and reconcile within 0.2 ft HW / 0.5 fps; VALENCIA-005 - keep independent spreadsheet checks labelled preliminary and separate.
   - Why it matters: both can hold if independent checks are internal QC (40_QC) and never appear in the deliverable; the rule needs that wording or agents will either drop the check or ship the spreadsheet.

8. **HYD-CF-08 Uniform Manning n in 2D models** (HYD-C11)
   - Side A: ELTORO-004 - keep uniform n = 0.035 to match the accepted model; changing it breaks comparability.
   - Side B: TANGERINE-005 (agency review comments) - spatially varied n from land cover is expected; uniform 0.035 accepted only for feasibility.
   - Why it matters: the library needs a rule for when an extended/reused model may keep uniform n (comparability with an accepted study) versus when reviewers will reject it (concept/master report).

9. **HYD-CF-09 Volume-error acceptance thresholds** (HYD-C01, HYD-C09, HYD-C11)
   - NORTHLOOP-007: FLO-2D volume error <= 0.1%.
   - SILVERBELL-018: gate next RAS run on volume error "0.5 pct or less".
   - SILVERBELL-005: proposed RAS run at 0.25% volume error rejected because of 3,520 iteration warnings and 17.1 ft max WSEL error.
   - CAMPBELL-001: 0.07% accepted only with residual and end-time checks.
   - Why it matters: one numeric gate in the supervisor would pass runs another card rejects. Set per-engine thresholds and require max WSEL residual / iteration warnings alongside volume error.

10. **HYD-CF-10 How to launch HEC-RAS headless** (HYD-C10, HYD-C11, HYD-C01)
    - RKN-007: Ras.exe -c <prj> <plan> -hideCompute works; judge by HDF.
    - SAH-009: Ras.exe -c plus a dialog watcher (already-running instance dialog); ras-commander compute_plan first attempt produced no result.
    - CALFIRE-009: ras_commander compute_plan reported FAILED on 3 of 4 plans; watchdog runs RasUnsteady.exe directly on p##.tmp.hdf.
    - EKOS-LOCAL-010: command-line runs gave no output within 90 s; COM (RAS66.HECRASController) fallback worked. CAMPBELL-004: COM preprocess then RasUnsteady.
    - Why it matters: the supervisor needs one primary launch path and a defined fallback order; current cards each recommend a different primary.

11. **HYD-CF-11 Concurrency limit for FLO-2D solvers** (HYD-C01, HYD-C28)
    - NORTHLOOP-007: at most two solvers at once, 8 threads each.
    - SAH-001: three FLO-2D affinity streams (8/8/4 threads) plus HEC-RAS on 12 cores on the same 32-thread machine; SAH-011: 4-thread runs took 1.5 h vs 0.8 h at 8.
    - STARVALLEY-019: Windows AppHang closed two runs at sim hour 7.7; restarts with fewer threads were needed.
    - Why it matters: workstation scheduling rule for the supervisor; needs a benchmark-based limit for the EKOS workstation.

12. **HYD-CF-12 Auto-answering FLO-2D Warning dialogs** (HYD-C02, HYD-C01)
    - Side A: SAH-004 - watcher posts Enter to any Warning dialog and logs the text so the run does not wait.
    - Side B: NORTHLOOP-007 - on any stop preserve, log and notify; do not report queued steps as done (implies warnings are a decision point).
    - Why it matters: blind acceptance can hide input errors. Rule should classify warnings (known benign list auto-answered; others stop and notify).

13. **HYD-CF-13 Heartbeat / notification cadence** (HYD-C01)
    - CAMPBELL-005: about 100 half-hour heartbeats still left the user asking for status 15 times; stay quiet, notify only on completion/failure/decision, publish one status file.
    - SILVERBELL-018: heartbeat every 15 min.
    - Why it matters: agent spec needs one policy (status file updated each poll; user notifications only on events).

14. **HYD-CF-14 hecras-result-rasters terrain handling and default grid** (HYD-C14)
    - Side A: hecras-result-rasters SKILL.md - engine auto-detects "the scenario terrain the plan actually used" (geometry Terrain Filename); depth = max WSE - terrain; default 10 ft grid.
    - Side B: DLR-006 - the script resolves the terrain name to a .vrt/.tif by basename only and does not see terrain modifications stored only in a terrain HDF; flat per-cell WSE gives stepped depth vs RAS Mapper sloped surface. RKN-009 exports at 3 ft.
    - Why it matters: the skill overstates terrain fidelity; scenario terrains with HDF-only modifications would give wrong depths. Skill should warn and require the RAS Mapper spot check.

15. **HYD-CF-15 Earthen channel n = 0.025 vs natural wash n** (HYD-C17, HYD-C25)
    - Side A: drainage-report-build / exhibit-standards section 1 - "Earthen channels n = 0.025".
    - Side B: RKN-008 - natural wash channel n 0.035, overbank 0.045; ELTORO-004 / TANGERINE-005 - 0.030-0.050 for washes and desert scrub; NORTHLOOP-014 - 0.025 only if unlined constructed channel.
    - Why it matters: the skill rule should say "constructed unlined earthen channels"; applied to natural washes it would be non-conservative.

16. **HYD-CF-16 FLO-2D engine build standard** (HYD-C04)
    - Side A: NORTHLOOP-008 - Town of Marana manual names build 17.08.17, which fails at startup (War30.bac) on this workstation.
    - Side B: NORTHLOOP-008, STARVALLEY-010, STARVALLEY-011, SAH-001 - build 26.02.25 adopted and runs; 23.10.25 stalled.
    - Why it matters: tool-version table in the library must record the agency-named build and the working build, with an agency-acceptance step whenever they differ.
