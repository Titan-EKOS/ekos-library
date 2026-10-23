# flo2d-model-runs add-on: FEMA (CLOMR / LOMR, duplicate effective)

Load for any FLO-2D model that supports a CLOMR, LOMR or duplicate-effective submittal (FEMA Region IX with
Pima County RFCD as floodplain administrator in the source cases). Package build: fema-clomr-lomr.

## Rules
1. Duplicate-effective basis: when the effective model is in a legacy build that will not run (e.g. 2009 build,
   demo mode without a license), convert to the current Pro build per Step 2 of the skill. The current build is
   the duplicate-effective basis. Document differences from legacy results by footprint (depth, hydrographs);
   never force a match by editing terrain, inflows or ratings (STARVALLEY-010, STARVALLEY-011).
2. Every condition (duplicate effective, corrected effective, existing, proposed) on one engine build with the
   same grid (CADPTS identical) and shared-input hashes equal (STARVALLEY-007).
3. Package QC: the CRLF scan and the size/hash checks from `flo2d_harness.py preflight` are part of the
   submittal package QC and must pass on the package copy, not only the working copy (STARVALLEY-001,
   STARVALLEY-003).
4. Structures: reviewers check zero-flow structures, HY-8 table names and discharge ranges, and tailwater
   assumptions; run Step 4 checks and include per-structure peak/volume in the submittal (STARVALLEY-012).
5. Development: reviewers ask for ARF, IRAINBUILDING, n and infiltration updates for proposed residential
   areas; use Step 5 (measured coverage ratio, unblocked-area CN) and a change memo listing every edit
   (STARVALLEY-013).
6. Work maps: use the depth-to-zone table of the effective study for the reach (source case: < 1 ft X;
   1.0-1.5 AO(1); 1.5-2.5 AO(2); 2.5-3.0 AO(3); > 3 ft AE); do not reuse it across studies without checking.
   Assign AE to channel cells, the connected inundated corridor along each 1D segment and detention basins;
   1-ft BFE contours inside AE from MAXWSELEV; write effective / existing / proposed zone shapefiles with an
   acreage table; show vector zones on the work map, not depth rasters; include the zone shapefiles in the GIS
   package (STARVALLEY-009).
7. Rise analysis under 44 CFR 65.12: impact-comparison, `addons/fema.md`.

## Gotchas
- Reviewer rejected depth rasters presented as the work map and flagged the channel and over-3-ft basins still shown as Zone A/AO (STARVALLEY-009)
- Zone shapefiles built months earlier were left out of the upload; package QC must check they exist (STARVALLEY-009)

## QC
- run `get_qc_rules('fema')` and `get_qc_rules('flo2d')`.
