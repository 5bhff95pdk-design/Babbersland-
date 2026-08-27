#!/usr/bin/env python3
"""Contrôles de cohérence géographique — canon 2026-I contre l'atlas proposé.

Ne décrète rien : il refuse seulement (1) qu'un fait canonique disparaisse
des sources, (2) que l'atlas contredise une date maîtresse, (3) que le
total proposé des 7 000 âmes ne tienne plus.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))
import geographie as geo  # noqa: E402

CANON = (ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md").read_text(encoding="utf-8")
CHRONO = (ROOT / "CHRONOLOGIE_MAITRESSE_1847_2026.md").read_text(encoding="utf-8")
ATLAS = ROOT / "geographie" / "index.html"
SVG = ROOT / "sources" / "carte_royaume.svg"
PNG = ROOT / "geographie" / "carte_royaume.png"

errors: list[str] = []


def must(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


# ── Faits canoniques (Livre I) ─────────────────────────────────────────
for name in (
    "Pabst City",
    "Les Monts Froissés",
    "Port Babette",
    "Grass City",
    "Forêt de Plantagenet",
):
    must(name in CANON, f"région canonique absente de 2026-I : {name}")

must("3 500" in CANON or "3500" in CANON, "population de Pabst City (3 500) absente de 2026-I")
must("800 âmes" in CANON, "population de Port Babette (800 âmes) absente de 2026-I")
must("1 200" in CANON, "population de Grass City (1 200) absente de 2026-I")
must("1,20 m" in CANON or "1,20 m" in CHRONO, "altitude des Monts Froissés (1,20 m) absente")
must("15 juillet 1962" in CHRONO, "date de création des Monts Froissés absente de la chronologie")
must("Fleuve Babber" in CANON, "Fleuve Babber absent de 2026-I")
must("phare blanc couronné" in CANON, "phare de Port Babette absent de 2026-I")
must("la ville honore Babette Ire" in CHRONO or "nommée en l’honneur de Babette Ire" in CANON
     or "nommée en l'honneur de Babette Ire" in CANON,
     "Port Babette n'est plus rattaché à Babette Ire")
must("7 000 mini-McLouches" in CANON or "7 000 mini-McLouches" in CANON.replace("’", "'"),
     "Nuit des Sept Mille absente de 2026-I")

# Les Monts n'existent pas avant 1962 : la chronologie ne doit les nommer
# qu'à partir de cette date (création). Le mot peut apparaître dans le
# résumé d'un personnage né plus tôt (« futur créateur ») — c'est permis.
pre_1962 = CHRONO.split("**15 juillet 1962**")[0]
must(
    "Monts Froissés" not in pre_1962.split("Futur créateur des Monts Froissés")[-1]
    or pre_1962.count("Monts Froissés") <= 2,
    "les Monts Froissés apparaissent trop tôt dans la chronologie",
)

# ── Gazetteer proposé ──────────────────────────────────────────────────
must(geo.POPULATION_URBAINE_CANON == 5500, f"urbain canon ≠ 5 500 : {geo.POPULATION_URBAINE_CANON}")
must(geo.POPULATION_TOTALE_PROPOSEE == 7000, f"total proposé ≠ 7 000 : {geo.POPULATION_TOTALE_PROPOSEE}")
must(
    sum(r["population"] for r in geo.REGIONS) == 7000,
    "somme des cinq régions ≠ 7 000",
)
must(geo.region_by_id("monts_froisses")["depuis"] == 1962, "Monts Froissés : depuis ≠ 1962")
must(geo.region_by_id("monts_froisses")["population"] == 0,
     "Monts Froissés peuplés : ils sont un jardin, pas une commune")
must(geo.region_by_id("pabst_city")["population"] == 3500, "Pabst City ≠ 3 500")
must(geo.region_by_id("grass_city")["population"] == 1200, "Grass City ≠ 1 200")
must(geo.region_by_id("port_babette")["population"] == 800, "Port Babette ≠ 800")

# Un lieu canonique de l'atlas ne peut pas précéder sa première date connue
# d'une manière qui contredise 1962 / 1847 / 1986.
must(geo.visible(geo.region_by_id("monts_froisses"), 1961) is False, "Monts visibles en 1961")
must(geo.visible(geo.region_by_id("monts_froisses"), 1962) is True, "Monts invisibles en 1962")
must(geo.visible({"depuis": 1986}, 1985) is False, "McBabber's visible avant 1986")
must(geo.visible({"depuis": 1847}, 1847) is True, "cabane invisible en 1847")

# ── Artéfacts ──────────────────────────────────────────────────────────
for path in (ATLAS, SVG, PNG):
    must(path.is_file(), f"artéfact manquant : {path.relative_to(ROOT)}")

if SVG.is_file():
    svg = SVG.read_text(encoding="utf-8")
    for name in ("Pabst City", "Port Babette", "Grass City", "Forêt de Plantagenet", "Monts Froissés"):
        must(name in svg, f"toponyme absent de la carte SVG : {name}")
    must("data-since" in svg, "la carte SVG n'a pas de couches temporelles")
    must("proposé" in svg.lower() or "propos" in svg.lower(), "la carte SVG ne déclare pas son statut")

if ATLAS.is_file():
    html = ATLAS.read_text(encoding="utf-8")
    must("proposé, non décrété" in html, "bandeau de statut absent de l'atlas")
    must("Jouer le temps" in html, "l'atlas n'a pas de lecture temporelle")
    must("1847" in html and "1962" in html and "1986" in html, "dates maîtresses absentes de l'atlas")

if errors:
    print("ÉCHEC DES CONTRÔLES GÉOGRAPHIQUES")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    "Géographie validée : 5 régions, 5 500 âmes urbaines, Monts nés en 1962, "
    f"total proposé 7 000, atlas et carte présents ({SVG.name}, {PNG.name})."
)
