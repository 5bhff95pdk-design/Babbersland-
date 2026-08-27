#!/usr/bin/env python3
"""Vérifie l'artefact final : légendes et illustrations du PDF canonique 2026-I.

Dépendance : pypdf (python -m pip install pypdf).
Complète sources/check_continuity.py, qui contrôle les sources : ici, on ouvre
le PDF réellement publié et l'on confirme que chaque légende de la table
d'illustrations du générateur y figure, et que le nombre d'images embarquées
correspond aux références du générateur (leçon du constat E-01).
"""
import ast
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
GENERATOR = ROOT / "sources" / "generate_encyclopedie_2026_i.py"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("’", "'")
    return re.sub(r"\s+", " ", text)


source = GENERATOR.read_text(encoding="utf-8")
tree = ast.parse(source)
captions: list[str] = []
images: set[str] = set()
for node in ast.walk(tree):
    if not isinstance(node, ast.Dict):
        continue
    for key, value in zip(node.keys, node.values):
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            continue
        if (isinstance(value, ast.Tuple) and len(value.elts) >= 2
                and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in value.elts)
                and value.elts[0].value.startswith("images/")):
            captions.append(value.elts[1].value)
            images.add(value.elts[0].value)
# Autres illustrations hors table (couverture, arbre généalogique du Livre V).
images.update(re.findall(r'"(images/[^"]+)"', source))

reader = PdfReader(str(PDF))
full_text = normalize(" ".join(page.extract_text() or "" for page in reader.pages))
embedded: set[str] = set()
for page in reader.pages:
    resources = page.get("/Resources") or {}
    xobjects = resources.get("/XObject") or {}
    for name in xobjects.keys():
        obj = xobjects[name].get_object()
        if obj.get("/Subtype") == "/Image":
            embedded.add(str(name))

errors: list[str] = []
for caption in captions:
    if normalize(caption) not in full_text:
        errors.append(f"légende absente du PDF : {caption!r}")
if len(embedded) != len(images):
    errors.append(f"images embarquées : {len(embedded)} trouvées, {len(images)} attendues d'après le générateur")
if not captions:
    errors.append("aucune légende attendue : table d'illustrations du générateur introuvable")

if errors:
    print("ÉCHEC DE LA VÉRIFICATION DU PDF 2026-I")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"PDF vérifié : {len(reader.pages)} pages, {len(embedded)} illustrations embarquées "
      f"(attendues : {len(images)}), {len(captions)} légendes présentes.")
