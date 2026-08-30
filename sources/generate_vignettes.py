#!/usr/bin/env python3
"""Vignettes du portail — le poids de la diffusion, sans toucher aux maîtres.

Le portail `index.html` montrait seize planches de ~2,9 Mio chacune : **44 Mio**
pour une seule page, sur des images affichées à 350 px de large. Ce générateur
en dérive des vignettes WebP de 640 px (~45 Kio pièce) ; les maîtres PNG ne sont
pas touchés, donc les scellés d'iconographie restent intacts.

Déterministe : mêmes octets d'entrée, mêmes octets de sortie — la CI peut donc
vérifier que les vignettes sont à jour par `git diff --exit-code`.

Dépendance : pillow (`make env`). Usage :
    python sources/generate_vignettes.py
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "images" / "realistes"
DEST = ROOT / "images" / "vignettes"
LARGEUR = 640
QUALITE = 82


def vignette(chemin: Path) -> Path:
    im = Image.open(chemin)
    im.load()
    rgb = im.convert("RGB")
    ratio = LARGEUR / rgb.width
    redim = rgb.resize((LARGEUR, round(rgb.height * ratio)), Image.LANCZOS)
    sortie = DEST / (chemin.stem + ".webp")
    redim.save(sortie, "WEBP", quality=QUALITE, method=6, exact=False)
    return sortie


def main() -> int:
    if not SOURCE.is_dir():
        sys.exit(f"sources absentes : {SOURCE}")
    DEST.mkdir(parents=True, exist_ok=True)
    total_entree = total_sortie = 0
    for chemin in sorted(SOURCE.glob("*.png")):
        entree = chemin.stat().st_size
        sortie = vignette(chemin)
        poids = sortie.stat().st_size
        total_entree += entree
        total_sortie += poids
        print(f"{sortie.relative_to(ROOT)} : {entree / 1024:6.0f} Kio → {poids / 1024:5.1f} Kio")
    # empreinte de contrôle : deux exécutions doivent la donner identique
    h = hashlib.sha256(b"".join((DEST / p.name).read_bytes()
                                for p in sorted(DEST.glob("*.webp")))).hexdigest()[:12]
    print(f"{len(list(DEST.glob('*.webp')))} vignettes · "
          f"{total_entree / 1e6:.1f} Mio → {total_sortie / 1e6:.2f} Mio · empreinte {h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
