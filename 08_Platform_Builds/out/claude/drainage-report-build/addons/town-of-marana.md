# drainage-report-build add-on: Town of Marana

Load when: the Town of Marana reviews the report or the site is within Town limits. Load `addons/pima-county-rfcd.md` for
shared County criteria and `addons/fema.md` for any CLOMR / LOMR. QC tag: `marana`.

## Governing manuals (confirm current edition)
- Town of Marana Drainage Manual (2024) (MDM); the former Northern Marana drainage requirements are folded into it and are
  superseded - do not cite them (BARNETT-004).
- Town Code 17-15-10 H.5 (finished floor above the 500-yr WSE) and Sec. H (500-yr delineation, erosion protection)
  (NORTHLOOP-003).
- Alluvial fan references for fan sites: MDM 2024, ADWR SS4-95 / SS5-96, FEMA alluvial fan guidance (TANGERINE-005).
- Town code online cannot be bulk-downloaded; save the chapters used as dated web extracts in 01_Reference (NORTHLOOP-002).

## Methods
- Design discharges (D24, default, to confirm): design on non-regional discharges per MDM 4.1, with onsite PC-Hydro;
  regional flows only where the facility is a regional channel or linear park; regional flows for FEMA comparisons
  (NORTHLOOP-003, BARNETT-006).
- Terminology: "regional" vs "local" (non-regional) defined once and used with every flow; no synonyms (BARNETT-006,
  NORTHLOOP-003).
- PC-Hydro for non-regional flows; default vegetation cover on graded ground (D20) (NORTHLOOP-013).
- FLO-2D (D03): MDM 4.5 names a build (17.08.17 per NORTHLOOP-008), which fails at startup on EKOS; runs use 26.02.25 with
  written Town acceptance logged per project; archived outputs from builds 19.07.21 / 21.08.23 are historical until
  accepted (NORTHLOOP-003, NORTHLOOP-008).
- Alluvial fan 2D: diffusive wave for broad fan flow, then test full momentum at road crossings, pinch points, berms and
  high-velocity cells; appendix documenting terrain, breaklines, boundary hydrographs, timestep, Courant, volume balance
  and instability locations; 200-yr or increased-rainfall stress run; node-to-node volume ledger; velocities approaching
  16-20 fps in erodible soils need bank protection or erosion-hazard setbacks; flag 1D vs 2D scope mismatch to the PM
  (TANGERINE-005).
- Existing / proposed comparison on a common mesh before any no-adverse-impact text (TANGERINE-003) (`impact-comparison`).
- Project CRS NAD83 AZ Central (intl ft) used on a concept report; confirm per project (TANGERINE-006).

## Criteria
- Critical facilities / structures: finished floor 1 ft above the 500-yr WSE (Town Code 17-15-10 H.5); 500-yr delineation
  and erosion protection required (NORTHLOOP-003).
- Collector channel freeboard 2 ft; lining evaluated for sediment load (shotcrete used where riprap unsuitable); level
  spreader where flow returns to natural ground (NORTHLOOP-014, -015, -016).
- Detention, first flush and sediment storage kept separate (TANGERINE-015).

## Review expectations
- Development Engineering flags any citation of the superseded Northern Marana document (BARNETT-004).
- CLOMR / LOMR coordination names RFCD and the Town; the Town co-signs the community acknowledgement (BARNETT-004).
- Corridor DCRs: one project-area map and a restricted set of defined terms (BARNETT-007).
- Concept channel / path reports: state in the introduction whether a path is continuous under I-10 / UPRR or ends there,
  and the crossing type at each road (BARNETT-011).
- Remove crossings built by development and structures tied to a closed road from proposed lists, exhibits and phasing
  (BARNETT-005).

## Open questions to confirm
- Town acceptance of FLO-2D build 26.02.25 (D03, default: JCO seeks acceptance) (NORTHLOOP-003).
- Reading of MDM 4.1 regional vs non-regional design flows and the linear-park / channel exception (D24).
- Accepted 500-yr hydrology (1.75 x Q100 provisional only), facility classification, collector channel and outlet
  criteria (NORTHLOOP-003, NORTHLOOP-010).
- Rise threshold for the project, cited per D29.
