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
- Share package (user, 2026-10-14; to upload to Box like bloaterTS review/share): scripts/04_share_package.py ->
  output/share/mixed_tows_huron.zip (15.9 MB): one HTML page (overview: catch by number and weight beside median
  TS and mean Sv, rows ordered by median TS; table; per tow catch table, TS histogram, echogram; inline SVG, no
  internet needed), img/, tows.csv, README.txt. Marked preliminary.

## Tasks
1. Huron calibrations for Sturgeon 2012, 2013, 2017, 2018 (14 tows) and the 2005 check (2 tows).
2. Echogram review of the processed tows -> this project's bad-data regions (config/bad_data_regions.csv in
   bloaterTS's regions.csv format), and start corrections if a GPS window runs into the haulback.
3. Rerun with this project's regions/corrections files; rebuild the share package.
