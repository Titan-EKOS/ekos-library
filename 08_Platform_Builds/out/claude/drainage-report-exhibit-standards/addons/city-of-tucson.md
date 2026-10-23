# Add-on: City of Tucson exhibits (drainage-report-exhibit-standards)

Load for City of Tucson work. Report-level rules: drainage-report-build `addons/city-of-tucson.md`.

## Rules
1. Culverts on drainage maps: label design-plan Q and calculated Q. (TANGERINE-022)
2. Offsite watershed exhibits near a City storm drain: bring in the City storm drain base (pipes, manholes, inlets);
   include roadway and upstream subdivision areas tributary to it; label upstream offsite infrastructure.
   (TANGERINE-024)
3. State the inlet capture assumption on the exhibit or in its note: inlets capture the 100-yr flow at each inlet
   unless shown otherwise. (TANGERINE-024)
4. Show storm drains as storm drain, not as part of the wash network. (TANGERINE-022)

## Gotchas
- Offsite watershed omitted roadway and subdivision areas tributary to the storm drain. (TANGERINE-024)
- Storm drain drawn as part of the wash network drew a redline. (TANGERINE-022)

## QC
`get_qc_rules('tucson')` plus `get_qc_rules('exhibits')`.
