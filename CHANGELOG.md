# 📜 JOURNAL DES MODIFICATIONS (CHANGELOG)

Toutes les modifications notables apportées au dépôt du **Royaume du Babberland** sont consignées dans ce document.

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
