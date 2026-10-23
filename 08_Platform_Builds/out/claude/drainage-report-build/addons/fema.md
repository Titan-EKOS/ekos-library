# drainage-report-build add-on: FEMA

Load when: the site touches a FEMA SFHA, the report states a FIRM zone or BFE, or the work is a CLOMR / LOMR, no-rise or
duplicate-effective study. Package build and AD responses are in `fema-clomr-lomr`; rise mapping in `impact-comparison`.
QC tag: `fema`.

## Governing documents
- 44 CFR 65.12 (rise evaluation), Region IX practice, FEMA MT-2 forms (STARVALLEY-008).
- Effective FIS, FIRM panels and NFHL layers S_FLD_HAZ_AR, S_BFE, S_XS, S_LOMR; check LOMRs before any regulatory statement
  (CALFIRE-017, SILVERBELL-013).
- Effective TDN and models from the community or the FEMA library (STARVALLEY-022).
- FEMA 2D guidance for rain-on-mesh builds; FEMA alluvial fan guidance for fan sites (SAH-010, TANGERINE-005).

## Methods
- Use effective inflows, not county design flows, for FEMA comparisons; flag whether FEMA and agency design flows share an
  engineering basis (STARVALLEY-022, PHXZOO-002).
- Every effective storm case (duration, depth) in the package; a missing case is requested before modelling; never claim an
  envelope from one storm (STARVALLEY-022).
- Duplicate effective required for any Zone A / AE, no-rise or CLOMR finding; local source models that differ from the
  effective are screening only and say so (CALFIRE-011, SILVERBELL-001, SILVERBELL-002).
- The current engine build is the duplicate-effective basis; document differences from legacy results rather than forcing
  a match (STARVALLEY-011).
- Rise evaluation (44 CFR 65.12, Region IX): dWSE = proposed MAXWSELEV - existing; evaluate where max depth >= 1.0 ft in
  both conditions (SFHA), any-depth counted separately; map new and removed SFHA cells; list every cell > 1.00 ft with
  ground change, depth change and location (applicant land, approved grading, channel prism); quote report values from the
  written rasters / summary JSON; cells on other ownership need alternatives, notices on the CLOMR template and PE
  certification (STARVALLEY-008).
- 500-yr: FIS 0.2% profile only where its sections bracket the site; Zone AO depth is not an elevation (D22) (NORTHLOOP-010).
- Work maps: depth-to-zone table from the effective study for the reach (source case < 1 ft X; 1.0-1.5 AO(1); 1.5-2.5
  AO(2); 2.5-3.0 AO(3); > 3 ft AE); AE on channel cells, connected corridor and basins; 1-ft BFE contours inside AE; zone
  shapefiles with acreage table, matching the work map (STARVALLEY-009).
- Proposed TOPO from others or edited for grading: scan for constant-elevation patches and regrade-boundary steps before
  CLOMR runs (STARVALLEY-015).
- Screening vs duplicate-effective wording kept distinct in text (SILVERBELL-013).

## Criteria and package rules
- Line-ending and hash checks on model files are part of package QC (STARVALLEY-001, STARVALLEY-003).
- Build-string consistency across all models; duplicate-effective warnings inherited and explained; zone / BFE shapefiles;
  ZIP64 upload packages (STARVALLEY-004, STARVALLEY-020).
- NFHL field values (ZONE_SUBTY strings) and effective vs preliminary status handled explicitly (CALFIRE-017, SAHPARK-010,
  TANGERINE-008).
- Floodplain text: FIRM summary (panel, date, zones); effective and pending panels and which governs at submittal; zone read
  at the alignment (PHXZOO-007). Pending map revision as a separate labelled appendix item (SAHPARK-010).

## Review expectations
- AD letter: 90-day response, no extensions; last model run at least 10 days before the deadline; community-dependent
  items started the same day (STARVALLEY-006).
- Every response row states what changed, file, folder and report page; any status other than Addressed does not ship
  (STARVALLEY-006, D45).
- Rerun-all gate: every model re-run after its last input edit, including existing conditions (STARVALLEY-006)
  (`model-run-supervisor`).
- An item FEMA already rejected is settled by call before resubmitting (STARVALLEY-006).
- Concept-level phases: expect removal or design-level grading and drainage plans; keep scripts switchable to produce
  with-phase and without-phase packages (STARVALLEY-017).
- Community items: signed acceptance of flooding-source names for each new AO / AH / AE source; O&M plan naming each
  FEMA-required basin with the community (not an HOA) as ultimate responsible party, who maintains and how often, and a
  community signature block; O&M scope does not exclude public basins or channels; CLOMR owner-notification template with
  approved names, draft submitted before mailing (STARVALLEY-018).
- Community: Pima County RFCD in the County; in Marana the Town also signs (BARNETT-004).

## Open questions to confirm
- Region IX acceptance of FLO-2D build 26.02.25 as the duplicate-effective basis on each case (D03).
- Effective vs pending panel governing at the planned submittal date.
- Community items still open on the active case (flooding-source names, O&M acceptance) (STARVALLEY-018).
