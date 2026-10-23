# drainage-report-build add-on: City of Tucson

Load when: the City of Tucson reviews the report. Confirm City vs County review from the parcel record and the contract
first; when they disagree, record both and ask JCO (TANGERINE-017). Load `addons/pima-county-rfcd.md` as well for shared
County criteria (PC-Hydro, Detention / Retention Manual). QC tag: `tucson`.

## Governing manuals (confirm current edition)
- City of Tucson drainage design and floodplain management standards manual, including its standard report outline
  (TANGERINE-017).
- Pima County / City of Tucson Stormwater Detention / Retention Manual (shared with the County) (TANGERINE-015).
- PC-Hydro accepted for onsite / non-regional work (HJR library structure table).

## Methods
- Report outline: the City outline is the section list; keep every section; "Intentionally left blank" with the reason
  where nothing applies; import styles from the current firm template (TANGERINE-017).
- Existing conditions split into hydrology (offsite and onsite watersheds with calcs) and existing stormwater
  infrastructure (TANGERINE-017).
- Offsite areas tributary to a City storm drain include roadway and upstream subdivision areas; bring in the storm drain,
  manholes and inlets; assume inlets capture the 100-yr flow at each inlet unless shown otherwise (TANGERINE-024).
- Retention vs discharge: justify the choice with receiving storm drain capacity and HGL; verify impervious-area claims
  against the site plan (TANGERINE-025).
- Contractor culvert substitutions: memo against the approved report HW using HY-8 with identical flow, slope, n, length
  and tailwater; bracket entrance loss; full-flow stress case (SILVERBELL-014) (`hy8-native-runs`).
- Record plans and field books: City Maps and Records public catalog (plan ID and description queries; field-book pages need
  a cookie + CSRF session) (EKOS-LOCAL-013).

## Criteria
- Critical facilities: improvements above the 500-yr WSE; FEMA floodplain section and 500-yr basis per core Sec. 1.6
  (TANGERINE-021).
- Separate detention, first flush and sediment storage; per-pod ledger for distributed detention (TANGERINE-015).
- Collector channel provisions where the City has adopted them (NORTHLOOP-015).
- Drainage maps: design-plan Q and calculated Q both labelled at culverts; location map without aerial (TANGERINE-022, D35).

## Review expectations
- JCO redlines on City drafts asked for the City outline, the critical-facility / 500-yr discussion, topo-supported
  watershed boundaries with arrows agreeing with contours, and the storm drain tributary area (TANGERINE-017, -021, -023, -024).
- Floodplain legend lists only zones present and includes the floodway hatch (TANGERINE-021).

## Open questions to confirm
- Current edition and section numbers of the City drainage standards manual and its outline.
- Whether the City or the County holds review on sites where the contract and parcel map disagree (TANGERINE-017).
- City freeboard above the 500-yr WSE for critical facilities, if any.
- Which collector channel provisions the City has adopted (NORTHLOOP-015).
