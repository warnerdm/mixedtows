# mixedtows

Acoustic tow-region data (as in bloaterTS) for midwater trawl tows whose catch was MIXED species, to look for
patterns in acoustic data that should come from mixed species. Lake Huron first.

**Read `STATUS.md` first.** It holds current status, decisions and the task list.

## Division of work
- trawlcomp (`D:\pyprojects\trawlcomp`) owns the "mixed" definition: `R/evenness.R` `mixed_tows()` (Pielou's J by
  number over alewife 106, smelt 109, cisco 202, bloater 204, emerald shiner 504, S fixed at 5; J >= 0.4 and
  >= 30 fish of the five; alewife in tows deeper than 40 m set to 0). This project calls it, never copies it.
- pydt4 (`D:\pyprojects\pydt4`) does the acoustic processing (matching, region Sv, Nv, single targets) with its
  settled conventions. This project holds only what is specific to these tows: the tow list, match overrides,
  start-time corrections, bad-data regions and outputs.

## Data (read only; never copy, edit, move or delete)
- Trawl data: `D:\pyprojects\bloaterTS\data\raw\trawl\` (USGS release for Huron: OP.csv, TR_OP.csv, TR_CATCH.csv).
- Acoustic data: `D:\Acoustics\Huron` (2004-2018 on disk). Never write there.
- Paths are set once in `R/paths.R`.

## Tow list
- `data/LH_tow_list_mixed.csv`, built by `analysis/01_tow_list.R` in the bloaterTS tow-list format (bloaterTS
  `R/1a. generate_trawl_data_from_rvcat.R`: same columns, trawl_ht 10 m, datetime from the logged OP_DATE/TIME,
  acoustic_format by vessel/year). The `LH_` prefix gives the lake to pydt4. Checked by rebuilding bloaterTS's 88
  Huron tows exactly.

## Matching
- `scripts/02_match_tows.py` (Python, echopype env) runs bloaterTS's match step on this tow list with
  `config/match_overrides.csv` (bloaterTS's format: exclude / accept_unfiltered / correct_start, with reasons)
  and writes `data/acoustic/tow_matches.csv` and `tow_files.csv`. Failed matches: screened with pydt4's
  gps_trawl_check (start coordinates from the tow list); no candidate -> excluded without investigation.

## Echoview steps (as bloaterTS; dongle)
- scripts/03_copy_tow_files.py, 04_make_ev_files.py <ids>, 05_export.py <ids>, 06_nv_index.py, 06b_combine_exports.py,
  07_fish_tracks.py track/summarize: bloaterTS's bloaterts code with this folder as project root (_bloaterts.py).
  Only tows with an ECS row in calibration/ecs_checklist.csv can be built.

## Processing (pydt4; cross-check)
- dt4: `python run_tow_batch.py --tows D:/pyprojects/mixedtows/data/LH_tow_list_mixed.csv --root D:/Acoustics/Huron
  --ecs data/ecs_parameters_usgs_steelhead.csv --out D:/pyprojects/mixedtows/data/derived/tow_results.csv
  --st-dir D:/pyprojects/mixedtows/output/tow_single_targets --regions "" --corrections "" --op-ids <calibrated tows>`
  (from pydt4). ONLY tows of vessel-years with a Huron calibration (see STATUS), never the whole list.
- Simrad: `tow_echograms.run_simrad_tows(<tow list>, "D:/Acoustics/Huron", results_csv=..., st_dir=..., regions_csv="",
  corrections="")` after run_tow_batch. Echograms: plot_all_echograms --tows --root --corrections --results --st-dir --out-dir.
- Share zip: `scripts/08_share_package.py` -> output/share/mixed_tows_huron.zip.

## Environment
- R 4.4.0: `C:\Program Files\R\R-4.4.0\bin\Rscript.exe`. Python: pydt4's `echopype` env (see pydt4 CLAUDE.md).
- Code lives in `R/` (functions); `analysis/` holds scripts that only call them; results go to `output/`.

## Working rules
- The user is the fisheries expert. One step at a time; ask before changing a settled choice.
- At session end, update `STATUS.md` and commit and `git push` (origin = github.com/warnerdm/mixedtows, private).
