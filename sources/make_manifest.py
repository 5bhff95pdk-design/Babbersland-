#!/usr/bin/env python3
"""Génère `gouvernance/MANIFEST.sha256` — le manifeste des livrables canoniques.

R1.3 (constats E-12 et E-13 du rapport RA-2026-II-01 ; dépend de R0.5).

Le dépôt scellait déjà par octets ses corpus *internes* de contrôle :

  - `gouvernance/ARCHIVE.sha256` : les volumes REMPLACÉS (2026-G, 2026-H) ;
  - `gouvernance/ICONOGRAPHIE.sha256` : les 28 masters d'illustration (`images/*.png`) ;
  - `gouvernance/GALERIE.sha256` : les 77 clichés réalistes (`images/realistes/*.png`, R1.9).

Et, pour le PDF 2026-I, la fraîcheur est SÉMANTIQUE (`pdf_fingerprint.txt` +
la section `PDF CANONIQUE` de `ARTIFACT_SIGNATURES.sha256`), pas un haché
d'octets : le volume n'est pas déterministe à l'octet (noms `FormXob.*` de
ReportLab), donc un `sha256` du PDF casserait à chaque régénération légitime
(R1.1, R1.4.g).

Ce manifeste scelle donc ce que **rien** ne scellait par octets : le corpus
canonique **livré** — le texte qui fait foi (2026-I), le registre chronologique,
et la source vectorielle de l'arbre (déterministe, jamais régénérée par la
chaîne). C'est la liste d'intégrité qui accompagne une Release (R1.5) et qui
rend **mécanique** la consigne « toute correction entre par I » (fin de E-13) :
un changement volontaire d'un fichier livré doit être un acte — `make manifest`
— lisible dans l'historique, jamais une retouche en silence.

Génération : `$(PY) sources/make_manifest.py` (acte d'assentiment, à commiter).
Vérification : `$(PY) sources/check_manifest.py --check` (CI, `make controle`).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "gouvernance" / "MANIFEST.sha256"

# Le corpus canonique livré : le texte qui fait foi, le registre chronologique
# et la source vectorielle de l'arbre. Les images (masters, galerie), les
# archives et le PDF ont leur propre contrat — voir le docstring et l'en-tête
# du manifeste. L'Atlas géographique reste « proposé, non décrété » : il n'entre
# pas dans un manifeste de livrables tant qu'un Avis ne l'a pas ratifié (R2.6).
LIVRABLES: list[str] = [
    "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md",
    "CHRONOLOGIE_MAITRESSE_1847_2026.md",
    "sources/arbre_genealogique_complet.svg",
]

HEADER = """# Manifeste des livrables du Royaume du Babberland — liste d'intégrité (R1.3).
# Génération (acte d'assentiment) : python sources/make_manifest.py
# Vérification (CI bloquante)    : python sources/check_manifest.py --check
# ------------------------------------------------------------------------
# Ce manifeste scelle par OCTETS le corpus canonique LIVRÉ : le texte qui fait
# foi (ENCYCLOPEDIE_CONSOLIDEE_2026_I.md), le registre chronologique
# (CHRONOLOGIE_MAITRESSE_1847_2026.md) et la source vectorielle de l'arbre
# (sources/arbre_genealogique_complet.svg), ces trois-là n'ayant aucun scellé
# par octets.
#
# Il ne scelle PAS — délégués à leurs contrats propres :
#   - le PDF 2026-I : octets NON-déterministes (ReportLab), fraîcheur SÉMANTIQUE
#     gouvernée par gouvernance/pdf_fingerprint.txt (la CI compare, jamais ne grave) ;
#   - les 28 masters d'illustration : gouvernance/ICONOGRAPHIE.sha256 ;
#   - les 77 clichés réalistes         : gouvernance/GALERIE.sha256 ;
#   - les archives 2026-G et 2026-H    : gouvernance/ARCHIVE.sha256.
#
# Un changement VOLONTAIRE d'un fichier listé se règle par « make manifest »
# dans le même commit, jamais en silence : sans ce re-grave, la CI est rouge —
# c'est la consigne « toute correction entre par I » rendue mécanique (E-13).
"""


def sha256_of(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main() -> int:
    missing = [p for p in LIVRABLES if not (ROOT / p).is_file()]
    if missing:
        print(f"ÉCHEC : livrable introuvable sur le disque — {missing}")
        return 1

    lines = [HEADER.rstrip() + "\n"]
    for path in LIVRABLES:
        lines.append(f"{sha256_of(path)}  {path}\n")

    MANIFEST.write_text("".join(lines), encoding="utf-8")
    # Le manifeste committé est scellé à son tour, mais par lui-même ? Non :
    # il reste un fichier de scellé à committer, pas un scellé circulaire.
    print(f"manifeste des livrables regreffé — {len(LIVRABLES)} fichiers ({MANIFEST})")
    for path in LIVRABLES:
        print(f"  {sha256_of(path)[:16]}…  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
