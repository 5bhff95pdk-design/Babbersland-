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

Comparaison avec l'échantillonnage de l'Atlas (NEAREST) et le hachage
exact d'une grille unique : ici, nul besoin d'espérer que le bruit
reste sous un seuil — le bruit **connu** est accepté, le reste bloque.

Sous GitHub Actions, `--check` émet la charge produite en **annotation
de check-run** (`::notice` en succès, `::error` détaillée — grille 16×16
complète, sha256 du fichier, version Pillow — en divergence). C'est le
seul canal de retour lisible depuis l'environnement d'agent.

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

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PNG = ROOT / "images" / "arbre_genealogique_complet.png"
STAMP = ROOT / "gouvernance" / "ARTIFACT_SIGNATURES.sha256"

# Seuil de luminance pour l'encre (texte '#3a2109', filets '#59320b' :
# luminances ~35-100 ; le papier '#f5e6bd' est à ~225, les cadres dorés > 120).
SEUIL_ENCRE = 100

VARIANTE_RE = re.compile(r"^arbre_variante_([\w.-]+) = (\S+)$", flags=re.M)
SECTION_RE = re.compile(r"\n?# === ARBRE GÉNÉALOGIQUE ===.*?(?=\n# =|\Z)", re.DOTALL)

TETE_SECTION = """# === ARBRE GÉNÉALOGIQUE ===
# Signé par sources/empreinte_arbre.py — modèle « variantes acceptées ».
# Le PNG est bit-stable par machine mais PAS entre machines (FreeType
# 2.12 vs 2.13 : antialiasing des glyphes). Mesure PR #26 : 3 cellules
# 16x16 sur 256 divergent d'1 niveau entre bac à sable et runner —
# zone qui chevauche la plus petite retouche de contenu (2 cellules).
# On accepte donc EXACTEMENT les rendus observés (ci-dessous), sans
# tolérance chiffrée : toute autre variante est une dérive à trancher.
#   - size/mode : géométrie du canevas (1600x1000, RGB) ;
#   - 16x16box  : moyennage BOX 16x16, canaux quantifiés en 16 niveaux ;
#   - ink       : proportion de pixels sombres (luminance < 100), au millième.
# Nouvelle machine légitime ? Lire l'annotation CI, puis
# `python sources/empreinte_arbre.py --accepter '<charge>' <étiquette>`.
"""


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


def lire_variantes() -> dict[str, str]:
    """Variantes gravées : {étiquette: charge}. Vide si pas de section ARBRE."""
    if not STAMP.is_file():
        return {}
    return {m.group(1): m.group(2)
            for m in VARIANTE_RE.finditer(STAMP.read_text(encoding="utf-8"))}


def tete_de_contrat(variantes: dict[str, str]) -> str:
    """SHA-256 de l'ensemble trié des charges — la valeur à une ligne."""
    return hashlib.sha256("|".join(sorted(variantes.values())).encode()).hexdigest()


def graver(variantes: dict[str, str]) -> None:
    """Réécrit la section ARBRE du scellé, en préservant les autres sections."""
    existing = STAMP.read_text(encoding="utf-8") if STAMP.is_file() else ""
    existing = SECTION_RE.sub("", existing).rstrip() + "\n"
    lignes = [f"arbre_png = {tete_de_contrat(variantes)}"]
    for etiquette in sorted(variantes):
        lignes.append(f"arbre_variante_{etiquette} = {variantes[etiquette]}")
    STAMP.write_text(existing + "\n" + TETE_SECTION + "\n".join(lignes) + "\n",
                     encoding="utf-8")


def _annoter(niveau: str, titre: str, message: str) -> None:
    """Émet une annotation de workflow lisible via l'API Checks.

    Sous GitHub Actions, `::notice`/`::error` deviennent des annotations
    du check-run — le SEUL canal lisible depuis l'environnement d'agent
    (les journaux d'étape transitent par Azure Blob, inaccessible).
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        safe = message.replace("\n", " ").replace("\r", " ")
        print(f"::{niveau} title={titre}::{safe}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true",
                        help="(re)grave la variante courante sous --variante")
    parser.add_argument("--variante", default="reference-locale",
                        help="étiquette de la variante gravée par --write "
                             "(défaut : reference-locale)")
    parser.add_argument("--accepter", nargs=2, metavar=("CHARGE", "ÉTIQUETTE"),
                        help="grave une charge observée ailleurs (ex. annotation CI)")
    parser.add_argument("--check", action="store_true",
                        help="échoue si la variante courante n'est pas gravée")
    args = parser.parse_args(argv)

    courante = variante_courante()
    variantes = lire_variantes()

    if args.write:
        if courante is None:
            print(f"PNG absent ou Pillow manquant : {PNG.relative_to(ROOT)}")
            return 1
        variantes[args.variante] = courante
        graver(variantes)
        print(f"Empreinte Arbre gravée dans {STAMP.relative_to(ROOT)} :")
        print(f"  variante « {args.variante} » = {courante}")
        print(f"  tête de contrat : {tete_de_contrat(variantes)}")
        print(f"  ensemble accepté : {sorted(variantes)}")
        return 0

    if args.accepter:
        charge, etiquette = args.accepter
        if not re.fullmatch(r"size:\d+x\d+\|mode:\w+\|16x16box:[0-9a-f]{32}\|ink:\d+(\.\d+)?",
                            charge):
            print(f"charge invalide : {charge!r}")
            print("forme attendue : size:WxH|mode:RGB|16x16box:<md5>|ink:<p>")
            return 1
        variantes[etiquette] = charge
        graver(variantes)
        connue = ("— c'est la variante courante" if courante == charge
                  else "(différente de la variante courante : normal si "
                       "gravée depuis un autre environnement)")
        print(f"Variante « {etiquette} » acceptée {connue} :")
        print(f"  {charge}")
        print(f"  tête de contrat : {tete_de_contrat(variantes)}")
        print(f"  ensemble accepté : {sorted(variantes)}")
        return 0

    if args.check:
        if courante is None:
            print(f"PNG absent ou Pillow manquant : {PNG.relative_to(ROOT)}")
            return 1
        if not variantes:
            print("aucune variante gravée : "
                  "lancer `python sources/empreinte_arbre.py --write`")
            return 1

        # Trace systématique en CI (notice) : chaque run laisse la charge
        # réellement produite dans une annotation lisible via l'API Checks.
        connues = {v: k for k, v in variantes.items()}
        _annoter("notice", "empreinte-arbre",
                 f"charge={courante} connue={connues.get(courante, 'NON')}")

        if courante in connues:
            print(f"Arbre conforme à la variante « {connues[courante]} » "
                  f"({courante})")
            return 0

        # Divergence : tout imprimer (console ET annotation détaillée) pour
        # qu'un log CI, seul disponible, suffise au diagnostic — douleur
        # historique de R1.4.a-v2, ne pas la reproduire.
        print("Arbre divergent : variante inédite, hors ensemble accepté.")
        print(f"  produite : {courante}")
        print(f"  acceptées :")
        for etiquette in sorted(variantes):
            print(f"    « {etiquette} » = {variantes[etiquette]}")
        if HAS_PIL:
            import PIL
            pillow_ver = PIL.__version__
            print(f"  Pillow : {pillow_ver}")
        else:
            pillow_ver = "absente"
        raw = hashlib.sha256(PNG.read_bytes()).hexdigest()
        print(f"  sha256 du fichier : {raw}")
        grille = grille_quantifiee()
        print(f"  grille 16x16 : {grille}")
        _annoter("error", "empreinte-arbre-divergence",
                 f"charge_inedite={courante} | sha256fichier={raw} | "
                 f"pillow={pillow_ver} | grille={grille} | "
                 f"acceptees={sorted(variantes)} | pour accepter apres revue : "
                 f"python sources/empreinte_arbre.py --accepter '{courante}' "
                 f"<etiquette>")
        print()
        print("Rendu légitime d'un nouvel environnement ? Relire la grille et")
        print("l'encre ci-dessus, puis accepter explicitement la charge dans")
        print("le scellé. Retouche de contenu ? Corriger, puis `make arbre`")
        print("et `make empreinte-arbre`.")
        return 1

    print(f"Arbre :")
    print(f"  variante courante : {courante or 'indisponible'}")
    connues = {v: k for k, v in variantes.items()}
    if courante is not None:
        statut = f"connue (« {connues[courante]} »)" if courante in connues \
                 else "INÉDITE — non gravée"
        print(f"  statut : {statut}")
    print(f"  ensemble accepté ({len(variantes)}) :")
    for etiquette in sorted(variantes):
        print(f"    « {etiquette} » = {variantes[etiquette]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
