# Royaume du Babberland

Archives narratives et iconographiques du Royaume du Babberland.

*Registre d'import : le nom du dépôt s'écrit « Babbersland » ; l'endonyme canonique, seul employé dans les volumes, est **Babberland**.*

## Référence officielle actuelle

1. **`Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf`** — encyclopédie illustrée consolidée et référence canonique autonome (24 illustrations après la campagne 2026-II).
2. **`ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`** — source éditoriale du volume 2026-I ; **c'est elle qui fait foi**, y compris sur la liste des illustrations que le PDF doit montrer.
3. **`CHRONOLOGIE_MAITRESSE_1847_2026.md`** — registre chronologique détaillé, avec règnes, sources et contrôles de continuité.
4. **`images/`** — portraits, numismatique et arbre généalogique illustré (28 maîtres du volume 2026-I).
5. **`images/realistes/`** — galerie photoréaliste du portail (77 clichés, dont les 18 figures du canon) ; hors PDF tant qu'un Avis ne les y fait pas entrer.
6. **`geographie/`** — atlas temporel (proposé, non décrété) : analyse, roadmap, carte SVG/PNG, page `index.html`.

L'édition **2026-I** intègre directement les corrections et ne nécessite aucune règle de préséance documentaire.

## Gouvernance & audits

| Document | Objet |
|---|---|
| `RAPPORT_DE_REVISION_2026_I.md` | Révision générale du 27 août 2026 (RR-2026-I-01) : réserve E-01 levée, contrôles étendus |
| `RAPPORT_ANALYSE_2026_II.md` | Audit technique, éditorial et documentaire (RA-2026-II-01) : constats E-07 à E-16, mesures reproductibles |
| `RAPPORT_DE_CONTRE_EXPERTISE_2026_III.md` | Contre-expertise RC-2026-III-01 : mutations rejouées (E-18 à E-28) ; lot C0 appliqué le 29 août, suivi d'exécution en §6 |
| `ROADMAP_2026_II.md` | Feuille de route en quatre horizons, 28 tickets, risques et indicateurs |
| `gouvernance/LIVRE_VIII_INSTITUTIONS.md` | Proposition Livre VIII (R2.1) : Les 5 corps d'État, gardiens du caillé, police de la sieste |
| `gouvernance/REGISTRE_DES_AVIS_ROYAUX.md` | Registre officiel des Avis royaux (R2.2) : restauration des décrets n° 1 à 4 et suite |
| `gouvernance/CODE_DE_LA_FRAICHEUR_ET_PARITE_POUTINE.md` | Code de la Fraîcheur (R2.4), Parité Poutine chiffrée (R2.3) et calendrier national (R2.5) |
| `gouvernance/GUIDE_GASTRONOMIQUE_ET_JEUX_LENTS.md` | Guide des 3 Spatules royales, Jeux Lents de Pabst City, bestiaire national et marine |
| `gouvernance/REGISTRE_DES_PERSONNAGES.md` | Registre d'autorité des 18 personnages historiques du canon (R2.9) |
| `gouvernance/HYMNE_NATIONAL.md` | Hymne national « Debout, tout doucement » (**décrété par l'Avis royal n° 8**, 29 août 2026) : six couplets, protocole d'exécution, partition ABC et enregistrement de référence (`make hymne`) |
| `canon/` | Données structurées JSON : personnages, monnaie, lieux, événements (R3.3) |
| `gouvernance/ARCHIVE.md` | Politique d'archivage : ce qui est gelé, ce qui ne l'est pas, comment dégeler |
| `gouvernance/ARCHIVE.sha256` | Scellés des archives 2026-G et 2026-H, vérifiés par la CI et par `make scelle` |
| `gouvernance/ICONOGRAPHIE.sha256` | Scellés des 28 maîtres d'illustration, par leur nom (E-18) |
| `canon/` + `propositions_declarées` | Données structurées (R3.3) sous contrat de parité : une affirmation est attestée par le corpus ou déclarée comme proposition |
| `gouvernance/pdf_fingerprint.txt` | Empreinte sémantique du PDF canonique — le contrat de fraîcheur de l'artefact |
| `gouvernance/index.html` | Version visuelle du rapport et de la roadmap (page autonome) |
| `geographie/ANALYSE.md` | GEO-2026-II-01 : ce que le canon situe, ce que le temps interdit, E-16.c en proposition |
| `geographie/ROADMAP.md` | Feuille de route géographique (G0 livré, G2 = Avis n° 7, hors 2026-I) |
| `geographie/index.html` | Atlas interactif 1830–2026 : les Monts n'existent pas avant le 15 juillet 1962 |

## Chroniques narratives (hors canon)

- `chroniques/LIVRE_I_LES_FONDATIONS.md` — *Les Chroniques de l'Ancien, Livre I : Les Fondations (1798–1889)* : histoire du premier roi racontée en sept tranches. Éléments nouveaux **proposés, non décrétés** ; toute addition au canon devra passer par décret et mise à jour de 2026-I.
- `chroniques/LIVRE_II_LES_BATISSEURS.md` — *Livre II : Les Bâtisseurs (1889–1914)*, sous-titré *Le Silence et l'Aqueduc* : **édition fusionnée unique** de la régence de Babette Ire, du refus de l'ordinal II, du chantier du Double Aqueduc, de la naissance du port, du Jour de l'Eau et de la succession de François-Babber au Dormeur. Sept tranches, **quarante-deux bancs**, premier coup de pelle au printemps 1893 et mise en service officielle le 12 octobre 1904. Même statut **proposé, non décrété** ; les lacunes volontaires du canon (filiation de Babette-Marine, naissance de Roger Bontemps, valeur chiffrée de la Parité Poutine) y sont gardées ouvertes et déclarées comme telles. Les quatre planches de chantier sont rattachées à cette édition dans son `Annexe C`.
- `chroniques/LIVRE_III_LAGE_HORIZONTAL.md` — *Livre III : L'Âge horizontal (1914–1959)* : le long règne de Babber le Dormeur, les audiences en hamac, l'Article 1 et l'Article 4.
- `chroniques/LIVRE_IV_LERE_BALNEAIRE.md` — *Livre IV : L'Ère balnéaire (1959–1998)* : le règne de Babber II, les Monts Froissés, l'ouverture de McBabber's en 1986 et le Babbersgate de 1991.
- `chroniques/LIVRE_V_LUNION_DES_REGNES.md` — *Livre V : L'Union des Règnes (1998–2010)* : les jumeaux Honoré-Pabst et Henri-Grain, la crise thermique du Pabstgate de 2004, la Guerre des Cornichons arbitrée par le Déchiré, et l'avènement de Babber Ier le Louche. Même statut **proposé, non décrété**.
- `chroniques/LIVRE_VI_LE_SIECLE_QUI_LOUCHE.md` — *Livre VI : Le Siècle qui Louche (2010–2026)* : le fauteuil retrouvé, la victoire du vrai caillé, la Série B en chanvre pur, le Sommet Pabst-Ketchup, l'avènement de Ti-Babber (Génération VII) et la Nuit des Sept Mille. Même statut **proposé, non décrété**.

## Documents archivés

- `Royaume_du_Babberland_Encyclopedie_Officielle_2026.pdf` — ancien volume 2026-G ;
- `HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md` — ancien supplément 2026-H.

Ils sont conservés pour l'historique éditorial et **scellés par haché** : leur contenu ne se corrige pas (voir `gouvernance/ARCHIVE.md`). Pour les comparer entre eux seulement, 2026-H corrige 2026-G ; pour toute consultation actuelle, utiliser **2026-I**.

## Points de continuité fixés

- En 1984–1986, Babber le Louche est encore **prince** ; Babber II le Piscineux règne et ratifie la création de McBabber's.
- Babber le Fou, né le jour de l'ouverture en 1986, ne participe pas à la fondation du restaurant.
- Ginette, née en 1988, hérite plus tard de la garde de la sauce ; Linéa tient ce rôle à l'origine.
- Irène des Érables, morte en 1966, ne préside pas le Babbersgate de 1991 : Colette-Pabst dirige la commission.
- Babber le Déchiré appartient à une branche collatérale issue de Babette-Marine ; Babber le Fou reste fils unique du Louche et de Linéa.
- Babber le Fou demeure premier dans l'ordre de succession ; Ti-Babber est deuxième.
- Dans « Babber VII », **VII désigne la septième génération**, pas un septième règne.
- Les **vingt-quatre** illustrations promises par 2026-I sont toutes servies dans le volume imprimé (les 4 planches de chantier des chroniques restent hors volume par statut). Une référence `images/…` du Markdown canonique sans ancre dans le générateur est une **erreur de contrôle** — et, symétriquement, une insertion sans promesse du canon en est une (constat E-22).

## Chaîne de production

Tout passe par `make`, qui installe ses propres dépendances dans un venv — les `pip install` directs échouent sur les systèmes récents (environnement géré, PEP 668) :

```bash
make env          # python3 -m venv .venv + pip install -r requirements.txt
make tout         # arbre → hymne → PDF → CONTRÔLES → empreinte (l'ordre est un contrôle, voir E-21)
make controle     # les huit contrôles, sans rien régénérer
make scelle       # gel des archives G et H + scellé des 28 maîtres d'illustration
```

Buts disponibles : `env`, `arbre`, `carte`, `hymne`, `vignettes`, `pdf`, `empreinte`, `controle`, `scelle`, `iconographie`, `batterie`, `workflows`, `tout`, `propre`.

`make batterie` ne contrôle pas le dépôt : il **malmène seize copies isolées** de son arbre (naissances fausses, deux portraits permutés, archive gelée raturée, générateur syntaxiquement cassé, un banc de plus non déclaré, une cote réattribuée, une déclaration obsolète) et vérifie que la chaîne refuse — puis qu'elle accepte quatre éditions légitimes. C'est la seule preuve que les contrôles ont des dents ; elle dure une minute et ne fait pas partie de `controle`, puisqu'elle réécrit des scellés dans ses laboratoires.
**Graver l'empreinte n'est jamais une vérification** : `empreinte` clôt la chaîne et consigne un assentiment ;
la CI, elle, ne fait que `--check`. Un changement d'empreinte voulu se dit à l'Avis. Hors venv : `make PY=python3 …`. Les générateurs cherchent les polices DejaVu sur Linux, macOS et Windows (`BABBERLAND_FONT_DIR` pour forcer un répertoire). L'atlas géographique (`make carte`) est **hors canon** : il ne rentre pas dans `make tout` ni dans le PDF, tant qu'un Avis ne l'a pas ratifié. L'hymne national (`make hymne`), décrété par l'Avis royal n° 8, **entre dans `make tout`** : son enregistrement de référence (`audio/`) se régénère au bit près, partition lue dans le dossier officiel.

## Régénération de l'encyclopédie PDF

```bash
make pdf          # équivalent de : python .venv/bin/python sources/generate_encyclopedie_2026_i.py
```

Le générateur ajoute la couverture, le sommaire, les signets PDF, les en-têtes, la pagination, les tableaux et les illustrations. Les illustrations sont insérées par la table `IMAGE_AFTER`, indexée sur les **titres exacts** du Markdown canonique ; une ancre peut en porter plusieurs.

Après toute modification assumée du volume, regraver le contrat de fraîcheur :

```bash
make empreinte    # grave l'empreinte sémantique dans gouvernance/pdf_fingerprint.txt
```

## Validation de la continuité

```bash
make controle     # ou, individuellement :
python .venv/bin/python -m py_compile sources/*.py
python .venv/bin/python sources/check_continuity.py
python .venv/bin/python sources/check_canon.py
python .venv/bin/python sources/check_chroniques.py
python .venv/bin/python sources/check_pdf.py
python .venv/bin/python sources/pdf_fingerprint.py --check
python .venv/bin/python sources/check_geography.py
python .venv/bin/python sources/check_portal.py
make scelle
```

- **`check_continuity.py`** (sans dépendance) vérifie les titres historiques, l'ordre de succession, les sept livres, les équivalences monétaires, les dates maîtresses, tous les liens d'illustrations, les ancres d'illustrations du générateur (chaque ancre doit exister telle quelle dans 2026-I, faute de quoi l'illustration disparaît silencieusement du PDF), la **couverture** — chaque image promise par 2026-I doit être servie ou expressément exclue par `<!-- hors-PDF: images/x.png — motif -->` — et le bandeau de statut des chroniques.
- **`check_canon.py`** (sans dépendance, constat E-19) fait la **parité des données** : `canon/*.json` contre 2026-I, la Chronologie maîtresse et le Registre des personnages — 18 fiches, sommes de population, échelle monétaire 24 Babetons, événements datés, **arithmétique des six successions** (durée annoncée = soustraction des bornes, chaîne continue, mort = fin de règne). Sa règle : dans un dossier nommé `canon`, une affirmation est soit **attestée** par le corpus, soit **inscrite dans `propositions_declarées`** avec sa source — 1 500 âmes de la forêt et le 12 octobre 1904 y sont, tant que l'Avis n° 7 n'a pas parlé.
- **`check_chroniques.py`** (sans dépendance) fait l'**arithmétique interne des chroniques** : sept grandeurs récurrentes (bancs, canaux, arches, villes, régions, kilomètres, population) confrontées d'un volume à l'autre, et les **cotes d'archives** — la même cote `Q-3` ou `A-34` ne peut pas désigner deux documents différents sans que la collision soit écrite. Sa règle, celle d'E-19 : une divergence est **résolue ou déclarée** dans `gouvernance/DIVERGENCES_CHRONIQUES.md`, et une déclaration qui ne décrit plus rien d'observable est elle-même une faute. Il porte les constats **F-02** (huit cotes en collision, dont une que l'audit n'avait pas vue) et **F-03** (généalogie castorale, déclarée hors contrôle automatique).
- **`check_pdf.py`** (`pypdf`) ouvre le PDF publié et **apparie chaque planche à sa légende, page par page**, sur le md5 du dérivé réellement embarqué : deux portraits intervertis, une planche de trop, une légende sans image sont des échecs (constats E-18, E-22). L'attendu vient du canon, pas du générateur ; la transformée d'image est unique (`sources/babberland_images.py`), partagée par le générateur et les contrôles.
- **`pdf_fingerprint.py --check`** compare l'artefact publié à l'empreinte gravée : le PDF n'est pas reproductible à l'octet (ReportLab nomme ses XObject aléatoirement), donc on compare ce que le lecteur voit — pages, texte, et **hachés d'images ordonnés page à page**. L'empreinte n'est plus un ensemble trié : permuter deux illustrations la modifie (E-18).
- **`check_portal.py`** (sans dépendance, constat C1) fait la **parité du portail racine** : `index.html` contre `canon/personnages.json` — chaque fiche du dictionnaire doit correspondre à *exactement une* fiche du canon et porter les **mêmes années de vie** (peu importe la rédaction : « né le 15 juillet 1962 » ≡ « né 1962 », « Babber Ier le Dormeur » ≡ « Babber le Dormeur »). C'est ce qui a pris le portail en flagrant délit de quatre dates contradictoires avec le canon.
- **`make scelle`** vérifie `gouvernance/ARCHIVE.sha256` (archives 2026-G et 2026-H) **et** `gouvernance/ICONOGRAPHIE.sha256` (les 28 maîtres, scellés par leur nom). Ce second scellé est la réponse au seul résidu que la chaîne assume : réengraver *les deux* après une permutation reste un acte éditorial, lisible dans le diff, et qui demande un Avis.

Les mêmes contrôles sont enchaînés à chaque push sur `main` et à chaque pull request par le workflow `sources/github_actions_continuite.yml` : arbre régénéré identique au bit près, régénération du volume, artéfact, empreinte de fraîcheur, scellé des archives, PDF déposé en pièce jointe de relecture.

**Activation** — le gabarit est tenu à jour, son installation reste un **acte de publication** :

```bash
make workflows    # copie sources/github_actions_continuite.yml → .github/workflows/continuite.yml
                  # et retire au passage le talon invalide main.yml
```

**18 étapes**, YAML validé, chacune rejouée localement : polices, dépendances, compilation,
continuité, parité des données, parité du portail, **chroniques**, atlas, arbre, **hymne (Avis
royal n° 8)**, **vignettes**, régénération du volume, artéfact apparié, fraîcheur, scellés,
pièce jointe.

Le fichier `.github/workflows/continuite.yml` **ne peut pas sortir d'une App** : GitHub refuse qu'un jeton
dépourvu du droit `workflows` crée ou modifie `.github/workflows/*` (constats **E-17** et **F-01**, mesuré
à nouveau le 29 août 2026 — refus à la fois par `git push` et par l'API *contents*). Le dépôt versionne
donc le modèle, pas sa copie. Deux façons de lever le blocage :

```bash
# (a) avec un jeton humain — trois commandes, dans un clone à vous
make workflows
git add .github/workflows/continuite.yml && git commit -m "CI : installation du workflow de continuité"
git push

# (b) sans y toucher : accorder le droit à l'App, puis demander sa réexécution
#     github.com/settings/installations → Arena → Permissions du dépôt → Workflows : Read and write
```

Tant que l'une des deux n'a pas eu lieu, **les contrôles ne tournent que si on les lance** (`make controle`) :
aucune vérification automatique ne protège `main`.

## Atlas géographique (proposé, non décrété)

```bash
make carte          # SVG + PNG 2026 + geographie/index.html
```

L'atlas temporel (`geographie/index.html`) fait glisser 1830 → 2026 : les Monts Froissés n'apparaissent que le 15 juillet 1962, McBabber's le 1er avril 1986. Analyse : `geographie/ANALYSE.md`. Tant qu'un Avis n° 7 n'aura pas parlé, **2026-I ne change pas**.

## Régénération de l'arbre

L'arbre dispose d'une maquette vectorielle éditable (`sources/arbre_genealogique_complet.svg`) et d'un générateur PNG déterministe (`sources/generate_genealogy.py`).

```bash
make arbre        # équivalent de : python .venv/bin/python sources/generate_genealogy.py
```

## Binaires lourds et Git LFS (R1.6)

Le portail ne charge plus les maîtres PNG en grille : les **vignettes WebP** (`images/vignettes/`,
`make vignettes`, 220 Mio → 4,65 Mio) servent les grilles des personnages et de la galerie, et le
maître pleine taille reste **un clic plus loin**, dans la visionneuse. Le poids de diffusion est
donc réglé sans bouger les maîtres.

Pour sortir les binaires du magasin Git (≈ 330 Mio de candidats), la procédure est écrite et
mesurée dans **`gouvernance/LFS_MIGRATION.md`** : options A (prospective) et A′ (variante
recommandée, ≈ 230 Mio) et B (réécriture de l'historique, à avis). `make lfs` exécute la variante
A′ — **sauf le `git push`**, qui exige l'accès au CDN de GitHub (mesuré le 30 août 2026 : le
batch LFS répond 200, l'upload des objets vers le S3 de GitHub est bloqué depuis
l'environnement d'agent ; la migration n'y est donc pas engagée, et ne le sera jamais depuis cet
environnement tant que ce blocage durera — un dépôt à pointeurs sans objets casserait tous les
autres clones).
