# Phase 5 regression - results (running log)

## 1. SAHPARK blind review (Draft 3 drainage memo, JCO redlines as answer key)
Method: JCO's markups removed from the draft (other authors' appendix divider titles kept); three reviewers worked
from the clean pages only, each with a different standard; a fourth agent matched findings to JCO's 50 text comments
with the sets relabeled. Leave-out = SAHPARK and PHXZOO cards and the 3 rules sourced only from them removed,
gotcha lines scrubbed.

| Standard | Findings | Hit | Partial | Miss | Hit rate (50) | Hit rate (42 visible*) | Valid extra | Noise |
|---|---|---|---|---|---|---|---|---|
| Previous skills (v1) | 72 | 28 | 7 | 15 | 56 pct | 67 pct | 38 | 2 |
| Library, SAHPARK held out | 89 | 36 | 4 | 10 | 72 pct | 86 pct | 44 | 5 |
| Library, full (in-sample) | 107 | 38 | 3 | 9 | 76 pct | 90 pct | 57 | 6 |

*8 comments (J31, J36-J42) need local knowledge not visible in the draft (subdivision built, school-plan pipes,
high-school ditch, zoo runoff, flow magnitude); all three reviewers missed them.

Reading: the held-out library catches 8 more of JCO's comments than the v1 skills (36 vs 28) on a project it did not
learn from, so the gain is not only memorized SAHPARK lessons. Gaps specific to held-out: engineering-scale scale
bar and Psomas border detail (in the full library from SAHPARK cards), property owner, pending FIRM.
Pass rule: new >= old on errors caught -> PASS (qc-reviewer, drainage-technical-memo, exhibit standards).
Files: D:\EKOS\Regression\JCO_20261022_SAHPARK_P5 (answer key, clean pages); scores.json in the regression folder.

## 1b. Cal_Fire SR-104 blind review (issued package: compiled report, checklist, open-items memo)
Answer key: 7 defects in the issued package traced to CALFIRE cards, locked before the reviews ran.
Leave-out = CALFIRE cards and the 2 rules sourced only from them removed. Matched blind (sets relabeled).

| Standard | Findings | Key hits (7) | Partial | Miss | Valid extra | Noise |
|---|---|---|---|---|---|---|
| Previous skills (v1) | 66 | 5 | 1 | 1 | 47 | 6 |
| Library, CALFIRE held out | 57 | 6 | 0 | 1 | 42 | 1 |
| Library, full (in-sample) | 70 | 7 | 0 | 0 | 54 | 5 |

Per item: CF1 checklist vs open items, CF2 re-typeset native output, CF3 bookmark order, CF5 constant HY-8 crest,
CF6 assumed bridge geometry - caught by all three. CF4 (0.2 pct zone missing on Figure 3-1) caught only by the
full library. CF7 (lidar limitation behind the FEMA bias) caught by both library versions, partial with v1.
Pass rule: new >= old -> PASS. Note: v1 skill text still names HEC-HMS 4.12 (one v1 finding flagged 4.13 as a
deviation; D01 made 4.13 the standard).

## 2. SAH HMS rerun
50 runs through hechms-headless scripts (Project API, confirmed): all 1950 matched element peaks within 0.01 cfs of
the original (max rel diff 2e-7). Compute about 22 min with RAS holding most cores (original chain about 40 min).
Library issues found: P5-02, P5-03, P5-04, P5-05.

## 3. SAH detection pass (new checks on the original outputs, read-only)
- RAS: 6 of 10 original plans exceed the 0.1 pct volume error limit (p01 0.27, p06 0.39, p07 0.12, p08 0.12,
  p09 0.18, p10 0.17); original queue checked only the finish message. -> new finding.
- FLO-2D: ERROR.CHK errors flagged in every original run (K03 caught); LOWER_3hr_100yr_MineFill incomplete
  (no termination line, MAXWSELEV missing) flagged; stale outputs from earlier runs flagged in all UPPER folders.
- FLO-2D: the HYSTRUC error was three in-series I-19 culverts snapped to the same nodes (modeled as parallel) -> new
  finding M-01.
- K02 stall (89.8 h vs 0.63 h): not caught by the completion check after the fact (wall time is a live-run check).

## 4. Pending
- RAS 1SEC trial (p01) then full queue; FLO-2D 10 pairs (started 2026-10-22 18:50); time and rework scoring.
