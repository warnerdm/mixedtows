"""Step 4 [Echoview dongle]: build one EV file per tow (bloaterts.ev_build, bloaterTS settings).

    python scripts/04_make_ev_files.py 76701 76706     # these tows (tows without an ECS row in
                                                        # calibration/ecs_checklist.csv fail with that reason)
EV files: echoview/ev_files/ (git-ignored); run logs: echoview/run_logs/build_<date_time>/.
"""
import sys

from _bloaterts import ROOT, tow_ids
from bloaterts.ev_build import build_ev_files

if __name__ == "__main__":
    result = build_ev_files(ROOT, tow_ids(sys.argv[1:]))
    print(result["status"].value_counts().to_string())
