# Catch of the five species (number, weight, J) for every tow in the mixed tow list -> data/derived/tow_catch.csv
suppressWarnings(suppressMessages(source("D:/pyprojects/mixedtows/R/tow_list.R")))
tl <- read_csv(TOW_LIST_LH, show_col_types = FALSE)
catch <- huron_tow_catch(tl$OP_ID)
dir.create(file.path(DATA_DIR, "derived"), showWarnings = FALSE)
write_csv(catch, file.path(DATA_DIR, "derived", "tow_catch.csv"), na = "")
cat(nrow(catch), "tows; J_n range", range(catch$J_n), "\n")
