# drainage-report-build add-on: Pima County RFCD

Load when: the site is in unincorporated Pima County, the Pima County Regional Flood Control District (RFCD) or Pima County
DOT reviews the work, or a Town / City adopts County criteria (City of Tucson, Town of Marana and Town of Sahuarita add-ons
point here for the base rules). QC tag: `pima-rfcd`.

## Governing manuals (confirm current edition at project start; cite only current editions)
- RFCD technical policies: TECH-010 (rainfall, NOAA Atlas 14 upper 90%), TECH-015 (PC-Hydro method), TECH-018 (HEC-HMS for
  systems over 1 sq mi), TECH-033 (2D modelling, Amendment A nested grids) (RKN-017, RKN-006, RKN-007, SAH-020).
- PC-Hydro 7.4 and the PC-Hydro User Guide (RKN-017, NORTHLOOP-013).
- Pima County / City of Tucson Stormwater Detention / Retention Manual, Table 2.1 (first flush), drawdown limits
  (RKN-016, PHXZOO-004).
- Pima County Roadway Design Manual (RDM): Table 2-9 inlet clogging, Sec. 2.10 roadway crossings (VALENCIA-012, PHXZOO-004).
- PAG Standard Details (Std Detail 305 inlet apron depression) (VALENCIA-012).
- Pima County riparian classification layer as the habitat source (TANGERINE-007).
- Older studies on NOAA Atlas 2 / the 1979 county manual: cross-check only (ELTORO-007).

## Methods
| Item | Rule | Source |
|---|---|---|
| Hydrology < 1 sq mi | PC-Hydro 7.4 (`pchydro-hydrographs`); confirm the version the agency accepts when reusing an older study | RKN-017, ELTORO-009 |
| Hydrology > 1 sq mi | HEC-HMS per TECH-018 (`hechms-headless`, add-on pima-county-rfcd): SCS CN from PC-Hydro ADOT tables, SCS UH lag 0.6 Tc, Modified Puls, Atlas 14 upper 90% at centroid with areal reduction | RKN-006 |
| Critical storm | max of 3-hr and 24-hr | RKN-006 |
| Rainfall | NOAA Atlas 14 upper 90% (TECH-010); PC-Hydro in-app fetch governs, edition recorded (D21) | RKN-017, EKOS-LOCAL-006 |
| Tc | program value, 5 min minimum | RKN-017 |
| Graded ground cover | PC-Hydro default (20%); no 5% Desert Brush override, no fixed CN (D20) | NORTHLOOP-013 |
| Regulatory washes | Q100 >= 100 cfs get 1D floodplains | RKN-017 |
| 2D rain-on-grid | TECH-033 for existing and each alternative (100 / 2 / 10 / 500-yr); compare 1-hr IDF storm with SCS Type II 3-hr and use the critical storm per TECH-018; CN from the PC-Hydro User Guide table (HSG A desert brush as B, 20% density = CN 83); RFCD acceptance of a 2D approach is an approval item | RKN-007, ELTORO-004, SAH-010 |
| Nested 2D grids | TECH-033 Amendment A: upstream outflow = downstream inflow | HYD-C07 |
| Closed depressions | non-contributing only with agreement at the methodology meeting; bracket both ways | SAH-016 |
| Offsite culvert inflows | culvert data from ADOT as-builts; PC-Hydro per watershed < 1 sq mi | RKN-003 |
| Pavement drainage | spread and capture reproduced in FHWA Hydraulic Toolbox | VALENCIA-001 |
| Terrain / CRS | lidar collection AZ_PimaCounty_2021_B21 preferred (2018, 2015 overlap); NAD83(HARN) AZ Central intl ft, EPSG:2868 (D55, default, to confirm) | RKN-002, SAH-018 |

## Criteria
- First flush (Detention / Retention Manual Table 2.1, lower-permeability rates): 1,440 cf/ac new impervious + 140 cf/ac
  disturbed pervious; higher Table 2.1 values in riparian habitat (RKN-016).
- First flush retained below the outlet invert, max 9 in deep (RKN-016).
- Drawdown: 12 h for basins <= 10 ac, 24 h for basins > 10 ac (RKN-016).
- Untested infiltration (D23, required-rate method): required field rate = retained depth x FS / drawdown limit, for
  example 9 in x 2.0 / drawdown limit; state that field testing is required (RKN-016).
- Inlet clogging (RDM Table 2-9): 0.80 curb openings, 0.50 grates, on grade and sump. If the calculator has no clogging
  input, reduce length or area to the effective value (25 ft clear = 20 ft effective); the 1.25 length multiplier is the
  reciprocal of 0.80, not a bypass allowance; recompute 10-yr and 100-yr capture and route bypass (VALENCIA-012).
- No double clogging: a two-grate sump with one grate assumed blocked already covers clogging (VALENCIA-012).
- Inlet depression per PAG Std Detail 305 (VALENCIA-012).
- Roadway crossings (RDM 2.10): 10-yr contained, 100-yr overtopping 1 ft max (PHXZOO-004).
- Street drainage: 10-yr max spread between curbs; clogging stated; scuppers in sump; ROW velocity < 3 fps; confirm which
  manual each value comes from (ELTORO-011).
- Critical facilities: improvements above the 500-yr WSE (TANGERINE-021).
- Crossing concepts with ADOT involvement: ADOT headwall / wingwall standards, drop inlets 6:1 or flatter, RCBC top slab
  1.0 ft for cover checks (SILVERBELL-004).
- Detention / Retention Manual favours distributed shallow basins; private-development provisions may not apply over
  1 sq mi (PHXZOO-004).

## Review expectations
- Required project-description text verbatim from the scope / RFP where the County requires it (TANGERINE-019).
- Comment responses written back into the agency's original comment-form layout; forms placed directly behind the cover
  (VALENCIA-007, CAMPBELL-015) (`agency-comment-response`).
- An agency request to omit a section (for example an extra FEMA comparison) stays in force in later passes (VALENCIA-007).
- Roadway reports: outfall Q labels and berm dimensions on drainage maps; design-plan Q and calculated Q labelled at
  culverts (CAMPBELL-018, TANGERINE-022).
- Difference maps: increases-only display and class set per the exhibit standard (CAMPBELL-016; D31, D33).
- Reviewers require common-mesh existing / proposed runs before any no-adverse-impact statement (TANGERINE-003).
- FEMA cases: RFCD is the community; see `addons/fema.md` (STARVALLEY-018).
- Do not cite City of Tucson standards on County or Town projects (SAHPARK-011).

## Open questions to confirm
- Current editions of TECH-010 / -015 / -018 / -033 and the Detention / Retention Manual.
- Whether RFCD accepts HEC-HMS 4.13 and FLO-2D build 26.02.25 without comment (D01, D03).
- Source manual sections for the 10-yr spread and 3 fps ROW velocity values (ELTORO-011).
- Source manual sections for the ADOT headwall, 6:1 drop inlet and 1.0 ft slab values (SILVERBELL-004).
- Road geometry values used on a master plan (95-ft spine ROW, R >= 600 ft, 8% max, 60-ft collector ROW) are project
  assumptions; confirm against the governing roadway standard (RKN-010).
- Rise threshold for the project (D29): cite from RFCD or the stakeholder; 0.10 ft was used on one evaluation memo (ELTORO-018).
