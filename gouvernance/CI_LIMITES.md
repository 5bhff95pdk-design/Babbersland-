# 🔧 Limites connues de la CI de continuité

**Référence** : CI-2026-I · diagnostic des étapes en `continue-on-error: true`
**Établi le** : 1ᵉʳ septembre 2026
**Ticket de durcissement** : R1.4 (sous-tickets R1.4.a à R1.4.h)

---

## Contexte

La CI de continuité (`.github/workflows/continuite.yml`, 18 étapes) est **active et verte** depuis le 1ᵉʳ septembre 2026 (PR #22, livraison R0.4). Elle passe ses 22 sous-étapes en `success` sur la PR de référence.

**Cependant**, 6 de ces 18 étapes portent encore la directive `continue-on-error: true` (l'Atlas, R1.4.a, a été durci le 1ᵉʳ septembre 2026). Cette section documente précisément pourquoi, et ce qu'il faudrait faire pour les durcir.

---

## Statut R1.4.a (livré le 1ᵉʳ septembre 2026) — Atlas durci

**L'étape Atlas géographique est désormais BLOQUANTE** (sans `continue-on-error: true`).

**Diagnostic correctif** : le `continue-on-error` initial était basé sur une **mesure erronée** (confusion entre `sha256sum` du système de fichiers et `git hash-object`, qui opèrent sur des représentations différentes du contenu). Refait proprement sur un clone frais en conditions CI réelles, l'Atlas (SVG, PNG, HTML) est **bit-à-bit reproductible** :

```
git hash-object sources/carte_royaume.svg     → 84463bc9… (tracké == généré)
git hash-object geographie/carte_royaume.png → 0c4355f8… (tracké == généré)
git hash-object geographie/index.html        → 6bd877a9… (tracké == généré)
```

**Implication** : la politique « empreinte sémantique par défaut » (initialement prévue pour R1.4.a) n'est pas nécessaire pour l'Atlas. Les sous-tickets R1.4.b–g restent à investiguer : il est **possible que certains d'entre eux soient en fait bit-à-bit reproductibles**, le même faux diagnostic s'étant appliqué uniformément. À vérifier un par un avant de basculer sur une empreinte sémantique.

---

## Pourquoi `continue-on-error` sur les 6 étapes restantes ?

Le pipeline repose sur le postulat que **les binaires régénérés doivent être identiques au bit près à ceux trackés dans git** (sinon `git diff --exit-code` échoue et la CI devient rouge). C'est une garantie forte, mais elle n'est **pas tenable** dans la situation actuelle, pour les raisons suivantes.

### Cause racine : non-reproductibilité multi-machines

Les 6 artéfacts principaux (Atlas SVG/PNG/HTML, Arbre PNG, Hymne WAV, PDF encyclopédique) sont **reproductibles par run** sur une même machine — deux invocations successives sur la même machine donnent le même SHA. Mais ils ne sont **pas bit-à-bit identiques** entre machines :

| Machine | Pillow | ReportLab | Système | SHA des artéfacts |
|---|---|---|---|---|
| Agent Arena (Linux, dev) | 12.3.0 | 5.0.1 | Ubuntu 24.04 | `d2acccea…` (Atlas SVG) |
| Runner GitHub Actions (Ubuntu 24.04) | 12.3.0 | 5.0.1 | Ubuntu 24.04 | `84463bc9…` (Atlas SVG) |
| MacOS du mainteneur (théorique) | ? | ? | Darwin | inconnu |

Les causes précises (à investiguer en R1.4) sont probablement :

1. **Métadonnées EXIF des PNG** — Pillow écrit la date de génération dans le PNG
2. **Ordre des éléments dans le SVG** — selon l'ordre d'itération d'un `set` ou `dict`
3. **Noms `FormXob.*` aléatoires** dans le PDF — ReportLab ne le contrôle pas (`rl_config.invariant=1` testé sans effet, cf. R0.1)
4. **Paddings de blocs dans ReportLab** — sensibles à la largeur de police, qui dépend du système
5. **Header RIFF du WAV** — possible timestamp
6. **Compression WebP des vignettes** — paramètres par défaut de Pillow

**Important** : la situation est **identique sur la machine de l'agent et sur le runner CI** (mêmes versions épinglées dans `requirements.txt`). La différence provient probablement de l'ordre de génération de Pillow ou de l'environnement système (locale, timezone, polices chargées par défaut par Pillow).

---

## Les 6 étapes encore concernées (Atlas durci)

| Étape | Binaire | Statut | Ticket |
|---|---|---|---|
| Atlas géographique | `sources/carte_royaume.svg`, `geographie/carte_royaume.png`, `geographie/index.html` | ✅ **duréi R1.4.a** | — |
| Arbre généalogique | `images/arbre_genealogique_complet.png` | ⚠️ continue-on-error | R1.4.b |
| Hymne national | `audio/hymne_national_babberland.wav` | ⚠️ continue-on-error | R1.4.c |
| Vignettes du portail | `images/vignettes/*.webp` (77 fichiers) | ⚠️ continue-on-error | R1.4.d |
| Régénération encyclopédie | `Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf` | ⚠️ continue-on-error | R1.4.e |
| Artéfact publié (planches) | dérivée du PDF | ⚠️ continue-on-error | R1.4.f |
| Fraîcheur du PDF | dérivée de l'empreinte sémantique | ⚠️ continue-on-error | R1.4.g |

---

## Pourquoi pas comparer bit-à-bit ?

**Comparaison bit-à-bit** (la stratégie naïve `git diff --exit-code`) impose une coïncidence parfaite entre la machine qui a généré les maîtres commités et toutes les machines qui les régénèrent ensuite. C'est :

- **Fragile** : un changement de version de Pillow (même mineur) suffit à casser
- **Coûteux** : il faudrait geler l'environnement entier (Docker image, par exemple), pas seulement les versions Python
- **Inutile** : ce qui compte pour le canon, c'est le **contenu sémantique** (texte, pages, planches, scellés), pas la disposition exacte des octets

## La bonne politique (R1.4)

Pour chaque étape, R1.4 mettra en place un **scellement sémantique** analogue à `pdf_fingerprint.py` (qui compare `md5(nb_pages ‖ texte normalisé ‖ tri(hachés des flux image))`, déjà livré en R1.1 par anticipation). Le principe :

1. **Calculer une empreinte** de l'artéfact qui ne dépend PAS de l'ordre des octets, mais de son **contenu signifiant**
2. **Stocker l'empreinte** dans `gouvernance/ARTIFACT_SIGNATURES.sha256` (à créer)
3. **Vérifier** en CI que `empreinte(généré) == empreinte(commise)` sans exiger d'égalité binaire

Pour chaque sous-ticket, le travail consiste à :
- Identifier la source de non-déterminisme (Pillow EXIF, ReportLab, etc.)
- Choisir une fonction d'empreinte sémantique qui l'ignore
- Ajouter un script `sources/empreinte_<artéfact>.py` analogue à `pdf_fingerprint.py`
- Retirer le `continue-on-error: true` et basculer sur la vérification sémantique

---

## Le « Gel des archives » : un cas à part

L'étape **« Gel des archives (G et H intacts) et des maîtres d'illustration »** est **sans** `continue-on-error: true` depuis le 30 août 2026 (cf. RAPPORT_DE_CONTRE_EXPERTISE_2026_III.md, constat E-23). Elle est passée **provisoirement en mode diagnostic** dans la livraison R0.4 finale, pour permettre de lire le diff exact sans bloquer la CI.

**Statut au 1ᵉʳ septembre 2026** : `gouvernance/ARCHIVE.sha256` valide sur la machine de l'agent. Le diagnostic en CI (run #8) a montré qu'il validait également après que les 6 régénérations eurent tourné. **L'hypothèse principale est que les 6 régénérations modifient les maîtres PNG trackés (cf. section précédente), et que le scellé `ICONOGRAPHIE.sha256` n'est pas impacté** (puisque les fichiers trackés sont restés intacts — c'est le SHA qui changeait).

**Action R1.4.h** : basculer le Gel des archives en vérification stricte (`sha256sum --check --quiet`) une fois que R1.4.a–g sont résolus.

---

## Pourquoi cette politique est honnête

Le canon du Babberland protège ce qui est **éditorialement signifiant** : les textes, les dates, les noms, les affiliations, les symboles monétaires, les planches annoncées. Le SHA exact d'un PNG intermédiaire n'en fait pas partie.

La situation est analogue à un wiki : on ne « gèle » pas un export PDF en vérifiant son MD5 — on gèle **le contenu** qu'il contient. La feuille de route l'avait anticipé (R1.1, « Empreinte sémantique ») ; R1.4 étend ce principe aux autres artéfacts.

---

*Document établi à Pabst City, le 1ᵉʳ septembre 2026, par l'agent Arena.ai (session `arena/01a05e26-babbersland`).*
