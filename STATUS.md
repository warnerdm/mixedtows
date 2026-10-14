# mixedtows status

## Current state (2026-10-14)
- Project created. Mixed-tow definition from trawlcomp (user, 2026-10-14): J by number >= 0.4, >= 30 fish.
- Huron tow list done: `data/LH_tow_list_mixed.csv`, 41 tows (`analysis/01_tow_list.R`).
  - 2005-2018 (none 2004, 2006); vessel 88 dt4 38 tows, vessel 35 Simrad raw 3 (2012: 1, 2018: 2).
  - Only 93118 is also in bloaterTS's Huron list (row identical); 40 tows have never been matched.
  - Builder check: bloaterTS's 88 Huron tows rebuilt with 0 differing cells.
  - Missing: SURF_TEMP 20, FISHING_TEMP 5, end coordinates 1 (not used by pydt4 matching).
  - Read by pydt4 (`run_tow_batch.apply_tow_corrections`, `lake_from_tow_list` -> Huron).

## Tasks
1. pydt4: make the per-project inputs arguments (bloaterTS stays the default): the bad-data regions CSV
   (`bad_data.BLOATERTS_REGIONS_CSV`) and the tow start-time corrections (`run_tow_batch.TOW_START_CORRECTIONS`).
2. Calibration coverage: the calibration table row (vessel, year, channel, lake) for each tow.
3. Match the 41 tows to acoustic files (pydt4 matching on `D:\Acoustics\Huron`); screen failures with
   gps_trawl_check; record overrides here.
4. Echogram review of the matched tows -> this project's bad-data regions.
5. Run tow regions (Sv, Nv, single targets).
