# hecras-2d-models add-on: Town of Marana (alluvial fan / piedmont 2D)

Load for 2D models on alluvial fans or distributary piedmont areas in the Town of Marana, and for Pima County
RFCD alluvial-fan reviews. Sources: Town of Marana Drainage Manual (2024), ADWR SS4-95 / SS5-96, FEMA alluvial
fan guidance (TANGERINE-005).

## Rules
1. Solver: DWE for broad fan flow; then test SWE at road crossings, pinch points, berms and high-velocity cells
   (skill Step 12). Report where SWE changes results.
2. Appendix documents: terrain source and seams, breaklines, boundary hydrographs, timestep, Courant, volume
   balance and instability locations.
3. Stress run: 200-yr or increased-rainfall run to test path switching on the fan.
4. Node-to-node volume ledger: inflow, outflow and storage between key nodes, closed to the volume balance.
5. Velocities in erodible soils approaching 16-20 fps need bank protection or erosion-hazard setbacks; state
   which.
6. Land-cover n, not uniform n, on concept / master studies (decision D28); reviewers carried uniform n as a
   deferred comment.
7. Common-mesh existing and proposed runs before any no-adverse-impact text (TANGERINE-003; impact-comparison).
8. Flag a 1D-contracted vs 2D-needed scope mismatch to the PM at the start (TANGERINE-005).
9. Flows: design on non-regional discharges (MDM 4.1) except regional channels / linear parks (decision D24,
   default, to confirm).

## Gotchas
- Every item above was raised by reviewers on a concept model (A-1, A-3, T1-4, T1-5, T1-7, T1-8) and carried as deferred work; build them into the first model (TANGERINE-005)

## QC
- run `get_qc_rules('marana')`.
