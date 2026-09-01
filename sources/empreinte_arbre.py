#!/usr/bin/env python3
"""Empreinte sémantique de l'Arbre généalogique — analogue à `empreinte_atlas.py`.

L'Arbre (`images/arbre_genealogique_complet.png`) est régénéré par
`sources/generate_genealogy.py` (Pillow, graine fixée à 1847). Il est
reproductible au bit près **en local** (`md5sum` stable), mais l'expérience
de l'Atlas (R1.4.a-v2, runs CI #21/#22) a montré qu'entre la machine de
l'agent et le runner CI, le rendu Pillow peut diverger légèrement
(tramage des polices, compilation des extensions, locale). La cause exacte
n'a jamais pu être isolée (logs Azure Blob inaccessibles).

Conception de l'empreinte — volontairement **plus tolérante** que celle
de l'Atlas :

1. `size` et `mode` : la géométrie du canevas (1600×1000, RGB).
2. `16x16box` : moyennage BOX de l'image à 16×16 cellules (~100×62 px
   chacune), chaque canal **quantifié en 16 niveaux** (valeur // 16).
   Contrairement au NEAREST de l'Atlas (qui prélève UN pixel source et
   peut basculer sur un bord de glyphe), le moyennage absorbe les
   variations de rendu d'antialiasing ; la quantification absorbe les
   écarts de quelques unités RVB. Détecte : déplacement d'un nœud,
   changement de couleur d'une branche, texte long ajouté/retiré.
   Ne détecte pas : retouche de quelques pixels, remplacement d'un
   caractère par un autre de largeur comparable.
3. `ink` : proportion de pixels sombres (luminance < 100 — l'encre du
   texte et des filets), arrondie au millième. Détecte : un libellé
   nettement raccourci ou allongé (changement du volume de texte).

Sous GitHub Actions, `--check` émet en outre la charge produite comme
**annotation du check-run** (`::notice`, et `::error` détaillée — grille
16×16 complète, sha256 du fichier, version Pillow — en cas de
divergence). C'est le seul canal de retour lisible depuis
l'environnement d'agent : les journaux d'étape transitent par Azure
Blob, qui n'y est pas joignable (douleur documentée de R1.4.a-v2).

Ce qui protège le contenu nomme par nomme est ailleurs et le reste :
`canon/personnages.json` + `check_canon.py` (parité des données) et la
revue humaine de `generate_genealogy.py`. R1.7 (source unique de
l'arbre) refera ce partage.

Usage :
    python sources/empreinte_arbre.py            # affiche l'empreinte
    python sources/empreinte_arbre.py --write    # grave dans gouvernance/ARTIFACT_SIGNATURES.sha256
    python sources/empreinte_arbre.py --check    # compare à l'empreinte gravée
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


def grille_quantifiee() -> str:
    """Grille 16×16 quantifiée lisible, pour le diagnostic en cas de divergence.

    Chaque pixel moyenné devient trois nombres (R,G,B en niveaux 0-15),
    séparés par des points ; les cellules par des virgules. ~2,3 ko : tient
    dans une annotation de check GitHub, ce qui permet de lire enfin ce que
    le runner a réellement produit (les logs Azure Blob, eux, sont
    inaccessibles depuis l'environnement d'agent — douleur R1.4.a-v2).
    """
    if not HAS_PIL or not PNG.is_file():
        return "indisponible"
    img = Image.open(PNG).convert("RGB").resize((16, 16), Image.BOX)
    data = img.tobytes()
    cells = []
    for i in range(0, len(data), 3):
        cells.append(f"{data[i]//16}.{data[i+1]//16}.{data[i+2]//16}")
    return ",".join(cells)


def _annoter(niveau: str, titre: str, message: str) -> None:
    """Émet une annotation de workflow lisible via l'API Checks.

    Sous GitHub Actions, `::notice`/`::error` deviennent des annotations
    du check-run — le SEUL canal lisible depuis l'environnement d'agent
    (les journaux d'étape transitent par Azure Blob, inaccessible).
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        safe = message.replace("\n", " ").replace("\r", " ")
        print(f"::{niveau} title={titre}::{safe}")


def arbre_semantic() -> tuple[str, str]:
    """Calcule l'empreinte sémantique du PNG de l'Arbre.

    Retourne (haché sha256, charge lisible) — la charge sert au diagnostic
    en cas de divergence (douleur identifiée à R1.4.a-v2 : sans elle, la
    cause d'un échec CI est ininvestigable depuis l'environnement d'agent).
    """
    if not HAS_PIL:
        return "no-pil", "PIL non disponible"
    if not PNG.is_file():
        return "missing", f"fichier absent : {PNG.relative_to(ROOT)}"

    img = Image.open(PNG).convert("RGB")
    w, h = img.size

    # 1) Géométrie moyennée 16×16, canaux quantifiés en 16 niveaux.
    #    Image.BOX = moyenne de chaque cellule : stable face aux bords
    #    de glyphes et au tramage qui bougent d'un pixel entre builds.
    thumb = img.resize((16, 16), Image.BOX)
    quant = [str(v // 16) for v in thumb.tobytes()]  # RVB entrelacés
    layout_md5 = hashlib.md5(",".join(quant).encode()).hexdigest()

    # 2) Proportion d'encre (luminance < seuil), au millième.
    gray = img.convert("L")
    sombres = sum(v < SEUIL_ENCRE for v in gray.tobytes())
    encre_pm = round(sombres / (w * h), 3)

    payload = f"size:{w}x{h}|mode:{img.mode}|16x16box:{layout_md5}|ink:{encre_pm}"
    return hashlib.sha256(payload.encode()).hexdigest(), payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="grave l'empreinte de référence")
    parser.add_argument("--check", action="store_true", help="compare à l'empreinte gravée")
    args = parser.parse_args(argv)

    arbre_hash, arbre_payload = arbre_semantic()

    if args.write:
        STAMP.parent.mkdir(exist_ok=True)
        # On préserve le contenu existant (section Atlas notamment) et on
        # remplace uniquement notre section.
        existing = STAMP.read_text(encoding="utf-8") if STAMP.is_file() else ""
        section_re = re.compile(
            r"\n?# === ARBRE GÉNÉALOGIQUE ===.*?(?=\n# =|\Z)", re.DOTALL
        )
        existing = section_re.sub("", existing).rstrip() + "\n"
        new_section = (
            "\n# === ARBRE GÉNÉALOGIQUE ===\n"
            "# Signé par sources/empreinte_arbre.py (analogue à empreinte_atlas.py).\n"
            "# Le PNG est bit-stable en local mais peut diverger entre machines\n"
            "# (rendu Pillow/polices — douleur R1.4.a-v2 de l'Atlas). On compare\n"
            "# donc son contenu sémantique, pas ses octets :\n"
            "# - size/mode : géométrie du canevas (1600x1000, RGB) ;\n"
            "# - 16x16box  : moyennage BOX 16x16, canaux quantifiés en 16 niveaux\n"
            "#   (tolère antialiasing et tramage, détecte structures et couleurs) ;\n"
            "# - ink       : proportion de pixels sombres au millième\n"
            "#   (détecte un libellé nettement raccourci ou allongé).\n"
            f"arbre_png = {arbre_hash}\n"
        )
        STAMP.write_text(existing + new_section, encoding="utf-8")
        print(f"Empreinte Arbre gravée dans {STAMP.relative_to(ROOT)} :")
        print(f"  PNG : {arbre_hash}")
        return 0

    if args.check:
        if not STAMP.is_file():
            print("aucune empreinte de référence : "
                  "lancer `python sources/empreinte_arbre.py --write`")
            return 1
        text = STAMP.read_text(encoding="utf-8")
        m = re.search(r"^arbre_png = (\S+)$", text, flags=re.M)
        if not m:
            print("section ARBRE absente du scellé : "
                  "lancer `python sources/empreinte_arbre.py --write`")
            return 1
        engraved = m.group(1)

        # Trace systématique en CI (notice) : chaque run laisse la charge
        # réellement produite par le runner dans une annotation lisible via
        # l'API Checks — avant même toute divergence.
        _annoter("notice", "empreinte-arbre",
                 f"charge={arbre_payload} sha256={arbre_hash}")

        if engraved == arbre_hash:
            print(f"Arbre à jour : PNG={arbre_hash[:8]}… ({arbre_payload})")
            return 0
        # Divergence : imprimer TOUT ce qui permet de diagnostiquer depuis
        # un log CI (R1.4.a-v2 n'a jamais pu identifier la cause faute de
        # données ; on ne reproduit pas cette erreur).
        print("Arbre divergent du contrat gravé :")
        print(f"  généré : {arbre_hash}")
        print(f"  gravé  : {engraved}")
        print()
        print(f"  charge générée : {arbre_payload}")
        if HAS_PIL:
            import PIL
            pillow_ver = PIL.__version__
            print(f"  Pillow : {pillow_ver}")
        else:
            pillow_ver = "absente"
        if PNG.is_file():
            raw = hashlib.sha256(PNG.read_bytes()).hexdigest()
            print(f"  sha256 du fichier : {raw}")
        else:
            raw = "absent"
        grille = grille_quantifiee()
        print(f"  grille 16x16 : {grille}")
        _annoter("error", "empreinte-arbre-divergence",
                 f"grave={engraved} != genere={arbre_hash} | "
                 f"charge={arbre_payload} | sha256fichier={raw} | "
                 f"pillow={pillow_ver} | grille={grille}")
        print()
        print("Si l'écart est un bruit de rendu CI (et NON un vrai changement),")
        print("le diagnostic ci-dessus doit le montrer : comparer la charge au")
        print("scellé attendu. Ne graver à nouveau qu'après avoir tranché.")
        return 1

    print("Arbre :")
    print(f"  PNG : {arbre_hash}")
    print(f"  charge : {arbre_payload}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
