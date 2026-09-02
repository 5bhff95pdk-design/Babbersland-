#!/usr/bin/env python3
"""Empreinte sémantique de l'Arbre généalogique — modèle « variantes acceptées ».

L'Arbre (`images/arbre_genealogique_complet.png`) est régénéré par
`sources/generate_genealogy.py` (Pillow, graine fixée à 1847). Il est
reproductible au bit près **sur une même machine**, mais pas garanti
entre machines : l'antialiasing de FreeType (2.12 sur Debian 12, 2.13
sur Ubuntu 24.04) décale le rendu des glyphes de quelques pixels.

**Mesure** (PR #26, 1ᵉʳ septembre 2026 — premier diagnostic jamais obtenu
grâce aux annotations de check-run, les journaux Azure Blob étant
inaccessibles depuis l'environnement d'agent) : entre la machine de
référence et le runner CI, la grille moyennée 16×16 quantifiée en 16
niveaux ne diverge que sur **3 cellules, chacune d'un seul niveau** —
cellules assises sur une frontière de quantification. Dans le même
temps, la plus petite retouche de contenu (titre d'un nœud gommé) ne
bouge que 2 cellules d'un niveau. **Les deux ensembles se chevauchent :
aucune tolérance chiffrée ne peut distinguer bruit de rendu et retouche.**

On grave donc, au lieu d'une valeur unique, **l'ensemble des variantes
de rendu observées et acceptées** (chaîne « variante » = géométrie +
mode + haché de la grille moyennée + proportion d'encre) :

- la régénération est conforme ssi sa variante est **dans l'ensemble** ;
- toute retouche de contenu (libellé, nœud, couleur, géométrie) produit
  une variante **hors ensemble** → échec, même minuscule ;
- tout nouvel environnement de rendu légitime (autre version de
  FreeType, nouveau runner) produit une variante hors ensemble → échec
  **diagnostiqué** (annotation lisible), puis accepté explicitement par
  `empreinte_arbre.py --accepter '<charge>' <étiquette>` — l'acte
  d'assentiment, tracé dans git. Jamais de bascule silencieuse.

La mécanique (sections du scellé, annotations, cérémonie d'acceptation) est
commune aux artéfacts régénérés depuis R1.4.c : elle vit dans
`sources/sceaux.py`. L'Arbre, premier livré (R1.4.b), en fixe la formule de
charge, gravée une fois pour toutes : `size|mode|16x16box|ink`.

Sous GitHub Actions, `--check` émet la charge produite en **annotation de
check-run** (`::notice` en succès, `::error` détaillée — grille 16×16
complète, sha256 du fichier, version Pillow — en divergence) : c'est le seul
canal de retour lisible depuis l'environnement d'agent.

Lignes du scellé (`gouvernance/ARTIFACT_SIGNATURES.sha256`) :
    arbre_png = <sha256 de l'ensemble trié des variantes>   (tête de contrat)
    arbre_variante_<étiquette> = size:WxH|mode:M|16x16box:<md5>|ink:<p>   (×N)

Usage :
    python sources/empreinte_arbre.py                          # affiche la variante courante
    python sources/empreinte_arbre.py --write [--variante N]   # (re)grave : variante courante sous N
    python sources/empreinte_arbre.py --accepter '<charge>' N  # grave une charge observée (ex. CI)
    python sources/empreinte_arbre.py --check                  # échoue si variante inconnue
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from sceaux import Sceau, sha256  # noqa: E402

PNG = ROOT / "images" / "arbre_genealogique_complet.png"

# Seuil de luminance pour l'encre (texte '#3a2109', filets '#59320b' :
# luminances ~35-100 ; le papier '#f5e6bd' est à ~225, les cadres dorés > 120).
SEUIL_ENCRE = 100

ENTETE = (
    "# Signé par sources/empreinte_arbre.py — modèle « variantes acceptées ».\n"
    "# Le PNG est bit-stable par machine mais PAS entre machines (FreeType\n"
    "# 2.12 vs 2.13 : antialiasing des glyphes). Mesure PR #26 : 3 cellules\n"
    "# 16x16 sur 256 divergent d'1 niveau entre bac à sable et runner —\n"
    "# zone qui chevauche la plus petite retouche de contenu (2 cellules).\n"
    "# On accepte donc EXACTEMENT les rendus observés (ci-dessous), sans\n"
    "# tolérance chiffrée : toute autre variante est une dérive à trancher.\n"
    "#   - size/mode : géométrie du canevas (1600x1000, RGB) ;\n"
    "#   - 16x16box  : moyennage BOX 16x16, canaux quantifiés en 16 niveaux ;\n"
    "#   - ink       : proportion de pixels sombres (luminance < 100), au millième.\n"
    "# Nouvelle machine légitime ? Lire l'annotation CI, puis\n"
    "# `python sources/empreinte_arbre.py --accepter '<charge>' <étiquette>`.\n"
)

MOTIF = r"size:\d+x\d+\|mode:\w+\|16x16box:[0-9a-f]{32}\|ink:\d+(\.\d+)?"


def variante_courante() -> str | None:
    """Chaîne « variante » du PNG présent : géométrie + rendu moyenné + encre.

    - `size`/`mode` : le canevas (1600×1000, RGB) ;
    - `16x16box` : moyennage BOX à 16×16 cellules (~100×62 px chacune),
      canaux quantifiés en 16 niveaux — stable face au bruit de tramage,
      sensible à tout changement de structure, couleur ou volume de texte ;
    - `ink` : proportion de pixels sombres (luminance < seuil), au millième.
    """
    if not HAS_PIL or not PNG.is_file():
        return None
    img = Image.open(PNG).convert("RGB")
    w, h = img.size

    thumb = img.resize((16, 16), Image.BOX)
    quant = [str(v // 16) for v in thumb.tobytes()]  # RVB entrelacés
    layout_md5 = hashlib.md5(",".join(quant).encode()).hexdigest()

    gray = img.convert("L")
    sombres = sum(v < SEUIL_ENCRE for v in gray.tobytes())
    encre_pm = round(sombres / (w * h), 3)

    return f"size:{w}x{h}|mode:{img.mode}|16x16box:{layout_md5}|ink:{encre_pm}"


def grille_quantifiee() -> str:
    """Grille 16×16 quantifiée lisible, pour le diagnostic de divergence.

    Chaque pixel moyenné devient trois nombres (R,G,B en niveaux 0-15) ;
    ~2,3 ko : tient dans une annotation de check GitHub, ce qui rend enfin
    lisible ce que le runner a réellement produit (les journaux d'étape
    transitent par Azure Blob, injoignable depuis l'environnement d'agent).
    """
    if not HAS_PIL or not PNG.is_file():
        return "indisponible"
    img = Image.open(PNG).convert("RGB").resize((16, 16), Image.BOX)
    data = img.tobytes()
    cells = []
    for i in range(0, len(data), 3):
        cells.append(f"{data[i]//16}.{data[i+1]//16}.{data[i+2]//16}")
    return ",".join(cells)


def diagnostic() -> str:
    """Ce que l'annotation d'échec doit dire : fichier, Pillow, grille complète."""
    import PIL
    return (f"sha256fichier={sha256(PNG)} | pillow={PIL.__version__} | "
            f"grille={grille_quantifiee()}")


sceau = Sceau(marqueur="ARBRE GÉNÉALOGIQUE", prefixe="arbre", entete=ENTETE, motif=MOTIF,
              charge=variante_courante, diagnostic=diagnostic, ligne_tete="arbre_png",
              libelle="Arbre")


def main(argv: list[str] | None = None) -> int:
    return sceau.main(sys.argv[1:] if argv is None else argv,
                      descriptif=__doc__.splitlines()[0])


if __name__ == "__main__":
    raise SystemExit(main())
