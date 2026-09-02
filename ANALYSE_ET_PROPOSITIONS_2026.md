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

### ⚖️ C2 — Images et PDF lourds dans git — **DÉCRÉTÉ le 2 septembre 2026 (Avis royal n° 9)**
**Gravité : haute. Impact : taille du clone, CI, sauvegardes.**

> **Arbitrage rendu.** Variante **A′** retenue (`images/realistes/`, `images/vignettes/`,
> `audio/` en LFS, ≈ 236 Mio) ; **Option B écartée** — la réécriture de l'historique briserait
> tout clone et toute branche, et le passé du Royaume ne se réécrit pas (dans la ligne de
> l'Avis n° 6). Aucun plafond de poids institué. **Exécution en attente** d'une machine ayant
> accès au CDN GitHub : `github-cloud.s3.amazonaws.com` et `uploads.github.com` restent
> inaccessibles depuis l'environnement d'agent (mesure reconduite le 2 sept.), et poser les
> filtres LFS sans pouvoir téléverser produirait des pointeurs orphelins.
> Voir `gouvernance/LFS_MIGRATION.md` § 5.

*Mesures corrigées le 2 septembre 2026* — le chiffre de 119 Mio de la rédaction initiale était
sous-évalué de presque trois fois :

| Corpus | Fichiers | Poids |
|---|---|---|
| `images/realistes/` | 83 | **227 Mio** |
| `images/*.png` (maîtres) | 28 | **75 Mio** |
| `*.pdf` | 2 | **22 Mio** |
| `images/vignettes/` + `audio/` | 86 | **8,7 Mio** |
| **Total hors `.git`** | | **334 Mio** — et le magasin `.git` en pèse **329** |

GitHub recommande de ne pas dépasser ~100 Mio par dépôt : on en est à plus du triple.

**Actions proposées**
- Adopter **Git LFS** pour `*.png`, `*.pdf`, `*.svg`, `audio/*.wav` (`.gitattributes` étend déjà la catégorie binaire). L'empreinte sémantique rend le suivi des dérivés **plus robuste** que le suivi binaire, donc Git LFS n'affaiblit pas le contrat de fraîcheur.
- Ou : déporter les maîtres d'illustration et les PDF vers une release GitHub / un stockage objet, en ne gardant dans le dépôt que les sources et le cache de dérivation — les scellés `ICONOGRAPHIE.sha256` restant la preuve d'intégrité.

---

### ✅ C3 — La CI n'est pas installée (`.github/` absent) — **RÉSOLU le 1ᵉʳ septembre 2026**
**Gravité à l'époque : moyenne. Impact : les contrôles ne tournaient qu'en local.**

> **Constat clos.** Le droit `workflows` a été accordé à l'installation de l'App, la PR #22 a
> installé `.github/workflows/continuite.yml` sur `main` (commit `9f527f3`), et la CI est
> **active, verte, 20 étapes bloquantes sur 20** (18 nommées + `checkout` + `setup-python` ;
> première exécution verte : 2026-09-01T21:46:19Z). `batterie.yml` est installé également.
> R1.8 vérifie désormais que les workflows installés sont l'octet de leurs modèles.
> **Le texte ci-dessous est conservé comme mémoire de l'instruction ; il ne décrit plus l'état
> du dépôt.**

~~Le gabarit `sources/github_actions_continuite.yml` (13 étapes) est excellent, mais `.github/workflows/continuite.yml` n'existe pas dans l'arbre de travail (constat déjà documenté **E-17**) : l'installation exige un jeton doté du droit `workflows`, hors de portée d'une App. Tant qu'aucun humain ne l'installe, la validation ne s'exécute qu'à la main (`make controle`).~~

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

*État au 2 septembre 2026 — la colonne « Statut » est tenue à jour ; les constats clos le disent.*

| # | Constat | Gravité | Effort | Effet | Statut |
|---|---|---|---|---|---|
| C1 | Portail `index.html` hors contrôle, dates en dérive | Haute | ~30 min (contrôle) | Le portail cesse d'être une zone aveugle du canon | ✅ **clos** — `check_portal.py` en CI |
| C2 | Images + PDF lourds dans git (**334 Mio** hors `.git` au 2 sept.) | Haute | moyen (Git LFS) | Clone/CI/sauvegardes allégés | ⚖️ **décrété** — Avis n° 9 : variante A′, réécriture d'historique écartée ; exécution en attente d'une machine avec accès au CDN |
| C3 | CI non installée (`.github/` absent) | Moyenne | humain requis | Les contrôles tournent enfin en continu | ✅ **clos** le 1ᵉʳ sept. — 20 étapes bloquantes, vertes |
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
- ~~**C2 — Git LFS**~~ → **tranché le 2 septembre 2026 par l'Avis royal n° 9** : variante A′
  (`images/realistes/`, `vignettes/`, `audio/` en LFS, ≈ 236 Mio), **Option B écartée** — la
  réécriture de l'historique briserait tout clone et toute branche, et le passé du Royaume ne se
  réécrit pas. Reste à exécuter (`make lfs && git push`) depuis une machine ayant accès au CDN
  GitHub, inaccessible depuis l'environnement d'agent (mesure reconduite le 2 sept.).
  Voir `gouvernance/LFS_MIGRATION.md` § 5.
- ~~**C3 — installation de la CI**~~ → **fait le 1ᵉʳ septembre 2026** : droit `workflows` accordé,
  PR #22, commit `9f527f3`. CI active et verte, 20 étapes bloquantes ; parité modèle ↔ installé
  vérifiée par R1.8.
- **C4 — génération du dictionnaire du portail** depuis `canon/*.json` : refactor souhaitable mais le contrôle C1 neutralise déjà la cause de dérive.

Ces éléments restent **non décrétés** ; leur incorporation se dit à l'Avis conformément au Rite de publication.

---

## 5. En un mot

Le Babberland est **exemplairement gouverné** : source unique, scellés, empreintes, batterie de mutations.

*Mise à jour du 2 septembre 2026.* Des trois gains annoncés par cette note, **deux sont acquis** :
le contrôle du portail racine (C1, `check_portal.py` en CI) et l'activation de la CI (C3, 20
étapes bloquantes et vertes). Le troisième, l'allègement du dépôt (C2), est **décidé sans être
exécuté** : l'Avis n° 9 retient la variante A′ et refuse la réécriture de l'historique, l'exécution
attendant une machine ayant accès au CDN GitHub.

Reste donc, par ordre d'intérêt : **C4** (générer le dictionnaire du portail depuis `canon/*.json`,
pour supprimer la cause de C1 plutôt que d'en surveiller l'effet), puis C6 et C7. Et un constat
que cette note n'avait pas fait : **l'appareil critique pèse désormais plus lourd que l'œuvre** —
quelque 340 Kio de rapports, roadmaps et contre-expertises pour un seul Livre de chroniques.
La machine de gouvernance fonctionne ; elle mérite d'être gelée dans son état plutôt qu'étendue,
et l'énergie rendue au récit.
