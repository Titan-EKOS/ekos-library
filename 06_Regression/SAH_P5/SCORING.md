# Phase 5 regression - SAH pilot (7SAH260101), scoring method

Regression job folder (outside git, models too large): `D:\EKOS\Regression\JCO_20261022_SAH_P5`.
Original work: `D:\7SAH260101_work` and the OneDrive job folder (read-only during the test).
Blind review tests: `D:\EKOS\Regression\JCO_20261022_SAHPARK_P5`, `D:\EKOS\Regression\JCO_20261022_CALFIRE_P5`.

## What is scored

| Measure | How it is counted | Baseline (original run, 2026-10-06 to 10-11) |
|---|---|---|
| Errors caught | Known defects from the original work (list below). A defect counts as caught when a library skill, agent check or QC rule flags it from files, before a person finds it. Detection pass runs the new checks read-only on the original outputs; the rerun counts defects that are prevented. | 0 of the listed defects were flagged by tooling at the time; all were found later by review or by the harvest. |
| Rework avoided | Sum of `hours_lost` on SAH cards whose cause the new skills prevent or flag early, checked against what happened in the rerun. | 43.0 h lost across SAH-001..020 (card estimates). |
| Time | Agent wall time and model wall time for the same scope. | About 25 h continuous agent time plus 43 h HEC-RAS queue; FLO-2D 2/10/25/50-yr never finished. |
| New findings | Defects the new checks found that the original work and the harvest did not record. | n/a |
| Blind review | qc-reviewer on a draft with the reviewer's markups removed; findings matched to the real markup (SAHPARK) or to a locked defect list (Cal_Fire) by a separate agent with the sets relabeled. Run with the full library, the library with that project's cards held out, and the previous v1 skills. | v1 skills = previous version. |

Pass rule (Phase 5): a new skill or agent version replaces the old one only if it scores at least as well on
every measure. Library bugs found by the test are logged as proposed changes (`PROPOSED_CHANGES.md`) and applied
only after JCO approval (Phase 6 rule).

## Known defects (seeded list)

| ID | Defect (original work) | Card | Expected catcher |
|---|---|---|---|
| K01 | FLO-2D nested handoff: inflow trapped in overlap strip, LOWER runs wasted | SAH-002 | flo2d-model-runs preflight (inflow nodes vs overlap) |
| K02 | FLO-2D run stalled 89.8 h vs 0.63 h base (time step collapse) | SAH-003 | model-run-supervisor stall watchdog / run_checks |
| K03 | ERROR.CHK HYSTRUC error and levee-crest warnings never fixed | SAH-006 | run_checks complete-flo2d / QC rule |
| K04 | 13 hand-edited queue files; PID waits broke after restart | SAH-001, SAH-015 | model-run-supervisor run register + detached launch |
| K05 | First RAS compute through ras-commander gave no result; queue rewritten 4 times | SAH-009 | hecras-2d-models ras_headless + register |
| K06 | Python from PATH lacked numpy/h5py after restart | SAH-015 | ENVIRONMENTS.md full interpreter paths |
| K07 | 30 pct draft issued with QC_Log 0/27, empty CalcRegister, 6 placeholders | SAH-013 | drainage-report-standard assembly gate / qc-reviewer |
| K08 | 226 assumptions unverified at draft issue | SAH-014 | qc-reviewer / report-writer gate |
| K09 | Narrative says 2- to 100-yr run in all models; FLO-2D only 100-yr | SAH-017 | report-writer run matrix check |
| K10 | USGS 2021 DEM contributed 0 cells to the composite | SAH-020 | project-intake terrain composite check |
| K11 | Only 3-hr 100-yr tested for the recommended alternative | SAH-011 | impact-comparison / qc-reviewer |
| K12 | openpyxl stale formula values; compiled PDF 23.8 MB | SAH-012 | drainage-report-standard xl_recalc + compile size check |
