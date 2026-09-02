#!/usr/bin/env python3
"""Empreinte sémantique des vignettes WebP du portail (R1.4.d).

Le portail `index.html` sert 83 vignettes dérivées de `images/realistes/*.png` par
`sources/generate_vignettes.py`. Tant que la CI les comparait **octet à octet**
(`git diff --exit-code`), deux défauts cohabitaient :

- une **dérive réelle** passait inaperçue : le `git diff` n'est pas une vérification
  du contenu dérivé, c'est une vérification d'égalité des octets *tels que commités* ;
  si les vignettes commitées sont périmées **et** que le générateur les reproduit
  telles quelles sur la machine de référence, le diff est vide et l'oubli est légal ;
- le moindre changement d'encodeur (libwebp 1.3 ↔ 1.4, `method=6`, drapeaux SIMD)
  aurait rendu la CI rouge pour du bruit — d'où le `continue-on-error` de l'étape.

La charge compare donc le **contenu décodé**, et non le conteneur :

- `nb` / `largeur` : la promesse du diffuseur (83 clichés, 640 px de large) ;
- `grilles` : pour chaque vignette, la grille 8×8 moyennée (BOX) et quantifiée sur
  16 niveaux, identifiée par son nom de fichier ; l'ensemble trié est haché.
  Une vignette périmée, absente, de travers ou recadrée change ce haché ; un
  ré-encodage bit à bit équivalent ne le change pas ;
Le **poids total** du lot (4,6 Mio au Kio) est imprimé au diagnostic mais n'entre **pas**
dans la charge : un encodeur qui change la taille des fichiers sans changer l'image ne doit
pas ouvrir une cérémonie d'acceptation. Ce qui se contracte est ce qui se voit.

Le diagnostic de divergence **imprime les 83 grilles** : c'est peu (≈ 800 octets),
ça tient dans une annotation de check-run, et cela permet de comparer deux
environnements sans accès aux journaux d'étape.

Politique : variantes acceptées, comme R1.4.b (voir `sources/sceaux.py`).

Usage :
    python sources/empreinte_vignettes.py                          # charge courante
    python sources/empreinte_vignettes.py --write [--variante N]    # grave
    python sources/empreinte_vignettes.py --accepter '<charge>' N   # accepte une charge observée
    python sources/empreinte_vignettes.py --check                   # échoue si inédite
    python sources/empreinte_vignettes.py --grilles                 # détail, pour comparer deux machines
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

from sceaux import Sceau, sha256  # noqa: E402
import generate_vignettes as gen  # noqa: E402  (largeur et source : une seule vérité)

VIGNETTES = ROOT / "images" / "vignettes"

ENTETE = (
    "# Signé par sources/empreinte_vignettes.py — modèle « variantes acceptées » (R1.4.d).\n"
    "# Les 83 vignettes WebP sont DÉRIVÉES de images/realistes/*.png : leurs octets\n"
    "# dépendent de libwebp (version, options SIMD), pas du canon. On compare donc le\n"
    "# contenu décodé :\n"
    "#   nb       : le nombre de vignettes (une promesse du diffuseur, pas un comptage)\n"
    "#   largeur  : la largeur de rendu (640 px)\n"
    "#   grilles  : md5 de la liste triée « nom:md5(grille 8x8 BOX quantifiée 16 niveaux) »\n"
    "# Le poids du lot est signalé au diagnostic, jamais contracté : un encodeur qui\n"
    "# change les octets sans changer l'image ne doit pas ouvrir d'acceptation.\n"
    "# Une vignette périmée ou recadrée change `grilles` ; un ré-encodage équivalent\n"
    "# ne le change pas. Nouvelle machine légitime ? Lire l'annotation CI, puis\n"
    "# `python sources/empreinte_vignettes.py --accepter '<charge>' <étiquette>`.\n"
)

MOTIF = r"nb:\d+\|largeur:\d+\|grilles:[0-9a-f]{32}"


def grilles() -> list[str]:
    """Une ligne par vignette : `stem:md5court` de sa grille 8×8 décodée, triées."""
    lignes = []
    for chemin in sorted(VIGNETTES.glob("*.webp")):
        im = Image.open(chemin).convert("RGB").resize((8, 8), Image.BOX)
        md5 = hashlib.md5(bytes(v // 16 for v in im.tobytes())).hexdigest()[:8]
        lignes.append(f"{chemin.stem}:{md5}")
    return lignes


def charge_courante() -> str | None:
    if not VIGNETTES.is_dir():
        return None
    lignes = grilles()
    if not lignes:
        return None
    return (f"nb:{len(lignes)}|largeur:{gen.LARGEUR}"
            f"|grilles:{hashlib.md5(','.join(lignes).encode()).hexdigest()}")


def diagnostic() -> str:
    lignes = grilles()
    fichiers = sorted(VIGNETTES.glob("*.webp")) if VIGNETTES.is_dir() else []
    poids = sum(f.stat().st_size for f in fichiers)
    premier = f"sha256 du 1er fichier={sha256(fichiers[0])[:12]}… ; " if fichiers else ""
    return (f"poids={poids:,} o ({poids // 1024} Kio, non contracté) ; 8×8 BOX ; {premier}"
            f"grilles={'|'.join(lignes)}")


sceau = Sceau(marqueur="VIGNETTES DU PORTAIL", prefixe="vignettes", entete=ENTETE,
              motif=MOTIF, charge=charge_courante, diagnostic=diagnostic,
              ligne_tete="vignettes_lot", libelle="vignettes")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if "--grilles" in argv:
        for ligne in grilles():
            print(f"  {ligne}")
        return 0
    return sceau.main([a for a in argv if a != "--grilles"], descriptif=__doc__.splitlines()[0])


if __name__ == "__main__":
    raise SystemExit(main())
