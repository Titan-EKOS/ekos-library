# HJR conflicts (hydrology + jurisdiction rules)

Real disagreements only. Jurisdiction-to-jurisdiction differences are add-ons (see HJR.md structure table), not listed here.

1. PC-Hydro terms-of-use acceptance (HJR-C01)
   - Side A: pchydro-hydrographs Operating rules and reference/pchydro_web_workflow.md step 2 - accepting "I Agree" is an explicit-permission action; ask the user every time.
   - Side B: EKOS-LOCAL-006 - terms approval is standing for PC-Hydro; record it, do not ask again. RKN-004 and SAH-007 batch scripts click I Agree automatically.
   - Why it matters: batch and unattended runs (model-run-supervisor) cannot stop for a prompt per session; the skill needs one rule (e.g., owner approval recorded once per project in the run log).

2. PC-Hydro run mode: headless vs Claude in Chrome only (HJR-C01)
   - Side A: pchydro-hydrographs Operating rules - "The web app requires Claude in Chrome ... It cannot be driven headlessly"; keep the window still.
   - Side B: RKN-004 (Playwright, Edge headless, file-input route), SAH-007 (Playwright, page functions and pdf.php/hydrograph.php posts, 67 subbasins in about 25 min), EKOS-LOCAL-006 (Edge isolated browser adapter).
   - Why it matters: the existing skill excludes the path that worked at scale; the skill should carry both modes and pick by CP count.

3. Which PC-Hydro series and peak go downstream (HJR-C03)
   - Side A: pchydro-hydrographs Phase 3 - compare the Peaks sheet to report peaks and resolve discrepancies before DSS; scripts/hydrographs_to_xlsx.py takes peak = max(sampled ordinates). drainage-report-build Sec. 3 - save program hydrographs "(not replicas)".
   - Side B: EKOS-LOCAL-007 - sampled maximum will differ from the reported peak; keep native export unchanged and make a separate peak-adjusted copy (max ordinate replaced by reported peak, tail closed to zero) for routing, with logged added volume; do not apply a volume-equality gate.
   - Why it matters: Side A will flag every 1-min export as a mismatch, and is silent on whether the native or adjusted series goes into DSS/RAS/HMS; "not replicas" can be read as prohibiting the adjusted copy. Decide: native retained as record, adjusted copy used for routing, script reports both peaks.

4. PC-Hydro vegetation default on graded ground (HJR-C04)
   - Side A: drainage-report-build Sec. 3 - leave the PC-Hydro default cover (Auto-fill Default Veg %) for all conditions including graded ground.
   - Side B: NORTHLOOP-013 - "keep PC-Hydro 20% default for graded ground", replacing an older saved 5% Desert Brush rule (still present in some saved standards). SAH-007 - default densities had to be probed from the live page; confirm they match the PC-Hydro guide before a batch.
   - Why it matters: if auto-fill varies by cover type, a hard-coded 20% in scripts or .pk6 builders (RKN-003, SAH-007) would contradict the "program default" rule. Confirm whether 20% is the auto-fill value for graded ground in 7.4 and purge the 5% rule from all saved standards.

5. Rainfall source in .pk6: script-written depths vs native fetch (HJR-C01, HJR-C02)
   - Side A: RKN-003 and SAH-007 - write Atlas 14 upper 90% depths at the centroid into each .pk6 from GIS/PFDS.
   - Side B: EKOS-LOCAL-006 and RKN-004 - use the in-app Fetch Rainfall (wait for Matches), compare to saved Atlas 14 arrays at 2 decimals; direct HTTP fetch returns 403; record the edition actually served (guide cites an older edition).
   - Why it matters: if the native fetch overwrites script values, the written depths are unchecked; if it does not, the run may use a different edition than the program. Rule should be: native fetch governs, script values used only as the comparison array.

6. HEC-HMS version standard (HJR-C05, HJR-C18)
   - Side A: drainage-report-build Sec. 3 - HEC-HMS 4.12 headless. RKN-006 - 4.12 is the standard; use of 4.13 logged as an EOR decision item.
   - Side B: SAH-008, CALFIRE-006, CALFIRE-007, EKOS-LOCAL-007, EKOS-LOCAL-015 - all ran 4.13. CAMPBELL-012 - opening a 4.12 project in 4.13 upgrades it (work on copies).
   - Why it matters: upgrade is one-way; reviewers reproducing results need the stated version; the skill should name one standard (or "4.13, upgraded copies, version stated in report") and the decision log entry.

7. Critical facility 500-yr WSE source (HJR-C12)
   - Side A: drainage-report-build Sec. 1 and drainage-report-exhibit-standards (Critical facilities line) - pull the 0.2% WSEL from the FIS profile at the upstream and downstream cross sections.
   - Side B: NORTHLOOP-010 - use the FIS 0.2% profile only if its sections bracket the site (nearest section 1,848 ft away could not be used); Zone AO depth/velocity is not an absolute 500-yr elevation; 1.75 x Q100 is provisional sensitivity only, agency 500-yr hydrology required. PHXZOO-002 - Q500 not published for LMW; ratio method needs written client agreement or extra scope.
   - Why it matters: Side A applied literally gives an unsupported elevation on sites away from studied reaches or in AO zones. Core rule needs the bracketing test and fallback order.

8. Watershed exhibit contour interval (HJR-C07)
   - Side A: drainage-report-exhibit-standards (Contours) - 1-ft for small onsite projects; otherwise 2-ft or other chosen by scale.
   - Side B: TANGERINE-023 - 1-ft contours minimum, 0.5-ft on flat sites, for watershed exhibits.
   - Why it matters: 2-ft contours on a flat site cannot support ridge-line boundaries the reviewer asked for; exhibit standard needs a minimum and a flat-site rule.

9. FLO-2D build for Town of Marana work (HJR-C12)
   - Side A: NORTHLOOP-003 citing Marana Drainage Manual (Sep 2024) 4.5 - FLO-2D Pro build 17.08.17 for the regional (TAFS) model.
   - Side B: NORTHLOOP-003 (runs moved to build 26.02.25 after a startup failure; archived outputs at 19.07.21 and 21.08.23), STARVALLEY-017 and STARVALLEY-022 (26.02.25 used on FEMA work).
   - Why it matters: Marana add-on must state whether the manual build is mandatory or a newer build is accepted with Town concurrence; affects reproducibility of regional results. (Cross-group: hydraulics owns FLO-2D.)

10. Untested infiltration rate: required rate vs assumed rate (HJR-C09, HJR-C16)
   - Side A: drainage-report-build Sec. 1 - if no tested rate, state the required field rate and that testing is required. RKN-016 - required rate = 9 in x FS 2.0 / drawdown limit.
   - Side B: HOMEWOOD-009 - until tested, use half the NRCS rate (1.0 in/hr) with a 0 in/hr sensitivity.
   - Why it matters: the core skill states Side A as a universal content rule; if Placer reviewers expect Side B, the core rule must be moved to the Pima add-on and the core reduced to "state basis and testing requirement". May resolve as an add-on split once confirmed.

11. Regional flows in Town of Marana design basis (HJR-C10, HJR-C12)
   - Side A: NORTHLOOP-003 citing MDM 4.1 - non-regional discharges are used for design and onsite PC-Hydro; regional results serve FEMA purposes.
   - Side B: BARNETT-006 - design basis carries both "10-yr regional" and "100-yr local" flows (reviewer asked for consistent qualifiers, not removal of regional flows).
   - Why it matters: possible misreading of MDM 4.1 (or a linear-park/channel case where regional flows legitimately size the facility). Confirm the rule wording for the Marana add-on before it is written as absolute.

12. East Placer water quality depth: 1.2 in vs 0.9 in at about 6,300 ft (HJR-C15, HJR-C16)
   - Side A: HOMEWOOD-002 and HOMEWOOD-008 step 3 - 85th percentile 24-hr depth is 1.2 in at 6,000-6,500 ft; scale the 2-yr storm shape to it.
   - Side B: HOMEWOOD-008 gotcha - SWQP template at about 6,300 ft gives 0.9 in "unit WQV" (1.0 in at 6,600 ft).
   - Why it matters: the difference is probably runoff coefficient applied inside the template (WQV = imp area x C x unit depth), but the cards do not say so; the add-on must state which number is rainfall depth and which is runoff depth to avoid repeating the 1.3 in error.
