#!/usr/bin/env python3
"""Contrôles éditoriaux sans dépendance pour le canon du Babberland.

Couvre le canon 2026-I, l'archive H, la chronologie maîtresse, les chroniques
et les ancres d'illustrations du générateur PDF (leçon du constat E-01 :
une ancre périmée privait le PDF publié du portrait du Prince Déchiré).
"""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
SUPPLEMENT = ROOT / "HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md"
CHRONOLOGY = ROOT / "CHRONOLOGIE_MAITRESSE_1847_2026.md"
CHRONICLES = sorted((ROOT / "chroniques").glob("*.md"))
GENERATOR = ROOT / "sources" / "generate_encyclopedie_2026_i.py"

texts = {p.name: p.read_text(encoding="utf-8") for p in (CANON, SUPPLEMENT, CHRONOLOGY)}
texts.update({p.name: p.read_text(encoding="utf-8") for p in CHRONICLES})
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
canon_text = texts[CANON.name]
for label, phrase in required.items():
    if phrase not in canon_text:
        errors.append(f"règle absente de 2026-I — {label}: {phrase!r}")

books = re.findall(r"^# LIVRE ([IVX]+) ·", canon_text, flags=re.MULTILINE)
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

# Ancres d'illustrations du générateur PDF : chaque titre d'ancrage doit exister
# tel quel dans 2026-I, faute de quoi l'illustration disparaît silencieusement du PDF.
def illustration_anchors(source: str) -> list[tuple[str, str]]:
    tree = ast.parse(source)
    anchors: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                continue
            if (isinstance(value, ast.Tuple) and value.elts
                    and isinstance(value.elts[0], ast.Constant)
                    and isinstance(value.elts[0].value, str)
                    and value.elts[0].value.startswith("images/")):
                anchors.append((key.value, value.elts[0].value))
    return anchors

try:
    anchors = illustration_anchors(GENERATOR.read_text(encoding="utf-8"))
except SyntaxError as exc:
    anchors, errors = [], errors + [f"générateur PDF illisible : {exc}"]
if not anchors:
    errors.append("aucune table d'illustrations trouvée dans le générateur PDF")
for anchor, rel in anchors:
    if anchor not in canon_text:
        errors.append(f"ancre d'illustration introuvable dans 2026-I : {anchor!r} (image {rel})")
    elif not (ROOT / rel).is_file():
        errors.append(f"illustration absente pour l'ancre {anchor!r} : {rel}")

# Chroniques : hors canon, mais elles doivent déclarer leur statut éditorial
# « proposé, non décrété » et respecter les formulations canoniques ci-dessus.
for path in CHRONICLES:
    text = texts[path.name]
    if "proposés" not in text or "décret" not in text:
        errors.append(f"chronique sans bandeau de statut « proposé, non décrété » : {path.name}")

if errors:
    print("ÉCHEC DES CONTRÔLES DE CONTINUITÉ")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Continuité validée : 2026-I, supplément H, chronologie, chroniques, "
      f"ancres du générateur ({len(anchors)} illustrations) et fichiers d'images concordent.")
