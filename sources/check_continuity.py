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
    """(ancre, chemin) pour chaque illustration déclarée, en table simple ou multiple."""
    tree = ast.parse(source)
    anchors: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                continue
            entries = value.elts if isinstance(value, ast.List) else [value]
            for entry in entries:
                if (isinstance(entry, ast.Tuple) and entry.elts
                        and isinstance(entry.elts[0], ast.Constant)
                        and isinstance(entry.elts[0].value, str)
                        and entry.elts[0].value.startswith("images/")):
                    anchors.append((key.value, entry.elts[0].value))
    return anchors

generator_source = ""
anchors: list[tuple[str, str]] = []
try:
    generator_source = GENERATOR.read_text(encoding="utf-8")
    anchors = illustration_anchors(generator_source)
except (OSError, SyntaxError, ValueError) as exc:
    # La branche d'erreur doit rester lisible : `anchors` reçoit une liste de
    # (ancre, fichier), jamais le tableau des erreurs (sinon: ValueError au unpack,
    # et le diagnostic « générateur illisible » ne monte jamais — RC-2026-III-01).
    errors.append(f"générateur PDF illisible : {type(exc).__name__}: {exc}")
if not anchors and not errors:
    errors.append("aucune table d'illustrations trouvée dans le générateur PDF")
for anchor, rel in anchors:
    if anchor not in canon_text:
        errors.append(f"ancre d'illustration introuvable dans 2026-I : {anchor!r} (image {rel})")
    elif not (ROOT / rel).is_file():
        errors.append(f"illustration absente pour l'ancre {anchor!r} : {rel}")

# Couverture (constat E-07/E-09) : l'autorité est le canon, pas le générateur.
# Toute illustration référencée dans 2026-I doit donc être servie par une insertion
# du script, ou expressément exclue du volume par « <!-- hors-PDF: images/x.png — motif --> ».
served = {rel for _, rel in anchors} | set(re.findall(r'"(images/[^"]+)"', generator_source))
exempted = set(re.findall(r"<!--\s*hors-PDF:\s*(images/[^\s]+)", canon_text))
promised = set(re.findall(r"`(images/[^`]+)`", canon_text))
for rel in sorted(promised):
    if rel not in served and rel not in exempted:
        errors.append(
            f"illustration promise par 2026-I et servie par aucun ancrage du générateur : {rel} "
            "(l'insérer dans IMAGE_AFTER ou l'exclure par un commentaire « hors-PDF: »)"
        )

# Sens inverse (constat E-22) : le générateur n'a pas droit à une planche que le
# canon ne promet pas. Sans cette règle, une insertion de plus restait invisible —
# le contrôle ne comparait que deux *comptes*, égaux par construction.
for rel in sorted(served - promised - exempted):
    errors.append(
        f"illustration insérée au volume sans promesse de 2026-I : {rel} "
        "(la promettre dans le canon, l'exclure, ou retirer l'insertion)"
    )

# Cinq silences sanctifiés (SERMENT_D_IGNORANCE.md §III). Le texte du Serment
# promet que la batterie « rejette toute tentative d'imposer une fixation
# arbitraire » : la voici, sinon la promesse reste de la rhétorique (E-24).
SILENCES = {
    "Babber le Déchiré": r"né(?:e)?\s+(?:le\s+)?(?:en\s+)?\d{4}|\(\s*(?:v\.\s*)?\d{4}[–-]",
    "Roger Bontemps": r"né(?:e)?\s+(?:le\s+)?(?:en\s+)?\d{4}|\(\s*(?:v\.\s*)?\d{4}[–-]",
}
SILENCES_EVENEMENTS = {
    "Transparence brune": r"\b\d{1,2}\s*h\s*\d{2}|\b\d{4}-\d{2}-\d{2}\b",
    "première pierre": r"\b\d{1,2}\s*h\s*\d{2}",
    "Recette (complète|royale|secrète)": r"\d+\s*(?:grammes|cuillères|pincées|ml|g)\b",
}
for figure, pattern in SILENCES.items():
    for line in canon_text.splitlines():
        if figure in line and re.search(pattern, line) and "non consignée" not in line:
            errors.append(
                f"silence sanctifié percé — naissance chiffrée de {figure} : « {line.strip()[:78]}… » "
                "(SERMENT_D_IGNORANCE.md, II.1 et II.2 : ces dates doivent rester tues)"
            )
for subject, pattern in SILENCES_EVENEMENTS.items():
    for line in canon_text.splitlines():
        if re.search(subject, line, flags=re.I) and re.search(pattern, line):
            errors.append(
                f"silence sanctifié percé — fixation arbitraire sur {subject} : « {line.strip()[:78]}… »"
            )

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
