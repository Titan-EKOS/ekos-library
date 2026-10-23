# Memo outlines

Headings below are the deliverable section names. Bracketed notes are instructions and never appear in the memo.
Every memo: purpose states what the memo documents or decides; Conclusions never empty; criteria table carries an
authority column; decisions carry the date and who made them; agency direction attributed to the meeting date.

## Format by memo size (D46, default, to confirm)
| Type | When | Layout |
|---|---|---|
| Letter memo | up to 10 pages, single topic | memo template; figures inline after first citation; no Contents, no List of Figures/Tables; running header with memo title; "Page x of y" |
| Multi-section technical memo | more than 10 pages or more than one topic | numbered main sections and subsections, Contents and List of Figures; 11x17 figures grouped at the end of their main section; Standard workbook in `--mode build` until the memo shell (TPL-02) exists |

## 1. Technical memorandum (TM) core
1. Purpose [what the memo documents: the approach and analyses supporting the design, or the decision being made;
   not the project description]
2. Background [project, location, what is designed or under construction]
3. Data Sources
4. Design Criteria [table: criterion | value | authority (manual, section, edition, or agency meeting date)]
5. Assumptions
6. Constraints
7. Decisions [table: decision | date | made by]
8. Methods [software and version, method reference]
9. Results [tables from native output; figures]
10. Summary and Conclusions [findings; next steps]
References [numbered 1), 2)]
Attachments [native output]

## 2. Drainage evaluation memo (existing 2D model)
1. Purpose
2. Analysis Approach [software and version, grid/cell size, Manning n basis (D28), flow source]
   - state that no new hydrology was done and flows come from the approved regional study [cite it];
   - state that regional flows applied to local areas give conservative depths.
3. Results
   - existing vs ultimate WSE; increases above the governing threshold [cite the agency or stakeholder threshold, D29]
     reported inside and outside ROW and at structures;
   - depth and difference figures attached.
4. Limitations [for qualitative concepts: not a full hydraulic design; does not pass Q100 without overtopping, where true]
5. Conclusions

## 3. Alternatives / justification memo (agency request)
Inputs: meeting transcript, meeting notes, one or two prior agency memos as format examples. Check every fact in
machine meeting notes against the transcript.
1. Purpose [the decision being made, including what is already designed or under construction]
2. Background
3. Alternatives [each defined once with a figure; same definition and name throughout]
4. Constraints (ROW, drainage)
5. Circulation / User Benefits [traffic data cited]
6. Constructability
7. Recommendation
References [cite specific parameters from each reference: speed, buffer width, volumes; not titles alone]

## 4. Crossing rise memo (RPT-C15)
For an agency or railroad owner who needs a reach memo on WSEL rise at a crossing.
1. Purpose
2. Modeling Effort [last proposed iteration only; models, plans, versions]
3. Assumptions and Data Gaps
4. Results
   - WSEL and velocity difference maps (existing vs proposed);
   - time above each rise threshold at common-wet cells (thresholds from the owner or agency, D29) with exceedance
     duration plot; note that maxima can occur at different cells (`scripts/rise_exceedance.py`);
   - depth x velocity^2 hazard for both conditions;
   - bridge and barrel flows shown separately.
5. Evaluation against owner criteria [railroad: subgrade and structure elevations, not one pass/fail rise limit]
6. Conclusions
