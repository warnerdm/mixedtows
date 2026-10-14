r"""Match each mixed tow to its acoustic data files (reads D:\Acoustics\Huron, read only).

Uses bloaterTS's match step (bloaterts.match_tows: pydt4's tow_matching with pydt4's rules for excluded tows,
unfiltered matches and vessel-17 channel checks) with this project's tow list and config/match_overrides.csv.
Writes data/acoustic/tow_matches.csv and data/acoustic/tow_files.csv.

    python scripts/02_match_tows.py
"""
import os
import sys

sys.path.insert(0, r"D:\pyprojects\bloaterTS\src")
from bloaterts.match_tows import match_tows  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_ROOTS = {"Huron": r"D:\Acoustics\Huron"}


def main():
    match_tows([os.path.join(ROOT, "data", "LH_tow_list_mixed.csv")], ARCHIVE_ROOTS,
               os.path.join(ROOT, "config", "match_overrides.csv"),
               os.path.join(ROOT, "data", "acoustic"))


if __name__ == "__main__":
    main()
