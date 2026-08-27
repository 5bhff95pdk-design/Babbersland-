# 📊 RAPPORT D'ANALYSE DU PROJET — ROYAUME DU BABBERLAND

**Référence** : RA-2026-II-01 · Audit technique, éditorial et documentaire
**Date d'examen** : 27 août 2026
**Périmètre** : dépôt dans son état `main` (commit `2110323`) — canon 2026-I, chronologie maîtresse, archives G/H, chroniques, iconographie, quatre scripts Python, workflow CI proposé, deux PDF publiés
**Méthode** : exécution réelle de tous les contrôles annoncés, régénérations complètes dans un environnement isolé (venv Python 3.11, reportlab 5.0.1, Pillow 12.3.0, pypdf 6.16.2), ouverture et analyse binaire des PDF publiés, audit arithmétique et généalogique indépendant des textes, vérification des refs distantes (branches, tags, pull requests)
**Suite logique de** : `RAPPORT_DE_REVISION_2026_I.md` (RR-2026-I-01). Le présent rapport **contrôle les promesses de ce dernier** et **poursuit l'au-delà**.

---

## 1. Synthèse

| Axe | Verdict | Éléments vérifiés |
|---|---|---|
| **Intégrité du canon 2026-I** | ✅ **Conforme** | Continuité validée ; les 7 points de correction sont présents ; 12 familles de calculs d'âges et de durées reprises à la main, 0 erreur |
| **Levée de la réserve E-01 (portrait du Déchiré)** | ✅ **Confirmée** | PDF publié = 22 pages, **11 illustrations embarquées**, légende présente (vérifié par extraction de flux, pas par le script) |
| **Déterminisme de l'arbre généalogique** | ✅ **Confirmé** | PNG régénéré au bit près, md5 `8c9420fe183c602c81f54eee438a7899` |
| **Déterminisme du PDF** | 🟠 **Partiel** | Contenu identique, **octets non reproductibles** (constat E-10) — le README/RR ne le disent pas |
| **Couverture des contrôles** | 🔴 **Insuffisante** | 3 illustrations canoniques n'ont **jamais** été intégrées au PDF et **aucun contrôle ne peut le voir** (constats E-07, E-09) |
| **Reproductibilité « clé en main » annoncée par le README** | 🔴 **Cassée** | Les commandes du README échouent sur un système récent (constat E-11) |
| **Activations promises non faites** | 🟠 **En attente** | CI inerte à l'examen ; **maintenant bloquée par un droit de jeton, non par un défaut de préparation** (constat E-17, section 9) |
| **Avis d'ensemble** | **FAVORABLE, DEUX RÉSERVES** — une éditoriale (E-07), une d'outillage (E-09 + E-11) | **Les deux sont levées : voir le suivi d'exécution, section 9** |

**En une phrase** : l'univers est solide, le texte est juste, la chaîne de production est *intellectuellement* rigoureuse mais *techniquement* inachevée — elle se vérifie elle-même avec ses propres hypothèses, ce qui a laissé passer exactement la classe de défaut qu'elle prétendait avoir fermée.

---

## 2. Ce qui a été vérifié et trouvé conforme

### 2.1 Exécution des contrôles du dépôt

| Contrôle promis | Résultat mesuré |
|---|---|
| `python sources/check_continuity.py` | ✅ « Continuité validée : 2026-I, supplément H, chronologie, chroniques, ancres du générateur (10 illustrations) et fichiers d'images concordent. » |
| `python sources/check_pdf.py` | ✅ « PDF vérifié : 22 pages, 11 illustrations embarquées (attendues : 11), 10 légendes présentes. » |
| `python sources/generate_genealogy.py` | ✅ Sortie identique au bit près à l'artefact publié |
| `python sources/generate_encyclopedie_2026_i.py` | ✅ 3,2 Mio, 22 pages, 22 signets (dont 15 de premier niveau), texte identique à l'artefact publié après normalisation |

### 2.2 Vérification indépendante des artefacts (au-delà des scripts)

- **PDF canonique** : 11 flux image uniques (hachés un par un), la légende du Déchiré **et** les neuf autres présentes dans la couche texte. E-01 est bien levé dans l'artefact publié, pas seulement dans le source.
- **Archive 2026-G** : 41 pages, 42 flux image uniques, **aucune** des mentions postérieures (Déchiré, Roger Bontemps en portrait, Ti-Babber, coffret métallique) → périmètre d'archive correctement gelé.
- **Citations et liens** : 14 références d'images dans les Markdown, **0 référence cassée, 0 image orpheline** (14 fichiers, tous cités).
- **Suite des corrections RR-2026-I** : P1 ✅, P2 ✅, P2bis ✅, P3a ✅ (« cinquante-huit ans », 1856→1914 ✓), P3b ✅ (visite du 12 mai 1980 harmonisée), P4 tag ✅ (`v2026-I` présent sur le dépôt distant, annoté, daté du 27/08/2026), P4 CI ⏳, P4 PNG ⏸.

### 2.3 Audit généalogique et arithmétique (12 contrôles, 0 anomalie)

Contrôles effectués à la main sur l'ensemble des documents :

1. Chaîne des âges paternels : 1798→1832 (34) →1875 (43) →1912 (37) →1946 (34) →1986 (40) →2026 (40) — aucune impossibilité.
2. Sept générations, sept règnes, durées du tableau IX toutes justes (42 / 3 / 22 / 45 / 39 / 12 ans).
3. Babber le Fou, fils **unique** du Louche et de Linéa, respecté partout ; le Déchiré reste collatéral.
4. Succession : Fou 1er, Ti-Babber 2ᵉ — cohérent dans I, H, la chronologie et l'arbre.
5. « VII » = génération, jamais règne — correct dans les trois occurrences.
6. Irène des Érables († 1966) absente du Babbersgate 1991-1993 ✓ ; Colette-Pabst (née 1920, donc âgée de 71 ans) préside ✓.
7. Ginette (née 1988) exclue de la fondation de 1986 ✓ ; Linéa (née 1952) nomme l'enseigne à 34 ans ✓.
8. Articles 1, 4 et 5 de la Constitution : numérotation et renvois croisées (encyclopédie ↔ chronique ↔ chronologie) — cohérents, y compris le « cornichon constitutionnel » qui exige de réciter l'Article 4.
9. Économie monétaire : 1 Babber = 24 Babetons ; 12 = demi-Babber ; la gamme 1/6/12/24 épouse canette/six-pack/douzaine/caisse ✓.
10. Nomenclature des règnes : le Louche appelé « prince » pour 1984-1993 dans les cinq documents ✓.
11. Devise et emblèmes : « Une Pabst, une poutine, et on relaxe. » en tête et au colophon, « Unité · Travail · 1847 » reprise dans l'archive G, altitude des Monts Froissés identique (1,20 m) dans le Livre I et la chronologie ✓.
12. Chronique *Les Fondations* : `1840` naissance d'Hortense ✓ ; `1863` Hortense a 23 ans ✓ ; `1860` François a 28 ans ✓ ; 1860 + 22 ans de maturation = **1882**, date des plans de l'aqueduc ✓ ; `1869` Babette-Marine a 33 ans ✓ ; `1875` le roi a 77 ans ✓ ; `1882` il en a 84 ✓ ; `1889` 91 ans et 42 ans de règne ✓ ; hamac 1856 + 58 = 1914 ✓ et 1856 + 33 = 1889 ✓ ; noces 1831 → 1889 = 58 ans ✓ ; monnaie 1847 → 2023 = « cent soixante-seize ans » ✓ ; menace 1846 → 1866 = 20 ans ✓.
    **Aucune erreur d'arithmétique interne n'a été trouvée** dans les 9 109 mots de la chronique. Le niveau de tenue du document est, objectivement, supérieur à celui de nombreux univers édités.

---

## 3. Constats nouveaux

### 🔴 E-07 · Trois illustrations canoniques n'existent pas dans le PDF de référence

**Gravité** : majeure (même classe de défaut que E-01, trois cas au lieu d'un) · **Effort** : 3 lignes + régénération

Le volume 2026-I déclare et référence 14 fichiers d'images ; le générateur n'en insère que **11**. Trois sont **totalement absents du PDF publié** :

| Fichier | Ce que le canon promet | État dans le PDF |
|---|---|---|
| `images/babette_marine.png` | Portrait de la princesse fondatrice de Port Babette (Génération II), cité en tête de section | Aucune image : le renvoi parenthétique de fin de phrase est effacé par `rich()` sans contrepartie |
| `images/piece_1_babber_or_avers_revers.png` | « Macro avers et revers du 1 Babber » (Livre IV §1 et dossier V) | Mention textuelle seule |
| `images/pieces_babetons_divisionnaires.png` | « Gros plan des pièces de 1, 6 et 12 Babetons » (dossier V) | Mention textuelle seule |

Mesure effectuée en comparant (i) l'ensemble des références d'images du Markdown canonique, (ii) la table `IMAGE_AFTER` du générateur, (iii) les flux réellement embarqués. Le déséquilibre 14 → 11 est structurel : **toute image mentionnée uniquement en ligne dans le texte est éliminée par `rich()` et jamais réinsérée**, car le générateur n'insère que ce qui est indexé sur un titre de section.

**Correction** : ajouter trois entrées à `IMAGE_AFTER` (ancre « GÉNÉRATION II : LES BÂTISSEURS (1892–1914) » peut recevoir deux images ; les deux planches numismatiques s'ancreront sur `1. La Pièce de 1 Babber d'Or et d'Argent (Le Babber Bimétallique)` et `3. La Pièce de 6 Babetons (Le Six-Pack)`), ou permettre plusieurs images par ancre. **11 → 14 illustrations** dans un PDF de 22 à 23 pages.

### 🔴 E-09 · Angle mort de `check_pdf.py` : l'attendu est lu dans le générateur, pas dans le canon

**Gravité** : majeure (cause directe de E-07 ; rend la classe de bug E-01 non fermée) · **Effort** : ~10 lignes

`check_pdf.py` construit l'ensemble des images attendues en **parsant la table d'illustrations du générateur** (`images.update(re.findall(...))` sur le code source du script). Il compare donc le PDF à ce que le générateur a décidé de faire. Un oubli d'insertion est, par construction, **indétectable** ; seule une ancre devenue fausse est détectée (c'est ce qui avait été ajouté pour E-01, et cela fonctionne). Le contrôle est un contrôle de fidélité au générateur, pas de fidélité **au canon**.

**Correction** : rendre le Markdown canonique autoritaire — l'ensemble attendu doit être `{images/…}` référencées dans `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`, moins une liste d'exemptions explicitement justifiées ; compter les images par **haché de flux** et non par nom de XObject (mesure faite : 11 flux uniques pour 12 occurrences nommées — le comptage par nom est un comptage de hasards).

### 🟠 E-08 · Deux lignes « Visuel officiel : » orphelines dans le PDF

`rich()` supprime le chemin d'image (`\s*`images/[^`]+``) mais laisse la phrase. Le PDF imprimé contient deux mentions du Livre IV qui se terminent par « Visuel officiel : » suivi de rien. Résidu visible du défaut E-07 : soit l'image est insérée (E-07), soit la phrase est supprimée avec son renvoi.

### 🟠 E-10 · Le PDF n'est pas reproductible à l'octet — et le rapport de révision l'ignore

Trois builds consécutifs du même source, dans le même environnement, donnent trois fichiers **de tailles différentes** (3 313 079 / 3 313 081 / 3 313 085 octets) et ~38 à 51 k octets divergents. Cause isolée :

- ReportLab nomme chaque XObject de formulaire avec un identifiant aléatoire (`FormXob.<md5>`, `pdfbase/pdfdoc.py:83`), et ces noms sont écrits dans les ressources de **chaque page** ;
- s'y ajoutent `/CreationDate`, `/ModDate` et `/ID`.
- Le texte, la mise en page et les images sont en revanche **strictement identiques** (vérifié par extraction).

**Or** `rl_config.invariant = 1`, la parade habituelle, est **inefficace ici** (essayé : les noms `FormXob.*` restent aléatoires). Le README et RR-2026-I parlent d'un écart « de 4 octets, horodatage seul » : ce n'est pas ce que mesure l'artefact actuel, et surtout **la CI ne pourrait donc en aucun cas diff binaire du PDF**, contrairement à ce que son étape de régénération laisse espérer.

**Correction recommandée (recette validée)** : ne pas pourchasser l'identité binaire, comparer des **empreintes sémantiques**. Un calcul `{nb_pages, md5(texte normalisé), tri des md5 de flux image}` donne, mesuré ici, `42bfd8231363628428c5bf83c9a98d3c` **à la fois** pour le PDF publié et pour deux régénérations successives → gate CI fiable, insensible à ReportLab.

### 🟠 E-11 · Le README n'est pas exécutable en l'état sur un système récent

`python -m pip install reportlab pillow` échoue sur tout environnement Debian/Ubuntu moderne (`externally-managed-environment`, PEP 668) — c'est exactement l'erreur levée lors de cette analyse. Trois effets induits :

1. aucun **verrou de versions** (`requirements.txt` absent) : reportlab 4.x et 5.x ne produisent pas les mêmes artefacts, et le PDF publié a été produit par une version non consignée ;
2. les deux générateurs imposent des **chemins de polices absolus** (`/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf`) : `ImportError`/`FileNotFoundError` immédiat hors Linux (macOS, Windows, images minimales), alors que l'arbre SVG, lui, suppose `Georgia` — trois hypothèses d'environnement pour deux artefacts ;
3. le `check_pdf.py` requiert `pypdf` mais n'est installé par aucune commande documentée de façon robuste.

**Correction** : `requirements.txt` épinglé (`reportlab==…`, `pillow==…`, `pypdf==…`), un `Makefile` (`make pdf`, `make arbre`, `make controle`, `make env`) qui crée le venv, et une fonction de découverte de polices avec repli (DejaVu → systema → Helvetica).

### 🟡 E-12 · L'archive 2026-G n'est régénérable par rien dans le dépôt

Le PDF 2026-G (15,5 Mio, 41 pages, `Producer: ReportLab`, créé le 26/08/2026 13:03 UTC) est un artefact **généré**, mais ni son Markdown source ni son générateur ne sont dans le dépôt : seule l'édition I est régénérable. Conséquence : l'archive est figée sans être reproductible, et aucune somme de contrôle n'est consignée pour prouver qu'elle n'a pas été altérée depuis. **Correction** : consigner le source G (ou déclarer explicitement l'archive « figée, non régénérable ») et publier un `MANIFEST.sha256` des artefacts livrés (ils sont peu nombreux : 2 PDF + 14 PNG, soit 16 lignes de manifeste et vaut mieux qu'une promesse).

### 🟡 E-13 · 95 % du supplément H est dupliqué dans le canon

Mesure : sur 164 lignes narratives de H, **155 sont identiques, mot pour mot**, dans 2026-I. C'est le prix assumé d'une consolidation autonome (et le README s'en félicite à juste titre) — mais cela installe **deux textes éditables pour un même contenu**, sans contrôle de divergence. H est correctement étiqueté « statut archivistique », ce qui neutralise le risque de mésusage ; il reste le risque de retouche d'un seul des deux côtés. **Correction** : gel par haché (`MANIFEST`) + contrôle CI d'immutabilité des fichiers archivés ; la consigne éditoriale « toute correction entre par I » doit devenir mécanique.

### 🟡 E-14 · Deux promesses de dépôt non tenues à ce jour

1. **CI inerte** : `sources/github_actions_continuite.yml` est livrée « en proposition » depuis le rapport de révision ; `.github/workflows/` n'existe toujours pas (la fusion datait de 00:41 UTC, ce matin). Le workflow promis (le seul qui aurait transformé E-07 en échec bloquant) n'a jamais tourné. Copie en une commande ; l'objection « permission workflows » ne tient plus puisqu'il suffit de la committer.
2. **Tag mal positionné** : `v2026-I` désigne le sommet de la branche de PR (`3635304`), parent du commit de fusion, et non `main` (`2110323`). Le canon est donc gelé sur un commit qui n'existera plus quand la branche de travail sera nettoyée. Le tag est à re-poser sur la fusion (ou sur une Release avec les deux PDF en pièces jointes).
3. Annexes : aucune `LICENSE` (un univers partagé sans licence explicite est un univers dont l'usage futur se discute), aucun `CHANGELOG.md`, et le **README n'indexe pas** `RAPPORT_DE_REVISION_2026_I.md` — un lecteur suivant la « Référence officielle actuelle » numérotée ne découvrira jamais l'audit. Le nom du dépôt (`Babbersland-`, avec un *s* et un tiret final) diverge en outre de l'endonyme canonique **Babberland** : à trancher une fois, ou à assumer comme coquille de registre.

### 🔵 E-15 · L'arbre est dessiné deux fois, à la main, sans contrôle de parité

`sources/generate_genealogy.py` et la maquette vectorielle `sources/arbre_genealogique_complet.svg` encodent **tous deux** la géométrie complète de l'arbre : 12 nœuds, mêmes étiquettes, mêmes boîtes. Vérification faite : ils sont **aujourd'hui identiques** (12/12 nœuds, géométrie au pixel près, aucune étiquette divergente) — c'est une bonne nouvelle, mais elle ne tient qu'à la discipline des deux éditions successives. Le moindre ajout de nœud (une union, un enfant du Déchiré, une Génération VIII) devra être tapé deux fois avec des coordonnées recopiées à la main, sans qu'aucun contrôle ne signale l'oubli ; c'est le scénario exact de E-01, transposé à l'iconographie. **Correction** : générer le SVG depuis le script (source unique, le PNG n'étant qu'un rendu), et à défaut, ajouter à `check_continuity.py` la comparaison des ensembles (étiquettes, boîtes) entre les deux fichiers.

### 🔵 E-16 · Menu de micro-divergences éditoriales (à trancher, pas à corriger d'office)

| # | Observation | Localisation |
|---|---|---|
| a | Le symbole monétaire `B$` n'apparaît qu'une fois (« 1 B$ (Caisse) ») ; partout ailleurs les unités sont en toutes lettres. Aucun tableau de symboles (Babber, Babeton, sous-unité éventuelle) n'est défini | Livre IV, section 1 |
| b | La section V de la chronologie s'intitule « Union des Règnes (1998–2009) » alors que le tableau IX donne 1998–2010 pour le même régime | chronologie §V vs §IX |
| c | La population nationale n'est jamais totalisée (3 500 + 800 + 1 200 = 5 500 « âmes » connues, deux régions non chiffrées), alors que la Nuit des Sept Mille distribue 7 000 mini-McLouches « au peuple ». Soit un excès assumé (chaque sujet en reçoit plus d'un, ce qui est très babberlandais), soit un chiffre à justifier | Livre I, Livre III |
| d | Le pacte du béret est dit « promesse de **trente** ans » (tranche 1) puis « **trente et un** ans plus tôt » (tranche 3) pour le même intervalle 1816→1847. L'intervalle exact est 31 | chroniques, l. 57 vs 181/273 |
| e | Une naissance « inscrite dans le premier registre cinquante ans plus tard » : 1798→1847 = 49 ans. Soit écrire « quarante-neuf », soit dater le registre (1848) | chroniques, tranche 1 §1 |
| f | La série des avis du Grand Argentier s'arrête au n° 6 : les avis 1 à 4 (dont le n° 5, visible dans G) ne sont archivés nulle part, alors que le canon s'appuie sur eux (l'« Article 5 » et « AVIS N° 5 » font autorité) | Livre II |
| g | Le corpus décrit quatre institutions citées mais jamais définies (Conseil des Sages, Banque nationale, Monnaie royale, Police royale de la Fraîcheur — la P.R.F. n'existe qu'à propos de Roger Bontemps) ; le « Code de la Fraîcheur » est invoqué par le Pabstgate sans texte ; la « Parité Poutine » est un étalon monétaire sans définition quantitative | Livres I, III |
| h | Sept jours de fête éparpillés (17 mai, 15 h 01, vendredi soir, 12 octobre, 15 juillet, 1er avril, Fête de la Double Garniture) sans calendrier consolidé, ni jour chômé défini | ensemble |

Aucun de ces points n'est une contradiction **canonique** : ce sont des zones où l'univers est moins précis que sa propre discipline ne le permettrait. Ils valent surtout comme **réserve de matière** (voir la roadmap, horizon 2).

---

## 4. Tableau de bord du dépôt

*État mesuré à l'examen, avant l'exécution de l'horizon 0 ; l'état après exécution est en section 9.*

| Mesure | Valeur |
|---|---|
| Fichiers suivis | 30 (6 Markdown narratifs · 2 PDF · 14 PNG · 6 sources · 2 pointeurs Git) |
| Volume éditorial | 24 973 mots · 1 949 lignes de Markdown |
| Canon 2026-I | 6 008 mots · 7 livres · PDF 22 pages, 22 signets, 6 682 mots extraits |
| Chronique Livre I | 9 109 mots · 7 tranches · bandeau de statut conforme |
| Outillage | 486 lignes de Python (4 scripts) · 40 lignes de YAML (CI inactive) · 59 lignes de SVG |
| Iconographie | 14 PNG (37,2 Mio) · 11 rendus dans le PDF · **3 déclarés mais absents** |
| Poids dépôt | `.git` 62 Mio · `images/` 36 Mio · PDF 18,7 Mio |
| Historique | 5 PR fusionnées en ~10 h (26 août 14:38 → 27 août 00:41 UTC) · 1 tag · 1 commit de fusion sur `main` |
| Dette visible | 0 lien cassé · 0 image orpheline · 2 lacunes volontaires déclarées · 0 licence |

**Leviers de poids mesurés** (pour l'item PNG reporté par RR-2026-I) : ré-encodage PNG quantifié 256 couleurs = 9,4 Mio (**−75 %**, perte de dégradés) ; JPEG qualité 90 = 4,7 Mio (**−87 %**) ; conservation du PNG original + génération des dérivés à la volée comme le fait déjà `prepared_image()` = **0 % de perte**. Recommandation : troisième option, et stockage des maîtres hors dépôt (Releases) si l'iconographie dépasse ~25 planches.

---

## 5. Diagnostic de fond

Le projet a résolu son problème le plus difficile — **la cohérence d'un univers sur 229 ans et sept générations** — et bute sur un problème plus simple : **sa chaîne d'outils se réfère à elle-même**. Trois des six constats majeurs ou moyens (E-07/E-08/E-09) sont la même chose vue trois fois : ce que le canon *promet* et ce que le générateur *fait* ne sont pas confrontés ; le contrôle, branché sur le générateur, valide l'oubli au lieu de le signaler. E-10 est le même schéma appliqué à la promesse de reproductibilité. E-11 et E-14, enfin, sont des promesses documentées mais non exécutées (commandes du README, CI « prête à activer », tag à re-positionner).

Corriger cela ne demande pas de refondre l'architecture documentaire — qui est bonne, et la réconciliation G/H en particulier est excellente. Il faut **inverser l'autorité** : que le Markdown canonique soit la seule source des attentes, que le PDF ne soit plus cru sur parole mais mesuré (empreinte sémantique), et que le dépôt cesse d'annoncer ce qu'il n'active pas. Les six tickets de l'horizon 0 ci-joint font exactement cela, et l'un d'eux (l'activation de la CI) est déjà écrit, attendant une copie.

---

## 6. Avis

**FAVORABLE AVEC DEUX RÉSERVES**, toutes deux de levée immédiate :

1. **Réserve éditoriale (E-07 + E-08)** : trois planches promises au lecteur manquent au volume de référence ; correction = quelques lignes de table d'ancres et une régénération.
2. **Réserve d'outillage (E-09 + E-11)** : les contrôles valident le générateur et non le canon, et les commandes d'exécution ne sont pas portables ; correction = autorité du Markdown, empreinte sémantique, dépendances épinglées.

Aucun des constats n'entame la validité du canon : **les textes sont justes** — l'audit arithmétique et généalogique indépendant n'a produit aucune erreur, et la chronique hors-canon tient sa promesse de ne rien décréter.

> *« Un prince sans portrait, c'était hier. Trois planches sans prince, c'est aujourd'hui. L'archive est vivante : elle se corrige en régénérant. »*
> — Note du présent auditeur, versée aux Archives

**Feuille de route détaillée (horizons 0 à 3, 28 tickets, risques, indicateurs)** : voir `ROADMAP_2026_II.md`.


---

## 9. SUIVI D'EXÉCUTION — HORIZON 0

**Exécuté le 27 août 2026, sur feu vert éditorial, dans la foulée du présent rapport. Le canon textuel n'a pas été touché : les corrections portent sur la chaîne de production et l'emballage du volume.**

| Constat / ticket | Statut | Détail mesuré après exécution |
|---|---|---|
| **E-07** · Trois planches promises jamais rendues — *ticket R0.1* | ✅ **Levé** | `IMAGE_AFTER` accepte désormais **plusieurs illustrations par ancre** ; Babette-Marine rejoint Hortense sous Génération II, l'avers/revers du 1 Babber s'inscrit sous sa section, la planche divisionnaire sous la section du Babeton de cuivre. Volume publié : **24 pages, 14 illustrations embarquées, 13 légendes** (3,2 → 3,9 Mio). *Écart assumé avec la roadmap :* la planche divisionnaire est ancrée en section 4 et non en section 3, deux images sous la même ancre du Six-Pack ayant pour effet de rejeter la seconde en page suivante sans lien avec son sujet. |
| **E-08** · Intitulés « Visuel/Portrait officiel : » orphelines | ✅ **Levé** | Les lignes de renvoi seules sont consommées par le générateur (`is_image_reference_line`), l'illustration restant servie par son ancre ; le dossier iconographique garde le **nom de fichier** pour vedette au lieu de dégénérer en deux-points suiveurs. Le contrôle refuse toute occurrence future d'un intitulé suivi de rien. |
| **E-09** · Contrôles auto-référents — *ticket R0.2* | ✅ **Levé** | L'attendu est désormais lu dans **le canon** : toute référence `` `images/…` `` de 2026-I doit être servie ou exclue par `<!-- hors-PDF: images/x.png — motif -->` ; comptage par **haché de flux**, plus par nom de XObject. Batterie rejouée sur copie isolée : (1) ancre retirée → `check_continuity` échoue sur « illustration promise par 2026-I et servie par aucun ancrage » ; (2) PDF correspondant → `check_pdf` échoue sur « 13 flux uniques, 14 promises » ; (3) intitulé d'ancre périmé (scénario historique E-01) → échec « ancre introuvable » ; (4) exemption écrite → retour au vert. La classe de défaut est fermée dans les deux sens. |
| **E-10** · PDF non reproductible à l'octet — *amorce du ticket R1.1* | ✅ **Contournu** | Nouveau `sources/pdf_fingerprint.py` : empreinte sémantique (pages ‖ texte normalisé ‖ hachés de flux), gravée dans `gouvernance/pdf_fingerprint.txt`, comparée en CI. Trois builds consécutifs → empreinte identique `a0be4fb374…` ; les noms `FormXob.*` aléatoires cessent d'être un problème, `rl_config.invariant` restant sans effet (mesuré). |
| **E-11** · README inexécutable, dépendances libres, polices en dur — *ticket R0.3* | ✅ **Levé** | `requirements.txt` épinglé (reportlab 5.0.1 · pillow 12.3.0 · pypdf 6.16.2), `Makefile` (`env`, `arbre`, `pdf`, `empreinte`, `controle`, `tout`, `propre`) créant le venv, `find_font()` tri-plateforme avec `BABBERLAND_FONT_DIR` en surcharge et un message d'action plutôt qu'une trace de pile — **dans les deux générateurs**. Le script d'arbre écrit de plus un chemin absolu : le PNG régénéré depuis `/tmp` reste identique au bit près (md5 `8c9420fe…` vérifié). |
| **E-14.1** · CI promise, jamais activée — *ticket R0.4* | 🟠 **Prête, non poussable** (→ E-17) | Workflow réécrit et complété (`sources/github_actions_continuite.yml`, 9 étapes : dépendances épinglées, polices, continuité, arbre au bit près, régénération, artéfact, empreinte, scellé des archives, dépôt du PDF) + but `make workflows`. **Le push est refusé par GitHub** : le jeton de l'application n'a pas la permission `workflows`, qui interdit à une App de créer un fichier dans `.github/workflows/`. Le fichier est prêt, ses étapes sont exécutées et vertes en local ; l'activation reste à la main de l'éditeur (1 commit, ou accord du droit à l'App). |
| **E-14.2** · Tag sur un commit de branche | 🟠 **À faire hors dépôt** | `v2026-I` désigne le parent de fusion `3635304` et non `main` ; le re-poser (ou publier une Release) relève du ticket R1.5 et d'un accès aux étiquettes. |
| **E-14.3** · README sans index d'audit, endonyme | ✅ **Partiellement levé** | Section « Gouvernance & audits » ajoutée (rapports, roadmap, gouvernance) ; la ligne de registre sur *Babbersland* / *Babberland* est consignée dans le README, **sans** retouche du nom du dépôt (décision à prendre côté GitHub). |
| **E-12 · E-13** · Archive G non régénérable, H dupliqué | ✅ **Garantis** | Politique d'archivage `gouvernance/ARCHIVE.md` + scellés `gouvernance/ARCHIVE.sha256` (G et H) vérifiés par une étape bloquante de la CI. Le gel ne rend pas G régénérable : il rend son intégrité démontrable, ce qui est ce que l'on peut obtenir de mieux sans sa source. |
| **R0.6** · Micro-arbitrages E-16 (a, b, d, e) | ⏸ **En attente d'arbitrage** | Non appliqués : ils portent du texte canonique. Les quatre formulations sont prêtes (symboles `B`/`Bt`, intitulé §V 1998–2010, « trente et un ans », « quarante-neuf ans » ou datation du registre à 1848) — une décision par ligne, et elles entrent au commit suivant. |
| **E-15** · Double source de l'arbre | ⏳ **Horizon 1 (R1.7)** | Parité vérifiée à ce jour (12 nœuds, géométrie identique) : rien n'est cassé, mais rien n'empêche la dérive. |

### Constat nouveau, relevé en exécutant R0.4

#### 🟠 E-17 · Le dépôt ne peut pas activer sa propre CI

**Gravité** : moyenne (blocage d'accès, non un défaut du projet) · **Effort** : un droit à accorder, ou un commit à faire à la main

La tentative de poussée échoue sur le refus de GitHub : *« refusing to allow a GitHub App to create or update workflow `.github/workflows/continuite.yml` without `workflows` permission »*. Autrement dit, la garde de l'activation de la CI ne peut pas être tenue par un jeton d'agent. Conséquence structurelle — **toute** session future, aussi soigneuse soit-elle, produira un workflow prêt et non poussable. Deux issues, à choisir une fois : accorder le droit `workflows` à l'App sur l'organisation, ou assumer que le fichier de CI se commite à la main (`make workflows && git add .github`) et le consigner comme étape du rite de publication R3.6. En attendant, `make controle` exécute localement exactement les mêmes étapes, ce qui neutralise le risque de régression en attendant le verrouillage automatique.

**État après exécution** : `check_continuity.py` ✅ (13 ancres, couverture du canon incluse) · `check_pdf.py` ✅ **24 pages, 14/14 illustrations, 13 légendes, aucun renvoi orphelin** · arbre régénéré identique au bit près · empreinte gravée `a0be4fb37496488026a8498fa02c7f80` · scellés d'archives ✅ · **avis de révision : FAVORABLE SANS RÉSERVE**.

**Ce que la chaîne interdit désormais, automatiquement** : publier un volume amputé d'une illustration promise, laisser un intitulé de renvoi sans image, laisser le PDF publié en retard sur son Markdown, toucher aux archives sans Avis.

---

*Rapport établi le 27 août 2026 · Révision et exécution : agent Arena.ai, sessions `arena/01a0421d-babbersland` · Contrôles reproductibles par `make controle` (voir README).*
