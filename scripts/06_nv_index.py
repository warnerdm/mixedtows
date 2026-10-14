"""Step 6 (no dongle): Sawada Nv per tow region from the exports (bloaterts.nv_index) -> data/derived/nv_by_tow.csv."""
import sys

from _bloaterts import ROOT, tow_ids
from bloaterts.nv_index import nv_all

if __name__ == "__main__":
    df = nv_all(ROOT, tow_ids(sys.argv[1:]))
    print(f"{df.nv.notna().sum()} of {len(df)} tows with Nv; median {df.nv.median():.4f}, max {df.nv.max():.4f}")
    bad = df[df.problems.fillna("") != ""]
    if len(bad):
        print(bad[["OP_ID", "problems"]].to_string(index=False))
