# Data locations (read only; bloaterTS owns the trawl data, trawlcomp owns the mixed-tow definition)
BLOATERTS_RAW  <- "D:/pyprojects/bloaterTS/data/raw"
TRAWL_DIR      <- file.path(BLOATERTS_RAW, "trawl")
TOW_LIST_LH_BLOATERTS <- file.path(BLOATERTS_RAW, "LH_tow_list_2004_2018.csv")
TRAWLCOMP_R    <- "D:/pyprojects/trawlcomp/R"
PROJECT_DIR    <- "D:/pyprojects/mixedtows"
DATA_DIR       <- file.path(PROJECT_DIR, "data")
OUTPUT_DIR     <- file.path(PROJECT_DIR, "output")
TOW_LIST_LH    <- file.path(DATA_DIR, "LH_tow_list_mixed.csv")
