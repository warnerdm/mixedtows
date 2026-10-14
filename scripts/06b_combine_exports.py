"""Step 6b (no dongle): stack the exports over all tows into data/derived/ (bloaterts.combine_exports)."""
import sys

from _bloaterts import ROOT, tow_ids
from bloaterts.combine_exports import TABLES, combine_all

if __name__ == "__main__":
    for name, df in combine_all(ROOT, tow_ids(sys.argv[1:])).items():
        print(f"{TABLES[name]}: {len(df)} rows, {df.OP_ID.nunique() if len(df) else 0} tows")
