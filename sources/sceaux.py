#!/usr/bin/env python3
"""Mécanique commune des sceaux d'artéfacts régénérés — modèle « variantes acceptées ».

Pourquoi ce module (R1.4, 1ᵉʳ septembre 2026). Les artéfacts que la chaîne produit —
Arbre PNG, Atlas (SVG/PNG/HTML), enregistrement de l'hymne, vignettes WebP, et jusqu'à
l'empreinte du PDF — sont **bit-stables sur une machine, pas entre machines** :
l'antialiasing de FreeType, la version de libwebp, un ULP de `math.sin` dans la
synthèse sonore suffisent à changer des octets sans rien changer au contenu. La
stratégie `git diff --exit-code` (comparer les octets) rend donc la CI rouge pour du
bruit — c'est exactement ce qui a fait vivre `continue-on-error` à six étapes
(douleur R1.4.a-v2, mesure R1.4.b, faux positif R1.4.h).

Le modèle retenu à R1.4.b, étendu ici aux autres artéfacts :

1. on calcule une **charge** sémantique (géométrie + rendu moyenné quantifié, jamais
   les octets du fichier) ;
2. on grave dans `gouvernance/ARTIFACT_SIGNATURES.sha256` **l'ensemble des charges
   observées et acceptées**, chacune nommée (`reference-locale`, `ci-ubuntu-24.04-py3.12`…) ;
3. la conformité = la charge courante **appartient** à l'ensemble. Rien de plus,
   rien de moins : aucune tolérance chiffrée à négocier, puisque le bruit *connu* est
   nommé et que tout le reste bloque ;
4. une divergence est **diagnostiquée** (annotation de check-run + comparaison
   composante par composante) puis acceptée à la main par `--accepter`, acte
   d'assentiment tracé dans git. Jamais de bascule silencieuse.

Le canal d'annotation n'est pas un ornement : les journaux d'étape GitHub transitent
par Azure Blob, injoignables depuis l'environnement d'agent. L'annotation de check-run
est à ce jour le **seul** retour lisible du runner — donc chaque `--check` en pose une,
même en succès (trace de ce que la machine a vraiment produit).

Conformité avec E-21 : ce module grave et vérifie, mais **jamais dans la même
invocation**. `--write`/`--accepter` sont des actes d'assentiment, `--check` la
vérification ; la chaîne (Makefile, CI) appelle l'un ou l'autre, pas les deux.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = ROOT / "gouvernance" / "ARTIFACT_SIGNATURES.sha256"


# ── lecture / écriture du fichier de scellés, par sections ─────────────────────
def motif_section(marqueur: str) -> re.Pattern[str]:
    """De `# === MARQUEUR ===` jusqu'à la section suivante (ou la fin du fichier)."""
    return re.compile(rf"\n?# === {re.escape(marqueur)} ===.*?(?=\n# =|\Z)", re.DOTALL)


def lire_variantes(marqueur: str, prefixe: str) -> dict[str, str]:
    """Variantes gravées pour une section : {étiquette: charge}. Vide si absente."""
    if not STAMP.is_file():
        return {}
    m = motif_section(marqueur).search(STAMP.read_text(encoding="utf-8"))
    if not m:
        return {}
    motif = re.compile(rf"^{re.escape(prefixe)}_variante_([\w.-]+) = (\S+)$", re.M)
    return {x.group(1): x.group(2) for x in motif.finditer(m.group(0))}


def tete_de_contrat(variantes: dict[str, str]) -> str:
    """SHA-256 de l'ensemble trié des charges : la valeur à une ligne du contrat."""
    return hashlib.sha256("|".join(sorted(variantes.values())).encode()).hexdigest()


def graver_variantes(marqueur: str, prefixe: str, entete: str,
                     variantes: dict[str, str], ligne_tete: str | None = None) -> None:
    """Réécrit **une** section du scellé, en préservant byte pour byte les autres."""
    existing = STAMP.read_text(encoding="utf-8") if STAMP.is_file() else ""
    existing = motif_section(marqueur).sub("", existing).rstrip() + "\n"
    tete = ligne_tete or f"{prefixe}_lot"
    lignes = [f"{tete} = {tete_de_contrat(variantes)}"]
    lignes += [f"{prefixe}_variante_{et} = {variantes[et]}" for et in sorted(variantes)]
    STAMP.write_text(existing + f"\n# === {marqueur} ===\n{entete}" + "\n".join(lignes) + "\n",
                     encoding="utf-8")


# ── diagnostic ────────────────────────────────────────────────────────────────
def annoter(niveau: str, titre: str, message: str) -> None:
    """Annotation de workflow lisible via l'API Checks (`::notice` / `::error`)."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        safe = message.replace("\n", " ").replace("\r", " ")
        print(f"::{niveau} title={titre}::{safe}")


def comparer_composantes(courante: str, acceptees: dict[str, str]) -> str:
    """Dit **quelle** composante de la charge a bougé, par rapport à la plus proche.

    Les charges sont des `cle:valeur` séparés par `|` : la composante fautive est
    celle qui diffère en premier auprès du voisin le plus proche. C'est ce qui permet
    de trancher en un coup d'œil « bruit de rendu » (une composante de pixels) vs
    « dérive de contenu » (la composante structurelle, ou plusieurs à la fois).
    """
    if not acceptees:
        return "aucune variante gravée"
    cle_courantes = dict(p.split(":", 1) for p in courante.split("|") if ":" in p)
    meilleur = None
    for etiquette, charge in sorted(acceptees.items()):
        cle_v = dict(p.split(":", 1) for p in charge.split("|") if ":" in p)
        ecarts = [k for k in cle_courantes if cle_v.get(k) != cle_courantes[k]]
        if meilleur is None or len(ecarts) < len(meilleur[1]):
            meilleur = (etiquette, ecarts)
    etiquette, ecarts = meilleur  # type: ignore[misc]
    if not ecarts:
        return f"identique à « {etiquette} »"
    return (f"diverge de « {etiquette} » sur {len(ecarts)} composante(s) : "
            + ", ".join(f"{k}={cle_courantes[k]}" for k in ecarts))


class Sceau:
    """Pilote de CLI pour un artéfact scellé par variantes acceptées.

    Un artéfact fournit : sa marque de section, son préfixe de lignes, l'en-tête
    documentaire gravé avec le scellé, la forme valide d'une charge, et deux
    fonctions — `charge()` (la valeur sémantique courante, `None` si l'artéfact
    est absent) et `diagnostic()` (texte lisible pour l'annotation d'échec).
    """

    def __init__(self, marqueur: str, prefixe: str, entete: str, motif: str,
                  charge, diagnostic=None, ligne_tete: str | None = None,
                  defaut_variante: str = "reference-locale", libelle: str = ""):
        self.marqueur = marqueur
        self.prefixe = prefixe
        self.entete = entete
        self.motif = re.compile(motif)
        self.charge = charge
        self.diagnostic = diagnostic or (lambda: "")
        self.ligne_tete = ligne_tete
        self.defaut_variante = defaut_variante
        self.libelle = libelle or marqueur.lower()

    # -- le vif : une seule famille d'actes, quatre entrées -------------------
    def main(self, argv: list[str] | None = None, descriptif: str = "") -> int:
        parser = argparse.ArgumentParser(description=descriptif or __doc__.splitlines()[0])
        parser.add_argument("--write", action="store_true",
                            help="(re)grave la charge courante sous --variante")
        parser.add_argument("--variante", default=self.defaut_variante,
                            help=f"étiquette de la variante gravée par --write "
                                 f"(défaut : {self.defaut_variante})")
        parser.add_argument("--accepter", nargs=2, metavar=("CHARGE", "ÉTIQUETTE"),
                            help="grave une charge observée ailleurs (ex. annotation CI)")
        parser.add_argument("--check", action="store_true",
                            help="échoue si la charge courante n'est pas gravée")
        args = parser.parse_args(argv)

        courante = self.charge()
        variantes = lire_variantes(self.marqueur, self.prefixe)

        if args.write:
            if courante is None:
                print(f"artéfact indisponible pour {self.libelle} — rien à graver")
                return 1
            variantes[args.variante] = courante
            graver_variantes(self.marqueur, self.prefixe, self.entete, variantes,
                             self.ligne_tete)
            print(f"Empreinte {self.libelle} gravée dans {STAMP.relative_to(ROOT)} :")
            print(f"  variante « {args.variante} » = {courante}")
            print(f"  tête de contrat : {tete_de_contrat(variantes)}")
            print(f"  ensemble accepté : {sorted(variantes)}")
            return 0

        if args.accepter:
            charge, etiquette = args.accepter
            if not self.motif.fullmatch(charge):
                print(f"charge invalide : {charge!r}")
                print(f"forme attendue : {self.motif.pattern}")
                return 1
            variantes[etiquette] = charge
            graver_variantes(self.marqueur, self.prefixe, self.entete, variantes,
                             self.ligne_tete)
            connue = ("— c'est la charge courante" if courante == charge
                      else "(différente de la charge courante : normal si gravée "
                           "depuis un autre environnement)")
            print(f"Variante « {etiquette} » acceptée {connue} :")
            print(f"  {charge}")
            print(f"  tête de contrat : {tete_de_contrat(variantes)}")
            print(f"  ensemble accepté : {sorted(variantes)}")
            return 0

        if args.check:
            if courante is None:
                print(f"artéfact indisponible pour {self.libelle} — le contrôle ne peut rien dire")
                return 1
            if not variantes:
                print(f"aucune variante gravée pour {self.libelle} : "
                      f"lancer `python sources/empreinte_{self.prefixe}.py --write`")
                return 1
            connues = {v: k for k, v in variantes.items()}
            annoter("notice", f"empreinte-{self.prefixe}",
                    f"charge={courante} connue={connues.get(courante, 'NON')}")
            if courante in connues:
                print(f"{self.libelle} — conforme à la variante "
                      f"« {connues[courante]} » ({courante})")
                return 0
            detail = self.diagnostic()
            verdict = comparer_composantes(courante, variantes)
            print(f"{self.libelle} — charge inédite, hors ensemble accepté.")
            print(f"  produite  : {courante}")
            print("  acceptées :")
            for etiquette in sorted(variantes):
                print(f"    « {etiquette} » = {variantes[etiquette]}")
            if detail:
                print(f"  détail : {detail}")
            annoter("error", f"empreinte-{self.prefixe}-divergence",
                    f"charge_inedite={courante} | {verdict} | acceptees={sorted(variantes)} | "
                    f"détail={detail or 'aucun'} | pour accepter après revue : "
                    f"python sources/empreinte_{self.prefixe}.py --accepter '{courante}' <etiquette>")
            print()
            print("Rendu légitime d'un nouvel environnement ? Lire la comparaison")
            print("ci-dessous, puis accepter explicitement la charge dans le scellé.")
            print("Dérive de contenu ? Corriger la source, régénérer, re-graver,")
            print("et le dire à l'Avis.")
            # La dernière ligne imprimée est la plus lisible : c'est elle que la
            # batterie rapporte quand elle consigne QUI a refusé (test_mutations.courir).
            print(f"  {verdict}")
            return 1

        print(f"{self.libelle} :")
        print(f"  charge courante : {courante or 'indisponible'}")
        if courante is not None:
            connues = {v: k for k, v in variantes.items()}
            statut = f"connue (« {connues[courante]} »)" if courante in connues \
                     else "INÉDITE — non gravée"
            print(f"  statut : {statut}")
        print(f"  ensemble accepté ({len(variantes)}) :")
        for etiquette in sorted(variantes):
            print(f"    « {etiquette} » = {variantes[etiquette]}")
        return 0


def sha256(chemin: Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()
