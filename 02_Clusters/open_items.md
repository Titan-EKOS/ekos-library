# Project open items found during harvest

Project-specific items, not library content. Grouped by reconcile group; duplicates across groups possible.

## HYD project-specific open items (not library content)

| Project | Item | Card |
|---|---|---|
| BARNETT | Development Engineering asked for the trail to stop at I-10 or for the crossing to be explained; state path continuity and crossing types in the introduction | BARNETT-011 |
| CALFIRE | Request effective LOMR model, DOT bridge as-builts and bridge hydraulic file; low chord (crest less assumed 1.5 ft slab) and pier width are assumptions; lidar model WSEL +0.15 to +1.53 ft vs effective | CALFIRE-011 |
| CALFIRE | 72 in RCP alternative has under 1 ft cover | CALFIRE-012 |
| CAMPBELL | Railroad rise not mitigated (1.33 ft vs 1.06 ft with smaller timestep; about 1.5 ft rise after opening lowering to 4.00 ft); no grading case met WSEL targets; proposed rail surface flow 700-900 cfs above existing | CAMPBELL-001, CAMPBELL-008 |
| CAMPBELL | Sub-minute native velocity peak (93 fps vs 3 fps saved 60 s max) unresolved | CAMPBELL-003 |
| CAMPBELL | GPU beta cannot carry the culverts/bridge or internal inflows; GPU runs not equivalent | CAMPBELL-006 |
| CAMPBELL | 1D breakout pair: residual mass-balance mismatch and existing stages several ft above 2D to be reported | CAMPBELL-007 |
| CAMPBELL | HY-8 cannot model 25 deg box inlet skew; note in report | CAMPBELL-013 |
| DLR | Plan p01 not registered in .prj; stray renamed p02 HDF and snapshot layer; stored maps reference undelivered terrain clones and need regeneration; duplicate DEM tiles | DLR-001, DLR-003 |
| DLR | Delivered spot points in EPSG 6426 vs rasters in EPSG 2230; record and reconcile | DLR-002 |
| DLR | Scripted rasters and the script package were shipped inside the delivered model folder; remove before release | DLR-006 |
| EKOS-LOCAL | All 100-yr detention cases fail native error 40253 (stage above storage curve); new geometry needed | EKOS-LOCAL-009 |
| EKOS-LOCAL | Project 1D/2D RAS model never completed (only synthetic tests passed) | EKOS-LOCAL-010 |
| EKOS-LOCAL | Unattended HY-8 run not achieved; Full Flow solver mode reported, not a matched RAS profile comparison | EKOS-LOCAL-012 |
| ELTORO | CP-13 carried twice in the accepted model; project note peaks (967/667/95/717 cfs) disagree with report developed values (2/40/3/43 cfs); CP concordance across 1999-2021 studies needed | ELTORO-001 |
| ELTORO | Roads omitted from CN layer (slightly non-conservative); burn from plans or county land use | ELTORO-004 |
| HOMEWOOD | Lower system fails 0.5 ft freeboard with tailwater 6 in below the receiving grate; memo claimed tailwater but model used free outfall | HOMEWOOD-010 |
| NORTHLOOP | Agency acceptance of FLO-2D build 26.02.25 (manual names 17.08.17) | NORTHLOOP-008 |
| NORTHLOOP | Old 500-yr was a 1.75 x Q100 multiplier, not a saved run; Alt1 folder includes artificial barriers not in the preferred alternative | NORTHLOOP-006 |
| NORTHLOOP | Old existing model stopped at 24 hr with inflows to 50 hr (about 18% volume unsimulated) | NORTHLOOP-005 |
| NORTHLOOP | Candidate 8 ft north bank below 8.71 ft conservative depth; revisit bank height and bend superelevation | NORTHLOOP-015 |
| NORTHLOOP | Level spreader basin at diversion outlet open in the response log | NORTHLOOP-016 |
| NORTHLOOP | Lining choice (shotcrete vs riprap) and sediment cleanout access to confirm in channel table | NORTHLOOP-014 |
| PHXZOO | Written client decisions pending: 100-yr vs 500-yr for enclosures, onsite containment, controlled flooding; Town and PCRFCD buy-in for any designed overflow | PHXZOO-005 |
| RKN | RFCD acceptance of the 2D approach | RKN-007 |
| SAH | Recommended road layout tested only for the 3-hr 100-yr storm; 24-hr storm not checked | SAH-011 |
| SAH | Referenced cards outside this group: SAH-003 (stream hang), SAH-015 (Python environment) | SAH-001, SAH-009 |
| SAHPARK | Plans p05 (100-yr) and p06 (10-yr) share flow file u02; 10-yr results suspect (matches mislabeled-storm comment) | SAHPARK-016 |
| SAHPARK | Culvert appendix shows options summary on arbitrary datum; insert native output for the selected 3 - 10x4 ft RCBC | SAHPARK-012 |
| SAHPARK | No outlet protection or scour content; 100-yr overtopping criterion met with no margin; perpendicular alignment sediment risk | SAHPARK-020 |
| SILVERBELL | Local source model differs from FEMA effective; no no-rise/CLOMR finding; results are screening | SILVERBELL-001 |
| SILVERBELL | Proposed 2D review run not accepted (3,520 iteration warnings, 17.1 ft max WSEL error) | SILVERBELL-005 |
| SILVERBELL | Contractor arch area loss 9.58 sq ft vs recomputed 10.00 sq ft; plan HW note repeats old box result | SILVERBELL-014 |
| STARVALLEY | Over-1-ft dWSE cells on other ownership need alternatives, notices and PE certification; property-boundary linework needed | STARVALLEY-008 |
| STARVALLEY | EOR acceptance of current-build (Pro) baseline in writing; legacy differences up to 1.57 ft documented | STARVALLEY-011 |
| STARVALLEY | 65 sections with synthetic banks flagged for engineer review | STARVALLEY-002 |
| STARVALLEY | Grade-control drops (up to 5.9 ft) list for EOR decision on structure ratings | STARVALLEY-016 |
| STARVALLEY | Open space lumped with ROW gives high CN; refine if mapping available | STARVALLEY-013 |
| TANGERINE | Common-mesh existing/proposed re-run deferred to the master drainage report (T1-6, T1-11, R-1) | TANGERINE-003 |
| TANGERINE | Captions cite Plan 12 / EX_<init>_LG but p12 has no short ID and notes name p09 as existing; fix plan register and captions | TANGERINE-004 |
| TANGERINE | Deferred reviewer items A-1, A-3, T1-4, T1-5, T1-7, T1-8; scope note for 1D-contracted vs 2D approach | TANGERINE-005 |
| TANGERINE | Substation site report: check receiving storm drain capacity/HGL and impervious-removal claim against site plan | TANGERINE-025 |
| VALENCIA | Signed-sealed and 100% workbooks differ; reproduce separately | VALENCIA-005 |
| VALENCIA | Element 207 capture INVALID (zero local-depression width) | VALENCIA-001 |
| VALENCIA | Inherited outlet tailwaters far above outfall inverts (e.g. 2504.42 vs 2472.59 ft); Known Q warning to reconcile | VALENCIA-004 |

## QC group - project-specific open items (not library content)

| Project | Item | Card |
|---|---|---|
| BARNETT | 15 pct comment log (about 104 rows, four divisions) has blank Action/Completed/Check; 30 pct DCR text cites an appendix response matrix not in the files | BARNETT-002 |
| BARNETT | Remediation list from 30 pct reconciliation (concept-affecting first) awaiting engineer review; figure legibility items marked Cannot Determine need native-file check | BARNETT-001 |
| BARNETT | Remove crossings built by development and structures tied to a closed road from proposed lists/exhibits/phasing; complete FEMA zone list in earlier section; cemetery access with road extension | BARNETT-005 |
| BARNETT | Funding statement contradiction, cost percentages not summing to 100, section heading hierarchy, crossing missing from crossing table, milestone statement | BARNETT-009 |
| BARNETT | Alternative evaluation matrix released early; hold until owner reviews underlying data | BARNETT-010 |
| CALFIRE | Constant road max HW (297.15 ft all events) is an extraction error; re-extract from WSE | CALFIRE-010 |
| CALFIRE | West normal-depth boundary carries 175 of 261 cfs; extend domain to receiving stream and refine mesh before overtopping conclusions | CALFIRE-010 |
| CALFIRE | Native-output appendix is re-typeset text; replace with printouts or retitle as extracted summary | CALFIRE-015 |
| CALFIRE | Checklist shows 21 rows Addressed vs 13 open items (culvert size/inverts, bridge low chord, new impervious area); re-status rows | CALFIRE-016 |
| CAMPBELL | Combined 1D/2D full events rejected (8.6 pct volume error); earlier accepted 2D comparison remains reported basis; diagnostics continue | CAMPBELL-002 |
| CAMPBELL | Design flow at the crossing held at 886.6 cfs per EOR; confirm narrative, tables, exhibits, HY-8 and protection sizing all use it | CAMPBELL-014 |
| CAMPBELL | Protection-table velocities do not match RAS; HEC-14 plunge basin sheet uses single barrel | CAMPBELL-019 |
| CAMPBELL | Restate ROW screening numbers that used a line burn | CAMPBELL-022 |
| EKOS-LOCAL | Local connector recovery loop not implemented | EKOS-LOCAL-011 |
| EKOS-LOCAL | Historical datum offset (+2.21 ft candidate) unadopted pending common monument tie | EKOS-LOCAL-014 |
| ELTORO | 2-yr flow file still carries the old 14-BC set (removed CP, duplicate CP-13) vs 29 BCs in 100-yr; rebuild | ELTORO-002 |
| ELTORO | Saved flow files show precipitation disabled; _v2 precip DSS missing; check for a later model version elsewhere before concluding runs were inflow-only | ELTORO-003 |
| ELTORO | Duplicate BC label 23 (582 / 483 cfs); 483 cfs matches master plan CP-22 | ELTORO-006 |
| ELTORO | Master plan items: culvert never constructed, pipe where bridge is shown, CP label at wrong location, missing scanned plan sheet to request | ELTORO-008 |
| HOMEWOOD | Storm drain model on kinematic wave; rerun dynamic wave for HGL criterion | HOMEWOOD-006 |
| HOMEWOOD | Galleries retain 1,893 of 3,763 cf (72-in) and almost nothing (30-in); 32-68 pct of WQ inflow untreated; raise outlets or add weir plate/riser and rerun | HOMEWOOD-007 |
| HOMEWOOD | Form 4-2 site area 111,270 vs 139,392 sf and YES answer with post > pre; Form 4-3 850 vs 1,178 cf required | HOMEWOOD-014 |
| HOMEWOOD | CMP gallery FG-to-SHGW depth: confirm 2 ft vs 5 ft separation | HOMEWOOD-017 |
| HOMEWOOD | Review package is a review draft, not stamped; awaiting EOR acceptance | HOMEWOOD-005 |
| NORTHLOOP | Carried-forward channel cuts about 0.10 ac of permanent water easement; 7 steep cell pairs at clipped channel; pad fill about 12.7 ft vs geotech about 12 in; infiltration tests not at basin | NORTHLOOP-017 |
| PHXZOO | Adjacent road 2D model defects (no outflow BC, artifact strip, cell size range, 2 vs 3 barrels, existing geometry with proposed culverts) before reuse | PHXZOO-006 |
| PHXZOO | Interface items with road team: entry culvert location/size, berm raise or removal, grading tie-in, CAD sharing; road alignment vs berm stabilization cost comparison open | PHXZOO-006 |
| PHXZOO | State effective vs pending FIRM panel and which governs; annexation status; floodplain-statement reversal noted in coordination record | PHXZOO-007 |
| RKN | Deviations (HMS 4.13 vs 4.12, Python exhibits vs QGIS, missing brand template) need EOR decisions | RKN-018 |
| SAH | FLO-2D results exist only for 100-yr; 2-, 10-, 25-, 50-yr 3-hr pairs and LOWER MineFill not run | SAH-003 |
| SAH | HYSTRUC inflow-node error and levee-crest warnings on all UPPER runs unfixed | SAH-006 |
| SAH | 30 pct draft: QC_Log 0/27, CalcRegister empty, 6 placeholders (EOR PE number, prior study fields), F-06/F-08 unregistered; VERIFY citations (prior study, ADEQ CGP edition) | SAH-013 |
| SAH | 226 assumption-log items unverified | SAH-014 |
| SAH | Narrative claims 2- to 100-yr runs in all models; correct to the run matrix | SAH-017 |
| SAHPARK | Rev B memo: HW 2,707.75 (soffit) vs 2,707.50 ft and control type; barrel length 65.99 vs 65.00 ft; truncated sentence; assumption A-2 source section; missing section 4.4 | SAHPARK-015 |
| SILVERBELL | Restricted parcel record may be split; confirm current record | SILVERBELL-003 |
| SILVERBELL | Proposed 2D convergence and bridge alternatives unresolved at freeze | SILVERBELL-011 |
| STARVALLEY | Response letter placeholders (10 TBC) and stale prior-letter text to address in cover letter | STARVALLEY-005 |
| STARVALLEY | Effective 24-hr storm model files absent; basin storage 15.71 vs 18.10 ac-ft; a culvert HW 0.02 ft over allowable; storm-drain inlet WL 2545.00 ft above inlet ground with full outlet loss (EOR decisions recorded) | STARVALLEY-021, STARVALLEY-023 |
| STARVALLEY | Three runs left running unmonitored at blind-rebuild session end | STARVALLEY-021 |
| TANGERINE | Crossing table adequacy statement vs upsizing text; update structures to latest roadway plans | TANGERINE-013 |
| TANGERINE | Rounding of percent increase; "approximately about"; tone/overstated conclusions in five comments | TANGERINE-012, TANGERINE-014 |
| VALENCIA | Structure D1 final decision (2-24 in) and native runs retained | VALENCIA-011 |
| VALENCIA | Workbook: 215 cached errors across 5 versions; confirm current copy (revert / overwrite / 100 pct / signed-sealed) | VALENCIA-014 |
| VALENCIA | Culvert inverts/slope/alt HW corrections; HERCP callouts; outlet protection note conflict | VALENCIA-016 |
| VALENCIA | About 40 CB/SC renumbers; CB13, CB32, SC11 missing; duplicate CB24; rerun capture where opening length changed | VALENCIA-017 |
| VALENCIA | Two missing upstream storm drain lines; pipe material; appendix output for redesigned runs | VALENCIA-018 |
| VALENCIA | Four channels without description; existing receiving channel not analyzed; removed arch pipes in table; existing 30 in CMP shown as proposed | VALENCIA-019 |
| VALENCIA | Remove wrong project/road names and unverified ditch/profile claims; add FIRM summary | VALENCIA-024 |

## RPT project-specific open items (not library content)

| Project | Item | Card |
|---|---|---|
| BARNETT | Final outreach survey analysis/charts not incorporated in the 30% DCR (two numbers only); survey exhibit placeholder empty; text claims full incorporation; preliminary plan/section graphics to be replaced with final versions | BARNETT-003 |
| CALFIRE | Cover office address and project number were placeholders - confirm set in issued copy | CALFIRE-013 |
| CALFIRE | LOMR source pages carry FreeText annotations into the compiled PDF - flatten or note | CALFIRE-014 |
| CALFIRE | Pending model rerun watcher - confirm recompile and copy to 10_Record completed | CALFIRE-014 |
| CAMPBELL | Appendix G exhibits swapped back to prior watershed maps - confirm EOR acceptance | CAMPBELL-021 |
| CAMPBELL | Replacement page 25 issued for urgent resubmittal - confirm full report reflects it | CAMPBELL-021 |
| CAMPBELL | Stale renders left in build folders (deletes not allowed) - clean before redistribution | CAMPBELL-021 |
| CAMPBELL | Non-working link in reviewed draft - verify fixed | CAMPBELL-020 |
| EKOS-LOCAL (GUILLERMO) | Earlier Word draft predates road-crossing results and was linked as current - retire | EKOS-LOCAL-016 |
| EKOS-LOCAL | Morning package refreshed 24 times overnight - set refresh batching | EKOS-LOCAL-017 |
| ELTORO | Memo header read "Drainage Statement" and "Page x of 3" in a 20-page PDF - verify corrected | ELTORO-018 |
| ELTORO | Alternatives memo: traffic data missing; alternative definitions and reference parameters flagged by reviewers | ELTORO-021 |
| HOMEWOOD | HGL table on wrong datum (about 1,580 ft vs 6,240 ft plans); HGL above rim at one node | HOMEWOOD-015 |
| HOMEWOOD | Conclusion cites bioretention planters (none proposed) and 10-yr storm (analysis 50-yr 1-hr) | HOMEWOOD-015 |
| HOMEWOOD | Appendix titled Hydraflow contains SSA report; unrelated RETDET.xls in storm folder | HOMEWOOD-015 |
| HOMEWOOD | Gallery sizes in vendor calcs (60-in / 18-in) differ from plans (72-in / 30-in) | HOMEWOOD-015 |
| HOMEWOOD | Package folder has two zips (5.9 MB, 8.8 MB) and a zip temp file - keep one final zip | HOMEWOOD-022 |
| RKN | Compiled PDFs 55-86 MB - check agency upload limit and compress | RKN-015 |
| SAH | Compiled PDF 23.8 MB; 3.4 MB compressed copy for transfer | SAH-012 |
| SAHPARK | Draft 3: no criteria/assumptions/decisions; empty Summary and Conclusions; three empty headings | SAHPARK-001, SAHPARK-002 |
| SAHPARK | Roadway typical section from 30% plans missing | SAHPARK-002 |
| SAHPARK | Hydrology appendix holds only floodplain mapping; uncited City of Tucson manual page; Appendix D-1 before D; channel calc in culvert appendix | SAHPARK-011 |
| SAHPARK | Table highlights, mixed decimals, caption mismatch, screenshot table, appendix table split across pages | SAHPARK-004 |
| SILVERBELL | Opening slide and DCR disagree on direction of a POC - confirm | SILVERBELL-016 |
| SILVERBELL | Mobile chat schedule dates conflict with deck - deck governs | SILVERBELL-016 |
| STARVALLEY | TDN draft sec. 4.8.3 contains a Python conditional string - remove | STARVALLEY-020 |
| STARVALLEY | Prior (June) package closed by FEMA; new case and fee - current package must pass full package QC gate before upload | STARVALLEY-004 |
| TANGERINE | Response matrix omits Town M-1..M-4, landowner agency A-1..A-4, county flood control R-1..R-4 and public N-1..N-5 comments | TANGERINE-002 |
| TANGERINE | Placeholder T1-? in remaining-items table; memo date June 2026 | TANGERINE-002 |
| TANGERINE | 96-page report PDF and three exhibit PDFs issued without bookmarks | TANGERINE-011, TANGERINE-016 |
| TANGERINE | Substation report draft: expansion direction stated opposite; footer dates; table mismatch; stray bracket | TANGERINE-018, TANGERINE-019 |
| VALENCIA | Initial vs later RFCD comments conflict (remove exhibit vs keep and label) - EOR decision open | VALENCIA-007 |
| VALENCIA | Agency asked to omit extra FEMA floodplain comparison - keep omitted in later passes | VALENCIA-007 |
| VALENCIA | 39 plan sheets lost revision clouds in merge; clouds to be removed from compiled copy, originals kept | VALENCIA-008 |
| VALENCIA | 9-23 editable Word body held corrections missing from its PDF - confirm newest source used | VALENCIA-008 |
| VALENCIA | Older D: copies not to be redistributed after OneDrive delivery | VALENCIA-010 |

## EXH project-specific open items (not library content)

| Project | Item | Card |
|---|---|---|
| BARNETT | Clean up "overbank" (29 uses, mixed meanings) and "corridor" (44 uses); add one project-area map; explain or remove borrowed master-plan study-area figures. | BARNETT-007 |
| BARNETT | Relabel 17 Figure / 15 Exhibit graphics to one series; close about 25 legibility/legend comments. | BARNETT-008 |
| CALFIRE | Floodplain exhibit issued with an empty 0.2% NFHL subset; reissue with corrected filter or "none mapped". | CALFIRE-017 |
| CAMPBELL | Confirm final WSEL difference class bands (re-cut three times) and push them into report text/tables; add velocity change exhibit with the WSEL one. | CAMPBELL-016 |
| CAMPBELL | Apply EOR exhibit label redlines (culverts, outfall Q, berms, wash names, depth classes, figure numbers). | CAMPBELL-018 |
| DLR | WSE difference rasters exist only in the VOID set; regenerate from final models before use. Final set mixes dates across variables; confirm consistency. | DLR-004 |
| DLR | Add plan numbers to the dictionary to tie tokens (TDAFW vs Mitigate_FW) to runs. | DLR-005 |
| ELTORO | Set up an inflow register and regenerate the existing flow-rates exhibit from it. | ELTORO-016 |
| HOMEWOOD | Gallery sizes drifted from vendor calculators over about 7 reissues; reconcile required vs provided per gallery and recheck outlet invert vs WQV. | HOMEWOOD-018 |
| HOMEWOOD | Adjust storm drain when the architectural base changes and note it on coordination exhibits. | HOMEWOOD-020 |
| NORTHLOOP | Basin values on the layout comparison exhibit marked pending; prior report figure not survey-registered; brand package not available (neutral styling used). | NORTHLOOP-011 |
| RKN | EOR decision pending on Python exhibits instead of QGIS layouts. | RKN-012 |
| SAHPARK | Investigate 48.898 ft max depth artifact before publishing depth map. | SAHPARK-006 |
| SAHPARK | Produce separate 10-yr and 100-yr exhibit sets; request 10-yr corridor depth mapping from the regional study. | SAHPARK-009 |
| SAHPARK | Add FEMA floodplain/BFEs to exhibits; add pending map revision as a separate labeled appendix item; tighten FIRM project box. | SAHPARK-010 |
| SILVERBELL | Renderings still show provisional 1D water; update to current model water and relabel the basis. Fill closure over barrels at C21, C22, C23, C45, C01 recurs after rebuilds. | SILVERBELL-010 |
| STARVALLEY | Zone shapefiles missing from the submittal upload; channel and >3 ft basins still shown as Zone A/AO on prior work map. | STARVALLEY-009 |
| TANGERINE | User asked for concept-report figures to be recreated in QGIS or CAD; DRAFT date in title blocks. | TANGERINE-006 |
| TANGERINE | Flood context sheets remain a source review draft until return period, condition and vertical datum are confirmed; supplied rasters carry conflicting CRS tags (EPSG 3498 vs 2223); aerial EPSG assumed from file names. | TANGERINE-008 |
| TANGERINE | Substation drainage report: close 12 exhibit comments across three figures (legend, orientation, parcel naming, culvert and Q labels, storm drain depiction, location map). | TANGERINE-022 |
| VALENCIA | Structure numbers missing on all proposed drainage maps; FIRMette box; crop stationing from location images; numbering vs text. | VALENCIA-023 |
| VALENCIA | Slope misprint note required on compact inlet sheets (110 cases). | VALENCIA-002 |

## HJR project-specific open items (not library content)

| Project | Item | Card |
|---|---|---|
| BARNETT | Design-basis summary sentence in 30% DCR still mixes regional/local wording; one flow carried as 4,324 and 4,325 cfs | BARNETT-006 |
| BARNETT | Replace citations of the superseded Northern Marana drainage requirements in sec 3, 5, 8.2 (No Action) and master plan alignment; add Town to CLOMR/LOMR coordination | BARNETT-004 |
| CALFIRE | Caltrans District Hydraulics to confirm accepted method for mid-size watersheds (HMS vs regression) | CALFIRE-006 |
| CALFIRE | District Hydraulics confirmation of 14-point CN calibration; calibrated 2-yr below regression (18 vs 27 cfs); DEM vs FIS area mismatch on the creek (open items list item 7) | CALFIRE-007 |
| CALFIRE | Highway class and posted speed for Table 831.3 storm pending traffic confirmation | CALFIRE-002 |
| CAMPBELL | Archived 24-hr HMS run never executed (missing basin depths, ERROR 23430); report as missing; ZERO_FLOW source removed in documented copy | CAMPBELL-012 |
| EKOS-LOCAL (GUILLERMO) | Basin outlet topology still an owner assumption (24-in RCP 1 ft above bottom); assumed pipe slope 0.017% implausible; as-built search outstanding | EKOS-LOCAL-015 |
| EKOS-LOCAL (GUILLERMO) | Imperviousness classifier failed (68.75% agreement); cover scenarios S1/S2/S3 used; north reach imagery coverage gap | EKOS-LOCAL-019 |
| EKOS-LOCAL (GUILLERMO) | 9 failed PC-Hydro tasks (NOAA mapping x3, Basin B import x4, road scenario, benchmark) to close out | EKOS-LOCAL-006 |
| ELTORO | North and south reach cross-culvert inventory not in source report; scope as new work; confirm PC-Hydro version with agency | ELTORO-009 |
| HOMEWOOD | County written confirmation of West vs East of crest basis (East about 35% lower) | HOMEWOOD-011 |
| HOMEWOOD | Replace mixed Small Watershed / model approach with hydrograph method for storage and HGL | HOMEWOOD-012 |
| HOMEWOOD | SWQP template elevation (6,600 vs about 6,300 ft) and memo WQ depth (1.3 in) to correct; reconcile DMA impervious areas across memo, exhibit, template | HOMEWOOD-008 |
| HOMEWOOD | SHGW at galleries undocumented; 2 ft separation assumption vs 5 ft rule for galleries and GW reinfiltration CMP; field infiltration testing | HOMEWOOD-009 |
| HOMEWOOD | Memo cites West Placer manual; change to East Placer | HOMEWOOD-013 |
| HOMEWOOD | GW reinfiltration overflow requirement open in markups (geotech says required) | HOMEWOOD-016 |
| HOMEWOOD | Corrected Small Watershed calcs reverse pre/post conclusion (existing 10-yr 7.87 to 4.32 cfs); headers, offsite elevation, 100% impervious DMAs, summary references to fix | HOMEWOOD-001 |
| NORTHLOOP | Town acceptance needed: 500-yr hydrology (1.75 x Q100 provisional only), facility classification, FLO-2D build 26.02.25 vs MDM 4.5 build, collector channel and outlet criteria | NORTHLOOP-003, NORTHLOOP-010 |
| NORTHLOOP | Equipment/floor elevations to be rechecked against Town Code 17-15-10 H.5 (1 ft above 500-yr) | NORTHLOOP-003 |
| NORTHLOOP | Update saved standards that still carry the 5% Desert Brush graded-ground rule | NORTHLOOP-013 |
| PHXZOO | Client decision on 500-yr refuge objective (Q500 not published; ratio method or added scope) | PHXZOO-002 |
| PHXZOO | Confirm FEMA effective/pending floodplains and PCRFCD 100-yr flows share the same basis; confirm site inside LMW-East study limit | PHXZOO-002 |
| PHXZOO | Town confirmation of roadway crossing criteria (RDM 2.10 currently County-only); ADEQ CAFO applicability; fencing/grate design at drainage penetrations | PHXZOO-004 |
| RKN | HEC-HMS 4.13 used instead of 4.12 - EOR decision item; tracked rerun list for CPs changed by DEM extension | RKN-006, RKN-003 |
| SAH | Agency agreement at methodology meeting to treat mine pits/tailings impoundments as non-contributing; terrain vintage in mine area | SAH-016 |
| SAHPARK | Written Floodplain Administrator concurrence that the raised berm is a drainage training embankment, not a levee, before 60%; berm ownership and maintenance | SAHPARK-019 |
| SAHPARK | Draft memo: 200-yr label, 10-yr caption on 100-yr map, missing table, approach flow vs crossing flow (2,673 vs 534 cfs) | SAHPARK-003 |
| STARVALLEY | Effective 24-hr (4.55 in) storm case missing from package; request from community/FEMA library | STARVALLEY-022 |
| STARVALLEY | Community items for new case: flooding-source name acceptance and O&M acceptance (community as responsible party, signature) | STARVALLEY-018 |
| STARVALLEY | With-phase vs without-phase package decision for concept-level phase | STARVALLEY-017 |
| TANGERINE | Substation site: confirm City vs County review; restructure to City outline; add critical facility/500-yr and FEMA section; fix floodplain legend | TANGERINE-017, TANGERINE-021 |
| TANGERINE | Watershed exhibits: topo support, flow arrows, Tc path; add roadway and upstream subdivision to offsite area to storm drain | TANGERINE-023, TANGERINE-024 |
| TANGERINE | Block-level detention per-pod ledger; preliminary pre-post detention and first-flush estimates in hydraulics appendix | TANGERINE-015 |
| VALENCIA | Agency comments RFCD-29/30/33, DOT-16: clogging factors, no double count on two-grate sump, PAG Std Detail 305 depression, bypass claims | VALENCIA-012 |

## DSO project-specific open items

Not library content. Project code | item | card id.

| Project | Open item | Card |
|---|---|---|
| CALFIRE | Confirm whether the state-agency project needs city floodplain review or state-coordinated review | CALFIRE-001 |
| CALFIRE | DWR Best Available Maps and CVFPB regulated-stream status not checked | CALFIRE-001 |
| CALFIRE | Standards not online (1988 city improvement standards; owner-agency drainage standard) - request | CALFIRE-001 |
| CALFIRE | Agency data requests outstanding: as-builts, effective HEC-RAS models, campus/master plan data, dam operator data (FEMA data request about 4 wk) | CALFIRE-001 |
| CALFIRE | Culvert inverts from lidar are estimates; replace with survey | CALFIRE-004 |
| CALFIRE | State the rule for dual HSG (B/D, C/D) and Not rated units (3-6 pct) before CN assignment | CALFIRE-005 |
| CALFIRE | NHD download incomplete from MapServer; confirm HU8 staged file used | CALFIRE-003 |
| CAMPBELL | Culvert native export and impervious-surface shapefile missing from the archive; obtain | CAMPBELL-011 |
| EKOS-LOCAL | Candidate crossing details not yet spatially anchored; OCR value 2698.20 vs 2696.20 to verify against page image | EKOS-LOCAL-013 |
| EKOS-LOCAL | RAG pilot qualified only on a synthetic 5-page test; real manuals not qualified | EKOS-LOCAL-022 |
| EKOS-LOCAL | Reference intake: 42 PDFs need rework (16 timeouts, 18 page-label failures, 8 zero-text); encrypted PDFs pending | EKOS-LOCAL-023 |
| EKOS-LOCAL | Pilot drainage report: RAS 1D/2D, HY-8 and 100-yr routing not done; draft is partial | EKOS-LOCAL-001 |
| EKOS-LOCAL | Queue: 3 tasks stuck pending on failed predecessors; 22 NEEDS_REVIEW tasks with no error text | EKOS-LOCAL-002 |
| EKOS-LOCAL | Knowledge base not integrated with standalone LM Studio/Ollama chats (open 4 wk) | EKOS-LOCAL-004 |
| EKOS-LOCAL | Account-bound or interactive install steps recorded as unresolved | EKOS-LOCAL-024 |
| ELTORO | CP concordance and reconciliation list across prior studies; full local OCR of scanned volumes | ELTORO-007 |
| ELTORO | Confirm governing sewer as-built set (Rev 7 vs Rev 5) with owner | ELTORO-023 |
| ELTORO | Inflow values mismatch flag; re-export model copy for checking | ELTORO-022 |
| ELTORO | Clean up duplicate plans (p16-p29), placeholder/Retry geometries, three live model folders, mixed 6.6/7.0 plans | ELTORO-005 |
| NORTHLOOP | Current town code chapters held only as web extracts | NORTHLOOP-002 |
| NORTHLOOP | Survey has no datum/benchmark statement; pad elevation and WSE provisional | NORTHLOOP-019 |
| NORTHLOOP | Confirm prior agency approval of the old report (addendum vs full replacement); Q500 basis stated two ways in prior report | NORTHLOOP-001 |
| NORTHLOOP | Historical DWG BAK lost after console refresh; DWG restored from backup | NORTHLOOP-018 |
| PHXZOO | Dedupe triplicate school as-built set and duplicate shapefile copies; move _tmp_render and .write_test out of synced folder | PHXZOO-001 |
| PHXZOO | Future WWTP outfall, wetlands and road-as-berm may change drainage; track | PHXZOO-001 |
| PHXZOO | Action Items/Data Exchange tabs empty after Meeting 1; dashboard placeholders unfilled | PHXZOO-003 |
| PHXZOO | Meeting budget about 6 vs weekly cadence about 26; change-order flag | PHXZOO-003 |
| PHXZOO | Undefined "third option" in scope; confirm; obtain current site plan iteration | PHXZOO-003 |
| SAHPARK | Add 2 - 36 in. pipes and grading-revision ditch; update imagery; address runoff direction from adjacent future facility | SAHPARK-014 |
| SAH | Mine tailings growth (30-80 ft) affects depression volumes and flow paths; USGS 2021 10-ft source contributed 0 cells | SAH-020 |
| SAH | 2/10/25/50-yr FLO-2D pairs not run; fix SAH-002/003/006/015 items and parameterize job root before rerun | SAH-018 |
| SILVERBELL | Updated local model is a screening, not duplicate-effective | SILVERBELL-013 |
| SILVERBELL | Chainage drift 32.7 ft; vertical-curve label conflict; DCR vertical datum unknown | SILVERBELL-007 |
| SILVERBELL | One CAD helper left unapplied after assembly error | SILVERBELL-009 |
| STARVALLEY | CAD vertex 100 ft off excluded; old channel files about 50 ft off centerline | STARVALLEY-014 |
| TANGERINE | Proposed corridor and six InfraWorks perspectives pending (Civil 3D seat) | TANGERINE-010 |
| TANGERINE | Nested duplicate project folder (about 2,258 files, 50 GB) in OneDrive | TANGERINE-009 |
| VALENCIA | Plan sheet internal conflicts (schedule vs profile labels; 3 arches note vs 2 barrels drawn); 387 ft profile length incl. 50 ft past junction | VALENCIA-006 |
| BARNETT | Irrigation district easement requirement for relocated facilities; 404 delineation at river tie-in; schedule phasing workshop | BARNETT-012 |
| BARNETT | Submitted proposal lists a task as both included and excluded | BARNETT-013 |
| HOMEWOOD | Ongoing architect base reissues; storm drain, gallery and exhibit rework after each | HOMEWOOD-021 |
