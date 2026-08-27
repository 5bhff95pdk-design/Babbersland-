# 🗺️ ROADMAP GÉOGRAPHIQUE — ROYAUME DU BABBERLAND

**Référence** : RM-GEO-2026-II · feuille de route du ticket R2.6
**Établie le** : 27 août 2026
**Règle d'autorité** : rien de ceci n'entre dans 2026-I sans Avis du Grand Argentier
**Dépendance** : R2.6 était rangé à l'horizon 2 de `ROADMAP_2026_II.md` (« rien de H2 avant la fin de H1 »). L'atlas est donc **livré en proposition**, comme les Chroniques : il n'ouvre pas le canon, il ne casse pas l'emballage.

---

## Vue d'ensemble

```
G0  LIVRÉ CE JOUR          G1  INDUSTRIALISER         G2  DÉCRÉTER              G3  HABITER
atlas + analyse + contrôles  (avec H1, pas avant)      un Avis, pas une PR        le territoire
─────────────────────────  ──────────────────────     ─────────────────────      ────────────────
G0.1 gazetteer Python      G1.1 carte dans `make tout` G2.1 Avis n° 7             G3.1 cadastre des
G0.2 SVG temporel          G1.2 PNG déterministe          (démographie 7 000)         établissements
G0.3 PNG 2026                  comparé en CI            G2.2 Livre I : un            McBabber's
G0.4 atlas HTML            G1.3 parité SVG/HTML           paragraphe + carte      G3.2 temps de marche
G0.5 check_geography.py    G1.4 toponymes proposés      G2.3 chronologie :            au pas
G0.6 ANALYSE.md                gelés ou retirés           dates géographiques     G3.3 Livre II des
                                                                              Chroniques (aqueduc
                                                                              vu du terrain)
```

---

## G0 — Ce qui est livré (27 août 2026)

| ID | Livrable | Où | Statut |
|---|---|---|---|
| **G0.1** | Gazetteer unique (régions, lieux, hydro, routes, époques, populations) | `sources/geographie.py` | ✅ |
| **G0.2** | Carte SVG à couches `data-since` / `data-until` | `sources/carte_royaume.svg` | ✅ |
| **G0.3** | PNG 2026, cadre parchemin, graine 1847 | `geographie/carte_royaume.png` | ✅ |
| **G0.4** | Atlas interactif (curseur 1830–2026, lecture du temps, 5 régions) | `geographie/index.html` | ✅ |
| **G0.5** | Contrôle de non-contradiction avec 2026-I | `sources/check_geography.py` | ✅ |
| **G0.6** | Analyse : ce que le canon sait, ce que le temps interdit, E-16.c fermé *en proposition* | `geographie/ANALYSE.md` | ✅ |

**Fait le jour où** : `python sources/check_geography.py` est vert, l'atlas montre les Monts absents en 1961 et présents le 15 juillet 1962, et 2026-I n'a **pas** bougé.

---

## G1 — Industrialiser (après Horizon 1, ou avec)

> Même exigence que l'arbre : une source, un artéfact comparable, une CI qui voit l'oubli.

| ID | Ticket | Détail | Effort | Dépend de |
|---|---|---|---|---|
| **G1.1** | `make carte` dans la chaîne | Cible déjà posée. L'ajouter à `make tout` seulement quand H1 aura fini de verrouiller le PDF : une carte nouvelle ne doit pas faire dériver l'empreinte sémantique. | 5 min | R1.1 |
| **G1.2** | PNG au bit près en CI | Comme l'arbre : régénérer et `git diff --exit-code geographie/carte_royaume.png`. | 15 min | G0.3, R0.4 |
| **G1.3** | Une seule géométrie | Aujourd'hui le SVG (couches) et le PNG (état 2026) partagent `geographie.py` mais redessinent. Extraire les polygones une fois. C'est E-15 transposé à la carte. | 2 h | G0.2 |
| **G1.4** | Gel des toponymes proposés | *Fjord des Fûts*, *Baie du Chanvre*, *Chemin du Pas*, *Route des Péniches*, *Route du Chanvre* : soit Avis qui les nomme, soit les retirer de la carte imprimée et les laisser dans l'atlas annoté « proposé ». Ne pas les laisser flotter. | 30 min | G2.1 |

---

## G2 — Décréter (matière nouvelle, un Avis)

> Objectif : que le Livre I cesse de citer cinq régions sans les situer, **sans** avaler la chronique.

| ID | Ticket | Contenu | Arbitrage requis |
|---|---|---|---|
| **G2.1** | **Avis n° 7 — Recensement de la Nuit des Sept Mille** | Fixer (ou prêter au silence) le total 7 000. Recommandation : 5 500 urbains (déjà canon) + 1 500 forestiers + 0 alpin = 7 000, et le double cornichon comme signe de prospérité, pas comme 7 001ᵉ âme. | **oui** : tonalité (blague de registre vs recensement sérieux) |
| **G2.2** | **Livre I, un alinéa + la carte** | Après « Les cinq régions », un court paragraphe d'orientation (nord = fleuve, sud = forêt, monts = jardin, 1962) et l'ancre d'illustration `images/carte_royaume.png`. **Hors-PDF tant que l'Avis n'est pas signé.** | oui : la carte entre-t-elle dans le volume ? |
| **G2.3** | **Chronologie, dates géographiques** | 1880 Pabst City (chronique), 1869 premier quai, 1916 phare : n'entrer qu'une fois distingué le canon de la chronique. Ne pas rétro-décréter 1880. | oui : 1880 est-il ratifié ? |
| **G2.4** | **Ne pas créer un Livre VIII de la géographie** | La géographie est le Livre I. Un huitième livre est déjà promis aux Institutions (R2.1). Deux livres pour cinq régions, ce serait courir. | — |

**Ne pas faire en G2** : nommer les deux sommets, chiffrer des km², inventer une mer, poser un château pour le Déchiré, dater Grass City avant 1920.

---

## G3 — Habiter (après décret, ou jamais)

| ID | Action | Intérêt | Effort |
|---|---|---|---|
| **G3.1** | Cadastre des McBabber's | Le canon parle d'« chaque établissement » au pluriel, d'un « établissement périphérique » (faux fromage, 2018) et du premier, face au Palais. Deux points suffisent ; une chaîne, non. | 0,5 j |
| **G3.2** | Temps de marche au pas | Table : cabane → capitale, capitale → port, capitale → Grass City, ascension des Monts (4 s). Un Royaume qu'on mesure en siestes. | 0,5 j |
| **G3.3** | Chroniques Livre II, *vu du terrain* | L'aqueduc de 1892–1914 est le prochain livre annoncé. S'il se écrit, il doit pouvoir se marcher sur cette carte (bancs, 2 km, Traité de la Digue) sans la déplacer. | avec R2.8 |
| **G3.4** | Carte dans le site de lecture | R3.1 (GitHub Pages) : l'atlas *est* déjà une page autonome. L'y brancher. | 15 min |

---

## Indicateurs

| Indicateur | Avant G0 | Après G0 | Après G2 |
|---|---|---|---|
| Régions situées sur une carte | 0 / 5 | **5 / 5** (proposé) | 5 / 5 (canon, si Avis) |
| Population nationale | 5 500 + 2 trous | 7 000 proposé, 5 500 canon | 0 trou, ou silence juré |
| Objets datés sur la carte | 0 | 19 époques, couches `data-since` | idem |
| Contradictions 1962 / 1847 / 1986 | impossibles à voir | **refusées par `check_geography.py`** | idem |
| 2026-I modifié | — | **non** | seulement par Avis |

---

## Ce qu'il ne faut pas faire

- **Ne pas glisser la carte dans `images/` et 2026-I** sans Avis : ce serait E-07 à l'envers (une planche que le canon n'a pas promise) *et* un décret déguisé.
- **Ne pas dessiner les Monts ailleurs que dans le jardin du Palais.** C'est la seule contrainte dure.
- **Ne pas peupler les Monts.** 22 guides alpins, ce serait une commune. Ils habitent déjà Pabst City.
- **Ne pas nommer une mer.** Grass City se baigne dans le fleuve, ou dans le silence.
- **Ne pas « corriger » 5 500.** Le canon a raison. 7 000 est une lecture de la Nuit, pas un démenti.

---

*Feuille de route géographique établie à Pabst City, le 27 août 2026.*
**« Une Pabst, une poutine, et on régénère — mais on ne décrète pas en marchant. »**
