#!/usr/bin/env python3
"""Contrôles éditoriaux sans dépendance pour le canon du Babberland."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
SUPPLEMENT = ROOT / "HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md"
CHRONOLOGY = ROOT / "CHRONOLOGIE_MAITRESSE_1847_2026.md"

texts = {p.name: p.read_text(encoding="utf-8") for p in (CANON, SUPPLEMENT, CHRONOLOGY)}
combined = "\n".join(texts.values())
errors: list[str] = []

for phrase in (
    "Babber le Fou à la friteuse",
    "Le nom fut trouvé par la Princesse Ginette",
    "présidée par Irène",
    "Attributs du Prince Héritier",
    "héritier miraculeux",
    "né un soir de fête",
):
    if phrase in combined:
        errors.append(f"formulation obsolète encore présente : {phrase!r}")

required = {
    "prince Louche en 1984": "Le prince Babber le Louche",
    "ratification de Babber II": "Babber II ratifie",
    "commission Colette-Pabst": "présidée par **Colette-Pabst",
    "Fou premier dans la succession": "Babber le Fou reste premier dans l’ordre de succession",
    "Ti-Babber deuxième": "Ti-Babber occupe le second rang",
    "équivalence monétaire": "1 Babber = 24 Babetons",
    "ordinal générationnel": "septième génération dynastique",
}
for label, phrase in required.items():
    if phrase not in texts[CANON.name]:
        errors.append(f"règle absente de 2026-I — {label}: {phrase!r}")

books = re.findall(r"^# LIVRE ([IVX]+) ·", texts[CANON.name], flags=re.MULTILINE)
if books != ["I", "II", "III", "IV", "V", "VI", "VII"]:
    errors.append(f"structure des livres inattendue : {books}")

for filename, text in texts.items():
    for rel in set(re.findall(r"`(images/[^`]+)`", text)):
        if not (ROOT / rel).is_file():
            errors.append(f"illustration absente dans {filename}: {rel}")

for date in ("12 octobre 1847", "15 juillet 1962", "1er avril 1986", "1991–1993", "26 août 2026"):
    if date not in texts[CHRONOLOGY.name]:
        errors.append(f"date maîtresse absente : {date}")
if "2026-I est la référence canonique autonome" not in texts[CHRONOLOGY.name]:
    errors.append("la chronologie ne désigne pas 2026-I comme référence actuelle")

if errors:
    print("ÉCHEC DES CONTRÔLES DE CONTINUITÉ")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Continuité validée : 2026-I, supplément H, chronologie et illustrations concordent.")
