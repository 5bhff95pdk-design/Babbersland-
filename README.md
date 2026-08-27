# Royaume du Babberland

Archives narratives et iconographiques du Royaume du Babberland.

*Registre d'import : le nom du dépôt s'écrit « Babbersland » ; l'endonyme canonique, seul employé dans les volumes, est **Babberland**.*

## Référence officielle actuelle

1. **`Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf`** — encyclopédie illustrée consolidée et référence canonique autonome (24 illustrations après la campagne 2026-II).
2. **`ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`** — source éditoriale du volume 2026-I ; **c'est elle qui fait foi**, y compris sur la liste des illustrations que le PDF doit montrer.
3. **`CHRONOLOGIE_MAITRESSE_1847_2026.md`** — registre chronologique détaillé, avec règnes, sources et contrôles de continuité.
4. **`images/`** — portraits, numismatique et arbre généalogique illustré.

L'édition **2026-I** intègre directement les corrections et ne nécessite aucune règle de préséance documentaire.

## Gouvernance & audits

| Document | Objet |
|---|---|
| `RAPPORT_DE_REVISION_2026_I.md` | Révision générale du 27 août 2026 (RR-2026-I-01) : réserve E-01 levée, contrôles étendus |
| `RAPPORT_ANALYSE_2026_II.md` | Audit technique, éditorial et documentaire (RA-2026-II-01) : constats E-07 à E-16, mesures reproductibles |
| `ROADMAP_2026_II.md` | Feuille de route en quatre horizons, 28 tickets, risques et indicateurs |
| `gouvernance/ARCHIVE.md` | Politique d'archivage : ce qui est gelé, ce qui ne l'est pas, comment dégeler |
| `gouvernance/ARCHIVE.sha256` | Scellés des archives 2026-G et 2026-H, vérifiés par la CI |
| `gouvernance/pdf_fingerprint.txt` | Empreinte sémantique du PDF canonique — le contrat de fraîcheur de l'artefact |
| `gouvernance/index.html` | Version visuelle du rapport et de la roadmap (page autonome) |

## Chroniques narratives (hors canon)

- `chroniques/LIVRE_I_LES_FONDATIONS.md` — *Les Chroniques de l'Ancien, Livre I : Les Fondations (1798–1889)* : histoire du premier roi racontée en sept tranches. Éléments nouveaux **proposés, non décrétés** ; toute addition au canon devra passer par décret et mise à jour de 2026-I.

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
- Les quatorze illustrations du dossier iconographique sont toutes servies dans le volume imprimé : une référence `images/…` du Markdown canonique sans ancre dans le générateur est une **erreur de contrôle**, plus un état possible du projet.

## Chaîne de production

Tout passe par `make`, qui installe ses propres dépendances dans un venv — les `pip install` directs échouent sur les systèmes récents (environnement géré, PEP 668) :

```bash
make env          # python3 -m venv .venv + pip install -r requirements.txt
make tout         # arbre → PDF → empreinte → contrôles
make controle     # les trois contrôles, sans rien régénérer
```

Buts disponibles : `env`, `arbre`, `pdf`, `empreinte`, `controle`, `workflows`, `tout`, `propre`. Hors venv : `make PY=python3 …`. Les générateurs cherchent les polices DejaVu sur Linux, macOS et Windows (`BABBERLAND_FONT_DIR` pour forcer un répertoire).

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
python .venv/bin/python sources/check_continuity.py
python .venv/bin/python sources/check_pdf.py
python .venv/bin/python sources/pdf_fingerprint.py --check
```

- **`check_continuity.py`** (sans dépendance) vérifie les titres historiques, l'ordre de succession, les sept livres, les équivalences monétaires, les dates maîtresses, tous les liens d'illustrations, les ancres d'illustrations du générateur (chaque ancre doit exister telle quelle dans 2026-I, faute de quoi l'illustration disparaît silencieusement du PDF), la **couverture** — chaque image promise par 2026-I doit être servie ou expressément exclue par `<!-- hors-PDF: images/x.png — motif -->` — et le bandeau de statut des chroniques.
- **`check_pdf.py`** (`pypdf`) ouvre le PDF publié et compte les **hachés de flux image**, non les noms de XObject : l'attendu vient du canon, pas du générateur. Il refuse aussi les intitulés de renvoi orphelins et les chemins d'images en clair.
- **`pdf_fingerprint.py --check`** compare l'artefact publié à l'empreinte gravée : le PDF n'est pas reproductible à l'octet (ReportLab nomme ses XObject aléatoirement), donc on compare ce que le lecteur voit — pages, texte, images.

Les mêmes contrôles sont enchaînés à chaque push sur `main` et à chaque pull request par le workflow `sources/github_actions_continuite.yml` : arbre régénéré identique au bit près, régénération du volume, artéfact, empreinte de fraîcheur, scellé des archives, PDF déposé en pièce jointe de relecture.

**Activation** — une commande, puis un commit :

```bash
make workflows && git add .github && git commit -m "CI : continuité, empreinte et scellé des archives"
```

Le fichier est prêt et ses étapes sont vérifiées localement ; seul le *pousser* demande un jeton tenant la permission **workflows** (un jeton d'application GitHub dépourvu de ce droit se voit refuser la création de `.github/workflows/*` — la voie de contournement est de committer le fichier depuis GitHub, ou d'accorder le droit à l'App).

## Régénération de l'arbre

L'arbre dispose d'une maquette vectorielle éditable (`sources/arbre_genealogique_complet.svg`) et d'un générateur PNG déterministe (`sources/generate_genealogy.py`).

```bash
make arbre        # équivalent de : python .venv/bin/python sources/generate_genealogy.py
```
