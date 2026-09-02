# 📜 JOURNAL DES MODIFICATIONS (CHANGELOG)

Toutes les modifications notables apportées au dépôt du **Royaume du Babberland** sont consignées dans ce document.

## [2026-XIV] — 2026-09-01, tard en soirée (R1.8 et R1.9 — les deux bornes nées de R1.4 sont fermées le jour même)

La vague R1.4 avait déclaré deux trous plutôt que de les résoudre en silence ; les voici
fermés, dans le grain du projet : **un scellé de plus, une parité vérifiée, deux scénarios
de batterie qui prouvent chacun le mécanisme qu'il vise — et rien d'autre**.

### Ajouté — R1.9 : `gouvernance/GALERIE.sha256`, le dernier corpus d'images sans scellé
* **Le trou, mesuré par R1.4.d** : `images/realistes/` (77 pièces, 211 Mio) n'était scellé
  par rien — `ICONOGRAPHIE.sha256` couvre les 28 maîtres du volume, la charge des vignettes
  ne regarde que les dérivés. Un cliché retouché dont on **oubliait** de régénérer les
  vignettes passait (retouché **et** régénéré, il bloquait : J1).
* `gouvernance/GALERIE.sha256` (77 lignes), gravé par le nouveau but **`make galerie`**,
  vérifié par `make scelle` — donc par `make controle` et par l'étape de gel en tête de
  chaîne, avant toute régénération (le placement de R1.4.h vaut pour lui aussi : le scellé
  protège les octets commités, le rendu régénéré a ses propres contrats).
* **Mesure jointe, conforme au ticket** : +77 lignes de scellé, **0 octet de plus en CI**
  (les fichiers sont déjà dans le checkout ; `sha256sum` les lit en ~1,3 s).
* La dépendance pressentie à R1.6 (LFS) s'est révélée inutile : le scellé lit des octets
  commités, où qu'ils habitent — une migration LFS ne changera que le canal de lecture.

### Ajouté — R1.8 : la parité modèle ↔ workflow installé, vérifiée au lieu d'espérée
* **Le trou, hérité d'E-17/F-01** : le dépôt versionne les modèles (`sources/github_actions_*.yml`)
  **et** leurs copies installées (`.github/workflows/*.yml`), parce qu'une App sans le droit
  `workflows` ne peut pas poser les secondes. `make workflows` les écrivait côte à côte, et
  **rien ne vérifiait qu'elles concordent** : un `|| true` glissé à la main dans le workflow
  installé désalignait la chaîne de son contrat, en silence — la classe E-09/C-01, celle que
  quatre audits ont poursuivie partout ailleurs.
* Deux `cmp` octet à octet dans `make scelle`, et une **19ᵉ étape CI dédiée**, bloquante
  d'emblée (« Parité modèle ↔ workflow installé (R1.8) »).
* **Borne d'honnêteté, écrite dans le YAML** : la CI exécute le workflow **installé** ; si
  les deux fichiers divergent, l'échec ne dit pas lequel porte la vérité — il force la
  question. `make workflows` la règle dans le sens du modèle, et le diff de revue fait foi.

### Batterie — 25 → **27 scénarios (27/27)**, chacun jugé par son propre mécanisme
* **J1bis** : la retouche de J1 (rectangle noir sur `babber_ier_l_ancien.png`), vignettes
  **pas** régénérées — exactement le cas qui passait avant R1.9. Refusé par `scelle` seul.
* **W1** : `pdf_fingerprint.py --check` neutralisé par `|| true` dans le workflow installé,
  modèle intact — exactement le cas qui passait avant R1.8. Refusé par `scelle` seul.
* Nouveau juge **`vue_scelle`** (le pendant de `vue_frais`) : un scénario de garde-fou doit
  être refusé par le mécanisme qu'il prouve, pas par un contrôle voisin — sans quoi il ne
  prouverait rien. Mesure du 1ᵉʳ septembre 2026 : 2 min 41 s pour les 27 scénarios.

### Mis à jour
* `Makefile` (buts `galerie` et `scelle` élargi), les deux modèles de workflows **et leurs
  copies installées** (resynchronisées par `make workflows`, comme le contrat l'exige
  désormais), `README.md`, `gouvernance/CI_LIMITES.md`, `ROADMAP_2026_II.md`.
* Comptes tenus à jour : CI de continuité à **19 étapes, 0 tolérante** ; `batterie.yml`
  annonce « Vingt-deux fautes refusées, cinq éditions acceptées ».

**Rejoué avant livraison** : `make controle` vert (12 vérifications + les scellés élargis),
`make batterie` **27/27**, `make scelle` idempotent après `make galerie`, YAML des deux
workflows validé au parseur, et les deux nouveaux scénarios éprouvés aussi en isolation
(refus par `scelle` seul, témoin intact accepté).

---

## [2026-XIII] — 2026-09-01, dans la soirée (R1.4.a-v3 et R1.4.c–g — la CI n'a plus une seule étape tolérante)

**Clôture de R1.4.** Après R1.4.b (Arbre) et R1.4.h (gel des archives) le même jour, les
six sous-tickets restants sont livrés : **Atlas (v3), Hymne, Vignettes, et les trois étapes
de la chaîne du PDF**. Le workflow de continuité passe de **6 étapes tolérantes sur 18** à
**0**. Ce n'est pas un durcissement de plus, c'est le retournement d'une hypothèse : la
chaîne ne demande plus aux artéfacts d'être **les mêmes octets**, elle leur demande d'avoir
**le même contenu** — et elle le dit, composante par composante, dans une annotation lisible.

### Ajouté — `sources/sceaux.py` : la mécanique commune des sceaux (200 lignes, quatre artéfacts)
* **Une famille de règles, pas quatre.** Variantes acceptées, sections du scellé, annotations
  de check-run, cérémonie d'acceptation (`--write` / `--accepter` / `--check` / listage) :
  tout ce que R1.4.b avait dû inventer dans un seul script est rendu réutilisable, et
  `empreinte_arbre.py` est **repassé dessus sans changer de contrat** — vérifié : la section
  `ARBRE GÉNÉALOGIQUE` de `gouvernance/ARTIFACT_SIGNATURES.sha256` est identique octet pour
  octet avant et après le remaniement (seule la graphie d'un commentaire d'école était à
  reprendre, `<étiquette>`).
* **`comparer_composantes()`** : une charge est une somme de `cle:valeur`, et la divergence
  nomme **la** composante fautive. La question « bruit de rendu ou dérive de contenu ? »
  cesse d'être une intuition : `svg`/`html` qui bougent = la carte a changé (délibération,
  re-gravure) ; seul `16x16box`/`encre` = un environnement de rendu (acceptation).
* **Le canal d'annotation est obligatoire, y compris en succès** (`::notice charge=… connue=…`) :
  les journaux d'étape passent par Azure Blob, injoignables depuis l'environnement d'agent —
  la trace de ce qu'une machine a réellement produit est la seule chose qui ne se négocie pas.

### Ajouté — R1.4.c : `sources/empreinte_hymne.py`
* Charge `frames|rate|bits|chan|profil|pcm8|crete` : géométrie du signal, **enveloppe RMS par
  fenêtre de 250 ms** quantifiée sur 8 bits, PCM replié sur 8 bits, amplitude crête au millième.
  Un ULP de libm ne la fait pas bouger ; permuter deux notes de même durée, si.
* **L'audit RIFF promis par le ticket est fait, et exposé** : `--chunks` énumère les chunks ;
  l'enregistrement de référence ne contient que `fmt ` et `data` — **aucun horodatage**. Un
  chunk ajouté par une future version de `wave` resterait ignoré par la charge **et signalé**
  au diagnostic : une tolérance doit être nommée, pas devenir un angle mort.
* Étape CI : `git diff --exit-code` remplacé par le `--check` ; but `make empreinte-hymne` ;
  `--check` dans `make controle`.

### Ajouté — R1.4.d : `sources/empreinte_vignettes.py`
* Lot des 77 WebP comparé **par contenu décodé** (grille 8×8 BOX quantifiée par vignette,
  liste triée hachée) plus `nb`, `largeur` et `octets` (mesure de diffusion signalée, non
  contractée). Le `git diff` avait ici un second défaut, plus grave que la fragilité : il ne
  comparait que ce qui était **commité** — une vignette périmée que la machine de référence
  reproduisait à l'identique passait comme une lettre.
* `--grilles` imprime les 77 empreintes courtes (~800 octets) : deux environnements se
  comparent **par annotation**, sans journal d'étape et sans manifeste à entretenir.
* But `make empreinte-vignettes` ; `--check` dans `make controle`.

### Durci — R1.4.a-v3 : l'Atlas, dont le contrat n'était pas appelé
* **Le défaut n'était pas l'empreinte, c'est l'étape** : elle lançait `generate_map.py` puis
  `check_geography.py`, sous `continue-on-error`, **sans jamais consulter**
  `gouvernance/ARTIFACT_SIGNATURES.sha256`. Le contrat vivait dans le dépôt, pas dans la
  chaîne — la classe exacte du constat E-09, en pire (là, rien n'était même tenté).
* Le PNG n'est plus échantillonné **NEAREST 16×16** (un pixel lu sur cent : la fragilité
  elle-même, et la cause probable des échecs de PR #25 qu'on n'avait pas pu lire) mais
  **moyenné BOX 16×16 quantifié sur 16 niveaux + proportion d'encre**, comme l'Arbre.
* **Migration assumée** : la section v2 (`atlas_svg`/`atlas_png`/`atlas_html`, trois SHA-256
  nus) est **remplacée** par `atlas_lot` + `atlas_variante_reference-locale`. Un contrat
  que la chaîne n'a jamais appliqué n'a pas de compatibilité à protéger.
* **Les trois options du ticket sont écartées, et c'est écrit** : image Docker épinglée
  (geler une machine pour un problème de sens), seuil de tolérance (mesure R1.4.b : il
  n'existe pas), régénération-gravure en CI (E-21 l'interdit).

### Durci — R1.4.e, R1.4.f, R1.4.g : la chaîne du PDF, trois `continue-on-error` retirés
* Les trois étapes portaient `continue-on-error: true  # R1.4 — voir note Atlas` : un
  **héritage de formulation**, pas une mesure. La non-reproductibilité binaire qui avait fait
  mettre l'Atlas en mode tolérant ne les concernait pas — elles ne comparent pas d'octets.
* Ce que chaque retrait corrige, noir sur blanc : l'étape de **régénération** ne vérifiait
  rien du tout (un générateur qui plante passait) ; **`check_pdf.py`** et la **fraîcheur**
  pouvaient dire vrai sans que le run bronche. Une CI verte avec un volume publié périmé
  (risque n° 1 du rapport RA-2026-IV-01) n'est plus une issue possible.
* R1.4.g donne au PDF sa **section de variantes d'environnement** (`PDF CANONIQUE` dans
  `ARTIFACT_SIGNATURES.sha256`, `pdf_fingerprint.py --accepter '<charge>' <étiquette>`),
  hiérarchisée sans ambiguïté : `gouvernance/pdf_fingerprint.txt` **reste** le contrat
  canonique, seul re-gravé par `make empreinte` ; la variante n'excuse qu'un rendu observé
  ailleurs. La CI grave toujours zéro.
* `--check` émet son `::notice charge=… connue=…` : la divergence du runner est **mesurée**,
  plus supposée.

### Nouveau — workflow `.github/workflows/batterie.yml` : le contrôle du contrôle, à horaires
* **Le trou que la batterie laissait.** `make batterie` est la seule preuve que les contrôles
  mordent ; il ne tournait **que** sur la machine de qui pense à le lancer. Or la défaillance
  propre à ce projet n'est pas la faute dans le texte, c'est le **contrôle émasculé** : C-01
  (un `|| echo` qui rend une étape infaillible) a survécu à quatre audits avant d'être vu.
* Un job **distinct**, à horaire (lundi 03:17 UTC) et à la demande (`workflow_dispatch`) :
  la batterie coûte 2 min 26 s (mesure du 1ᵉʳ septembre 2026, 24 scénarios à ce moment-là —
  25 et 2 min 29 s après P1c, plus bas ; `time make batterie`), réécrit des scellés dans ses laboratoires et n'a rien à dire d'un commit qui
  ne touche ni sources ni artéfacts — elle n'a donc rien à faire sur chaque push.
* **Deux pas de plus que le script local** : la preuve que l'isolation est vraie
  (`git diff --quiet` + `git status` sur l'arbre de référence, après la course) et que les
  scellés n'ont pas bougé. Une promesse de laboratoire qui ne vérifie pas sa paillasse.
* `workflow_dispatch` et `timeout-minutes: 20` ajoutés à `continuite.yml` (run manuel avant
  une Release ; un run qui s'éternise n'est pas un run qui vérifie).

### Mesuré — le canari CI, et ce qu'il a fallu voir deux fois
* **Run #33573944229 : rouge, une seule étape — l'Atlas.** L'annotation disait déjà l'essentiel :
  les cinq composantes structurelles (`svg`, `html`, `taille`, `mode`, `encre`) **identiques** à
  `reference-locale`, seule `16x16box` dans l'inconnu. Autrement dit la carte n'avait pas bougé,
  son rendu si — mais **compter** le divergence exigeait la grille, et le diagnostic de l'Atlas ne
  la donnait pas. Ajoutée au commit suivant (même formule que l'Arbre), elle a rendu le verdict
  mesurable : **3 cellules sur 256, un seul niveau chacune**, sous le titre et sur les étiquettes
  de la forêt, encre intacte. FreeType 2.12 ↔ 2.13, exactement la signature de R1.4.b.
* La mutation témoin A2, elle, déplace **4 cellules d'amplitudes 2, 6 et 7 niveaux et change
  l'encre**. Les deux distributions se touchent par le **nombre** et pas par l'**amplitude** :
  la preuve, pour l'Atlas, qu'aucun seuil ne sépare le bruit du contenu. La variante du runner a
  donc été **acceptée à la main** (`atlas_variante_ci-ubuntu-24.04-py3.12`), pas tolérée.
* **Ce que le rouge a révélé de non prévu** : une étape bloquante **arrête la chaîne**. Atlas
  échouant en position 9, les étapes 10 à 16 n'avaient pas tourné — leurs sceaux n'étaient pas
  conformes, ils n'avaient pas été évalués. Un canari rouge n'est pas un canari qui a tout vérifié :
  la preuve reste le run **vert complet**, dont les `::notice` consigneront les quatre charges.
* PNG du runner 99 129 o contre 98 814 o ici : même image, autre compresseur — ce que la charge
  ignore par construction, et ce que `git diff --exit-code` aurait appelé une faute.

### Validé — batterie portée de 20 à 24 scénarios, tous conformes
* **Trois fautes nouvelles, une par sceau branché** — chacune refusée **par le seul** contrôle
  ajouté aujourd'hui : `A2` PNG d'Atlas noyé d'un rectangle noir (textes et données intacts) →
  `empreinte_atlas` ; `H1` hymne rejoué graine 1848 (même partition, même 72,5 s, même promesse)
  → `empreinte_hymne` ; `J1` photographie réaliste retouchée **et** ses vignettes régénérées →
  `empreinte_vignettes`. Les `CONTROLES` de la batterie intègrent les quatre empreintes : sans
  quoi elle prouvait les dents des contrôles d'hier.
* **Une édition légitime nouvelle (`V4`), qui teste l'autre sens du contrat** : régénérer sur
  une graine étrangère, **lire la charge produite** dans le message d'échec, l'accepter à la
  main sous une étiquette — et la chaîne laisse passer. Si `--accepter` n'existait pas, V4 le
  dirait ; si ce n'était qu'un `|| true` déguisé, V4 le dirait aussi.
* Diagnostic mesuré des trois fautes, dans l'ordre attendu : l'Atlas diverge sur
  `16x16box` **et** `encre` (le rendu, pas la structure), l'hymne sur `profil` et `pcm8`
  (`frames` intact : la durée promise tient), les vignettes sur `grilles` seul — le poids du
  lot, sorti de la charge pour cette raison, n'y figure plus que comme signalement.
* `make controle` : **12 vérifications + les scellés, 0 échec** ; YAML des deux workflows
  validé au parseur (18 et 7 étapes, 0 `continue-on-error`).

### Mesuré (acte II du canari) — la fraîcheur du PDF, et ce que le runner a vraiment dit
* **Run #33574244756** : les six étapes durcies **passent toutes** sur le runner — dont les deux
  charges neuves, **identiques à la référence locale** : vignettes `grilles:b0bb7402…` (le contenu
  décodé ne dépend pas de l'encodeur, c'était la thèse du ticket) et hymne
  `frames:1598625|…|crete:0.720`. Reste la fraîcheur du PDF, rouge, avec
  `pages:29|images:24|placements:25` conformes et le seul `fingerprint` dans l'inconnu.
* **Refus de conclure là-dessus** : le diagnostic a été ajouté (`texte=` et `disposition=` dans les
  deux annotations), un run de plus a été demandé, et la mesure est tombée —
  `texte=8296cf53ba12` **identique** des deux côtés, `disposition` `cd6fdb58…` contre `7f47b597…`.
  Cause nommée : `derive_bytes()` encode en JPEG `quality=78, optimize, progressive`, donc le
  bitstream appartient à la libjpeg du moteur, et `page_image_hashes()` hachait **ces octets-là**.
  Le PDF était le dernier artéfact de la chaîne signé sur ses **conteneurs** et non sur son
  **contenu**.
* **Deux actes, distincts** : (1) `texte` devient un **champ contracté** de
  `gouvernance/pdf_fingerprint.txt` (comparé, machine-indépendant — la table du canari le prouve),
  `disposition` y est consignée en commentaire, informative et non comparée, et l'écart est
  **nommé** : `CONTENU : … à corriger, pas à accepter` si le texte bouge, `EMBALLAGE` si seul
  l'empreinte combinée bouge. Accepter une variante ne peut plus effacer une dérive de texte.
  (2) `pdf_variante_ci-ubuntu-24.04-py3.12` acceptée **sur ces nombres**, dans `PDF CANONIQUE`.
* **Une limite nouvelle, déclarée en ticket** : **R1.10** (signature du PDF par **identité** de
  planches plutôt que par haché de leurs octets — la voie qui rendrait la variante inutile, avec
  son contre-poids écrit : ce que le scellé des maîtres devrait alors garantir).
* Re-gravure de `pdf_fingerprint.txt` (acte d'assentiment) : `fingerprint`, `pages`, `images`,
  `placements` **inchangés**, deux lignes ajoutées. Le volume publié, lui, n'a pas été touché.
* **Et le garde-fou, mesuré** : la clause ne valait pas d'être écrite sans qu'on la teste au
  pire usage — accepter une divergence de texte comme si c'était un rendu. Nouveau scénario
  **P1c** dans la batterie : une date du volume est altérée, le volume est réimprimé, la charge
  inédite est **acceptée à la main comme une variante**, et `pdf_fingerprint.py --check` refuse
  quand même (`variante_acceptée_mais_texte_divergent`). Batterie **25/25 en 2 min 29 s** —
  avec une vue de contrôle dédiée (`vue_frais`), pour qu'un scénario de garde-fou ne soit jamais
  validé par un contrôle voisin du sien.
* **Verdict du canari — le run vert complet (#33575391219), 18 étapes sur 18, aucune tolérante** :
  hymne et vignettes donnent sur le runner **la charge de la référence locale** (contrat
  machine-indépendant, aucune variante à graver) ; Atlas et Arbre donnent leur variante
  d'environnement **nommément acceptée** ; le PDF, `connue=variante-acceptee:ci-ubuntu-24.04-py3.12`.
  C'est la preuve bloquante que ce lot promettait : non pas « un canari est rouge puis devient
  vert », mais cinq annotations qui disent, à chaque run, quelle charge a été vue sur quelle
  machine et au titre de quel contrat.

### Documenté — constats C-02, C-03, C-04 du rapport RA-2026-IV-01
* **C-02** (achevé) : le README n'annonce plus « 7 étapes » tolérantes.
* **C-03** : les comptages **inexpliqués sont retirés, pas réexpliqués**. « 4 post-step »
  (README, ROADMAP, CHANGELOG 2026-XI) et « 22 sous-étapes » (`CI_LIMITES.md`) ne décrivent
  rien de mesurable : le workflow a 18 étapes (16 nommées + `actions/checkout` +
  `actions/setup-python`), **aucune** section `post:`. Un compte qu'on ne peut pas vérifier
  est un compte qui mentira tout seul dans six mois — le précédent « 6 contre 7 » a déjà coûté
  une PR. Les chiffres du jour sont pris au **parseur YAML**, pas à un grep.
* **C-04** : `getdata()` n'est plus appelé nulle part (l'Atlas passe par `tobytes()` comme
  l'Arbre) — le `DeprecationWarning` Pillow qui pollue `make controle` depuis des jours a
  disparu avec la réécriture, sans qu'il ait fallu attendre Pillow 14 (2027-10-15).
* `gouvernance/CI_LIMITES.md` : sections « Statut R1.4.a-v3 », « R1.4.c et R1.4.d »,
  « R1.4.e–g » ; table des sept artéfacts régénérés (tous **bloquants**) ; les causes de
  non-reproductibilité deviennent une **mémoire**, avec post-scriptum sur ce qui s'est résolu
  sans être investigué ; et **ce qui est trouvé en route, déclaré** : `images/realistes/`
  (211 Mio) n'est scellé par rien.
* Deux **tickets nouveaux** ouverts plutôt que des notes en l'air : **R1.8** (parité
  modèle ↔ workflow installé — rien ne vérifie qu'ils concordent) et **R1.9** (sceller la
  galerie réaliste, que le sceau des vignettes ne garde qu'à moitié).

## [2026-XII] — 2026-09-01 (R1.4.h — Gel des archives : mode strict restauré, vérifié avant régénération)

### Corrigé — `RAPPORT_ANALYSE_2026_IV.md`, constat C-01
* **Constat** : l'étape CI « Gel des archives (G et H intacts) et des maîtres d'illustration » ne pouvait pas échouer — `sha256sum --check … || echo "::warning::…"` ; et aucun contrôleur Python ne vérifie les scellés (le seul verrou réel était `make scelle`, local).
* **Mesure (annotation de check-run du run #33568899178)** : `ICONOGRAPHIE.sha256 a des écarts` est émis sur **chaque run, y compris les verts** — faux positif structurel : le scellé couvre `images/arbre_genealogique_complet.png`, le runner régénère l'arbre (étape R1.4.b) en une variante légitime (FreeType 2.13, R1.4.b) avant le gel, et la vérification post-régénération comparait le rendu du runner au maître commité. Le `|| true` masquait donc le diagnostic **et** la garde.
* **Correctif** : `sha256sum --check --quiet` restauré (un écart = échec du run) ; étape **déplacée en tête de chaîne** (après `py_compile`, avant toute régénération) pour valider l'arbre de travail tel que commité (contrat du gel, E-18) ; le rendu régénéré reste régi par `empreinte_arbre.py` (R1.4.b).
* **Réfutation honnête** : la correction « naïve » (retirer `|| true` sans déplacer l'étape) aurait rendu la CI **rouge permanente** — l'étape échoue sur le rendu du runner. Le déplacement n'est pas une commodité, il est la condition du strict.
* **Validation** : `py_compile` + YAML parsé (18 étapes, gel strict en position 6) + scellés vérifiés localement (`make scelle` : G/H intactes, 28 maîtres conformes) ; la preuve bloquante viendra du run CI de cette PR sur `main`.

### Fait — `RAPPORT_ANALYSE_2026_IV.md` (RA-2026-IV-01)
* Nouveau rapport d'analyse du 1ᵉʳ septembre 2026 : `make controle` 12/12, batterie 20/20, état distant vérifié ; constats C-01 (gel non bloquant), C-02 (README « 7 étapes » → 6), C-03 (comptages « 22 sous-étapes / 4 post-step » inexpliqués), C-04 (DeprecationWarning Pillow `getdata()`, Pillow 14, 2027-10-15).

### Corrigé — documentation (suites du rapport)
* `README.md` : « 7 étapes » → « 6 étapes » (constat C-02) ; ligne CI_LIMITES de la table de gouvernance mise à jour (R1.4.c–g restants, R1.4.h livré).
* `ROADMAP_2026_II.md` : R1.4.h ✅ (livré), limitation connue « 7 étapes » → « 6 étapes », section « Reste ouvert » mise à jour (restent R1.4.c–g).
* `gouvernance/CI_LIMITES.md` : section « Statut R1.4.h » (mesure, cause, correctif, ce que le gel ne fait pas) ; note sur la dépréciation Node.js 20.
* `.github/workflows/continuite.yml` et modèle `sources/github_actions_continuite.yml` : identiques (mis à jour ensemble).

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
