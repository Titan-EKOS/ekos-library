# Add-on: Town of Marana exhibits (drainage-report-exhibit-standards)

Load for Town of Marana work. Report-level rules: drainage-report-build `addons/town-of-marana.md`.

## Rules
1. Corridor DCRs: one project-area map early in the report (study limits, affected properties, canal, railroad,
   river, interstate). (BARNETT-007)
2. Restricted defined terms: one term for project limits; zone terms (Top of Channel, Overbank Terrace, low-flow
   channel) used only as defined; run a term-count search before issue. (BARNETT-007)
3. Explain borrowed master-plan study-area figures or remove them. (BARNETT-007)
4. One label series (Figure or Exhibit) across the DCR. (BARNETT-008)
5. Project CRS: NAD83 Arizona Central (intl ft) was used on a concept report; confirm per project and state it in
   the datum callout. (TANGERINE-006)

## Gotchas
- "Overbank" appeared 29 times in mixed meanings and "corridor" 44 times. (BARNETT-007)
- 17 Figure and 15 Exhibit labels side by side in a 30% DCR. (BARNETT-008)

## QC
`get_qc_rules('marana')` plus `get_qc_rules('exhibits')`.
