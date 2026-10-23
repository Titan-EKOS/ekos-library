# Add-on: Pima County RFCD / Pima County DOT (agency-comment-response)

Load when the reviewing agency is Pima County Regional Flood Control District or Pima County DOT.

1. Write responses back into the agency's original comment-form layout (same columns, numbering and sheet order);
   do not re-key the agency text (VALENCIA-007, CAMPBELL-015).
2. Place the completed forms (response table) directly behind the cover page of the resubmitted report, and also
   deliver the editable log separately (D49). In the compile manifest the forms follow the cover and precede the TOC;
   bookmark them "Response to Comments".
3. Final forms state what was done, in completed tense, with section, table, figure and appendix numbers as displayed;
   no "will comply" (VALENCIA-007, CAMPBELL-015).
4. Turn off markups on the included forms before compile (QC-C06).
5. Initial and later RFCD comments can conflict (remove an exhibit vs keep and label it); record JCO's decision in the
   Decisions sheet and answer both comments consistently (VALENCIA-007).
6. Rise thresholds, freeboard and criteria quoted in responses are cited from the RFCD manual or the agency's own
   comment, never a hard-coded value (D29).

QC: `get_qc_rules('pima-rfcd')` and `get_qc_rules('comment-response')`.

Change log
- 1.0.0 2026-10-22: from RPT-C05 jurisdiction add-on (VALENCIA-007, CAMPBELL-015), QC-C06 step 4; D29, D49.
