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

Usage :
    python sources/pdf_fingerprint.py            # affiche l'empreinte du PDF publié
    python sources/pdf_fingerprint.py --write    # la grave dans gouvernance/pdf_fingerprint.txt
    python sources/pdf_fingerprint.py --check    # échoue si le PDF publié a dérivé

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

PDF = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
STAMP = ROOT / "gouvernance" / "pdf_fingerprint.txt"


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--write", action="store_true", help="grave l'empreinte de référence")
    parser.add_argument("--check", action="store_true", help="compare le PDF à l'empreinte gravée")
    args = parser.parse_args(argv)

    if not args.pdf.is_file():
        print(f"PDF introuvable : {args.pdf}")
        return 1
    digest, pages, images, placements = fingerprint(args.pdf)

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
        if not drift:
            print(f"PDF à jour : empreinte {digest} ({pages} pages, {images} illustrations, "
                  f"{placements} placements)")
            return 0
        print("PDF publié divergent du contrat gravé :")
        for field, (engraved, actual) in drift.items():
            print(f"- {field} : publié {actual} != gravé {engraved}")
        print("→ régénérer (`make pdf`) puis, si le changement est voulu, `make empreinte` et le consigner à l'Avis.")
        return 1

    print(f"{digest}  {pages} pages  {images} illustrations ({placements} placements)  {args.pdf.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
