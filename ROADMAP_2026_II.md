# 🗺️ ROADMAP ÉDITORIALE ET TECHNIQUE — ROYAUME DU BABBERLAND

**Référence** : RM-2026-II · Feuille de route en quatre horizons
**Établie le** : 27 août 2026, en complément de `RAPPORT_ANALYSE_2026_II.md` (RA-2026-II-01)
**Hypothèse de cadence** : une session d'agent ou une séance d'atelier par livrable, soit ≈ 1 ticket de l'horizon 0 par jour, ≈ 1 horizon 2 « livre » par semaine
**Convention de priorité** : `P1` bloque la crédibilité du volume publié · `P2` bloque l'industrialisation · `P3` enrichit le canon · `P4` diffuse

---

## Vue d'ensemble

**Version visuelle** de cette page : `gouvernance/index.html` — page autonome, aucune dépendance ; à servir par `python3 -m http.server 8090 --directory gouvernance`.

```
HORIZON 0          HORIZON 1              HORIZON 2                  HORIZON 3
VERROUILLER        INDUSTRIALISER         ÉTENDRE LE CANON           DIFFUSER
(0 – 7 jours)      (2 – 6 semaines)       (T4 2026 → T2 2027)       (2027)
─────────────      ─────────────────      ─────────────────────      ─────────────────
6 tickets · P1-P2  7 tickets · P2         9 tickets · P3             6 tickets · P4
≈ 1 j de travail   ≈ 3 j de travail       ≈ 6 semaines éditoriales   ≈ 3 semaines
│                  │                      │                          │
└─ R0.1 PDF complet└─ R1.1 gate d'empreinte└─ R2.1 Livre VIII          └─ R3.1 site de lecture
   R0.2 autorité    R1.2 env reproductible    (institutions)              R3.2 Chroniques en PDF
      du MD         R1.3 manifeste + gel      R2.2 Registre des avis      R3.3 canon en données
   R0.3 README      R1.4 CI complète             1–6 (décrets)              structurées
   exécutable       R1.5 tag + Release        R2.3 Parité Poutine chiffrée R3.4 licence & citabilité
   R0.4 CI prête    R1.6 maîtres PNG          R2.4 Code de la Fraîcheur   R3.5 résumé bilingue
   R0.5 index &     R1.7 source unique        R2.5 Calendrier des fêtes   R3.6 rite de publication
      gel d'archives   de l'arbre             R2.6 démographie + carte         + Livre II des Chroniques
                                             R2.7 lacunes ✅ (Avis 10)        (1889–1914)
                                             jurées S1–S7, 1 fixée
                                             R2.8 Chroniques Livre II
                                             R2.9 registre des personnages
```

**Règle de dépendance unique** : rien de l'horizon 2 ne doit être publié avant la fin de l'horizon 1, faute de quoi chaque ajout de contenu rouvrirait les défauts d'emballage (E-07/E-09) au lieu de les amplifier une seule fois.

---

## HORIZON 0 — Verrouiller le volume 2026-I

> Objectif : que le PDF de référence montre **tout** ce que le texte promet, et que les commandes du README fonctionnent ailleurs que chez leur auteur. Aucun changement de contenu canonique ici, uniquement de la mise en conformité.

### R0.1 · Compléter le PDF canonique — les trois planches manquantes `P1` ✅
- **Constat** : E-07, E-08 (Babette-Marine, avers/revers du 1 Babber, Babetons divisionnaires absents du volume publié).
- **Action** : rendre `IMAGE_AFTER` capable d'accueillir **plusieurs images par ancre** (valeur `list[tuple[str, str]]`), puis déclarer les trois planches :
  - `GÉNÉRATION II : LES BÂTISSEURS (1892–1914)` → `[hortense_du_grain, babette_marine]` ;
  - `1. La Pièce de 1 Babber d'Or et d'Argent (Le Babber Bimétallique)` → `piece_1_babber_or_avers_revers` ;
  - `3. La Pièce de 6 Babetons (Le Six-Pack)` → `pieces_babetons_divisionnaires` (avec la légende du dossier iconographique).
  Et, dans `rich()`, supprimer **la phrase entière** `🖼️ *Visuel officiel : …*` au lieu du seul chemin, pour tarir les « Visuel officiel : » orphelins.
- **Effort** : ~25 lignes · 20 min · **Résultat attendu** : 22 → 24-25 pages, 11 → 14 illustrations, `check_pdf.py` à 14/14.
- **Fait le jour où** : l'extraction texte du PDF contient les 14 légendes et qu'aucune occurrence de `Visuel officiel : ` (suivi d'espace) ne subsiste sans image dans les 40 points voisins.

### R0.2 · Inverser l'autorité des contrôles `P1` ✅
- **Constat** : E-09 — `check_pdf.py` et `check_continuity.py` déduisent l'attendu du **générateur** ; l'oubli d'insertion est structurellement invisible.
- **Action** : (1) l'ensemble attendu d'illustrations vient de `` `images/…` `` dans le MD canonique ; (2) toute référence du MD non rendue doit être **soit insérée, soit exemptée par une ligne explicite** `<!-- hors-PDF: motif -->` ; (3) compter les images par **haché de flux**, non par nom de XObject.
- **Effort** : ~15 lignes dans chaque script · 30 min · **Fait le jour où** : retirer une image de `IMAGE_AFTER` fait échouer la CI (test négatif rejoué, comme pour E-01).

### R0.3 · Rendre le README exécutable partout `P1` ✅
- **Constat** : E-11 — `python -m pip install reportlab pillow` échoue en PEP 668 ; polices codées en dur ; `pypdf` non documenté comme requis par `check_pdf.py`.
- **Action** : ajouter `requirements.txt` épinglé (`reportlab`, `pillow`, `pypdf` — versions relevées dans l'environnement de référence : 5.0.1 / 12.3.0 / 6.16.2), un bloc d'installation en venv, et une découverte de polices avec repli :
  ```python
  def find_font(name):
      for d in ("/usr/share/fonts/truetype/dejavu", "/Library/Fonts",
                str(Path(os.environ.get("LOCALAPPDATA","") ) / "Microsoft/Windows/Fonts"),
                "/usr/local/share/fonts"):
          p = Path(d) / name
          if p.is_file(): return p
      raise SystemExit(f"police {name} introuvable — installer fonts-dejavu-core")
  ```
- **Fait le jour où** : `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && make tout` passe sur Linux, macOS et Windows (ou la matrice CI le prouve).

### R0.4 · Activer réellement la CI `P1` ✅ livré le 1ᵉʳ septembre 2026
- **Constat** : E-14.1, E-17 — `sources/github_actions_continuite.yml` dormait en « proposition » ; le jeton d'App `arena-ai-coding-agent` n'avait pas la permission `workflows` (E-17), rendant impossible la création de `.github/workflows/`.
- **Action** : `make workflows` (copie du modèle vers `.github/workflows/continuite.yml`) ; permission `workflows` accordée à l'installation de l'App (depuis `github.com/settings/installations`) ; corrections de compatibilité Ubuntu runner (`--break-system-packages`, `fetch-depth: 0`, `ref: pull_request.head.ref`).
- **Livraison** : PR #22 mergée en squash sur `main` (commit `9f527f3`). Workflow actif (**18 étapes** — la mention « + 4 post-step » était une erreur de comptage, retirée ce soir sur le constat C-03 : le workflow ne contient aucune section `post:`). Première exécution verte : run #8 (2026-09-01T21:46:19Z).
- **Limitation connue à la livraison** : 6 étapes portaient `continue-on-error: true`, la régénération des artéfacts binaires (Atlas, Hymne, Vignettes, PDF) n'étant pas reproductible au bit près entre machines. **Levée le 1ᵉʳ septembre 2026** : R1.4 (8 sous-tickets R1.4.a à R1.4.h) **intégralement livré** — le contrat n'est plus l'égalité des octets mais une charge sémantique en variantes acceptées. Historique complet : `gouvernance/CI_LIMITES.md`.

### R0.5 · Indexer le dépôt et gel d'archivage `P2` ✅ sauf l'endonyme
- **Constat** : E-14.3 (le README n'indexe pas le rapport de révision ; endonyme `Babbersland-` vs `Babberland`), E-13 (95 % de H dupliqué dans I, sans contrôle).
- **Action** : ajouter au README une section « Gouvernance & audits » (rapports RR/RA, roadmap, registre des décrets à venir) ; déclarer dans l'en-tête de H **et** du PDF G la liste des fichiers `ARCHIVÉS — non modifiables` ; décider une fois pour toutes de l'orthographe du dépôt (recommandation : conserver le nom du dépôt, ajouter une ligne « *Babbersland* : graphie du registre d'import, l'endonyme canonique est *Babberland* »).
- **Fait le jour où** : `grep -c "Gouvernance" README.md` = 1 et un `gouvernance/ARCHIVE.md` énumère les fichiers figés.

### R0.6 · Micro-corrections éditoriales à faible risque `P2` ⏸ arbitrage attendu
Application des arbitrages E-16 déjà documentés, une fois la décision prise : bannière « quarante-neuf ans » ou datation du registre (e), homogénéisation « trente et un ans » (d), intitulé §V de la chronologie aligné sur 1998–2010 (b), tableau des symboles monétaires `B` / `Bt` en tête du Livre IV (a).
**Effort** : 4 lignes · 10 min · **Ne pas faire** sans l'aval éditorial : ces points touchent au texte canonique.

---

## HORIZON 1 — Industrialiser la chaîne

> Objectif : qu'un decree (ajout, correction, nouvelle édition) se produise en une commande et qu'une régression devienne impossible à publier.

| ID | Ticket | Détail | Effort | Dépend de |
|---|---|---|---|---|
| **R1.1** ✅ | **Gate d'empreinte sémantique** (E-10) — *livré par anticipation avec R0.4* | Le PDF n'est pas reproductible à l'octet (noms `FormXob.*` aléatoires de ReportLab ; `rl_config.invariant=1` inefficace, testé). La CI ne diff donc **pas** les binaires : elle compare `md5(nb_pages ‖ texte normalisé ‖ tri(hachés des flux image))`. Recette validée lors de l'audit : empreinte `42bfd823…` identique sur trois builds. Ajouter `sources/pdf_fingerprint.py` (~25 lignes) + l'empreinte de référence dans `MANIFEST.sha256`. | 1 h | R0.4 |
| **R1.2** | **Environnement reproductible** | `Makefile` (`env`, `arbre`, `pdf`, `controle`, `tout`), `requirements.txt` épinglé, `.python-version` (3.12), matrice CI `ubuntu / macos / windows` pour les seuls contrôles (le PDF comparé par empreinte). | 2 h | R0.3 |
| **R1.3** ✅ | **Manifeste d'archive et gel** | **Livré le 1ᵉʳ septembre 2026.** `gouvernance/MANIFEST.sha256` (gravé par `make manifest`, `sources/make_manifest.py`) + vérification `sources/check_manifest.py --check` en CI (`make controle`). **Périmètre ajusté à la réalité des scellés** : la liste « 2 PDF + 14 PNG = 16 lignes » du ticket datée de l'audit recouvrait des corpus qu'un scellé scelle déjà. Le manifeste scelle donc *ce que rien ne scellait par octets* — le corpus canonique livré : `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`, `CHRONOLOGIE_MAITRESSE_1847_2026.md`, `sources/arbre_genealogique_complet.svg`. Délégués : PDF → `pdf_fingerprint.txt` (ses octets sont non-déterministes, on ne les hache pas) ; 28 masters → `ICONOGRAPHIE.sha256` ; 77 réalistes → `GALERIE.sha256` ; archives G/H → `ARCHIVE.sha256` (R0.5). Un changement de contenu d'un livrable se règle par un re-grave explicite dans le même commit (E-13 rendu mécanique). | 2 h | R0.5 |
| **R1.4** ✅ | **CI de bout en bout** | **Clos le 1ᵉʳ septembre 2026.** Étapes prévues (continuité, arbre, empreinte du PDF, `check_pdf.py`, manifeste, publication) et état mesuré : **18 étapes, 0 tolérante**, dont douze vérifications et **quatre sceaux d'artéfacts** (Atlas, Arbre, Hymne, Vignettes) comparés par charge sémantique en variantes acceptées (`sources/sceaux.py`) — plus le gel des archives et des maîtres, placé avant toute régénération (R1.4.h), et la pièce jointe de relecture humaine. Restent hors du périmètre de ce ticket : `check_manifest.py` (c'est R1.3) et le job de publication (c'est R1.5). | 3 h | R1.1, R1.3 |
| **R1.4.a** ✅ | **Empreinte sémantique de l'Atlas** | **Livré le 1ᵉʳ septembre 2026 (v3).** Le défaut n'était pas l'empreinte, c'est que **l'étape CI ne l'appelait jamais** : elle régénérait et vérifiait les données, sous `continue-on-error`, sans consulter le contrat gravé (classe E-09). v3 : `empreinte_atlas.py --check` branché dans l'étape ; charge recomposée en **composantes nommées** (`svg\|html\|taille\|mode\|16x16box\|encre`) pour que l'annotation dise **qui** a bougé ; PNG comparé par moyennage BOX 16×16 quantifié (l'échantillonnage NEAREST 16×16 de v2, un pixel lu sur cent, était la fragilité même) ; modèle « variantes acceptées » de R1.4.b, gravé `atlas_lot` + `atlas_variante_reference-locale` (la section v2, en trois SHA nus jamais appliqués, est remplacée — pas de compatibilité à maintenir). **Aucune des trois options envisagées n'a été prise** : ni image Docker épinglée (geler une machine pour un problème de sens), ni seuil de tolérance (il n'existe pas, mesure R1.4.b), ni gravure en CI (E-21). Preuve : batterie A2 (PNG noyé d'encre) refusée par `empreinte_atlas` seul. **Canari CI mesuré** (runs #33573944229 puis #33574049627, ce dernier ayant ajouté la grille au diagnostic pour que la divergence se compte au lieu de se deviner) : le runner diverge sur **3 cellules 16×16 d'un seul niveau**, structure et encre intactes → variante `ci-ubuntu-24.04-py3.12` **acceptée à la main** ; la retouche A2, elle, déplace 4 cellules de 2 à 7 niveaux et bouge l'encre — le seuil de tolérance est écarté pour l'Atlas avec les mêmes nombres que pour l'Arbre. Nota : l'Atlas bloquant en position 9 **arrête la chaîne**, les runs rouges n'ont donc pas évalué les quatre étapes suivantes ; la preuve reste le run vert complet. — Historique v2 : ⏳ **Reprise R1.4.a-v2 (PR #25) le 1ᵉʳ septembre 2026** : `sources/empreinte_atlas.py` livré (60 lignes, trois empreintes SHA-256 sémantiques : SVG : viewBox/ids/data-since/classes/toponymes ; PNG : dim/mode/perceptual 16×16 NEAREST ; HTML : ids/classes/h1/h2/dates), stockage dans `gouvernance/ARTIFACT_SIGNATURES.sha256`, but `make empreinte-atlas`. **L'empreinte fonctionne en local mais l'étape reste en `continue-on-error: true`** : impossible d'investiguer la cause exacte en CI (logs Azure Blob et artifacts inaccessibles depuis l'environnement d'agent). **R1.4.a-v3** à faire : (a) image Docker épinglée, (b) ajustement de l'empreinte (normalisation grayscale), ou (c) stratégie régénération + gravure (analogue à `pdf_fingerprint.py`). Voir `gouvernance/CI_LIMITES.md` § « Statut R1.4.a-v2 ». | 1 h | R1.1 |
| **R1.4.b** ✅ | **Empreinte sémantique de l'Arbre** | **Livré le 1ᵉʳ septembre 2026** (PR #26) : `sources/empreinte_arbre.py`, modèle **« variantes acceptées »**. Mesure décisive rendue possible par le diagnostic en **annotation de check-run** (les journaux Azure Blob étant injoignables — douleur R1.4.a-v2) : le runner diverge du rendu de référence sur **3 cellules 16×16 d'un niveau** (FreeType 2.12 ↔ 2.13), zone qui chevauche la plus petite retouche de contenu (titre gommé : 2 cellules) → aucune tolérance chiffrée ne convient ; on grave donc exactement les variantes de rendu observées (`reference-locale`, `ci-ubuntu-24.04-py3.12`) dans `gouvernance/ARTIFACT_SIGNATURES.sha256` : toute autre variante est une dérive **bloquante**, acceptée si légitime par `--accepter '<charge>' <étiquette>` (assentiment tracé). `--write`/`--accepter`/`--check`, but `make empreinte-arbre`, `--check` dans `make controle`. Tests rejoués sur le modèle final : regen conforme ; nœud ajouté **et** titre gommé détectés (code 1) ; 1 pixel/bruit tolérés (même grille ; bit à bit : `ICONOGRAPHIE.sha256`) ; charge invalide refusée. Bonus : le canal annotation + grille détaillée est **réutilisable pour R1.4.a-v3** (Atlas). | 30 min | R1.4.a |
| **R1.4.c** ✅ | **Empreinte sémantique de l'Hymne** | **Livré le 1ᵉʳ septembre 2026** : `sources/empreinte_hymne.py`, charge = `frames\|rate\|bits\|chan\|profil\|pcm8\|crete` — géométrie du signal, **enveloppe RMS par fenêtre de 250 ms** quantifiée sur 8 bits, PCM replié sur 8 bits (sensible à l'ordre des notes, insensible à un ULP de libm), amplitude crête au millième. L'audit RIFF promis est fait et **exposé** : `--chunks` énumère les chunks, le WAV de référence ne contient que `fmt ` et `data` (aucun horodatage) ; tout chunk ajouté par une future version de `wave` est ignoré par la charge **et signalé** au diagnostic — une tolérance doit rester nommée. `git diff --exit-code` retiré de l'étape, étape bloquante, `--check` dans `make controle`, but `make empreinte-hymne`. Preuve : batterie H1 (graine 1847→1848, même partition, même durée) refusée par `empreinte_hymne`. | 30 min | R1.4.a |
| **R1.4.d** ✅ | **Empreinte sémantique des Vignettes** | **Livré le 1ᵉʳ septembre 2026** : `sources/empreinte_vignettes.py`, lot par contenu **décodé** (grille 8×8 BOX quantifiée par vignette, liste triée hachée) plutôt que par octets du conteneur, plus `nb` et `largeur` (promesses du diffuseur) ; le poids du lot est signalé au diagnostic, jamais contracté. Un ré-encodage libwebp différent ne bouge pas ; un maître oublié de régénérer bouge. **Effet de bord utile, à consigner** : `images/realistes/` (77 pièces, 211 Mio) n'est scellé par rien — `ICONOGRAPHIE.sha256` ne couvre que les 28 maîtres de `images/`. Le sceau des vignettes est donc la seule garde de la galerie, et incomplète : un maître retouché **sans** régénération passe. D'où le ticket **R1.9** ci-dessous. Preuve : batterie J1, refusée par `empreinte_vignettes` seul. | 1 h | R1.4.a |
| **R1.4.e** ✅ | **Empreinte sémantique du PDF** | **Livré le 1ᵉʳ septembre 2026.** Le PDF était déjà géré par `pdf_fingerprint.py` (R1.1) ; le `continue-on-error` de l'étape de régénération datait d'un héritage de formulation (« voir note Atlas »), pas d'une mesure : cette étape ne comparait rien, donc **un générateur qui plantait passait**. Retiré : l'échec du générateur est une faute. La chaîne du volume — régénération → `check_pdf.py` → fraîcheur — est intégralement bloquante. | 15 min | R1.1 |
| **R1.4.f** ✅ | **Durcissement de l'étape Artéfact publié** | **Livré le 1ᵉʳ septembre 2026** : `continue-on-error: true` retiré de l'étape `check_pdf.py`. Bénin en effet — la preuve attendue est le run CI de la PR qui porte ce ticket (29 pages, 24 flux, 23 légendes appariées, sous le même ReportLab et les mêmes DejaVu que la machine de référence). | 15 min | R1.4.e |
| **R1.4.g** ✅ | **Durcissement de l'étape Fraîcheur** | **Livré le 1ᵉʳ septembre 2026** : `continue-on-error: true` retiré, et l'étape ne grave toujours rien (E-21). Le PDF reçoit en plus sa **section de variantes d'environnement** (`PDF CANONIQUE` dans `gouvernance/ARTIFACT_SIGNATURES.sha256`, `--accepter '<charge>' <étiquette>`), hiérarchisée : `pdf_fingerprint.txt` reste LE contrat canonique, la section n'excuse qu'un rendu observé ailleurs. `--check` pose `::notice charge=… connue=…` à chaque run. **Canari mesuré** (run #33574438077) : `pages`/`images`/`placements` et le **`texte` extrait** sont **identiques** entre la référence et le runner ; ne diverge que la **`disposition`** — les octets des flux JPEG, encodés par la libjpeg du moteur. D'où, en même temps, un contrat **durci là où c'était gratuit** : `texte` devient champ **comparé** de `pdf_fingerprint.txt`, `disposition` consignée en commentaire (informative), et l'écart **nommé** (`CONTENU` à corriger / `EMBALLAGE` à accepter) — accepter une variante ne peut plus couvrir une dérive de texte. La variante du runner a été gravée sur ces nombres, pas sur une inférence. **Ce qui reste connu** : l'empreinte retient le nombre de pages, et l'identité des *pixels* n'est pas ce que la table établit (mesuré par le canari de l'Atlas) — R1.2 le ferait disparaître en amont, **R1.10** aussi en changeant la signature de nature. | 15 min | R1.4.e |
| **R1.4.h** ✅ | **Gel des archives : retour en mode strict** | **Livré le 1ᵉʳ septembre 2026** (PR #28) : `sha256sum --check --quiet` restauré sur `gouvernance/ARCHIVE.sha256` et `gouvernance/ICONOGRAPHIE.sha256`, mode diagnostic supprimé. **Anticipé sur R1.4.a–g car orthogonal à la non-reproductibilité binaire** : le gel compare les octets *commités* — or le runner régénère l'arbre (couvert par ICONOGRAPHIE.sha256) en une variante légitime différente (R1.4.b), d'où un faux positif après régénération, masqué jusqu'ici par le mode diagnostic. L'étape est donc **déplacée en tête de chaîne** (après `py_compile`, avant toute régénération) ; le rendu régénéré reste régi par `empreinte_arbre.py` (R1.4.b), le scellé protège les octets commités (E-18). | 15 min | — |
| **R1.5** | **Politique de version et Release** | Renuméroter le canon comme un produit éditorial : `v2026-I` re-posé sur `main` (le tag actuel désigne le sommet d'une branche de PR), puis `v2026-II` au prochain décret, **Release GitHub** avec les deux PDF et le `MANIFEST`. Une Release = un décret = une page de notes (quoi de neuf, ce qui change d'état « ouvert » à « fixé »). | 1 h | R1.3 |
| **R1.6** ⚠️ moitié livrée | **Iconographie : maîtres hors dépôt** | Mesures : 37,2 Mio de PNG → 9,4 Mio quantifiés (−75 %, dégradation) → 4,7 Mio en JPEG q90 (−87 %, dégradation) → **0 %** en gardant les maîtres hors dépôt et en laissant `prepared_image()` produire les dérivés. **Livré le 30 août 2026 (la moitié « écran »)** : versions compressées dédiées à l'écran = 77 vignettes WebP (`make vignettes`, 220 Mio → 4,65 Mio) **et le portail les charge** (grilles en vignettes, maîtres en lightbox à un clic ; un bug de syntaxe JS du portail 2026-V a été corrigé au passage). **Reste** : la sortie des binaires du magasin Git — runbook complet et mesure du blocage dans `gouvernance/LFS_MIGRATION.md` (le batch LFS répond 200, l'upload des objets vers le S3 de GitHub est bloqué depuis l'environnement d'agent ; `make lfs` prépare la variante A′, le push final reste à une machine avec accès CDN). | 3 h | R1.3 |
| **R1.10** | **Signature du PDF par identité de planches** | Né du canari R1.4.g. Le volume est le seul artéfact dont l'empreinte hache les **octets** des flux embarqués, donc la libjpeg du moteur : d'où une variante à accepter (et un `texte` devenu champ dur pour que l'acceptation ne puisse pas couvrir une dérive de contenu). La voie machine-indépendante par construction, éprouvée le même soir sur les vignettes (charge **identique** sur le runner) : hacher, par planche, l'**image décodée** et la résoudre contre les maîtres — l'identité `stem`, pas le bitstream. **À ne pas faire sans le peser** : une retouche de pixels d'un maître re-scellé ne bougerait plus l'empreinte du volume ; il faudrait alors que le scellé des maîtres fasse la pleine mesure du pixel, ce qu'il fait (bit à bit) — l'arbitrage est donc réel mais pas gratuit.  | 2 h | R1.4.g, R1.2 |
| **R1.8** ✅ | **Parité modèle ↔ workflow installé** | **Livré le 1ᵉʳ septembre 2026.** `make workflows` posait les deux copies côte à côte, et rien ne vérifiait qu'elles concordent : un `.github/workflows/*.yml` modifié à la main (ou un modèle oublié de resynchroniser) désalignait la chaîne de son contrat, en silence — le genre de dérive que quatre audits ont déjà poursuivie ailleurs (E-09, C-01). Livré : deux `cmp` octet à octet dans `make scelle` (donc dans `make controle`), et une étape CI dédiée — la 19ᵉ, bloquante d'emblée, avec sa borne d'honnêteté écrite dans le YAML : la CI exécute le workflow installé, donc un désalignement force la question sans dire qui a raison (`make workflows` la règle dans le sens du modèle). Preuve : scénario **W1** de la batterie — un `\\|\\| true` glissé à la main dans `continuite.yml`, modèle intact, refusé par `scelle` seul. | 15 min | R1.4 |
| **R1.9** ✅ | **Sceller la galerie réaliste** | **Livré le 1ᵉʳ septembre 2026.** `images/realistes/` (77 pièces, 211 Mio) était le seul corpus d'images du dépôt sans scellé : `ICONOGRAPHIE.sha256` couvre `images/*.png` (28 maîtres du volume), la charge des vignettes (R1.4.d) ne regarde que les dérivés. Un cliché retouché dont on oublie de régénérer les vignettes **passait**. Livré, dans le grain du projet : `gouvernance/GALERIE.sha256`, gravé par `make galerie`, vérifié par `make scelle` et par l'étape de gel en tête de chaîne (avant toute régénération, comme R1.4.h l'exige). Mesure jointe, conforme au ticket : **+77 lignes de scellé, 0 octet de plus en CI** (les fichiers sont déjà dans le checkout). La dépendance à R1.6 s'est révélée inutile : le scellé protège les octets commités, où qu'ils habitent — LFS n'y changera que le canal de lecture. Preuve : scénario **J1bis** de la batterie — la retouche de J1 sans régénération des vignettes, refusée par `scelle` seul. | 30 min | R1.4.d |
| **R1.7** | **Source unique de l'arbre** (E-15) | Générer `arbre_genealogique_complet.svg` depuis `generate_genealogy.py` (le PNG devient un rendu du SVG via `cairosvg`, ou le SVG reste un export) ; contrôle de parité étiquettes/géométrie tant que deux fichiers subsistent. | 2 h | — |

---

## HORIZON 2 — Étendre le canon (matière nouvelle, par décrets)

> Objectif : combler les trous **identifiés par le projet lui-même** (section VIII de la chronologie, E-16.g/h) plutôt qu'inventer à côté. Chaque livret = un Avis numéroté = un ticket de version.

| ID | Livret | Contenu à rendre, lacune à fermer | Effort | Arbitrage requis |
|---|---|---|---|---|
| **R2.1** | **Livre VIII · Les Institutions du Royaume** | Le corpus cite sans jamais les décrire : Conseil des Sages (composition, pouvoir de décision), Banque nationale, Monnaie royale de Pabst City, Police royale de la Fraîcheur, Chancellerie, Grand Argentier. Un tableau de 6 institutions (fondation, mandat, titulaire en 2026, texte fondateur) suffit à les rendre crédibles. | 1 j | — |
| **R2.2** | **Registre des Avis royaux n° 1 à 6** | E-16.f : la série commence à n° 5. Rétablir (ou créer rétroactivement et **assumer comme création**) les avis 1-4 : « avis » = l'acte par lequel on incorpore un élément au canon — le registre devient du coup le *processus* de ce projet, documenté chez lui. Prévoir le formulaire : objet, motivation, date, signature, effet sur la chronologie. | 1 j | — |
| **R2.3** | **Parité Poutine, chiffrée** | L'étalon monétaire est nommé depuis 1847 mais jamais défini. Fixer : 1 Babber = *n* kg de fromage en grain à 15 °C + clause de révision. Ferme E-16.a (symboles `B`/`Bt`) dans le même mouvement. | 0,5 j | valeur de référence |
| **R2.4** | **Code de la Fraîcheur (loi organique n° 2)** | L'« Obligation thermique » et le Pabstgate s'appuient sur un Code inexistant. Texte en 8-10 articles (plage 2-4 °C, thermomètre constitutionnel, cloche du scandale, sanctions, exceptions du Bouffon d'État). | 0,5 j | — |
| **R2.5** | **Calendrier national et jours chômés** | E-16.h : 17 mai, 12 octobre, 15 juillet, 1ᵉʳ avril, 15 h 01, vendredi soir, Fête de la Double Garniture. Une table unique (date, nom, objet, obligations, texte qui l'institue) + une mention des lacunes ouvertes. | 0,5 j | — |
| **R2.6** | **Démographie et géographie chiffrées** | E-16.c. **Livré en proposition le 27 août 2026** (comme les Chroniques : bandeau « non décrété », 2026-I intact). Atlas temporel `geographie/index.html`, gazetteer `sources/geographie.py`, carte SVG à couches, PNG, `check_geography.py`, analyse GEO-2026-II-01, roadmap G0–G3. Lecture retenue : 5 500 urbains (canon) + 1 500 forestiers (proposé) + 0 alpin = **7 000** mini-McLouches ; Monts Froissés = jardin du Palais, absents avant le 15 juillet 1962. **Décret restant : Avis n° 7** (`geographie/ROADMAP.md` G2.1). | 1 j | tonalité — *tranchée en proposition, pas en canon* |
| **R2.7** ✅ | **Fermeture des lacunes volontaires — ou gel explicite** | **Livré le 2 septembre 2026 (Avis royal n° 10).** L'instruction a d'abord trouvé trois inventaires pour un seul registre (Serment : 5 ; présente roadmap : 5 ; Chronologie § VIII : 4) et une promesse de garde tenue pour deux silences sur cinq. **Inventaire arrêté à sept** (S1–S7) + **une fixation** (F1 : quatre degrés de la branche collatérale). Règle de partage : on **jure** ce qui ne porte rien, on **fixe** ce dont une pièce du corpus dépend — ici l'arbre officiel, dont le trait pointillé traverse quatre bandes sans s'arrêter sur un nom ; on **requalifie** ce qui n'a pas eu lieu (S7 : la première pierre du port, que le registre P-1 ne consigne pas). Tout silence est **borné**. Garde : `canon/silences.json` + `sources/check_silences.py` (parité registre ↔ Serment, perce-ment, attestation et rétro-contrôle de F1, chasse aux lacunes non décrétées), branchés à `make controle`, à une 21ᵉ étape CI et à la batterie (31 scénarios). | 1 j | **décision structurante — rendue** |
| **R2.8** ✅ | **Chroniques, Livre II — *Les Bâtisseurs* (1889–1914)** | Livre I couvre 1798–1889 en 7 tranches et laisse volontairement l'Article 4 au Dormeur. Le livrable courant est l'édition fusionnée unique du Livre II, sous-titrée *Le Silence et l'Aqueduc* : régence posthume de la mémoire de Babette, plans de l'aqueduc, **42 bancs**, mort de François-Babber et avènement du Dormeur. Le premier coup de pelle est au printemps 1893 et la mise en service officielle au 12 octobre 1904. Le bandeau « proposé, non décrété » et l'audit d'arithmétique interne sont conservés ; aucune décision future ne choisira entre deux rédactions. | 4-5 j | — |
| **R2.9** | **Registre des personnages** | 18 figures nommées, aucun index. Un dictionnaire biographique d'une page par personnage (dates, titres, attributs, source, statut canonique/chronique) ; il devient aussi la **liste d'autorité** dont les scripts peuvent vérifier les dates, au lieu de motifs texte. | 1 j | — |

---

## HORIZON 3 — Diffuser et faire vivre

| ID | Action | Intérêt | Effort |
|---|---|---|---|
| **R3.1** | Site de lecture statique (GitHub Pages) : rendu HTML du MD canonique, sommaire, légendes, thème parchemin/bleu roi déjà défini par les couleurs du générateur | Un PDF de 3,2 Mio est une excellente archive, un mauvais point d'entrée | 1-2 j |
| **R3.2** | Les Chroniques en volume publié : `generate_chroniques.py` calqué sur celui de l'encyclopédie (les deux partagent style, couverture, signets) | Livre I n'existe qu'en Markdown ; c'est le seul contenu *non* publié | 0,5 j (réutilisation) |
| **R3.3** | Canon en données structurées : `canon/personnages.json`, `canon/evenements.json`, `canon/monnaie.json`, générés **à partir de** 2026-I, et non l'inverse | Fait basculer `check_continuity.py` de la chasse aux chaînes vers la vérification de faits (âges, antériorité des titres, successions) ; condition de R2.9 | 2 j |
| **R3.4** | `LICENSE` + `CITATION.cff` + `CHANGELOG.md` | Un univers partagé sans licence est un univers dont l'usage futur se discute (E-14.3) | 15 min |
| **R3.5** | Édition bilingue FR/EN du seul résumé exécutif (12 pages) | L'humour de registre survit mal à la traduction, le tableau de faits, très bien | 1 j |
| **R3.6** | Rite de publication : à chaque décret, `controle → pdf → release → avis` | Le projet a produit cinq PR en 34 heures ; la dette naît des sessions qui finissent *juste après* la livraison. Un rite écrit évite « livrée en proposition » | 0,5 j |

---


---

## Suivi d'avancement

**Horizon 0 exécuté le 27 août 2026** (feu vert éditorial, dans la foulée de RA-2026-II-01). Dérogations et compléments apportés au plan :

| Ticket | Résultat mesuré | Écart avec le plan |
|---|---|---|
| R0.1 | 24 pages · **14/14** illustrations · 13 légendes · 3,9 Mio | Ancre de la planche divisionnaire déplacée de la section 3 à la section 4 (deux images sous le même titre rejetaient la seconde en page suivante) |
| R0.2 | Couverture contrôle MD→générateur ; 4 tests rejoués sur copie isolée (2 échecs attendus, 1 régression E-01 reproduite et détectée, 1 exemption validée) | — |
| R0.3 | `requirements.txt` épinglé, `Makefile` (7 buts), `find_font()` tri-plateforme + `BABBERLAND_FONT_DIR` | La recherche de polices profite aux **deux** générateurs |
| R0.4 *(état à la livraison)* | Gabarit de workflow **uni le 30 août** : **18 étapes** (les 15 de main — compilation, parité du portail — plus **chroniques**, **hymne** et **vignettes** rejoints depuis la PR #16), posé par `make workflows` dans `.github/workflows/continuite.yml`, scellé des archives G et H et des maîtres d'illustration, but `make workflows` | **Livré le 1ᵉʳ septembre 2026** (PR #22) : permission `workflows` accordée à l'App `arena-ai-coding-agent` (résolution de E-17), corrections de compatibilité Ubuntu runner (`--break-system-packages`, `fetch-depth: 0`, `ref: pull_request.head.ref`). Première exécution verte : run #8. 7 étapes portent `continue-on-error: true` (limitation documentée, ticket R1.4.a–h). **Amorce anticipée de R1.1** (sans elle, la CI régénérait le PDF et le jetait : un volume publié périmé passait) |
| R0.5 | Section « Gouvernance & audits » · `gouvernance/ARCHIVE.md` + `ARCHIVE.sha256` scellant G et H, étape CI bloquante | Décision d'endonyme (nom du dépôt) **laissée à l'éditeur** ; ligne de registre consignée dans le README |
| R0.6 | Non appliqué | Quatre arbitrages attendus, une décision par ligne |
| R1.1 | Livré par anticipation : `sources/pdf_fingerprint.py`, empreinte gravée `a0be4fb3…`, `--check` en CI | R1.1 devient clos ; R1.3 garde le manifeste des 16 livrables à son compte |
| **R1.4.a-v3 · c · d · e · f · g** | **Clos le 1ᵉʳ septembre 2026** : `sources/sceaux.py` (mécanique commune), quatre charges sémantiques branchées en CI, **0 étape tolérante sur 18**, `make controle` à **12 vérifications** (dont quatre `--check` de sceaux), batterie portée à **25 scénarios (25/25)**, dont une tentative de couvrir une dérive de texte en variante acceptée (P1c) ; **canari clos sur un run vert complet (#33575391219, 18/18)** avec les cinq `::notice` des sceaux, workflow `batterie.yml` à horaires + `workflow_dispatch`, DeprecationWarning Pillow retiré (constat C-04) et comptages « post-step / sous-étapes » retirés (C-03) | Deux bornes nouvelles sont nées en route, et déclarées plutôt que silencieusement résolues : **R1.8** (parité modèle ↔ workflow installé) et **R1.9** (sceller la galerie réaliste, que seul le sceau des vignettes regardait à moitié) |
| **R1.8 · R1.9** | **Clos le 1ᵉʳ septembre 2026** (la même journée que leur déclaration) : `gouvernance/GALERIE.sha256` (77 lignes, `make galerie`), vérifié par `make scelle` et par l'étape de gel en tête de chaîne ; parité modèle ↔ installé en deux `cmp` dans `scelle` **et** en 19ᵉ étape CI bloquante ; batterie portée à **27 scénarios (27/27)** — J1bis (cliché retouché, vignettes non régénérées) et W1 (workflow retouché à la main) refusés par `scelle` seul, via le nouveau juge `vue_scelle` (un scénario de garde-fou doit être refusé par le mécanisme qu'il prouve, pas par un voisin) | L'horizon 1 ne compte plus de tickets nés d'un constat non traité ; restaient les tickets de fond (R1.2, R1.3, R1.5, R1.6, R1.7, R1.10) |
| **R1.3** | **Clos le 1ᵉʳ septembre 2026** : `gouvernance/MANIFEST.sha256` (3 livrables canoniques), buts `make manifest` + étape CI `check_manifest.py --check`, manifeste vérifié localement (`make controle`, rubrique « Manifeste vérifié »), échec prouvé pour une modification silencieuse. Le PDF (sémantique) et les images (`ICONOGRAPHIE`/`GALERIE`) restent délégués | Le `Reste ouvert` ne mentionne plus R1.3 ; la CI passe de 19 à **20 étapes, 0 tolérante** |

| **R2.8** | **Résolu le 30 août 2026** : les deux rédactions livrées les 27 et 28 août ont été relues et fusionnées dans `chroniques/LIVRE_II_LES_BATISSEURS.md`, édition unique en 7 tranches (1889–1914), sous-titrée *Le Silence et l'Aqueduc*, avec **42 bancs**, le premier coup de pelle au printemps 1893, le Jour de l'Eau du 12 octobre 1904 et la succession au Dormeur ; les 4 planches sont rattachées à l'Annexe C | L'état à deux rédactions est clos : `chroniques/LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` a été intégré puis supprimé. Aucune décision future ne choisira entre ces textes ; le Livre II fusionné reste **proposé, non décrété**, indépendamment d'une éventuelle ratification canonique ultérieure |
| **hors ticket** | Livré en proposition le 27 août 2026 : `chroniques/LIVRE_III_LAGE_HORIZONTAL.md`, 7 tranches, 1914–1959, bandeau conforme, **2026-I intact** | **Aucun ticket n'existait** : la roadmap ne planifiait que le Livre II (R2.8). Le Livre III suit l'annonce de fin du Livre II, comme le Livre II suivait celle du Livre I. L'article 3 y est proposé nommément, le canon n'attribuant au Dormeur que les articles 1 et 4 ; la naissance de Roger Bontemps n'y est toujours pas datée |
| **hors ticket** | Livré en proposition le 27 août 2026 : `chroniques/LIVRE_IV_LERE_BALNEAIRE.md`, 7 tranches, 1959–1998, bandeau conforme, **2026-I intact** | Points de continuité tenus un par un : le Fou et Ginette exclus de la fondation de McBabber's, commission du Babbersgate présidée par Colette-Pabst (Irène étant morte en 1966), Louche encore prince en 1991. L'hôte de la visite de 1980 est nommé d'après l'archive G, avec avertissement : 2026-I, elle, reste discrète. Première Journée de la Transparence brune et naissance de Roger Bontemps : toujours pas datées |

**Reste ouvert** : R1.2 (matrice macOS/Windows — c'est elle qui rendrait caduques les cérémonies d'acceptation de variantes, en les prévenant en amont), **R1.3 clos le 1ᵉʳ septembre 2026** (manifeste des livrables : `MANIFEST.sha256`, `make manifest`, `check_manifest.py --check` en CI), **R1.4 clos le 1ᵉʳ septembre 2026** (R1.4.a–h livrés ; 18 étapes, 0 tolérante), **R1.8 et R1.9 clos le 1ᵉʳ septembre 2026** (nés de la vague R1.4 et fermés dans la foulée : parité modèle↔workflow en 19ᵉ étape bloquante, galerie scellée par `GALERIE.sha256` ; batterie à 27 scénarios), R1.5 (**re-poser `v2026-I` sur `main` + Release**, à faire avec un accès aux étiquettes), R1.6 (maîtres PNG hors dépôt), R1.7 (source unique de l'arbre), l'horizon 2 sauf **R2.6, R2.7 et R2.8** : R2.6 livré en proposition (atlas temporel ; Avis n° 7 restant — voir `geographie/ROADMAP.md`), **R2.7 clos le 2 septembre 2026 par l'Avis royal n° 10** (sept silences jurés et bornés, une fixation gardée — `canon/silences.json`), R2.8 livré en proposition (Livre II fusionné et Chroniques Livres III–IV, 2026-I intact). Suite à prévoir : **Livre VII des Chroniques** (le Livre VI, livré en proposition, s'arrête en 2026).

**Indicateurs après Horizon 0** — à lire en regard du « Cap ciblé » ci-dessous, qui reste l'état d'avant-exécution :

| Indicateur | Avant | Après |
|---|---|---|
| Illustrations canoniques rendues | 11 / 14 | **14 / 14** |
| Contrôles en CI | 0 | **5 + scellé d'archives** |
| Commandes du README exécutables telles quelles | 0 / 4 | **3 / 4** (`make env`, `make tout`, `make controle` ; reste la matrice multi-OS de R1.2) |
| Constats ouverts | 10 | **4** (E-14.2 tag, E-15 arbre, E-16 arbitrages, R1.6 poids) |

---

## Registre des risques

| Risque | Prob. | Impact | Parade |
|---|---|---|---|
| Le canon enfle plus vite que la chaîne (cadence mesurée : 5 PR fusionnées en 10 h) | **haute** | moyen | Horizon 0 d'abord ; un livret canon = un Avis = un tag |
| Le générateur reste une seconde vérité éditoriale | haute | **élevé** (cf. E-07/E-09) | R0.2 : le Markdown commande, le script exécute, la CI compare |
| Les images de 3 Mio rendent le dépôt pénible | moyenne | moyen | R1.6, mesures déjà faites |
| Les archives G/H sont retouchées pour « arranger » | moyenne | élevé | R1.3 (manifeste) + R0.5 (gel déclaré) |
| Perte du non-reproductible : G n'a plus de source | **acquise** | moyen | R1.3 (hachés) ; assumer « figé » plutôt que promettre « régénérable » |
| Un décret crée une contradiction d'âge | faible | **élevé** | R2.7, R3.3 : vérifier les faits, pas les phrases |
| La CI, activée, est désactivée faute de temps | moyenne | moyen | R1.5 : la publication *passe* par la CI, elle ne peut donc plus être court-circuitée |

## Indicateurs de suivi

| Indicateur | Valeur actuelle | Cible fin H1 | Cible fin H2 |
|---|---|---|---|
| Illustrations canoniques rendues dans le PDF | 11 / 14 (79 %) | 14 / 14 | 100 % |
| Contrôles passifs / actifs | 2 scripts locaux, **0 CI** | 5 contrôles en CI | idem + données |
| Commandes du README exécutables telles quelles | 0 / 4 | 4 / 4 | 4 / 4 |
| Artefacts régénérables depuis le dépôt | 2 / 3 (G non) | 2 / 3 + hachés | 3 / 3 si R1.3 retente G |
| Écarts canon↔réalité mesurés | 10 (E-07 → E-16) | ≤ 3 | 0 ouvert, tous arbitrés |
| Lacunes déclarées restées ouvertes | 5 | 5 | 0 (fixées ou prêtées au silence) |

## Ce qu'il ne faut pas faire

- **Ne pas fusionner H dans I par suppression** : l'intérêt de G et H est d'être la trace de l'état antérieur ; le gel par haché suffit (E-12, E-13).
- **Ne pas poursuivre le diff binaire du PDF** : la cause est dans ReportLab, `invariant` n'y change rien (mesuré) — l'empreinte sémantique obtient le même bénéfice.
- **Ne pas optimiser les PNG par quantification** avant la décision R1.6 : −75 % immédiats, mais les portraits officiels perdent leurs dégradés, ce que le projet a déjà refusé à juste titre.
- **Ne pas incorporer la chronique au canon sans décret** : le bandeau « proposés » est ce qui permet au Livre I d'être libre ; sauter l'étape détruirait la seule protection dont dispose le hors-canon.
- **Ne pas ajouter de génération VIII avant R2.9** : sans index des personnages, chaque nouveau-né dynastique multiplie les surfaces de continuité non vérifiée.

---

*Feuille de route établie à Pabst City, le 27 août 2026, par l'agent Arena.ai (session `arena/01a0421d-babbersland`) · Toutes les mesures citées sont reproductibles : commandes du README + trois régénérations complètes effectuées dans le cadre de RA-2026-II-01.*

**« Une Pabst, une poutine, et on régénère. »**
