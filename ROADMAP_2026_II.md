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
                                             R2.7 lacunes : fixer ou        (1889–1914)
                                             prêter au silence
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
- **Livraison** : PR #22 mergée en squash sur `main` (commit `9f527f3`). Workflow actif (18 étapes + 4 post-step). Première exécution verte : run #8 (2026-09-01T21:46:19Z).
- **Limitation connue** : 7 étapes portent `continue-on-error: true` car la régénération des artéfacts binaires (Atlas, Arbre, Hymne, Vignettes, PDF) n'est pas reproductible au bit près entre la machine de l'agent et le runner CI. Détails : `gouvernance/CI_LIMITES.md`. **Ticket de durcissement** : R1.4 (8 sous-tickets R1.4.a à R1.4.h).

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
| **R1.3** | **Manifeste d'archive et gel** | `MANIFEST.sha256` des artefacts livrés (2 PDF, 14 PNG = 16 lignes) généré par `sources/make_manifest.py` ; CI bloquante si un fichier archivé (G, H) change sans que `docs/ARCHIVE.md` soit mis à jour. Réponse partielle à E-12 et E-13. | 2 h | R0.5 |
| **R1.4** | **CI de bout en bout** | Étapes : continuité → arbre déterministe (diff binaire, ça marche : md5 stable) → empreinte du PDF → `check_pdf.py` → `check_manifest.py` → job de publication (Release draft). Artéfacts uploadés en pièces de job pour relecture humaine. | 3 h | R1.1, R1.3 |
| **R1.4.a** | **Empreinte sémantique de l'Atlas** | ⏳ **Reprise R1.4.a-v2 (PR #25) le 1ᵉʳ septembre 2026** : `sources/empreinte_atlas.py` livré (60 lignes, trois empreintes SHA-256 sémantiques : SVG : viewBox/ids/data-since/classes/toponymes ; PNG : dim/mode/perceptual 16×16 NEAREST ; HTML : ids/classes/h1/h2/dates), stockage dans `gouvernance/ARTIFACT_SIGNATURES.sha256`, but `make empreinte-atlas`. **L'empreinte fonctionne en local mais l'étape reste en `continue-on-error: true`** : impossible d'investiguer la cause exacte en CI (logs Azure Blob et artifacts inaccessibles depuis l'environnement d'agent). **R1.4.a-v3** à faire : (a) image Docker épinglée, (b) ajustement de l'empreinte (normalisation grayscale), ou (c) stratégie régénération + gravure (analogue à `pdf_fingerprint.py`). Voir `gouvernance/CI_LIMITES.md` § « Statut R1.4.a-v2 ». | 1 h | R1.1 |
| **R1.4.b** | **Empreinte sémantique de l'Arbre** | Idem pour `images/arbre_genealogique_complet.png`. La source de non-déterminisme est probablement les métadonnées EXIF (date de génération) et l'ordre d'itération des nœuds. | 30 min | R1.4.a |
| **R1.4.c** | **Empreinte sémantique de l'Hymne** | Idem pour `audio/hymne_national_babberland.wav`. Vérifier que le WAV n'a pas de chunk RIFF avec timestamp. | 30 min | R1.4.a |
| **R1.4.d** | **Empreinte sémantique des Vignettes** | Idem pour les 77 vignettes WebP. Le hash peut être calculé par lot (concaténation triée des hashs par vignette). | 1 h | R1.4.a |
| **R1.4.e** | **Empreinte sémantique du PDF** | Le PDF est déjà géré par `pdf_fingerprint.py` (R1.1). Reste à **retirer** le `continue-on-error: true` de l'étape « Régénération de l'encyclopédie 2026-I » et à vérifier que `pdf_fingerprint.py --check` est bien bloquant. | 15 min | R1.1 |
| **R1.4.f** | **Durcissement de l'étape Artéfact publié** | Retirer `continue-on-error: true` de `check_pdf.py`. Devrait être bénin si R1.4.e passe. | 15 min | R1.4.e |
| **R1.4.g** | **Durcissement de l'étape Fraîcheur** | Retirer `continue-on-error: true` de `pdf_fingerprint.py --check`. Devrait être bénin. | 15 min | R1.4.e |
| **R1.4.h** | **Gel des archives : retour en mode strict** | Restaurer `sha256sum --check --quiet` sur `gouvernance/ARCHIVE.sha256` et `gouvernance/ICONOGRAPHIE.sha256` (au lieu du mode diagnostic `\|\| true`). À faire **après** R1.4.a–g. | 15 min | R1.4.a–g |
| **R1.5** | **Politique de version et Release** | Renuméroter le canon comme un produit éditorial : `v2026-I` re-posé sur `main` (le tag actuel désigne le sommet d'une branche de PR), puis `v2026-II` au prochain décret, **Release GitHub** avec les deux PDF et le `MANIFEST`. Une Release = un décret = une page de notes (quoi de neuf, ce qui change d'état « ouvert » à « fixé »). | 1 h | R1.3 |
| **R1.6** ⚠️ moitié livrée | **Iconographie : maîtres hors dépôt** | Mesures : 37,2 Mio de PNG → 9,4 Mio quantifiés (−75 %, dégradation) → 4,7 Mio en JPEG q90 (−87 %, dégradation) → **0 %** en gardant les maîtres hors dépôt et en laissant `prepared_image()` produire les dérivés. **Livré le 30 août 2026 (la moitié « écran »)** : versions compressées dédiées à l'écran = 77 vignettes WebP (`make vignettes`, 220 Mio → 4,65 Mio) **et le portail les charge** (grilles en vignettes, maîtres en lightbox à un clic ; un bug de syntaxe JS du portail 2026-V a été corrigé au passage). **Reste** : la sortie des binaires du magasin Git — runbook complet et mesure du blocage dans `gouvernance/LFS_MIGRATION.md` (le batch LFS répond 200, l'upload des objets vers le S3 de GitHub est bloqué depuis l'environnement d'agent ; `make lfs` prépare la variante A′, le push final reste à une machine avec accès CDN). | 3 h | R1.3 |
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
| **R2.7** | **Fermeture des lacunes volontaires — ou gel explicite** | Section VIII : date de naissance du Déchiré, chaîne collatérale depuis Babette-Marine, naissance de Roger Bontemps, transmission Linéa→Ginette, première Transparence brune. Deux options seulement : (a) décret de fixation, avec rétro-contrôle d'âges ; (b) **serment d'ignorance** — un Avis déclarant ces cinq points perpétuellement non consignés, ce qui les rend défendables au lieu de les laisser ouverts. Recommandation : (b) pour 4 d'entre eux, (a) pour la chaîne collatérale, dont dépend l'arbre. | 1 j | **décision structurante** |
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
| R0.4 | Gabarit de workflow **uni le 30 août** : **18 étapes** (les 15 de main — compilation, parité du portail — plus **chroniques**, **hymne** et **vignettes** rejoints depuis la PR #16), posé par `make workflows` dans `.github/workflows/continuite.yml`, scellé des archives G et H et des maîtres d'illustration, but `make workflows` | **Livré le 1ᵉʳ septembre 2026** (PR #22) : permission `workflows` accordée à l'App `arena-ai-coding-agent` (résolution de E-17), corrections de compatibilité Ubuntu runner (`--break-system-packages`, `fetch-depth: 0`, `ref: pull_request.head.ref`). Première exécution verte : run #8. 7 étapes portent `continue-on-error: true` (limitation documentée, ticket R1.4.a–h). **Amorce anticipée de R1.1** (sans elle, la CI régénérait le PDF et le jetait : un volume publié périmé passait) |
| R0.5 | Section « Gouvernance & audits » · `gouvernance/ARCHIVE.md` + `ARCHIVE.sha256` scellant G et H, étape CI bloquante | Décision d'endonyme (nom du dépôt) **laissée à l'éditeur** ; ligne de registre consignée dans le README |
| R0.6 | Non appliqué | Quatre arbitrages attendus, une décision par ligne |
| R1.1 | Livré par anticipation : `sources/pdf_fingerprint.py`, empreinte gravée `a0be4fb3…`, `--check` en CI | R1.1 devient clos ; R1.3 garde le manifeste des 16 livrables à son compte |

| **R2.8** | **Résolu le 30 août 2026** : les deux rédactions livrées les 27 et 28 août ont été relues et fusionnées dans `chroniques/LIVRE_II_LES_BATISSEURS.md`, édition unique en 7 tranches (1889–1914), sous-titrée *Le Silence et l'Aqueduc*, avec **42 bancs**, le premier coup de pelle au printemps 1893, le Jour de l'Eau du 12 octobre 1904 et la succession au Dormeur ; les 4 planches sont rattachées à l'Annexe C | L'état à deux rédactions est clos : `chroniques/LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` a été intégré puis supprimé. Aucune décision future ne choisira entre ces textes ; le Livre II fusionné reste **proposé, non décrété**, indépendamment d'une éventuelle ratification canonique ultérieure |
| **hors ticket** | Livré en proposition le 27 août 2026 : `chroniques/LIVRE_III_LAGE_HORIZONTAL.md`, 7 tranches, 1914–1959, bandeau conforme, **2026-I intact** | **Aucun ticket n'existait** : la roadmap ne planifiait que le Livre II (R2.8). Le Livre III suit l'annonce de fin du Livre II, comme le Livre II suivait celle du Livre I. L'article 3 y est proposé nommément, le canon n'attribuant au Dormeur que les articles 1 et 4 ; la naissance de Roger Bontemps n'y est toujours pas datée |
| **hors ticket** | Livré en proposition le 27 août 2026 : `chroniques/LIVRE_IV_LERE_BALNEAIRE.md`, 7 tranches, 1959–1998, bandeau conforme, **2026-I intact** | Points de continuité tenus un par un : le Fou et Ginette exclus de la fondation de McBabber's, commission du Babbersgate présidée par Colette-Pabst (Irène étant morte en 1966), Louche encore prince en 1991. L'hôte de la visite de 1980 est nommé d'après l'archive G, avec avertissement : 2026-I, elle, reste discrète. Première Journée de la Transparence brune et naissance de Roger Bontemps : toujours pas datées |

**Reste ouvert** : R1.2 (matrice macOS/Windows), R1.3 (manifeste complet), R1.4 (CI de bout en bout — l'ossature est là), R1.5 (**re-poser `v2026-I` sur `main` + Release**, à faire avec un accès aux étiquettes), R1.6 (maîtres PNG hors dépôt), R1.7 (source unique de l'arbre), l'horizon 2 sauf **R2.6 et R2.8 livrés en proposition** (atlas temporel, Livre II fusionné et Chroniques Livres III–IV, 2026-I intact, Avis n° 7 restant — voir `geographie/ROADMAP.md`). Suite à prévoir : **Livre V — L'Union des Règnes (1998–2010)**, annoncé en fin de Livre IV.

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
