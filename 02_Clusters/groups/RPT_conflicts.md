# RPT conflicts

1. **RPT-X01 Status, partial dispositions and open items in the deliverable vs internal only** (RPT-C05)
   - Side A: Responses must read as completed ("has been revised", never "will"); agency-acceptance status and open items stay in a separate internal record, not in the deliverable. (CAMPBELL-015; VALENCIA-007 "final forms must state what was done")
   - Side B: Response matrix dispositions comments as Incorporated / Partial / Deferred and carries a remaining-items table by workstream inside the issued memo. (TANGERINE-002) Open items go in a separate memo on the memo template (issued with the report). (CALFIRE-013) Existing skill: "open items listed" before submittable, location not stated. (drainage-report-build sec. 4)
   - Why it matters: decides whether an agency sees deferred items. Likely resolution: Partial/Deferred allowed for planning-level or internal/mock reviews; agency resubmittals use completed tense with open items internal. Needs EOR rule.

2. **RPT-X02 Memo format: inline figures, no lists vs Contents and List of Figures with grouped 11x17 figures** (RPT-C06, RPT-C08)
   - Side A: Memos place figures inline after first citation with no List of Figures/Tables; memos use the _Electronic-Memo.doc template. (drainage-report-exhibit-standards sec. 0 item 2 and item 4)
   - Side B: H&H memos built with numbered sections, Contents and List of Figures, 11x17 figures grouped at the end of each main section. (RKN-014, EOR format patches) Evaluation memo appends depth/difference figures after the text. (ELTORO-018)
   - Why it matters: memo builders get restructured late (RKN-014 rework). Need a size/type threshold (e.g. letter memo vs multi-section TM).

3. **RPT-X03 Table style: header color + alternating shading vs thin borders only** (RPT-C06)
   - Side A: Psomas table style = standard header row color with white text, alternating row shading, no highlight fills, centered. (SAHPARK-004)
   - Side B: Thin line borders on all cells, no heavy borders, text centered (no mention of fills). (drainage-report-build sec. 2; drainage-report-exhibit-standards sec. 2; VALENCIA-009)
   - Why it matters: scripted builders apply one style globally. Confirm the table style actually defined in Report_Template_7 and write it into Standard v0.3.

4. **RPT-X04 Markups in the compiled PDF: flatten vs remove** (RPT-C10)
   - Side A: Flatten markups before submittal (flattened but recoverable); highlight relevant Q values in reference studies; place markup over table numbers in images. (CAMPBELL-020)
   - Side B: Final report must not carry plan revision clouds - remove them from the compiled copy, keep original marked PDFs; preserve annotation appearance or flatten when merging. (VALENCIA-008) Source LOMR FreeText annotations: flatten or note them. (CALFIRE-014)
   - Why it matters: a single compile rule is needed per annotation class (author highlights = flatten; inherited plan revision clouds = remove; third-party FreeText = flatten or note).

5. **RPT-X05 0.1 ft rise as a threshold** (RPT-C08, RPT-C14, RPT-C15)
   - Side A: Report WSE increases above 0.10 ft inside/outside ROW and at structures (ELTORO-018); compute time above 0.1/0.5/1.0 ft rise (CAMPBELL-024).
   - Side B: Do not treat a 0.1 ft rise as a universal trigger; railroad guidance uses subgrade/structure elevations, not one pass limit. (SILVERBELL-016, CAMPBELL-024)
   - Why it matters: the threshold must be cited from the governing jurisdiction (Pima County RFCD / Sahuarita / FEMA / railroad) per project, not hardcoded. Belongs in jurisdiction add-ons.

6. **RPT-X06 HEC-HMS version** (RPT-C02)
   - Side A: HEC-HMS 4.12 headless. (drainage-report-build sec. 3)
   - Side B: HEC-HMS 4.13 used in the RKN chain. (RKN-001)
   - Why it matters: skill version string and headless run.py calls must match the installed build; confirm which version is standard (cross-check hydrology group).

7. **RPT-X07 Excel recalc method** (RPT-C01)
   - Side A: CalculateFull on the calcs workbook via Excel COM. (CALFIRE-013) xl_recalc.ps1 (method not stated). (SAH-012)
   - Side B: Private DispatchEx instance with events/macros/link updates off and CalculateFullRebuild, then semantic compare. (EKOS-LOCAL-018)
   - Why it matters: CalculateFull may leave stale dependency chains; a shared instance can touch the user's open workbooks. Standardize xl_recalc in Standard v0.3 on CalculateFullRebuild in a private instance.

8. **RPT-X08 Comment-response log: inside compiled PDF behind cover vs separate deliverable** (RPT-C05, RPT-C10)
   - Side A: Response table / agency forms placed directly behind the cover page of the resubmitted report. (CAMPBELL-015, VALENCIA-007)
   - Side B: Comment-response log listed as a separate deliverable alongside the report and compiled PDF. (drainage-report-build sec. 4; drainage-report-exhibit-standards sec. 5)
   - Why it matters: compile manifest order. Possibly both (separate editable log + bound copy); Pima County RFCD add-on should state it.

9. **RPT-X09 Blank pages** (RPT-C10, RPT-C06)
   - Side A: Insert intentionally blank pages for future items. (CAMPBELL-020)
   - Side B: No half-empty pages; remove large white areas; remove unneeded pages and unrequested appendices. (drainage-report-build sec. 2; SAHPARK-005; VALENCIA-008)
   - Why it matters: minor; rule should read "placeholder pages only for named future items, labeled 'intentionally blank'; no blank areas in the body".

Gaps noted (not conflicts, need a Standard v0.3 decision):
- Figure/table numbering scheme (sequential vs by section, e.g. Figure 4-1) not defined; caused a full exhibit re-render. (CALFIRE-013, SAHPARK-004)
- No stated PDF size limit / compression target; sizes ranged 23.8 MB to 1 GB. (SAH-012, RKN-015, VALENCIA-008, TANGERINE-011)
- Minimum bookmark set not in existing skills (they only say "verify every bookmark resolves"). (TANGERINE-016)
