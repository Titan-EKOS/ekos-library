# Phase 3 build ranking

Score = sum over source cards of hours_lost x recurrence. A cluster that feeds two targets counts toward both, so
scores overlap. QC-rule recurrence often counts individual redline comments (e.g. QC-C11 = 366 from 130 agency
comments), so read QC scores alongside hours and project count. Per-cluster ranking: all_rank in each group file.

## Proposed Phase 4 build (in order)

| # | Master | Kind | Score | Hours | Clusters | Notes |
|---|---|---|---|---|---|---|
| 1 | 05_QC_Rules/rules.md | QC rules | 1730 | 377 | 58 | about 70 rules, each tied to its redline or review card |
| 2 | model-run-supervisor | agent | 631 | 134 | 15 | HEC-RAS / FLO-2D / HMS queues, preflight, acceptance gate, status file |
| 3 | drainage-report-build | update + 7 add-ons | 469 | 148 | 26 | core + pima-rfcd, city-of-tucson, town-of-marana, town-of-sahuarita, fema, placer-county-ca, caltrans-california |
| 4 | flo2d-model-runs | new skill | 429 | 101 | 9 | run harness, engine build, 1D channels, structures, result mapping |
| 5 | drainage-report-exhibit-standards | update | 311 | 42 | 11 | sheet standards, base content, ramps, sizes, FIRM marking |
| 6 | ekos-local-supervisor | agent (proposed) | 308 | 21 | 3 | cloud budget, local queue worker, morning package |
| 7 | hecras-2d-models | new skill | 208 | 55 | 5 | scripted build, native automation, stability triage, project hygiene |
| 8 | Drainage Report Standard v0.4 | update | 172 | 45 | 12 | assembly gate, decision register, folder map, numbering, PDF size, bookmarks, recalc, licensed tools |
| 9 | due-diligence-researcher | agent | 172 | 58 | 10 | prior/adjacent study screen, existing-conditions check, jurisdiction confirm |
| 10 | qc-reviewer | agent | 138 | 87 | 5 | independent review, submittal audit, blind-rebuild mode, mock agency review |
| 11 | scripted-exhibit-sheets | new skill | 130 | 27 | 3 | register-driven values; scope per D37 |
| 12 | fema-clomr-lomr | new skill | 124 | 81 | 2 | AD responses, package build, pre-upload QC |
| 13 | swmm-ssa-storm-drain | new skill (Placer add-on) | 121 | 13 | 1 | |
| 14 | cad-base-update | new skill | 116 | 16 | 4 | consultant base reissue, Civil 3D helper loads, LandXML handoff |
| 15 | report-writer | agent | 113 | 39 | 6 | always paired with qc-reviewer |
| 16 | impact-comparison | new skill (+FEMA add-on) | 108 | 37 | 1 | matched existing/proposed models, 5 projects |
| 17 | hecras-result-rasters | update | 102 | 21 | 4 | volume pre-check, terrain warning, naming, mask vs display |
| 18 | project-intake | new skill | 64 | 27 | 5 | intake, terrain/DEM, public GIS harvest, CRS log |
| 19 | pchydro-hydrographs | update | 54 | 11 | 4 | batch mode, terms, native vs adjusted series |
| 20 | groundwater-reinfiltration-sizing | new skill (Placer) | 50 | 10 | 1 | |
| 21 | legacy-calc-reproduction | agent (proposed) | 49 | 17 | 1 | Toolbox / Hydraflow / HY-8 reruns of legacy calcs |
| 22 | drainage-technical-memo | new skill | 42 | 12 | 1 | |
| 23 | hy8-native-runs | new skill | 41 | 12 | 1 | template writer, supervised export |
| 24 | agency-comment-response | new skill | 35 | 26 | 2 | log template, status vocabulary (D45) |
| 25 | hechms-headless | new skill | 30 | 10 | 4 | 4.13 per D01 |
| 26 | exhibit-reviewer | agent | 17 | 4 | 2 | low card score, but it enforces the rules in #1 and #5 |
| 27 | local-model-gateway | new skill | 18 | 3 | 1 | role table per D15 |
| 28 | delivery-package-build | new skill | 9 | 4 | 1 | |
| 29 | project-harvest | new skill | - | - | - | Phase 6 closeout skill |

## Deferred (low score or single use; kept in clusters for later)
blender-crossing-renderings (20), proposal-drainage-approach (20), ekos-environment-rules (15; folded into
local-model-gateway), grading-footprint-screening (11), knowledge-lesson-lifecycle (8), software-install-validation (5.5),
hecras-1d-network-build (4.5), project-coordination-tracker (4), archive-recovery (3), session-continuation (2;
folded into model-run-supervisor), concept-site-layout (2), crossing-rise-impact-memo (2), bluebeam-mcp-setup (1.5),
construction-phasing-plan (1).
