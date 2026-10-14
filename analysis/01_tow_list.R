# Huron tow list of the mixed-species tows (trawlcomp definition), in the bloaterTS tow-list format.
# Check: the same builder applied to bloaterTS's 88 Huron OP_IDs must reproduce LH_tow_list_2004_2018.csv.
suppressWarnings(suppressMessages(source("D:/pyprojects/mixedtows/R/tow_list.R")))

ref <- read_csv(TOW_LIST_LH_BLOATERTS, show_col_types = FALSE, col_types = cols(.default = "c"))
chk <- build_tow_list(as.integer(ref$OP_ID)) %>% mutate(across(everything(), as.character))
cat("bloaterTS check: rows", nrow(ref), "rebuilt", nrow(chk), " same columns:", identical(names(ref), names(chk)), "\n")
diff <- map_int(names(ref), \(v) {
  a <- ref[[v]][order(as.integer(ref$OP_ID))]; b <- chk[[v]]
  num <- suppressWarnings(as.numeric(a)); numb <- suppressWarnings(as.numeric(b))
  sum(ifelse(!is.na(num) & !is.na(numb), abs(num - numb) > 1e-9, coalesce(a, "NA") != coalesce(b, "NA")))
}) %>% set_names(names(ref))
cat("cells differing per column:\n"); print(diff[diff > 0]); if (all(diff == 0)) cat("none\n")

ids <- huron_mixed_op_ids()
tl <- build_tow_list(ids)
write_csv(tl, TOW_LIST_LH, na = "")
cat("\nmixed tow list:", nrow(tl), "tows ->", TOW_LIST_LH, "\n")
print(count(tl, YEAR, VESSEL, acoustic_format), n = 50)
cat("in bloaterTS list:", paste(intersect(tl$OP_ID, as.integer(ref$OP_ID)), collapse = ", "), "\n")
cat("missing values:\n"); print(colSums(is.na(tl))[colSums(is.na(tl)) > 0])
