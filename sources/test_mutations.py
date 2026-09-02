#!/usr/bin/env python3
"""Batterie de mutations de la chaîne de contrôle (RC-2026-III-01, lot C0).

Répondre à « le verrou tient-il ? » ne se fait pas en lisant le code : on **casse**
une copie du dépôt et l'on regarde qui bronche.

**Vingt-cinq fautes à refuser, six éditions légitimes à laisser passer** — dont la
cérémonie d'acceptation d'une variante de rendu (V4), qui teste l'autre sens du
contrat : une dérive d'environnement se RÉSOUT par un acte tracé, elle ne se subit
pas par tolérance. Et son envers, P1c : une dérive de CONTENU présentée comme un
rendu doit être refusée **même après acceptation explicite de la variante** — la
porte ouverte par V4 ne doit pas devenir une porte de service.

Depuis l'Avis royal n° 10 (2 septembre 2026), la batterie juge aussi les silences
dans les deux sens : S5, F1 et E1 refusent l'année imposée à une fête, la fixation
retirée du canon et la lacune que personne n'a décrétée ; V5 laisse passer une
lacune nouvelle **jurée selon le rite** — registre et Serment ensemble. Une lacune
non décrétée est une dette, non un mystère : encore faut-il que le rite qui la
décrète soit, lui, praticable.

Chaque scénario travaille sur sa propre copie de l'arbre (hors dépôt, hors `.git`,
hors `.venv`) : la référence n'est jamais touchée, même quand un scénario régénère
le PDF et regrave les scellés — et le workflow `batterie.yml` le vérifie après coup
par `git diff --quiet`, au lieu de le promettre.

    make batterie          # ou : python .venv/bin/python sources/test_mutations.py

Sortie : une ligne par scénario, et le compte des scénarios conformes à l'attendu.
Code de sortie 0 si tout est conforme, 1 sinon.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PY = sys.executable

# Les temps que la CI exécute, plus les quatre sceaux d'artéfacts, plus le gel des
# archives : un scénario est « bloqué » dès que l'un d'eux refuse, et l'on consigne
# lequel — la valeur du contrôle est dans sa parole, pas dans son verdict.
# R1.4.c–g (1ᵉʳ septembre 2026) : les quatre empreintes entrent dans la liste. Sans
# elles, la batterie prouverait les dents des contrôles d'hier et non de ceux
# qu'on vient de rendre bloquants.
CONTROLES = [
    "sources/check_continuity.py",
    "sources/check_silences.py",
    "sources/check_canon.py",
    "sources/check_chroniques.py",
    "sources/check_pdf.py",
    "sources/pdf_fingerprint.py --check",
    "sources/check_geography.py",
    "sources/empreinte_atlas.py --check",
    "sources/empreinte_arbre.py --check",
    "sources/empreinte_hymne.py --check",
    "sources/empreinte_vignettes.py --check",
]
LEGENDE_ANCRE = ('("images/ginette_de_port_babette.png", '
                 '"La Princesse Ginette et le Grand Sauciériste d’Or."),')
PORTRAIT_ANCRE = "* 🖼️ *Portrait officiel : `images/roger_bontemps.png`*"
COTE_LIVRE_V = ("| **UR-1998** | Décret d'ouverture de l'Union des Règnes : alternance des "
                "signatures et vacance ministérielle | 1 |")


def courir(labo: Path, commande: str) -> tuple[int, str]:
    r = subprocess.run(f"cd {labo} && {commande}", shell=True, capture_output=True, text=True)
    lignes = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, (lignes[-1] if lignes else "")


def sortie(labo: Path, commande: str) -> tuple[int, str]:
    """Comme `courir`, mais rend toute la sortie — utile pour relire une charge produite."""
    r = subprocess.run(f"cd {labo} && {commande}", shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def retoucher(labo: Path, relatif: str, zone: tuple[int, int, int, int]) -> None:
    """Peint un rectangle noir sur une image : la plus petite retouche de rendu qui tienne.

    Quelques pixels sur une planche de 3 Mio ne changent ni le nombre de pages d'un
    PDF ni la population d'un canon — mais ils changent une charge sémantique, et
    c'est précisément ce qu'on veut prouver : le sceau voit ce que les textes ne
    voient pas.
    """
    script = ("import sys;from PIL import Image,ImageDraw;"
              "p=sys.argv[1];z=tuple(int(v) for v in sys.argv[2:6]);"
              "im=Image.open(p).convert('RGB');ImageDraw.Draw(im).rectangle(z,fill=(0,0,0));"
              "im.save(p)")
    x0, y0, x1, y1 = zone
    r = subprocess.run(f'{PY} -c "{script}" {relatif} {x0} {y0} {x1} {y1}',
                       shell=True, cwd=labo, capture_output=True, text=True)
    assert r.returncode == 0, f"retouche impossible sur {relatif} : {r.stderr.strip()[:200]}"


def regenerer_seulement(labo: Path, script: str) -> None:
    """Régénère un artéfact sans retoucher l'empreinte : le contrat doit hurler."""
    rc, dernier = courir(labo, f"{PY} sources/{script}")
    assert rc == 0, f"{script} a échoué : {dernier[:200]}"


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
    """"Réimprime le volume, re-grave empreinte ET manifeste, et re-scelle les maîtres.

    R1.3 (1ᵉʳ septembre 2026) a mis `check_manifest.py --check` dans la chaîne. Une
    édition légitime du canon qui réimprime sans re-graver le manifeste échoue donc —
    à juste titre, puisque le manifeste est le scellé du texte. La batterie doit
    suivre le rite entier (ÉCRIRE → CONTRÔLER → COMPILER → VÉRIFIER → GRAVER), sans
    quoi les scénarios V2 et R1 prouvaient la chaîne d'avant R1.3 : trouvé le
    2 septembre 2026 en rejouant la batterie, les deux scénarios échouant **aussi**
    sur `HEAD`, c'est-à-dire avant tout changement de cette session.
    """
    courir(labo, f"{PY} sources/generate_encyclopedie_2026_i.py")
    courir(labo, f"{PY} sources/pdf_fingerprint.py --write")
    courir(labo, f"make --no-print-directory PY={PY} manifest")
    if sceller:
        courir(labo, f"make --no-print-directory PY={PY} iconographie")


def vue_frais(labo: Path) -> tuple[bool, str]:
    """Un seul contrôle, et lui seul : celui dont un scénario prouve le garde-fou.

    Là où `vue_controles` répond « qui bronche en premier », celle-ci répond « est-ce
    que LUI bronche » — sans quoi un scénario de garde-fou serait validé par un contrôle
    voisin et ne prouverait rien du mécanisme visé.
    """
    rc, dernier = courir(labo, f"{PY} sources/pdf_fingerprint.py --check")
    return rc != 0, f"pdf_fingerprint --check → {dernier}"


def vue_scelle(labo: Path) -> tuple[bool, str]:
    """Le gel seul : `make scelle`, sans les dix contrôles qui le précèdent.

    Même raison d'être que `vue_frais` : les scénarios R1.8 et R1.9 prouvent des
    garde-fous qui vivent dans `scelle` (parité des workflows, scellé de la galerie) —
    si un contrôle voisin bronchait à leur place, on n'aurait rien prouvé du mécanisme.
    """
    rc, dernier = courir(labo, f"make --no-print-directory PY={PY} scelle")
    return rc != 0, f"scelle → {dernier}"


def vue_silences(labo: Path) -> tuple[bool, str]:
    """La garde des silences seule (Avis royal n° 10, ticket R2.7).

    Même raison d'être que `vue_frais` et `vue_scelle` : un scénario de garde-fou
    doit être refusé par le mécanisme qu'il prouve. Les scénarios de silence
    passaient avant ce jour par la continuité, qui les tenait pour deux figures
    sur sept ; ils passeraient encore par un voisin si on les jugeait à la chaîne
    entière, et ne prouveraient rien du registre.
    """
    rc, dernier = courir(labo, f"{PY} sources/check_silences.py")
    return rc != 0, f"check_silences → {dernier}"


def vue_controles(labo: Path) -> tuple[bool, str]:
    for controle in CONTROLES:
        rc, dernier = courir(labo, f"{PY} {controle}")
        if rc:
            return True, f"{Path(controle).stem} → {dernier}"
    rc, dernier = courir(labo, f"make --no-print-directory PY={PY} scelle")
    if rc:
        return True, f"scelle → {dernier}"
    return False, "rien ne bronche"


def _accepter_comme_rendu(labo: Path) -> None:
    """Le pire usage imaginable de `--accepter` : couvrir une dérive de CONTENU.

    On réimprime le volume après avoir changé une date, on lit la charge que le contrôle
    produit, on l'accepte sous une étiquette de rendu — et le sceau doit refuser quand
    même, parce que le texte extrait, lui, n'est plus celui du contrat. C'est la clause
    qui empêche la porte ouverte par R1.4.g (variantes d'environnement) de devenir une
    porte de service : la variante dit « ce rendu-là est légitime ailleurs », jamais
    « ce texte-là est le bon ».
    """
    courir(labo, f"{PY} sources/generate_encyclopedie_2026_i.py")
    rc, out = sortie(labo, f"{PY} sources/pdf_fingerprint.py --check")
    assert rc != 0, "la charge du volume altéré aurait dû être refusée avant acceptation"
    produites = [ligne.split(":", 1)[1].strip() for ligne in out.splitlines()
                 if ligne.strip().startswith("produite")]
    assert produites, f"aucune charge produite dans le diagnostic : {out[:300]}"
    courir(labo, f"{PY} sources/pdf_fingerprint.py --accepter "
                 f"'{produites[0]}' batterie-fausse-variante-de-rendu")


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
    ("P1c · texte du volume altéré, réimprimé, et sa divergence ACCEPTÉE comme variante : le refus tient",
     lambda d: (editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md", "1875–1959", "1875–1958"),
                _accepter_comme_rendu(d)), vue_frais),
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
    ("P4 · un banc de plus dans le Livre III (divergence non déclarée)",
     lambda d: editer(d, "chroniques/LIVRE_III_LAGE_HORIZONTAL.md",
                      "ses quarante-deux bancs", "ses quarante-trois bancs"), vue_controles),
    ("P5 · cote H-1 réattribuée par le Livre V, sans déclaration",
     lambda d: editer(d, "chroniques/LIVRE_V_LUNION_DES_REGNES.md", COTE_LIVRE_V,
                      COTE_LIVRE_V + "\n| **H-1** | Registre des audiences de l'Union (1998–2010) | 1 |"),
     vue_controles),
    ("M18 · déclaration obsolète : le 82 de la Note de consolidation devient 83",
     lambda d: editer(d, "gouvernance/DIVERGENCES_CHRONIQUES.md",
                      '"grandeur":"bancs","valeurs":[3,42,82]',
                      '"grandeur":"bancs","valeurs":[3,42,83]'), vue_controles),
    ("A2 · PNG de l'Atlas retouché (une région noyée d'encre), textes intacts",
     lambda d: retoucher(d, "geographie/carte_royaume.png", (700, 900, 900, 980)),
     vue_controles),
    ("H1 · hymne rejoué sur une autre graine : même partition, même durée, même promesse",
     lambda d: (editer(d, "sources/generate_hymne.py", "GRAINE = 1847", "GRAINE = 1848"),
                regenerer_seulement(d, "generate_hymne.py")),
     vue_controles),
    ("J1 · photographie réaliste retouchée ET vignettes régénérées : seul le sceau des "
     "vignettes a des yeux",
     lambda d: (retoucher(d, "images/realistes/babber_ier_l_ancien.png", (40, 40, 260, 200)),
                regenerer_seulement(d, "generate_vignettes.py")),
     vue_controles),
    ("J1bis · photographie retouchée, vignettes PAS régénérées : le scellé de la galerie "
     "seul (R1.9)",
     lambda d: retoucher(d, "images/realistes/babber_ier_l_ancien.png", (40, 40, 260, 200)),
     vue_scelle),
    ("W1 · workflow installé retouché à la main, modèle intact : la parité seule (R1.8)",
     lambda d: editer(d, ".github/workflows/continuite.yml",
                      "python sources/pdf_fingerprint.py --check",
                      "python sources/pdf_fingerprint.py --check || true"),
     vue_scelle),
    ("S5 · année imposée à la première Transparence brune — silence juré que rien ne gardait",
     lambda d: editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md",
                      "célèbre depuis la **Journée de la Transparence brune**",
                      "célèbre depuis 1994 la **Journée de la Transparence brune**"),
     vue_silences),
    ("F1 · fixation retirée du canon, Serment et registre intacts : le décret devient une opinion",
     lambda d: editer(d, "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md",
                      "**au quatrième degré** (de la Génération II à la Génération VI) ", ""),
     vue_silences),
    ("E1 · lacune nouvelle non décrétée : le phare allumé une année qu'on ne dit pas (art. 7)",
     lambda d: editer(d, "CHRONOLOGIE_MAITRESSE_1847_2026.md",
                      "## VIII. Dates non consignées par décret",
                      "## VIII. Dates non consignées par décret\n\n"
                      "L'année d'allumage du phare de Port Babette n'est pas précisée par le registre."),
     vue_silences),
]

# Une divergence nouvelle que le registre déclare doit passer : c'est le contrat
# « résolue ou déclarée », éprouvé dans les deux sens.
def divergence_nouvelle_declares(labo: Path) -> None:
    editer(labo, "chroniques/LIVRE_III_LAGE_HORIZONTAL.md",
           "ses quarante-deux bancs", "ses quarante-trois bancs")
    editer(labo, "gouvernance/DIVERGENCES_CHRONIQUES.md",
           '"grandeur":"bancs","valeurs":[3,42,82]',
           '"grandeur":"bancs","valeurs":[3,42,43,82]')

def ceremony_acceptation(labo: Path) -> None:
    """L'autre moitié du contrat : une dérive de rendu se résout, elle ne se subit pas.

    On régénère l'hymne sur une graine étrangère (un autre environnement de rendu,
    simulé), on lit la charge que le contrôle a produite dans son message d'échec,
    on l'accepte explicitement sous une étiquette — et la chaîne doit alors passer.
    Si `--accepter` n'existait pas, ce scénario prouverait qu'il manque ; s'il
    n'était qu'un `|| true` déguisé, il prouverait qu'il est inutile. Là, il prouve
    ce qu'il est : une porte qui ne s'ouvre que de l'intérieur, et qui laisse une trace.
    """
    editer(labo, "sources/generate_hymne.py", "GRAINE = 1847", "GRAINE = 1849")
    regenerer_seulement(labo, "generate_hymne.py")
    rc, out = sortie(labo, f"{PY} sources/empreinte_hymne.py --check")
    assert rc != 0, "le contrôle aurait dû refuser la charge inédite"
    produites = [ligne.split(":", 1)[1].strip() for ligne in out.splitlines()
                 if ligne.strip().startswith("produite")]
    assert produites, f"aucune charge produite dans le diagnostic : {out[:300]}"
    courir(labo, f"{PY} sources/empreinte_hymne.py --accepter "
                 f"'{produites[0]}' batterie-environnement-etranger")


def silence_nouveau_decrete(labo: Path) -> None:
    """Le rite de l'Avis n° 10 éprouvé dans le bon sens : on jure, la chaîne passe.

    Sans ce scénario, l'article 7 ne serait qu'une interdiction de raconter. Il est
    une obligation de déclarer : un huitième silence est juré — son entrée au
    registre, son titre au Serment, et le compte que le Serment annonce en tête —
    et la chaîne entière doit le laisser passer.
    """
    registre = labo / "canon" / "silences.json"
    doc = json.loads(registre.read_text(encoding="utf-8"))
    doc["silences"].append({
        "id": "S8",
        "objet": "Nom du castor qui mordit la botte du Dormeur",
        "borne": "Le fait est attesté par le rapport A-41 : la botte fut conservée, le castor relâché.",
        "tu": "Le nom de l'animal. Le rapport ne donne que son rang dans la hiérarchie des castors.",
        "couvre": ["castor"],
        "portee": ["ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"],
        "gardes": [{"ancrage": "castor",
                    "motif": "matricule\\s+\\d{2,4}-\\d{2,4}",
                    "dit": "matricule d'un castor du chantier"}],
    })
    registre.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    serment = labo / "gouvernance" / "SERMENT_D_IGNORANCE.md"
    texte = serment.read_text(encoding="utf-8")
    ancre = "## IV. La fixation"
    assert ancre in texte, "rubrique des fixations introuvable dans le Serment"
    texte = texte.replace(ancre,
                          "### S8 · Le nom du castor qui mordit la botte du Dormeur\n\n"
                          "* **Borne (ce qui est su)** — Le fait est attesté par le rapport A-41 : "
                          "la botte fut conservée, le castor relâché.\n"
                          "* **Tu** — Le nom de l'animal. Le rapport ne donne que son rang dans la "
                          "hiérarchie des castors.\n"
                          "* **Garde** — Aucun matricule ne peut être attaché à un castor du chantier.\n\n"
                          + ancre, 1)
    texte = texte.replace("7 silences jurés", "8 silences jurés")
    serment.write_text(texte, encoding="utf-8")


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
    ("V3 · divergence nouvelle surgie ET déclarée au registre : la chaîne laisse passer",
     divergence_nouvelle_declares),
    ("V4 · rendu d'un autre environnement OBSERVÉ puis ACCEPTÉ à la main : la chaîne laisse passer",
     ceremony_acceptation),
    ("V5 · lacune nouvelle JURÉE selon le rite (registre + Serment + compte) : la chaîne laisse passer",
     silence_nouveau_decrete),
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
