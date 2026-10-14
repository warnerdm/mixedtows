"""Shared setup for the Echoview steps: bloaterTS's pipeline code (bloaterts package) run with this project as root."""
import os
import sys

BLOATERTS_SRC = r"D:\pyprojects\bloaterTS\src"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BLOATERTS_SRC not in sys.path:
    sys.path.insert(0, BLOATERTS_SRC)


def tow_ids(args):
    return [int(a) for a in args if not a.startswith("--")] or None
