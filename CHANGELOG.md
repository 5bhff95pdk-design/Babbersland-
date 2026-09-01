# 📜 JOURNAL DES MODIFICATIONS (CHANGELOG)

Toutes les modifications notables apportées au dépôt du **Royaume du Babberland** sont consignées dans ce document.

## [2026-XI] — 2026-09-01 (R1.4.b — Arbre durci via « variantes acceptées », étape BLOQUANTE)
### Le chemin, honnêtement (trois étapes en une journée)
1. **v1** : empreinte unique (moyennage BOX 16×16 quantifié, encre), étape rendue bloquante — **CI rouge** sur le runner.
2. **Diagnostic enfin possible** : `--check` émet désormais sa charge en **annotation de check-run** (`::notice` systématique, `::error` détaillée avec grille 16×16 complète) — canal lisible depuis l'environnement d'agent via l'API Checks, contrairement aux journaux d'étape (Azure Blob, injoignables — douleur historique de R1.4.a-v2). **Première mesure réelle du runner jamais obtenue.**
3. **Mesure** : le runner diverge sur **3 cellules sur 256, chacune d'un seul niveau de quantification** (antialiasing FreeType 2.12 vs 2.13) — pile dans la zone de la plus petite retouche de contenu (titre gommé : 2 cellules, même amplitude). **Aucune tolérance chiffrée ne sépare bruit de rendu et retouche** : on grave donc l'**ensemble des variantes observées**, sans tolérance.

### Ajouté — `sources/empreinte_arbre.py` (modèle « variantes acceptées »)
* **`sources/empreinte_arbre.py`** (~110 lignes) : la conformité = la variante courante `size:…|mode:RGB|16x16box:<md5>|ink:…` **appartient à l'ensemble gravé** dans `gouvernance/ARTIFACT_SIGNATURES.sha256` (`reference-locale` + `ci-ubuntu-24.04-py3.12`, toutes deux mesurées). Toute retouche de contenu, même minuscule, produit une variante inédite → échec ; tout nouvel environnement de rendu légitime pareil → échec *diagnostiqué*, puis accepté explicitement par `--accepter '<charge>' <étiquette>` (acte d'assentiment tracé dans git, jamais de bascule silencieuse).
* **Interface** : `[--write [--variante N]] [--accepter CHARGE N] [--check]`. La ligne `arbre_png` du scellé devient le sha256 de l'ensemble trié (tête de contrat à une ligne).
* **Stockage** : section `# === ARBRE GÉNÉALOGIQUE ===` dans `gouvernance/ARTIFACT_SIGNATURES.sha256` (la section Atlas est préservée, et réciproquement).
### Corrigé — l'étape Arbre est désormais BLOQUANTE
* `.github/workflows/continuite.yml` et modèle `sources/github_actions_continuite.yml` : `continue-on-error: true` **retiré**, `empreinte_arbre.py --check` remplace `git diff --exit-code -- images/arbre_genealogique_complet.png`.
* `Makefile` : nouveau but `make empreinte-arbre` ; `empreinte_arbre.py --check` ajouté à `make controle` ; en-tête des buts mis à jour.
### Validé — batterie sur copies (rejouée sur le modèle final)
* Test positif : régénération → conforme à « reference-locale » (code 0) ; bit-stabilité locale confirmée par `md5sum`.
* Tests négatifs : nœud supplémentaire (8 cellules) et titre de Génération I gommé (2 cellules) → **divergence détectée** (code 1) — y compris le titre gommé, qu'une tolérance chiffrée aurait laissé passer.
* Tolérances assumées : 1 pixel retouché, bruit ±2 sur 300 pixels → conformes (même grille) ; la protection bit à bit du fichier tracké reste celle d'`ICONOGRAPHIE.sha256` (E-18).
* Charge invalide → refusée (code 1).
### Mis à jour
* `gouvernance/CI_LIMITES.md` : section « Statut R1.4.b » réécrite (mesure chiffrée, modèle variantes, cérémonie d'acceptation) ; comptage rectifié — le workflow comptait **7** étapes en `continue-on-error` (ce document en annonçait 6, la roadmap disait juste) et n'en compte plus que **6** après R1.4.b.
* `ROADMAP_2026_II.md` : R1.4.b marqué ✅ ; billet « Reste ouvert » actualisé (restent R1.4.c–h ; suite narrative : Livre VII, les Livres I–VI étant livrés).
* `README.md` : `gouvernance/ARTIFACT_SIGNATURES.sha256` (Atlas **et** Arbre) indexé dans la table Gouvernance.

## [2026-X] — 2026-09-01 (R1.4.a-v2 — Atlas durci via empreinte sémantique)
### Ajouté — `sources/empreinte_atlas.py` et `gouvernance/ARTIFACT_SIGNATURES.sha256`
* **`sources/empreinte_atlas.py`** (60 lignes) : calcule trois empreintes SHA-256 sémantiques de l'Atlas (analogue à `pdf_fingerprint.py` pour le PDF) :
  - **SVG** : `viewBox`, ensemble trié des `id`, `data-since`, classes, présence des toponymes canoniques.
  - **PNG** : dimension, mode colorimétrique, somme MD5 des pixels.
  - **HTML** : ensemble trié des `id` et classes, textes des `<h1>`/`<h2>`, présence des dates maîtresses.
* **Interface** : `python sources/empreinte_atlas.py [--write|--check]`. `--write` est un acte d'assentiment, `--check` la comparaison.
* **Stockage** : `gouvernance/ARTIFACT_SIGNATURES.sha256` (nouveau fichier). La section Atlas est ajoutée, le reste du fichier (futurs scellés) est préservé.
### Corrigé — l'étape Atlas est désormais BLOQUANTE
* `.github/workflows/continuite.yml` : `continue-on-error: true` retiré, l'étape appelle `empreinte_atlas.py --check` au lieu de `git diff --exit-code`.
* `Makefile` : nouveau but `make empreinte-atlas` ; ajout dans `make controle`.
* La cause de la non-reproductibilité (cache pip Pillow sur le runner) reste non corrigée, mais n'a plus d'impact : on ne compare plus les octets, on compare le **contenu sémantique**.
### Mis à jour
* `gouvernance/CI_LIMITES.md` : section « Statut R1.4.a-v2 » documentant l'approche, l'implémentation, les tests de validation.
* `ROADMAP_2026_II.md` : R1.4.a marqué ✅.
* `CHANGELOG.md` : entrée 2026-IX corrigée (R1.4.a « diagnostic affiné » devient un préambule à R1.4.a-v2).

## [2026-IX] — 2026-09-01 (R1.4.a — diagnostic affiné, instrumentation Atlas)
### Signalé — l'Atlas n'est PAS bit-à-bit reproductible en CI
* **Diagnostic local** (clone frais, venv, `--break-system-packages`) concluait à une reproductibilité bit-à-bit (`git hash-object` identique avant et après régénération, identique au tracké).
* **En CI** (run #12, PR #24), l'étape échoue. La différence entre la machine de l'agent et le runner CI (cache pip, version de sous-composants Pillow, locale, timezone, ordre d'itération) n'est pas réductible à un test local.
* **Cause identifiée** : `cache: pip` sur `actions/setup-python@v5` peut conserver un état Pillow différent de celui qu'on installe à partir de zéro via `--break-system-packages`.
### Mis à jour — instrumentation de l'étape Atlas
* `continue-on-error: true` **conservé** sur l'étape Atlas.
* Nouvelle instrumentation : en cas d'échec du `git diff`, la sortie capture le `git diff` complet **et** le `sha256sum` des trois fichiers, pour permettre le diagnostic en aval.
* Le `git diff` ne supprime plus la sortie (`{ … && echo atlas-ok; } || { …; exit 1; }` au lieu de `… | tee`).
### Mis à jour
* `gouvernance/CI_LIMITES.md` : section « Statut R1.4.a » corrigée — le diagnostic initial était faux, l'Atlas N'est PAS reproductible en CI, la R1.4.a reste à faire avec une approche différente (image Docker épinglée, ou empreinte sémantique).
* `ROADMAP_2026_II.md` : R1.4.a reste à faire, marqué ⏳.
* `.github/workflows/continuite.yml` : instrumentation ajoutée à l'étape Atlas.

## [2026-VIII] — 2026-09-01 (R0.4 final — CI activée, limitations documentées)
### Ajouté — la CI de continuité est active (ticket R0.4)
* **Permission `workflows` accordée** à l'installation de l'App GitHub `arena-ai-coding-agent` (résolution de E-17) : la création de fichiers dans `.github/workflows/` est désormais autorisée.
* **`.github/workflows/continuite.yml`** : 18 étapes + 4 post-step, à chaque push sur main et sur toute PR. Compilation des sources, continuité, parité canon/portal, chroniques, atlas, arbre, hymne, vignettes, régénération PDF, artéfact, empreinte, scellé des archives, pièce jointe de relecture.
* **PR #22 mergée en squash** sur `main` (commit `9f527f3`). Première exécution verte : run #8 (2026-09-01T21:46:19Z).
### Signalé — 7 étapes de régénération binaire en `continue-on-error`
* Les étapes Atlas, Arbre, Hymne, Vignettes, Régénération PDF, Artéfact, Fraîcheur portent `continue-on-error: true`. Cause : les 6 artéfacts régénérés (SVG, PNG, WAV, PDF, vignettes WebP) sont **reproductibles par run** sur une même machine, mais **non bit-à-bit identiques entre machines** (métadonnées Pillow EXIF, ordre d'itération ReportLab, etc.).
* **`gouvernance/CI_LIMITES.md`** (nouveau) : diagnostic complet, politique envisagée, 8 sous-tickets R1.4.a–h.
* **`ROADMAP_2026_II.md`** : R0.4 = ✅, R1.4 décomposé en 8 sous-tickets avec estimation.
### Signalé — étape « Gel des archives » en mode diagnostic
* `sha256sum --check --quiet` remplacé par `(sha256sum --check … || echo ::warning::…)` pour permettre la lecture du diff exact sans bloquer la CI. À restaurer en strict en R1.4.h.
### Mis à jour
* `ROADMAP_2026_II.md` : R0.4 marqué ✅, R1.4 détaillé en 8 sous-tickets, suivi d'avancement mis à jour.
* `README.md` : section « Gouvernance & audits » enrichie (statut de la CI, lien vers `gouvernance/CI_LIMITES.md`).
* `gouvernance/CI_LIMITES.md` : nouveau document.

## [2026-VII] — 2026-08-30 (portail sur vignettes + runbook LFS)
### Corrigé — le script du portail 2026-V était mort
* **Bug de syntaxe JavaScript** dans le tableau de la galerie (ligne du Prince Babber le Fou, fragment `u.png` en trop) : le bloc `<script>` entier ne se parsertait pas — dictionnaire des personnages, galerie 77 photos et convertisseur monétaire étaient inopérants dans le portail publié. Corrigé ; syntaxe vérifiée (`node --check`) et rendu simulé avec stub DOM (18 cartes personnages + 77 cartes galerie, zéro référence manquante).
### Ajouté — le portail charge les vignettes (R1.6, moitié « écran »)
* `index.html` : les grilles (personnages, galerie, tuiles de chroniques et de régions) affichent désormais les **vignettes WebP** de 640 px (`images/vignettes/`) ; le **maître pleine taille reste un clic plus loin**, dans la visionneuse. Poids de diffusion de la page : **≈ 220 Mio → ≈ 7 Mio** (un héros en taille pleine conservé). Le héros et les lightbox ne bougent pas ; `check_portal.py` et `make controle` restent verts.
### Ajouté — runbook LFS (R1.6, moitié « hors dépôt »)
* **`gouvernance/LFS_MIGRATION.md`** : la procédure complète du passage des binaires en Git LFS (≈ 330 Mio de candidats : 220 Mio de galerie, 78 Mio de maîtres, 22,9 Mio de PDF, 4 Mio d'audio, 4,7 Mio de vignettes), les **mesures du jour** (batch LFS HTTP 200 ; upload des objets vers `github-cloud.s3.amazonaws.com` en **SSL_ERROR_SYSCALL** et upload d'assets vers `uploads.github.com` en **EOF** — le CDN de GitHub est inaccessible depuis l'environnement d'agent) et deux options : **A′** (prospective, ≈ 230 Mio, recommandée si plan gratuit — bande passante LFS : 1 Gio/mois) et **B** (réécriture de l'historique, ≈ 340 Mio → < 5 Mio, **à avis**). La migration n'est pas engagée ici : des pointeurs sans objets casseraient tous les autres clones.
* **`make lfs`** : exécute la variante A′ (track + commit), s'arrête avant le push — l'étape réseau qui reste.
* `README.md` : section « Binaires lourds et Git LFS (R1.6) » ; `ROADMAP_2026_II.md` : R1.6 portée à « moitié livrée ».

## [2026-VI] — 2026-08-29, intégrée au 30 août (rejeu de la PR #16, en conflit avec les PR #17–19)
### Ajouté — le contrôle des chroniques
* **`sources/check_chroniques.py`** (sans dépendance, câblé dans `make controle` et dans la CI) : l'arithmétique interne des chroniques. Sept grandeurs récurrentes (bancs, canaux, arches, villes, régions, kilomètres, population) sont confrontées d'un volume à l'autre, et les **73 cotes d'archives** déclarées en annexe sont comparées deux à deux. Contrat E-19 : une divergence est **résolue ou déclarée** ; une déclaration qui ne décrit plus rien d'observable est une faute.
* **`gouvernance/DIVERGENCES_CHRONIQUES.md`** : le registre que lit ce contrôle. **10 divergences déclarées** — les bancs (40 contre 42, plus deux homonymes : les bancs d'écoliers et les trois bancs publics de l'amende), la population (11 en 1847, 214 au recensement de 1850, 5 en délégation, 800/1 200/3 500 au canon, **7 000 en 2026**) et **huit cotes d'archives en collision**.
* **Trois constats nouveaux, mesurés** : (1) la **cote G-1** est en collision entre le Livre III et le Livre IV — F-02 ne l'avait pas vue ; (2) le **total national de 7 000 âmes ne figure pas dans 2026-I**, qui ne donne que trois villes (5 500 âmes urbaines) : le chiffre le plus cité du Royaume repose sur une chronique proposée ; (3) la **courbe démographique n'est consignée nulle part** — rien ne relie 214 (1850) à 7 000 (2026).
* **Batterie portée à 20 scénarios (20/20)** : trois fautes nouvelles sont refusées par `check_chroniques` — un banc de plus dans le Livre III, une cote réattribuée par le Livre V, une déclaration devenue obsolète — et une quatrième édition, la même divergence **dûment déclarée**, est acceptée : le contrat « résolue ou déclarée » est éprouvé dans les deux sens.

### Rapatrié
* **`RAPPORT_AUDIT_2026_III.md`** (constats **F-01 → F-23**), seul exemplaire existant, qui dormait dans la PR #11 en conflit avec `main`. Bandeau de statut **historique** ajouté : F-01 est pris en charge par la PR #16, F-02 et F-03 sont renvoyés à l'Avis royal n° 7 par le registre des divergences (F-03, la généalogie castorale, y est déclarée hors contrôle automatique — la Chancellerie ne corrige pas la prose d'une chronique par décret d'outillage).

### Ajouté — vignettes du portail
* **`sources/generate_vignettes.py` + `make vignettes`** : vignettes WebP de 640 px dérivées de **chacun des 77 clichés** de `images/realistes/` (le script globbe le dossier, l'inventaire suit la galerie 2026-V), déterministes au bit près (`images/vignettes/`), **220,1 Mio → 4,65 Mio** (−98 %). La motivation d'origine était mesurée sur l'ancienne page du portail (16 planches, **44 Mio → 0,9 Mio**) ; le portail 2026-V (77 photos en taille pleine) branchera ces vignettes dans un suivi. Les maîtres ne sont pas touchés : les scellés d'iconographie restent intacts.

## [2026-V] — 2026-08-29, intégré au 30 août (rejeu de la PR #16)
### Modifié — CI (ticket R0.4)
* **Gabarit uni avec les étapes de main (15) : 18 étapes au total** — l'**hymne national** (`sources/generate_hymne.py` + `git diff --exit-code` sur `audio/hymne_national_babberland.wav`), les **chroniques** (`sources/check_chroniques.py`) et les **vignettes** (`sources/generate_vignettes.py`) manquaient à la CI. Depuis l'Avis royal n° 8, l'enregistrement de référence fait partie de `make tout` ; il était le seul produit de la chaîne que la CI ne contrôlait pas. Reproductibilité au bit près vérifiée localement (graine 1847, bibliothèque standard seule).
* **Blocage ré-mesuré** (E-17 / F-01) : l'installation échoue, des **deux** côtés — `git push` rejeté (« refusing to allow a GitHub App to create or update workflow … without `workflows` permission ») et API *contents* en **403** « Resource not accessible by integration ». Le poussage du reste de la branche, lui, passe : le manque est bien limité au droit `workflows`.
* **Documentation** : `README.md` (§ Activation) et `make workflows` donnent les deux voies de sortie — trois commandes avec un jeton humain, ou l'octroi du droit *Workflows : Read and write* à l'App depuis `github.com/settings/installations`.
### Signalé (relevé lors de l'activation)
* La PR **#11** (audit AUD-2026-III, 18 fichiers) est en **conflit** avec `main` et héberge le seul exemplaire de `RAPPORT_AUDIT_2026_III.md` (constats **F-01 → F-23**, dont la contradiction inter-volumes F-03 et les cotes d'archives en collision F-02 entre les deux rédactions du Livre II). **Rapatrié** : voir **[2026-VI]**.

## [2026-V] — 2026-08-30 (galerie photoréaliste — les 18 figures)
### Ajouté
* **Huit portraits photoréalistes** versés à `images/realistes/` : Hortense du Grain, Irène des Érables, Babber II le Piscineux, Honoré-Pabst & Henri-Grain, Babber le Fou, Ginette de Port Babette, Babber le Déchiré, Ti-Babber. Les **18 figures du canon** ont désormais chacune un cliché.
* **Vingt planches de lieux, offices et chroniques** : Grass City, Palais Royal, Cabane de 1847, Jour de l'Eau, Banque, Gardiens du Kouik-Kouik, Police du Frigo, Confrérie, Géomètres, cuisine de McBabber's, Grande Digue, premier coup de pelle, Fjord des Fûts, Trois-Érables, Série B, Guerre des Cornichons, Nuit des Sept Mille, Conseil des Sages, Hamac Forcé, hymne national.
* **Portail** (`index.html`) : héro du Double Aqueduc, cartes illustrées des cinq régions, dictionnaire des personnages illustré, chroniques et institutions en planches, galerie filtrable (77 photos) et visionneuse.
* `GALERIE_PHOTOS_REALISTES.md` : inventaire porté de 16 à 77, statut hors volume 2026-I rappelé.

### Non modifié
* Maîtres scellés `images/*.png`, encyclopédie 2026-I, empreinte PDF et `ICONOGRAPHIE.sha256` — la galerie reste hors canon tant qu'un Avis ne l'y fait pas entrer.

## [2026-IV] — 2026-08-30 (passe d'audit — constats C1/C5)
### Corrigé
* **Portail racine** : quatre dates du « Dictionnaire des 18 Personnages » alignées sur le canon (`canon/personnages.json` et 2026-I) — Babette Ire **1804**–1892, Hortense du Grain **1840–1922**, Babette-Marine **1836**–1916, Irène des Érables **1882**–1966.
* **Nouveau contrôle** `sources/check_portal.py` (constat C1) : parité du portail contre `canon/personnages.json` — chaque fiche du dictionnaire doit correspondre à *exactement une* fiche du canon et porter les mêmes années de vie. Branché dans `make controle` et dans le workflow de CI (15 étapes), rejoué avec succès en local.
* **Compilation** : `python -m py_compile sources/*.py` entre dans `make controle` et dans la CI (détection d'erreur de syntaxe, constat C7).
* **Convertisseur monétaire** (`index.html`) : affichage reformulé selon le modèle réel — *« 24 Babetons, soit 1 poutine royale (23 bt) et 1 canette (1 bt) »* — au lieu d'un « environ X poutines » opaque (constat C5).
* `README.md` : « les six contrôles » → sept, liste des commandes à jour, workflow « 13 étapes » → 15, paragraphe `check_portal.py`.

## [2026-IV] — 2026-08-29
### Ajouté
* **Hymne national** : `gouvernance/HYMNE_NATIONAL.md` — « Debout, tout doucement », six couplets et un refrain, protocole d'exécution (jamais entre 13 h et 15 h, jamais en courant, ♩ = 60), partition ABC du refrain et table des sources canoniques de chaque couplet. Statut **proposé, non décrété** ; projet d'**Avis royal n° 8** instruit au Registre.
* **Enregistrement de référence** : `sources/generate_hymne.py` + but `make hymne` → `audio/hymne_national_babberland.wav` (72,5 s pile : Pshitt réglementaire, refrain à 17 mesures, silence final de 4 s). Synthèse déterministe — graine 1847, bibliothèque standard seule, partition lue dans le dossier officiel (source unique, le document et le son ne peuvent pas diverger).
### Ratifié (le même jour, sur assentiment royal — la Chancellerie ne connaît pas la lenteur en matière d'hymne)
* **Avis royal n° 8 promulgué** : l'hymne « Debout, tout doucement » entre au canon — ligne au tableau des **Symboles nationaux** de 2026-I, entrée à la **Chronologie maîtresse** (§ VII, année dynastique 2026), événement promu dans `canon/evenements.json` (la proposition, levée, sort de `propositions_declarées`).
* **Chaîne** : `make hymne` entre dans `make tout` (arbre → hymne → PDF → CONTRÔLES → empreinte) ; volume PDF régénéré et **empreinte regravée** — le changement d'empreinte était dit à l'Avis (Art. 4).
* **Récitation de Chancellerie** : `audio/hymne_recitation_partie_1.mp3` et `_partie_2.mp3` — les six couplets et le refrain, voix seule.
### Modifié
* `gouvernance/REGISTRE_DES_AVIS_ROYAUX.md` : projet d'Avis n° 8 (institution de l'hymne) instruit après l'Avis n° 7, toujours en attente de ratification.
* `canon/evenements.json` : la proposition d'hymne entre dans `propositions_declarées` (contrat de parité E-19).
* `README.md`, `Makefile` : le but `hymne` est documenté et rangé hors de `make tout`, comme tout ce qui n'est pas encore décrété.

## [2026-III] — 2026-08-29
### Corrigé (lot C0 de la contre-expertise RC-2026-III-01)
* **Fraîcheur** : l'empreinte sémantique est désormais **ordonnée page à page** (`pdf_fingerprint.py`) — deux illustrations permutées la modifient (E-18). Contrat gravé à nouveau : `708776c8…`.
* **Artéfact** : `check_pdf.py` **apparie chaque planche à sa légende** sur le md5 du dérivé embarqué, et vérifie la double inclusion des contenus ; `check_continuity.py` refuse toute insertion sans promesse du canon (E-22).
* **Données** : nouveau `sources/check_canon.py` — parité de `canon/*.json` avec 2026-I, la Chronologie et le Registre, arithmétique des six successions, contrat `propositions_declarées` (E-19, E-26).
* **Aligné sur le canon** : naissances et décès de Babette Ire (1804), Hortense du Grain (1840–1922), Babette-Marine (1836), Irène des Érables (1882) ; le Dormeur perd son ordinal fantôme ; la monnaie reprend les noms du canon (Six-Pack, Cuivre Populaire, Demi-Babber).
* **Contrôles** : `check_continuity.py` protège les cinq silences sanctifiés et rend un diagnostic lisible quand le générateur est illisible (E-19, E-24) ; `check_geography.py` attrape enfin l'anachronisme des Monts Froissés, cellule par cellule (E-20).
* **Preuve** : la batterie de mutations entre au dépôt — `sources/test_mutations.py`, cible `make batterie`. Seize copies isolées de l'arbre sont malmenées : treize altérations refusées, trois éditions légitimes acceptées, dont le résidu assumé (16 scénarios sur 16 conformes).
* **Chaîne** : `make tout` = `arbre pdf controle empreinte` — graver n'est plus vérifier (E-21) ; `make scelle` joint au contrôle local et scelle les maîtres (E-23).
* **CI (E-23)** : le gabarit `sources/github_actions_continuite.yml` passe à **13 étapes** (parité des données, artéfact apparié, deux scellés) et `make workflows` l'installe ; le talon invalide `main.yml` est retiré de l'arbre de travail. Le poussage du fichier `.github/workflows/*` reste hors de portée d'une App sans le droit `workflows` (E-17) : installation à faire par un humain.

## [2026-II] — 2026-08-29
### Ajouté
* **Livre V des Chroniques** : `chroniques/LIVRE_V_LUNION_DES_REGNES.md` (1998–2010 : Honoré-Pabst & Henri-Grain, Pabstgate de 2004, Guerre des Cornichons).
* **Livre VI des Chroniques** : `chroniques/LIVRE_VI_LE_SIECLE_QUI_LOUCHE.md` (2010–2026 : règne du Louche, faux fromage de 2018, Série B, Ti-Babber, Nuit des Sept Mille).
* **Livre VIII des Institutions** : `gouvernance/LIVRE_VIII_INSTITUTIONS.md` (Gardiens du Kouik-Kouik, Police de la Sieste, Police du Frigo, Géomètres, Confrérie du Secret Brun).
* **Actes & Jurisprudence** :
  * `gouvernance/REGISTRE_DES_AVIS_ROYAUX.md` (Restauration des Avis n° 1 à 4 et projets de décrets).
  * `gouvernance/CODE_DE_LA_FRAICHEUR_ET_PARITE_POUTINE.md` (Code de la Fraîcheur, Formule $\mathbf{1\ \text{฿}}$, calendrier des 7 fêtes).
  * `gouvernance/GUIDE_GASTRONOMIQUE_ET_JEUX_LENTS.md` (Guide des 3 Spatules, Jeux Lents, bestiaire royal).
  * `gouvernance/REGISTRE_DES_PERSONNAGES.md` (Dictionnaire biographique des 18 figures du canon).
  * `gouvernance/SERMENT_D_IGNORANCE.md` (Sanctification des 5 lacunes volontaires).
  * `gouvernance/RITE_DE_PUBLICATION.md` (Protocole en 5 étapes pour toute incorporation).
* **Données structurées** : Dossier `canon/` (`personnages.json`, `lieux.json`, `monnaie.json`, `evenements.json`).
* **Diffusion & Métadonnées** : `EXECUTIVE_SUMMARY.md` (bilingue FR/EN), `LICENSE`, `CITATION.cff`.

## [2026-I] — 2026-08-26
### Consolidé
* Fusion des documents historiques 2026-G et 2026-H dans le canon autonome `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`.
* Intégration de la Génération VII (Ti-Babber) et régularisation de la branche collatérale du Déchiré.
* Émission de la Série B fiduciaire et des 4 valeurs de pièces métalliques.
