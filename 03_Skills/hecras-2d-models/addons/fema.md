# hecras-2d-models add-on: FEMA

Load when a HEC-RAS model touches a FEMA-studied stream or supports a CLOMR / LOMR or no-rise finding.

## Rules
1. Rain-on-mesh builds follow FEMA 2D modeling guidance (cited in the model basis) (SAH-010).
2. A duplicate-effective model is required for any Zone A / AE, no-rise or CLOMR finding. A lidar 1D model, a
   local model or iterated-tailwater runs are screening only and labelled so (CALFIRE-011, SILVERBELL-001,
   SILVERBELL-002).
3. Screening may proceed without the effective model (skill Step 14); request the effective model early.
4. Caltrans / California bridges: take span, length, deck width and channel rating from the NBI record; request
   DOT as-builts and the bridge hydraulic file; low chord and pier width are assumptions until received
   (CALFIRE-011).
5. Package build and rise analysis: fema-clomr-lomr and impact-comparison `addons/fema.md`.

## QC
- run `get_qc_rules('fema')`.
