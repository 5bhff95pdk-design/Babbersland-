#!/usr/bin/env python3
"""Gazetteer du Royaume du Babberland.

Statut éditorial : **proposé, non décrété**. Les faits marqués
``canon=True`` figurent dans l'Encyclopédie consolidée 2026-I (ou dans
la chronologie maîtresse, qui s'aligne sur elle). Tout le reste est
reconstruction géographique pour la carte : il ne contredit aucun point
de continuité, et n'en fixe aucun.

Coordonnées : pixels du canevas 1600×1100, nord en haut, même cadre
parchemin que l'arbre généalogique.
"""
from __future__ import annotations

from typing import Any

CANVAS = (1600, 1100)
STATUT = "proposé, non décrété"
EDITION = "Atlas temporel 2026-Géo · 27 août 2026"

# Échelle : le Double Aqueduc mesure 2 km dans la chronique (Livre I,
# tranche 6 — « une bière qui supporterait deux kilomètres de canal »).
# 170 px de canal → 85 px / km. Emprise du Royaume ≈ 10 km est-ouest,
# 8 km nord-sud.
PX_PER_KM = 85.0
AQUEDUC_KM = 2.0
EMPRISE_EO_KM = 10.0
EMPRISE_NS_KM = 8.0

# ── Régions (Livre I du canon : les cinq, dans cet ordre) ──────────────
REGIONS: list[dict[str, Any]] = [
    {
        "id": "pabst_city",
        "nom": "Pabst City",
        "rang": 1,
        "role": "Capitale",
        "population": 3500,
        "population_statut": "canon",
        "depuis": 1880,
        "canon": True,
        "xy": (730, 495),
        "resume": "Palais royal, Banque nationale, Double Aqueduc. "
                  "Réserves de fromage en grain et de boissons de cérémonie.",
        "source": "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md · Livre I · Les cinq régions",
    },
    {
        "id": "monts_froisses",
        "nom": "Les Monts Froissés",
        "rang": 2,
        "role": "Alpes nationales",
        "population": 0,
        "population_statut": "proposé",
        "depuis": 1962,
        "canon": True,
        "xy": (805, 448),
        "altitude_m": 1.20,
        "resume": "Deux tas de terre de 1,20 m, déblais de la piscine royale "
                  "creusée le 15 juillet 1962 dans le jardin du Palais. "
                  "Région pour le prestige ; géographiquement un massif de jardin. "
                  "Population permanente : nulle. Population transitoire : deux, "
                  "le temps de quatre secondes.",
        "source": "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md · Livre I + Génération IV",
    },
    {
        "id": "port_babette",
        "nom": "Port Babette",
        "rang": 3,
        "role": "Ville portuaire",
        "population": 800,
        "population_statut": "canon",
        "depuis": 1869,
        "canon": True,
        "xy": (1245, 305),
        "resume": "800 âmes, nommée en l'honneur de Babette Ire. "
                  "Quais, phare blanc couronné et flottille de péniches "
                  "de curds et de fûts, œuvre de Babette-Marine.",
        "source": "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md · Livre I + Génération II",
    },
    {
        "id": "grass_city",
        "nom": "Grass City",
        "rang": 4,
        "role": "Station balnéaire",
        "population": 1200,
        "population_statut": "canon",
        "depuis": 1920,
        "canon": True,
        "xy": (295, 355),
        "resume": "1 200 habitants, station balnéaire et capitale du chanvre "
                  "légal. Fibres du papier fiduciaire Série B. Devise : « Pousse ».",
        "source": "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md · Livre I",
    },
    {
        "id": "foret_plantagenet",
        "nom": "Forêt de Plantagenet",
        "rang": 5,
        "role": "Sanctuaire de la fondation",
        "population": 1500,
        "population_statut": "proposé",
        "depuis": 1847,
        "canon": True,
        "xy": (700, 780),
        "resume": "Cabane de 1847, Chêne du Hamac royal, Nappe Sacrée. "
                  "Le Dénombrement de 1850 y comptait déjà le cœur du Royaume. "
                  "1 500 âmes proposées (cabane, Trois-Érables, hameau de la Digue, "
                  "érablières) pour totaliser les 7 000 de la Nuit des Sept Mille.",
        "source": "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md · Livre I ; chroniques (1850)",
    },
]

# Total proposé : 3 500 + 1 200 + 800 + 1 500 + 0 = 7 000.
POPULATION_URBAINE_CANON = 3500 + 1200 + 800  # 5 500
POPULATION_FOREST_PROPOSEE = 1500
POPULATION_MONTS_PROPOSEE = 0
POPULATION_TOTALE_PROPOSEE = 7000

# ── Lieux ponctuels ────────────────────────────────────────────────────
LIEUX: list[dict[str, Any]] = [
    {
        "id": "cabane_1847",
        "nom": "Cabane de 1847",
        "kind": "sanctuaire",
        "xy": (690, 800),
        "depuis": 1847,
        "canon": True,
        "note": "Toit du jour de la fondation. On refusa le mot « palais ».",
    },
    {
        "id": "chene_hamac",
        "nom": "Chêne du Hamac royal",
        "kind": "sanctuaire",
        "xy": (755, 755),
        "depuis": 0,
        "canon": True,
        "note": "Arbre remarquable antérieur au Royaume. Hamac suspendu en 1856 ; "
                "tombe de Babber Ier à son pied (automne 1889, chronique).",
    },
    {
        "id": "nappe",
        "nom": "Nappe Sacrée",
        "kind": "sanctuaire",
        "xy": (690, 800),
        "depuis": 1847,
        "canon": True,
        "note": "Conservée sous protection au sanctuaire. Pas un lieu distinct "
                "de la cabane : un objet-document.",
    },
    {
        "id": "grande_digue",
        "nom": "Grande Digue",
        "kind": "ouvrage",
        "xy": (725, 690),
        "depuis": 0,
        "canon": False,
        "note": "Barrage castoral sur le ruisseau Plantagenet. Traité de 1886 "
                "(chronique). Siège du Témoin royal adjoint.",
    },
    {
        "id": "trois_erables",
        "nom": "Colonie des Trois-Érables",
        "kind": "hameau",
        "xy": (1080, 845),
        "depuis": 0,
        "canon": False,
        "note": "Voisine d'avant le Royaume, érablières. Naissance d'Irène en 1882. "
                "Citoyens « depuis toujours » au recensement de 1860 (chronique).",
    },
    {
        "id": "champs_orge",
        "nom": "Champs d'orge du Grain",
        "kind": "culture",
        "xy": (430, 630),
        "depuis": 1840,
        "canon": False,
        "note": "Famille du Grain, 1840. Malterie d'Hortense. Origine de Pabst City.",
    },
    {
        "id": "malterie",
        "nom": "Malterie d'Hortense",
        "kind": "ouvrage",
        "xy": (480, 580),
        "depuis": 1864,
        "canon": False,
        "note": "Grande maîtrise de la malterie. Batch 47, 1885 : bière « qui tient "
                "dans le tuyau » (chronique).",
    },
    {
        "id": "douane",
        "nom": "Douane du bout du chemin",
        "kind": "ouvrage",
        "xy": (700, 625),
        "depuis": 1865,
        "canon": False,
        "note": "Entrée nord de la forêt. Délivre le laissez-aller (chronique).",
    },
    {
        "id": "palais",
        "nom": "Palais royal",
        "kind": "capitale",
        "xy": (730, 478),
        "depuis": 1892,
        "canon": True,
        "note": "Siège de la Couronne à Pabst City. Jardin : piscine et Monts Froissés. "
                "Date de construction non consignée ; la carte l'affiche dès le règne "
                "des Bâtisseurs.",
    },
    {
        "id": "banque",
        "nom": "Banque nationale",
        "kind": "capitale",
        "xy": (690, 510),
        "depuis": 1892,
        "canon": True,
        "note": "Cité au Livre I, jamais décrite (lacune R2.1). Point sur la carte, "
                "pas un plan.",
    },
    {
        "id": "aqueduc",
        "nom": "Double Aqueduc",
        "kind": "ouvrage",
        "xy": (730, 590),
        "depuis": 1882,
        "canon": True,
        "note": "Plans 1882, chantier 1892–1914, deux canaux (eau pure / Pabst fraîche), "
                "≈ 2 km. Bancs imposés par l'Ancien : « un canal où l'on ne peut "
                "s'asseoir n'est qu'un tuyau » (chronique).",
    },
    {
        "id": "piscine",
        "nom": "Piscine royale",
        "kind": "capitale",
        "xy": (785, 458),
        "depuis": 1962,
        "canon": True,
        "note": "Creusée le 15 juillet 1962. Babber II meurt en 2002 dans un transat "
                "face à elle.",
    },
    {
        "id": "mcbabbers",
        "nom": "McBabber's (premier)",
        "kind": "capitale",
        "xy": (730, 545),
        "depuis": 1986,
        "canon": True,
        "note": "Entrée de Pabst City, face au Palais. Terrain refusé aux arches "
                "dorées au printemps 1984 ; ruban coupé le 1er avril 1986 à 15 h 01.",
    },
    {
        "id": "phare",
        "nom": "Phare blanc couronné",
        "kind": "port",
        "xy": (1335, 225),
        "depuis": 1916,
        "canon": True,
        "note": "Érigé par Babette-Marine ; elle le laisse à sa mort en 1916.",
    },
    {
        "id": "quais",
        "nom": "Quais de Port Babette",
        "kind": "port",
        "xy": (1245, 320),
        "depuis": 1869,
        "canon": True,
        "note": "Première barge 1869 (chronique) ; port moderne achevé avant 1916.",
    },
    {
        "id": "fjord",
        "nom": "Fjord des Fûts",
        "kind": "hydro",
        "xy": (1320, 175),
        "depuis": 0,
        "canon": False,
        "note": "Nom proposé. Le titre « Rambo du Fjord » (né le 15 juillet 1962) "
                "implique un fjord ; le canon ne le localise pas. Place : débouché "
                "nord-est du Fleuve Babber, rapides gardés contre les fûts tièdes.",
    },
    {
        "id": "baie_chanvre",
        "nom": "Baie du Chanvre",
        "kind": "hydro",
        "xy": (250, 310),
        "depuis": 0,
        "canon": False,
        "note": "Nom proposé. Grass City est station balnéaire : la carte lui donne "
                "une anse sableuse du Fleuve, terrasses de chanvre au-dessus.",
    },
    {
        "id": "clairiere",
        "nom": "Clairière Plantagenet",
        "kind": "hameau",
        "xy": (640, 720),
        "depuis": 1830,
        "canon": False,
        "note": "Lisière nord de la forêt, 1830. Table et nappe vichy. Chronique.",
    },
]

HYDRO: list[dict[str, Any]] = [
    {
        "id": "fleuve_babber",
        "nom": "Fleuve Babber",
        "nom_ancien": "la grande eau",
        "renomme": 1847,
        "canon": True,
        "note": "Canon : péniches de curds et de fûts ; Rambo, prince du Fleuve. "
                "Chronique : au nord de la forêt, encore sans nom en 1836.",
    },
    {
        "id": "ruisseau_plantagenet",
        "nom": "Ruisseau Plantagenet",
        "canon": False,
        "note": "Affluent méridional, grande digue castorale. Chronique.",
    },
]

ROUTES: list[dict[str, Any]] = [
    {
        "id": "chemin_du_pas",
        "nom": "Chemin du Pas",
        "de": "cabane_1847",
        "a": "pabst_city",
        "canon": False,
        "note": "Forêt → capitale. On n'y court pas.",
    },
    {
        "id": "route_peniches",
        "nom": "Route des Péniches",
        "de": "pabst_city",
        "a": "port_babette",
        "canon": False,
        "note": "Capitale → port. Le chargement de cornichons de 2007 y fut "
                "retenu pour excès de croquant.",
    },
    {
        "id": "route_chanvre",
        "nom": "Route du Chanvre",
        "de": "pabst_city",
        "a": "grass_city",
        "canon": False,
        "note": "Capitale → station balnéaire.",
    },
]

# Seuils temporels de la carte (année → ce qui change).
EPOCHS: list[dict[str, Any]] = [
    {
        "annee": 1830,
        "titre": "La lisière",
        "canon": False,
        "fait": "La famille Plantagenet défriche une clairière au nord de la forêt.",
    },
    {
        "annee": 1840,
        "titre": "L'orge",
        "canon": False,
        "fait": "Les du Grain sèment. La malterie commencera ici.",
    },
    {
        "annee": 1847,
        "titre": "Fondation",
        "canon": True,
        "fait": "12 octobre · Constitution sur la Nappe Sacrée. Cabane, Royaume, "
                "frontières « jusqu'où porte la voix pour le souper » (chronique).",
    },
    {
        "annee": 1850,
        "titre": "Dénombrement de la sieste",
        "canon": False,
        "fait": "214 humains comptés à 14 h (chronique, registre C-4).",
    },
    {
        "annee": 1852,
        "titre": "« Ici, un port. Un jour. »",
        "canon": False,
        "fait": "Babette-Marine, 16 ans, esquisse la rive nord.",
    },
    {
        "annee": 1856,
        "titre": "Le hamac",
        "canon": False,
        "fait": "Suspendu au chêne ; il attendra 58 ans son maître.",
    },
    {
        "annee": 1865,
        "titre": "La douane",
        "canon": False,
        "fait": "Poste du laissez-aller, entrée nord de la forêt.",
    },
    {
        "annee": 1869,
        "titre": "Le quai avant le port",
        "canon": False,
        "fait": "Première barge de curds et de fûts. Le quai croit au port.",
    },
    {
        "annee": 1880,
        "titre": "Pabst City",
        "canon": False,
        "fait": "Le hameau des brasseurs prend son nom. « On dit Pabst City depuis "
                "un bout. Autant l'écrire. »",
    },
    {
        "annee": 1882,
        "titre": "Plans du Double Aqueduc",
        "canon": True,
        "fait": "Deux sillons, prince et ingénieur. On ne creuse pas encore.",
    },
    {
        "annee": 1892,
        "titre": "Les Bâtisseurs",
        "canon": True,
        "fait": "Avènement de François-Babber. Le chantier de l'aqueduc s'ouvre. "
                "Palais (proposé).",
    },
    {
        "annee": 1914,
        "titre": "Aqueduc en service",
        "canon": True,
        "fait": "Fin du règne de l'Aqueducien. Les deux canaux coulent.",
    },
    {
        "annee": 1916,
        "titre": "Port moderne",
        "canon": True,
        "fait": "Mort de Babette-Marine. Elle laisse quais, phare et flottille.",
    },
    {
        "annee": 1920,
        "titre": "Grass City attestée",
        "canon": True,
        "fait": "Naissance de Colette-Pabst de Grass City : première date canonique "
                "qui nomme la ville. La station existait ; on ne sait pas depuis quand.",
    },
    {
        "annee": 1962,
        "titre": "Ère géologique",
        "canon": True,
        "fait": "15 juillet · piscine, Monts Froissés (1,20 m), naissance de "
                "Rambo du Fjord.",
    },
    {
        "annee": 1984,
        "titre": "Station de repos",
        "canon": True,
        "fait": "Terrain face au Palais rendu à la Couronne. Trois rocking-chairs.",
    },
    {
        "annee": 1986,
        "titre": "McBabber's",
        "canon": True,
        "fait": "1er avril, 15 h 01. L'enseigne s'ouvre à l'entrée de Pabst City.",
    },
    {
        "annee": 2007,
        "titre": "Guerre des Cornichons",
        "canon": True,
        "fait": "Chargement retenu « à la frontière » — limite interne entre "
                "maraîchers de Port Babette et cuisines de la capitale.",
    },
    {
        "annee": 2026,
        "titre": "Aujourd'hui",
        "canon": True,
        "fait": "Sept générations, cinq régions, 5 500 âmes urbaines canoniques, "
                "7 000 mini-McLouches. L'atlas propose 7 000 âmes en tout.",
    },
]


def region_by_id(rid: str) -> dict[str, Any]:
    for row in REGIONS:
        if row["id"] == rid:
            return row
    raise KeyError(rid)


def visible(feature: dict[str, Any], year: int) -> bool:
    """True si le lieu existe à l'année donnée (depuis 0 = toujours)."""
    return int(feature.get("depuis", 0) or 0) <= year


def population_en(year: int) -> dict[str, int | str]:
    """Effectifs affichés à une date. Avant 2026, seuls 1850 et 2026 sont chiffrés."""
    if year < 1850:
        return {"total": "non dénombré", "detail": "avant le Dénombrement de la sieste"}
    if year == 1850 or year < 1880:
        return {"total": 214, "detail": "Dénombrement de 1850 (chronique, proposé)"}
    if year < 2026:
        return {
            "total": "croissant",
            "detail": "214 (1850) → 7 000 (2026, proposé) · pas de recensement intermédiaire",
        }
    return {
        "total": POPULATION_TOTALE_PROPOSEE,
        "urbain_canon": POPULATION_URBAINE_CANON,
        "foret_proposee": POPULATION_FOREST_PROPOSEE,
        "monts": POPULATION_MONTS_PROPOSEE,
        "detail": "3 500 + 1 200 + 800 + 1 500 + 0 = 7 000",
    }
