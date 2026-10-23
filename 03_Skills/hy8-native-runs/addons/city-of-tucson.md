# hy8-native-runs add-on: City of Tucson

Load for City of Tucson crossings, especially contractor substitution requests.

## Rules
1. Substitution memo (e.g. arches for boxes): one page, native HY-8 output attached, compared with the
   approved report HW at the same flow, slope, n, length and fixed tailwater (SILVERBELL-014).
2. Include the stress cases (high tailwater; full crossing flow through one structure) and the Ke bracket
   (0.2 / 0.5) (SILVERBELL-014).
3. Report computed opening-area loss and any difference from the contractor value (SILVERBELL-014).
4. If the plan sheet HW note repeats an older design result, flag it for the plan revision list (SILVERBELL-014).

## QC
- run `get_qc_rules('tucson')`.
