# Exhibit checklist (exhibit-reviewer)

Pull `get_qc_rules('exhibits')` (+ `fema`, `crs`, jurisdiction tag) and apply those rules first; this list adds the
standard and decision items. Each item gets Pass / Finding / N/A per sheet.

## A. Sheet standards (EXH-C03, D34, D36, D52)
- [ ] Report exhibits 11x17 (scalable to 22x34); CAD coordination exhibits 30x42 allowed; appendix 8.5x11 with the
      Psomas border (D36).
- [ ] Border and title block complete: firm, project no., figure no., scale, legend, north arrow, scale bar, source.
- [ ] Engineering scale; scale bar measured on the plotted sheet equals the stated scale.
- [ ] Text 9 pt minimum for new text; inherited CAD text 0.1 in absolute minimum (D34).
- [ ] One label type (Figure or Exhibit); numbering by section (Figure 4-1); continuous; matches TOC and text (D52).
- [ ] Consistent orientation and title-block position across the set; match lines / sheet key on multi-sheet exhibits.
- [ ] No pixelated raster images; style-variant search run (fonts, line weights, label styles consistent).
- [ ] Preparer shown as Psomas (initials); no footer date; no draft, working or tool names anywhere on the sheet.

## B. Legends (EXH-C04)
- [ ] Entry for every symbol shown; no entry for absent symbols.
- [ ] Graphic sample, not words, for every entry.
- [ ] Script log shows no empty-layer warnings, or each is resolved/noted.

## C. Base content and labeling (EXH-C05, D35, D40, D41, D42)
- [ ] Aerial at full strength under the full sheet (except the location/vicinity map, which has no aerial, D35);
      basemap source/year credit line.
- [ ] Major roads and landmarks labelled on every sheet.
- [ ] Every culvert labelled with cells, size, type; every structure numbered.
- [ ] Existing vs proposed distinguishable by layer/linetype and legend.
- [ ] Contours screened; 1-ft minimum on watershed exhibits, 0.5-ft on flat sites, 2-ft only for large offsite areas
      (D42); no unexplained red lines; labels inside the sheet with wipeouts.
- [ ] Drainage maps: node letters plus Q100 at CPs; full attributes in the report table (D41).
- [ ] Watershed boundaries thick dark/bright pink; flowlines cyan dashed with arrows; sheet-flow arrows short with
      squiggly leaders; basin labels show required/provided first flush, 100-yr volume, depth and WSEL.
- [ ] No draft or working names on parcels.

## D. Location / vicinity / project-area map (EXH-C06)
- [ ] One project-area map near the front; one defined term for limits; zone terms used only as defined
      (term-count search across text and exhibits).
- [ ] Scale, T-S-R and road labels present; borrowed figures credited and explained.

## E. 2D result exhibits (EXH-C07, D31-D33, D40, D43)
- [ ] Ramp stated on the sheet: "local" (<0.2 ft hidden, 0.2-0.5, 0.5-1.0, 1.0-2.0, 2.0-3.0, >3.0 ft; yellow, cyan,
      blue, orange, red) or "deep-flow" (0-3, 3-5, 5-10, >10 ft) (D31).
- [ ] Continuous class bounds, upper bound exclusive (D32); units shown; no stretched or 3-decimal legends.
- [ ] Display cutoff = bottom of the chosen ramp; difference maps hide |d| < 0.10 ft unless the agency threshold
      differs (stated on sheet) (D33).
- [ ] Result raster at 60 pct opacity over full-strength aerial (D40).
- [ ] Max depth/value checked for artifacts (closed-domain fill, wet-dry spikes).
- [ ] One exhibit set per storm named in the text; storm title on each sheet; inflow XS labelled with peak Q matching
      the discharge table.
- [ ] Difference sign, wet/dry rule and display threshold stated; velocity change exhibit accompanies WSEL change.
- [ ] Raster names follow <scenario>_<event>_<variable>_<units>_<cell>ft.tif; each maps to a plan in the dictionary
      (D43); provenance README present.

## F. FEMA content (EXH-C10, D39)
- [ ] SFHA extents and BFEs shown when present; effective date on sheet and in text; legend matches mapped zones.
- [ ] No empty NFHL subset issued; pending revisions shown separately and labelled preliminary.
- [ ] FIRM marking: tight box or sketched alignment, labelled; full panel only with the project marked tightly (D39).

## G. Values (EXH-C11, D30)
- [ ] Every Q and volume label traces to one register row and matches the report table.
- [ ] Required vs provided shown for each storage unit; outlet invert vs WQV rechecked after each size change.
- [ ] No independent-check values (40_QC) shown on a deliverable exhibit.

## H. Text cross-check (EXH-C02)
- [ ] Every exhibit cited in the text; pending values marked pending; unmodeled concepts labelled.
