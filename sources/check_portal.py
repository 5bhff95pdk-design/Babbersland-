#!/usr/bin/env python3
"""Parité du portail racine : `index.html` contre `canon/personnages.json`.

Constat C1 (note d'audit du 30 août 2026) : `gouvernance/index.html` et
`geographie/index.html` sont contrôlés par la chaîne, mais le portail racine
`index.html` ne l'était pas — son « Dictionnaire des 18 Personnages » portait
quatre dates contradictoires avec le canon (Babette Ire 1805, Hortense 1845–1930,
Babette-Marine 1840, Irène 1880). Le canon, seul à faire foi, vit dans
`canon/personnages.json` (déjà la liste d'autorité de R2.9).

Principe : chaque fiche du portail doit correspondre **à exactement une** fiche du
canon (parité, bijection) et porter les **mêmes années** de vie — peu importe la
rédaction (« né le 15 juillet 1962 » ≡ « né 1962 », « Babber le Dormeur » ≡
« Babber Ier le Dormeur »). Deux comparaisons suffisent :

A. couverture — 18 fiches portail ↔ 18 fiches canon, sans doublon ni orphelin ;
B. dates — les années extraites de la fiche portail égalent celles du canon.

Une fiche sans année (Babber le Déchiré, « collatéral ») doit en rester dépourvue.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CANON = ROOT / "canon" / "personnages.json"

# Même famille de normalisation que check_canon.py : on compare des *clefs*, pas
# des textes — « Reine Linéa de Grass City » ≡ « Linéa de Grass City ».
HONORIFIQUES = re.compile(
    r"^(?:S\.M\.|S\.A\.R\.|Sa Majest[ée]|Son Altesse Royale|Le Roi|La Reine|"
    r"Reine|Roi|Prince|Princesse|King|Queen)\s+", re.I)
ORDINAUX = re.compile(r"\b(?:Ier|II|III|VII|IV|V|VI)\b", re.I)
ANNEE = re.compile(r"(?<!\d)(1[6-9]\d{2}|20[0-2]\d)(?!\d)")


def norm_texte(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))  # retire les accents
    s = s.replace("’", "'").replace("«", "").replace("»", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def clef(nom: str) -> str:
    """Clef canonique d'un nom : sans honneur, sans ordinal, sans parenthèse."""
    n = HONORIFIQUES.sub("", nom)
    n = re.sub(r"\(.*?\)", "", n)          # « (Babber VII l'Éveillé) » disparaît
    n = ORDINAUX.sub(" ", n)               # « Ier », « II »… ne comptent pas
    n = n.replace("-", " ")
    return norm_texte(n)


def annees(dates: str) -> set[str]:
    return set(ANNEE.findall(dates or ""))


def extraire_portail() -> list[tuple[str, str]]:
    """(nom, dates) de chaque fiche du dictionnaire du portail."""
    text = INDEX.read_text(encoding="utf-8")
    bloc = text.split("const characters = [", 1)[1].split("];", 1)[0]
    pat = re.compile(r"name: \"([^\"]+)\",\s*dates: \"([^\"]+)\"")
    return [(m.group(1), m.group(2)) for m in pat.finditer(bloc)]


def extraire_canon() -> list[dict]:
    doc = json.loads(CANON.read_text(encoding="utf-8"))
    return doc["persons"] if "persons" in doc else doc["personnages"]


def matcher(cible: str, candidats: list[str]) -> list[str]:
    """Toutes les clefs canon qui correspondent à la clef du portail."""
    if cible in candidats:
        return [cible]
    # inclusion (préfixe/suffixe) : « ginette » ≡ « ginette de port babette »,
    # « ti-babber babber » ≡ « ti-babber babber eveille »
    return [k for k in candidats if cible in k or k in cible]


def main(argv: list[str] | None = None) -> int:
    portail = extraire_portail()
    canon = extraire_canon()
    errors: list[str] = []

    # A · couverture : 18 ↔ 18, bijection (une fiche portail = une fiche canon).
    clefs_canon = [clef(p["nom"]) for p in canon]
    if len(clefs_canon) != len(set(clefs_canon)):
        errors.append(f"personnages.json : {len(clefs_canon) - len(set(clefs_canon))} clef(s) canon dupliquée(s)")
    if len(portail) != len(canon):
        errors.append(f"index.html : {len(portail)} fiches — canon/personnages.json en compte {len(canon)}")

    attribuees: set[str] = set()
    for nom, dates in portail:
        k = clef(nom)
        correspondances = matcher(k, clefs_canon)
        if not correspondances:
            errors.append(f"fiche portail sans équivalent canonique : {nom!r} (clef {k!r})")
            continue
        if len(correspondances) > 1:
            errors.append(f"fiche portail ambiguë : {nom!r} correspond à {correspondances}")
            continue
        clef_canon = correspondances[0]
        if clef_canon in attribuees:
            errors.append(f"deux fiches du portail pointent le même canon : {clef_canon!r}")
        attribuees.add(clef_canon)

        # B · dates : mêmes années de vie, peu importe la rédaction.
        p = canon[clefs_canon.index(clef_canon)]
        annees_portail, annees_canon = annees(dates), annees(p.get("dates", ""))
        if annees_portail != annees_canon:
            errors.append(
                f"{nom!r} : années « {dates} » ({sorted(annees_portail)}) dans le portail, "
                f"« {p.get('dates')} » ({sorted(annees_canon)}) dans le canon — c'est le canon qui fait foi")
            continue

    for clef_canon in clefs_canon:
        if clef_canon not in attribuees:
            errors.append(f"fiche canon jamais servie par le portail : {clef_canon!r}")

    if errors:
        print("ÉCHEC DE LA PARITÉ DU PORTAIL — index.html contre canon/personnages.json")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Parité du portail validée : {len(portail)} fiches ↔ {len(canon)} du canon, "
          "dates et couverture conformes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
