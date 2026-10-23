# Plan-report-calc crosswalk (module of qc-reviewer; source DSO-C08, VALENCIA-006)

Use when report and calcs must be checked against a newer or earlier plan set.

1. Extract all PDF markups and text from report, redlines and plan sets to CSV registers
   (pypdf annotations: page, author, subject, contents; drop links, popups, plain shapes).
2. Build one CSV per feature type. Keep plan ID, report ID and model ID in separate columns; never assume equal.
   Keep watershed IDs as given.
3. Three-way compare: prior plan vs prior report vs latest plan. List design changes and the action each needs.
4. Locate features by station/offset from LandXML alignments (cad-base-update) when coordinates are needed.

## inlets_scuppers.csv
plan_id_prior, plan_id_latest, report_id, model_id, sheet, station, offset, type, opening (L x W or grate),
local_depression, Q_design_cfs, report_value_source_page, model_value, in_report (Y/N), note

## storm_pipes.csv
plan_id_prior, plan_id_latest, report_id, model_id, from_node, to_node, size_in, material, length_ft, slope_ftft,
us_invert_ft, ds_invert_ft, us_rim_ft, ds_rim_ft, report_page, model_value, in_report (Y/N), note

## culverts.csv
plan_id_prior, plan_id_latest, report_id, model_id, barrels, span_ft, rise_ft, shape, length_ft, us_invert_ft,
ds_invert_ft, HW_allowable_ft, HW_report_ft, HW_native_ft, native_file_page, in_report (Y/N), note

## plan_conflicts.csv (questions to the designer, never resolved silently)
sheet_a, item_a, sheet_b, item_b, conflict, question

Checks: every feature in the latest plan set has a row; dimension corrections are checked against the drawn
geometry (a profile length can include a segment past a junction).
