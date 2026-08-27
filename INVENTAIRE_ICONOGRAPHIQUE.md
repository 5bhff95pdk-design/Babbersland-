# Inventaire iconographique du Royaume du Babberland

**Date** : 27 août 2026 · Campagne 2026-II  
**Référentiel** : `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md` et table `IMAGE_AFTER`

---

## Vue d’ensemble

| Mesure | Valeur |
|---|---|
| PNG dans `images/` | **24** (14 d’origine + 10 portraits dynastiques 2026-II) |
| Orphelins / manquants | aucun |
| Source vectorielle | `sources/arbre_genealogique_complet.svg` |
| Couverture PDF | les 24 fichiers sont servis |

Deux familles techniques :

1. **Arbre généalogique** — Pillow déterministe, 1600×1000, ~124 Kio.
2. **Portraits et scènes** — PNG RVB 8 bits, ~2,3–2,9 Mio, 72 dpi.

---

## Table-mère

### Dossier d’origine (14)

| Fichier | Sujet | Catégorie |
|---|---|---|
| `arbre_genealogique_complet.png` | Maison royale, 7 générations | Schéma |
| `hortense_du_grain.png` | Hortense du Grain | Portrait |
| `babette_marine.png` | Babette-Marine | Portrait |
| `irene_des_erables.png` | Irène des Érables | Portrait |
| `babber_le_dechire.png` | Prince le Déchiré | Portrait |
| `ginette_de_port_babette.png` | Princesse Ginette | Portrait |
| `roger_bontemps.png` | Grand Bouffon | Portrait |
| `ti_babber_generation_7.png` | Ti-Babber | Portrait |
| `mcbabbers_enseigne_royale.png` | Premier McBabber’s | Scène |
| `mcbabbers_menu_pabst.png` | Menu royal | Document |
| `babbersgate_scandale_sauce.png` | Commission 1991 | Scène |
| `pieces_monnaie_babberland_coffret.png` | Coffret Proof 2026 | Numismatique |
| `piece_1_babber_or_avers_revers.png` | 1 Babber bimétallique | Numismatique |
| `pieces_babetons_divisionnaires.png` | 1 / 6 / 12 Babetons | Numismatique |

### Galerie 2026-II (10)

| Fichier | Sujet |
|---|---|
| `babber_ier_ancien.png` | Fondateur, nappe vichy et castor patriote |
| `babette_ire_plantagenet.png` | Reine fondatrice, nappe sacrée |
| `francois_babber_aqueducien.png` | Double Aqueduc, circlet d’ingénieur |
| `babber_le_dormeur.png` | Hamac d’État, couronne penchée |
| `babber_ii_piscineux.png` | Piscine, pelleteuse, Monts Froissés |
| `honore_pabst_henri_grain.png` | Union des Règnes : l’un signe, l’autre dort |
| `babber_ier_le_louche.png` | Roi régnant, béret couronné, louche d’or |
| `linea_de_grass_city.png` | Chanvre, papier fiduciaire, première sauce |
| `rambo_du_fjord.png` | Prince du Fleuve, canoe, fûts glacés |
| `babber_le_fou.png` | Héritier, Aspirateur-Couronne, Ballon Jaune Ier |

Colette-Pabst n’a pas encore de portrait dédié (elle apparaît dans le Babbersgate).

---

## Constats sur le dossier d’origine

Les **portraits d’attributs** (louches de Ginette, phare de Babette-Marine, sirop d’Irène, pouce du Déchiré, vin de Roger) collent au canon. Défauts restants, non bloquants :

| Id | Fichier | Écart |
|---|---|---|
| I-01 | `mcbabbers_enseigne_royale.png` | Graphie *McBABBBER’S* (B en trop) |
| I-03 | `mcbabbers_menu_pabst.png` | Légendes génératives (*raevas*, *Pabstus Rex*) |
| I-05 | `roger_bontemps.png` | Cartouche *GRANO BOUFFON* |
| I-06 | `pieces_monnaie_babberland_coffret.png` | Légende *ESHFTY* ; coins discordants avec la macro |
| I-11 | `babbersgate_scandale_sauce.png` | Cadre médiéval, dollars US, Louche déjà couronné en 1991 |

Hortense, Irène et Babette-Marine partagent encore un gabarit facial proche.

---

## Chaîne

Toute référence `` `images/…` `` du Markdown 2026-I est ancrée dans `IMAGE_AFTER` (ou l’arbre, inséré sur le schéma généalogique).  
`make controle` vérifie présence et couverture ; il ne lit pas le contenu sémantique des peintures.
