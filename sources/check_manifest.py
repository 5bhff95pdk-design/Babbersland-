#!/usr/bin/env python3
"""Vérifie `gouvernance/MANIFEST.sha256` — le manifeste des livrables n'a pas dérivé.

R1.3. Pendant de `make_manifest.py` : celui-ci GRAVE l'acte d'assentiment, celui-ci
le VÉRIFIE (comme `make empreinte`/`--check` ou `sha256sum --check` ailleurs).
La CI ne grave jamais : elle compare. Ici, pas de `--accepter` et pas de variante
d'environnement : le corpus livré est statique (texte + SVG), ses octets n'ont
aucune raison de diverger d'une machine à l'autre — une divergence nomme donc
un changement de CONTENU, à régler par re-grave explicite (E-13).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "gouvernance" / "MANIFEST.sha256"


def entries() -> dict[str, str]:
    """(chemin → haché attendu) depuis le manifeste."""
    out: dict[str, str] = {}
    if not MANIFEST.is_file():
        print(f"ÉCHEC : {MANIFEST} introuvable — lancer « make manifest » puis commiter.")
        sys.exit(1)
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            print(f"ÉCHEC : ligne de manifeste illisible — {line!r}")
            sys.exit(1)
        out[parts[1].strip()] = parts[0]
    return out


def sha256_of(path: str) -> str | None:
    p = ROOT / path
    if not p.is_file():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    expected = entries()
    if not expected:
        print("ÉCHEC : manifeste vide (aucun livrable déclaré).")
        return 1

    errors: list[str] = []
    for path, wanted in expected.items():
        real = sha256_of(path)
        if real is None:
            errors.append(f"livrable listé absent du dépôt : {path}")
        elif real != wanted:
            errors.append(
                f"livrable dérivé de son scellé : {path}\n"
                f"    prévu  {wanted[:16]}…\n"
                f"    réel   {real[:16]}…"
            )

    if errors:
        print("ÉCHEC DE LA VÉRIFICATION DU MANIFESTE DES LIVRABLES")
        for error in errors:
            print(f"- {error}")
        print()
        print("Un changement de contenu du canon se RÈGLE, il ne se subit pas :")
        print("re-graver le manifeste (make manifest) et commiter dans le MÊME commit")
        print("que le changement, selon la consigne « toute correction entre par I » (E-13).")
        return 1

    print(
        f"Manifeste vérifié : {len(expected)} livrables canoniques intacts "
        "(texte 2026-I, chronologie, source vectorielle de l'arbre) — R1.3."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
