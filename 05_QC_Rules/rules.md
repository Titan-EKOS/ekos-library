# QC Rules

Each rule comes from a redline. Format (parsed by the server's get_qc_rules):

    ## QC-0001 Short title
    ```yaml
    id: QC-0001
    rule: One-sentence check.
    scope: [all]                 # or jurisdictions / functions / tags
    function: qc
    jurisdiction: all
    source_redline: <job no> <markup file> p.<page> comment <n>
    projects: [<job no>]
    added: YYYY-MM-DD
    ```

<!-- Rules start below this line -->
<!-- Built 2026-10-22 from Phase 3 clusters and qc_rule cards; decisions D01-D57 applied. Order: report-text, tables, exhibits, hydrology, hydraulics-2d, flo2d, culverts, storm-drain, model-runs, existing-conditions, crs, appendix, package, comment-response, then jurisdiction (fema, pima-rfcd, tucson, marana, sahuarita, placer, caltrans). Channel rules carry the culverts tag. -->

## QC-0001 Report numbers trace to output rows
```yaml
id: QC-0001
rule: "Every number in the report text and tables traces to a structured calculation output row or a native program output line, and quoted hydraulic results (Q, headwater elevation, inlet or outlet control, barrel length, slope, outlet velocity) match that line, with no soffit or crown elevation reported as computed headwater."
check: "Pick every numeric value in the narrative and summary tables and map it to an output file and row; list any value without a source as a finding; compare control type and HW against the HY-8 or Hydraulic Toolbox printout."
scope: [report-text, tables, culverts]
function: qc
jurisdiction: all
source_redline: "EKOS-LOCAL-016, SAHPARK-015, RKN-005, RKN-001, SAH-012 (review finding)"
projects: [EKOS-LOCAL, SAHPARK, RKN, SAH]
added: 2026-10-22
```

## QC-0002 Run matrix matches narrative
```yaml
id: QC-0002
rule: "Statements naming storms, durations, return periods or scenarios match a run matrix (model x storm x RP x scenario) built from completed runs (SUMMARY.OUT or result HDF), not from the plan list, and the report states which return periods were run in each model."
check: "Build the run matrix from completion evidence; search the text for every storm, duration and RP phrase and compare; flag any run that finished after the draft date."
scope: [report-text, model-runs]
function: qc
jurisdiction: all
source_redline: "SAH-017, SAH-003 (review finding)"
projects: [SAH]
added: 2026-10-22
```

## QC-0003 Design discharge: one value, one qualifier, one source
```yaml
id: QC-0003
rule: "Each design flow appears with one value, one storm qualifier (e.g. 100-yr local, 10-yr regional) and one source in a design discharge table, every Q in text, captions and table titles matches that table and the storm of the values shown, the summary flow equals the flow used to size the structure, and only the jurisdiction's design recurrence intervals are used unless labeled as a sensitivity."
check: "Compare every Q in text, tables and map captions with the design discharge table (value, event, duration, source); search for return periods outside the jurisdiction design set (e.g. 200-yr) and for approach flows quoted as crossing flows."
scope: [report-text, tables, hydrology]
function: qc
jurisdiction: all
source_redline: "BARNETT-006 (agency comment); SAHPARK-003, PHXZOO-007, NORTHLOOP-010 (JCO redline)"
projects: [BARNETT, SAHPARK, PHXZOO, NORTHLOOP]
added: 2026-10-22
```

## QC-0004 Design-value changes need a decision record
```yaml
id: QC-0004
rule: "No design flow, structure size or other basis value changes in tables without a decision-register entry (values, sources, choice, reason, dependency check), and once decided the value is identical across narrative, tables, exhibit labels, HY-8 runs and protection sizing, with JCO working assumptions kept out of report text unless JCO directs otherwise."
check: "Diff basis values between the previous and current draft; each change cites a decision-register entry; search narrative, tables, exhibits and calc files for the decided value and for superseded values."
scope: [report-text, tables]
function: qc
jurisdiction: all
source_redline: "VALENCIA-011, CAMPBELL-014 (JCO redline)"
projects: [VALENCIA, CAMPBELL]
added: 2026-10-22
```

## QC-0005 No carried-over text or unverified design claims
```yaml
id: QC-0005
rule: "The report contains no names of other projects, roads or washes, no old-job footers, design criteria (lane count, storm per system type) are this project's, the project description uses the scope or RFP wording where one is required and states the improvement and its direction correctly, and statements about ditches, profile changes, ponding or features (curb inlets, storm drains) are verified against the current design or removed."
check: "Search the text for prior project, road and wash names (target 0 hits); compare the description with the scope document; check each feature statement against the current plans and delete boilerplate for absent features."
scope: [report-text]
function: report-assembly
jurisdiction: all
source_redline: "VALENCIA-024, CAMPBELL-017, TANGERINE-019 (JCO redline)"
projects: [VALENCIA, CAMPBELL, TANGERINE]
added: 2026-10-22
```

## QC-0006 Agency outline followed; no empty headings
```yaml
id: QC-0006
rule: "The section list follows the reviewing agency's report outline (agency confirmed from property records and the contract), every heading has body text, and any outline section that does not apply reads \"Intentionally left blank\" with the reason."
check: "Compare the TOC one to one with the agency outline; scan for headings followed directly by another heading; record how the reviewing agency was confirmed."
scope: [report-text]
function: report-assembly
jurisdiction: all
source_redline: "TANGERINE-017, SAHPARK-002, SAHPARK-001 (JCO redline)"
projects: [TANGERINE, SAHPARK]
added: 2026-10-22
```

## QC-0007 Existing conditions content is complete
```yaml
id: QC-0007
rule: "The existing conditions section covers land use in every direction, slopes (range or average % and direction), soils, adjacent owners and development, existing infrastructure with sizes, drainage easements, mapped floodplains, existing basins, how the site drains today including ponding locations with spill elevation and path, and the roadway typical section from the latest plan set (or a statement that the road is uncurbed and spread and inlet analyses do not apply)."
check: "Tick each listed item against the section; check ponding and spill statements against topo; check the typical section date against the latest issued plans."
scope: [report-text, existing-conditions]
function: report-assembly
jurisdiction: all
source_redline: "SAHPARK-002, TANGERINE-020, CAMPBELL-017 (JCO redline)"
projects: [SAHPARK, TANGERINE, CAMPBELL]
added: 2026-10-22
```

## QC-0008 Analysis narrative content
```yaml
id: QC-0008
rule: "The analysis narrative states that CP flows are sums of sub-basins, presents calculated Q against prior-study Q for every CP in one table with differences discussed, describes the 2D model setup (culverts, cell size, refinement, inflows) before results, and states whether any increase reaches a habitable structure and its cause."
check: "Confirm the CP comparison table exists when a prior study exists; confirm the model setup subsection precedes results; search for the habitable-structure statement."
scope: [report-text, hydrology, hydraulics-2d]
function: report-assembly
jurisdiction: all
source_redline: "CAMPBELL-017 (JCO redline)"
projects: [CAMPBELL]
added: 2026-10-22
```

## QC-0009 Terms and style used consistently
```yaml
id: QC-0009
rule: "Natural washes are called washes and engineered ones channels, relative location words (near) are replaced by defined limits, one defined term is used for the project limits, zone terms (Top of Channel, Overbank Terrace, low-flow channel) are used only for those zones, allowable velocity is written as the velocity permitted over a lining or soil, agency names and abbreviations are spelled out on first use, and model names, units, dollar amounts and road names have one spelling and one report font."
check: "Run a term-count search for each limit and zone term and each style variant (FLO-2D, ROW, 10 ft, agency names); confirm road names against the plans; confirm one font in the document properties."
scope: [report-text, exhibits]
function: report-assembly
jurisdiction: all
source_redline: "CAMPBELL-017, TANGERINE-020, VALENCIA-020 (JCO redline); BARNETT-007, BARNETT-008, BARNETT-006 (agency comment)"
projects: [CAMPBELL, TANGERINE, BARNETT, VALENCIA]
added: 2026-10-22
```

## QC-0010 Internal numeric and statement consistency
```yaml
id: QC-0010
rule: "Every percent or ratio in the text recomputes from the table values with one rounding rule, cost-category percentages sum to 100, structure counts and funding or scope statements agree across sections, volumes and flows quoted in different sections share one basis, statements on figures do not contradict each other or the text, headings are parallel without duplicate titles, the milestone (15 or 30 pct) is stated up front, and no doubled qualifiers, stray characters or filler remain."
check: "Build a recompute table for each percent and ratio; sum cost percentages; list structure counts by section; read each figure's notes against the text; search for doubled qualifiers (approximately about) and stray brackets."
scope: [report-text, tables]
function: qc
jurisdiction: all
source_redline: "BARNETT-009 (agency comment); TANGERINE-014 (JCO redline)"
projects: [BARNETT, TANGERINE]
added: 2026-10-22
```

## QC-0011 Floodplain status statement
```yaml
id: QC-0011
rule: "The floodplain discussion tabulates the FIRM panels for the project limits (map number, panel, effective date, zones), reads the zone at the actual alignment rather than a blanket statement, names the effective and any pending panel and which governs at submittal, lists every effective zone the first time zones are listed with later lists matching, and states the town-limits or annexation status where it sets the floodplain authority."
check: "Compare the FIRM summary table with the NFHL at the alignment; compare each zone list in the report; confirm effective dates against the FEMA map service; check the annexation statement on Town projects."
scope: [report-text, fema, sahuarita]
function: report-assembly
jurisdiction: all
source_redline: "PHXZOO-007 (JCO redline); BARNETT-005 (agency comment)"
projects: [PHXZOO, BARNETT]
added: 2026-10-22
```

## QC-0012 Concept report framing
```yaml
id: QC-0012
rule: "A concept or rezoning report is labeled concept-level on the title page and executive summary, states what it does not do (no entitlement, no new hydrology, no permitting) in the executive summary, public-concern section and conclusions, uses \"is structured to meet, to be confirmed in the master drainage report\" in place of unearned compliance words, keeps objective findings separate from land-plan recommendations, states in the introduction whether a path is continuous under each major crossing and the crossing type, states for each existing structure whether it stays, is adequate or is replaced, describes flow paths in downstream order, and records written client decisions (level of protection, onsite containment, any designed overflow with agency buy-in) before relying on them."
check: "Search for conforms, adequate, decisively, opponents, preserves natural drainage; confirm the concept label and limitation statements in the three sections; confirm the crossing and structure statements appear in the introduction; confirm a client decision record exists for each protection-level choice."
scope: [report-text]
function: report-assembly
jurisdiction: all
source_redline: "TANGERINE-012, PHXZOO-005 (review finding); BARNETT-011 (agency comment)"
projects: [TANGERINE, BARNETT, PHXZOO]
added: 2026-10-22
```

## QC-0013 Claims match content and analysis
```yaml
id: QC-0013
rule: "Every \"incorporated in\" or \"see Section\" claim resolves to real content, sections use the final sub-consultant batch (logged by date) with final-vintage graphics, exhibit placeholders are populated or removed, summary tables actually pass the stated criteria, and conclusions name only facilities, BMPs and storms that were analyzed."
check: "Search for incorporated, see Section, refer to and follow each to its target; compare sub-consultant batch dates and file sizes with the report content; read conclusions against the run matrix and facility list."
scope: [report-text]
function: qc
jurisdiction: all
source_redline: "BARNETT-003, HOMEWOOD-015 (review finding)"
projects: [BARNETT, HOMEWOOD]
added: 2026-10-22
```

## QC-0014 Deliverable and proposal wording
```yaml
id: QC-0014
rule: "Deliverable text reads in completed tense, carries no AI or software-tool wording, no description of who did what between tools and engineers, no evidence-path or status labels, no code fragments and nothing that reads as interim; proposal text leads with the client, states goals in the client's terms, labels schedule durations (CLOMR, LOMR, historic review) as planning allowances and asserts no unconfirmed site facts."
check: "Scan the DOCX text for will be, TBD, working, unresolved, code tokens (if, else, {, }) and tool names; for proposals read the opening sentence and every site fact against confirmed data."
scope: [report-text, package]
function: report-assembly
jurisdiction: all
source_redline: "EKOS-LOCAL-016, STARVALLEY-020, ELTORO-020, SILVERBELL-016 (review finding); ELTORO-019 (JCO redline)"
projects: [EKOS-LOCAL, STARVALLEY, ELTORO, SILVERBELL]
added: 2026-10-22
```

## QC-0015 Report layout and formatting
```yaml
id: QC-0015
rule: "The report uses template heading and paragraph styles with numbered sections and no numbering gaps, no manual returns, page breaks only before main sections and appendices, no large white areas, orphaned headings or truncated sentences, aligned TOC tab leaders, numbered references to real sources only, no dates in footers, preparer and file properties set to the firm, and a project-specific cover photo; a letter memo (up to 10 pages, single topic) uses inline figures and no lists, while a multi-section report or technical memo has Contents and a List of Figures with 11x17 figures grouped at the end of their main section."
check: "Scroll the compiled PDF page by page for white space, orphans and truncation; check section numbers run without gaps; check footers and document properties; confirm memo or report layout matches the document type."
scope: [report-text]
function: report-assembly
jurisdiction: all
source_redline: "RKN-014, SAHPARK-005, TANGERINE-018 (JCO redline); SAHPARK-015, RKN-015 (review finding)"
projects: [RKN, SAHPARK, TANGERINE]
added: 2026-10-22
```

## QC-0016 Table style, captions and precision
```yaml
id: QC-0016
rule: "Tables are native Word tables (never screenshots) with thin borders on all cells, the header row in the template header style, no alternating shading or highlight fills, centered content, one caption above each table numbered by section (Table 4-1) with no second title inside the table, a \"presented in Table n\" sentence in the text, the header row repeated on any page break, elevations to 2 decimals without thousands separator, discharges in whole cfs, one precision per column, an existing-conditions summary wherever a proposed one is shown, and N/A or blank cells footnoted."
check: "Open each table: check border, fill and shading; compare caption with any internal title; check column precision; confirm each table is cited in text; confirm a paired existing table exists for each proposed table."
scope: [tables]
function: report-assembly
jurisdiction: all
source_redline: "SAHPARK-004, VALENCIA-021, RKN-014, TANGERINE-018 (JCO redline)"
projects: [SAHPARK, VALENCIA, RKN, TANGERINE]
added: 2026-10-22
```

## QC-0017 Structure tables match latest signed-sealed plans
```yaml
id: QC-0017
rule: "Every culvert row (barrel count, size, material, length, inverts, slope, Q100, HW) and outlet protection note matches the latest signed-sealed plan set with the plan sheet cited per value, each alternative row uses its own HW and velocity, and structures removed from or replaced in later roadway plans are updated."
check: "Diff the table against the latest signed-sealed plans and plan outlet protection table; list every value with sheet reference; confirm the plan set date is the newest issued."
scope: [tables, culverts]
function: qc
jurisdiction: all
source_redline: "VALENCIA-016 (agency comment); TANGERINE-013 (review finding)"
projects: [VALENCIA, TANGERINE]
added: 2026-10-22
```

## QC-0018 Crossing table complete and consistent
```yaml
id: QC-0018
rule: "The crossing table lists every existing, planned and proposed crossing with design Q, capacity and status, every crossing on the exhibits appears in the table and vice versa, and the table's adequacy statement agrees with the text."
check: "Cross-list crossings from exhibits and table; read the adequacy column against the paragraph that discusses upsizing."
scope: [tables, culverts, exhibits]
function: qc
jurisdiction: all
source_redline: "TANGERINE-013 (review finding); BARNETT-009 (agency comment)"
projects: [TANGERINE, BARNETT]
added: 2026-10-22
```

## QC-0019 IDs agree across maps, tables and appendix
```yaml
id: QC-0019
rule: "Every watershed, CP, inlet and structure ID on the maps appears in the tables and appendix calcs with the same label and location, with no duplicate IDs."
check: "Extract ID lists from map labels, report tables and appendix calc headings and diff them; check CP labels against their tabulated location; search for duplicate IDs."
scope: [tables, exhibits, appendix]
function: qc
jurisdiction: all
source_redline: "ELTORO-013, ELTORO-008 (review finding); VALENCIA-017 (agency comment)"
projects: [ELTORO, VALENCIA]
added: 2026-10-22
```

## QC-0020 Elevation datum and facility sizes
```yaml
id: QC-0020
rule: "Every elevation table uses the vertical datum of the current model and plans, and facility sizes in the report equal the current plans and vendor calculators."
check: "Spot-check three elevations per table against plan rims and model nodes; compare gallery, pipe and basin sizes in report, plans and vendor sheets."
scope: [tables, crs, storm-drain]
function: qc
jurisdiction: all
source_redline: "HOMEWOOD-015, HOMEWOOD-018 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0021 Calc workbook reuse and recalculation
```yaml
id: QC-0021
rule: "Before a reused calc workbook feeds report tables, cached errors (#REF!, #VALUE!) are listed per sheet with the sheets that feed the report, values pasted from legacy programs are flagged, numeric cells holding text are fixed, external links point to local copies, the current copy (revert, overwrite, 100 pct, signed-sealed) is confirmed, and the workbook is recalculated in a private Excel instance (events and link updates off, CalculateFullRebuild) followed by a value compare."
check: "Run the error scan and the recalc-and-compare script; attach the error register and the confirmed-current-copy note to the QC record."
scope: [tables]
function: qc
jurisdiction: all
source_redline: "VALENCIA-014 (review finding)"
projects: [VALENCIA]
added: 2026-10-22
```

## QC-0022 Exhibit sheet standards
```yaml
id: QC-0022
rule: "Each exhibit uses the Psomas border at the set size (report exhibits 11x17, scalable to 22x34; CAD coordination 30x42 allowed; appendix 8.5x11), one orientation and title-block position across the set, an engineering scale whose scale bar measures true on the plotted sheet, match lines and a sheet key when it spans sheets, north arrow, datums and data credits with pull dates, one label type (Figure or Exhibit) numbered by section without gaps and matching the TOC and text citations, new text at 9 pt minimum (inherited CAD text 0.1 in minimum), and no pixelated images."
check: "Measure the scale bar on the plotted PDF; list figure numbers from captions, TOC and text and diff them; check text heights in the source; zoom to 200 pct for pixelation."
scope: [exhibits]
function: exhibits
jurisdiction: all
source_redline: "SAHPARK-008, TANGERINE-022, CAMPBELL-018, VALENCIA-023, NORTHLOOP-011, CAMPBELL-016 (JCO redline); SAH-019, RKN-012 (review finding); BARNETT-008 (agency comment); HOMEWOOD-020 (team markup)"
projects: [SAHPARK, TANGERINE, SAH, BARNETT, CAMPBELL, VALENCIA, NORTHLOOP, RKN, HOMEWOOD]
added: 2026-10-22
```

## QC-0023 Legends show only mapped symbols as graphic samples
```yaml
id: QC-0023
rule: "Each legend entry shows the real mapped symbol with a short label, every symbol on the sheet has an entry, no entry appears for a layer with no features in the frame (or it reads \"none mapped\"), existing and proposed are named and drawn by condition, result legends define every class and state units, and scripted exhibits test every filtered layer for features and stop or warn before rendering."
check: "Compare symbols on each sheet with legend entries both ways; read the render log for empty-layer warnings and confirm each is resolved."
scope: [exhibits]
function: exhibits
jurisdiction: all
source_redline: "NORTHLOOP-012, TANGERINE-022, SAHPARK-007, SAHPARK-006 (JCO redline); CALFIRE-017, RKN-012 (review finding); HOMEWOOD-020 (team markup)"
projects: [NORTHLOOP, TANGERINE, SAHPARK, CALFIRE, RKN, HOMEWOOD]
added: 2026-10-22
```

## QC-0024 Drainage map base and context labels
```yaml
id: QC-0024
rule: "Every drainage map labels major roads plus some local roads and key landmarks (including the facility the project serves), wash names, at-grade crossings, existing culverts and bridges, protected areas, property boundary, parcels (named neutrally, subject parcel shaded but not solid) and easements, with contours screened back, labels inside the sheet with wipeouts, and no unexplained red lines."
check: "Check each sheet for the listed base items; search parcel labels for draft or working names."
scope: [exhibits]
function: exhibits
jurisdiction: all
source_redline: "SAHPARK-007, CAMPBELL-018, VALENCIA-023, TANGERINE-022 (JCO redline); TANGERINE-006 (review finding)"
projects: [SAHPARK, CAMPBELL, VALENCIA, TANGERINE]
added: 2026-10-22
```

## QC-0025 Drainage map infrastructure and node labels
```yaml
id: QC-0025
rule: "Drainage maps show pink watershed boundaries, flowlines with arrows, CP symbols by type, node letters with Q100 at each node (full attributes in the report table), HEC-HMS subbasins distinct from PC-Hydro watersheds, every structure number, every culvert with cell count, size and type (design-plan Q and calculated Q where both exist), curb and scupper outfalls with arrows and Q, berms as thick lines with basic dimensions, storm drains drawn as storm drain, and proposed linework on a separate layer and linetype from existing."
check: "Compare map labels with the structure and CP tables; confirm HMS and PC-Hydro basins have separate legend entries."
scope: [exhibits]
function: exhibits
jurisdiction: all
source_redline: "RKN-013 (review finding); CAMPBELL-018, VALENCIA-023, TANGERINE-022, SAHPARK-007 (JCO redline)"
projects: [RKN, CAMPBELL, VALENCIA, TANGERINE, SAHPARK]
added: 2026-10-22
```

## QC-0026 Watershed exhibits supported by topography
```yaml
id: QC-0026
rule: "Watershed exhibits show topography with 1-ft contours minimum (0.5-ft on flat sites, 2-ft only for large offsite areas), boundaries that follow visible ridge lines, flow arrows that agree with contours, the Tc flow path, depressions and the flowline into them, and the onsite boundary set at the project boundary so pre and post are compared there."
check: "Check contour interval in the legend; trace each boundary segment against contours; check arrow direction against contours."
scope: [exhibits, hydrology]
function: exhibits
jurisdiction: all
source_redline: "TANGERINE-023 (JCO redline); EKOS-LOCAL-008 (review finding)"
projects: [TANGERINE, EKOS-LOCAL]
added: 2026-10-22
```

## QC-0027 Location and project-area maps
```yaml
id: QC-0027
rule: "The report has one project-area map near the front showing study limits, affected properties and reference features, and a location map at about 1 in = 3 mi with township-section-range and road and landmark labels, cropped of plan clutter, with no aerial or FEMA layers; regional study-area figures borrowed from master plans are explained or removed."
check: "Confirm both maps, their scale and T-S-R; confirm no aerial on the location map; confirm each borrowed figure has an explanatory sentence."
scope: [exhibits]
function: exhibits
jurisdiction: all
source_redline: "BARNETT-007 (agency comment); TANGERINE-022, VALENCIA-023 (JCO redline)"
projects: [BARNETT, TANGERINE, VALENCIA]
added: 2026-10-22
```

## QC-0028 Result map symbology
```yaml
id: QC-0028
rule: "Depth and result maps state which ramp is used (local default: <0.2 ft hidden, 0.2-0.5, 0.5-1.0, 1.0-2.0, 2.0-3.0, >3.0 ft in yellow, cyan, blue, orange, red; deep-flow: 0-3, 3-5, 5-10, >10 ft), use continuous class bounds with the upper bound exclusive, a 0.01 ft data mask with display cutoff at the bottom of the ramp, a legend range set to the area of interest (no min-max stretch or 3-decimal breaks), aerial at full strength with the raster at 60 pct opacity, the same scale, classes and legend on existing and proposed sheets, proposed road and culvert linework, one exhibit set per storm named in the text with the storm in the title block, class breaks agreed with JCO before rendering and the same breaks used in text and tables, and a checked maximum value with no artifact top bin."
check: "Read the legend against the ramp definitions; compare raster max with plausible depth for the setting; confirm one set per storm cited; compare existing and proposed legends."
scope: [exhibits, hydraulics-2d, flo2d]
function: exhibits
jurisdiction: all
source_redline: "SAHPARK-006, CAMPBELL-018, SAHPARK-009, CAMPBELL-016 (JCO redline); TANGERINE-006, ELTORO-015 (review finding)"
projects: [SAHPARK, CAMPBELL, TANGERINE, ELTORO]
added: 2026-10-22
```

## QC-0029 Difference map symbology
```yaml
id: QC-0029
rule: "Proposed-minus-existing maps show increases only, hide |d| < 0.10 ft unless the agency threshold differs, state the difference sign and wet-dry rule on the sheet (WSE difference only where both are wet; depth difference treats dry as 0 ft), show newly wet ground as a separate hatch, and are paired with a velocity change exhibit for every WSE change exhibit."
check: "Read the sheet notes for sign, wet-dry rule and threshold; confirm a velocity change sheet exists for each WSE change sheet."
scope: [exhibits, hydraulics-2d, flo2d]
function: exhibits
jurisdiction: all
source_redline: "CAMPBELL-016 (JCO redline); DLR-005 (review finding)"
projects: [CAMPBELL, DLR]
added: 2026-10-22
```

## QC-0030 FEMA floodplain content on exhibits
```yaml
id: QC-0030
rule: "Where a FEMA SFHA is present, exhibits show Zone AE and 0.2 pct extents, BFEs and floodway hatch with the mapping effective date on the sheet and in the text, the 0.2 pct zone filtered on the NFHL ZONE_SUBTY text and tested non-empty, legend zones matching the mapped zones, any pending revision shown as a separate appendix item labeled preliminary, and the FIRM or FIRMette marked with a tight labeled box or sketched alignment covering the project (full panel only with the project marked tightly)."
check: "Compare legend zones with the NFHL features in the frame; confirm the effective date; check the FIRM box extent against the project limits; read the script log for empty-subset warnings."
scope: [exhibits, fema]
function: exhibits
jurisdiction: all
source_redline: "SAHPARK-010, TANGERINE-021, VALENCIA-023 (JCO redline); CALFIRE-017, SILVERBELL-017, TANGERINE-008 (review finding)"
projects: [SAHPARK, CALFIRE, TANGERINE, VALENCIA, SILVERBELL]
added: 2026-10-22
```

## QC-0031 Exhibit values come from one register
```yaml
id: QC-0031
rule: "Every changing value on an exhibit (CP and inflow Q, required and provided storage, inverts) is placed from one register table and matches the report table, every model inflow is shown as a labeled cross-section line with its ID and peak Q for that storm, and storage exhibits show Volume Required and Calculated to Provide for each unit."
check: "Diff exhibit labels against the register and report tables; confirm labels regenerate from the register rather than hand edits."
scope: [exhibits, tables]
function: exhibits
jurisdiction: all
source_redline: "ELTORO-016, HOMEWOOD-018 (review finding); SAHPARK-009 (JCO redline)"
projects: [ELTORO, HOMEWOOD, SAHPARK]
added: 2026-10-22
```

## QC-0032 CAD coordination and cut exhibits
```yaml
id: QC-0032
rule: "CAD coordination exhibits clip master-plan xrefs and draw master-plan linework in a muted color distinct from survey, freeze unneeded layers, weight key proposed lines heavier, label FF, FG and major contours, note base changes, and match table text across the sheet; cut or boring exhibits show cut at every test pit or boring, a note stating the reference surface, max and min cut, and a ramp with clearly different shades at key depths."
check: "Check the xref clip and layer states; check every boring has a cut label; read the reference-surface note."
scope: [exhibits]
function: exhibits
jurisdiction: all
source_redline: "HOMEWOOD-020, HOMEWOOD-019 (team markup)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0033 Exhibit render-and-review pass
```yaml
id: QC-0033
rule: "Before compile, every sheet of the current revision is rendered to PNG in a dated 40_QC review folder with figure ID and title in the file name, one full checklist pass is logged before fixes, each fix is applied to every sheet that shares it, pending values are marked pending, unmodeled concepts are labeled, and scripted sheets pass the same checks as QGIS or CAD sheets with editable source kept."
check: "Confirm the PNG set covers every sheet; confirm one logged pass per revision; spot-check that a fixed item is fixed on all sheets."
scope: [exhibits, package]
function: qc
jurisdiction: all
source_redline: "SAH-019, RKN-018 (review finding); TANGERINE-022, NORTHLOOP-011 (JCO redline)"
projects: [SAH, TANGERINE, NORTHLOOP, RKN]
added: 2026-10-22
```

## QC-0034 Nested and tributary area accounting
```yaml
id: QC-0034
rule: "A parent-child area table shows which outlet areas include upstream basins or pipe catchments, incremental areas sum to the total, no flows are summed across nested areas (route upstream outflow and add only the incremental area), attributes are joined on the same catchment key as geometry, and offsite areas draining to a storm drain include the tributary roadway and subdivision areas with the inlet capture assumption stated."
check: "Sum incremental areas against the total; search calcs and narrative for sums of nested flows; check key match counts in the join log; overlay the storm drain on the offsite watershed map."
scope: [hydrology]
function: hydrology
jurisdiction: all
source_redline: "EKOS-LOCAL-008 (review finding); TANGERINE-024 (JCO redline)"
projects: [EKOS-LOCAL, TANGERINE]
added: 2026-10-22
```

## QC-0035 PC-Hydro native output matches report
```yaml
id: QC-0035
rule: "Every CP and return period in the report matches a native PC-Hydro rerun printout with max abs difference 0.0 cfs (for a rebuild the old report is the target), the comparison table is kept in the QC record, and the record states that this check does not replace the independent check."
check: "Rerun each CP natively, compile the native-vs-report table and confirm max abs diff = 0.0 cfs."
scope: [hydrology, tables]
function: hydrology
jurisdiction: all
source_redline: "RKN-005 (review finding)"
projects: [RKN]
added: 2026-10-22
```

## QC-0036 PC-Hydro inputs and hydrograph exports
```yaml
id: QC-0036
rule: "PC-Hydro runs on graded ground use the program default vegetation cover (20 pct) verified against the 7.4 auto-fill before each batch, native runoff parameters (no fixed CN) and the program Tc (5 min minimum); hydrograph exports are confirmed at 60-s spacing in cfs, the native export is kept unchanged, any peak-adjusted copy and tail closure log the added volume, the peaks table reports both reported peak and sampled maximum, and DSS writes (INST-VAL, CFS, 1Minute) are reopened and verified ordinate by ordinate."
check: "Open the run inputs for typed cover or CN; check the export time step; compare native and adjusted files; run the DSS round-trip check."
scope: [hydrology, model-runs]
function: hydrology
jurisdiction: all
source_redline: "NORTHLOOP-013 (JCO redline); EKOS-LOCAL-007 (review finding)"
projects: [NORTHLOOP, EKOS-LOCAL]
added: 2026-10-22
```

## QC-0037 Uncalibrated CN models compared to independent estimates
```yaml
id: QC-0037
rule: "A HEC-HMS CN model on HSG C/D watersheds is compared with an independent estimate (FIS, regression) after reconciling the DEM area with the FIS area, any calibration (uniform CN reduction) is reported with its magnitude and its effect on the full frequency curve, the uncalibrated 100-yr is carried as a sensitivity through the hydraulics, and the calibration is listed in the open items for agency confirmation."
check: "Compare Q100 to FIS and regression; confirm the calibration table and the sensitivity run exist; confirm the open-items entry."
scope: [hydrology, caltrans]
function: hydrology
jurisdiction: all
source_redline: "CALFIRE-007 (review finding)"
projects: [CALFIRE]
added: 2026-10-22
```

## QC-0038 Percent impervious has a stated source
```yaml
id: QC-0038
rule: "No percent impervious or cover value enters a model without a stated source: plans, independent labels that meet a stated acceptance with imagery covering the full hydraulic extent, or a named cover scenario."
check: "Trace each impervious value in the model inputs to its source; for imagery classifiers check holdout agreement against the acceptance value and coverage extent."
scope: [hydrology]
function: hydrology
jurisdiction: all
source_redline: "EKOS-LOCAL-019 (review finding)"
projects: [EKOS-LOCAL]
added: 2026-10-22
```

## QC-0039 500-yr basis stated once
```yaml
id: QC-0039
rule: "The 500-yr WSE basis is stated once: the FIS 0.2 pct profile only where its sections bracket the site, else agency 500-yr hydrology, else a documented provisional value with agency agreement, with any 1.75 x Q100 scaling labeled a sensitivity and floor, pad and equipment elevations tabulated with datum against the controlling 100-yr and 500-yr WSE."
check: "Measure distance from the nearest FIS section to the site; search for every 500-yr basis statement; check the elevation table datum."
scope: [hydrology, fema, marana, tucson, pima-rfcd]
function: hydrology
jurisdiction: all
source_redline: "NORTHLOOP-010, TANGERINE-021 (JCO redline); NORTHLOOP-006 (review finding)"
projects: [NORTHLOOP, TANGERINE]
added: 2026-10-22
```

## QC-0040 Detention, first-flush and sediment basins shown separately
```yaml
id: QC-0040
rule: "A report proposing detention or retention gives preliminary pre and post peak Q and storage estimates even at concept level, separates flood detention, first-flush or WQ retention, sediment storage and harvesting with their own criteria, tabulates allowable outflow and volume per development pod with the phasing trigger for distributed detention, and names maintenance access and the responsible entity."
check: "Confirm the per-facility table and per-pod ledger; confirm the responsible entity is named."
scope: [hydrology, storm-drain, pima-rfcd]
function: hydrology
jurisdiction: all
source_redline: "TANGERINE-015 (JCO redline)"
projects: [TANGERINE]
added: 2026-10-22
```

## QC-0041 2D volume accounting acceptance
```yaml
id: QC-0041
rule: "No 2D result (HEC-RAS or FLO-2D) is mapped, reused or reported until native volume accounting shows global and per-area error <= 0.1 pct for final runs (<= 0.5 pct for screening runs only) with no large opposing regional errors, max WSEL residual and iteration warnings are checked, rejected events are not published, and diagnostics change one control at a time from closed source inputs."
check: "Read the computation log volume accounting (or SUMMARY.OUT) for every plan and area; record pass/fail; confirm a solver success message was not used as acceptance."
scope: [hydraulics-2d, flo2d, model-runs]
function: hydraulics-model-run
jurisdiction: all
source_redline: "CAMPBELL-002, CALFIRE-010 (review finding)"
projects: [CAMPBELL, CALFIRE]
added: 2026-10-22
```

## QC-0042 Boundaries and result plausibility
```yaml
id: QC-0042
rule: "Every 2D domain has an outflow boundary at the downstream mesh limit, the flow split between boundaries and structures is reported and the domain is extended when a boundary drives the answer, and any metric identical across events (e.g. same max HW for 10- through 100-yr) is treated as an extraction error or artifact and resampled from the WSE result."
check: "List BCs from the geometry; tabulate boundary vs structure peak flow; compare max values event to event for identical results."
scope: [hydraulics-2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "CALFIRE-010, PHXZOO-006 (review finding)"
projects: [CALFIRE, PHXZOO]
added: 2026-10-22
```

## QC-0043 Reused or converted 2D models screened
```yaml
id: QC-0043
rule: "Before a reused or converted 2D model is the existing-condition basis, it is screened for cell size range against agency guidance, breaklines on channels, roads and berms, culverts matched to latest plans and as-builts (barrels, inverts, length, slope, station), existing geometry free of proposed crossings, terrain VRT source order and spurious modification rasters, velocity spikes at wet-dry faces, and (for HEC-RAS 2025 GPU conversions) an audited import, native plan preparation confirming supported features and a short test with nonzero depths."
check: "Complete the reused-model screening list and attach it to the run register; for conversions attach the plan-preparation message and short-test depth summary."
scope: [hydraulics-2d, model-runs]
function: hydraulics-model-run
jurisdiction: all
source_redline: "PHXZOO-006, CAMPBELL-006 (review finding)"
projects: [PHXZOO, CAMPBELL]
added: 2026-10-22
```

## QC-0044 Unsteady flow files and precipitation verified
```yaml
id: QC-0044
rule: "Each BC line is named <source>-<CP>-<Q100> and unique, every frequency's unsteady flow file carries the same BC name set with frequency-specific hydrographs and none keeps a removed or duplicate line, each plan points to the intended flow file, and rain-on-grid plans show Precipitation Mode not Disable with an existing DSS path matching the plan frequency and precipitation volume in the log."
check: "Export BC names and peaks from every .u0x and diff the name sets (target empty); open each flow file's precipitation settings; list the plan-to-flow-file map in the run register."
scope: [hydraulics-2d, model-runs]
function: hydraulics-model-run
jurisdiction: all
source_redline: "ELTORO-002, ELTORO-003, ELTORO-006 (review finding)"
projects: [ELTORO]
added: 2026-10-22
```

## QC-0045 Boundary inflow register reconciled
```yaml
id: QC-0045
rule: "Inflow BCs in a hybrid rain-on-grid model are kept only for contributing areas outside the mesh, come from a register (CP, area, Q2/Q10/Q100, report page, condition) with a map-based CP concordance across studies, remove the upstream CP whenever its downstream CP is entered, contain no double-counted sub-basins, and reconcile line by line with the BC list exported from the model."
check: "Overlay CP watersheds on the 2D perimeter; diff the exported BC list against the register; search for one watershed under two names."
scope: [hydraulics-2d, hydrology]
function: hydraulics-model-run
jurisdiction: all
source_redline: "ELTORO-001, CAMPBELL-010 (review finding)"
projects: [ELTORO, CAMPBELL]
added: 2026-10-22
```

## QC-0046 Cited plans exist and are condition-specific
```yaml
id: QC-0046
rule: "Every HEC-RAS plan cited in a caption or table exists, is registered in the .prj, has a condition-specific title, points to the flow file matching its title and storm, and is cited by plan file, short ID and geometry."
check: "Read the .prj and each .p## as text; build the plan-geometry-flow register; compare with captions and tables."
scope: [hydraulics-2d, report-text]
function: hydraulics-model-run
jurisdiction: all
source_redline: "TANGERINE-004, SAHPARK-016, DLR-001 (review finding)"
projects: [TANGERINE, SAHPARK, DLR]
added: 2026-10-22
```

## QC-0047 Flow accounting at railroads, breakouts and structures
```yaml
id: QC-0047
rule: "Railroad surface flow, bridge opening flow and culvert barrel flow are reported separately, total crossing flow is the peak of the simultaneous combined series rather than a sum of peaks, serial breakout sections are not added, flow beneath tracks is labeled only when bridge HW and TW stay below the deck, and stages are compared at peak structure flow."
check: "Check the extraction script uses bridge variable flow, not terminal reach flow; recompute total crossing flow from the combined series."
scope: [hydraulics-2d, culverts]
function: hydraulics-model-run
jurisdiction: all
source_redline: "CAMPBELL-009 (review finding)"
projects: [CAMPBELL]
added: 2026-10-22
```

## QC-0048 Matched models for impact comparison
```yaml
id: QC-0048
rule: "Existing and proposed (and control) conditions share one model set (same perimeter or CADPTS, cell size, breaklines, 1D network, FPXSEC, INFLOW, OUTFLOW, TOLER, RAIN, controls and engine build, verified by hash), differ only in terrain inside approved grading and roughness, use the effective grid as base terrain, compare cells wet above 0.1 ft with new wet areas reported separately, review extreme differences at fill or excavation as ground change, and are processed together so the results register is complete."
check: "Hash the shared input files across conditions (target equal); confirm the control plan reproduces base; confirm the results register lists every scenario."
scope: [hydraulics-2d, flo2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-007, CAMPBELL-008, ELTORO-017, STARVALLEY-008, NORTHLOOP-009 (review finding); TANGERINE-003 (agency comment)"
projects: [STARVALLEY, TANGERINE, CAMPBELL, ELTORO, NORTHLOOP]
added: 2026-10-22
```

## QC-0049 Impact and no-rise claims
```yaml
id: QC-0049
rule: "No-adverse-impact or no-rise wording appears only with matched-model difference maps and tables, rise thresholds are cited from the governing agency or stakeholder for the project (no hard-coded 0.1 ft), sensitivity series stop at a limit agreed with JCO without changing approved grading to fix numerical behavior, and lidar, local or iterated-tailwater models are labeled screening with no no-rise or CLOMR finding drawn from a non-effective model."
check: "Search the text for no adverse, no rise, no impact; confirm each has a matched-model exhibit and table and a cited threshold source; confirm screening labels on non-effective models."
scope: [hydraulics-2d, report-text, fema, marana]
function: qc
jurisdiction: all
source_redline: "TANGERINE-003 (agency comment); CAMPBELL-008, SILVERBELL-016, CALFIRE-011, SILVERBELL-001 (review finding); SILVERBELL-002 (JCO redline)"
projects: [TANGERINE, CAMPBELL, SILVERBELL, CALFIRE]
added: 2026-10-22
```

## QC-0050 Manning n basis
```yaml
id: QC-0050
rule: "A uniform 2D Manning n is used only when extending an accepted model and the report says so; new, concept and master studies use land-cover n; n = 0.025 applies to constructed unlined earthen channels; natural channel n comes from land cover with the source cited."
check: "Read the roughness layers and channel n values; search the report for the n basis statement."
scope: [hydraulics-2d, flo2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "TANGERINE-001 (review finding); TANGERINE-003 (agency comment); NORTHLOOP-014 (JCO redline)"
projects: [TANGERINE, NORTHLOOP]
added: 2026-10-22
```

## QC-0051 Result raster provenance and spot check
```yaml
id: QC-0051
rule: "Result rasters come from the final set (not VOID or superseded copies, checked by entry date), are named <scenario>_<event>_<variable>_<units>_<cell>ft.tif with a plan-number dictionary and differences in a Differences folder, scripted max rasters are spot-checked at 5-10 points against a RAS Mapper map of the same plan and terrain with a warning where terrain modifications live only in a terrain HDF, max face velocity spikes far above physical are screened and the run labeled diagnostic until the mesh is fixed, and quoted velocity is identified as a max face velocity proxy."
check: "List zip and folder entry dates; check names against the pattern; compare spot values with RAS Mapper; read max face velocity and its location for each run."
scope: [hydraulics-2d, exhibits]
function: hydraulics-model-run
jurisdiction: all
source_redline: "DLR-004, DLR-006, CAMPBELL-003 (review finding)"
projects: [DLR, CAMPBELL]
added: 2026-10-22
```

## QC-0052 FLO-2D text inputs use CRLF
```yaml
id: QC-0052
rule: "FLO-2D .DAT and .RGH text inputs are written with explicit CRLF and a trailing CRLF, every text input is scanned for bare LF before each run (binary NEIGHBORS.DAT untouched), and patches preserve the existing line-ending style via temp file and rename."
check: "Run the line-ending scan on the model folder (target zero bare-LF files) and record the result in the run register."
scope: [flo2d, model-runs]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-001 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0053 ERROR.CHK, structure and levee data clean
```yaml
id: QC-0053
rule: "ERROR.CHK is read after the first short test run with each ERROR and WARNING listed by file and either fixed or answered from the known-benign list and logged, no production queue starts with open errors, no HYSTRUC inflow node is shared by two structures (repeated outflow nodes have a limit or separate nodes), and no grid element next to a levee is higher than the levee crest."
check: "Parse ERROR.CHK into the run register with a disposition per message; scan HYSTRUC.DAT for duplicate inflow nodes; compare LEVEE.DAT crests with adjacent grid elevations."
scope: [flo2d, model-runs]
function: hydraulics-model-run
jurisdiction: all
source_redline: "SAH-006 (review finding)"
projects: [SAH]
added: 2026-10-22
```

## QC-0054 Proposed TOPO free of placeholder surfaces
```yaml
id: QC-0054
rule: "A proposed-conditions TOPO.DAT has no large patches of cells at one constant elevation, agrees with the design TIN and with existing ground inside grading limits (mean, median, std, pct within 0.5 ft reported), and has no artificial steps at the regrade boundary."
check: "Run the constant-elevation patch scan and TIN comparison; report max adjacent-cell step at the regrade boundary."
scope: [flo2d, existing-conditions]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-015 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0055 FLO-2D 1D channel geometry valid
```yaml
id: QC-0055
rule: "Bank cells are the first floodplain cell perpendicular to flow (never a channel cell), each grid cell belongs to one segment, stub reaches of 2 cells or less are dropped, onsite channels are not dead-end reaches without their outlet culverts, each cross section has 20-25 station points (hard limit near 33) with an interior thalweg, relief >= 0.5 ft and no duplicate stations, natural sections are numbered consecutively with one XSEC per channel element, CHANBANK is built after the final section cut, synthetic bank or relief adjustments are listed in xsec_adjustments_*.csv, and plan, profile and section QC plots exist before the first run."
check: "Run the channel validity script on CHAN, CHANBANK and XSEC; check numbering gaps; review the adjustments CSV."
scope: [flo2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-002 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0056 Grade-control drops kept in channel geometry
```yaml
id: QC-0056
rule: "Abrupt invert drops in constructed channels are kept as grade-control structures (not smoothed), each listed with location and height for JCO review and a decision on whether a structure rating is needed."
check: "Compare channel invert profile with design drops; confirm the drop list and JCO decision exist."
scope: [flo2d, culverts]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-016 (JCO redline)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0057 FLO-2D hydraulic structures pass flow
```yaml
id: QC-0057
rule: "Structure inlet and outlet cells are never channel-interior cells and IFPORCHAN matches the cell type, rating tables use ICURVTABLE = 1, HEADREFEL offsets from HY-8 culvert invert to inlet-cell bed are recorded, all tables come from one HY-8 project with matching names, a discharge range covering the model peak and the model's tailwater assumption, and per-structure peak and volume are read after each run with any wet-inlet structure at zero flow stopping the work."
check: "Check HYSTRUC.DAT cells against CHAN and CHANBANK; compare tables with the HY-8 export; run the structure-flow script after each run."
scope: [flo2d, culverts]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-012 (agency comment); STARVALLEY-004 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0058 FLO-2D build recorded
```yaml
id: QC-0058
rule: "Each FLO-2D project records the agency-named build and the working build, and runs on build 26.02.25 carry a logged written agency acceptance for that project."
check: "Compare FLOPRO.exe build, CONT.DAT line 1 and SUMMARY.OUT build in every model folder; confirm the acceptance record."
scope: [flo2d, model-runs, marana]
function: hydraulics-model-run
jurisdiction: all
source_redline: "NORTHLOOP-003, STARVALLEY-004 (review finding)"
projects: [NORTHLOOP, STARVALLEY]
added: 2026-10-22
```

## QC-0059 Capacity, freeboard and protection values
```yaml
id: QC-0059
rule: "Channel and culvert results show max flow depth and required freeboard, a reported headwater states whether freeboard is included, velocities in protection tables equal the HEC-RAS or HY-8 value at the same station with their source stated, HEC-14 sheets use the plan barrel count, outlet protection is designed for each culvert and basin outlet, aprons over 10 fps carry a wire-tied note, edge protection is D50 6 in at least 5 ft from pavement edge or to toe of fill, and toe-down depths are tabulated with station-to-station limits."
check: "Compare protection-table velocities with model output at matching stations; compare HEC-14 barrel count with plans; check freeboard labels on HW values."
scope: [culverts, tables]
function: qc
jurisdiction: all
source_redline: "ELTORO-012 (review finding); CAMPBELL-019 (JCO redline)"
projects: [ELTORO, CAMPBELL]
added: 2026-10-22
```

## QC-0060 Culverts in sediment-laden piedmont areas
```yaml
id: QC-0060
rule: "New culverts in alluvial or piedmont areas use survey or as-built sizes, size outlet protection per HEC-14 (a dumped riprap apron alone is not enough at 9-13 fps), set inlet and outlet channel inverts at or below the box invert, note sediment risk for alignments perpendicular to flow, provide cutoff walls for 100-yr scour plus long-term degradation, plan HEC-18/HEC-20 scour for final design, and state the overtopping criterion with margin and weir-length sensitivity."
check: "Check outlet velocity against the protection type; check invert relationships on the profile; confirm scour and margin statements."
scope: [culverts, sahuarita, marana]
function: qc
jurisdiction: all
source_redline: "SAHPARK-020 (JCO redline)"
projects: [SAHPARK]
added: 2026-10-22
```

## QC-0061 Crossing geometry and restricted ROW
```yaml
id: QC-0061
rule: "Crossing concepts confirm which frontage is restricted before extending outlets, grading or easements on that side, keep footprint overlap with restricted parcels (current county parcel geometry) at 0 sq ft, extend barrels to the roadway fill toes with any length far outside its neighbors checked, set bridge low chord at least 2 ft above computed Q100 spanning the full existing flood envelope, and carry one geometry through CAD, 1D/2D models and renderings."
check: "Overlay the footprint on restricted parcels and report overlap area; compare barrel ends with fill toes; flag barrel length outliers; compare low chord with Q100 WSE."
scope: [culverts, existing-conditions, pima-rfcd]
function: qc
jurisdiction: all
source_redline: "SILVERBELL-003 (JCO redline); SILVERBELL-004, SILVERBELL-008 (review finding)"
projects: [SILVERBELL]
added: 2026-10-22
```

## QC-0062 Channels described, sized and tabulated
```yaml
id: QC-0062
rule: "Each proposed channel has a narrative (location, tributary watersheds, inflow structures, outlet) and a channel-table row numbered like the appendix calcs, an existing receiving channel that gets added flow is analyzed, freeboard and provided depth are shown separately from normal depth, collector channels are sized for the combined intercepted flow with superelevation at bends and a conservative bank-height screen, lining is stated (riprap not the default under high sediment load; earthen n = 0.025 only if unlined) with maintenance access, and a level spreader is provided where a collector returns flow to natural ground."
check: "Compare channel table, narrative and appendix labels; recompute required depth = normal depth + freeboard + superelevation for each reach; confirm lining and outlet statements."
scope: [culverts, tables, marana]
function: qc
jurisdiction: all
source_redline: "VALENCIA-019 (agency comment); NORTHLOOP-014, NORTHLOOP-015, NORTHLOOP-016 (JCO redline)"
projects: [VALENCIA, NORTHLOOP]
added: 2026-10-22
```

## QC-0063 Storm drain HGL routing and freeboard
```yaml
id: QC-0063
rule: "Any storm drain model used to report HGL, surcharge or tailwater uses dynamic (hydrodynamic) routing with a short routing step and entrance and exit losses, and reports minimum freeboard to rim or grate per structure against the governing criterion."
check: "Open the model options for routing method and step; compare the freeboard table with structure rims."
scope: [storm-drain, placer]
function: hydraulics-model-run
jurisdiction: all
source_redline: "HOMEWOOD-006 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0064 Receiving system and tailwater
```yaml
id: QC-0064
rule: "Receiving-structure rim, invert and HGL come from the agency or as-builts, fixed-tailwater and free-outfall cases are both run and reported with model and memo stating the same boundary, assumed tailwater is compared with the lowest onsite rims and gallery crowns, proposed peaks are compared with receiving capacity and HGL, each discharge or retention alternative is explained, and report claims (e.g. impervious removed) match the site plan."
check: "Read the outfall boundary in the model and the memo; confirm both tailwater cases; check claims against the site plan."
scope: [storm-drain, tucson, placer]
function: qc
jurisdiction: all
source_redline: "HOMEWOOD-010 (review finding); TANGERINE-025 (JCO redline)"
projects: [HOMEWOOD, TANGERINE]
added: 2026-10-22
```

## QC-0065 WQ volume retained below the lowest outlet
```yaml
id: QC-0065
rule: "Storage below the lowest outlet invert as drawn (from the stage-storage curve) is at least the WQ volume, outlets are modeled exactly as drawn on plan and detail sheets, the WQ event is routed with and without infiltration with the untreated volume reported, and the check is repeated after every gallery size change."
check: "Compute storage below the drawn outlet invert; compare model outlet geometry with the detail sheet; read the routed untreated volume."
scope: [storm-drain, hydrology]
function: qc
jurisdiction: all
source_redline: "HOMEWOOD-007, HOMEWOOD-018 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0066 Inlet, scupper and storm drain tables match plans
```yaml
id: QC-0066
rule: "Inlet IDs, stations and sides match the latest plans with removed inlets shown as removed and no duplicates, modified catch basins record actual sump length and wings with non-PAG standards noted and capture rerun when opening length changes, scupper tables state design frequency and clogging factors with Q matching the hydrology for that frequency and scuppers analyzed in sump (or splashover length given), and each storm drain line lists upstream structure, length, slope, size and material, Q, HGL and velocity matching plan profiles and model output, with existing lines receiving added flow checked and appendix output regenerated after any redesign."
check: "Diff inlet and storm drain tables against plan sheets and model output pages; confirm capture reruns for changed openings; check scupper Q frequency against the hydrology table."
scope: [storm-drain, tables]
function: qc
jurisdiction: all
source_redline: "VALENCIA-017, VALENCIA-018 (agency comment); ELTORO-011 (review finding)"
projects: [VALENCIA, ELTORO]
added: 2026-10-22
```

## QC-0067 Inflow series and run duration
```yaml
id: QC-0067
rule: "Every inflow series has strictly increasing times at the source interval with matching units (1MIN vs 1HOUR), integrated volume and peak per node match the source workbook before and after scaling (repairs change timestamps only and are logged), and the run duration covers the last inflow and the recession (shortest end time with < 0.01 ft later rise, or for an archived model the simulation time compared with the last inflow time)."
check: "Run the chronology and volume audit; compare CONT.DAT or plan end time with the last inflow; note that 0.0 pct volume error in SUMMARY.OUT does not validate chronology."
scope: [model-runs, flo2d, hydraulics-2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "NORTHLOOP-004, NORTHLOOP-005, CAMPBELL-010 (review finding)"
projects: [NORTHLOOP, CAMPBELL]
added: 2026-10-22
```

## QC-0068 Preflight gate before launch
```yaml
id: QC-0068
rule: "No production run launches unless preflight_pass is true: chronology and volume checks pass, duration covers the recession, no double counts, CRLF scan clean, every copied file matches the source by size and hash (NEIGHBORS.DAT size matches the grid; FLOPRO.exe build and DLL count checked), shared inputs hash equal across compared scenarios, and HEC-RAS plans save face flow output."
check: "Read preflight_checks output for the run; confirm the launch log shows preflight_pass true."
scope: [model-runs, flo2d, hydraulics-2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "STARVALLEY-003, NORTHLOOP-004, CAMPBELL-010 (review finding)"
projects: [STARVALLEY, NORTHLOOP, CAMPBELL]
added: 2026-10-22
```

## QC-0069 Run supervision and completion
```yaml
id: QC-0069
rule: "Each run records expected time from its base run and is stopped when simulated hours per wall hour fall below 25 pct of the base or one element controls the time step for many intervals, a FLO-2D run counts as complete only with the SUMMARY.OUT termination line, all outputs and no TMP files (a HEC-RAS run by its result HDF), and no run is left unmonitored at session end without being stopped or handed off."
check: "Read the watchdog log, SUMMARY.OUT and TIME.OUT; list TMP files; check the status file at session end for running jobs."
scope: [model-runs, flo2d]
function: hydraulics-model-run
jurisdiction: all
source_redline: "SAH-003, STARVALLEY-021 (review finding)"
projects: [SAH, STARVALLEY]
added: 2026-10-22
```

## QC-0070 Source integrity and model intake
```yaml
id: QC-0070
rule: "Received files and archives stay unchanged (work on copies; hash before and after any automated CAD export or scripted edit; timestamped backups of .g0x and .u0x before edits), the as-received current plan and versions are recorded, stray or snapshot HDFs and conflict copies are never treated as results, and archived FLO-2D alternatives are selected from a native folder register, not by folder name or newest timestamp."
check: "Compare before and after hash manifests; check the model register for status of each plan or folder; search for snapshot, conflict and renamed HDFs."
scope: [model-runs, existing-conditions]
function: data-gathering
jurisdiction: all
source_redline: "NORTHLOOP-018, ELTORO-006, DLR-001, NORTHLOOP-006, DLR-003, CAMPBELL-011, NORTHLOOP-001, EKOS-LOCAL-023 (review finding)"
projects: [NORTHLOOP, ELTORO, DLR, CAMPBELL, EKOS-LOCAL]
added: 2026-10-22
```

## QC-0071 Existing conditions verified against current records
```yaml
id: QC-0071
rule: "Crossings, structures and road status are confirmed with the agency and current records before use (built crossings removed from proposed lists, master-plan structures checked against aerials, as-builts and site visit), the governing revision of each as-built set is recorded with conflicting sets noted and the owner decision logged, adjacent as-builts and grading revisions are tabulated with pipe and ditch sizes, the imagery date is later than the newest adjacent construction (or the gap noted), regional flow corridors crossing or bordering the site carry Q100 and an intercept statement, and redirected runoff from adjacent future development is recorded as an assumption."
check: "Compare the structure list with agency confirmation and as-builts; check revision blocks; compare imagery date with adjacent construction dates; confirm corridor Q100 statements."
scope: [existing-conditions]
function: data-gathering
jurisdiction: all
source_redline: "BARNETT-005 (agency comment); ELTORO-008, ELTORO-023 (review finding); SAHPARK-014 (JCO redline)"
projects: [BARNETT, ELTORO, SAHPARK]
added: 2026-10-22
```

## QC-0072 As-built and approved-plan rechecks
```yaml
id: QC-0072
rule: "Existing crossings modeled from as-builts compare modeled max WSE with the road centerline high point and match culvert Q100, n and entrance loss to the as-built values, and approved plans without as-builts are rechecked (stage-storage from the supplied grading surface, culvert and storm drain HW against allowable at the design flow) with each difference recorded in numbers and a JCO decision."
check: "Tabulate approved vs recalculated values with JCO decision references; compare modeled WSE with road high point and observed overtopping."
scope: [existing-conditions, culverts]
function: qc
jurisdiction: all
source_redline: "ELTORO-014 (review finding); STARVALLEY-023 (JCO redline)"
projects: [ELTORO, STARVALLEY]
added: 2026-10-22
```

## QC-0073 Assumption log verified and reported
```yaml
id: QC-0073
rule: "Every assumed structure, berm and grading edit is logged with ID, basis, source, verify-by and X/Y (CSV plus GIS layer), sorted by influence, high-influence items (berms and culverts near the road) are verified before issue, and the unverified count is stated in the report assumptions appendix."
check: "Read the assumption log for verified flags; compare the unverified count with the report statement."
scope: [existing-conditions, appendix]
function: qc
jurisdiction: all
source_redline: "SAH-014 (review finding)"
projects: [SAH]
added: 2026-10-22
```

## QC-0074 Model inputs read from records cite source
```yaml
id: QC-0074
rule: "Values read from record plans keep WSEL, banktop, crest, apron size and utility inverts in separate fields, depth is checked as WSEL minus invert in one datum, weir width is never taken from slab width or scaled from an NTS section, historical datum offsets stay unadopted until a monument tie is verified, local-model plan reads are reviewed by a supervisor, and every basin outlet element cites as-built, survey or a versioned owner assumption with implausible derived slopes flagged."
check: "Spot-check plan-read records against the source image; confirm each outlet element's source field; list derived slopes below 0.1 pct."
scope: [existing-conditions, hydrology]
function: data-gathering
jurisdiction: all
source_redline: "EKOS-LOCAL-014, EKOS-LOCAL-015 (review finding)"
projects: [EKOS-LOCAL]
added: 2026-10-22
```

## QC-0075 Footprint, easement and grading screening
```yaml
id: QC-0075
rule: "Screening areas are built from closed parcel polygons with a statement that parcels screen only and do not certify ROW, corridor surfaces have an explicit outer boundary and superseded exports are marked, cut and fill area and max depth inside each recorded easement are reported, new slopes steeper than 3:1 between adjacent cells are screened, max fill depth is compared with the geotech settlement basis and infiltration test locations with basin locations, and earthwork is reported as screening quantities."
check: "Read the overlap, slope and fill screens; confirm the surface used for hydraulics is the current export."
scope: [existing-conditions]
function: qc
jurisdiction: all
source_redline: "CAMPBELL-022, NORTHLOOP-017, SILVERBELL-008 (review finding)"
projects: [CAMPBELL, NORTHLOOP, SILVERBELL]
added: 2026-10-22
```

## QC-0076 Acreage from official boundary GIS
```yaml
id: QC-0076
rule: "Every acreage of development, preserve, habitat or swap land comes from a scripted overlap of the official property, preserve and parcel GIS logged with source, date and CRS, and is rerun and pushed to text, tables and figures in one pass after any layer update."
check: "Rerun the overlap script on the logged layer versions and compare with every acreage in the report."
scope: [existing-conditions, tables, pima-rfcd]
function: data-gathering
jurisdiction: all
source_redline: "TANGERINE-007 (review finding)"
projects: [TANGERINE]
added: 2026-10-22
```

## QC-0077 Incoming CAD, GIS and survey placed by known points
```yaml
id: QC-0077
rule: "Every incoming LandXML, CAD, shapefile or survey is checked against the model grid at three or more known points regardless of its declared EPSG or .prj, local site coordinates are transformed with the documented transform, LandXML is read in N, E, Z order and interpolated on its original triangles without extrapolation across voids, and the survey-vs-grid difference table (mean, std dev) explains every difference over 2 ft."
check: "Read the known-point log and the difference table for each incoming file."
scope: [crs, existing-conditions]
function: data-gathering
jurisdiction: all
source_redline: "STARVALLEY-014, NORTHLOOP-019 (review finding)"
projects: [STARVALLEY, NORTHLOOP]
added: 2026-10-22
```

## QC-0078 Datum, realization and units recorded
```yaml
id: QC-0078
rule: "Every survey used to set an elevation states its vertical datum and benchmark (else dependent elevations are labeled provisional), units are reconciled before any grid update, the horizontal datum realization of every layer (including .rasmap and .vrt projections) is recorded in the data log with mixed realizations flagged, and Pima County work defaults to NAD83(HARN) Arizona Central intl ft (EPSG:2868)."
check: "Read the data log CRS column; compare .rasmap, .vrt and delivered .prj EPSG codes; confirm the benchmark note in the survey."
scope: [crs, pima-rfcd]
function: data-gathering
jurisdiction: all
source_redline: "NORTHLOOP-019, SILVERBELL-007, DLR-002, STARVALLEY-014 (review finding)"
projects: [NORTHLOOP, SILVERBELL, DLR, STARVALLEY]
added: 2026-10-22
```

## QC-0079 Native output in the appendix
```yaml
id: QC-0079
rule: "The appendix holds native program output (PC-Hydro printouts and hydrographs, HEC-HMS results, HEC-RAS summaries, HY-8 reports, PFDS printouts); any extracted or compact sheet is titled \"extracted summary\" with values traced to the native file kept in the record; and software versions in the text (HEC-HMS 4.13, HEC-RAS 6.6 unless a logged decision says otherwise) match the versions on every printout."
check: "Open each appendix item and confirm it is a program printout or carries the extracted-summary title; compare version strings in text and printouts."
scope: [appendix, report-text]
function: report-assembly
jurisdiction: all
source_redline: "CALFIRE-015, RKN-015, ELTORO-010, RKN-018 (review finding)"
projects: [CALFIRE, RKN, ELTORO]
added: 2026-10-22
```

## QC-0080 Appendix titles, order and contents
```yaml
id: QC-0080
rule: "Each appendix title matches its contents and the software used, appendices run A, B, C, D with subparts (D-1, D-2) after the parent and channel calcs in their own subpart, the hydrology appendix holds the actual hydrologic basis (source-study discharge tables and a location map annotated to the sections used), general floodplain mapping is kept only if annotated, and every reference excerpt states source, section and purpose and cites only the governing manual for the jurisdiction."
check: "Compare appendix titles with contents; check appendix order in the TOC and bookmarks; read each excerpt's purpose note."
scope: [appendix]
function: report-assembly
jurisdiction: all
source_redline: "SAHPARK-011 (JCO redline); HOMEWOOD-015 (review finding)"
projects: [SAHPARK, HOMEWOOD]
added: 2026-10-22
```

## QC-0081 Appendix organization and removed analyses
```yaml
id: QC-0081
rule: "Appendices have bookmarks and sub-section dividers, storm events are ordered 2, 10, 100-yr with matching headings, offsite hydrology is grouped by event, analyses removed at agency request carry a short statement why with appendix names updated, and sections lacking references are filled or removed."
check: "Read appendix headings and bookmarks in order; search for removed-section references."
scope: [appendix]
function: report-assembly
jurisdiction: all
source_redline: "VALENCIA-021, VALENCIA-022 (JCO redline)"
projects: [VALENCIA]
added: 2026-10-22
```

## QC-0082 Hydraulic calc deliverables
```yaml
id: QC-0082
rule: "Once plans show a selected design, the appendix holds native output for that design (plan size, count, length and project-datum inverts) without option-comparison tables, or calc sheets for each open option; calcs use the licensed set (FHWA Hydraulic Toolbox, HY-8, Civil 3D hydraulic tools, HEC-RAS) or a named existing office spreadsheet, with FlowMaster and CulvertMaster treated as legacy and no new custom spreadsheet; and each printout is printed from the program on one page, not a screenshot."
check: "Compare calc inputs with plan dimensions and datum; list software per calc; check print areas and confirm no screenshot images."
scope: [appendix, culverts]
function: report-assembly
jurisdiction: all
source_redline: "SAHPARK-012, SAHPARK-013, VALENCIA-021 (JCO redline)"
projects: [SAHPARK, VALENCIA]
added: 2026-10-22
```

## QC-0083 Zero placeholders in transmitted files
```yaml
id: QC-0083
rule: "No transmitted report, letter, matrix or workbook contains placeholders ([DATE], TBC, TO BE CONFIRMED, [ ], bracketed notes) or code fragments; the package fails until the scan returns zero hits."
check: "Run the placeholder and code-fragment scan on every DOCX, XLSX and PDF in the package; attach the result."
scope: [package, comment-response]
function: qc
jurisdiction: all
source_redline: "STARVALLEY-004, STARVALLEY-005, STARVALLEY-020, SAH-013 (review finding)"
projects: [STARVALLEY, SAH]
added: 2026-10-22
```

## QC-0084 Assembly gate and open items
```yaml
id: QC-0084
rule: "A draft compiles for issue only when QC_Log Tier 1 has answers, CalcRegister is populated for a design report, every [FIGURE:F-nn] matches an ExhibitRegister ID, VERIFY library entries carry checked citations, and every assembly-report WARN, placeholder and human decision is closed; open items live in one internal QC open-items document and block compile unless JCO authorizes, in which case they are listed in a separate unresolved-items document."
check: "Read _ASSEMBLY_REPORT.md sections 1, 5 and 9, the QC_Log and CalcRegister counts and the open-items document; confirm JCO authorization for any open item."
scope: [package]
function: qc
jurisdiction: all
source_redline: "SAH-013, RKN-018 (review finding); VALENCIA-011 (JCO redline)"
projects: [SAH, RKN, VALENCIA]
added: 2026-10-22
```

## QC-0085 Checklist status agrees with open items
```yaml
id: QC-0085
rule: "Requirements-checklist rows use the status vocabulary Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale, rows resting on lidar culvert data, assumed bridge geometry, unknown layout or unconfirmed calibration are not marked Addressed, and deviations from the standard are listed as JCO decisions."
check: "Cross-check each checklist row against the open-items list; list rows marked Addressed that cite an open item."
scope: [package, comment-response]
function: qc
jurisdiction: all
source_redline: "CALFIRE-016, RKN-018 (review finding)"
projects: [CALFIRE, RKN]
added: 2026-10-22
```

## QC-0086 Transmittal control: freeze, hold list and final cleanup
```yaml
id: QC-0086
rule: "At a freeze, geometry edits and reruns stop and current CAD, plans, results and exhibits are packaged with checksums and unresolved items listed in the README; before transmittal, a search for every hold-until-final item returns zero hits, DRAFT is removed from the cover, the date and office address are current, author highlights are flattened, and no internal check markup or review note remains in text or exhibits."
check: "Run the hold-list search on the compiled PDF; check cover date and address; search annotations and exhibit notes for review markup."
scope: [package]
function: qc
jurisdiction: all
source_redline: "SILVERBELL-011, BARNETT-010, VALENCIA-020 (JCO redline)"
projects: [SILVERBELL, BARNETT, VALENCIA]
added: 2026-10-22
```

## QC-0087 Compiled PDF navigation
```yaml
id: QC-0087
rule: "The compiled PDF is built from the newest editable source through an assembly manifest, has bookmarks at minimum for cover, TOC, each main section, each appendix and each exhibit sorted by page, no hardcoded page numbers in prose, every bookmark, link and named destination resolving (checked by script and then in a native PDF reader), and a page-by-page comparison against the sources recorded in a QA JSON."
check: "Run the bookmark and link checker; open the PDF in a native reader; read the QA JSON page counts."
scope: [package]
function: compile-pdf
jurisdiction: all
source_redline: "TANGERINE-016, TANGERINE-011, CAMPBELL-020 (JCO redline); CALFIRE-014, VALENCIA-008 (review finding)"
projects: [TANGERINE, CALFIRE, CAMPBELL, VALENCIA]
added: 2026-10-22
```

## QC-0088 Compiled PDF print state, pages and size
```yaml
id: QC-0088
rule: "The compiled PDF has author highlights flattened, inherited plan revision clouds removed (originals kept), third-party FreeText annotations flattened or noted, placeholder pages only for named future items and labeled, no blank areas in the body, no unrequested appendices, and each file at or under 50 MB or the agency limit if lower (split otherwise)."
check: "List annotations by type in the compiled file; check file sizes against the agency limit; page through for blank or unlabeled placeholder pages."
scope: [package]
function: compile-pdf
jurisdiction: all
source_redline: "CALFIRE-014, VALENCIA-008, RKN-015, SAH-012 (review finding); CAMPBELL-020 (JCO redline)"
projects: [CALFIRE, VALENCIA, CAMPBELL, RKN, SAH]
added: 2026-10-22
```

## QC-0089 Package contents and hygiene
```yaml
id: QC-0089
rule: "Model files and excerpts of referenced reports go with the report, independent spreadsheet or Python checks stay in 40_QC and never in a deliverable, internal tools and scripts are not shipped, files from other projects are removed, the README states which files are new and where originals stay, and one final zip excludes temp, .bck and .sol files with its contents confirmed by a zip listing."
check: "List zip contents; search the package for .py, .skill, temp and other-project files; read the README."
scope: [package]
function: compile-pdf
jurisdiction: all
source_redline: "ELTORO-013, HOMEWOOD-022, DLR-006, HOMEWOOD-015 (review finding)"
projects: [ELTORO, HOMEWOOD, DLR]
added: 2026-10-22
```

## QC-0090 Model package outputs current
```yaml
id: QC-0090
rule: "Every model folder in a transmitted package has outputs newer than its newest input, no TMP files, headers and build strings that match the executable used, and no missing outputs."
check: "List member timestamps from the zips as uploaded; compare oldest output with newest input per folder; search for *.TMP."
scope: [package, model-runs]
function: qc
jurisdiction: all
source_redline: "STARVALLEY-005, STARVALLEY-004 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0091 Revisions start from the as-submitted version
```yaml
id: QC-0091
rule: "A revision of a submitted report or proposal starts from the as-submitted PDF, with totals and task text compared against the working files and differences and internal contradictions listed before editing."
check: "Confirm the as-submitted PDF is in the record and the difference list exists."
scope: [package, report-text]
function: qc
jurisdiction: all
source_redline: "BARNETT-013, CAMPBELL-023 (review finding)"
projects: [BARNETT, CAMPBELL]
added: 2026-10-22
```

## QC-0092 Comment log complete with status and disposition
```yaml
id: QC-0092
rule: "Every agency comment (each division tab, summary list and PDF markup) and internal redline is logged with a stable source-prefixed ID, copyedit or substantive tag, status (Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale), a separate disposition (incorporated / superseded / no change), revised location, Completed by and Check by, with no blank fields before issue."
check: "Compare the log row count with extracted annotations and xlsx rows; filter for blank status, disposition, Completed by or Check by."
scope: [comment-response]
function: qc
jurisdiction: all
source_redline: "BARNETT-001, BARNETT-002 (agency comment); SAHPARK-017 (JCO redline)"
projects: [BARNETT, SAHPARK]
added: 2026-10-22
```

## QC-0093 Response wording and placement
```yaml
id: QC-0093
rule: "Responses are one per comment, in completed tense, cite report section, table and figure numbers as displayed and cross-reference other responses by number; the log is an editable separate deliverable with a bound copy behind the cover where the agency asks, any appendix matrix named in the text is in the package, and agency acceptance status, open items and internal redline logs stay in internal records."
check: "Search responses for will; check each cited location exists; confirm the bound copy and appendix matrix are in the package; confirm no internal log is in the transmittal."
scope: [comment-response]
function: report-assembly
jurisdiction: all
source_redline: "CAMPBELL-015 (JCO redline); BARNETT-002, BARNETT-001 (agency comment)"
projects: [CAMPBELL, BARNETT]
added: 2026-10-22
```

## QC-0094 Responses verified against the issued files
```yaml
id: QC-0094
rule: "Before resubmittal each comment is checked in the issued text and files with page or section evidence (text-only exports marked Cannot Determine for graphics), each fix is carried to every related section, every response-letter claim cites a file and page in the package, and agency text repeated from a prior letter that the files disprove is marked Stale with file evidence."
check: "For each row open the cited page or file; search the whole report for the comment's term; list claims without a file and page."
scope: [comment-response, package]
function: qc
jurisdiction: all
source_redline: "BARNETT-001 (agency comment); STARVALLEY-005 (review finding)"
projects: [BARNETT, STARVALLEY]
added: 2026-10-22
```

## QC-0095 Pre-QC self-check before JCO review
```yaml
id: QC-0095
rule: "A draft goes to JCO QC only with a self-check findings list attached and zero open basic items (flow labels, return periods, numbering)."
check: "Confirm the findings list is attached to the QC transmittal and its basic-item count is zero."
scope: [comment-response, report-text]
function: qc
jurisdiction: all
source_redline: "SAHPARK-018 (JCO redline)"
projects: [SAHPARK]
added: 2026-10-22
```

## QC-0096 Mock review sets merged by source ID
```yaml
id: QC-0096
rule: "Mock or multi-platform review comments carry source-prefixed IDs, a report location, what is missing and the expected revision, duplicates are collapsed keeping the stricter wording with the raising set logged, and text written from a public or opposition view stays internal."
check: "Check ID prefixes are unique across sets; confirm no mock-review wording appears in the deliverable."
scope: [comment-response]
function: qc
jurisdiction: all
source_redline: "TANGERINE-001 (review finding)"
projects: [TANGERINE]
added: 2026-10-22
```

## QC-0097 FEMA package build and file gate
```yaml
id: QC-0097
rule: "Before a CLOMR or LOMR upload, each model folder shows FLOPRO.exe build = CONT.DAT line 1 build = SUMMARY.OUT build with all DLLs, all required inputs and outputs present (CHAN, CHANBANK, XSEC when ICHANNEL = 1; CHANMAX, CROSSMAX, HYDROSTRUCT, MAXWSELEV, DEPTH, ERROR.CHK), zero TMP files, oldest output newer than newest input, and SUMMARY.OUT showing a completed run with its volume conservation rating."
check: "Run package_qc on every folder; include package_QC_report.txt as a report appendix; fail the upload on any miss."
scope: [fema, package, flo2d]
function: jurisdiction-rules
jurisdiction: "FEMA"
source_redline: "STARVALLEY-004 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0098 FEMA cross-model identity, warnings and GIS
```yaml
id: QC-0098
rule: "CADPTS, INFLOW, OUTFLOW, FPXSEC, TOLER and RAIN hash identical across duplicate effective, existing and proposed models, text inputs pass the CRLF check, HYSTRUC rating tables equal the HY-8 export (names, discharge pairs, headwater offset), flood zone and BFE shapefiles exist for every condition, and an appendix tabulates every ERROR.CHK and runtime warning per model with inherited items (also in the duplicate effective) marked and a disposition for each."
check: "Run the hash and HY-8 comparison; list shapefiles per condition; compare the warnings appendix with each ERROR.CHK."
scope: [fema, package, flo2d]
function: jurisdiction-rules
jurisdiction: "FEMA"
source_redline: "STARVALLEY-004, STARVALLEY-020, STARVALLEY-001, STARVALLEY-003 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0099 FEMA additional-data responses and community items
```yaml
id: QC-0099
rule: "An additional-data response logs the 90-day deadline with the last model run at least 10 days before it, re-runs every model after its last input edit (including comparison existing conditions), gives each response row what changed with file, folder and report page, ships no status other than addressed, settles previously rejected decisions (e.g. concept-level phases) by call before resubmitting, and carries community-signed acceptance of flooding-source names, an O&M plan naming each required basin with the community as responsible party and a signature, and the CLOMR owner-notification template."
check: "Check the timeline log, model timestamps against input edits, the response matrix status column and the community letters and O&M plan in the package."
scope: [fema, comment-response]
function: jurisdiction-rules
jurisdiction: "FEMA"
source_redline: "STARVALLEY-006, STARVALLEY-017, STARVALLEY-018 (agency comment)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0100 Effective model complete before duplicate effective
```yaml
id: QC-0100
rule: "A duplicate effective study includes every storm case in the effective TDN (duration and depth) with its rainfall-runoff and detailed model inputs, uses effective inflows rather than county design flows for the FEMA comparison, claims no flood envelope from one storm, and any Zone A/AE, no-rise or CLOMR finding rests on a duplicate effective model."
check: "Compare the TDN storm list with the supplied package; confirm the duplicate effective model reproduces the effective results."
scope: [fema, hydrology, hydraulics-2d]
function: jurisdiction-rules
jurisdiction: "FEMA"
source_redline: "STARVALLEY-022, CALFIRE-011, SILVERBELL-001 (review finding)"
projects: [STARVALLEY, CALFIRE, SILVERBELL]
added: 2026-10-22
```

## QC-0101 FEMA 44 CFR 65.12 rise evaluation
```yaml
id: QC-0101
rule: "dWSE is computed as proposed MAXWSELEV minus existing, rises are evaluated where max depth >= 1.0 ft in both conditions with any-depth counts reported separately, new and removed SFHA cells are mapped, every cell over 1.00 ft is listed with ground change, depth change and location class (applicant land, approved grading, channel prism), and report values are quoted from the written rasters, polygons and summary JSON."
check: "Rerun the dWSE script and compare its summary JSON with report tables; review the over-1-ft cell list."
scope: [fema, hydraulics-2d, flo2d]
function: jurisdiction-rules
jurisdiction: "FEMA"
source_redline: "STARVALLEY-008 (review finding)"
projects: [STARVALLEY]
added: 2026-10-22
```

## QC-0102 Pima inlet clogging factors
```yaml
id: QC-0102
rule: "Curb openings and grates use RDM Table 2-9 clogging factors (0.80 curb openings, 0.50 grates, on grade and sump) applied as reduced effective length or area when the calculator has no clogging input, with no second reduction where a sump grate is already assumed blocked, inlet depression per PAG Standard Detail 305, and capture and bypass recomputed for 10-yr and 100-yr with no \"no bypass\" claim unless the calcs show it."
check: "Check effective length or area in each inlet calc; confirm one clogging reduction only; compare depression with Detail 305."
scope: [pima-rfcd, storm-drain]
function: jurisdiction-rules
jurisdiction: "Pima County RFCD"
source_redline: "VALENCIA-012 (agency comment)"
projects: [VALENCIA]
added: 2026-10-22
```

## QC-0103 Street spread and ROW velocity
```yaml
id: QC-0103
rule: "Street drainage reports show 10-yr max spread between curbs and ROW velocities below 3 fps (manual section to be confirmed per jurisdiction before citing)."
check: "Read the spread and velocity tables against the criteria; confirm the manual citation."
scope: [pima-rfcd, sahuarita, storm-drain]
function: jurisdiction-rules
jurisdiction: "Pima County RFCD; Town of Sahuarita"
source_redline: "ELTORO-011 (review finding)"
projects: [ELTORO]
added: 2026-10-22
```

## QC-0104 City of Tucson report outline
```yaml
id: QC-0104
rule: "City of Tucson drainage reports use the City manual outline as the section list with every section present, existing conditions split into hydrology (offsite and onsite watersheds with calcs) and existing stormwater infrastructure, and styles imported from the current firm template."
check: "Compare the TOC one to one with the City outline."
scope: [tucson, report-text]
function: jurisdiction-rules
jurisdiction: "City of Tucson"
source_redline: "TANGERINE-017 (JCO redline)"
projects: [TANGERINE]
added: 2026-10-22
```

## QC-0105 City of Tucson inlet capture and storm drain base
```yaml
id: QC-0105
rule: "Offsite watersheds near a City storm drain include the City storm drain, manholes and inlets on the base and assume each inlet captures the 100-yr flow unless shown otherwise."
check: "Check the base for the storm drain layer and the capture assumption statement."
scope: [tucson, hydrology, storm-drain]
function: jurisdiction-rules
jurisdiction: "City of Tucson"
source_redline: "TANGERINE-024 (JCO redline)"
projects: [TANGERINE]
added: 2026-10-22
```

## QC-0106 Critical facility above the 500-yr WSE
```yaml
id: QC-0106
rule: "Substation, BESS, utility or emergency facilities confirm critical-facility designation with the jurisdiction, place improvements above the 500-yr WSE plus any required freeboard, include a FEMA floodplain section stating the consequence where existing ground is below the 500-yr WSE, and show the 500-yr limit, 1-ft WSE contours and FEMA lettered cross sections on the exhibit."
check: "Compare the facility elevation table with the 500-yr WSE; confirm the designation record and exhibit content."
scope: [tucson, pima-rfcd, fema, exhibits]
function: jurisdiction-rules
jurisdiction: "City of Tucson; Pima County RFCD"
source_redline: "TANGERINE-021 (JCO redline)"
projects: [TANGERINE]
added: 2026-10-22
```

## QC-0107 Town of Marana governing manual and FEMA coordination
```yaml
id: QC-0107
rule: "Town of Marana reports cite the Town of Marana Drainage Manual (2024) and current versions of redone prior studies (not the superseded Northern Marana drainage requirements), and CLOMR/LOMR coordination names Pima County RFCD and the Town, with the Town signing the community acknowledgement form."
check: "Search the report for superseded document titles; check the coordination and signature block."
scope: [marana, report-text, fema]
function: jurisdiction-rules
jurisdiction: "Town of Marana"
source_redline: "BARNETT-004 (agency comment)"
projects: [BARNETT]
added: 2026-10-22
```

## QC-0108 Town of Marana design discharges and channels
```yaml
id: QC-0108
rule: "Town of Marana designs use non-regional discharges (MDM 4.1) with regional flows only where the facility is a regional channel or linear park, the regional and local qualifiers are defined once and used with every reference, collector channels carry 2 ft freeboard, and common-mesh existing and proposed runs support any no-adverse-impact text."
check: "Check the design discharge table qualifier column; check collector freeboard in the channel table; confirm matched-model runs for impact text."
scope: [marana, hydrology, culverts]
function: jurisdiction-rules
jurisdiction: "Town of Marana"
source_redline: "BARNETT-006, TANGERINE-003 (agency comment); NORTHLOOP-003 (review finding); NORTHLOOP-015 (JCO redline)"
projects: [BARNETT, NORTHLOOP, TANGERINE]
added: 2026-10-22
```

## QC-0109 Town of Marana critical facilities and FLO-2D build
```yaml
id: QC-0109
rule: "Town of Marana critical facilities set finished floor 1 ft above the 500-yr WSE with 500-yr delineation and erosion protection (Town Code 17-15-10 H), archived FLO-2D builds are treated as historical until accepted, and FLO-2D work uses the MDM 4.5 build or build 26.02.25 with written Town acceptance logged."
check: "Compare finished floor with the 500-yr WSE; check the build record and Town acceptance."
scope: [marana, flo2d, hydrology]
function: jurisdiction-rules
jurisdiction: "Town of Marana"
source_redline: "NORTHLOOP-003 (review finding)"
projects: [NORTHLOOP]
added: 2026-10-22
```

## QC-0110 Town of Sahuarita design events, citations and cutoff walls
```yaml
id: QC-0110
rule: "Town of Sahuarita and Pima County RFCD projects use the 10-yr and 100-yr design events, cite Town and County standards (no City of Tucson standards), and provide culvert cutoff walls per the local Development Criteria."
check: "Search for return periods outside 10 and 100-yr and for City of Tucson citations; check culvert details for cutoff walls."
scope: [sahuarita, pima-rfcd, report-text, culverts]
function: jurisdiction-rules
jurisdiction: "Town of Sahuarita; Pima County RFCD"
source_redline: "SAHPARK-003, SAHPARK-011, SAHPARK-020 (JCO redline)"
projects: [SAHPARK]
added: 2026-10-22
```

## QC-0111 Placer County manuals and hydrology method
```yaml
id: QC-0111
rule: "East Placer (Lake Tahoe Basin) work cites the East Placer manual and SWQP template (not West Placer), uses Small Watershed peaks only for inlet and upper-system pipe sizing with storage, peak control and HGL shown by a hydrograph method, and runs every hydrology case with both West and East of crest values compared with NOAA Atlas 14 at the site, with the selected basis confirmed by the County in writing."
check: "Search for West Placer citations; check that storage calcs use a hydrograph method; confirm both crest cases and the County confirmation."
scope: [placer, hydrology]
function: jurisdiction-rules
jurisdiction: "Placer County CA (East Placer / TRPA)"
source_redline: "HOMEWOOD-013, HOMEWOOD-012, HOMEWOOD-011 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0112 Placer County storm drain criteria
```yaml
id: QC-0112
rule: "Placer County storm drains are designed for the 10-yr event with HGL at least 0.5 ft below rim or grate, the same freeboard checked for the 50-yr 1-hr event, and the 2-yr 24-hr event rerun after any outlet change."
check: "Read the freeboard table for each event against the 0.5 ft criterion."
scope: [placer, storm-drain]
function: jurisdiction-rules
jurisdiction: "Placer County CA (East Placer / TRPA)"
source_redline: "HOMEWOOD-006, HOMEWOOD-010 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0113 Placer County water quality volume
```yaml
id: QC-0113
rule: "The 85th percentile WQV is retained or infiltrated, SWQP Form 3-1 uses the actual site elevation, WQV back-checks as impervious area x runoff coefficient x unit depth with the memo depth matching, the 85th percentile 24-hr depth is not equated with the 50-yr 1-hr depth, the WQ depth is flagged for confirmation from the East Placer manual, and DMA impervious areas have one source across memo, exhibit and template."
check: "Recompute WQV from the DMA table; compare depths in memo and template; compare DMA areas across documents."
scope: [placer, storm-drain, hydrology]
function: jurisdiction-rules
jurisdiction: "Placer County CA (East Placer / TRPA)"
source_redline: "HOMEWOOD-008 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0114 Placer County hydromodification forms
```yaml
id: QC-0114
rule: "SWQP Forms 4-2 and 4-3 use the full site area checked against survey, 2-yr rainfall at Tt (not a 1-hr WQ depth), a YES/NO answer that agrees with the computed post and pre numbers, and provided volume at least the required volume or routed model results per SWQP Sec. 4.4."
check: "Compare form site area with survey acreage; recompute the YES/NO answer; compare provided and required volume."
scope: [placer, hydrology]
function: jurisdiction-rules
jurisdiction: "Placer County CA (East Placer / TRPA)"
source_redline: "HOMEWOOD-014 (review finding)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0115 Placer County BMP siting, infiltration and gallery depth
```yaml
id: QC-0115
rule: "Each infiltration BMP documents SHGW at its footprint with the bottom at least 5 ft above SHGW (or a move, redesign or variance), uses a field infiltration rate at BMP depth or until tested half the NRCS rate with a 0 in/hr sensitivity (to be confirmed with the County), sizes subsurface infiltration for at least the TRPA 20-yr 1-hr volume from tributary impervious area with stated void ratios, and computes required depth from finished grade to SHGW under pavement as pipe diameter + bedding + cover to the bottom of the structural section + structural section + required separation."
check: "Check SHGW records per BMP; recompute required depth and TRPA volume; confirm the infiltration rate source and sensitivity run."
scope: [placer, storm-drain]
function: jurisdiction-rules
jurisdiction: "Placer County CA (East Placer / TRPA)"
source_redline: "HOMEWOOD-009, HOMEWOOD-013 (review finding); HOMEWOOD-017 (team markup)"
projects: [HOMEWOOD]
added: 2026-10-22
```

## QC-0116 Caltrans bridge data and hydrology review
```yaml
id: QC-0116
rule: "Caltrans and California crossings take bridge span, length, deck width and channel rating from DOT as-builts and the NBI record with low chord and pier width flagged as assumptions until confirmed, and any calibrated CN hydrology is listed for District Hydraulics confirmation."
check: "Check bridge inputs against NBI and as-builts; confirm the assumption flags and open-items entry."
scope: [caltrans, hydraulics-2d, hydrology]
function: jurisdiction-rules
jurisdiction: "Caltrans"
source_redline: "CALFIRE-011, CALFIRE-007 (review finding)"
projects: [CALFIRE]
added: 2026-10-22
```
