# HYD project-specific open items (not library content)

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
