# EXH - Exhibits group: reconciled clusters

Group file: group_exhibits.json (30 cards, 14 projects). Each card is scored in one primary cluster only; "Also cited" lists cards whose content is merged into a cluster but scored elsewhere.
Score = sum(hours_lost x recurrence). QC-rule recurrence values mostly count individual redline comments (e.g., BARNETT-008 = 40 comments, TANGERINE-022 = 12, CAMPBELL-018 = 20), so QC clusters rank high on comment volume, not hours.

Standing requirement (already in drainage-report-exhibit-standards and not repeated as new content): every map carries north arrow, scale bar, horizontal and vertical datum, and a legend that defines every class interval and symbol. Cards that restate it are listed under the cluster as confirmations.

Source tag key: "JCO QC redline" = EOR redline on a draft PDF; "agency redline" = reviewing-agency comments; "EOR instruction" = written EOR standard or correction; "Codex session" = transcript of a Codex run; "script log" = script, log or README evidence; "file history" = repeated versions in a project folder.

---

### EXH-C01 Scripted exhibit sheet framework (11x17 sheet module, one script per set)
skill | target: new skill `scripted-exhibit-sheets` (referenced from drainage-report-exhibit-standards §3; exhibit-reviewer runs the review pass, see EXH-C02) | score 49.2 | hours 9.3 | cards 4 | projects 4 | confidence medium-high

Trigger: Report, memo, proposal or presentation exhibits produced from GIS layers and model rasters by script (matplotlib/rasterio/geopandas) instead of QGIS or CAD layouts.

Steps (merged):
1. Before building anything, confirm with the PM/EOR whether figures must be editable by others. If yes, build in QGIS or CAD from the start, not as scripted images. If scripted, log the use of Python instead of QGIS layouts as a deviation for EOR decision. (TANGERINE-006, RKN-012)
2. Finish the figure list (IDs, titles, extents, storms, conditions) before the first export. (TANGERINE-006)
3. Fix one sheet template first: page size and orientation (11x17 landscape default), margins, title block at bottom, legend, north arrow and scale bar placed in the margin, datum note, basemap source/year credit line, minimum text 0.1 in. (ELTORO-015, RKN-012, SAH-019, TANGERINE-022)
4. Use one CRS for all layers; check every .prj / world-file sidecar and record any CRS assumed from file names on the sheet. (TANGERINE-006, TANGERINE-008)
5. Basemap: current aerial (NAIP or local aerial service) plus hillshade where useful; credit imagery source and date on each sheet (imagery date can differ from lidar date). (RKN-012, SILVERBELL-017)
6. Provide shared symbology helpers: watersheds, flowlines with arrows, sheet-flow arrows, CP labels with Q100, depth classes; pick one depth color ramp and one overlay opacity before rendering any sheet. (RKN-012, ELTORO-015)
7. Place dense labels with callouts (leader lines, minimum spacing, staggered rows) rather than fixed offsets; drive label text and positions from a register table (EXH-C11). (RKN-012, ELTORO-016)
8. Generate every sheet of the set (overview + north/mid/south, existing + proposed) from one script that takes figure IDs as arguments, so a style change re-renders the whole set. Use the same scale, classes and legend on existing and proposed sheets. (ELTORO-015, SAH-019, TANGERINE-006)
9. Show protected areas, property boundary, parcels, roads, easements and named washes on every map sheet; add large-scale insets or typical sections where the text cites a corridor width. (TANGERINE-006)
10. Split dense maps into 1of2/2of2 sheets with match lines (EXH-C03). (SAH-019)
11. Export full-size PDF and PNG with the margin visible in both; combined PDF with one bookmark per figure. Keep editable slides with native tables when the output is a presentation. (ELTORO-015, TANGERINE-006, SILVERBELL-017)
12. Save outputs with an incrementing suffix (v2, v3), never overwrite; write issued exhibits to 10_Record\X_Exhibits and register each in the ExhibitRegister with the template figure ID; keep superseded sets in 10_Record. Save the source/extent JSON used for each sheet. (TANGERINE-006, SAH-019, SILVERBELL-017, NORTHLOOP-011)
13. Hand the rendered set to the exhibit-reviewer pass (EXH-C02) before compile.

Gotchas:
- Scripted matplotlib PDFs could not be edited by the user, who later asked for the figures to be recreated in QGIS or CAD. (TANGERINE-006, claude via Codex session)
- Using Python instead of QGIS layouts is a deviation that must be logged for EOR decision. (RKN-012, claude script log)
- Three exhibit versions were exported within about 2.3 hr on submittal morning (v1, v2 adding Figure 12, v3 16 min later); finish the figure list before export. (TANGERINE-006, claude via Codex session)
- A DRAFT date in every title block forces replotting the whole set when the date changes. (TANGERINE-006, claude via Codex session)
- Reviewers found report-scale figures too dense and the Preserve boundary missing; full-size sheets and the Preserve polygon on every map closed comments B-1, P2-7, P2-8. (TANGERINE-006, claude via Codex session)
- Reviewer markup: move legend, scale bar and north arrow into the margin; show the margin in the PNG as well as the PDF; cut the top margin by 50%. (ELTORO-015, claude from reviewer markup)
- About 45 depth exhibit files were produced (v2-v6, three opacity variants, four sheets each in 11x17 and 8.5x11 landscape and portrait) because template, ramp and opacity were not fixed first. (ELTORO-015, claude file history)
- Fixed-offset labels overlapped; replaced with a callouts() helper on E and P2 sheets and staggered offsite-watershed labels. (RKN-012, claude script log)
- A filter on BC line type returned an empty layer and BC lines silently dropped off an exhibit; warn on empty layers (see EXH-C04). (RKN-012, claude script log)
- Road profile exhibit first showed the raw grade-following profile; reduce to tangent grades between PVIs and label percent grade. (RKN-012, claude script log)
- Exhibit scripts were rerun about 6 times in one day; largest rework item after report formatting. (RKN-012, claude script log)
- Image date can differ from lidar date; credit imagery source on each exhibit. (SILVERBELL-017, claude script log)

Jurisdiction add-ons:
- Town of Marana: project CRS NAD83 AZ Central (ft, intl) used on the concept report; confirm per project. (TANGERINE-006)

QC checks:
- Editable-or-scripted decision recorded before build; deviation logged if scripted.
- All layers share one CRS; CRS assumptions noted on sheet.
- Existing and proposed sheets share scale, classes and legend.
- Margin, legend, north arrow, scale bar visible in PDF and PNG.
- File suffix incremented; superseded set kept in 10_Record; ExhibitRegister updated.

Source cards: RKN-012, ELTORO-015, TANGERINE-006, SILVERBELL-017. Also cited: ELTORO-016, SAH-019, NORTHLOOP-011, TANGERINE-008, TANGERINE-022.

---

### EXH-C02 Exhibit render-and-review pass (independent check before compile)
agent | target: agent `exhibit-reviewer` (checklist = QC rules from EXH-C03 to C07 and C10, written to 05_QC_Rules) | score 16 | hours 3.5 | cards 2 | projects 2 | confidence medium-high

Trigger: Any exhibit set is rendered or re-rendered, before it goes into the compiled report, memo, proposal or presentation.

Steps (merged):
1. Render every sheet in the set to PNG (and PDF QA images) into a dated QC folder: 40_QC\JO_<date>_exhibit_review\rev, r2, r3 ... Keep figure ID and title in each PNG name. (SAH-019, SILVERBELL-017, RKN-012)
2. Review all sheets in one pass against the exhibit checklist (sheet standards C03, legends C04, base content C05, location map C06, result symbology C07, FEMA content C10), recording every finding before any fix. (SAH-019, TANGERINE-022)
3. Fix a finding on one figure, then apply the same fix to every figure that shares it; re-render the full set once. (TANGERINE-022, SAH-019)
4. Check that every exhibit has a figure/exhibit number cited in the text and that numbering matches the TOC and the text. (CAMPBELL-018, VALENCIA-023, BARNETT-008)
5. Check pending values are marked pending and unmodeled concepts are labeled as such. (NORTHLOOP-011)
6. For a layout comparison exhibit (prior study vs current plan): use the figure of the alternative the prior report actually adopted; note if drawings are not survey-registered; build 11x17 landscape sheets: (1) prior figure vs current plan with numbered drainage callouts, (2) current layout on full-coverage aerial, (3) any unmodeled concept, clearly labeled. (NORTHLOOP-011)
7. Issue only after a clean pass; move superseded exhibits to 10_Record. (NORTHLOOP-011)

Gotchas:
- Eight review rounds were rendered in one day; rounds r2 to r4 came within 7 min, so check all sheets in one pass before re-rendering. (SAH-019, claude QC render folder)
- File names were truncated in round r3; keep figure ID and title in the PNG name. (SAH-019, claude QC render folder)
- First comparison exhibit was one 24x18 sheet with text legends and was rebuilt to three 11x17 sheets after the EOR standards arrived (about 2 h). (NORTHLOOP-011, claude from EOR instruction)
- Brand package was not available; neutral styling used and no brand claim made. (NORTHLOOP-011, claude from EOR instruction)
- 12 exhibit comments on three figures, several repeated on each figure; fixing one figure and copying the fix to the rest saves review cycles. (TANGERINE-022, claude from JCO QC redline)

QC checks:
- PNG render of every sheet exists for the current revision.
- One complete checklist pass logged per revision.
- Figure numbering continuous, cited in text, matches TOC.
- Preparer shown as Psomas (initials); no footer date; minimum text size met.

Source cards: SAH-019, NORTHLOOP-011. Also cited: RKN-012, SILVERBELL-017, TANGERINE-022, CAMPBELL-018, VALENCIA-023, BARNETT-008.

---

### EXH-C03 Sheet standards: border, engineering scale, orientation, numbering, style consistency
qc_rule | target: update drainage-report-exhibit-standards §3 + QC rule (05_QC_Rules) | score 83 | hours 3 | cards 2 | projects 2 | confidence high

Trigger: Any exhibit or figure placed in a report body or appendix; final compile check of any report with graphics and abbreviations.

Steps (merged):
1. Use the standard Psomas exhibit border (11x17 default; 8.5x11 for memo inline figures; portrait or landscape); get the template from the CAD/GIS lead if not on hand. (SAHPARK-008)
2. Use one orientation for all exhibits in a set (title block at bottom); rotate the north arrow, not the sheet layout. (TANGERINE-022)
3. Set the viewport to an engineering scale (1 in = 100, 200, 500 ft, etc.) with a matching scale bar; measure the bar on the plotted sheet against the stated scale. (SAHPARK-008)
4. Add match lines and a sheet key when an exhibit spans more than one sheet. (SAHPARK-008, SAH-019)
5. Label all graphics either Figure or Exhibit (not both), numbered in order with none missing, matching the TOC; give every exhibit a number cited in the report. (BARNETT-008, CAMPBELL-018, VALENCIA-023)
6. Reject pixelated images; every symbol on a map has a legend entry (see EXH-C04). (BARNETT-008)
7. Use one style for agency names and abbreviations (spell out on first use), dollar amounts, model names (FLO-2D), ROW, Frontage Road, dimensions (10 ft); run a consistency search for each variant before issue. (BARNETT-008)
8. Minimum new text height on exhibits per §3 (0.1 in); see conflict EXH-X04 for the 9 pt value. (NORTHLOOP-011, RKN-012)

Gotchas:
- Draft scale bar measured 2.4 in per 1,000 ft, not a usable scale; Rev A set 1 in = 200 ft on 11x17. (SAHPARK-008, claude from JCO QC redline)
- The 30% DCR still had 17 Figure and 15 Exhibit labels side by side; about 25 reviewer comments were on legibility or legends. (BARNETT-008, claude from agency redline)

QC checks:
- Scale bar measured on plotted sheet = stated scale.
- One label type (Figure or Exhibit), continuous numbering, matches TOC and text citations.
- Consistent orientation and title-block position across the set.
- Match lines/sheet key on multi-sheet exhibits.
- No pixelated raster images; style-variant search run before issue.

Source cards: SAHPARK-008, BARNETT-008. Also cited: TANGERINE-022, SAH-019, CAMPBELL-018, VALENCIA-023, NORTHLOOP-011, RKN-012.

---

### EXH-C04 Legends: graphic samples, only symbols present, warn on empty layers
qc_rule | target: update drainage-report-exhibit-standards §3 + QC rule; empty-layer check also coded into `scripted-exhibit-sheets` | score 1 | hours 1 | cards 1 | projects 1 (plus 7 citing cards across 6 projects) | confidence high

Trigger: Any GIS, CAD or model exhibit with a legend, including viewer/dashboard legends.

Steps (merged):
1. Each legend entry shows the real mapped symbol (color, line weight and style, arrow, fill, hatch) with a concise feature label beside it; no text descriptions of symbology. (NORTHLOOP-012, NORTHLOOP-011)
2. Every symbol on the sheet (flow arrows, hatches, lines) appears in the legend; repeat a legend fix on every exhibit in the set. (TANGERINE-022, BARNETT-008)
3. Include only symbols present on the sheet; if a layer has no features in the frame, drop its legend entry or state "none mapped". (NORTHLOOP-012, CALFIRE-017)
4. Scripts test every filtered layer for a non-empty result and stop or warn before rendering. (CALFIRE-017, RKN-012)
5. Name legend entries by condition: existing vs proposed clearly separated; no ambiguous entries such as "Proposed Road" vs "Road Lines". (SAHPARK-007, HOMEWOOD-020)
6. Result maps: legend defines every class interval (standing requirement) and states units. (CAMPBELL-016, SAHPARK-006)

Gotchas:
- Legends describing symbology in words were rejected by the EOR and replaced. (NORTHLOOP-012, claude via Codex session, EOR correction)
- Legend shown with the full map checklist: north arrow, scale, datums, credits (confirms standing requirement). (CAMPBELL-016, claude from JCO QC redline)
- GeoPandas warned the 0.2% subset was empty and the figure was issued anyway. (CALFIRE-017, claude script log)
- BC-line filter returned an empty layer and BC lines silently dropped off an exhibit. (RKN-012, claude script log)
- Draft legend: "Proposed Road" covered only the roundabout and "Road Lines" mixed existing and proposed. (SAHPARK-007, claude from JCO QC redline)

QC checks:
- Legend entry for every symbol shown; no entry for absent symbols.
- Graphic sample, not words, for every entry.
- Script log shows no empty-layer warnings, or each is resolved/noted.

Source cards: NORTHLOOP-012. Also cited: NORTHLOOP-011, TANGERINE-022, BARNETT-008, CALFIRE-017, RKN-012, SAHPARK-007, HOMEWOOD-020, CAMPBELL-016, SAHPARK-006.

---

### EXH-C05 Drainage map base content and labeling
qc_rule | target: update drainage-report-exhibit-standards §3 (drainage map symbology/labels) + QC rule | score 76 | hours 6.5 | cards 4 | projects 4 | confidence high

Trigger: Existing/proposed drainage maps, watershed maps, pavement drainage maps and result/floodplain exhibits, especially for roadway reports.

Steps (merged):
1. Locate the site: label major roads on every exhibit plus a few local/subdivision roads; in sparse areas label key landmarks (school, major adjacent parcel, the facility the project serves). (SAHPARK-007, CAMPBELL-018)
2. Label existing culverts and bridges, at-grade crossings, wash names and well sites. (CAMPBELL-018)
3. Show existing and proposed drainage infrastructure with sizes: culverts (count of cells, size, type), channels, berm segments and limits where the berm is raised; label known culvert size and cells, and both design-plan Q and calculated Q. (SAHPARK-007, TANGERINE-022)
4. Label every structure number on drainage maps (Q not required on pavement drainage maps). (VALENCIA-023)
5. Label curb and scupper outfalls with arrows and Q values. (CAMPBELL-018)
6. Draw berms as thick colored lines with basic dimensions. (CAMPBELL-018)
7. Show storm drains as storm drain (sketched from as-builts and aerials), not as part of the wash network. (TANGERINE-022)
8. Thicker watershed lines; flow direction arrows; wipeouts behind labels; move labels inside the sheet. (CAMPBELL-018, VALENCIA-023)
9. Screen back contours so roads and labels stand out; use solid or tight-dash lines; explain any red lines or remove them. (VALENCIA-023)
10. Draw proposed linework only for proposed; label existing roads or give them a different linetype; name layers by condition. (SAHPARK-007)
11. Show proposed road and culvert linework on result maps. (CAMPBELL-018)
12. Shade the subject parcel darker but not solid; label parks and neighbors; name parcels neutrally (parcel or owner type), never with draft/working labels. (TANGERINE-022)
13. Show protected areas, property boundary, parcels, easements and named washes on every map sheet. (TANGERINE-006)

Gotchas:
- RAS screenshots were allowed early but still needed these labels. (CAMPBELL-018, claude from JCO QC redline)
- Draft exhibit had no road labels, no culverts and an ambiguous road legend. (SAHPARK-007, claude from JCO QC redline)
- The destination facility the road is built for was not labeled. (SAHPARK-007, claude from JCO QC redline)
- Structure numbers were missing on all proposed drainage maps. (VALENCIA-023, claude from JCO QC redline)
- 12 exhibit comments on three figures, several repeated on each figure. (TANGERINE-022, claude from JCO QC redline)

Jurisdiction add-ons:
- Pima County RFCD roadway reports: outfall Q labels and berm dimensions expected on drainage maps. (CAMPBELL-018)
- City of Tucson/Pima County: design-plan Q and calculated Q both labeled at culverts. (TANGERINE-022)

QC checks:
- Major roads and landmarks labeled on every sheet.
- Every culvert labeled with cells, size, type; every structure numbered.
- Existing vs proposed distinguishable by layer/linetype and legend.
- Contours screened; no unexplained red lines; labels inside sheet with wipeouts.
- No draft or working names on parcels.

Source cards: CAMPBELL-018, SAHPARK-007, VALENCIA-023, TANGERINE-022. Also cited: TANGERINE-006.

---

### EXH-C06 Location / vicinity / project-area map and defined limit terms
qc_rule | target: update drainage-report-exhibit-standards §3 (Location/Vicinity figure) + QC rule | score 20 | hours 2 | cards 1 | projects 1 (plus 3 citing cards, 3 projects) | confidence high

Trigger: Any drainage report or concept report; especially long channel or linear-park corridors with several study areas.

Steps (merged):
1. Provide one project-area map early in the report showing study limits, affected properties and reference features (canal, railroad, river, interstate). (BARNETT-007)
2. Location map at about 1 in = 3 mi, taken from the design plans when available, with township-section-range; no aerial or FEMA layers on the location map (see conflict EXH-X05). (TANGERINE-022)
3. Label major roads and landmarks so the site can be located. (SAHPARK-007)
4. Crop location images to remove stationing and other plan clutter. (VALENCIA-023)
5. Pick one term for project limits; define how vicinity, study limits and project area differ, or stop using the extras. (BARNETT-007)
6. Use defined section zones (Top of Channel, Overbank Terrace, low-flow channel) only for those zones; do not call other areas overbank. (BARNETT-007)
7. Explain regional study-area figures borrowed from master plans, or remove them. (BARNETT-007)

Gotchas:
- "Overbank" appeared 29 times in mixed meanings and "corridor" 44 times after the reviewer asked for defined limits. (BARNETT-007, claude from agency redline)

Jurisdiction add-ons:
- Town of Marana corridor DCRs: reviewer expects one project-area map and restricted defined terms. (BARNETT-007)

QC checks:
- One project-area map near the front; single defined term for limits; zone terms used only as defined (term-count search).
- Location map scale, T-S-R and road labels present; borrowed figures explained.

Source cards: BARNETT-007. Also cited: TANGERINE-022, SAHPARK-007, VALENCIA-023.

---

### EXH-C07 2D result exhibits: depth and difference symbology, storm sets, inflow labels
qc_rule | target: update drainage-report-exhibit-standards §3 (new "Result maps" subsection) + QC rule; add symbology/preview step to hecras-result-rasters §QC | score 19 | hours 5.5 | cards 3 | projects 2 | confidence high

Trigger: Any HEC-RAS 2D or FLO-2D depth, velocity, WSE or proposed-minus-existing difference exhibit over aerial imagery.

Steps (merged):
1. Depth maps: semi-transparent depth classes over the aerial; distinct colors and clean class breaks (default set in dispute, see EXH-X01/X02/X03): SAHPARK-006 set 0-0.2 ft not displayed, 0.21-0.50 yellow, 0.51-1.00 cyan, 1.01-2.00 blue, 2.01-3.00 orange, >3 red; CAMPBELL-018 set 0-3, 3-5, 5-10, >10 ft. (SAHPARK-006, CAMPBELL-018, TANGERINE-006)
2. Set the legend range to depths in the area of interest, not the raster min-max stretch; no 3-decimal breaks. (SAHPARK-006)
3. Check the max depth; an implausible value (e.g., 48 ft on a piedmont) is a rendering or terrain artifact; find it before publishing. (SAHPARK-006)
4. Difference maps (proposed minus existing WSEL or depth): show increases only; blank zero and decreases; default classes yellow 0-0.10, cyan 0.10-0.25, green 0.25-0.50, blue 0.50-1, orange 1-2, red >2 ft, continuous bounds; turn off values under 0.10 ft for impact maps when asked; hatch newly wet ground separately or drop it on request. (CAMPBELL-016)
5. Difference sign and wet/dry handling stated on the sheet (WSE difference only where both scenarios wet; depth difference treats dry as 0 ft). (DLR-005)
6. Pair a velocity change exhibit with every WSEL change exhibit. (CAMPBELL-016)
7. Base: aerial at about 52% overlay, 2-5 ft contours, structure labels, easement notes; proposed road and culvert linework on result maps. (CAMPBELL-016, CAMPBELL-018)
8. Use the same scale, classes and legend on existing and proposed sheets. (TANGERINE-006)
9. Produce a separate exhibit set for each storm analyzed in the text, with the storm in the title block. (SAHPARK-009)
10. Show every model inflow location as a cross-section line labeled with ID and peak Q for that storm; cross-reference exhibit IDs to the design discharge table. (SAHPARK-009, ELTORO-016)
11. Fix class breaks with the EOR before rendering, then push the same breaks into report text and tables in one change. (CAMPBELL-016, ELTORO-015)

Gotchas:
- Difference classes were re-cut three times (fine bands 0.1/0.15/0.2/0.25), and each change had to be pushed into the report too. (CAMPBELL-016, claude from JCO QC redline + Codex session)
- Legend shown with the full map checklist: north arrow, scale, datums, credits. (CAMPBELL-016, claude from JCO QC redline)
- Default stretched legend showed breaks at 3 decimals and a 48.898 ft top bin from an artifact. (SAHPARK-006, claude from JCO QC redline)
- Opaque raster hid the aerial base. (SAHPARK-006, claude from JCO QC redline)
- Text said 10-yr and 100-yr were analyzed but only one unlabeled map was provided. (SAHPARK-009, claude from JCO QC redline)
- 10-yr corridor depth mapping was not in the regional study record obtained; request it early. (SAHPARK-009, claude from JCO QC redline)
- RAS screenshots still need full labels. (CAMPBELL-018, claude from JCO QC redline)

Jurisdiction add-ons:
- Pima County RFCD: difference-map class set and increases-only display per CAMPBELL-016 (if adopted as default, move to core).
- Town of Sahuarita/Pima County RFCD: depth class set per SAHPARK-006 (pending conflict resolution).

QC checks:
- Legend range set to area of interest; no stretched/3-decimal legends; units shown.
- Max depth/value checked for artifacts.
- One exhibit set per storm named in text; inflow XS labeled with peak Q matching discharge table.
- Difference sign, wet/dry rule and display threshold stated.
- Velocity change exhibit present with WSEL change exhibit.

Source cards: CAMPBELL-016, SAHPARK-006, SAHPARK-009. Also cited: CAMPBELL-018, TANGERINE-006, DLR-005, ELTORO-015, ELTORO-016.

---

### EXH-C08 Result raster provenance, naming and delivery package
skill | target: update hecras-result-rasters (naming, data dictionary, terrain export, received-set check) | score 1.5 | hours 0.5 | cards 2 | projects 1 | confidence medium-high

Trigger: Exporting, receiving or delivering max depth, WSE, velocity and difference rasters for several scenarios of one 2D model.

Steps (merged):
1. Received sets: list entry dates inside every result zip and the model Result_Rasters folder; treat files or zips marked VOID, and copies older than the latest final zip, as superseded. Sort by entry dates, not file names. (DLR-004)
2. Build a table of variable x scenario x source zip x date; flag variables that exist only in a VOID set; check date consistency between variables in the final set. (DLR-004)
3. Map and sample only from the final set; list any variable that must be regenerated. (DLR-004)
4. Name outputs condition_event[_future][_mitigation]_variable.tif (e.g., Baseline2025_500_LTR_Mitigate_FW_Depth.tif); put differences in a Differences subfolder with a _Difference suffix (see conflict EXH-X09 with the current script naming). (DLR-005)
5. Use the same token in the file name, plan title and data dictionary for each scenario; list the plan number for each token. (DLR-005)
6. Define the difference sign once (mitigated minus base, negative = improvement); state that WSE differences are valid only where both scenarios are wet and depth differences treat dry as 0 ft. (DLR-005)
7. Deliver a README and a field dictionary CSV with any sampled point table (field, plan, scenario, variable, units, sign, source raster). (DLR-005)
8. Export the terrain used for depth as its own raster per scenario so the receiver can recompute depth. (DLR-005)

Gotchas:
- Rasters and the spot elevation table inside the model folder were the earlier set later marked VOID; final depth and depth-difference rasters were dated weeks later in a separate zip. (DLR-004, claude received data review)
- The final set mixed dates (WSE and velocity from one date, depth and difference from a later date, points from a third); check consistency between variables. (DLR-004, claude received data review)
- WSE difference rasters existed only in the VOID set; the final difference zip held depth differences only. (DLR-004, claude received data review)
- A VOID zip name carried a typo in the year; sort by entry dates, not by file name. (DLR-004, claude received data review)
- Without the plan number in the dictionary the receiver cannot tie a raster to a run when plan titles and file tokens differ (TDAFW vs Mitigate_FW). (DLR-005, claude received data review)

QC checks:
- Source-set table built; no VOID-set variable used.
- Every delivered raster maps to a plan number in the dictionary.
- Terrain raster delivered per scenario; difference sign and wet/dry rules documented in README.

Source cards: DLR-004, DLR-005.

---

### EXH-C09 FLO-2D output to GIS rasters and FEMA zone delineation
skill | target: new skill `flo2d-result-mapping` (core: TANGERINE-008) + jurisdiction add-on `flo2d-result-mapping/FEMA` (CLOMR/LOMR work-map zones: STARVALLEY-009) | score 13 | hours 7 | cards 2 | projects 2 | confidence high

Trigger: A FLO-2D model or export (TOPO.DAT, DEPTH.OUT, MAXWSELEV.OUT, MapCrafter rasters) must be mapped as max depth/WSE, or Zone AE/AO delineations and BFE contours are needed for a CLOMR/LOMR work map.

Steps (merged):
1. Read TOPO.DAT, DEPTH.OUT and MAXWSELEV.OUT; assert their cell coordinates match. (TANGERINE-008)
2. Grid values on the model cell size (100 ft in the source case) using the bounds of a correctly tagged reference raster. (TANGERINE-008)
3. Before using any supplied raster, compare arrays and CRS tags of apparent duplicates. (TANGERINE-008)
4. Take WSE directly from MAXWSELEV.OUT; do not derive it from depth plus a different terrain. (TANGERINE-008)
5. Mask dry cells (WSE coded 0) and depths below the display threshold (0.1 ft in source case, see EXH-X02); keep cell edges visible. (TANGERINE-008)
6. Compute WSE - terrain - depth residuals on wet cells only. (TANGERINE-008)
7. Clip FEMA S_FLD_HAZ_AR, S_BFE, S_XS, S_LOMR to the extent; label the sheet a source review draft until return period, condition and vertical datum are confirmed; record any CRS assumed from file names or world files on the sheet. (TANGERINE-008)
FEMA add-on (work maps):
8. Use the depth-to-zone table of the effective study (source case: <1 ft X; 1.0-1.5 AO(1); 1.5-2.5 AO(2); 2.5-3.0 AO(3); >3 ft AE). (STARVALLEY-009)
9. Assign AE to channel cells, the connected inundated corridor along each 1D channel segment, and detention basins. (STARVALLEY-009)
10. Generate 1-ft BFE contours inside AE from MAXWSELEV. (STARVALLEY-009)
11. Write effective/existing/proposed zone shapefiles with an acreage table; map vector delineations, not depth rasters, on the work map. (STARVALLEY-009)
12. Include the zone shapefiles in the GIS package and confirm they match the work map. (STARVALLEY-009)

Gotchas:
- A MapCrafter MAXIMUM_DEPTH.tif carried a California CRS tag (EPSG 3498) while its identical twin carried AZ Central EPSG 2223; compare arrays and CRS before use. (TANGERINE-008, claude script log)
- WSE minus terrain minus depth showed large residuals driven by dry zero cells; compute residuals on wet cells only. (TANGERINE-008, claude script log)
- Aerial EPSG came only from file names and world files; record that assumption on the sheet. (TANGERINE-008, claude script log)
- Reviewer rejected depth rasters presented as the work map and flagged the channel and over-3-ft basins still shown as Zone A/AO. (STARVALLEY-009, claude from FEMA review comment matrix)
- Zone shapefiles built months earlier were left out of the upload; package QC must check they exist. (STARVALLEY-009, claude from FEMA review comment matrix)

Jurisdiction add-ons:
- FEMA Region IX / Pima County RFCD: depth-to-zone table comes from the effective study for the reach; do not reuse across studies without checking. (STARVALLEY-009)

QC checks:
- Cell coordinates match across input files; CRS verified.
- WSE from MAXWSELEV, not depth + terrain.
- Work map shows vector zones; channels and basins >3 ft depth are AE; BFE contours 1 ft.
- Zone shapefiles present in the submittal GIS package.

Source cards: TANGERINE-008, STARVALLEY-009.

---

### EXH-C10 FEMA floodplain and FIRM content on exhibits
qc_rule | target: update drainage-report-exhibit-standards §3 (Floodplain/FIRM figure) + jurisdiction add-on `drainage-report-exhibit-standards/FEMA` + QC rule | score 4.6 | hours 1.6 | cards 2 | projects 2 (plus 3 citing cards) | confidence high

Trigger: Project exhibits where a FEMA SFHA (Zone AE, 0.2% chance) is present, a FIRM panel or FIRMette is included, or NFHL layers are plotted.

Steps (merged):
1. Show FEMA floodplain extents and BFE lines on project exhibits (Zone AE and the 0.2% chance area). (SAHPARK-010, SILVERBELL-017)
2. State the effective date of the mapping on the exhibit and in the text. (SAHPARK-010)
3. Filter the 0.2% zone on the actual NFHL ZONE_SUBTY text ("0.2 PCT ANNUAL CHANCE FLOOD HAZARD") and test that the subset is non-empty; drop the legend entry or say "none mapped" if empty. (CALFIRE-017)
4. If a map revision is pending, add the preliminary/work map as a separate labeled appendix item with its status; never show it as effective. (SAHPARK-010)
5. FIRM panel/FIRMette: sketch the actual alignment or use a tight box labeled "this project" that covers the whole project, not a box over the whole panel (see EXH-X10). (SAHPARK-010, VALENCIA-023)
6. Pull effective FEMA layers for each exhibit extent and credit the source and pull date. (SILVERBELL-017, TANGERINE-008)

Gotchas:
- GeoPandas warned the 0.2% subset was empty and the figure was issued anyway. (CALFIRE-017, claude script log)
- Draft exhibits omitted the FEMA floodplain entirely and the FIRM appendix held only the current panel. (SAHPARK-010, claude from JCO QC redline)
- The project location box covered most of the panel. Floodplain status and jurisdiction wording are covered by a separate card (PHXZOO-007, other group). (SAHPARK-010, claude from JCO QC redline)

Jurisdiction add-ons:
- FEMA: NFHL field values (ZONE_SUBTY strings), effective vs preliminary status handling, layer set S_FLD_HAZ_AR / S_BFE / S_XS / S_LOMR. (CALFIRE-017, SAHPARK-010, TANGERINE-008)

QC checks:
- SFHA extents and BFEs on exhibits when present; effective date stated on sheet and in text.
- No empty NFHL subset issued; legend matches mapped zones.
- Pending revisions shown separately and labeled preliminary.
- FIRMette box tight to project or alignment sketched.

Source cards: SAHPARK-010, CALFIRE-017. Also cited: VALENCIA-023, SILVERBELL-017, TANGERINE-008.

---

### EXH-C11 Exhibit values driven from one register table (Q labels, required vs provided)
qc_rule | target: QC rule (exhibit value = report table = calc) + section in new skill `scripted-exhibit-sheets` (label placement from register) | score 68 | hours 11 | cards 2 | projects 2 | confidence medium

Trigger: Exhibits that show values that change with design iterations: peak Q at CPs or inflow locations, storage/gallery required vs provided volume, inverts.

Steps (merged):
1. Keep each changing value set in one table: inflow locations and Q (inflow register); per-gallery required volume, provided volume, footprint, inverts. (ELTORO-016, HOMEWOOD-018)
2. Place labels from that table by script on the aerial or model extent; regenerate the exhibit when values change instead of editing labels by hand. (ELTORO-016)
3. Label storage exhibits with "Volume Required" and "Calculated to Provide" taken from the table. (HOMEWOOD-018)
4. Re-check outlet invert vs WQV each time the gallery size changes. (HOMEWOOD-018)
5. Cross-check exhibit labels against the report discharge/volume tables before issue. (SAHPARK-009, HOMEWOOD-018)

Gotchas:
- Four versions of the existing flow-rates exhibit carried 50-70 hand-placed text labels each, re-placed for each extent and plan change. (ELTORO-016, claude file history)
- Stormwater exhibit and gallery sizing reissued about 7 times with sizes drifting from the vendor calculators. (HOMEWOOD-018, claude file history)

Jurisdiction add-ons:
- Placer County / Lake Tahoe Basin (TRPA): gallery sizing vs WQV and outlet invert check (HOMEWOOD-018); confirm whether this belongs in a Placer County add-on to drainage-report-build.

QC checks:
- Every Q and volume label on an exhibit traces to one register row and matches the report table.
- Required vs provided shown for each storage unit; outlet invert vs WQV rechecked after each size change.

Source cards: ELTORO-016, HOMEWOOD-018. Also cited: SAHPARK-009.

---

### EXH-C12 CAD coordination and cut/boring exhibits (non-drainage owner-team exhibits)
qc_rule | target: update drainage-report-exhibit-standards (new §3b "CAD coordination exhibits") + QC rule | score 57 | hours 9 | cards 2 | projects 1 | confidence medium

Trigger: Utility, grading, gondola, overhead-utility or boring/cut comparison exhibits prepared in Civil 3D for the owner team.

Steps (merged):
1. Clip master plan xrefs and show the actual site plan and survey; show master plan linework in a distinct muted color so it does not read as survey. (HOMEWOOD-020)
2. Freeze unneeded layers (e.g., canopies), thicken key proposed lines, add a legend for existing vs proposed. (HOMEWOOD-020)
3. Label FF, FG and major contours; trace grading breaklines from the grading model. (HOMEWOOD-020)
4. Use 30x42 when detail is lost at a smaller sheet size (see EXH-X06). (HOMEWOOD-020)
5. Adjust storm drain when the architectural base changes and say so on the exhibit. (HOMEWOOD-020)
6. Cut/boring exhibits: show proposed cut at each test pit or boring; state in a note what the cut is measured to (bottom of foundation inside buildings, finished surface outside); show max and min cut; use a color ramp with clearly different shades at key depths (e.g., 6 ft vs 8 ft). (HOMEWOOD-019)
7. Match table text size and properties across all tables on the sheet. (HOMEWOOD-019)

Gotchas:
- Repeated markups for line weight, legend and xref clutter across 8+ exhibits. (HOMEWOOD-020, claude from team markups)
- Three review rounds on the bore hole exhibit for missing cut labels and an unclear color ramp. (HOMEWOOD-019, claude from team markups)

Jurisdiction add-ons:
- Placer County / Lake Tahoe Basin (TRPA): project-type content only; no jurisdiction rule identified.

QC checks:
- Master plan linework muted and distinct from survey; xrefs clipped.
- Existing vs proposed legend; key proposed lines heavier.
- Cut exhibits: cut at every boring, reference surface note, max/min cut, distinguishable ramp at key depths.

Source cards: HOMEWOOD-019, HOMEWOOD-020.

---

### EXH-C13 FHWA Hydraulic Toolbox inlet output for appendices (compact sheet, slope misprint)
skill | target: new skill `hydraulic-toolbox-inlet-sheets` + Standard v0.3 change (allowed exception to native-output rule in drainage-report-exhibit-standards §4) | score 4.5 | hours 1.5 | cards 1 | projects 1 | confidence high

Trigger: Inlet calculations from FHWA Hydraulic Toolbox are going into a report appendix.

Steps (merged):
1. Do not tick Add Profile in the export; it adds pages of unneeded output. (VALENCIA-002)
2. Export the native Word report and keep it as evidence. (VALENCIA-002)
3. Reformat to the approved one-page compact layout (one inlet per page), filling displayed values only from the saved native .hyd values; check every numeric field. (VALENCIA-002)
4. Where the export prints longitudinal slope 0.0000, display the saved slope with a note that the native export misprints it. (VALENCIA-002)
5. Visually check every compact page, not a sample. (VALENCIA-002)

Gotchas:
- Native Word export prints longitudinal slope 0.0000 although the saved input and dialog have a nonzero slope; reproducible across 110 cases (Toolbox 5.5). (VALENCIA-002, claude via Codex session, decision/warning log)
- Raw program output took 2 pages per inlet; reformatting in Word from native values was accepted by the EOR. (VALENCIA-002, claude via Codex session, decision log)

QC checks:
- Native export retained in evidence folder; every compact-page value matches .hyd input/output.
- Slope note present wherever the native export shows 0.0000.
- 100% page visual check logged.

Source cards: VALENCIA-002.

---

### EXH-C14 Civil 3D handoff: LandXML surfaces/alignments and headless DWG
skill | target: new skill `civil3d-landxml-handoff` | score 0.4 | hours 0.2 | cards 1 | projects 1 | confidence medium

Trigger: Site plan geometry produced outside CAD must go to Civil 3D users.

Steps (merged):
1. Write LandXML 1.2 with EX and PR TIN surfaces (25-ft grid inside grading limits + 300 ft), road alignments with FG profiles, private streets, block and lot parcels. (RKN-011)
2. Write a layered DXF (AutoCAD 2018 format) with lot numbers and 2-ft/10-ft contours. (RKN-011)
3. Convert DXF to DWG with AutoCAD accoreconsole headless; confirm the file exists and return code is 0. (RKN-011)

Gotchas:
- Check point counts for EX and PR surfaces match the grid before export. (RKN-011, claude script log)

QC checks:
- Surface point counts = grid count; DWG exists, rc 0; opens in Civil 3D with surfaces and alignments.

Source cards: RKN-011.

---

### EXH-C15 3D crossing renderings from CAD and model geometry (Blender)
skill | target: new skill `blender-crossing-renderings` | score 20 | hours 4 | cards 1 | projects 1 | confidence high

Trigger: A proposal or public exhibit needs 3D views of culvert and bridge crossings with modeled water.

Steps (merged):
1. Use native CAD sections, barrel endpoints, project terrain and the current model water surface; sample display terrain at about 10 ft. (SILVERBELL-010)
2. Two cameras per crossing: aerial looking upstream from the downstream side, and pedestrian view through the barrel. (SILVERBELL-010)
3. Semi-transparent water, ground-draped FEMA lines, wide views showing both ties. (SILVERBELL-010)
4. Run a fill-closure check after each rebuild so open barrels are not covered; restore natural ground under bridge decks and run pavement finishing passes. (SILVERBELL-010)
5. Plot each view to PDF plus a combined PDF; label the water source (1D/2D, plan, date) and concept status on each sheet. (SILVERBELL-010)

Gotchas:
- Fill display closed over open barrels at five crossings; a separate fill-closure pass was needed after each rebuild. (SILVERBELL-010, claude render log)
- Bridge views needed natural ground restored under the deck and pavement finishing passes. (SILVERBELL-010, claude render log)
- Renderings kept showing provisional 1D water after design changes; note the water basis on each sheet. (SILVERBELL-010, claude render log)
- Thumbnail and OptiX cache write warnings are harmless. (SILVERBELL-010, claude render log)

QC checks:
- Every barrel open in render; water basis and concept status labeled on each view.

Source cards: SILVERBELL-010.
