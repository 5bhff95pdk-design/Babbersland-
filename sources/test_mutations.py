#!/usr/bin/env python3
"""Batterie de mutations de la chaîne de contrôle (RC-2026-III-01, lot C0).

Répondre à « le verrou tient-il ? » ne se fait pas en lisant le code : on **casse**
une copie du dépôt et l'on regarde qui bronche. Ce script rejoue quatorze altérations
qui doivent être refusées et trois éditions qui doivent être laissées passer.

Chaque scénario travaille sur sa propre copie de l'arbre (hors dépôt, hors `.git`,
hors `.venv`) : la référence n'est jamais touchée, même quand un scénario régénère
le PDF et regrave les scellés.

    make batterie          # ou : python .venv/bin/python sources/test_mutations.py

Sortie : une ligne par scénario, et le compte des scénarios conformes à l'attendu.
Code de sortie 0 si tout est conforme, 1 sinon.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PY = sys.executable

# Les cinq temps que la CI exécute, plus le scellé : un scénario est « bloqué » dès
# que l'un d'eux refuse, et l'on consigne lequel — la valeur du contrôle est dans sa
# parole, pas dans son verdict.
CONTROLES = [
    "sources/check_continuity.py",
    "sources/check_canon.py",
    "sources/check_pdf.py",
    "sources/pdf_fingerprint.py --check",
    "sources/check_geography.py",
]
LEGENDE_ANCRE = ('("images/ginette_de_port_babette.png", '
                 '"La Princesse Ginette et le Grand Sauciériste d’Or."),')
PORTRAIT_ANCRE = "* 🖼️ *Portrait officiel : `images/roger_bontemps.png`*"


def courir(labo: Path, commande: str) -> tuple[int, str]:
    r = subprocess.run(f"cd {labo} && {commande}", shell=True, capture_output=True, text=True)
    lignes = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, (lignes[-1] if lignes else "")


def editer(labo: Path, relatif: str, old: str, new: str) -> None:
    chemin = labo / relatif
    texte = chemin.read_text(encoding="utf-8")
    assert old in texte, f"cible absente de {relatif} : {old[:60]}"
    chemin.write_text(texte.replace(old, new, 1), encoding="utf-8")


def intervertir(labo: Path, a: str, b: str) -> None:
    pa, pb = labo / "images" / a, labo / "images" / b
    x, y = pa.read_bytes(), pb.read_bytes()
    pa.write_bytes(y)
    pb.write_bytes(x)


def regenerer(labo: Path, sceller: bool = True) -> None:
    """"Réimprime le volume, grave à nouveau l'empreinte et, par défaut, re-scelle les maîtres."""
    courir(labo, f"{PY} sources/generate_encyclopedie_2026_i.py")
    courir(labo, f"{PY} sources/pdf_fingerprint.py --write")
    if sceller:
        courir(labo, f"make --no-print-directory PY={PY} iconographie")


def vue_controles(labo: Path) -> tuple[bool, str]:
    for controle in CONTROLES:
        rc, dernier = courir(labo, f"{PY} {controle}")
        if rc:
            return True, f"{Path(controle).stem} → {dernier}"
    rc, dernier = courir(labo, f"make --no-print-directory PY={PY} scelle")
    if rc:
        return True, f"scelle → {dernier}"
    return False, "rien ne bronche"


def ajouter_planche(legende: str) -> str:
    return LEGENDE_ANCRE + f'\n        ("images/portrait_bis.png", "{legende}"),'


def faute_planche_sans_promesse(labo: Path) -> None:
    shutil.copy(labo / "images/babber_le_dechire.png", labo / "images/portrait_bis.png")
    editer(labo, "sources/generate_encyclopedie_2026_i.py", LEGENDE_ANCRE,
           ajouter_planche("Portrait bis de la cour."))
    regenerer(labo)


# ── ce que la chaîne doit refuser ─────────────────────────────────────────────
FAUTES: list[tuple[str, object, object]] = [
    ("P1 · deux portraits intervertis, volume non réimprimé",
     lambda d: intervertir(d, "babber_le_fou.png", "babber_le_dormeur.png"), vue_controles),
    ("P1b · permutation, volume et empreinte gravés à nouveau, scellé des maîtres oublié",
     lambda d: (intervertir(d, "babber_le_fou.png", "babber_le_dormeur.png"),
                regenerer(d, sceller=False)), vue_controles),
    ("P2 · planche insérée au volume sans promesse du canon",
     faute_planche_sans_promesse, vue_controles),
    ("P3 · naissance imposée à Roger Bontemps (silence sanctifié n° 2)",
     lambda d: editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md", "Roger Bontemps, Premier Joyeux",
                      "Roger Bontemps (né en 1802), Premier Joyeux"), vue_controles),
    ("M1 · Monts Froissés affirmés debout en 1946 (Chronologie)",
     lambda d: editer(d, "CHRONOLOGIE_MAITRESSE_1847_2026.md",
                      "| **1946** | Naissance de Babber le Louche.",
                      "| **1946** | Naissance de Babber le Louche, sous les Monts Froissés déjà debout."),
     vue_controles),
    ("M3 · mort du Dormeur décalée dans 2026-I seul",
     lambda d: editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md", "1875–1959", "1875–1958"), vue_controles),
    ("M9 · Ti-Babber promu 8ᵉ génération dans les données seules",
     lambda d: editer(d, "canon/personnages.json", '"generation": 7', '"generation": 8'), vue_controles),
    ("M10 · population totale portée à 9 000 dans les données seules",
     lambda d: editer(d, "canon/lieux.json", '"population_totale": 7000', '"population_totale": 9000'),
     vue_controles),
    ("M11 · avis ajouté dans l'archive gelée 2026-H",
     lambda d: (d / "HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md").write_text(
         (d / "HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md").read_text(encoding="utf-8")
         + "\n\nAvis n° 99 après scellement.\n", encoding="utf-8"), vue_controles),
    ("M14 · événement daté d'un jour hors corpus",
     lambda d: editer(d, "canon/evenements.json", '"date": "1882"', '"date": "3 février 1885"'), vue_controles),
    ("M15 · date du Registre décrochée du canon",
     lambda d: editer(d, "gouvernance/REGISTRE_DES_PERSONNAGES.md", "Née en 1882", "Née en 1879"),
     vue_controles),
    ("M16 · générateur PDF à la syntaxe cassée",
     lambda d: (d / "sources/generate_encyclopedie_2026_i.py").write_text(
         (d / "sources/generate_encyclopedie_2026_i.py").read_text(encoding="utf-8")
         + '\nprint("parenthèse non fermée →\n', encoding="utf-8"), vue_controles),
    ("M17 · chronique qui se déclare adoptée sans Avis n° 7",
     lambda d: editer(d, "chroniques/LIVRE_VI_LE_SIECLE_QUI_LOUCHE.md", "proposés", "adoptés"), vue_controles),
]

# ── ce que la chaîne doit laisser passer ─────────────────────────────────────
JUSTES: list[tuple[str, object]] = [
    ("V1 · dépôt tel quel, chaîne complète", None),
    ("V2 · planche légitime : promise, ancrée, scellée",
     lambda d: (shutil.copy(d / "images/babber_le_dechire.png", d / "images/babber_le_dechire_bis.png"),
                editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md",
                       "* 🖼️ *Portrait officiel : `images/babber_le_dechire.png`*",
                       "* 🖼️ *Portrait officiel : `images/babber_le_dechire.png`*\n"
                       "* 🖼️ *Portrait de second rang : `images/babber_le_dechire_bis.png`*"),
                editer(d, "sources/generate_encyclopedie_2026_i.py",
                       '("images/babber_le_dechire.png", "Portrait officiel du Prince Babber le Déchiré."),',
                       '("images/babber_le_dechire.png", "Portrait officiel du Prince Babber le Déchiré."),\n'
                       '        ("images/babber_le_dechire_bis.png", "Portrait de second rang du Prince Déchiré."),'),
                regenerer(d))),
    ("R1 · planche bénie par le canon ET scellés re-scellés : le résidu passe, et c'est assumé",
     lambda d: (shutil.copy(d / "images/babber_le_dechire.png", d / "images/portrait_bis.png"),
                editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md", PORTRAIT_ANCRE,
                       PORTRAIT_ANCRE + "\n* 🖼️ *Portrait bis de la cour : `images/portrait_bis.png`*"),
                editer(d, "sources/generate_encyclopedie_2026_i.py", LEGENDE_ANCRE,
                       ajouter_planche("Portrait bis de la cour.")),
                regenerer(d))),
]


def labo(nom: str, base: Path) -> Path:
    d = base / nom
    shutil.copytree(RACINE, d, ignore=shutil.ignore_patterns(
        ".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"))
    return d


def main() -> int:
    conformes = 0
    with tempfile.TemporaryDirectory(prefix="babbersland-mutations-") as tmp:
        base = Path(tmp)
        print("=" * 100)
        print("FAUTES — la chaîne doit refuser")
        print("=" * 100)
        for i, (titre, muter, juger) in enumerate(FAUTES):
            d = labo(f"faute-{i}", base)
            muter(d)  # type: ignore[operator]
            bloquee, detail = juger(d)  # type: ignore[operator]
            conformes += bool(bloquee)
            marque = f"✅ refusée par {detail[:62]}" if bloquee else "🔴 PASSÉE — la chaîne ne voit rien"
            print(f"{titre:<62}{marque}")
        print("=" * 100)
        print("ÉDITIONS LÉGITIMES — la chaîne doit laisser passer")
        print("=" * 100)
        for i, (titre, muter) in enumerate(JUSTES):
            d = labo(f"juste-{i}", base)
            if muter:
                muter(d)  # type: ignore[operator]
            rc, dernier = courir(d, f"make --no-print-directory PY={PY} controle")
            conformes += rc == 0
            marque = f"✅ acceptée — {dernier[:60]}" if rc == 0 else f"🔴 refusée à tort (rc={rc}) {dernier[:60]}"
            print(f"{titre:<62}{marque}")
    total = len(FAUTES) + len(JUSTES)
    print("=" * 100)
    print(f"scénarios conformes à l'attendu : {conformes}/{total}")
    return 0 if conformes == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
