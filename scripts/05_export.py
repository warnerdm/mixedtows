"""Step 5 [Echoview dongle]: export each tow's results from its EV file (bloaterts.ev_export): noise-reduced Sv and
single targets by region, targets used, bottom line, calibration used, echogram image.

    python scripts/05_export.py 76701 76706
Output: echoview/exports/tow_<OP_ID>/; manifest in echoview/run_logs/export_<date_time>/.
"""
import sys

from _bloaterts import ROOT, tow_ids
from bloaterts.ev_export import export_tows

if __name__ == "__main__":
    result = export_tows(ROOT, tow_ids(sys.argv[1:]))
    print(result["status"].value_counts().to_string())
