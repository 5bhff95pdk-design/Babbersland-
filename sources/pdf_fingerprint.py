#!/usr/bin/env python3
"""Empreinte sémantique du PDF canonique — le contrat de la CI (constat E-10).

Le PDF produit par ReportLab n'est pas reproductible à l'octet : chaque XObject de
formulaire reçoit un nom aléatoire (`FormXob.<md5>`, reportlab/pdfbase/pdfdoc.py),
et `/CreationDate`, `/ModDate`, `/ID` varient à chaque build. Un `git diff` binaire
du PDF est donc impossible, même quand le livre est rigoureusement identique.

On compare plutôt ce que le lecteur voit : nombre de pages, texte normalisé, et
hachés des flux d'images embarqués. Trois builds consécutifs du même source donnent
la même empreinte (mesuré), et n'importe quelle perte d'illustration, de légende ou
de page la modifie.

Usage :
    python sources/pdf_fingerprint.py            # affiche l'empreinte du PDF publié
    python sources/pdf_fingerprint.py --write    # la grave dans gouvernance/pdf_fingerprint.txt
    python sources/pdf_fingerprint.py --check    # échoue si le PDF publié a dérivé
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
STAMP = ROOT / "gouvernance" / "pdf_fingerprint.txt"


def text_of(reader: PdfReader) -> str:
    raw = " ".join((page.extract_text() or "") for page in reader.pages)
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", raw).replace("’", "'"))


def image_streams(reader: PdfReader) -> set[str]:
    digests: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources") or {}
        for name in (resources.get("/XObject") or {}):
            obj = resources["/XObject"][name].get_object()
            if obj.get("/Subtype") == "/Image":
                digests.add(hashlib.md5(obj.get_data()).hexdigest())
    return digests


def fingerprint(pdf: Path) -> tuple[str, int, int]:
    reader = PdfReader(str(pdf))
    streams = sorted(image_streams(reader))
    payload = f"{len(reader.pages)}|{hashlib.md5(text_of(reader).encode()).hexdigest()}|{''.join(streams)}"
    return hashlib.md5(payload.encode()).hexdigest(), len(reader.pages), len(streams)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--write", action="store_true", help="grave l'empreinte de référence")
    parser.add_argument("--check", action="store_true", help="compare le PDF à l'empreinte gravée")
    args = parser.parse_args(argv)

    if not args.pdf.is_file():
        print(f"PDF introuvable : {args.pdf}")
        return 1
    digest, pages, images = fingerprint(args.pdf)

    if args.write:
        STAMP.parent.mkdir(parents=True, exist_ok=True)
        STAMP.write_text(
            "# Empreinte sémantique du PDF canonique — générée par `make empreinte`.\n"
            "# Le PDF n'est pas reproductible à l'octet (noms FormXob de ReportLab) :\n"
            "# c'est cette empreinte, et non le binaire, que la CI compare.\n"
            f"fingerprint = {digest}\npages = {pages}\nimages = {images}\n",
            encoding="utf-8",
        )
        print(f"Empreinte gravée dans {STAMP.relative_to(ROOT)} : {digest}")
        return 0

    if args.check:
        if not STAMP.is_file():
            print(f"aucune empreinte de référence : lancer `make empreinte` (attendu dans {STAMP})")
            return 1
        expected = re.search(r"fingerprint = ([0-9a-f]{32})", STAMP.read_text(encoding="utf-8"))
        if not expected:
            print(f"empreinte de référence illisible dans {STAMP}")
            return 1
        if expected.group(1) != digest:
            print(f"PDF publié divergent du source : {digest} != {expected.group(1)} gravée")
            print("→ régénérer (`make pdf`) puis, si le changement est voulu, `make empreinte`.")
            return 1
        print(f"PDF à jour : empreinte {digest} ({pages} pages, {images} illustrations)")
        return 0

    print(f"{digest}  {pages} pages  {images} illustrations  {args.pdf.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
