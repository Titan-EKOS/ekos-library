# QC group - conflicts

1. HEC-HMS version
   - Skill side: drainage-report-build sec. 3 specifies "HEC-HMS 4.12 headless".
   - Card side: CALFIRE-015 and CAMPBELL-014 work in HEC-HMS 4.13; EKOS-LOCAL-011 qualified the HMS connector on 4.13; RKN-018 lists "HMS 4.13 vs 4.12" as a deviation needing an EOR decision.
   - Why it matters: the version on native printouts must match the version stated in the report (C07, ELTORO-010 rule), and the connector benchmarks are tied to one build. Decide the library's current version and update the skill.

2. Native-output appendix: extracted summaries allowed or not
   - Skill side: drainage-report-build sec. 3 and drainage-report-exhibit-standards sec. 4: native program printouts, "no replicas", not recreated tables.
   - Card side: CALFIRE-015 allows results extracted from XML/HDF to a text PDF if titled "extracted summary" and the program file is kept in the record.
   - Why it matters: decides whether HMS/RAS results that cannot be printed natively may appear in the native-output appendix at all, and what the checklist may mark Addressed.

3. Direction of authority in the PC-Hydro peak check
   - Skill side: pchydro-hydrographs operating rules / Phase 3: QC site peaks against the report's stated peaks and flag mismatches (report treated as reference; no tolerance stated).
   - Card side: RKN-005: native PC-Hydro output is the reference; report Q must match it with max abs diff 0.0 cfs; record the table in the QC document.
   - Why it matters: for a rebuild from an old report the report is the target; for a new report the native output governs. The skill should say which applies and state the 0.0 cfs tolerance.

4. Drainage map CP labeling
   - Skill side: drainage-report-exhibit-standards sec. 3: CP descriptive attributes live in the shapefile; maps show only node letters (A, B, C); node table goes in the report.
   - Card side: RKN-013: CP symbols by type and watershed labels with CP number and Q100 on the map.
   - Why it matters: exhibit-reviewer will flag one or the other as a defect. Decide whether Q100 labels on maps are standard or project-specific.

5. Checklist / comment status vocabulary
   - CALFIRE-016: Addressed / Partial / Assumed.
   - BARNETT-001: Addressed / Partially Addressed / Not Addressed / Cannot Determine.
   - STARVALLEY-005: addressed with file evidence / done but not run / not done / stale / new.
   - BARNETT-002 / SAHPARK-017 dispositions: incorporated / superseded / no change - comment noted.
   - Why it matters: one log template (comment-response-log skill, Standard v0.3 QC_Log) needs one controlled list; mixed terms make status counts and gates unreliable. Proposed: separate "status" (Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale) from "disposition" (incorporated / superseded / no change).

6. Where open items are listed when a draft issues with items open
   - Skill side: drainage-report-build sec. 4: "open items listed" before submittable (location not set).
   - VALENCIA-011: do not compile while items are open unless the EOR authorizes it; then a separate unresolved-items document.
   - SAH-013: close or list every WARN/placeholder/decision in the transmittal; keep them listed in _ASSEMBLY_REPORT.md.
   - RKN-018: numbered open items in the QC open-items / EOR checklist document.
   - Why it matters: three different homes for the same list; Standard v0.3 should name one (proposed: QC open-items document, referenced in the transmittal) and make compile blocking the default.

7. Standard v0.3 post-process hides open items
   - Standard side: s60 docx post-process deletes leftover placeholder paragraphs; assembler treats PROJECT-TEXT as one entry per report.
   - Card side: SAH-013: deleting placeholders hides open items in the docx; PROJECT-TEXT lookup failed and duplicated text in later sections.
   - Why it matters: the assembly gate can pass a draft with unresolved content. Standard v0.3 change needed (keep placeholders flagged until the assembly report shows them closed; fix PROJECT-TEXT handling).

8. CMP gallery groundwater separation (East Placer)
   - HOMEWOOD-017: worked example uses 2 ft separation (7.17 ft for 36 in), then says "redo with 5 ft separation if East Placer rule governs".
   - Why it matters: 3 ft difference in required FG-to-SHGW depth changes gallery feasibility; the Placer add-on cannot be written until the governing value is confirmed from the East Placer manual.

9. Exhibit production tool
   - Skill side: drainage-report-build sec. 3: QGIS layouts exported headless.
   - Card side: RKN-018 (and RKN-013 patching) produced exhibits with Python and lists "Python exhibits vs QGIS" as a deviation for EOR decision.
   - Why it matters: if Python exhibits are acceptable the skill should allow them with the same symbology checks; otherwise they must be flagged every time.

10. Change one diagnostic control at a time vs combined setting changes (minor, practice)
   - CAMPBELL-002: change one control at a time; combined coupling-iteration + BC volume-check change caused 99.99 pct inflow loss.
   - No library skill currently covers RAS 1D/2D volume diagnostics; hecras-result-rasters step 4 only says "sanity-check magnitudes". Not a disagreement, but the existing skill would export rasters from a run that fails the 0.1 pct volume rule; add a volume-accounting pre-check.

Not conflicts (noted for completeness):
- HOMEWOOD-007 (WQV below lowest outlet; raise outlet or add weir plate) agrees with skill rule "first flush below the outlet invert; raise the outlet".
- ELTORO-012 / VALENCIA-019 (freeboard shown separately from normal depth) agree with skill "required depth = normal depth + freeboard vs provided".
- VALENCIA-021 table borders/centering agree with skill sec. 2.
- ELTORO-013 (model files and reference excerpts with the report) is a gap in skill sec. 4 deliverables, not a disagreement.
- Placer County values (HOMEWOOD-006/007/014/017) vs Pima County practice are jurisdiction add-ons.
