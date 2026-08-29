#!/usr/bin/env python3
"""Vérifie l'artéfact final : le PDF canonique 2026-I montre bien ce que le canon promet.

Dépendance : pypdf (`make env`). Autorité : `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`,
jamais le générateur (leçon de E-07/E-09). Quatre couches, de la plus lâche à la
plus forte — les trois premières validation des *présences*, la quatrième de
l'*affectation*, que rien ne contrôlait avant RC-2026-III-01 (constat E-18) :

1. toute légende de la table d'illustrations figure dans la couche texte ;
2. tout dérivé prévu à partir d'une illustration promise est embarqué, et tout
   flux embarqué est promis (double inclusion par md5, plus de comparaison de comptes) ;
3. aucun intitulé de renvoi orphelin, aucun chemin `images/…` en clair ;
4. **appairement** : la page qui porte la légende d'une planche doit porter le flux
   correspondant à l'illustration promise — deux portraits intervertis sont une faute.

Les masques (`/SMask`) sont exclus par `babberland_images.page_image_hashes`, définition
unique partagée avec l'empreinte sémantique (constat E-22).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

from babberland_images import (  # noqa: E402
    derive_md5, normalize, page_image_hashes, page_texts,
)

PDF = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
CANON = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
GENERATOR = ROOT / "sources" / "generate_encyclopedie_2026_i.py"


def expected_from_canon() -> set[str]:
    """Illustrations que le volume doit montrer : promesses du canon, exemptions retirées."""
    canon = CANON.read_text(encoding="utf-8")
    wanted = set(re.findall(r"`(images/[^`]+)`", canon))
    return wanted - set(re.findall(r"<!--\s*hors-PDF:\s*(images/[^\s]+)", canon))


def placements() -> list[tuple[str, str]]:
    """(illustration, légende) pour chaque insertion déclarée par le générateur."""
    tree = ast.parse(GENERATOR.read_text(encoding="utf-8"))
    out: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for value in node.values:
            for entry in (value.elts if isinstance(value, ast.List) else [value]):
                if (isinstance(entry, ast.Tuple) and len(entry.elts) >= 2
                        and all(isinstance(e, ast.Constant) and isinstance(e.value, str)
                                for e in entry.elts[:2])
                        and entry.elts[0].value.startswith("images/")):
                    out.append((entry.elts[0].value, entry.elts[1].value))
    return out


wanted = expected_from_canon()
placed = placements()
reader = PdfReader(str(PDF))
texts = page_texts(reader)
per_page_hashes = page_image_hashes(reader)
embedded = {digest for hashes in per_page_hashes for digest in hashes}

errors: list[str] = []
if not placed:
    errors.append("aucune insertion déclarée : table d'illustrations du générateur introuvable")
if not wanted:
    errors.append("aucune illustration attendue : références `images/…` absentes de 2026-I")

# 1 · légendes, et 4 · appairement légende ↔ flux, page à page.
paired = 0
for rel, caption in placed:
    cap = normalize(caption)
    with_caption = [i for i, text in enumerate(texts) if cap in text]
    if not with_caption:
        errors.append(f"légende absente du PDF : {caption!r}")
        continue
    if not (ROOT / rel).is_file():
        errors.append(f"illustration déclarée introuvable sur le disque : {rel}")
        continue
    expected = derive_md5(rel)
    with_image = [i for i, hashes in enumerate(per_page_hashes) if expected in hashes]
    if not with_image:
        errors.append(
            f"flux manquant pour l'illustration promise : {rel} "
            f"(aucune page ne porte le dérivé attendu {expected[:12]}…)"
        )
        continue
    if not set(with_caption) & set(with_image):
        errors.append(
            f"illustration mal appariée à sa légende : {rel} est embarquée page(s) "
            f"{[i + 1 for i in with_image]} mais sa légende est page(s) "
            f"{[i + 1 for i in with_caption]} — légende « {caption[:48]}… »"
        )
        continue
    paired += 1

# 2 · double inclusion par contenu : ce que le canon promet est là, et rien d'autre n'y est.
promised_digests: dict[str, str] = {}
for rel in sorted(wanted):
    if not (ROOT / rel).is_file():
        errors.append(f"illustration promise par 2026-I et absente du dépôt : {rel}")
        continue
    promised_digests[derive_md5(rel)] = rel
lost = sorted(rel for rel in promised_digests.values())
missing = [digest for digest in promised_digests if digest not in embedded]
if missing:
    for digest in missing:
        errors.append(f"illustration promise par 2026-I, absente du PDF : {promised_digests[digest]}")
extra = sorted(embedded - set(promised_digests))
if extra:
    errors.append(
        f"{len(extra)} flux embarqué(s) sans promesse du canon "
        f"(illustration non consentie dans le volume de référence) : {extra[:3]}"
    )

# 3 · résidus de mise en page.
full_text = " ".join(texts)
for label in re.findall(r"(?:Portrait|Visuel) officiel\s*:\s*(?![A-ZÀ-Ý«`])", full_text):
    errors.append(f"intitulé de renvoi orphelin dans le PDF : {label.strip()!r}")
if "images/" in full_text:
    errors.append("des chemins d'illustrations apparaissent en clair dans le PDF")

if errors:
    print("ÉCHEC DE LA VÉRIFICATION DU PDF 2026-I")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    f"PDF vérifié : {len(reader.pages)} pages, {len(embedded)} flux embarqués pour "
    f"{len(wanted)} illustrations promises par 2026-I, {len(placed)} légendes attendues "
    f"dont {paired} appariées à leur flux sur la même page, aucun renvoi orphelin, "
    "aucune planche non consentie."
)
