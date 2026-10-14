# mixedtows status

## Current state (2026-10-14)
- Project created. Mixed-tow definition from trawlcomp (user, 2026-10-14): J by number >= 0.4, >= 30 fish.
- Huron tow list done: `data/LH_tow_list_mixed.csv`, 41 tows (`analysis/01_tow_list.R`).
  - 2005-2018 (none 2004, 2006); vessel 88 dt4 38 tows, vessel 35 Simrad raw 3 (2012: 1, 2018: 2).
  - Only 93118 is also in bloaterTS's Huron list (row identical).
  - Builder check: bloaterTS's 88 Huron tows rebuilt with 0 differing cells.
  - Missing: SURF_TEMP 20, FISHING_TEMP 5, end coordinates 1 (not used by matching).
- pydt4 takes per-project inputs (pydt4 9e82590): run_tow_batch --regions / --corrections,
  run_simrad_tows regions_csv= / corrections=, plot_all_echograms --corrections. Pass "" for none, or this
  project's files; the defaults are bloaterTS's.
- Matching done (`scripts/02_match_tows.py`: bloaterTS's match step, bloaterts.match_tows, with this project's
  tow list and `config/match_overrides.csv`) -> `data/acoustic/tow_matches.csv`, `tow_files.csv`.
  - 35 ok (33 dt4, 2 Simrad 2018), all transect_only tier (filename; 58517 content-based, 2005). 6 excluded.
  - Check: 93118 matched the same 2 files as bloaterTS.
  - Excluded: 79281 (Huron 2009 is 38 kHz only; user rule 2026-10-13, as bloaterTS 79287). 58532, 58555,
    58580 (2005), 78319 (2008): no file covers the logged start and gps_trawl_check finds no candidate at the
    logged start or +-24 h -> excluded without investigation (user rule 2026-10-05). 85687 (Baird 2012, Simrad,
    so no gps_trawl_check): mw4 files run 2012-09-07 00:07-02:18, nothing at 03:59 on the logged date or a day
    later -> excluded the same way.
  - No start corrections needed so far (none of the 35 needed one to match).
- Calibration coverage of the 35: every vessel-year except vessel 88 2005 is one bloaterTS already processes in
  Huron (same table rows, lake rows where they exist). OPEN: vessel 88 Huron 2005 (58517, 58540) has only a
  blank-lake row (channel 3), from Michigan; check the Huron 2005 transducer serial/channel before using it
  (pydt4 rule). The Huron 2005 folder holds "Sturgeon 2005 new Cal 129 kHz Channel 3.ecs",
  "Steelhead Michigan 2005 new Cal 129 kHz Channel 1.ecs" and EV folders "Sturgeon EVfiles_where_120_is_channel1
  (MDNR equip)" / "..._channel3", so 2005 may have used two set-ups.

- 58517 and 58540 (Huron 2005) ON HOLD (user, 2026-10-14): exclude rows in config/match_overrides.csv -> 33 ok.
- CORRECTION (2026-10-14): the coverage note above was wrong. pydt4 has Huron calibrations only for Sturgeon 2004,
  2007, 2008, 2010, 2011 (provisional), 2014, 2015 (provisional), 2016 and Baird 2011, 2014, 2015, 2018 (pydt4
  STATUS: "do NOT run run_tow_batch on the whole LH list"). Of the 33: 19 runnable; 14 wait for a Huron
  calibration: Sturgeon 2012 (85699, 85711, 85746), 2013 (86749, 86782, 86786, 86828), 2017 (104608, 104708),
  2018 (107022, 107027, 107031, 107053, 107201).
- PRELIMINARY RUN (2026-10-14; no bad-data regions, no start corrections: --regions "" --corrections ""):
  data/derived/tow_results.csv: 19 ok (17 dt4 via run_tow_batch --op-ids; 2 Baird via run_simrad_tows; 85687 row
  no_file_match). Single targets in output/tow_single_targets/, echograms in output/echograms/ (plot_all_echograms).
  Check: 93118 identical to pydt4's tow_results row (no bloaterTS regions or correction for it).
  Nv median 0.004, max 0.029 (76725); median TS -57.2 to -43.5 dB (82904 highest); 89205 has 22% of the region
  below the bottom line.
- Catch per tow: data/derived/tow_catch.csv (analysis/03_tow_catch.R, trawlcomp tow_evenness).
- Share package (user, 2026-10-14; to upload to Box like bloaterTS review/share): scripts/08_share_package.py ->
  output/share/mixed_tows_huron.zip (15.9 MB): one HTML page (overview: catch by number and weight beside median
  TS and mean Sv, rows ordered by median TS; table; per tow catch table, TS histogram, echogram; inline SVG, no
  internet needed), img/, tows.csv, README.txt. Marked preliminary.

- ECHOVIEW PIPELINE (user, 2026-10-14: "do this with Echoview"; the project goes through Echoview as bloaterTS):
  bloaterTS's pipeline code (bloaterts package) run with this folder as root (scripts/_bloaterts.py).
  config/project.yaml + copies of bloaterTS st_method2.yaml, exports.yaml, nv_index.yaml, transducer_depths.csv
  (c27739e); calibration/ = bloaterTS's Huron ecs_checklist rows with ECS files (copies; bloaterTS is master).
  - Step 3 copy: 129 files, 33 tows, 4.3 GB -> data/acoustic/Huron/ (git-ignored), SHA-256 in tow_files.csv.
  - Step 4 EV files: 19 made (Echoview 16.1.73), no problems; channels as pydt4 (81791 ch1 from the data file).
  - Step 5 exports: 19 (107xxx/one tow: 2 region pings without a bottom pick, bottom 36 m below the region).
  - Step 6 Nv (data/derived/nv_by_tow.csv): median 0.0034, max 0.0234. Step 6b combined tables in data/derived/.
  - Echoview vs pydt4: dt4 17 tows |Sv diff| median 0.0002, max 0.0018 dB; targets 12,252 vs 12,253 (7 tows +-1).
    Simrad 2 tows 0.003 / 0.005 dB (known range-window convention); targets 340 = 340.
  - Step 7 fish tracks (scripts/07_fish_tracks.py: bloaterTS fish_tracks_all_gap0 run_tracks/summarize_tracks,
    gap 0, min 2 targets/pings, TS weight 0) -> echoview/fish_tracks/ (tow_track_summary.csv, tracks_all_tows.csv,
    targets_with_track.csv, figures/): 19 ok; targets used = pipeline in every tow, 0 assignment mismatches.
    1,970 fish tracks; share in tracks median 0.94 (107738 0.67, 30 targets). Per-fish minus per-ping mean TS
    -3.12 (93112) to +2.36 dB (93142), wider than the bloater tows (-1.07..+0.66). Strong fish (track mean TS >
    -35 dB) in 7 tows (76706 4, 76725 3, 81791 3): under the bloater rule (>= 13 dB above the median fish) they would
    be removed; for mixed tows the review rules are to be relaxed (user, 2026-10-14), not yet defined.
- Share package now includes the track figures and per-fish TS (scripts/08_share_package.py; 16.6 MB).

## Tasks
1. Huron calibrations for Sturgeon 2012, 2013, 2017, 2018 (14 tows) and the 2005 check (2 tows).
2. Define the relaxed review rules for mixed tows (what to include, exclude or flag; user), then the
   echogram review of the processed tows -> this project's bad-data regions (config/bad_data_regions.csv in
   bloaterTS's regions.csv format), and start corrections if a GPS window runs into the haulback.
3. Rerun (steps 4-7 for Echoview; pydt4 with --regions/--corrections) and rebuild the share package.
