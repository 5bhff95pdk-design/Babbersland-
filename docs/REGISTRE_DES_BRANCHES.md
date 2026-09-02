# 🗂 REGISTRE DES BRANCHES DE TRAVAIL

*Chancellerie royale — séance de nettoiement du 2 septembre 2026.*
*Ce registre n'est pas un décret : il constate, il archive, et il rend réversible.*

---

## I. Objet

Le dépôt comptait **33 branches `arena/*`** encore vivantes sur `origin`, dont aucune n'avait été
rangée après sa fusion, `delete_branch_on_merge` étant désactivé sur le dépôt (le jeton dont
dispose la Chancellerie n'a pas le droit `administration` : le réglage doit être coché à la main,
voir § V).

Vérification préalable, menée avant toute suppression :

| Ce qui a été mesuré | Résultat |
|---|---|
| Bout de branche ancêtre de `main` (donc réellement fusionné) | **0 sur 33** |
| Arborescence du bout de branche identique à `main` (dernière en date) | **identique à 0 octet près** |
| Contenu d'une branche ancienne comparé à `main` | `+42 lignes / −19 675` : un **état antérieur**, pas du travail en attente |
| Commits hors de `main` | **107** (104 conservés au bundle, 2 élagués pour cause de filtre, 1 hors périmètre) |
| Date d'auteur ↔ date de commit | **confondues sur toute la ligne** (`14:56:49` partout sur `main`) |

**Conclusion — l'unique lieu du passé.** `main` porte un commit **sans parent** (squash à chaque
fusion) : les 107 commits de détail des campagnes 2026-II à 2026-XIX n'existaient QUE sur ces
branches. Les supprimer sans preuve, c'était supprimer l'histoire. Le CHANGELOG raconte ; lui seul
montre, commit par commit, ce qui a bougé. **D'où le présent archivement, qui précède le
nettoiement et non l'inverse.**

**Conséquence mesurée sur la valeur probante des scellés** : puisque les dates d'auteur et de
commit sont confondues (le squash les réécrit), l'historique ne prouvait de toute façon **rien**
sur l'antériorité d'un scellé. Cela confirme, en la nuanceant, la mesure du 2 septembre sur
l'absence d'ancrage horodaté externe : la seule preuve d'antériorité disponible est **hors du
dépôt** (Release, tag — cf. `ROADMAP_2026_II.md` R1.5, et § V ci-dessous).

---

## II. Archive

| Pièce | Valeur |
|---|---|
| Fichier | `docs/archives/babberland-histoire-texte-2026-09-02.bundle` |
| Empreinte | `38903db478093e294f2bbb3f2842220aaff2c2352d4ff8ea9ee149bb5498d2ab` |
| Poids | 813 Kio (pour 335 Mio de dépôt : le texte pèse peu, les images pèsent tout) |
| Contenu | 33 refs de têtes, 104 commits, du 26 août (généalogie révisée) au 2 septembre (cérémonie d'acceptation close) |
| Filtre appliqué | retraits de `*.png *.pdf *.webp *.wav *.mp3 *.jpg` — **les binaires ne sont pas dans le bundle** |
| Vérification | `git bundle verify` → « the bundle records a complete history » ; **cloné** dans un répertoire vierge, 33 refs retrouvées, un fichier restauré et relu (`sources/check_portal.py`) |

Le bundle est **autoportant** : il n'exige aucun objet du dépôt d'origine, il peut donc être lu
même après le garbage-collect de GitHub.

---

## III. Inventaire des refs archivées

| Branche (`arena/`) | Bout | Dernière date | Commits | Objet du bout de branche |
|---|---|---|---|---|
| `01a03e66-babbersland` | `7171d09695` | 2026-08-26 14:37 | 3 | Ajout de la généalogie révisée 1847-2026, chroniques dynastiqu |
| `01a03fbc-babbersland` | `1b2f7e335a` | 2026-08-26 21:45 | 9 | Retire les références québécoises de l'enseigne McBabber's |
| `01a04015-babbersland` | `44653cfe41` | 2026-08-26 22:21 | 14 | Revise la coherence de l edition 2026-I |
| `01a04039-babbersland` | `b97ecc8d92` | 2026-08-26 23:35 | 16 | Ajout des Chroniques de l'Ancien — Livre I : Les Fondations (1 |
| `01a0408b-babbersland` | `3635304840` | 2026-08-27 00:41 | 18 | Révision 2026-I : levée de la réserve E-01 et durcissement des |
| `01a0421d-babbersland` | `b0f94b55d2` | 2026-08-27 08:12 | 24 | Rapport : cellule E-07 réécrite lisiblement |
| `01a0445a-babbersland` | `b7d90516c4` | 2026-08-27 20:55 | 26 | Add the 2026-II dynastic portrait gallery and iconographic inv |
| `01a0450b-babbersland` | `ec97655287` | 2026-08-27 21:25 | 29 | Géographie : atlas temporel proposé (R2.6 / E-16.c) |
| `01a04631-babbersland` | `b2b9152dff` | 2026-08-28 05:22 | 33 | Chroniques : Livre IV — L'Ère balnéaire (1959–1998) |
| `01a046ca-babbersland` | `acb106dfd4` | 2026-08-28 05:36 | 36 | Fusion main : le Livre II existe en deux rédactions, l'Avis tr |
| `01a047e7-babbersland` | `ef739a6a2b` | 2026-08-28 10:31 | 38 | Ajouter un numéro complet de la Gazette du Babberland |
| `01a049ea-babbersland` | `3cbe832058` | 2026-08-28 20:40 | 38 | Audit 2026-III : 19 constats corrigés, rapport d'audit (la CI  |
| `01a04f4f-babbersland` | `2a3101b1fb` | 2026-08-29 21:18 | 38 | feat(lore): Livres V & VI des Chroniques, Livre VIII Instituti |
| `01a04f7a-babbersland` | `84d0a4f735` | 2026-08-29 22:45 | 41 | CI : retirer le talon invalide .github/workflows/main.yml (une |
| `01a04fc9-babbersland` | `4f92b5332c` | 2026-08-29 23:16 | 43 | feat: ajout de la galerie de 16 photos ultra-réalistes et mise |
| `01a04fd4-babbersland` | `a74637d30d` | 2026-08-29 23:33 | 46 | fix: déplace pages.yml en template sources/ (E-17 workflows pe |
| `01a04ff5-babbersland` | `d39d989591` | 2026-08-30 00:20 | 45 | Hymne national « Debout, tout doucement » : dossier, enregistr |
| `01a0504c-babbersland` | `6229e349d1` | 2026-08-30 02:02 | 48 | Chroniques : arithmetique interne et cotes d'archives ; vignet |
| `01a053cc-babbersland` | `1825542096` | 2026-08-30 18:00 | 47 | Corrections d'audit : parité du portail, compilation, converti |
| `01a05480-babbersland` | `518d340a51` | 2026-08-30 21:50 | 55 | Galerie 2026-V : neuf planches, du phare au Jour de l'Eau |
| `01a054ae-babbersland` | `3a313c413b` | 2026-08-30 22:25 | 57 | Fuse the two Livre II chronicle editions |
| `01a054cc-babbersland` | `d50b76a632` | 2026-08-30 23:08 | 60 | Portail sur vignettes (220 → 7 Mio), bug JS corrigé, runbook L |
| `01a059c2-babbersland` | `e66d7ecd9a` | 2026-08-31 21:41 | 2 | chore: supprime les images lourdes (>1 Mo) |
| `01a05e11-babbersland` | `32ba7dcc27` | 2026-09-01 18:04 | 64 | R0.4 : le droit accordé ne suffit pas à un jeton déjà émis (pr |
| `01a05f15-babbersland` | `14c66fc974` | 2026-09-01 22:57 | 68 | R1.4.b doc: rectificatif de comptage des etapes continue-on-er |
| `01a05f35-babbersland` | `cb64cfe13c` | 2026-09-01 23:13 | 70 | R1.4.h: suivi — run CI 33569884539 vert (gel strict, étape 7 s |
| `01a05f55-babbersland` | `f486075e77` | 2026-09-02 00:29 | 75 | R1.4 — le canari est clos sur un run vert : preuve, et non plu |
| `01a05f96-babbersland` | `37d1ca0e69` | 2026-09-02 01:09 | 71 | R1.8 + R1.9 : parité modèle ↔ workflow installé, scellé de la  |
| `01a05fce-babbersland` | `88b58981af` | 2026-09-02 02:15 | 73 | R1.3 : manifeste des livrables canoniques (MANIFEST.sha256) +  |
| `01a05fed-babbersland` | `29d066e71e` | 2026-09-02 02:37 | 75 | feat(lore): enrichissement du lore avec biographies et portail |
| `01a05fff-babbersland` | `061723570a` | 2026-09-02 04:01 | 78 | Galerie 2026-VII : transports et marine royale (+2 clichés réa |
| `01a060b6-babbersland` | `139acc134a` | 2026-09-02 06:54 | 83 | Livre VI : porter Le Siècle qui Louche au standard du corpus ( |
| `01a06265-babbersland` | `f88a7bb59f` | 2026-09-02 14:51 | 87 | Docs : la cérémonie d'acceptation est close (run #33644538835  |

*Têtes reprises telles quelles de `git ls-remote --heads origin`, relevé le 2 septembre 2026 à
15:47 UTC. Le nom de branche est l'identifiant de la session d'agent qui l'a produite ; il est
conservé ici comme cote, non comme référence vivante.*

---

## IV. Procédure de restauration

```bash
git clone docs/archives/babberland-histoire-texte-2026-09-02.bundle restauration && cd restauration
git branch -a                                   # 33 têtes, sous refs/remotes/origin/arena/*
git show origin/arena/01a053cc-babbersland:sources/check_portal.py   # n'importe quel fichier texte
git checkout -b restauration/01a053cc origin/arena/01a053cc-babbersland
```

Tant que GitHub n'a pas garbage-collecté les anciennes refs, les **binaires** d'une campagne
restent aussi récupérables par SHA (`git fetch origin <sha>`) : le bundle, lui, ne contient que le
texte. Après collecte, le texte reste ; l'image se régénère par la chaîne (`make tout`).

---

## V. Ce que le nettoiement n'a pas pu faire, et qui reste à faire

1. **Cocher `Settings → General → Automatically delete head branches`** sur
   `github.com/5bhff95pdk-design/Babbersland-/settings` — le jeton de l'App répond `403` au
   `PATCH` sur `delete_branch_on_merge`. Faute de ce réglage, les branches repousseront d'elles-mêmes.
2. **Créer le tag `v2026-I` et la Release** (R1.5 / R0.4, ouverts depuis le 30 août) : c'est la
   seule ancre d'antériorité que rien, dans le dépôt, ne peut re-graver. Le présent registre en
   démontre le besoin par la négative.
3. **La taille du dépôt ne baisse pas avec ce nettoiement.** Un clone pèse toujours ~335 Mio : le
   poids est dans le commit courant, pas dans l'historique. Seule la sortie des PDF (fait ici pour
   2026-I, **impossible** pour 2026-G, scellée par `ARCHIVE.sha256` et régénérable par rien — E-12)
   ou un passage en LFS (A′, Avis n° 9) y change quelque chose.

---

*Registre établi à Pabst City le 2 septembre 2026, sans aucune hâte.*
*Il ne scelle rien : il atteste qu'on n'a rien jeté.*
