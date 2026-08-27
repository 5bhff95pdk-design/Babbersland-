#!/usr/bin/env python3
"""Carte officielle du Royaume du Babberland (SVG + PNG + atlas HTML).

Statut : proposé, non décrété. Même pipeline que l'arbre (R1.7 / R2.6) :
une source Python, un SVG vectoriel, un PNG déterministe au bit près
(graine 1847, polices DejaVu).
"""
from __future__ import annotations

import html
import os
import sys
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import geographie as geo  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
W, H = geo.CANVAS
rng = Random(1847)


def find_font(filename: str) -> str:
    searched = []
    if os.environ.get("BABBERLAND_FONT_DIR"):
        searched.append(Path(os.environ["BABBERLAND_FONT_DIR"]) / filename)
    local = os.environ.get("LOCALAPPDATA", str(Path.home()))
    searched += [
        Path("/usr/share/fonts/truetype/dejavu") / filename,
        Path("/usr/local/share/fonts") / filename,
        Path.home() / ".fonts" / filename,
        Path("/Library/Fonts") / filename,
        Path("/System/Library/Fonts/Supplemental") / filename,
        Path(local) / "Microsoft/Windows/Fonts" / filename,
        Path("C:/Windows/Fonts") / filename,
    ]
    for candidate in searched:
        if candidate.is_file():
            return str(candidate)
    raise SystemExit(
        f"police {filename} introuvable — installez fonts-dejavu-core "
        "ou indiquez un répertoire via BABBERLAND_FONT_DIR."
    )


# ── Géométrie partagée (nord en haut) ──────────────────────────────────
# Terre d'abord, eau par-dessus : le titre (y < 155) ne doit jamais être noyé.
# Fleuve : bande navigable ouest → est ; fjord au NE ; baie du chanvre à l'ouest.
FLEUVE = (
    "M 90,175 C 220,158 340,200 480,178 C 620,156 760,198 900,176 "
    "C 1040,154 1160,190 1280,168 C 1360,156 1440,148 1510,158 "
    "L 1510,268 C 1400,290 1280,305 1160,292 C 1020,276 880,310 740,292 "
    "C 600,274 460,318 320,300 C 220,288 140,310 90,278 Z"
)
FJORD = (
    "M 1180,168 C 1220,128 1300,118 1400,126 C 1480,134 1510,150 1510,175 "
    "C 1510,235 1460,278 1375,282 C 1275,286 1195,248 1180,210 Z"
)
BAIE = (
    "M 90,250 C 130,285 195,328 275,336 C 350,344 395,312 370,278 "
    "C 348,248 250,232 155,236 C 118,240 95,245 90,250 Z"
)
FORET = (
    "M 180,640 C 260,580 360,600 470,590 C 560,580 620,610 700,600 "
    "C 820,585 940,620 1080,600 C 1220,580 1320,650 1380,720 "
    "C 1450,810 1400,940 1280,970 C 1100,1000 700,1005 420,980 "
    "C 240,955 140,850 180,640 Z"
)
CHANVRE = (
    "M 155,350 C 210,342 270,358 318,390 C 350,418 338,470 285,495 "
    "C 225,522 155,498 140,440 C 128,392 128,362 155,350 Z"
)
ORGE = (
    "M 330,560 C 400,540 490,555 540,590 C 560,620 530,665 470,680 "
    "C 390,700 320,660 330,560 Z"
)
RUISSEAU = "M 760,955 C 750,880 740,800 735,720 C 730,660 728,600 732,530 C 736,470 740,390 736,300"
AQUEDUC_A = "M 728,668 L 732,500"
AQUEDUC_B = "M 742,668 L 746,500"
CHEMIN_PAS = "M 700,790 C 710,720 720,660 728,560 C 730,530 732,510 730,495"
ROUTE_PORT = "M 770,490 C 900,450 1040,380 1180,320 C 1220,300 1250,288 1260,282"
ROUTE_GRASS = "M 690,495 C 540,460 400,400 285,330"


def g(tag: str, attrs: dict[str, object], body: str = "") -> str:
    bits = " ".join(f'{k}="{v}"' for k, v in attrs.items() if v is not None)
    if body:
        return f"<{tag} {bits}>{body}</{tag}>"
    return f"<{tag} {bits}/>"


def layer(since: int, body: str, until: int | None = None) -> str:
    attrs = {"class": "epoch", "data-since": since}
    if until is not None:
        attrs["data-until"] = until
    return g("g", attrs, body)


def build_svg() -> str:
    trees = []
    trng = Random(1847)
    for _ in range(220):
        x = trng.randint(200, 1360)
        y = trng.randint(620, 960)
        # Rejection-ish : rester dans la tache forestière.
        if y < 600 or x < 170 or x > 1400:
            continue
        r = trng.choice((7, 8, 9, 10, 11))
        shade = trng.choice(("#2F5A3C", "#3E6B4A", "#4A7A55", "#356044"))
        trees.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{shade}" opacity=".85"/>'
        )
        trees.append(
            f'<circle cx="{x}" cy="{y - 6}" r="{max(4, r - 3)}" fill="#5A8A64" opacity=".7"/>'
        )

    hemp = []
    hrng = Random(1847)
    for _ in range(80):
        x = hrng.randint(150, 320)
        y = hrng.randint(340, 500)
        hemp.append(
            f'<rect x="{x}" y="{y}" width="2" height="{hrng.randint(8, 16)}" '
            f'fill="#5E7A3A" opacity=".7" rx="1"/>'
        )

    def label(x, y, text, size=15, fill="#3a2109", anchor="middle", italic=False, weight=700):
        style = f"font:{weight} {size}px Georgia,serif"
        if italic:
            style = f"font:italic {size}px Georgia,serif"
        return (
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
            f'style="{style}">{html.escape(text)}</text>'
        )

    svg = f'''\
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Carte du Royaume du Babberland">
  <defs>
    <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#f5e4b8"/><stop offset=".5" stop-color="#fff5d6"/><stop offset="1" stop-color="#dfc27b"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#6e3e09"/><stop offset=".45" stop-color="#ddb95b"/><stop offset="1" stop-color="#7a470b"/>
    </linearGradient>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop stop-color="#6A97B0"/><stop offset="1" stop-color="#3E6E88"/>
    </linearGradient>
    <pattern id="waves" width="28" height="12" patternUnits="userSpaceOnUse">
      <path d="M0 8 Q7 2 14 8 T28 8" fill="none" stroke="#d7ecf4" stroke-width="1.1" opacity=".35"/>
    </pattern>
    <filter id="shadow"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-opacity=".35"/></filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="#512b08"/>
    </marker>
    <style>
      .title{{font:700 34px Georgia,serif;fill:#512b08;letter-spacing:2px}}
      .subtitle{{font:italic 16px Georgia,serif;fill:#76501e}}
      .water{{fill:url(#water)}}
      .land{{fill:#e6d3a4}}
      .forest{{fill:#3E6B4A}}
      .hemp{{fill:#7A9A5C}}
      .orge{{fill:#C4B56A}}
      .city{{fill:#f3e2b4;stroke:#6f430b;stroke-width:2.4}}
      .city-label{{font:700 15px Georgia,serif;fill:#3a2109}}
      .muted{{font:italic 12px Georgia,serif;fill:#70481c}}
      .road{{fill:none;stroke:#a07840;stroke-width:3.2;stroke-linecap:round;stroke-dasharray:9 7}}
      .river{{fill:none;stroke:#4d7e96;stroke-width:5;stroke-linecap:round}}
      .aqueduct{{fill:none;stroke:#2A5A78;stroke-width:3.2;stroke-linecap:round}}
      .aqueduct-beer{{fill:none;stroke:#B78A35;stroke-width:3.2;stroke-linecap:round}}
      .plan{{stroke-dasharray:6 6;opacity:.85}}
      .legend{{font:13px Georgia,serif;fill:#563714}}
      .hot{{cursor:pointer}}
    </style>
  </defs>
  <rect width="{W}" height="{H}" fill="#20180e"/>
  <rect x="28" y="28" width="1544" height="1044" rx="22" fill="url(#gold)" filter="url(#shadow)"/>
  <rect x="55" y="55" width="1490" height="990" rx="12" fill="url(#paper)" stroke="#59320b" stroke-width="5"/>
  <rect x="77" y="77" width="1446" height="946" fill="none" stroke="#b88735" stroke-width="2"/>

  <text x="800" y="118" text-anchor="middle" class="title">ROYAUME DU BABBERLAND</text>
  <text x="800" y="144" text-anchor="middle" class="subtitle">Carte cohérente avec le temps · 1847–2026 · {html.escape(geo.STATUT)}</text>

  <!-- Terre d'abord, eau par-dessus (le titre reste au sec). -->
  <rect class="land" x="90" y="155" width="1420" height="840"/>
  <path class="water" d="{FLEUVE}"/>
  <path class="water" d="{FJORD}"/>
  <path class="water" d="{BAIE}"/>
  <path fill="url(#waves)" d="{FLEUVE}"/>
  <path fill="url(#waves)" d="{FJORD}"/>
  <path class="forest" d="{FORET}" opacity=".92"/>
  {''.join(trees)}
  {layer(1840, f'<path class="orge" d="{ORGE}"/>')}
  {layer(1920, f'<path class="hemp" d="{CHANVRE}"/>' + ''.join(hemp))}
  <path class="river" d="{RUISSEAU}"/>

  <!-- Routes (apparaissent avec les villes qu'elles relient) -->
  {layer(1880, f'<path class="road" d="{CHEMIN_PAS}"/>')}
  {layer(1869, f'<path class="road" d="{ROUTE_PORT}"/>')}
  {layer(1920, f'<path class="road" d="{ROUTE_GRASS}"/>')}

  <!-- Aqueduc : plan 1882, chantier 1892, service 1914 -->
  {layer(1882, f'<path class="aqueduct plan" d="{AQUEDUC_A}"/><path class="aqueduct-beer plan" d="{AQUEDUC_B}"/>', 1892)}
  {layer(1892, f'<path class="aqueduct" stroke-dasharray="10 6" d="{AQUEDUC_A}"/><path class="aqueduct-beer" stroke-dasharray="10 6" d="{AQUEDUC_B}"/>', 1914)}
  {layer(1914, f'<path class="aqueduct" d="{AQUEDUC_A}"/><path class="aqueduct-beer" d="{AQUEDUC_B}"/>'
               + label(790, 620, "Double Aqueduc", 12, "#2A5A78", anchor="start"))}

  <!-- Forêt : sanctuaire -->
  {layer(0, label(700, 930, "Forêt de Plantagenet", 18, "#f5e6bd") + label(700, 950, "sanctuaire de la fondation", 12, "#d9c48a", italic=True))}
  {layer(1847, '<g class="hot" data-id="cabane_1847">'
              '<rect x="672" y="786" width="36" height="24" rx="3" fill="#7a4a1b" stroke="#3a2109"/>'
              '<polygon points="668,786 690,768 714,786" fill="#5c3210"/>'
              + label(690, 830, "Cabane de 1847", 12, "#f5e6bd") + "</g>")}
  {layer(0, '<g class="hot" data-id="chene_hamac">'
            '<circle cx="755" cy="755" r="16" fill="#2d4a28"/>'
            '<circle cx="755" cy="750" r="11" fill="#4a7a45"/>'
            '<line x1="738" y1="758" x2="772" y2="752" stroke="#6b4220" stroke-width="2"/>'
            + label(800, 758, "Chêne du Hamac", 12, anchor="start") + "</g>")}
  {layer(0, '<g class="hot" data-id="grande_digue">'
            '<rect x="705" y="682" width="44" height="10" rx="2" fill="#6b5428" stroke="#3a2109"/>'
            + label(727, 710, "Grande Digue", 11) + "</g>")}
  {layer(0, label(1080, 860, "Trois-Érables", 13, "#f5e6bd") + label(1080, 876, "érablières", 11, "#d9c48a", italic=True))}
  {layer(1840, label(430, 655, "Champs d'orge", 13) + label(430, 671, "famille du Grain", 11, italic=True))}
  {layer(1865, '<g class="hot" data-id="douane">'
               '<rect x="688" y="612" width="24" height="16" fill="#efe0b8" stroke="#6f430b"/>'
               + label(700, 648, "Douane", 11) + "</g>")}

  <!-- Pabst City -->
  {layer(1870, '<g class="hot" data-id="pabst_city" opacity=".9">'
               '<circle cx="730" cy="495" r="28" fill="#efe6c4" stroke="#9d6b26" stroke-dasharray="5 4" stroke-width="2"/>'
               + label(730, 538, "hameau chez Pabst", 12, italic=True) + "</g>", 1880)}
  {layer(1880, '<g class="hot" data-id="pabst_city">'
               '<circle cx="730" cy="495" r="52" fill="#f3e2b4" stroke="#6f430b" stroke-width="2.6"/>'
               '<circle cx="730" cy="495" r="38" fill="none" stroke="#b88735" stroke-width="1"/>'
               + label(730, 430, "PABST CITY", 17) + label(730, 575, "capitale · 3 500 âmes", 12, italic=True) + "</g>")}
  {layer(1892, '<g class="hot" data-id="palais">'
               '<rect x="716" y="462" width="28" height="22" fill="#f7e7b0" stroke="#6f430b"/>'
               '<polygon points="714,462 730,448 746,462" fill="#8a1e24"/>'
               + label(778, 458, "Palais", 12, anchor="start") + "</g>")}
  {layer(1962, '<g class="hot" data-id="piscine">'
               '<rect x="772" y="450" width="34" height="18" rx="6" fill="#7BA3B8" stroke="#2A5A78"/>'
               + label(848, 464, "piscine 1962", 11, anchor="start", italic=True) + "</g>")}
  {layer(1962, '<g class="hot" data-id="monts_froisses">'
               '<polygon points="800,448 808,432 816,448" fill="#8B7355" stroke="#5c4630"/>'
               '<polygon points="812,450 820,434 828,450" fill="#9a8060" stroke="#5c4630"/>'
               + label(848, 444, "Monts Froissés 1,20 m", 12, anchor="start") + "</g>")}
  {layer(1984, '<g class="hot" data-id="repos">'
               '<rect x="714" y="532" width="32" height="14" rx="3" fill="#edf2da" stroke="#718043" stroke-dasharray="3 3"/>'
               + label(730, 560, "station de repos", 11, italic=True) + "</g>", 1986)}
  {layer(1986, '<g class="hot" data-id="mcbabbers">'
               '<rect x="710" y="530" width="40" height="18" rx="3" fill="#8a1e24" stroke="#B78A35" stroke-width="2"/>'
               + label(730, 564, "McBabber's 1986", 12) + "</g>")}

  <!-- Port Babette -->
  {layer(1852, '<g class="hot" data-id="port_babette">'
               '<circle cx="1260" cy="278" r="10" fill="none" stroke="#2A5A78" stroke-dasharray="3 3"/>'
               + label(1260, 302, "« un port, un jour »", 11, italic=True) + "</g>", 1869)}
  {layer(1869, '<g class="hot" data-id="port_babette">'
               '<ellipse cx="1260" cy="278" rx="40" ry="24" fill="#e8d7a8" stroke="#2A5A78" stroke-width="2"/>'
               '<rect x="1232" y="286" width="56" height="7" fill="#6b5428"/>'
               + label(1260, 322, "Port Babette", 15) + "</g>")}
  {layer(1916, '<g class="hot" data-id="phare">'
               '<polygon points="1310,275 1348,228 1380,232 1362,282 1322,288" fill="#e6d3a4" stroke="#c4b07a"/>'
               '<rect x="1336" y="198" width="22" height="50" fill="#f7f1dc" stroke="#6f430b" stroke-width="2"/>'
               '<polygon points="1330,198 1347,174 1364,198" fill="#8a1e24"/>'
               '<circle cx="1347" cy="186" r="5" fill="#B78A35"/>'
               + label(1372, 210, "Phare blanc couronné", 12, anchor="start") + "</g>")}
  {layer(1916, label(1260, 340, "800 âmes · quais &amp; flottille", 12, italic=True))}

  <!-- Grass City -->
  {layer(1920, '<g class="hot" data-id="grass_city">'
               '<ellipse cx="270" cy="318" rx="42" ry="26" fill="#edf2da" stroke="#718043" stroke-width="2.4"/>'
               + label(270, 286, "GRASS CITY", 15) + label(270, 358, "« Pousse » · 1 200 âmes", 12, italic=True) + "</g>")}

  <!-- Hydro labels -->
  {layer(0, label(720, 230, "la grande eau", 16, "#f5e6bd", italic=True), 1847)}
  {layer(1847, label(720, 228, "Fleuve Babber", 17, "#f5e6bd") + label(720, 248, "péniches de curds et de fûts", 12, "#d9c48a", italic=True))}
  {layer(0, label(1360, 148, "Fjord des Fûts", 14, "#f5e6bd") + label(1360, 164, "(nom proposé)", 11, "#d9c48a", italic=True))}
  {layer(1920, label(175, 268, "Baie du Chanvre", 13, "#f5e6bd", italic=True))}
  {layer(0, label(780, 880, "Ruisseau Plantagenet", 12, "#d9c48a", italic=True, anchor="start"))}

  <!-- Rose des vents -->
  <g transform="translate(1455,250)">
    <circle r="28" fill="#fff8df" stroke="#9d6b26" stroke-width="2"/>
    <polygon points="0,-22 5,0 0,8 -5,0" fill="#8a1e24"/>
    <polygon points="0,22 5,0 0,-8 -5,0" fill="#3E6B4A"/>
    <text y="-32" text-anchor="middle" style="font:700 11px Georgia,serif" fill="#512b08">N</text>
  </g>

  <!-- Échelle : 2 km = longueur de l'aqueduc -->
  <g transform="translate(120,980)">
    <text y="-8" class="legend">échelle · 2 km (longueur de l'aqueduc)</text>
    <line x1="0" y1="0" x2="{int(2 * geo.PX_PER_KM)}" y2="0" stroke="#512b08" stroke-width="3"/>
    <line x1="0" y1="-6" x2="0" y2="6" stroke="#512b08" stroke-width="2"/>
    <line x1="{int(geo.PX_PER_KM)}" y1="-4" x2="{int(geo.PX_PER_KM)}" y2="4" stroke="#512b08" stroke-width="2"/>
    <line x1="{int(2 * geo.PX_PER_KM)}" y1="-6" x2="{int(2 * geo.PX_PER_KM)}" y2="6" stroke="#512b08" stroke-width="2"/>
    <text x="0" y="18" class="legend">0</text>
    <text x="{int(geo.PX_PER_KM)}" y="18" text-anchor="middle" class="legend">1</text>
    <text x="{int(2 * geo.PX_PER_KM)}" y="18" text-anchor="middle" class="legend">2 km</text>
  </g>

  <!-- Cartouche -->
  <g transform="translate(980,820)">
    <rect x="0" y="0" width="500" height="175" rx="10" fill="#fff8df" stroke="#9d6b26" stroke-width="2"/>
    <text x="16" y="28" style="font:700 14px Georgia,serif" fill="#512b08">Cinq régions · 2026</text>
    <text x="16" y="50" class="legend">Pabst City — 3 500 âmes (canon)</text>
    <text x="16" y="68" class="legend">Grass City — 1 200 âmes (canon)</text>
    <text x="16" y="86" class="legend">Port Babette — 800 âmes (canon)</text>
    <text x="16" y="104" class="legend">Forêt de Plantagenet — 1 500 âmes (proposé)</text>
    <text x="16" y="122" class="legend">Monts Froissés — 0 âme, 1,20 m, 1962 (jardin du Palais)</text>
    <text x="16" y="148" style="font:italic 12px Georgia,serif" fill="#70481c">Total proposé : 7 000 — un mini-McLouche par âme.</text>
    <text x="16" y="166" style="font:italic 11px Georgia,serif" fill="#9E2B25">Hors canon tant qu'un Avis ne l'aura pas ratifié.</text>
  </g>
</svg>
'''
    return svg


def build_html(svg: str) -> str:
    epochs_js = ",\n".join(
        f'    {{annee:{e["annee"]}, titre:{e["titre"]!r}, canon:{str(e["canon"]).lower()}, fait:{e["fait"]!r}}}'
        for e in geo.EPOCHS
    )
    regions_js = ",\n".join(
        f'    {{id:{r["id"]!r}, nom:{r["nom"]!r}, role:{r["role"]!r}, pop:{r["population"]!r}, '
        f'statut:{r["population_statut"]!r}, depuis:{r["depuis"]!r}, resume:{r["resume"]!r}}}'
        for r in geo.REGIONS
    )
    # The SVG is full document; extract inner for inline embed? Keep as-is inside a wrapper
    # by stripping xml header — our string starts with <svg.
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas temporel · Royaume du Babberland</title>
<style>
  :root{{
    --navy:#132A44; --gold:#B78A35; --cream:#F6EEDB; --ink:#29251F; --muted:#6E624F;
    --green:#3E6B4A; --red:#9E2B25;
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--cream);color:var(--ink);font:15px/1.55 Georgia,"DejaVu Serif",serif}}
  header{{background:var(--navy);color:#fff;padding:28px 24px 20px;border-bottom:5px double var(--gold)}}
  header h1{{margin:0 0 6px;font-size:24px;letter-spacing:.4px}}
  header .sub{{color:#DFCE9F;font-style:italic;font-size:14px}}
  header .meta{{margin-top:10px;font-size:12px;color:#BFD0E2;letter-spacing:.4px}}
  .banner{{background:#FFF6D8;border-bottom:1px solid #E0D4B4;color:var(--muted);
    padding:10px 24px;font-size:13.5px}}
  .banner b{{color:var(--red)}}
  main{{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:0;min-height:calc(100vh - 210px)}}
  .mapwrap{{padding:12px 8px 8px;overflow:auto;background:#2a2116}}
  .mapwrap svg{{width:100%;height:auto;display:block;background:transparent}}
  aside{{background:#fff;border-left:1px solid #E0D4B4;padding:16px 16px 28px;overflow:auto}}
  aside h2{{margin:0 0 8px;font-size:13px;color:var(--navy);letter-spacing:.6px;text-transform:uppercase}}
  .year{{font-size:42px;color:var(--navy);margin:0;line-height:1}}
  .era{{color:var(--gold);font-style:italic;margin:4px 0 14px}}
  .fait{{background:#FFFDF6;border:1px solid #E0D4B4;border-left:4px solid var(--gold);
    padding:10px 12px;font-size:13.5px;margin-bottom:16px}}
  .canon{{display:inline-block;font:10px/1.6 "DejaVu Sans",sans-serif;letter-spacing:.5px;
    padding:1px 7px;border-radius:8px;color:#fff;background:var(--green);vertical-align:2px}}
  .prop{{background:var(--gold)}}
  .kpi{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 16px}}
  .card{{background:var(--cream);border:1px solid #E0D4B4;border-radius:5px;padding:8px 10px}}
  .card .n{{font-size:22px;color:var(--navy)}}
  .card .k{{font-size:11px;color:var(--muted);letter-spacing:.4px;text-transform:uppercase}}
  .reg{{border-top:1px dashed #EADFC4;padding:8px 0;cursor:pointer}}
  .reg:hover{{color:var(--navy)}}
  .reg b{{display:block;font-size:14px}}
  .reg span{{font-size:12.5px;color:var(--muted)}}
  .snaps{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}}
  .snaps button{{font:12px Georgia,serif;background:#fff;border:1px solid #E0D4B4;border-radius:12px;
    padding:3px 9px;cursor:pointer;color:var(--navy)}}
  .snaps button.on{{background:var(--navy);color:var(--cream);border-color:var(--navy)}}
  footer{{background:#fff;border-top:1px solid #E0D4B4;padding:12px 22px 18px}}
  .slide{{display:flex;align-items:center;gap:14px}}
  input[type=range]{{flex:1;accent-color:var(--gold)}}
  .play{{background:var(--navy);color:var(--cream);border:0;border-radius:16px;padding:6px 14px;
    font:13px Georgia,serif;cursor:pointer}}
  @media (max-width: 980px){{
    main{{grid-template-columns:1fr}}
    aside{{border-left:0;border-top:1px solid #E0D4B4}}
  }}
</style>
</head>
<body>
<header>
  <h1>🗺️ Atlas temporel du Royaume du Babberland</h1>
  <div class="sub">Carte cohérente avec le temps · cinq régions, un fleuve, des Alpes de jardin</div>
  <div class="meta">CHANCELLERIE ROYALE · PABST CITY · 27 AOÛT 2026 · TICKET R2.6 LIVRÉ EN PROPOSITION · {html.escape(geo.EDITION)}</div>
</header>
<div class="banner">Statut éditorial — <b>proposé, non décrété</b>. Les cinq régions, les 5 500 âmes urbaines, les Monts Froissés de 1962 et le Fleuve Babber sont canoniques. Le reste (1 500 âmes de la forêt, toponymes du fjord et de la baie, tracé des routes, 2 km d'aqueduc) est reconstruction pour la carte, sans force de loi.</div>
<main>
  <div class="mapwrap" id="map">{svg}</div>
  <aside>
    <h2>Année affichée</h2>
    <p class="year" id="yearlab">2026</p>
    <p class="era" id="eralab">Aujourd'hui</p>
    <div class="fait" id="fait"></div>
    <h2>Population</h2>
    <div class="kpi">
      <div class="card"><div class="k">Total</div><div class="n" id="poptot">7 000</div></div>
      <div class="card"><div class="k">Dont canon</div><div class="n">5 500</div></div>
    </div>
    <p id="popdetail" style="font-size:12.5px;color:var(--muted);margin-top:-6px"></p>
    <h2>Cinq régions</h2>
    <div id="regs"></div>
    <h2 style="margin-top:18px">Aller à</h2>
    <div class="snaps" id="snaps"></div>
  </aside>
</main>
<footer>
  <div class="slide">
    <button class="play" id="play" type="button">▶ Jouer le temps</button>
    <span style="font-size:12px;color:var(--muted);width:42px">1830</span>
    <input type="range" id="slider" min="1830" max="2026" value="2026">
    <span style="font-size:12px;color:var(--muted);width:42px">2026</span>
  </div>
</footer>
<script>
const EPOCHS = [
{epochs_js}
];
const REGIONS = [
{regions_js}
];
const slider = document.getElementById('slider');
const yearlab = document.getElementById('yearlab');
const eralab = document.getElementById('eralab');
const fait = document.getElementById('fait');
const poptot = document.getElementById('poptot');
const popdetail = document.getElementById('popdetail');
const regs = document.getElementById('regs');
const snaps = document.getElementById('snaps');
let timer = null;

function epochAt(y){{
  let cur = EPOCHS[0];
  for (const e of EPOCHS) if (e.annee <= y) cur = e;
  return cur;
}}
function setYear(y){{
  y = +y;
  slider.value = y;
  yearlab.textContent = y;
  const e = epochAt(y);
  eralab.textContent = e.titre;
  fait.innerHTML = (e.canon ? '<span class="canon">CANON</span> ' : '<span class="canon prop">PROPOSÉ</span> ') + e.fait;
  document.querySelectorAll('#map .epoch').forEach(g => {{
    const since = +g.dataset.since;
    const until = g.dataset.until === undefined ? 9999 : +g.dataset.until;
    const on = y >= since && y < until;
    g.style.opacity = on ? '1' : '0';
    g.style.pointerEvents = on ? 'auto' : 'none';
  }});
  if (y < 1850) {{ poptot.textContent = '—'; popdetail.textContent = 'Avant le Dénombrement de la sieste (1850).'; }}
  else if (y < 1880) {{ poptot.textContent = '214'; popdetail.textContent = 'Dénombrement de 1850 (chronique, proposé). Humains, à 14 h.'; }}
  else if (y < 2026) {{ poptot.textContent = '…'; popdetail.textContent = '214 (1850) → 7 000 (2026, proposé). Pas de recensement intermédiaire consigné.'; }}
  else {{ poptot.textContent = '7 000'; popdetail.textContent = '3 500 + 1 200 + 800 (canon) + 1 500 forêt (proposé) + 0 monts = 7 000 mini-McLouches.'; }}
  regs.innerHTML = REGIONS.map(r => {{
    const born = y >= r.depuis;
    const pop = !born ? 'pas encore' : (r.statut === 'canon' ? r.pop.toLocaleString('fr-FR') + ' âmes' : r.pop.toLocaleString('fr-FR') + ' âmes · proposé');
    return '<div class="reg" data-id="'+r.id+'"><b>'+r.nom+'</b><span>'+r.role+' · depuis '+r.depuis+' · '+pop+'</span></div>';
  }}).join('');
  snaps.querySelectorAll('button').forEach(b => b.classList.toggle('on', +b.dataset.y === y));
}}
EPOCHS.forEach(e => {{
  const b = document.createElement('button');
  b.textContent = e.annee;
  b.dataset.y = e.annee;
  b.onclick = () => setYear(e.annee);
  snaps.appendChild(b);
}});
slider.addEventListener('input', () => setYear(slider.value));
document.getElementById('play').onclick = function(){{
  if (timer) {{ clearInterval(timer); timer = null; this.textContent = '▶ Jouer le temps'; return; }}
  this.textContent = '❚❚ Pause';
  if (+slider.value >= 2026) slider.value = 1830;
  timer = setInterval(() => {{
    const y = +slider.value + 1;
    if (y > 2026) {{ clearInterval(timer); timer = null; this.textContent = '▶ Jouer le temps'; setYear(2026); return; }}
    setYear(y);
  }}, 28);
}};
setYear(2026);
</script>
</body>
</html>
'''


def draw_png() -> Image.Image:
    """État 2026, même langage visuel que l'arbre généalogique."""
    im = Image.new("RGB", (W, H), "#20180e")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((28, 28, 1572, 1072), 22, fill="#a87525", outline="#e0bd62", width=8)
    d.rounded_rectangle((55, 55, 1545, 1045), 12, fill="#f5e6bd", outline="#59320b", width=5)
    d.rectangle((77, 77, 1523, 1023), outline="#b88735", width=2)
    prng = Random(1847)
    for _ in range(8000):
        x = prng.randrange(60, 1540)
        y = prng.randrange(60, 1040)
        d.point((x, y), fill=prng.choice(["#ead7a8", "#f8eccb", "#dfc990"]))

    font = find_font("DejaVuSerif.ttf")
    bold = find_font("DejaVuSerif-Bold.ttf")

    def F(size, b=False):
        return ImageFont.truetype(bold if b else font, size)

    def center(text, xy, size=19, color="#3a2109", b=True):
        box = d.textbbox((0, 0), text, font=F(size, b))
        d.text(
            (xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2),
            text, font=F(size, b), fill=color,
        )

    def poly(points, fill, outline=None):
        d.polygon(points, fill=fill, outline=outline)

    center("ROYAUME DU BABBERLAND", (800, 108), 34, "#512b08")
    center("Carte cohérente avec le temps · 1847–2026 · proposée, non décrétée", (800, 140), 16, "#76501e", False)

    # Terre d'abord (sous le titre), eau ensuite.
    d.rectangle((90, 155, 1510, 995), fill="#e6d3a4")
    poly([
        (90, 175), (220, 158), (340, 200), (480, 178), (620, 156), (760, 198),
        (900, 176), (1040, 154), (1160, 190), (1280, 168), (1440, 148), (1510, 158),
        (1510, 268), (1400, 290), (1280, 305), (1160, 292), (1020, 276), (880, 310),
        (740, 292), (600, 274), (460, 318), (320, 300), (140, 310), (90, 278),
    ], "#4d7e96")
    d.ellipse((1188, 122, 1510, 282), fill="#3E6E88")
    d.ellipse((90, 248, 390, 350), fill="#5B8AA3")

    # Forêt
    poly([(180, 640), (360, 600), (560, 580), (700, 600), (940, 620), (1220, 580),
          (1380, 720), (1400, 940), (1280, 970), (700, 1005), (420, 980), (140, 850)],
         "#3E6B4A")
    trng = Random(1847)
    for _ in range(180):
        x, y = trng.randint(220, 1340), trng.randint(640, 960)
        r = trng.choice((6, 7, 8, 9))
        d.ellipse((x - r, y - r, x + r, y + r), fill=trng.choice(["#2F5A3C", "#4A7A55"]))

    # Chanvre / orge
    poly([(155, 350), (318, 390), (338, 470), (225, 522), (140, 440)], "#7A9A5C")
    poly([(330, 560), (540, 590), (530, 665), (390, 700), (330, 560)], "#C4B56A")

    def curve(points, fill, width=4):
        d.line(points, fill=fill, width=width, joint="curve")

    curve([(760, 955), (740, 800), (735, 720), (728, 600), (736, 470), (736, 300)], "#4d7e96", 6)
    curve([(700, 790), (720, 660), (728, 560), (730, 495)], "#a07840", 4)
    curve([(770, 490), (1040, 380), (1260, 282)], "#a07840", 4)
    curve([(690, 495), (400, 400), (285, 330)], "#a07840", 4)
    d.line([(728, 668), (732, 500)], fill="#2A5A78", width=5)
    d.line([(742, 668), (746, 500)], fill="#B78A35", width=5)

    # Villes
    d.ellipse((730 - 52, 495 - 52, 730 + 52, 495 + 52), fill="#f3e2b4", outline="#6f430b", width=3)
    center("PABST CITY", (730, 428), 16)
    d.rectangle((716, 462, 744, 484), fill="#f7e7b0", outline="#6f430b")
    d.polygon([(714, 462), (730, 448), (746, 462)], fill="#8a1e24")
    d.rectangle((772, 450, 806, 468), fill="#7BA3B8", outline="#2A5A78")
    d.polygon([(800, 448), (808, 430), (816, 448)], fill="#8B7355", outline="#5c4630")
    d.polygon([(812, 450), (820, 428), (828, 450)], fill="#9a8060", outline="#5c4630")
    d.rectangle((710, 530, 750, 548), fill="#8a1e24", outline="#B78A35", width=2)
    center("McBabber's", (730, 566), 13, "#3a2109", False)

    d.ellipse((1260 - 40, 278 - 24, 1260 + 40, 278 + 24), fill="#e8d7a8", outline="#2A5A78", width=3)
    d.rectangle((1232, 286, 1288, 293), fill="#6b5428")
    center("Port Babette", (1260, 322), 15)
    d.polygon([(1310, 275), (1348, 228), (1380, 232), (1362, 282), (1322, 288)], fill="#e6d3a4", outline="#c4b07a")
    d.rectangle((1336, 198, 1358, 248), fill="#f7f1dc", outline="#6f430b", width=2)
    d.polygon([(1330, 198), (1347, 174), (1364, 198)], fill="#8a1e24")
    d.ellipse((1342, 180, 1352, 190), fill="#B78A35")
    center("phare", (1347, 258), 12, "#3a2109", False)

    d.ellipse((270 - 42, 318 - 26, 270 + 42, 318 + 26), fill="#edf2da", outline="#718043", width=3)
    center("GRASS CITY", (270, 286), 15)

    d.rectangle((672, 786, 708, 810), fill="#7a4a1b", outline="#3a2109")
    d.polygon([(668, 786), (690, 768), (714, 786)], fill="#5c3210")
    d.ellipse((739, 739, 771, 771), fill="#2d4a28")
    center("Cabane de 1847", (690, 828), 13, "#f5e6bd", False)
    center("Forêt de Plantagenet", (700, 940), 18, "#f5e6bd")
    center("Fleuve Babber", (720, 228), 18, "#f5e6bd")
    center("Fjord des Fûts", (1360, 148), 14, "#f5e6bd", False)
    center("Baie du Chanvre", (175, 268), 13, "#f5e6bd", False)
    center("Trois-Érables", (1080, 860), 14, "#f5e6bd", False)
    center("Double Aqueduc", (820, 620), 12, "#2A5A78", False)
    center("Champs d'orge", (430, 655), 13, "#3a2109", False)
    center("Monts Froissés 1,20 m", (910, 438), 13, "#3a2109", False)

    d.ellipse((1460, 372, 1516, 428), fill="#fff8df", outline="#9d6b26", width=2)
    d.polygon([(1488, 378), (1493, 400), (1488, 408), (1483, 400)], fill="#8a1e24")
    center("N", (1488, 362), 12)

    # Échelle
    x0, y0 = 120, 990
    d.line((x0, y0, x0 + int(2 * geo.PX_PER_KM), y0), fill="#512b08", width=3)
    d.text((x0, y0 - 22), "échelle · 2 km", font=F(13), fill="#563714")
    d.text((x0, y0 + 6), "0", font=F(12), fill="#563714")
    d.text((x0 + int(2 * geo.PX_PER_KM) - 20, y0 + 6), "2 km", font=F(12), fill="#563714")

    # Cartouche
    d.rounded_rectangle((980, 820, 1480, 995), 10, fill="#fff8df", outline="#9d6b26", width=2)
    d.text((996, 834), "Cinq régions · 2026", font=F(15, True), fill="#512b08")
    lines = [
        "Pabst City — 3 500 âmes (canon)",
        "Grass City — 1 200 âmes (canon)",
        "Port Babette — 800 âmes (canon)",
        "Forêt de Plantagenet — 1 500 âmes (proposé)",
        "Monts Froissés — 0 âme · jardin du Palais, 1962",
        "Total proposé : 7 000 = Nuit des Sept Mille",
    ]
    y = 860
    for line in lines:
        d.text((996, y), line, font=F(13), fill="#563714")
        y += 18

    d.text((90, 1015), "Traits pointillés (SVG) : routes au pas  ·  Canal bleu : eau  ·  Canal or : Pabst",
           font=F(14), fill="#563714")
    return im


def main() -> None:
    out_svg = ROOT / "sources" / "carte_royaume.svg"
    out_geo_svg = ROOT / "geographie" / "carte_royaume.svg"
    out_png = ROOT / "geographie" / "carte_royaume.png"
    out_html = ROOT / "geographie" / "index.html"
    svg = build_svg()
    out_svg.write_text(svg, encoding="utf-8")
    out_geo_svg.write_text(svg, encoding="utf-8")
    draw_png().save(out_png, optimize=True)
    out_html.write_text(build_html(svg), encoding="utf-8")
    print(f"SVG  : {out_svg} ({out_svg.stat().st_size} o)")
    print(f"PNG  : {out_png} ({out_png.stat().st_size / 1024:.1f} Kio)")
    print(f"Atlas: {out_html} ({out_html.stat().st_size / 1024:.1f} Kio)")


if __name__ == "__main__":
    main()
