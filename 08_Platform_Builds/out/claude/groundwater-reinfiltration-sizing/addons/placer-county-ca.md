# Add-on: Placer County CA - East Placer / Lake Tahoe Basin / TRPA
For: groundwater-reinfiltration-sizing v1.0.0. Overrides only what differs from the core procedure.
Report-level Placer rules (hydrology method, design storms, storm drain, SWQP) live in
`drainage-report-build` `addons/placer-county-ca.md`; this file covers the reinfiltration gallery.

## Governing documents (confirm current editions at project start)
- East Placer Storm Water Management Manual (2024) and the East Placer SWQP template (App. A 2024).
  Use the East Placer names, not West Placer, in every memo (HOMEWOOD-013).
- Placer County Stormwater Management Manual (hydrology, storm drain).
- TRPA BMP Handbook (Sec. 4.1-d subsurface infiltration).
- Confirm West vs East of crest basis in writing for any rainfall value used.

## Rules that override the core
1. **Separation to SHGW = 5 ft** from the gallery or BMP bottom (East Placer Sec. 3.1.1) (D25).
   Document SHGW at each footprint from borings or the geotech memo. If 5 ft cannot be met: move the
   facility, redesign (shallower/wider), or obtain a variance; record which. A 2 ft separation
   assumption is not used unless the County confirms in writing that the 5 ft rule does not apply to
   groundwater (not stormwater) reinfiltration (HOMEWOOD-009; open item until confirmed).
2. **Untested infiltration rate (D23, to confirm with County):** until field testing at gallery depth,
   use half the NRCS rate for the mapped soil (1.0 in/hr on the source project) and report a 0 in/hr
   sensitivity. State that field testing at gallery depth is required before final design.
3. **Geotech limits:** check limits on infiltrating above the lowest foundation elements (setback or
   depth) before siting.
4. **Surface runoff into the same gallery:** if the gallery also takes stormwater, size the subsurface
   infiltration to retain at least the TRPA 20-yr 1-hr volume from tributary impervious area
   (TRPA BMP Handbook 4.1-d) on top of the groundwater storage; prefab chambers give 80-90% voids
   vs 40% for gravel.
5. **Water quality depth flag (D25):** do not state a WQ design depth in a groundwater memo without the
   East Placer manual check. The 85th percentile 24-hr rainfall depth (1.2 in at 6,000-6,500 ft) and
   the SWQP template "unit WQV" (about 0.9 in at 6,300 ft, 1.0 in at 6,600 ft) disagree, and the cards
   do not say which is rainfall and which is runoff depth. Back-check the template with
   WQV = impervious area x C x unit depth and flag the value for confirmation from the East Placer
   manual; never use a 50-yr 1-hr depth (e.g. 1.3 in) as a WQ depth (HOMEWOOD-008).
6. **One source for impervious areas:** DMA impervious areas used in the gallery sizing, the memo, the
   exhibit and the SWQP template come from one table (HOMEWOOD-008).

## Depth check with the 5 ft rule
| Unit | Stack to bottom of structural section (in) | Stack (ft) | + 5 ft separation (ft) |
|---|---|---|---|
| 36 in CMP | 36 + 2 + 12 + 12 | 5.17 | 10.17 |
| 24 in CMP | 24 + 2 + 12 + 12 | 4.17 | 9.17 |
| 18 in CMP | 18 + 2 + 12 + 12 | 3.67 | 8.67 |
Structural section 12 in shown as the source-project value; use the pavement design value.

## Acceptance items to confirm in writing (open items until answered)
- 5 ft separation applies to groundwater reinfiltration galleries (vs stormwater BMPs only).
- Half-NRCS untested rate with 0 in/hr sensitivity is acceptable for preliminary sizing.
- Overflow outlet location and receiving system.

## QC (scope tag `placer`)
- Manual named is East Placer; separation 5 ft documented per gallery with SHGW source.
- Untested rate basis and testing requirement stated; 0 in/hr sensitivity reported.
- TRPA 20-yr 1-hr volume met where surface runoff enters the gallery.
- WQ depth, if quoted, is flagged or confirmed from the East Placer manual.

Source cards: HOMEWOOD-016, HOMEWOOD-009, HOMEWOOD-017, HOMEWOOD-008, HOMEWOOD-013.
