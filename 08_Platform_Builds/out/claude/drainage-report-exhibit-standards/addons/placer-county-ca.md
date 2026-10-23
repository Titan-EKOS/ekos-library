# Add-on: Placer County, CA exhibits (drainage-report-exhibit-standards)

Load for Placer County / Lake Tahoe Basin work. Report-level rules and gallery sizing: drainage-report-build
`addons/placer-county-ca.md` and groundwater-reinfiltration-sizing.

## Rules
1. Stormwater storage exhibits: per-gallery "Volume Required" and "Calculated to Provide", footprint and inverts
   placed from the register table, never typed by hand (scripted-exhibit-sheets register section). (HOMEWOOD-018)
2. Re-check outlet invert vs WQV each time a gallery size changes, before the exhibit is reissued. (HOMEWOOD-018)
3. Owner-team coordination exhibits follow core 4.9 (30x42 allowed, muted master plan linework, storm drain adjusted
   and noted when the architectural base changes). No jurisdiction rule identified beyond project type.
   (HOMEWOOD-019, HOMEWOOD-020)

## Gotchas
- Stormwater exhibit and gallery sizing reissued about 7 times with sizes drifting from the vendor calculators.
  (HOMEWOOD-018)
- Repeated markups for line weight, legend and xref clutter across 8+ exhibits. (HOMEWOOD-020)

## QC
`get_qc_rules('placer')` plus `get_qc_rules('exhibits')`.
