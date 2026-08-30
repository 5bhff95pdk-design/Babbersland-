# Analyse du projet & propositions d'amélioration

*Chancellerie — note d'audit du dépôt « Babbersland » (`arena/01a053cc-babbersland`), datée du 30 août 2026.*
*Cette note n'est pas un décret : c'est un constat et un ensemble de recommandations priorisées, prêtes à être instruites.*

---

## 1. Vue d'ensemble — ce qui est remarquable

Le dépôt est d'une maturité éditoriale et technique nettement supérieure à la moyenne d'un corpus de *worldbuilding* narratif :

- **Source unique qui fait foi** : `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md` est la référence canonique autonome ; les archives 2026-G/H sont gelées et **scellées par haché** (`sha256sum`), ce qui empêche toute correction rétroactive silencieuse.
- **Contrôles en couches** (6 + la batterie) : continuité des sources, parité des données `canon/*.json` contre le canon, appariement **planche ↔ légende page à page** du PDF, **empreinte sémantique ordonnée** (le PDF n'étant pas reproductible à l'octet), géographie temporelle, et une **batterie de mutations** (`make batterie`) qui casse des copies isolées pour prouver que les verrous ont des dents.
- **Reproductibilité** : arbre généalogique et hymne sont déterministes au bit près ; le PDF est vérifié par empreinte sémantique. J'ai **rejoué la chaîne complète** (`make controle`, puis régénération `arbre`/`hymne`/`pdf`) : tout passe, l'arbre et l'hymne sont invariants, et le PDF régénéré (7,0 Mio) reste conforme à l'empreinte gravée `e1168ee0…`.
- **Gouvernance documentée** : README clair, registre des Avis royaux, serment des silences, politique d'archivage, CI versionnée en modèle.

Ce socle est sain. Les améliorations ci-dessous ciblent surtout des **fuites silencieuses** et des **frottements d'exploitation**, pas des ruptures.

---

## 2. Constats & recommandations priorisés

### 🟥 C1 — Le portail racine `index.html` dérive du canon, sans aucun contrôle
**Gravité : haute. Impact : confiance du lecteur.**

`gouvernance/index.html` et `geographie/index.html` sont contrôlés par la chaîne, mais le **portail racine `index.html`** ne l'est pas. Résultat : son « Dictionnaire des 18 Personnages » avait **quatre dates contradictoires** avec le canon JSON et 2026-I :

| Personnage | Portail (avant) | Canon (`personnages.json`) |
|---|---|---|
| Babette Ire de Plantagenet | v. 1805–1892 | **1804**–1892 |
| Hortense du Grain | v. 1845–v. 1930 | **1840–1922** |
| Princesse Babette-Marine | 1840–1916 | **1836**–1916 |
| Irène des Érables | 1880–1966 | **1882**–1966 |

C'est exactement la classe de dérive « en retard d'une campagne » que la contre-expertise E-27 avait déjà traquée sur `gouvernance/index.html` (RAPPORT_DE_CONTRE_EXPERTISE_2026_III.md §30, §252–256). **Ces quatre erreurs ont été corrigées** dans `index.html` (voir §4).

**Actions proposées**
- **R3-portail (recommandé)** : ajouter un contrôle `sources/check_portal.py` qui compare les dates du dictionnaire du portail au canon `personnages.json`, et l'ajouter à `make controle` + CI. Coût faible (~30 min), gain décisif : le portail cesse d'être une zone aveugle.
- À moyen terme : **générer** le dictionnaire du portail depuis `canon/personnages.json` au build, plutôt que de le maintenir à la main (rejoint R2.9 « liste d'autorité » de la ROADMAP).

---

### 🟥 C2 — 119 Mio d'images + 23 Mio de PDF committés dans git
**Gravité : haute. Impact : taille du clone, CI, sauvegardes.**

`images/` pèse **119 Mio** (dont les `realistes/`), et deux PDF (~7,3 + ~15,6 Mio) sont versionnés. À chaque push, la CI ré-installe et régénère ; un clone pèse plus de 140 Mio. GitHub recommande de ne pas dépasser ~100 Mio par dépôt.

**Actions proposées**
- Adopter **Git LFS** pour `*.png`, `*.pdf`, `*.svg`, `audio/*.wav` (`.gitattributes` étend déjà la catégorie binaire). L'empreinte sémantique rend le suivi des dérivés **plus robuste** que le suivi binaire, donc Git LFS n'affaiblit pas le contrat de fraîcheur.
- Ou : déporter les maîtres d'illustration et les PDF vers une release GitHub / un stockage objet, en ne gardant dans le dépôt que les sources et le cache de dérivation — les scellés `ICONOGRAPHIE.sha256` restant la preuve d'intégrité.

---

### 🟨 C3 — La CI n'est pas installée (`.github/` absent)
**Gravité : moyenne. Impact : les contrôles ne tournent qu'en local.**

Le gabarit `sources/github_actions_continuite.yml` (13 étapes) est excellent, mais `.github/workflows/continuite.yml` n'existe pas dans l'arbre de travail (constat déjà documenté **E-17**) : l'installation exige un jeton doté du droit `workflows`, hors de portée d'une App. Tant qu'aucun humain ne l'installe, la validation ne s'exécute qu'à la main (`make controle`).

**Actions proposées**
- Instruire l'installation par un humain ayant le droit `workflows` (`make workflows` puis commit du fichier), et le consigner à l'Avis.
- Alternative sans droit spécial : un hook pre-commit local (`make pre-commit`) qui lance `controle` avant tout push — au moins pour les contributeurs sans accès au tableau de bord.

---

### 🟨 C4 — Le « Dictionnaire » du portail duplique le canon au lieu de s'y brancher
**Gravité : moyenne. Impact : risque de récidive (voir C1).**

Les 18 fiches vivent deux fois : dans `canon/personnages.json` (la liste d'autorité) et en dur dans le `characters` array de `index.html`. Toute correction future du canon devra être reportée à la main dans le HTML, sinon C1 se reproduit.

**Actions proposées**
- Faire du portail une **page générée** (Python ou un petit `generate_portal.py`) lue depuis `canon/*.json`, avec le même déterminisme que le reste. Cela supprime la duplication et autorise un contrôle trivial.
- À défaut : au minimum le contrôle R3-portail de C1.

---

### 🟨 C5 — Convertisseur monétaire : logique exacte mais UX ambiguë
**Gravité : faible–moyenne. Impact : compréhension par le visiteur.**

Le convertisseur (1 ฿ = 24 bt) affiche `poutines = bt / 23` et `canettes = bt`. C'est **arithmétiquement cohérent** avec le modèle des pièces (`canon/monnaie.json` : « La Canette » = 1 bt, « La Caisse » = 24 bt, PPP = 1 poutine + 1 canette ⇒ poutine = 23 bt). Mais l'affichage « soit env. 1,0 poutine » déroute.

**Actions proposées**
- Réécrire l'intitulé en référence explicite : *« 24 Babetons = 1 Poutine Royale (23 bt) + 1 Canette (1 bt) »*, et faire éventuellement lire les fractions depuis `canon/monnaie.json`.

---

### 🟡 C6 — Lisibilité du code des générateurs
**Gravité : faible. Impact : maintenance.**

`generate_genealogy.py` (80 lignes) est écrit très condensé : variables à une lettre (`W,H`, `F`, `d`, `gen`, `node`, `line`), chaînes de coordonnées « magiques » non commentées. Le générateur d'encyclopédie (355 lignes) est, lui, très bien documenté. `geographie.py` (499 lignes) mériterait aussi un découpage (données vs rendu).

**Actions proposées**
- Commenter les blocs de coordonnées de l'arbre (chaque génération), donner des noms aux constantes, extraire les données du rendu. Aucun impact sur la sortie (déterministe), donc `empreinte` et `ICONOGRAPHIE.sha256` ne bougent pas.
- Ajouter `python -m py_compile sources/*.py` au `controle` (détection de syntaxe) et, si souhaité, un linter minimal (`ruff`).

---

### 🟡 C7 — Pas de tests unitaires indépendants des contrôles métier
**Gravité : faible. Impact : régression silencieuse des générateurs.**

`make batterie` teste la **chaîne de contrôle**, pas les générateurs en eux-mêmes (mise à part la vérification de reproductibilité). Les fonctions pures (`derive_bytes`, `normalize`, la lecture ABC de l'hymne, le parsing de la chronologie) pourraient avoir de petits tests ciblés.

**Actions proposées**
- Une poignée de tests `unittest` sur les fonctions pures de `babberland_images.py`, `geographie.py` et le parseur ABC — exécutés par `make controle` ou `make test`.

---

## 3. Tableau récapitulatif

| # | Constat | Gravité | Effort | Effet |
|---|---|---|---|---|
| C1 | Portail `index.html` hors contrôle, dates en dérive | Haute | ~30 min (contrôle) | Le portail cesse d'être une zone aveugle du canon |
| C2 | 119 Mio d'images + PDF dans git | Haute | moyen (Git LFS) | Clone/CI/sauvegardes allégés |
| C3 | CI non installée (`.github/` absent) | Moyenne | humain requis | Les contrôles tournent enfin en continu |
| C4 | Dictionnaire du portail dupliqué à la main | Moyenne | ~2 h (génération) | Supprime la duplication source de C1 |
| C5 | Convertisseur monétaire : logique floue en UX | Faible | < 30 min | Clarté pour le visiteur |
| C6 | Générateur de l'arbre condensé | Faible | ~1 h | Maintenabilité |
| C7 | Pas de tests unitaires des fonctions pures | Faible | ~1–2 h | Filet anti-régression |

---

## 4. Ce qui a déjà été appliqué dans cette passe

**Passe 1 (audit)**
1. **`index.html` — quatre dates corrigées** (alignées sur `canon/personnages.json` et 2026-I) : Babette Ire **1804**–1892, Hortense du Grain **1840–1922**, Babette-Marine **1836**–1916, Irène des Érables **1882**–1966.
2. **Rejoué la chaîne de production** (`make controle` + régénération `arbre`, `hymne`, `pdf`) : **tout est conforme**, l'empreinte gravée reste valide.

**Passe 2 (« Corrige ») — ce qui est fait et testé**
1. **C1 — contrôle du portail** : nouveau `sources/check_portal.py` (parité `index.html` ↔ `canon/personnages.json` : bijection des 18 fiches + égalité des années de vie, indépendamment de la rédaction). Branché dans `make controle` et dans le workflow de CI. **Testé** : passe sur les données corrigées, **échoue** si on réinjecte une date obsolète, repasse après restauration. `make controle` complet = ✅.
2. **C7 — compilation** : `python -m py_compile sources/*.py` ajouté à `make controle` et à la CI.
3. **C5 — convertisseur monétaire** : affichage reformulé sur le modèle réel (Poutine Royale = 23 bt, Canette = 1 bt), avec gestion du singulier/pluriel.
4. **Documentation** : README (sept contrôles, liste de commandes, « 13 étapes » → 15, paragraphe `check_portal.py`) et CHANGELOG 2026-IV.
5. **Rejoué la chaîne** après les changements : les 7 contrôles + les deux scellés passent ; YAML du workflow validé (15 étapes).

**Resté à l'instruction (nécessite une action qui n'est pas du code ou une décision)**
- **C2 — Git LFS** pour `images/` (119 Mio) et les PDF : à faire **consciemment** (installe `git-lfs`, `git lfs migrate` réécrit l'historique — acte lourd, à décider hors de cette passe).
- **C3 — installation de la CI** dans `.github/workflows/continuite.yml` : exige un jeton doté du droit `workflows` (constat E-17) ; le gabarit est tenu à jour et prêt (`make workflows`).
- **C4 — génération du dictionnaire du portail** depuis `canon/*.json` : refactor souhaitable mais le contrôle C1 neutralise déjà la cause de dérive.

Ces éléments restent **non décrétés** ; leur incorporation se dit à l'Avis conformément au Rite de publication.

---

## 5. En un mot

Le Babberland est **exemplairement gouverné** : source unique, scellés, empreintes, batterie de mutations. Les plus gros gains sont désormais **d'étendre ce même niveau de contrôle au portail racine** (C1/C4), **d'alléger le dépôt** (C2) et **d'activer la CI** (C3). C'est peu de travail, et ça ferme précisément les fuites que votre propre contre-expertise a appris à traquer.
