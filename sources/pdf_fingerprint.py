#!/usr/bin/env python3
"""Empreinte sémantique du PDF canonique — le contrat de la CI (constats E-10, E-18).

Le PDF produit par ReportLab n'est pas reproductible à l'octet : chaque XObject de
formulaire reçoit un nom aléatoire (`FormXob.<md5>`, reportlab/pdfbase/pdfdoc.py),
et `/CreationDate`, `/ModDate`, `/ID` varient à chaque build. Un `git diff` binaire
du PDF est donc impossible, même quand le livre est rigoureusement identique.

On compare donc ce que le lecteur voit, **page par page et dans l'ordre** :
nombre de pages, texte normalisé, et hachés des flux d'images *affectés à leur page*.
L'empreinte était construite jusqu'ici sur un *ensemble* trié de hachés : deux
portraits intervertis laissaient l'ensemble inchangé, donc le volume fautif portait
le sceau du volume juste (constat E-18, RC-2026-III-01). L'ordonnancement par page
ferme cette classe : déplacer, permuter ou dupliquer une planche change l'empreinte.

Deux contrats, un seul verdict (R1.4.g). L'empreinte gravée dans
`gouvernance/pdf_fingerprint.txt` est celle de la **machine de référence** : seul ce
contrat se re-grave, par `make empreinte`. Les autres environnements de rendu
légitimes (le runner CI, plus tard la matrice multi-OS de R1.2) ne doivent pas
rendre la CI rouge pour un décalage de pagination venu d'une police : ils
s'enregistrent comme **variantes acceptées** dans
`gouvernance/ARTIFACT_SIGNATURES.sha256`, section `PDF CANONIQUE`, par
`--accepter` — le même acte d'assentiment tracé qu'en R1.4.b, pour la même raison :
une tolérance non nommée est un angle mort, une tolérance gravée est un choix.

Comme les autres sceaux, `--check` pose une **annotation de check-run** portant la
charge produite : c'est le seul canal lisible depuis l'environnement d'agent (les
journaux d'étape transitent par Azure Blob — douleur R1.4.a-v2).

Usage :
    python sources/pdf_fingerprint.py            # affiche l'empreinte du PDF publié
    python sources/pdf_fingerprint.py --write    # la grave dans gouvernance/pdf_fingerprint.txt
    python sources/pdf_fingerprint.py --check    # échoue si le PDF publié a dérivé
    python sources/pdf_fingerprint.py --accepter '<charge>' <étiquette>  # variante d'environnement

Attention : `--write` est un **acte d'assentiment**, pas une étape de contrôle.
Le graver dans la même commande qui le vérifie rend la vérification infaillible par
construction — voir la leçon E-21 et l'ordre du `Makefile`.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

from babberland_images import normalize, page_image_hashes  # noqa: E402
from sceaux import (annoter, graver_variantes, lire_variantes,  # noqa: E402
                    tete_de_contrat)

PDF = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
STAMP = ROOT / "gouvernance" / "pdf_fingerprint.txt"

# Section des environnements de rendu acceptés (R1.4.g) — distincte du contrat
# canonique ci-dessus : `pdf_fingerprint.txt` reste la seule référence à laquelle
# le volume publié doit conformer ; les variantes n'excusent qu'un rendu.
MARQUEUR_VARIANTES = "PDF CANONIQUE"
PREFIXE_VARIANTES = "pdf"
ENTETE_VARIANTES = (
    "# Signé par sources/pdf_fingerprint.py --accepter — variantes d'environnement (R1.4.g).\n"
    "# Le contrat canonique du volume reste la valeur unique de\n"
    "# gouvernance/pdf_fingerprint.txt (gravée par `make empreinte`). Cette section\n"
    "# n'accepte que des VARIANTES DE RENDU d'un autre environnement (runner CI,\n"
    "# matrice multi-OS R1.2) : la charge compare l'empreinte ordonnée, le nombre de\n"
    "# pages, d'illustrations et de placements. Accepter une variante n'est JAMAIS\n"
    "# excuser une dérive sur la machine de référence : là, on régénère et on re-grave.\n"
)
MOTIF_CHARGE = re.compile(r"fingerprint:[0-9a-f]{32}\|pages:\d+\|images:\d+\|placements:\d+")



def text_of(reader: PdfReader) -> str:
    return normalize(" ".join((page.extract_text() or "") for page in reader.pages))


def layout_of(reader: PdfReader) -> str:
    """Ordonné : `page:flux,flux|page:flux|…`. La permutation de deux planches le modifie."""
    parts = []
    for number, digests in enumerate(page_image_hashes(reader), start=1):
        if digests:
            parts.append(f"{number}:{','.join(sorted(digests))}")
    return "|".join(parts)


def fingerprint(pdf: Path) -> tuple[str, int, int, int]:
    reader = PdfReader(str(pdf))
    layout = layout_of(reader)
    per_page = [d for chunk in layout.split("|") if chunk for d in chunk.split(":", 1)[1].split(",")]
    digest = hashlib.md5(
        f"{len(reader.pages)}|{hashlib.md5(text_of(reader).encode()).hexdigest()}|{layout}".encode()
    ).hexdigest()
    return digest, len(reader.pages), len(set(per_page)), len(per_page)


def charge_de(digest: str, pages: int, images: int, placements: int) -> str:
    return (f"fingerprint:{digest}|pages:{pages}|images:{images}|placements:{placements}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--write", action="store_true", help="grave l'empreinte de référence")
    parser.add_argument("--check", action="store_true", help="compare le PDF à l'empreinte gravée")
    parser.add_argument("--accepter", nargs=2, metavar=("CHARGE", "ÉTIQUETTE"),
                        help="grave une variante d'environnement observée ailleurs (ex. CI)")
    args = parser.parse_args(argv)

    if not args.pdf.is_file():
        print(f"PDF introuvable : {args.pdf}")
        return 1
    digest, pages, images, placements = fingerprint(args.pdf)
    charge = charge_de(digest, pages, images, placements)
    variantes = lire_variantes(MARQUEUR_VARIANTES, PREFIXE_VARIANTES)

    if args.accepter:
        charge_obs, etiquette = args.accepter
        if not MOTIF_CHARGE.fullmatch(charge_obs):
            print(f"charge invalide : {charge_obs!r}")
            print(f"forme attendue : {MOTIF_CHARGE.pattern}")
            return 1
        variantes[etiquette] = charge_obs
        graver_variantes(MARQUEUR_VARIANTES, PREFIXE_VARIANTES, ENTETE_VARIANTES, variantes,
                         ligne_tete="pdf_variantes_acceptees")
        connue = ("— c'est la charge courante" if charge_obs == charge
                  else "(différente de la charge courante : normal si observée ailleurs)")
        print(f"Variante d'environnement « {etiquette} » acceptée {connue} :")
        print(f"  {charge_obs}")
        print(f"  tête de contrat : {tete_de_contrat(variantes)}")
        print(f"  ensemble accepté : {sorted(variantes)}")
        return 0

    if args.write:
        STAMP.parent.mkdir(exist_ok=True)
        STAMP.write_text(
            "# Empreinte sémantique du PDF canonique — générée par `make empreinte`.\n"
            "# Le PDF n'est pas reproductible à l'octet (noms FormXob de ReportLab) :\n"
            "# c'est cette empreinte, et non le binaire, que la CI compare.\n"
            "# Elle est ordonnée page à page (constat E-18) : permuter deux illustrations\n"
            "# la modifie. Graver ici = assumer un changement, pas le contrôler (E-21).\n"
            f"fingerprint = {digest}\npages = {pages}\nimages = {images}\n"
            f"placements = {placements}\n",
            encoding="utf-8",
        )
        print(f"Empreinte gravée dans {STAMP.relative_to(ROOT)} : {digest}")
        return 0

    if args.check:
        if not STAMP.is_file():
            print(f"aucune empreinte de référence : lancer `make empreinte` (attendu dans {STAMP})")
            return 1
        fields = dict(re.findall(r"^(\w+) = (\S+)$", STAMP.read_text(encoding="utf-8"), flags=re.M))
        current = {"fingerprint": digest, "pages": str(pages), "images": str(images),
                   "placements": str(placements)}
        drift = {k: (fields.get(k), v) for k, v in current.items() if k in fields and fields[k] != v}
        connues = {v: k for k, v in variantes.items()}
        if not drift:
            annoter("notice", "empreinte-pdf", f"charge={charge} connue=reference-gravee")
            print(f"PDF à jour : empreinte {digest} ({pages} pages, {images} illustrations, "
                  f"{placements} placements)")
            return 0
        # Pas conforme au contrat de référence : seul un environnement de rendu
        # **déjà accepté** peut légitimer l'écart (R1.4.g). Sinon, c'est bloquant.
        if charge in connues:
            annoter("notice", "empreinte-pdf",
                    f"charge={charge} connue=variante-acceptee:{connues[charge]}")
            print(f"PDF conforme à la variante d'environnement « {connues[charge]} » "
                  f"({digest}) — le contrat de référence, lui, reste {fields.get('fingerprint')}.")
            print("→ ce n'est pas un blanc-seing : la variante a été acceptée sur revue, "
                  "et l'écart doit se résorber par `make pdf` puis `make empreinte`.")
            return 0
        detail = " | ".join(f"{k}={v}" for k, (g, v) in drift.items())
        print("PDF publié divergent du contrat gravé :")
        for field, (engraved, actual) in drift.items():
            print(f"- {field} : publié {actual} != gravé {engraved}")
        print(f"  produite  : {charge}")
        print(f"  acceptées : {sorted(variantes) or 'aucune'}")
        annoter("error", "empreinte-pdf-divergence",
                f"charge_inedite={charge} | {detail} | acceptees={sorted(variantes)} | "
                f"pour accepter après revue : python sources/pdf_fingerprint.py --accepter "
                f"'{charge}' <etiquette>")
        print("→ régénérer (`make pdf`) puis, si le changement est voulu, `make empreinte` et le consigner à l'Avis.")
        print("→ rendu légitime d'un autre environnement ? `--accepter '<charge>' <étiquette>`.")
        return 1

    print(f"{digest}  {pages} pages  {images} illustrations ({placements} placements)  {args.pdf.name}")
    print(f"  charge : {charge}")
    print(f"  variantes acceptées ({len(variantes)}) : {sorted(variantes) or 'aucune'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
