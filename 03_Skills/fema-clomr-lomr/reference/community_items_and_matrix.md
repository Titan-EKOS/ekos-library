# CLOMR/LOMR community items and AD response matrix

Reference for fema-clomr-lomr Steps 3 and 6. Source cards: STARVALLEY-006, STARVALLEY-018,
STARVALLEY-005, BARNETT-004.

## 1. Community items (long lead: start the day the case starts or the AD letter arrives)

| Item | Needed when | Content checks | Who signs |
|---|---|---|---|
| Flooding-source name acceptance | Each new or revised Zone AO / AH / AE flooding source | One name per source, matching the work map, FIRM annotation and report text | Community floodplain administrator (letter or email) |
| Operation and maintenance (O&M) plan | Any FEMA-required detention basin, channel or levee-like feature credited in the proposed condition | See O&M checklist below | Community official signature or written concurrence |
| Owner notification | Any property where BFE rises, SFHA is added, or floodway changes (44 CFR 65.12 cases) | FEMA **CLOMR** owner-notification template for a CLOMR (not the LOMR template); approved flooding-source names; draft submitted to the community/FEMA before mailing | Applicant, after draft acceptance |
| Community acknowledgement (MT-2 Form 1 / community concurrence) | Every case | Every community with jurisdiction listed | Pima County RFCD as community; in the Town of Marana the Town also signs (BARNETT-004) |

### O&M plan checklist
- [ ] Names each FEMA-required basin and channel (same names as the model, work map and report).
- [ ] Community (not an HOA) is the ultimate responsible party.
- [ ] States who performs maintenance and how often (inspection frequency, after-event inspection,
      sediment removal trigger).
- [ ] Scope does not exclude publicly owned basins or channels.
- [ ] Carries a community official signature block or a written concurrence attached.
- [ ] Matches the proposed-condition model geometry (storage, outlet, spillway).

Failure seen: revised O&M named the HOA as responsible party, excluded public basins, lacked a
community signature block and did not name the basins; two community items stayed open at closure
and at the new-case build (STARVALLEY-018).

### Day-one email list (draft on day one; these are the long-lead items)
1. Flooding-source names for acceptance (list with map excerpt).
2. O&M plan draft for community review and signature.
3. Owner-notification draft (CLOMR template) for review before mailing.
4. Any decision the agency rejected before: request a call date (Step 3.5 of the skill).

## 2. AD response matrix columns

One row per FEMA comment. The matrix is an editable separate deliverable plus a bound copy where the
agency asks (D49). Status vocabulary per D45.

| Column | Content |
|---|---|
| AD item | Letter and item number (e.g. AD02-14) |
| Comment text | Verbatim from the letter |
| Response | What changed, in completed tense |
| Status | Addressed / Partial / Assumed / Not Addressed / Cannot Determine / Stale (D45) |
| Disposition | incorporated / superseded / no change |
| Evidence file | File name in the upload package |
| Folder | Package folder (zip member path) |
| Report page | Page or section in the report / TDN |
| Model run date | Output timestamp of the run that supports the response (later than last input edit) |
| Verified by | Independent auditor initials or agent id and date |

Rules:
- Ship only when every row is Addressed (or Stale with file evidence that disproves the repeated
  text). Partial, Assumed, Not Addressed or Cannot Determine stops the upload.
- A row may not cite a file that is not in the archived upload package.
- Stale rows: about a third of one closure letter repeated prior-letter wording that the files
  disproved; the cover letter states this with the file evidence, without arguing (STARVALLEY-005).
- The letter text is generated from the matrix, not typed separately, so letter and matrix cannot
  disagree. A working letter once carried 10 TO BE CONFIRMED placeholders while the uploaded PDF
  stated the items complete (STARVALLEY-005).

## 3. Deadline worksheet (AD letter)

| Line | Value |
|---|---|
| AD letter date (received) | YYYYMMDD |
| Response deadline (90 days, no extension) | letter date + 90 d |
| Last model input edit allowed | deadline - 14 d (default) |
| Last model run complete | deadline - 10 d at latest |
| Package QC gate + independent audit | deadline - 7 d |
| JCO sign-off | deadline - 5 d |
| Upload | deadline - 3 d target |
Record the worksheet in `00_Admin/` and the open-items document (D44). Early submittal is not a
goal: a response sent 37 days early with unrun models and missing community letters closed the case
(STARVALLEY-006).
