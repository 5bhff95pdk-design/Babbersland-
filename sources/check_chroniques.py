#!/usr/bin/env python3
"""Arithmétique interne des chroniques et cotes d'archives — constats F-02, F-03.

Sans dépendance. Trois objets, que rien ne contrôlait avant ce script :

1. **Grandeurs chiffrées récurrentes.** Les chroniques citent des nombres qui
   engagent le monde (quarante bancs, deux canaux, trois villes, 214 sujets…).
   Que deux volumes n'en disent pas la même chose est une divergence ; que le
   canon en dise une autre est une faute. Le contrôle les relève toutes.
2. **Cotes d'archives.** Chaque chronique tient en annexe une table
   `| **A-34** | description | tranche |`. Deux rédactions peuvent donner la
   même cote à deux documents différents (F-02 : huit collisions) : la table
   rend la collision vérifiable, ce que `check_continuity.py` ne fait pas.
3. **Registre des divergences déclarées** (`gouvernance/DIVERGENCES_CHRONIQUES.md`).
   Même contrat que `propositions_declarées` (E-19) : une divergence est
   **résolue** ou **déclarée**. Une déclaration qui ne correspond plus à rien
   — divergence disparue, cote réconciliée — est elle-même une faute : le
   registre ne doit pas accréditer des conflits qui n'existent plus.

Autorité : `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`. Une chronique est « proposée,
non décrétée » : elle peut taire, elle ne peut pas contredire.

Usage :
    python sources/check_chroniques.py              # contrôle (échec = code 1)
    python sources/check_chroniques.py --inventaire # relève tout, sans exiger
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHRONIQUES = sorted((ROOT / "chroniques").glob("*.md"))
CANON = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
CHRONOLOGIE = ROOT / "CHRONOLOGIE_MAITRESSE_1847_2026.md"
REGISTRE = ROOT / "gouvernance" / "DIVERGENCES_CHRONIQUES.md"

# ---------------------------------------------------------------- nombres

UNITES = {
    "zéro": 0, "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10, "onze": 11, "douze": 12,
    "treize": 13, "quatorze": 14, "quinze": 15, "seize": 16, "dix-sept": 17,
    "dix-huit": 18, "dix-neuf": 19, "vingt": 20, "vingts": 20, "trente": 30, "quarante": 40,
    "cinquante": 50, "soixante": 60, "cent": 100, "cents": 100, "mille": 1000,
    "mil": 1000,
}
MOTS = "|".join(sorted(UNITES, key=len, reverse=True))
# « deux cent quatorze », « quarante-deux », « 1 200 », « 7 000 »
# NB : l'alternance doit être groupée, sinon le groupe final ne porte que sur le
# dernier terme de MOTS et « quarante-deux » se lit « deux ».
NOMBRE = rf"(?P<n>\d[\d  \xa0]*|(?:{MOTS})(?:[- ](?:et[- ])?(?:{MOTS}))*)"


def en_entier(brut: str) -> int | None:
    """« quarante-deux » → 42 ; « deux cent quatorze » → 214 ; « 7 000 » → 7000."""
    brut = brut.strip()
    if re.fullmatch(r"\d[\d  \xa0]*", brut):
        return int(re.sub(r"[\s \xa0]", "", brut))
    total = courant = 0
    vu = False
    for mot in re.split(r"[\s-]+", brut):
        if mot in ("et", ""):
            continue
        if mot not in UNITES:
            return None
        val = UNITES[mot]
        vu = True
        if val == 1000:
            courant = (courant or 1) * 1000
            total += courant
            courant = 0
        elif val == 100:
            courant = (courant or 1) * 100
        elif val in (20, 30, 40, 50, 60) and courant in (2, 3, 4, 5, 6):
            courant *= val          # quatre-vingts, trois-vingts (usage ancien)
        else:
            courant += val
    return total + courant if vu else None


# ------------------------------------------------------------- grandeurs

# (identifiant, libellé, motifs) — le motif capture le nombre devant l'objet.
GRANDEURS: list[tuple[str, str, list[str]]] = [
    ("bancs", "bancs du Double Aqueduc", [rf"{NOMBRE}\s+bancs(?!\s+d'essai)",
                                          rf"{NOMBRE}\s+banc\b"]),
    ("canaux", "canaux de l'aqueduc", [rf"{NOMBRE}\s+canaux", rf"{NOMBRE}\s+canal\b"]),
    ("arches", "arches de l'aqueduc", [rf"{NOMBRE}\s+arches", rf"{NOMBRE}\s+arche\b"]),
    ("villes", "villes du Royaume", [rf"{NOMBRE}\s+villes"]),
    ("regions", "régions du Royaume", [rf"{NOMBRE}\s+régions"]),
    ("km", "kilomètres d'ouvrage", [rf"{NOMBRE}\s+kilomètres", rf"{NOMBRE}\s+km\b"]),
    ("population", "population (âmes, habitants, sujets)",
     [rf"{NOMBRE}\s+(?:âmes|habitants|sujets\s+officiels|sujets|humains|citoyens)"]),
]

COTE_TABLE = re.compile(r"^\|\s*\*\*([A-Z]+-\d+(?:\s+bis)?)\*\*\s*\|([^|]*)\|")


def documents() -> list[tuple[str, Path]]:
    """Les textes à confronter : le canon d'abord, puis les chroniques."""
    return ([("canon", CANON), ("chronologie", CHRONOLOGIE)]
            + [(p.name, p) for p in CHRONIQUES])


def releve_grandeurs() -> dict[str, dict[str, list[tuple[int, int, str]]]]:
    """grandeur → document → [(valeur, ligne, extrait)]"""
    out: dict[str, dict[str, list[tuple[int, int, str]]]] = {}
    for gid, _lib, motifs in GRANDEURS:
        out[gid] = {}
        for doc, chemin in documents():
            if not chemin.exists():
                continue
            for i, ligne in enumerate(chemin.read_text(encoding="utf-8").splitlines(), 1):
                for motif in motifs:
                    for m in re.finditer(motif, ligne, flags=re.IGNORECASE):
                        val = en_entier(m.group("n"))
                        if val is None or val <= 0:
                            continue
                        # « sur un banc », « une âme » : article, pas dénombrement.
                        if val == 1 and m.group("n").strip().lower() in ("un", "une"):
                            continue
                        extrait = " ".join(ligne[max(0, m.start() - 40):m.end() + 30].split())
                        out[gid].setdefault(doc, []).append((val, i, extrait))
    return out


def releve_cotes() -> dict[str, dict[str, tuple[int, str]]]:
    """cote → document → (ligne, description) — tables d'annexe des chroniques."""
    out: dict[str, dict[str, tuple[int, str]]] = {}
    for doc, chemin in documents():
        if not chemin.exists():
            continue
        for i, ligne in enumerate(chemin.read_text(encoding="utf-8").splitlines(), 1):
            m = COTE_TABLE.match(ligne.strip())
            if not m:
                continue
            cote = " ".join(m.group(1).split())
            desc = " ".join(m.group(2).split())
            if desc:
                out.setdefault(cote, {})[doc] = (i, desc)
    return out


# --------------------------------------------------------------- registre


def charge_registre() -> list[dict]:
    """Lit le bloc JSON déclaré dans gouvernance/DIVERGENCES_CHRONIQUES.md."""
    if not REGISTRE.exists():
        return []
    texte = REGISTRE.read_text(encoding="utf-8")
    blocs = re.findall(r"```json\s*(.*?)```", texte, flags=re.S)
    if not blocs:
        sys.exit(f"{REGISTRE.relative_to(ROOT)} : aucun bloc ```json déclaré.")
    try:
        return json.loads(blocs[-1])
    except json.JSONDecodeError as exc:
        sys.exit(f"{REGISTRE.relative_to(ROOT)} : JSON illisible ({exc}).")


def couvre_chiffre(entree: dict, gid: str, valeurs: list[int], docs: list[str]) -> bool:
    return (entree.get("type") == "chiffre" and entree.get("grandeur") == gid
            and sorted(entree.get("valeurs", [])) == sorted(valeurs)
            and sorted(entree.get("documents", [])) == sorted(docs))


def couvre_cote(entree: dict, cote: str, docs: list[str]) -> bool:
    return (entree.get("type") == "cote" and entree.get("cote") == cote
            and sorted(entree.get("documents", [])) == sorted(docs))


# ------------------------------------------------------------- le contrôle


def main() -> int:
    inventaire = "--inventaire" in sys.argv
    fautes: list[str] = []
    declarees = charge_registre()
    utilisees = set()

    # ---- 1. grandeurs chiffrées — une grandeur qui ne dit pas le même chiffre
    #         partout est une divergence ; une seule déclaration la couvre.
    releve = releve_grandeurs()
    for gid, libelle, _ in GRANDEURS:
        par_doc = {d: {v for v, _i, _e in occ} for d, occ in releve[gid].items()}
        if not par_doc or not any(d != "canon" for d in par_doc):
            continue
        union = sorted(set().union(*par_doc.values()))
        if inventaire:
            print(f"\n### {libelle}")
            for d, vals in sorted(par_doc.items()):
                ex = releve[gid][d][0]
                print(f"    {d[:34]:36} {sorted(vals)}  (ex. l.{ex[1]})")
        if len(union) < 2:
            continue
        temoins = sorted(d for d, v in par_doc.items() if v)
        couvrantes = [e for e in declarees
                      if couvre_chiffre(e, gid, union, temoins)]
        if couvrantes:
            utilisees.add(json.dumps(couvrantes[-1], sort_keys=True))
            continue
        gravite = ("le canon est contredit" if par_doc.get("canon")
                   else "les volumes divergent entre eux")
        detail = " ; ".join(f"{d} → {sorted(v)}" for d, v in sorted(par_doc.items()) if v)
        fautes.append(f"grandeur « {libelle} » : {gravite} — {union} selon les documents "
                      f"({detail})")

    # ---- 2. cotes d'archives en collision
    cotes = releve_cotes()
    collisions = 0
    for cote, par_doc in sorted(cotes.items()):
        if len(par_doc) < 2:
            continue
        descs = {d: v[1] for d, v in par_doc.items()}
        if len(set(descs.values())) < 2:
            continue
        collisions += 1
        docs = sorted(descs)
        if inventaire:
            print(f"\n### cote {cote} (collision)")
            for d in docs:
                print(f"    {d[:34]:36} l.{par_doc[d][0]}  {par_doc[d][1][:90]}")
        if any(couvre_cote(e, cote, docs) for e in declarees):
            utilisees.add(json.dumps(
                [e for e in declarees if couvre_cote(e, cote, docs)][-1], sort_keys=True))
            continue
        detail = " | ".join(f"{d} : « {descs[d][:60]} »" for d in docs)
        fautes.append(f"cote d'archives {cote} en collision : {detail}")

    # ---- 3. déclarations qui ne correspondent plus à rien
    for entree in declarees:
        cle = json.dumps(entree, sort_keys=True)
        if cle not in utilisees:
            fautes.append(
                f"déclaration obsolète dans {REGISTRE.name} — elle ne décrit plus "
                f"aucune divergence observée : {cle[:160]}")

    if inventaire:
        print(f"\n{len(declarees)} déclaration(s) au registre, "
              f"{len(utilisees)} utilisée(s), {collisions} cote(s) en collision.")
        print(f"{len(fautes)} divergence(s) non déclarée(s).")
        return 0

    if fautes:
        print("Chroniques — divergences non déclarées :", file=sys.stderr)
        for f in fautes:
            print(f"  - {f}", file=sys.stderr)
        print(f"\n{len(fautes)} constat(s). Résoudre, ou déclarer dans "
              f"{REGISTRE.relative_to(ROOT)}.", file=sys.stderr)
        return 1

    print(f"Chroniques validées : {len(GRANDEURS)} grandeurs confrontées, "
          f"{sum(len(v) for v in cotes.values())} cotes d'archives, "
          f"{len(declarees)} divergence(s) déclarée(s), toutes observées.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
