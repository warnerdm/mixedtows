"""Step 7 [Echoview dongle]: gap-0 fish tracks for each tow, then per-tow summaries, with bloaterTS's tracking code
and settings (bloaterTS echoview/experiments/fish_tracks_all_gap0: run_tracks.py, summarize_tracks.py; Echoview 16.1
fish-tracking defaults except maximum gap 0, minimum targets 2, minimum pings 2, TS weight 0; user, 2026-10-07).

The bloaterTS scripts are imported and pointed at this project: EV files from echoview/ev_files/, exports from
echoview/exports/, output to echoview/fish_tracks/ (raw/ git-ignored; tables and figures committed), Nv from this
project's pydt4 results (data/derived/tow_results.csv).

    python scripts/07_fish_tracks.py track [OP_ID ...]    (dongle; Echoview closed; default every ok tow)
    python scripts/07_fish_tracks.py summarize
"""
import importlib.util
import os
import sys

import pandas as pd

from _bloaterts import ROOT

EXP = r"D:\pyprojects\bloaterTS\echoview\experiments"
OUT = os.path.join(ROOT, "echoview", "fish_tracks")
sys.path.insert(0, os.path.join(EXP, "fish_track_pilot_2026-10-07"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def point_at_project(mod):
    mod.ROOT, mod.HERE = ROOT, OUT


if __name__ == "__main__":
    import fish_track_pilot
    fish_track_pilot.ROOT = ROOT                         # ping_range() reads this project's exports
    cmd, ids = sys.argv[1], [int(a) for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "track":
        rt = load("run_tracks", os.path.join(EXP, "fish_tracks_all_gap0", "run_tracks.py"))
        point_at_project(rt)
        rt.MANIFEST = os.path.join(OUT, "run_manifest.csv")
        if not ids:
            m = rt.load_inputs(ROOT)["matches"]
            ids = [int(t) for t in m.index[m["status"] == "ok"]
                   if os.path.exists(os.path.join(ROOT, "echoview", "exports", f"tow_{t}", "sv_by_region.csv"))]
        done = pd.read_csv(rt.MANIFEST) if os.path.exists(rt.MANIFEST) else pd.DataFrame(columns=["OP_ID", "status"])
        todo = [t for t in ids if t not in set(done.OP_ID[done.status == "ok"])]
        print(f"{len(ids)} tows, {len(todo)} to do", flush=True)
        ev = rt.start_echoview()
        for i, tow in enumerate(todo, 1):
            try:
                rec = rt.track_one(ev, tow)
            except Exception as e:
                rec = dict(OP_ID=tow, status="error", problem=f"{type(e).__name__}: {e}")
                ev = rt.start_echoview()
            print(f"[{i}/{len(todo)}] {tow}: {rec['status']} {rec.get('problem', '')}", flush=True)
            done = pd.concat([done[done.OP_ID != tow], pd.DataFrame([rec])], ignore_index=True)
            done.to_csv(rt.MANIFEST, index=False)
    elif cmd == "summarize":
        st = load("summarize_tracks", os.path.join(EXP, "fish_tracks_all_gap0", "summarize_tracks.py"))
        point_at_project(st)
        st.PYDT4_RESULTS = os.path.join(ROOT, "data", "derived", "tow_results.csv")
        st.main()
    else:
        sys.exit(__doc__)
