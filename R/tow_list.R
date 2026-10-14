# Tow list in the bloaterTS format (columns and rules of bloaterTS "R/1a. generate_trawl_data_from_rvcat.R"),
# so pydt4 reads it as it reads bloaterTS's LH_tow_list_2004_2018.csv. The LH_ file name prefix gives the lake.
library(tidyverse)
source("D:/pyprojects/mixedtows/R/paths.R")

OP_FIELDS <- c("OP_ID", "LAKE", "YEAR", "VESSEL", "OP_DATE", "TIME", "TRANSECT", "TOW_TIME", "FISHING_DEPTH",
               "BEG_LATITUDE_DD", "BEG_LONGITUDE_DD", "END_LATITUDE_DD", "END_LONGITUDE_DD",
               "BEG_DEPTH", "END_DEPTH", "TR_DESIGN", "MESH_SIZE", "SPEED", "FISHING_TEMP", "SURF_TEMP")
TRAWL_HT_M <- 10   # headrope-to-footrope height used for every tow, as bloaterTS

# Acoustic format by vessel and year, as bloaterTS: 35 and 37 Simrad raw; 17 dt4; 88 dt4 before 2022, raw after.
acoustic_format <- function(vessel, year) {
  case_when(vessel %in% c(35, 37) ~ "raw",
            vessel == 17 ~ "dt4",
            vessel == 88 & year < 2022 ~ "dt4",
            vessel == 88 ~ "raw")
}

# "25-OCT-04" + 242 -> "2004-10-25T02:42:00" (the logged date; after-midnight corrections are made in matching)
tow_datetime <- function(op_date, time) {
  time_str <- sprintf("%04d", as.integer(time))
  parts <- str_split_fixed(op_date, "-", 3)
  month <- match(toupper(parts[, 2]), toupper(month.abb))
  sprintf("20%s-%02d-%sT%s:%s:00", parts[, 3], month, parts[, 1], substr(time_str, 1, 2), substr(time_str, 3, 4))
}

# One row per OP_ID, from the USGS release OP.csv and TR_OP.csv (Huron)
build_tow_list <- function(op_ids) {
  op <- read_csv(file.path(TRAWL_DIR, "OP.csv"), show_col_types = FALSE, guess_max = 1e6) %>%
    filter(OP_ID %in% op_ids)
  tr_op <- read_csv(file.path(TRAWL_DIR, "TR_OP.csv"), show_col_types = FALSE, guess_max = 1e6) %>%
    filter(OP_ID %in% op_ids)
  tl <- inner_join(op, tr_op, by = "OP_ID", suffix = c("", ".tr")) %>%
    select(all_of(OP_FIELDS)) %>%
    mutate(TIME = as.character(TIME), trawl_ht = TRAWL_HT_M,
           datetime = tow_datetime(OP_DATE, TIME),
           acoustic_format = acoustic_format(VESSEL, YEAR),
           fishing_depth_source = "sensor(Simrad/Netmind/Marport)") %>%
    arrange(OP_ID)
  missing <- setdiff(op_ids, tl$OP_ID)
  if (length(missing)) warning("not in OP.csv/TR_OP.csv: ", paste(missing, collapse = ", "))
  tl
}

# Huron mixed tows from trawlcomp's definition (evenness.R: mixed_tows(), J by number >= 0.4, >= 30 fish)
# Runs in a separate R process (callr) because trawlcomp's scripts set their own paths in the global environment.
huron_mixed_op_ids <- function() {
  callr::r(function(f) {
    suppressWarnings(suppressMessages(source(f)))
    tows <- select_tows() %>% drop_bad_coordinates() %>% filter(lake == "Huron")
    mixed_tows(tow_evenness(tows))$OP_ID
  }, args = list(file.path(TRAWLCOMP_R, "evenness.R")))
}

# Catch of the five species per tow (numbers, weights, J; trawlcomp tow_evenness) for these OP_IDs
huron_tow_catch <- function(op_ids) {
  callr::r(function(f, ids) {
    suppressWarnings(suppressMessages(source(f)))
    tows <- select_tows() %>% filter(lake == "Huron", OP_ID %in% ids)
    tow_evenness(tows)
  }, args = list(file.path(TRAWLCOMP_R, "evenness.R"), op_ids))
}
