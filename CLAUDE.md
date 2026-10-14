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

## Environment
- R 4.4.0: `C:\Program Files\R\R-4.4.0\bin\Rscript.exe`. Python: pydt4's `echopype` env (see pydt4 CLAUDE.md).
- Code lives in `R/` (functions); `analysis/` holds scripts that only call them; results go to `output/`.

## Working rules
- The user is the fisheries expert. One step at a time; ask before changing a settled choice.
- At session end, update `STATUS.md` and commit and `git push` (origin = github.com/warnerdm/mixedtows, private).
