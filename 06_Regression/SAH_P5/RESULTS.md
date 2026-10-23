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

## 3b. RAS volume error - trial and cause
- Trial: p01 at 1SEC finished with 0.283 pct volume error (2SEC original 0.270 pct); wall 4.21 h on cores 12-27.
  Time step is not the cause; the 1SEC queue was not launched.
- Diagnosis (read-only, HDF volume accounting and residual cells): p01 error is about 2 ac-ft of 698 ac-ft in;
  p06 5.2 of 1348 ac-ft. Cell 191222 holds the max volume residual in 71 pct of p06 steps and 51 pct of p01 steps.
  It sits at the I-19 crossing, where NBI-05788, NBI-06342 and NBI-06343 are three SA/2D connections stacked 5 ft
  apart, each about 530 ft long across the corridor: three parallel culverts in one place. The structures are really
  in series (west ramp 3-10x4, mainline 3-10x5, east ramp 3-10x5). Same defect as FLO-2D M-01, in both models.
  Second residual cluster at the UPRR connection DUPRR-KH. -> new finding M-03.
- RAS rerun stopped; next step (JCO): rebuild the crossing in series in the RAS geometry, test p01/p06 at 2SEC.

## 3c. FLO-2D rerun (library harness, model-run-supervisor job table)
20 runs (UPPER/LOWER x 3-hr/24-hr x 2/10/25/50/100-yr) on two 8-thread streams, cores 0-11 and 28-31,
2026-10-22 18:50 to 10-23 08:43 (13.9 h wall, about 27.6 h of solver time). No stalls, no dialog stops, no reruns.
The original work finished only the 100-yr pairs (the 3-hr MineFill run stalled 89.8 h and blocked the queue);
the 2- to 50-yr FLO-2D set now exists for both durations.

| Run | Solver h (new) | Original 100-yr solver h |
|---|---|---|
| UPPER 3-hr 100-yr | 0.54 | 0.63 |
| LOWER 3-hr 100-yr | 0.84 | 0.82 |
| UPPER 24-hr 100-yr | 1.73 | 1.86 |
| LOWER 24-hr 100-yr | 2.54 | 2.91 |
| UPPER 3-hr 2/10/25/50 | 0.29 / 0.33 / 0.43 / 0.47 | not run |
| LOWER 3-hr 2/10/25/50 | 0.60 / 0.62 / 0.76 / 0.72 | not run |
| UPPER 24-hr 2/10/25/50 | 1.16 / 1.24 / 1.59 / 1.64 | not run |
| LOWER 24-hr 2/10/25/50 | 2.27 / 2.05 / 2.65 / 2.16 | not run |

Checks: every run complete by D04 (termination line, outputs, no TMP). Overlap-strip handoff (s41) conserved
volume on every pair (e.g. 24-hr 100-yr 1540.6 -> 1540.6 ac-ft). ERROR.CHK: UPPER 5 errors / 13 warnings (original
8 / 15) - the HYSTRUC repeated-inflow-node error is gone after the series rebuild; remaining items are levee crests
below adjacent ground, outflow cells beside I-19 levee cells on the east boundary, and a CADPTS note (all present in
the original). LOWER 4 / 1, same as the original. Volume conservation still read by hand (P5-07). Every new run is
flagged "stale output" by run_checks - false positive (P5-12).

Effect of the I-19 series fix (MAXWSELEV, same grid, 100-yr):
- UPPER: 153 of 309,211 cells change more than 0.1 ft, all at the I-19 crossing. West of the west ramp -3.1 ft
  (ponding behind the ramp now drains through its culvert); mainline to east ramp -6.1 to -6.7 ft; ramp to mainline
  and east of the east ramp +0.5 to +0.85 ft.
- LOWER: water surface rises up to 0.48 ft in 703-912 cells (none over 0.5 ft) because more flow now passes the
  crossing. The original LOWER results understate flow reaching the La Villita corridor from this crossing; the
  report and the RAS model (M-03) need the same correction.

Errors caught / rework (FLO-2D): K02 stall prevented (watchdog armed, none occurred); K03 caught and the structure
error fixed; K04 replaced by one job table (no hand-written stream files; one driver bug found and fixed in about
5 min, no solver time lost); K06 prevented (full interpreter paths). K01 handled by the imported s41 step (P5-08).

## 4. Pending
- RAS crossing rebuild in series (JCO); report text and RAS results to be updated for the I-19 correction;
  time/rework summary across all parts.
