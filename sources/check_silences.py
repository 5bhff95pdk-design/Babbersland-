#!/usr/bin/env python3
"""Garde du registre des silences — Avis royal n° 10 (ticket R2.7).

Le Serment d'Ignorance promettait depuis le 30 août 2026 que « les scripts de
validation reconnaissent ces lacunes comme conformes au canon et rejettent toute
tentative d'imposer une fixation arbitraire ». La promesse n'était tenue qu'à
moitié : cinq silences proclamés, deux réellement gardés, et deux listes de cinq
qui ne se recouvraient pas (celle du Serment, celle de la ROADMAP) — sans parler
de la Chronologie, qui en tenait une troisième. Une lacune que rien ne garde
n'est pas un mystère, c'est un trou.

Ce contrôle ferme la question par le seul moyen qui tienne ici : **le registre
est la source unique** (`canon/silences.json`), le Serment en est le miroir
lisible, et le garde vérifie qu'aucun des deux ne parle sans l'autre.

Vérifications
-------------
A. **Registre** — ids uniques, champs requis, silences bornés, portées existantes.
B. **Parité registre ↔ Serment** — tout silence du registre est décrété dans
   `gouvernance/SERMENT_D_IGNORANCE.md` (titre `### S1 · …`) et réciproquement ;
   idem pour les fixations (`### F1 · …`). Un silence hors registre est une
   lacune non décrétée ; un registre hors Serment est une cérémonie oubliée.
C. **Perce-ment** — sur chaque fichier de la portée d'un silence, aucune ligne
   ne satisfait à la fois l'ancrage et le motif interdit, sauf exemption écrite
   au registre (`permet`).
D. **Fixation attestée** — la valeur fixée est portée au canon, et son
   rétro-contrôle arithmétique tient (rangs de génération, écart décrété).
E. **Anti-dette** — tout marqueur de lacune relevé dans les fichiers sous garde
   est couvert par un silence décrété ou par une dispense écrite. Une lacune
   trouvée par la machine doit être décrétée dans la session qui la trouve.

Usage :
    python sources/check_silences.py            # la garde complète (make controle)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRE = ROOT / "canon" / "silences.json"
SERMENT = ROOT / "gouvernance" / "SERMENT_D_IGNORANCE.md"

# Fenêtre de couverture d'un marqueur de lacune : une rubrique vaut pour les
# lignes qu'elle chapeaute — le nom de la figure est dans le titre, la mention
# « non consignée » trois lignes plus bas (cas de Roger Bontemps en 2026-I).
AVANT, APRES = 3, 1


def normaliser(texte: str) -> str:
    return texte.replace("\u2019", "'").replace("\u2018", "'").replace("\u00a0", " ")


def lire_registre() -> dict:
    if not REGISTRE.is_file():
        raise SystemExit(f"ÉCHEC DE LA GARDE DES SILENCES — registre absent : {REGISTRE.name}")
    return json.loads(REGISTRE.read_text(encoding="utf-8"))


def lignes_de(rel: str) -> list[str]:
    return [normaliser(l) for l in (ROOT / rel).read_text(encoding="utf-8").splitlines()]


def percees(rel: str, texte: str | None = None) -> list[str]:
    """Erreurs de perce-ment pour un fichier : le garde appliqué, rien de plus.

    `check_continuity.py` s'en sert pour tenir la promesse du Serment sur le
    canon sans redéfinir les silences : le registre dit, ce garde applique.
    """
    doc = lire_registre()
    lignes = [normaliser(l) for l in texte.splitlines()] if texte is not None else lignes_de(rel)
    out: list[str] = []
    for silence in doc.get("silences", []):
        if rel not in silence.get("portee", []):
            continue
        sid = silence.get("id", "?")
        for numero, ligne in enumerate(lignes, 1):
            # L'ancrage peut être trois lignes plus haut : dans 2026-I, le nom de la
            # figure est dans le titre de sa notice et la phrase fautive sous ce titre.
            # Le motif interdit, lui, ne se lit que sur la ligne même.
            contexte = " ".join(lignes[max(0, numero - 1 - AVANT):numero])
            for garde in silence.get("gardes", []):
                motif = garde.get("motif")
                if not motif:
                    continue
                ancre = garde.get("ancrage")
                if ancre and not (re.search(ancre, ligne, re.I) or re.search(ancre, contexte, re.I)):
                    continue
                trouve = re.search(motif, ligne, re.I)
                if not trouve:
                    continue
                # Une exemption ne s'apprécie que sur ce que le motif a saisi :
                # « issu de la branche de Babette-Marine » est permis, « issu de
                # la sœur du Dormeur » ne l'est pas.
                cible = " ".join(g for g in trouve.groups() if g) if trouve.groups() else ligne
                if any(re.search(p, cible, re.I) for p in garde.get("permet", [])):
                    continue
                out.append(
                    f"silence {sid} percé — {garde.get('dit', 'fixation interdite')} "
                    f"({rel}:{numero}) : « {ligne.strip()[:88]}… »")
    return out


def verifier() -> tuple[list[str], list[str]]:
    """(erreurs, constats) — la garde complète, hors perce-ment délégué."""
    erreurs: list[str] = []
    constats: list[str] = []

    def dire(condition: bool, message: str) -> bool:
        if not condition:
            erreurs.append(message)
        return condition

    doc = lire_registre()
    silences = doc.get("silences", [])
    fixations = doc.get("fixations", [])
    dispenses = doc.get("dispenses", [])
    marqueurs = doc.get("marqueurs_lacune", [])

    # ── A. le registre ────────────────────────────────────────────────────────
    ids = [s.get("id") for s in silences]
    dire(len(ids) == len(set(ids)), f"identifiants de silences en doublon : {ids}")
    dire(bool(silences), "aucun silence décrété au registre : le Serment ne garderait rien")

    gardes_total = 0
    applications = 0
    fichiers: list[str] = []
    for silence in silences:
        sid = silence.get("id", "?")
        for cle in ("objet", "tu", "portee", "gardes"):
            dire(cle in silence, f"{sid} : champ « {cle} » absent du registre")
        if "borne" not in silence:
            erreurs.append(
                f"{sid} : silence non borné — ce qui est SU doit être dit, sinon ce n'est pas "
                "un mystère mais un trou (Avis royal n° 10, art. 2)")
        gardes_total += len(silence.get("gardes", []))
        for rel in silence.get("portee", []):
            if dire((ROOT / rel).is_file(), f"{sid} : fichier sous garde introuvable : {rel}"):
                if rel not in fichiers:
                    fichiers.append(rel)
                applications += len(silence.get("gardes", []))
                for garde in silence.get("gardes", []):
                    dire("motif" in garde,
                         f"{sid} : garde sans motif — un garde qui ne dit pas ce qu'il interdit ne garde rien")
                    dire("dit" in garde,
                         f"{sid} : garde sans libellé « dit » : un motif seul ne se relit pas")

    # ── B. parité registre ↔ Serment ──────────────────────────────────────────
    texte_serment = normaliser(SERMENT.read_text(encoding="utf-8")) if SERMENT.is_file() else ""
    dits_silences = re.findall(r"^#{2,4}\s*(S\d+)\s*[·–—-]", texte_serment, re.M)
    dits_fixations = re.findall(r"^#{2,4}\s*(F\d+)\s*[·–—-]", texte_serment, re.M)
    for sid in ids:
        dire(sid in dits_silences,
             f"{sid} : silence présent au registre mais non décrété dans le Serment "
             f"(titre attendu « ### {sid} · … ») — une lacune non proclamée n'est pas défendable")
    for sid in dits_silences:
        dire(sid in ids,
             f"{sid} : silence proclamé par le Serment mais absent du registre — "
             "le Serment parle sans la machine, et la machine sans lui")
    for fixation in fixations:
        dire(fixation.get("id", "?") in dits_fixations,
             f"{fixation.get('id', '?')} : fixation absente du Serment")
    for fid in dits_fixations:
        dire(fid in [f.get("id") for f in fixations],
             f"{fid} : fixation proclamée par le Serment mais non inscrite au registre")
    dire("Avis royal n° 10" in texte_serment,
         "le Serment ne mentionne pas l'Avis royal n° 10 qui le fonde")
    # Le compte doit être ÉCRIT, pas déductible du hasard des chiffres : « S8 » dans un
    # titre ferait passer un inventaire de huit pour annoncé. On exige donc la formule.
    compte = re.search(r"(\d+)\s+silences?\s+jur[ée]s?", texte_serment, re.I)
    dire(compte is not None and int(compte.group(1)) == len(ids),
         f"le Serment annonce {compte.group(1) + ' silence(s) juré(s)' if compte else 'aucun compte'} "
         f"quand le registre en jure {len(ids)} — le compte des silences doit être écrit en "
         "toutes lettres dans le Serment, et non se déduire d'un numéro de titre")

    # ── C. perce-ment ─────────────────────────────────────────────────────────
    for rel in fichiers:
        erreurs.extend(percees(rel))

    # ── D. fixations attestées et rétro-contrôlées ────────────────────────────
    def champ(chemin_rel: str, identifiant: str, cle: str):
        donnees = json.loads((ROOT / chemin_rel).read_text(encoding="utf-8"))
        for entree in donnees.get("personnages", []):
            if entree.get("id") == identifiant:
                return entree.get(cle)
        return None

    for fixation in fixations:
        fid = fixation.get("id", "?")
        attestation = fixation.get("attestation", {})
        rel, motif = attestation.get("fichier", ""), attestation.get("motif", "")
        chemin = ROOT / rel
        if dire(chemin.is_file(), f"{fid} : fichier d'attestation introuvable : {rel}"):
            texte = normaliser(chemin.read_text(encoding="utf-8"))
            dire(bool(motif) and re.search(motif, texte, re.I),
                 f"{fid} : fixation non portée au canon — {rel} ne contient pas « {motif} ». "
                 "Un décret qui n'est pas écrit là où il s'applique est une opinion.")
        arith = fixation.get("arithmetique", {})
        if arith:
            souche, bout = arith.get("souche", {}), arith.get("bout", {})
            a = champ(souche.get("fichier", ""), souche.get("id", ""), souche.get("champ", ""))
            b = champ(bout.get("fichier", ""), bout.get("id", ""), bout.get("champ", ""))
            if dire(a is not None and b is not None,
                    f"{fid} : rétro-contrôle impossible — fiche absente des données"):
                dire(int(b) - int(a) == int(arith.get("ecart", 0)),
                     f"{fid} : rétro-contrôle en défaut — {bout.get('id')} ({b}) moins "
                     f"{souche.get('id')} ({a}) fait {int(b) - int(a)}, et non {arith.get('ecart')} : "
                     "redessiner l'arbre ou corriger le décret")

    # ── E. anti-dette : toute lacune relevée doit être décrétée ───────────────
    couvertures = {s.get("id"): s.get("couvre", []) for s in silences}
    marqueurs_trouves = 0
    for rel in fichiers:
        lignes = lignes_de(rel)
        for numero, ligne in enumerate(lignes):
            if not any(m.lower() in ligne.lower() for m in marqueurs):
                continue
            marqueurs_trouves += 1
            fenetre = " ".join(lignes[max(0, numero - 1 - AVANT):numero + APRES])
            couvert = any(any(re.search(token, fenetre, re.I) for token in tokens)
                          for tokens in couvertures.values() if tokens)
            dispense = any(d.get("fichier") == rel and re.search(d.get("motif", "$."), ligne, re.I)
                           for d in dispenses)
            dire(couvert or dispense,
                 f"lacune non décrétée ({rel}:{numero}) : « {ligne.strip()[:88]}… » — "
                 "la déclarer au registre (Avis royal n° 10, art. 7) ou la combler")

    constats.append(f"{len(silences)} silences jurés, {gardes_total} gardes "
                 f"appliqués {applications} fois")
    constats.append(f"{len(fixations)} fixation(s) attestée(s) et rétro-contrôlée(s)")
    constats.append(f"{len(fichiers)} fichier(s) sous garde")
    constats.append(f"{marqueurs_trouves} marqueur(s) de lacune, tous décrétés ou dispensés")
    return erreurs, constats


def main() -> int:
    erreurs, constats = verifier()
    if erreurs:
        print("ÉCHEC DE LA GARDE DES SILENCES — Avis royal n° 10")
        for erreur in erreurs:
            print(f"- {erreur}")
        return 1
    print("Silences gardés : " + " · ".join(constats) + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
