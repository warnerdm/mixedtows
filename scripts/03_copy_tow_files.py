"""Step 3 (reads the acoustic archive; no dongle): copy the data files of "ok" tows into
data/acoustic/Huron/<year>/<vessel>/<transect>/ (git-ignored) and record their SHA-256 in data/acoustic/tow_files.csv
(bloaterts.copy_tow_files). Safe to rerun: files already copied are skipped.

    python scripts/03_copy_tow_files.py
"""
import os

from _bloaterts import ROOT
from bloaterts.copy_tow_files import copy_tow_files

if __name__ == "__main__":
    copy_tow_files(os.path.join(ROOT, "data", "acoustic"), ROOT)
