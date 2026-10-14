r"""Share package of the mixed-tow results, to upload as one zip (as bloaterTS review/share_review.py).

Writes output/share/mixed_tows_huron/ and output/share/mixed_tows_huron.zip (git-ignored; rebuilt in seconds):
    mixed_tows_huron.html   one page: an overview of every processed tow (catch composition by number and by weight
                            beside the tow's single-target TS and mean Sv), a table, and one section per tow (catch,
                            TS histogram, echogram). Charts are inline SVG, so the page needs no internet.
    img/                    the pydt4 echogram of each tow
    tows.csv                one row per tow: catch, J, acoustic results
    README.txt              what the package is, definitions, and what is not done yet

Inputs (this project): data/LH_tow_list_mixed.csv, data/acoustic/tow_matches.csv, data/derived/tow_catch.csv,
data/derived/tow_results.csv (pydt4), output/tow_single_targets/, output/echograms/.

    python scripts/08_share_package.py          (echopype env)
"""
import glob
import html
import os
import shutil

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "mixed_tows_huron"
OUT = os.path.join(ROOT, "output", "share", NAME)
ST_DIR = os.path.join(ROOT, "output", "tow_single_targets")
ECHO_DIR = os.path.join(ROOT, "output", "echograms")
TRACK_DIR = os.path.join(ROOT, "echoview", "fish_tracks")

# Species in a fixed order; categorical slots 1-5 of the reference palette (light, dark)
SPECIES = [("alewife", "Alewife"), ("smelt", "Rainbow smelt"), ("cisco", "Cisco"), ("bloater", "Bloater"),
           ("emerald_shiner", "Emerald shiner")]
COLORS = [("#2a78d6", "#3987e5"), ("#eb6834", "#d95926"), ("#1baf7a", "#199e70"), ("#eda100", "#c98500"),
          ("#e87ba4", "#d55181")]
TS_RANGE = (-60, -30)
VESSELS = {88: "Sturgeon (dt4)", 35: "Baird (Simrad EK60/EK80)"}


def esc(x):
    return html.escape(str(x))


def fmt(x, nd=1):
    return "" if pd.isna(x) else f"{x:.{nd}f}"


def load():
    tl = pd.read_csv(os.path.join(ROOT, "data", "LH_tow_list_mixed.csv"))
    matches = pd.read_csv(os.path.join(ROOT, "data", "acoustic", "tow_matches.csv"))
    catch = pd.read_csv(os.path.join(ROOT, "data", "derived", "tow_catch.csv"))
    res = pd.read_csv(os.path.join(ROOT, "data", "derived", "tow_results.csv"))
    res = res[res.status == "ok"]
    d = (res[["OP_ID", "mean_sv_db", "nv", "st_n_targets", "st_mean_ts_db", "st_median_ts_db", "channel_freq_hz",
              "bottom_frac_region_masked", "acoustic_format"]]
         .merge(tl[["OP_ID", "YEAR", "VESSEL", "TRANSECT", "datetime", "TOW_TIME", "FISHING_DEPTH", "BEG_DEPTH",
                    "END_DEPTH", "BEG_LATITUDE_DD", "BEG_LONGITUDE_DD"]], on="OP_ID")
         .merge(catch.drop(columns=["YEAR", "VESSEL", "lake", "transect", "time", "lat", "lon"]), on="OP_ID"))
    tr = pd.read_csv(os.path.join(TRACK_DIR, "tow_track_summary.csv"))
    d = d.merge(tr[["OP_ID", "fish_tracks", "frac_in_tracks", "ts_per_fish_median", "strong_tracks"]], on="OP_ID",
                how="left")
    targets = {}
    for op in d.OP_ID:
        f = os.path.join(ST_DIR, f"{op}_single_targets.csv")
        targets[op] = pd.read_csv(f, usecols=["TS_comp"]).TS_comp.to_numpy() if os.path.exists(f) else np.array([])
    return tl, matches, d.sort_values("st_median_ts_db", ascending=False).reset_index(drop=True), targets


def stacked_bar(x0, y, w, h, vals, op, basis, unit):
    """100% stacked bar of the five species; 2 px surface gap between segments; tooltips per segment."""
    tot = sum(vals)
    out = []
    if not tot > 0:
        return f'<text x="{x0}" y="{y + h - 3}" class="muted">no data</text>'
    x = x0
    for i, ((key, label), v) in enumerate(zip(SPECIES, vals)):
        if v <= 0:
            continue
        sw = w * v / tot
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(sw - 2, 0.5):.1f}" height="{h}" rx="2" '
                   f'fill="var(--s{i + 1})"><title>{op} {esc(label)}: {v:g} {unit} '
                   f'({100 * v / tot:.0f}% {basis})</title></rect>')
        x += sw
    return "".join(out)


def overview_svg(d):
    """Rows = tows (ordered by median single-target TS, highest first). Panels with their own axes:
    catch by number, catch by weight, median TS (dB), mean Sv (dB)."""
    row_h, top, left = 22, 46, 118
    bw, gap, dot_w = 210, 26, 150
    xs = [left, left + bw + gap, left + 2 * (bw + gap), left + 2 * (bw + gap) + dot_w + gap]
    width = xs[3] + dot_w + 20
    height = top + row_h * len(d) + 34
    sv_lo = np.floor(d.mean_sv_db.min() / 5) * 5
    sv_hi = np.ceil(d.mean_sv_db.max() / 5) * 5
    if sv_hi - sv_lo < 10:
        sv_hi = sv_lo + 10

    def sx(v, lo, hi, x0):
        return x0 + dot_w * (v - lo) / (hi - lo)

    p = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Catch composition and acoustic '
         f'results for each tow">']
    heads = ["Catch by number", "Catch by weight", "Median TS (dB)", "Mean Sv (dB)"]
    for x, t in zip(xs, heads):
        p.append(f'<text x="{x}" y="16" class="head">{esc(t)}</text>')
    # axes for the dot panels: recessive grid, ticks at the bottom
    for x0, lo, hi, step in ((xs[2], TS_RANGE[0], TS_RANGE[1], 10), (xs[3], sv_lo, sv_hi, 5)):
        for v in np.arange(lo, hi + 0.1, step):
            gx = sx(v, lo, hi, x0)
            p.append(f'<line x1="{gx:.1f}" x2="{gx:.1f}" y1="{top - 8}" y2="{top + row_h * len(d)}" class="grid"/>')
            p.append(f'<text x="{gx:.1f}" y="{top + row_h * len(d) + 16}" class="tick" text-anchor="middle">'
                     f'{v:g}</text>')
    for x0 in xs[:2]:
        for f in (0, 0.5, 1):
            gx = x0 + bw * f
            p.append(f'<text x="{gx:.1f}" y="{top + row_h * len(d) + 16}" class="tick" text-anchor="middle">'
                     f'{f * 100:.0f}%</text>')
    for i, r in d.iterrows():
        y = top + i * row_h
        p.append(f'<a href="#t{r.OP_ID}"><text x="{left - 8}" y="{y + 12}" text-anchor="end" class="lab">'
                 f'{r.OP_ID} ({r.YEAR})</text></a>')
        n = [r[f"n_{k}"] for k, _ in SPECIES]
        w = [r[f"w_{k}"] for k, _ in SPECIES]
        p.append(stacked_bar(xs[0], y + 2, bw, 14, n, r.OP_ID, "by number", "fish"))
        p.append(stacked_bar(xs[1], y + 2, bw, 14, [0 if pd.isna(v) else v for v in w] if not r.w_missing else
                             [0] * 5, r.OP_ID, "by weight", "g"))
        if r.w_missing:
            p.append(f'<text x="{xs[1]}" y="{y + 13}" class="muted">weight missing</text>')
        if not pd.isna(r.st_median_ts_db):
            cx = sx(np.clip(r.st_median_ts_db, *TS_RANGE), *TS_RANGE, xs[2])
            p.append(f'<circle cx="{cx:.1f}" cy="{y + 9}" r="5" class="dot"><title>{r.OP_ID}: median TS '
                     f'{r.st_median_ts_db:.1f} dB, mean {r.st_mean_ts_db:.1f} dB, {int(r.st_n_targets)} targets'
                     f'</title></circle>')
        cx = sx(r.mean_sv_db, sv_lo, sv_hi, xs[3])
        p.append(f'<circle cx="{cx:.1f}" cy="{y + 9}" r="5" class="dot"><title>{r.OP_ID}: mean Sv '
                 f'{r.mean_sv_db:.1f} dB, Nv {fmt(r.nv, 3)}</title></circle>')
    p.append("</svg>")
    return "".join(p)


def legend():
    return '<div class="legend">' + "".join(
        f'<span><i style="background:var(--s{i + 1})"></i>{esc(label)}</span>'
        for i, (_, label) in enumerate(SPECIES)) + "</div>"


def ts_hist_svg(ts, op):
    w, h, l, b, t = 420, 150, 40, 26, 10
    edges = np.arange(TS_RANGE[0], TS_RANGE[1] + 1, 1)
    cnt, _ = np.histogram(ts, edges)
    ymax = max(cnt.max(), 1) if len(cnt) else 1
    bw = (w - l - 10) / len(cnt)
    p = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img" '
         f'aria-label="TS histogram of tow {op}">']
    for f in (0.5, 1):
        gy = t + (h - b - t) * (1 - f)
        p.append(f'<line x1="{l}" x2="{w - 10}" y1="{gy:.1f}" y2="{gy:.1f}" class="grid"/>'
                 f'<text x="{l - 4}" y="{gy + 4:.1f}" class="tick" text-anchor="end">{ymax * f:.0f}</text>')
    for i, c in enumerate(cnt):
        if c == 0:
            continue
        bh = (h - b - t) * c / ymax
        p.append(f'<rect x="{l + i * bw + 1:.1f}" y="{h - b - bh:.1f}" width="{bw - 2:.1f}" height="{bh:.1f}" rx="1.5" '
                 f'class="bar"><title>{edges[i]:g} to {edges[i + 1]:g} dB: {c} targets</title></rect>')
    p.append(f'<line x1="{l}" x2="{w - 10}" y1="{h - b}" y2="{h - b}" class="axis"/>')
    for v in range(TS_RANGE[0], TS_RANGE[1] + 1, 5):
        x = l + (v - TS_RANGE[0]) * bw
        p.append(f'<text x="{x:.1f}" y="{h - b + 14}" class="tick" text-anchor="middle">{v}</text>')
    p.append(f'<text x="{(l + w) / 2:.0f}" y="{h - 1}" class="tick" text-anchor="middle">TS (dB), 1 dB bins</text>')
    p.append("</svg>")
    return "".join(p)


CSS = """
:root{color-scheme:light;--bg:#fcfcfb;--card:#ffffff;--text:#0b0b0b;--text2:#52514e;--muted:#7a7974;--line:#e4e3df;
--grid:#ecebe7;--accent:#2a78d6;--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#1a1a19;--card:#222221;
--text:#ffffff;--text2:#c3c2b7;--muted:#9a998f;--line:#3a3936;--grid:#2e2d2b;--accent:#3987e5;--s1:#3987e5;
--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#1a1a19;--card:#222221;--text:#ffffff;--text2:#c3c2b7;--muted:#9a998f;
--line:#3a3936;--grid:#2e2d2b;--accent:#3987e5;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1060px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:1.6rem;margin:0 0 4px}h2{font-size:1.2rem;margin:40px 0 8px}h3{font-size:1.05rem;margin:0 0 6px}
p{margin:6px 0;color:var(--text2)} a{color:var(--accent)} .scroll svg{display:block;max-width:none}
.note{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin:14px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:16px 0}
.scroll{overflow-x:auto}
table{border-collapse:collapse;font-size:13px;width:100%}
th,td{padding:4px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th{color:var(--text2);font-weight:600} td:first-child,th:first-child{text-align:left}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:var(--text2);margin:6px 0}
.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
svg text{fill:var(--text2);font-size:11px}
svg .head{fill:var(--text);font-size:12px;font-weight:600} svg .lab{fill:var(--accent);font-size:11px}
svg .tick{fill:var(--muted);font-size:10px} svg .muted{fill:var(--muted);font-size:10px}
svg .grid{stroke:var(--grid);stroke-width:1} svg .axis{stroke:var(--muted);stroke-width:1}
svg .dot{fill:var(--accent);stroke:var(--card);stroke-width:2} svg .bar{fill:var(--accent)}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
@media (max-width:760px){.grid2{grid-template-columns:minmax(0,1fr)}}
img{max-width:100%;height:auto;border-radius:6px;border:1px solid var(--line)}
"""


def tow_section(r, ts):
    rows = "".join(
        f'<tr><td><i style="display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;'
        f'background:var(--s{i + 1})"></i>{esc(label)}</td><td>{r[f"n_{k}"]:g}</td>'
        f'<td>{fmt(r[f"w_{k}"], 0)}</td></tr>'
        for i, (k, label) in enumerate(SPECIES))
    img = [f for f in glob.glob(os.path.join(OUT, "img", f"*{r.OP_ID}*.png")) if "tracks_" not in f]
    img_html = (f'<img src="img/{esc(os.path.basename(img[0]))}" alt="Echogram of tow {r.OP_ID}" loading="lazy">'
                if img else '<p>No echogram.</p>')
    return f"""
<section class="card" id="t{r.OP_ID}">
<h3>Tow {r.OP_ID} &middot; {r.YEAR} &middot; {esc(VESSELS.get(int(r.VESSEL), r.VESSEL))} &middot; transect {esc(r.TRANSECT)}</h3>
<p>Start {esc(str(r.datetime).replace("T", " "))} (local), {r.TOW_TIME:g} min; headrope {r.FISHING_DEPTH:g} m below the
surface, bottom {fmt(r.bottom_depth)} m. J by number {r.J_n:.2f}, by weight {fmt(r.J_w, 2)}.
Mean Sv {r.mean_sv_db:.1f} dB, Nv {fmt(r.nv, 3)}, {int(r.st_n_targets)} single targets
(median TS {fmt(r.st_median_ts_db)} dB).</p>
<div class="grid2">
<div><table><tr><th>Species</th><th>Number</th><th>Weight (g)</th></tr>{rows}
<tr><td>Other species</td><td>{r.n_other:g}</td><td></td></tr></table></div>
<div>{ts_hist_svg(ts, r.OP_ID)}</div>
</div>
<p style="margin-top:12px">Fish tracks (Echoview, maximum gap 0): {int(r.fish_tracks)} fish; {r.frac_in_tracks:.0%} of
targets in tracks; median TS per fish {r.ts_per_fish_median:.1f} dB; {int(r.strong_tracks)} fish with mean TS above -35 dB.
Left: targets per detection; middle: per fish (track mean); right: TS within fish.</p>
<img src="img/tracks_{r.OP_ID}.png" alt="Fish-track TS of tow {r.OP_ID}" loading="lazy">
<div style="margin-top:12px">{img_html}</div>
</section>"""


README = """\
Mixed-species tows, Lake Huron: catch and acoustics (preliminary)
================================================================

What this is
  Midwater trawl tows from the Lake Huron acoustic surveys whose catch was MIXED, with the acoustic data from the
  trawled depth band during each tow, to look for patterns in acoustic data that should come from more than one
  species. Open {name}.html (double-click; keep img/ next to it). No internet needed.

Which tows
  Catch of five species: alewife, rainbow smelt, cisco, bloater, emerald shiner (numbers summed over life stages;
  alewife in tows fishing deeper than 40 m counted as 0, since they are caught while the net passes through the
  upper water column). A tow is "mixed" when Pielou's evenness of the five, by number, is at least 0.4 and at least
  30 fish of the five were caught. J = H' / ln(5): 0 = one species, 1 = all five equal; two species 50:50 = 0.43,
  three equal = 0.68.
  {n_mixed} Huron tows (2005-2018) meet this. {n_ok} are in this package: {why_missing}

Acoustics (pydt4, the same processing as the bloater TS study)
  Tow region: the trawl's depth band (headrope to 10 m below it) for the tow's duration. Sv: mean volume
  backscattering strength there (background noise removed; samples below the bottom line excluded). Nv: number of
  fish per acoustic sampling volume (single-target TS can be biased above about 0.04-0.1). Single targets: Great
  Lakes SOP settings, TS -60 to -30 dB. 120 kHz (Sturgeon BioSonics dt4; Baird Simrad).
  Echoview (16.1) EV files built with the bloater study's settings give the same results: Sv within 0.002 dB
  (dt4) and 0.005 dB (Simrad), single targets 12,592 vs 12,593. Fish tracks: Echoview fish tracking on the
  single targets, maximum gap 0 (targets on consecutive pings only), at least 2 targets; one TS per fish
  (track mean) counts fish the way the trawl does, instead of echoes.

Not done yet
  The echograms have not been reviewed: no bad-data regions and no tow start corrections have been applied, so
  results for individual tows may still change.

Files
  {name}.html   overview, table and one section per tow
  img/          echogram of each tow (tow region outlined; single targets as points; bottom line in white),
                and tracks_<tow>.png: TS per detection, per fish and within fish
  tows.csv      one row per tow (catch, J, acoustic results)
"""


def main():
    tl, matches, d, targets = load()
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "img"))
    for op in d.OP_ID:
        for f in glob.glob(os.path.join(ECHO_DIR, f"*{op}*.png")):
            shutil.copy2(f, os.path.join(OUT, "img"))
        shutil.copy2(os.path.join(TRACK_DIR, "figures", f"tow_{op}.png"), os.path.join(OUT, "img", f"tracks_{op}.png"))
    n_mixed = len(tl)
    held = matches[matches.status != "ok"]
    no_cal = n_mixed - len(held) - len(d)
    why = (f"{len(held)} have no usable acoustic file or are on hold (2009 recorded 38 kHz only; five with no file "
           f"covering the tow; two from 2005 waiting for a calibration check) and {no_cal} are from years without a "
           f"Lake Huron calibration yet (Sturgeon 2012, 2013, 2017, 2018).")
    table_rows = "".join(
        f'<tr><td><a href="#t{r.OP_ID}">{r.OP_ID}</a></td><td>{r.YEAR}</td><td>{esc(r.TRANSECT)}</td>'
        f'<td>{r.FISHING_DEPTH:g}</td><td>{int(r.n_tot)}</td><td>{r.J_n:.2f}</td><td>{fmt(r.J_w, 2)}</td>'
        f'<td>{esc(dict(SPECIES).get(r.dom_n, r.dom_n))}</td><td>{fmt(r.mean_sv_db)}</td><td>{fmt(r.nv, 3)}</td>'
        f'<td>{int(r.st_n_targets)}</td><td>{fmt(r.st_median_ts_db)}</td><td>{int(r.fish_tracks)}</td>'
        f'<td>{fmt(r.ts_per_fish_median)}</td></tr>' for r in d.itertuples())
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Mixed Tows Huron</title>
<style>{CSS}</style></head><body><main>
<h1>Mixed-species tows, Lake Huron</h1>
<p>Catch composition and acoustics of {len(d)} midwater trawl tows whose catch was mixed (evenness of five species by
number, J &ge; 0.4, &ge; 30 fish). See README.txt for definitions.</p>
<div class="note"><strong>Preliminary.</strong> The echograms have not been reviewed yet: no bad-data regions or start
corrections are applied. {esc(why)}</div>
<h2>Overview</h2>
<p>One row per tow, ordered by the median TS of its single targets (highest first); TS and Sv are for the trawled depth band during the tow. Hover a segment or dot for
values; click a tow number for its section.</p>
{legend()}
<div class="card scroll">{overview_svg(d)}</div>
<h2>Table</h2>
<div class="card scroll"><table>
<tr><th>Tow</th><th>Year</th><th>Transect</th><th>Headrope (m)</th><th>Fish (5 spp.)</th><th>J number</th>
<th>J weight</th><th>Most by number</th><th>Mean Sv (dB)</th><th>Nv</th><th>Targets</th><th>Median TS (dB)</th>
<th>Fish tracks</th><th>Median TS per fish (dB)</th></tr>
{table_rows}</table></div>
<h2>Tows</h2>
{"".join(tow_section(r, targets[r.OP_ID]) for _, r in d.iterrows())}
</main></body></html>"""
    with open(os.path.join(OUT, f"{NAME}.html"), "w", encoding="utf-8") as f:
        f.write(page)
    d.drop(columns=["acoustic_format"]).to_csv(os.path.join(OUT, "tows.csv"), index=False)
    with open(os.path.join(OUT, "README.txt"), "w", encoding="utf-8") as f:
        f.write(README.format(name=NAME, n_mixed=n_mixed, n_ok=len(d), why_missing=why))
    z = shutil.make_archive(os.path.join(ROOT, "output", "share", NAME), "zip", os.path.dirname(OUT), NAME)
    print(f"{len(d)} tows -> {z} ({os.path.getsize(z) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
