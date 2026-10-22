# EXH conflicts

Real disagreements between cards, or between a card and an existing skill. Jurisdiction-only differences are handled as add-ons in EXH.md and are not listed here.

1. EXH-X01 Default depth class breaks (both Pima County RFCD area)
   - Side A: 0-0.2 ft not displayed, 0.21-0.50 yellow, 0.51-1.00 cyan, 1.01-2.00 blue, 2.01-3.00 orange, >3 ft red. (SAHPARK-006, JCO QC redline)
   - Side B: depth classes 0-3, 3-5, 5-10, >10 ft. (CAMPBELL-018, JCO QC redline)
   - Existing skills: drainage-report-exhibit-standards and hecras-result-rasters are silent on depth classes.
   - Why it matters: an exhibit script needs one default ramp. Likely scale-driven (local sheet flow vs regional wash/roadway corridor); EOR should set a default plus a "deep-flow" alternate and the rule for choosing. Clusters: EXH-C07.

2. EXH-X02 Minimum depth shown / wet threshold
   - 0.2 ft not displayed on depth maps. (SAHPARK-006)
   - Depths below 0.1 ft masked on FLO-2D maps. (TANGERINE-008)
   - Difference values under 0.10 ft turned off on impact maps when asked. (CAMPBELL-016)
   - hecras-result-rasters (Method notes / script WET = 0.01): one wet mask depth > 0.01 ft applied to all three rasters.
   - Why it matters: raster wet mask and display threshold are different settings but are not separated anywhere; WSE extents, inundated acreage and legend bottom class change with the value. Standard should state both (data mask vs display cutoff) and the default for each.

3. EXH-X03 Class-bound notation: continuous vs discrete
   - Continuous bounds (0-0.10, 0.10-0.25, ...). (CAMPBELL-016)
   - Discrete bounds (0.21-0.50, 0.51-1.00, 1.01-2.00). (SAHPARK-006)
   - Why it matters: discrete bounds leave gaps (e.g., 0.20-0.21 ft) against a continuous raster, so some cells fall in no class; the legend rule "define all intervals" needs one convention.

4. EXH-X04 Minimum text size on exhibits
   - 0.1 in minimum (= 7.2 pt). (drainage-report-exhibit-standards §3; RKN-012)
   - 9 pt minimum for new text. (NORTHLOOP-011, EOR instruction)
   - Why it matters: different pass/fail threshold for the exhibit-reviewer; 9 pt is stricter.

5. EXH-X05 Aerial on location maps
   - drainage-report-exhibit-standards §3: full-size figures have full aerial coverage of the sheet.
   - Location map: about 1 in = 3 mi from design plans, no aerial or FEMA layers, with township-section-range. (TANGERINE-022, JCO QC redline)
   - Why it matters: the location/vicinity figure is in the standard figure series; the standard needs an explicit exception or the reviewer will flag one or the other.

6. EXH-X06 Sheet size
   - drainage-report-exhibit-standards §3: 11x17, scalable to 22x34, or as the EOR decides.
   - 30x42 when detail is lost at smaller size. (HOMEWOOD-020, team markup; CAD coordination exhibits)
   - 8.5x11 Psomas border allowed for appendix exhibits. (SAHPARK-008) and 8.5x11 variants produced for a memo/proposal (ELTORO-015)
   - Why it matters: report exhibits vs coordination exhibits vs memo figures need stated sizes; 30x42 is outside the "scalable to 22x34" rule.

7. EXH-X07 Scripted (matplotlib) vs editable (QGIS/CAD) figures
   - Scripted exhibit framework used as the working method. (SAH-019, ELTORO-015, NORTHLOOP-011, SILVERBELL-017)
   - Python instead of QGIS layouts is a deviation logged for EOR decision. (RKN-012)
   - Confirm editability first; user asked for scripted figures to be recreated in QGIS or CAD. (TANGERINE-006)
   - Existing skill: silent (CAD-derived and GIS/aerial exhibits only).
   - Why it matters: decides whether the new `scripted-exhibit-sheets` skill is a default or an exception path; affects rework when another discipline must edit the figures.

8. EXH-X08 Native output vs reformatted appendix sheets
   - drainage-report-exhibit-standards §4: include native program output, not recreated tables; table values must match it.
   - Hydraulic Toolbox inlet output reformatted to a one-page compact layout from native .hyd values, native export retained as evidence; accepted by the EOR. (VALENCIA-002)
   - Why it matters: either §4 gets a documented exception (native export kept, compact sheet values traced to native file, misprint noted) or the compact sheets violate the standard. Standard v0.3 change candidate.

9. EXH-X09 Result raster file naming
   - hecras-result-rasters script: `<tag>_<MaxDepth_ft|MaxVelocity_fps|MaxWSE_ft>_<cellsize>ft.tif`, tag = plan number (p##) by default.
   - condition_event[_future][_mitigation]_variable.tif, differences in a Differences subfolder with _Difference suffix, plan number listed per token in a dictionary. (DLR-005)
   - Why it matters: multi-scenario deliveries need scenario tokens and a plan-number dictionary; the script's plan-tag naming does not carry condition/event. Pick one scheme (e.g., scenario token + plan number + variable + units + cell size).

10. EXH-X10 FIRM panel / FIRMette project marking
    - Sketch the actual alignment or use a tight box; not a box over the whole panel. (SAHPARK-010)
    - FIRMette must cover the whole project with a red box labeled "this project", or use the full panel. (VALENCIA-023)
    - Why it matters: mostly compatible (box must cover the project), but VALENCIA-023 accepts a full panel, which may be read as a full panel with a large box - the exact case SAHPARK-010 rejected. Standard wording should say: tight box or alignment sketch, labeled; full panel allowed only with the project marked tightly.

11. EXH-X11 Aerial vs result-layer transparency
    - Aerial base at about 52% overlay under result classes. (CAMPBELL-016)
    - Depth raster semi-transparent over a full-strength aerial. (SAHPARK-006, TANGERINE-006)
    - Pick one overlay opacity before rendering (no value given; three opacity variants were produced). (ELTORO-015)
    - Why it matters: no standard value; exhibit sets are re-rendered over opacity choices. EOR should fix one default (layer and percentage).
