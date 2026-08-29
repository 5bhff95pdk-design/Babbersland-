#!/usr/bin/env python3
"""Transformée d'image et lecture des flux embarqués — source unique (constat E-22).

Le générateur n'imprime jamais un PNG : il en dérive un JPEG borné à 1500×900,
qualité 78, progressif. Les contrôles, eux, doivent raisonner sur **ce qui est
embarqué**, sinon ils comparent des comptes au lieu de comparer des contenus.
Ce module tient donc les deux bouts :

* `derive_bytes()` — la transformée, exactement telle que le générateur l'applique ;
* `derive_to_file()` — son écriture en cache dans le répertoire temporaire ;
* `page_image_hashes()` — les hachés md5 de chaque page d'un PDF, hors masques ;
* `normalize()` — la normalisation de texte partagée avec l'empreinte sémantique.

Une seule définition de « illustration embarquée » : le filtre `/SMask` vit ici,
plus dans chaque script (il en existait deux, divergentes, avant RC-2026-III-01).
"""
from __future__ import annotations

import hashlib
import io
import re
import unicodedata
from pathlib import Path

from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]

# Paramètres de dérivation : les déplacer déplace l'empreinte sémantique du volume.
THUMB_MAX = (1500, 900)
JPEG_PARAMS = dict(quality=78, optimize=True, progressive=True)


def derive_bytes(source: Path | str) -> bytes:
    """Octets JPEG du dérivé imprimable d'une illustration, sans écrire de fichier."""
    path = Path(source)
    if not path.is_absolute():
        path = ROOT / path
    with PILImage.open(path) as pic:
        pic = pic.convert("RGB")
        pic.thumbnail(THUMB_MAX, PILImage.Resampling.LANCZOS)
        buf = io.BytesIO()
        pic.save(buf, "JPEG", **JPEG_PARAMS)
    return buf.getvalue()


def derive_md5(relpath: Path | str) -> str:
    """md5 du dérivé — ce que le PDF doit contenir pour cette illustration."""
    return hashlib.md5(derive_bytes(relpath)).hexdigest()


def derived_name(source: Path | str) -> str:
    """Nom de cache du dérivé dans le répertoire temporaire du générateur.

    Les stems sont uniques dans `images/` ; `avoid_collision` garde la main en cas
    de doublon (constat E-22 : deux sources de noms voisins partageaient un cache).
    """
    path = Path(source)
    return f"{path.stem}-{hashlib.md5(str(path.resolve()).encode()).hexdigest()[:8]}.jpg"


def derive_to_file(source: Path | str, tmp: Path) -> Path:
    """Écrit (ou réutilise) le dérivé dans `tmp`, et renvoie son chemin."""
    out = Path(tmp) / derived_name(source)
    if not out.exists():
        out.write_bytes(derive_bytes(source))
    return out


def normalize(text: str) -> str:
    """Même normalisation pour les légendes et pour l'empreinte : NFKC, apostrophes plates, espaces pliés."""
    text = unicodedata.normalize("NFKC", text).replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", text)


def page_image_hashes(reader, skip_masks: bool = True) -> list[list[str]]:
    """Par page, la liste ordonnée des md5 de flux image (masques exclus par défaut)."""
    pages: list[list[str]] = []
    for page in reader.pages:
        resources = page.get("/Resources") or {}
        digests: list[str] = []
        for name in (resources.get("/XObject") or {}):
            obj = resources["/XObject"][name].get_object()
            if obj.get("/Subtype") != "/Image":
                continue
            if skip_masks and obj.get("/SMask") is not None:
                continue
            digests.append(hashlib.md5(obj.get_data()).hexdigest())
        pages.append(digests)
    return pages


def page_texts(reader) -> list[str]:
    return [normalize(page.extract_text() or "") for page in reader.pages]
