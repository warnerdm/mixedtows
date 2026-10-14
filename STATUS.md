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

## Tasks
1. Huron 2005 calibration for 58517 and 58540 (see above; ask the user).
2. Echogram review of the 35 matched tows -> this project's bad-data regions (config/bad_data_regions.csv in
   bloaterTS's regions.csv format), and start corrections if a GPS window runs into the haulback.
3. Run tow regions (Sv, Nv, single targets) with pydt4, passing this project's regions/corrections files.
