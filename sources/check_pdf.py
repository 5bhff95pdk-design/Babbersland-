#!/usr/bin/env python3
"""Vérifie l'artefact final : légendes et illustrations du PDF canonique 2026-I.

Dépendance : pypdf (python -m pip install -r requirements.txt).
Complète sources/check_continuity.py, qui contrôle les sources : ici, on ouvre
le PDF réellement publié et l'on confirme que chaque légende de la table
d'illustrations du générateur y figure, et que **toute** illustration promise par
le canon y est embarquée.

L'autorité est `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`, non le générateur : c'est
l'angle mort qui avait laissé passer E-01 (une ancre périmée) puis E-07 (trois
planches jamais déclarées au générateur, donc jamais attendues par le contrôle).
Le comptage se fait par **haché de flux image**, pas par nom de XObject — les noms
sont attribués par ReportLab et ne reflètent ni les doublons ni les omissions.
"""
import ast
import hashlib
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
CANON = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
GENERATOR = ROOT / "sources" / "generate_encyclopedie_2026_i.py"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("’", "'")
    return re.sub(r"\s+", " ", text)


def expected_from_canon() -> tuple[set[str], list[str]]:
    """Illustrations que le volume doit montrer, et légendes promises par le script."""
    canon = CANON.read_text(encoding="utf-8")
    wanted = set(re.findall(r"`(images/[^`]+)`", canon))
    wanted -= set(re.findall(r"<!--\s*hors-PDF:\s*(images/[^\s]+)", canon))
    captions: list[str] = []
    tree = ast.parse(GENERATOR.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for value in node.values:
            entries = value.elts if isinstance(value, ast.List) else [value]
            for entry in entries:
                if (isinstance(entry, ast.Tuple) and len(entry.elts) >= 2
                        and all(isinstance(e, ast.Constant) and isinstance(e.value, str)
                                for e in entry.elts)
                        and entry.elts[0].value.startswith("images/")):
                    captions.append(entry.elts[1].value)
    return wanted, captions


def embedded_images(reader: PdfReader) -> dict[str, int]:
    """haché de flux image -> nombre d'occurrences, en ignorant les masques."""
    found: dict[str, int] = {}
    for page in reader.pages:
        resources = page.get("/Resources") or {}
        for name in (resources.get("/XObject") or {}):
            obj = resources["/XObject"][name].get_object()
            if obj.get("/Subtype") != "/Image" or obj.get("/SMask") is not None:
                continue
            digest = hashlib.md5(obj.get_data()).hexdigest()
            found[digest] = found.get(digest, 0) + 1
    return found


wanted, captions = expected_from_canon()
reader = PdfReader(str(PDF))
full_text = normalize(" ".join(page.extract_text() or "" for page in reader.pages))
embedded = embedded_images(reader)

errors: list[str] = []
if not captions:
    errors.append("aucune légende attendue : table d'illustrations du générateur introuvable")
if not wanted:
    errors.append("aucune illustration attendue : références `images/…` absentes de 2026-I")

for caption in captions:
    if normalize(caption) not in full_text:
        errors.append(f"légende absente du PDF : {caption!r}")

if len(embedded) != len(wanted):
    errors.append(
        f"illustrations embarquées : {len(embedded)} flux uniques dans le PDF, "
        f"{len(wanted)} promises par 2026-I"
    )

# Un intitulé de renvoi suivi de rien = image perdue à l'impression (constat E-08).
for label in re.findall(r"(?:Portrait|Visuel) officiel\s*:\s*(?![A-ZÀ-Ý«`])", full_text):
    errors.append(f"intitulé de renvoi orphelin dans le PDF : {label.strip()!r}")

# Le chemin d'image ne doit jamais fuiter dans le volume publié.
if "images/" in full_text:
    errors.append("des chemins d'illustrations apparaissent en clair dans le PDF")

if errors:
    print("ÉCHEC DE LA VÉRIFICATION DU PDF 2026-I")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"PDF vérifié : {len(reader.pages)} pages, {len(embedded)} illustrations embarquées "
      f"(promises par 2026-I : {len(wanted)}), {len(captions)} légendes présentes, "
      "aucun renvoi orphelin.")
