# 🧾 CONTRE-EXPERTISE TECHNIQUE 2026-III
## RC-2026-III-01 · Ce que la batterie de contrôles ne voit pas

**Chancellerie royale · Pabst City** — audit indépendant du dépôt, conduite le 29 août 2026.
Statut à l'émission : **proposé, non décrété**. Le texte canonique 2026-I n'a été touché **ni par
l'expertise, ni par ses correctifs** ; ce qui a été modifié depuis, c'est l'outillage (cinq scripts,
un module partagé, le `Makefile`, le rite, le workflow) et les **documents dérivés** alignés sur le
canon (`canon/*.json`, `gouvernance/REGISTRE_DES_PERSONNAGES.md`). Chaque correctif reste
reproductible par les commandes données, et l'exécution est consignée en **§6**.

Périmètre : `Makefile`, `sources/*.py` (8 scripts, 2 018 lignes), `canon/*.json`,
`gouvernance/ARCHIVE.sha256`, artefact publié 2026-I, pages HTML, chaîne de production complète.
Suite logique des constats E-01 → E-17 (`RAPPORT_DE_REVISION_2026_I.md`, `RAPPORT_ANALYSE_2026_II.md`).

---

## 1. Verdict

| Objet | État mesuré |
|---|---|
| Batterie de contrôles sur l'état déposé | ✅ **4/4 verts** (continuité, PDF, empreinte, géographie) + scellés G/H intacts |
| artefact publié vs source Markdown | ✅ **synchrone** — PDF régénéré : octets différents, **empreinte sémantique identique** (`a129fa3f…`, 29 p., 24 ill.) |
| Déterminisme de l'arbre | ✅ **bit près** (`md5 8c9420fe…`, régénéré depuis une copie hors dépôt) |
| Liens internes (Markdown + HTML) | ✅ **0 cassé** sur 86 fichiers suivis |
| **Couverture réelle des contrôles** | 🔴 **7 bloquages pour 13 fautes injectées** ; 4 vraies fautes laissées passer, dont 2 majeures |
| **Fraîcheur du volume (E-10/E-17)** | 🔴 **le contrat ne protège pas ce qu'on croit** : deux portraits intervertis, `make tout` est vert **et l'empreinte gravée ne bouge pas** |
| `canon/*.json` (R3.3) | 🔴 **quatrième copie du canon, lue par zéro contrôle** — 4 divergences biographiques déjà constituées |
| CI (R0.4 / E-17) | 🔴 **inerte** : `.github/workflows/` ne contient qu'un fichier invalide ; le scellé des archives n'est vérifié **nulle part localement** |
| Poids suivi (R1.6) | 🟠 mesure à reprendre : **75 Mio de PNG** (37,2 mesurés au bilan), 250 Mo de dépôt, 93 Mo de `.git`, pas de LFS |
| Pages de diffusion | 🟠 `gouvernance/index.html` et deux points du README **en retard d'une campagne** |

**Avis : FAVORABLE SUR LE FOND, RÉSERVÉ SUR LE VERROUILLAGE.** L'univers est cohérent — 229 ans,
sept générations, aucune contradiction de filiation ni de succession trouvée, les lacunes déclarées
tiennent. La fragilité n'est pas éditoriale : **les contrôles valident des présences de chaînes,
pas des faits**, et une partie du dispositif (JSON, empreinte, scellé) n'est adossée à rien.

> **Suivi du 29 août 2026 — lot C0 appliqué.** Dix des quatorze constats sont clos de bout en bout,
> un (E-23) clos côté gabarit et en attente d'un poussage humain, deux alignements de données faits,
> un résidu assumé et documenté : voir **§6, Suivi d'exécution**.
> La batterie de mutations a été rejouée contre la chaîne corrigée, et elle est **devenue un fichier
> du dépôt** : `make batterie` (`sources/test_mutations.py`) casse seize copies isolées de l'arbre et
> rend son verdict — **16 scénarios sur 16 conformes à l'attendu** : les treize altérations sont
> refusées, les trois éditions légitimes acceptées, dont le résidu du §6 qui passe parce qu'il doit passer.

---

## 2. Preuve maîtresse : la batterie est aveugle à la permutation

Scénario réaliste, non fantaisiste : à la fabrication, deux fichiers d'illustration sont échangés
(erreur de renommage, de réexport, de `git mv`). Le portrait du Dormeur se retrouve sous la légende
du Fou, et réciproquement.

```bash
cp -r . /tmp/mut6 && cd /tmp/mut6
# échange des octets de deux portraits canoniques
python3 - <<'EOF'
from pathlib import Path
a, b = Path('images/babber_le_fou.png'), Path('images/babber_le_dormeur.png')
x, y = a.read_bytes(), b.read_bytes()
a.write_bytes(y); b.write_bytes(x)          # les deux figures ont inversé leurs visages
EOF
make PY=python3 tout          # la chaîne complète, celle que le RITE de publication impose
```

Résultat obtenu : **exit 0 sur les six étapes**, `24 illustrations embarquées`, et surtout
`Empreinte gravée : a129fa3f447aecc10264771e33d600d4` — **la valeur même de l'empreinte de
référence**. Le volume fautif porte donc le sceau du volume juste.

Cause, ligne à ligne :

* `pdf_fingerprint.py::image_streams()` construit un **`set`** de hachés, trié, concaténé.
  Une permutation laisse l'ensemble inchangé → empreinte inchangée. Le contrat d'E-10 protège
  la **perte** d'illustration, pas l'**affectation**.
* `check_pdf.py` vérifie que chaque légende *apparaît quelque part* dans la couche texte. Comme
  les légendes restent sous leurs images respectives, elles sont toutes présentes : le test prouve
  le texte, pas l'appariement.

**Correctif proposé (≈ 25 lignes, dans `check_pdf.py`)** — appariement positionnel :

```python
# pour chaque (fichier, légende) d'IMAGE_AFTER : la page qui porte la légende doit porter le flux
# dont le md5 est celui du fichier promis. attendus = [(md5(images/x.png), légende), …]
pages_h = {i: hashes_des_flux_de_la_page(i) for i in range(len(reader.pages))}
for digest, caption in attendus:
    ports = [i for i, h in pages_h.items() if normalize(caption) in text_of_page(i)]
    if not ports or not all(digest in pages_h[i] for i in ports):
        errors.append(f"illustration mal appariée à sa légende : {caption!r}")
```

et, en cohérence, rendre l'empreinte **ordonnée** : `pages | md5(texte) | [(page, [md5 flux]…), …]`
au lieu d'un tri d'ensembles. Le PDF est alors pris en défaut par la permutation, et
`gouvernance/pdf_fingerprint.txt` devient un vrai contrat, non un récépissé.

---

## 3. Constats

### 🔴 E-18 · Le contrat de fraîcheur est insensible à l'affectation des images
**Gravité** : majeure (classe E-01, mais indétectable par le contrôle censé la fermer) · **Effort** : 25 lignes
**Preuve** : section 2. **Portée** : toute planche déplacée, doublonnée sous un autre ancrage, ou échangée
avec une consœur. **Mesure** : permutation de deux portraits → chaîne verte, empreinte stable.
**Correction** : appariement légende↔flux par page (section 2) + empreinte ordonnée + `make empreinte`
gravé à nouveau, et consigné au Registre des Avis comme révision du contrat.

### 🔴 E-19 · `canon/*.json` n'est contrôlé par personne, et a déjà dérivé
**Gravité** : majeure (exactement la classe E-15 — double source sans parité — étendue à quatre sources) · **Effort** : 40 lignes
`grep -rn "canon/" sources/*.py .github/` → **aucun résultat** : ni générateur, ni contrôle, ni étape de CI
ne lit les quatre fichiers de données. Deux injections, toutes deux silencieuses :
`"generation": 7 → 8` pour Ti-Babber, `"population_totale": 7000 → 9000`. La somme des régions
(`lieux.json`) reste juste, donc l'arithmétique ne sauve pas non plus le champ touché.

**Divergences constituées, 2026-I faisant foi :**

| Figure | 2026-I (canon) | `canon/personnages.json` | `REGISTRE_DES_PERSONNAGES.md` |
|---|---|---|---|
| Babette Ire de Plantagenet | **1804**–1892 | **v. 1805**–1892 | *(sans dates)* |
| Hortense du Grain | **1840–1922** | **v. 1845–v. 1930** | *(sans dates)* |
| Princesse Babette-Marine | **1836**–1916 | **1840**–1916 | **1840**–1916 (2 fois) |
| Irène des Érables | **1882**–1966 | **1880**–1966 | **1880**–1966 (2 fois) |

Trois autres dérives du même registre, non chronologiques :
* **ordinal fantôme** : `Babber Ier le Dormeur` (JSON + Registre, fiche 6) contre `Babber le Dormeur`
  dans 2026-I — quatre occurrences, jamais d'ordinal ; or le dossier iconographique et le
  refus de l'ordinal II font de ce détail un point de doctrine, pas une coquetterie ;
* **`Babber VII l'Éveillé`** en données : la clef `generation: 7` dit « septième génération »
  (règle du README), le nom dit « septième règne ». Dans un fichier destiné aux machines,
  l'ambiguïté se résoudra en erreur ;
* **objet doublement nommé** : `Grand Sauciériste d'Or` (prose, l. 149 ; légende imprimée au PDF)
  contre `saucière d'or` (dossier iconographique, l. 432, **même fichier** `ginette_de_port_babette.png`).
  Un récipient et une charge ne sont pas la même chose.

**Correction** : `sources/check_canon.py`, cinquième but de `make controle` — bijection des 18 `id`
contre les vedettes du Registre ; années de chaque fiche ⊆ années de 2026-I ; `population_*`
égales à la somme des régions et à la prose du canon ; dates maîtresses de `evenements.json`
retrouvées dans la Chronologie ; liste noire d'ordinaux non canoniques (`Ier le Dormeur`) ;
interdire qu'un `nom` porte un ordinal absent de 2026-I.

### 🔴 E-20 · Le contrôle d'anachronisme des Monts Froissés ne peut pas échouer
**Gravité** : moyenne (rend l'invariant GEO le plus vendu de l'atlas inexistant) · **Effort** : 6 lignes
`check_geography.py` :

```python
must("Monts Froissés" not in pre_1962.split("Futur créateur des Monts Froissés")[-1]
     or pre_1962.count("Monts Froissés") <= 2, "les Monts Froissés apparaissent trop tôt")
```

La seconde branche est **vraie dès qu'il y a ≤ 2 mentions**, quel que soit leur sens — et la première
s'applique à une chaîne tronquée par `split(...)[-1]`, c'est-à-dire à ce qui reste *après*
l'exception, pas à la période interdite. Injection : « *12 octobre 1847 — les Monts Froissés dominent
déjà la plaine* » dans la Chronologie maîtresse → **quatre contrôles verts**. L'atlas promet
pourtant que « les Monts n'existent pas avant le 15 juillet 1962 ».
**Correction** : itérer sur les lignes antérieures au marqueur 1962 et refuser toute occurrence non
précédée de `futur|devra|deviendra` ; le seuil « 2 » disparaît.

### 🔴 E-21 · `make tout` grave l'empreinte avant de la vérifier : auto-validation
**Gravité** : moyenne · **Effort** : 1 mot
`Makefile` : `tout: arbre pdf empreinte controle`. L'étape `controle` compare le PDF à l'empreinte
**que `tout` vient d'écrire** : `--check` y est structurellement infaillible (il ne peut échouer que
si le PDF change *pendant* la cible, ce qui n'arrive pas). Le `gouvernance/RITE_DE_PUBLICATION.md`
§IV reproduit le même ordre (`make empreinte` puis `make controle`), donc le rite écrit
l'auto-validation. La CI, elle, a raison (`--check` seul, sans `--write`) — mais la CI est inerte
(E-23) : en pratique, **personne ne vérifie plus rien** à cette étape.
**Correction** : `tout: arbre pdf controle empreinte` — et dire dans le RITE que `empreinte` est un
**acte d'assentiment** distinct de la vérification. Plus sûr encore : que `--check` échoue si
l'empreinte gravée n'a pas été touchée *au commit précédent*, pour interdire le re-gravage réflexe.

### 🟠 E-22 · `check_pdf.py` compare deux cardinalités, pas des identités
**Gravité** : moyenne · **Effort** : 10 lignes
`len(flux uniques) != len(chemins promis)` : à gauche un dénombrement de **contenus**, à droite un
dénombrement de **noms de fichiers**. L'égalité de deux comptes n'implique pas la bijection :

* *planche non consentie* : une insertion supplémentaire dont les octets reproduisent une planche
  existante → `24 flux / 24 promises`, tout est vert, **légende neuve imprimée dans le volume de
  référence** et acceptée par `check_pdf` (compteur de légendes passé à 24) ;
* *faute de goût symétrique* : deux `images/*.png` canoniques aux octets identiques (un double-emploi
  non déclaré) → 23 flux pour 24 promesses : **échec** sur un livre pourtant juste.

**Angles morts voisins, mesurés :**

| Scénario | Verdict |
|---|---|
| ancre exacte requise par le générateur (`IMAGE_AFTER.get(title)`), **sous-chaîne** admise par `check_continuity` (`anchor not in canon_text`) | asymétrie : un titre rallongé garde la sous-chaîne, perd ses images ; ne sont rattrapés aujourd'hui que par le comptage, donc que pour les images à usage unique |
| `check_pdf` ignore les flux masqués (`/SMask`), `pdf_fingerprint` les compte | deux définitions de « illustration embarquée » ; coïncidence actuelle (24 = 24), latente |
| `prepared_image` met son dérivé en cache sous `src.stem + ".jpg"` | deux sources de noms voisins (`x.png`, `x.jpg`) se partageraient un fichier ; stems uniques aujourd'hui |
| `EMOJI_RE` = plage Unicode **puis** liste explicite d'emojis | tout emoji absent de la liste survit dans un titre → l'ancre exacte casse ; le comptage sauve, mais le diagnostic reste obscur |

**Correction** : une fonction commune `plates_de_2026_i() -> {md5_sur_disque: (chemin, légende)}`,
utilisée par les deux scripts ; le contrôle devient « chaque md5 promis est présent, et tout flux
embarqué est promis » (double inclusion), plus la parité SMask réglée une fois pour toutes.

### 🟠 E-23 · CI inerte **et** fichier de workflow invalide ; le scellé n'est vérifié nulle part
**Gravité** : bloquante pour R0.4 · **Effort** : 1 commit + 3 lignes
Deux défauts distincts, le second non signalé par E-17 :

1. `make controle` ne teste **pas** le gel des archives : `sha256sum --check gouvernance/ARCHIVE.sha256`
   n'existe que dans l'étape CI. Or la CI n'est pas installée. Un fichier archivé modifié passe donc
   **en local comme en ligne** — vérification faite : le scellé est intact *aujourd'hui* (2/2 OK),
   mais rien ne l'empêche de bouger.
2. `.github/workflows/main.yml` ne contient qu'une ligne, `github.com/settings/apps`, qui n'est pas
   un mapping : GitHub refuse ce fichier comme workflow (le dépôt affiche donc un onglet Actions
   **en erreur**, distinct de « CI absente »). Le vrai workflow — 12 étapes, et non 9 comme annoncé
   au tableau de bord et dans `ROADMAP_2026_II.md` — dort dans `sources/github_actions_continuite.yml`.

**Correction** : `make workflows`, supprimer le talon `main.yml` (ou le remplacer par le modèle),
ajouter au `controle` local la cible `scelle` (`sha256sum --check --quiet gouvernance/ARCHIVE.sha256`).
Le blocage E-17 (jeton d'App sans droit `workflows`) reste réel pour un agent ; il tombe dès qu'un
mainteneur tenant un compte habilité fait le commit.

### 🟠 E-24 · « Les cinq silences sanctifiés » sont protégés par un texte, pas par le code
**Gravité** : moyenne (le Serment fait une promesse d'outillage fausse) · **Effort** : 8 lignes
`gouvernance/SERMENT_D_IGNORANCE.md` §III : « *Les générateurs automatiques et les scripts de
validation (`check_continuity.py`) reconnaissent ces lacunes comme conformes au canon et rejettent
toute tentative d'imposer une fixation arbitraire.* » Aucun tel contrôle n'existe — `grep -n
"lacune\|silence\|ignorance" sources/*.py` est vide.
Mesure : **percer le silence n° 2** (donner une date de naissance à Roger Bontemps dans 2026-I,
`**Roger Bontemps** → **Roger Bontemps (né en 1802)**`) → **trois contrôles verts**.
Le silence n° 1, lui, est « protégé » par accident : dater le Déchiré casse le **titre** d'ancre,
donc `check_continuity` échoue — sur un motif de mise en page, et il échouerait de même pour un
simple retitrage innocent. Un contrôle qui confond mystère et typographie protège mal les deux.
**Correction** : table `SILENCES = {figure: motif_interdit}` dans `check_continuity.py` (refuser
`\(\s*(?:v\.\s*)?\d{4}` dans les lignes des cinq figures concernées), et, pour le Déchiré, une
ancre indépendante du titre (voir E-25).

### 🟡 E-25 · Les ancres d'illustration sont des titres, donc le canon est réécrit pour plaire au script
**Gravité** : moyenne, structurelle · **Effort** : 1 h
Toute la table `IMAGE_AFTER` est indexée sur des **titres de niveau 1 à 4**, nettoyés d'emojis puis
comparés exactement (`clean_heading`). Conséquences observables : l'ancre du Déchiré est
`"2. S.A.R. le Prince Babber le Déchiré (date de naissance non consignée ; majeur attesté en 2007)"` —
un **titre de chapitre portant une clause historiographique**, qu'aucun rédacteur ne peut retoucher
sans déclencher une perte d'image. Les 16 ancres sont des chaînes de 40 à 110 caractères : surface de
rupture maximale, message d'échec minimal (« ancre introuvable »).
**Correction** : marqueur d'ancrage explicite dans le Markdown, insensible au titre —
`<!-- fig:dechire -->` — et table `IMAGE_AFTER` indexée sur ces identifiants courts ; conserver un an
la vérification par titre pour les deux conventions.

### 🟡 E-26 · Dates de vie non recoupées entre les quatre registres
**Gravité** : moyenne · **Effort** : 15 lignes (avec E-19)
`1959 → 1958` pour la mort du Dormeur **dans 2026-I seul** : quatre contrôles verts. La Chronologie
maîtresse, qui fixe l'avènement du successeur à 1959, n'est confrontée aux dates de vie du canon
nulle part : `check_continuity` épingle cinq dates maîtresses *en tant que chaînes*, et
`required`/`phrases` — jamais une arithmétique de règnes. Le « 0 erreur d'arithmétique généalogique
sur 229 ans » du tableau de bord repose donc sur une vérification **humaine**, réitérée à l'audit 2026-II
(18 calculs), et non sur un contrôle rejouable.
**Correction** : dans `check_canon.py`, contrôler pour chaque régnant
`début_règne == max(année de naissance + 18, date d'avènement de la Chronologie)`-invariant non :
retenir plus simple et plus fort — `mort_année` du prédécesseur **égale** l'année d'avènement du
successeur dans la Chronologie, pour les sept successions.

### 🔵 E-27 · Diffusion : trois artefacts en retard d'une campagne
| Lieu | Annonce | Réalité mesurée |
|---|---|---|
| `gouvernance/index.html` l. 74 | « 22 pages, 11 illustrations, 10 légendes » | 29 p., 24 ill., 23 légendes |
| `gouvernance/index.html` l. 76 · KPI | « 14 / 14 embarquées · 24 pages · 3,9 Mio » | 24 / 24 · 29 pages · 7,0 Mio |
| `gouvernance/index.html` l. 107 note | « 0 licence (R3.4) » | `LICENSE` présente (MIT/l Libre, citée au CHANGELOG 2026-II) |
| `gouvernance/index.html` l. 107 | empreinte « `a0be4fb3…` » | `a129fa3f…` |
| `gouvernance/index.html` KPI poids | « 37,2 Mio de PNG » | 78,2 Mo (74,6 Mio) dans `images/` |
| `README.md`, « Points de continuité fixés » | « les **quatorze** illustrations du dossier iconographique sont toutes servies » | le dossier en compte 24 servies + 4 hors-volume (`INVENTAIRE_ICONOGRAPHIQUE.md`) — la règle est vraie, l'énoncé périmé |
| `ROADMAP_2026_II.md` / `RAPPORT_ANALYSE_2026_II.md` | « workflow de 9 étapes » | 12 `name:`/`uses:` dans `sources/github_actions_continuite.yml` |

Corrections de pure documentation, à servir au prochain commit de chiffres.

### 🔵 E-28 · Poids : la mesure de R1.6 est à reprendre, et elle est maintenant deux fois pire
37,2 Mio annoncés au bilan d'Horizon 0 → **78,2 Mo de PNG** depuis la campagne 2026-II
(10 portraits dynastiques + 4 planches de chantier). Rééchantillonnage sur 4 fichiers :

| fichier | PNG actuel | PNG réoptimisé | JPEG q90 @ ≤1500 px |
|---|---|---|---|
| `aqueduc_arches_pabst_city.png` | 3,09 Mo | 2,29 Mo | 0,46 Mo |
| `aqueduc_chantier_castors.png` | 3,05 Mo | 2,27 Mo | 0,44 Mo |
| `aqueduc_jour_de_l_eau.png` | 3,15 Mo | 2,14 Mo | 0,41 Mo |
| `aqueduc_premier_coup_pelle.png` | 3,04 Mo | 2,15 Mo | 0,40 Mo |

soit **≈ 14 % du poids actuel** pour un rendu d'écran, la chaîne d'impression passant déjà par
`prepared_image()` (thumbnail 1500×900, JPEG q78). Dépôt : 250 Mo, `.git` 93 Mo, `.gitattributes`
déclare `binary` **sans** filtre LFS, deux PDF de 7 et 15 Mo historifiés. Le choix recommandé au
ticket R1.6 — maîtres hors dépôt, dérivés produits par le générateur — reste le bon et n'est pas
coûteux ; la quantification PNG (−75 %) demeure justement rejetée.
**Contrainte à consigner** : réencoder les maîtres change **chaque flux embarqué**, donc l'empreinte
sémantique → `make empreinte` + Avis au Registre, dans le même commit.

---

## 4. Ce qui a été vérifié et trouvé juste

À consigner comme acquis, pour que la contre-expertise ne soit pas soupçonnée de parti pris :

1. **continuité interne** : aucune des six formulations obsolètes traquées n'est revenue ; les sept
   règles épinglées sont présentes ; structure `LIVRE I…VII` conforme ; 23/23 ancres résolues.
2. **artefact** : 29 pages, 24 illustrations embarquées pour 24 promises, 23 légendes, aucun renvoi
   orphelin, aucune fuite de chemin `images/`.
3. **fraîcheur** : empreinte du PDF publié = empreinte gravée ; **et** le PDF régénéré depuis le
   Markdown courant redonne la même empreinte → l'artefact n'a pas dérivé du source (le point que
   rien d'autre que ce test ne prouvait).
4. **déterminisme** : arbre régénéré identique au bit près, y compris hors du dépôt.
5. **archives** : les deux hachés de `gouvernance/ARCHIVE.sha256` correspondent aux fichiers déposés.
6. **géographie** : 3 500 + 1 200 + 800 + 1 500 = 7 000 ; urbain 5 500 ; Monts à population nulle et
   `depuis = 1962` ; atlas, SVG et PNG présents et conformes à leurs propres invariants.
7. **monnaie** : 1 Babber = 24 Babetons, l'échelle 24/12/6/2/1 est régulière, la Série B est datée 2026.
8. **succession** : Fou premier, Ti-Babber second, Déchiré collatéral, aucun conflit d'âge ou de
   filiation relevé sur les 18 figures (dont Babette-Marine, 1836, fille cadette d'un père né 1798).
9. **chroniques** : sept livres, bandeau de statut conforme ; les deux rédactions du Livre II
   coexistent **assumées et déclarées** (40 vs 42 bancs, signalé au README) — un désaccord
   documenté n'est pas une incohérence.
10. **licence, citation, changelog** : présents ; `CITATION.cff` se lit ; 0 lien mort sur les 86 fichiers.

---

## 5. Programme proposé (à porter en roadmap, horizons 0 et 1)

| id | action | effort | bloque |
|---|---|---|---|
| **C0.1** | appariement légende↔flux par page + empreinte ordonnée (E-18) | 1 h | toute la valeur du contrat de fraîcheur |
| **C0.2** | `make controle` : ordre `arbre pdf controle empreinte` + cible `scelle` (E-21, E-23.1) | 10 min | auto-validation, gel non vérifié |
| **C0.3** | gabarit à 13 étapes + `make workflows` ; supprimer le talon invalide ; corriger « 9 étapes » (E-23.2) — **poussage du fichier `.github/` hors de portée de l'App** | 1 commit + 1 poussage humain | E-17, R0.4 |
| **C0.4** | garde-fou des cinq silences dans `check_continuity.py` (E-24) | 8 lignes | SERMENT §III, promesse fausse |
| **C1.1** | `sources/check_canon.py` : parité JSON/Registre/Chronologie + arithmétique des successions (E-19, E-26) | 1 h | R3.3, qui livrait une quatrième copie sans contrat |
| **C1.2** | `check_pdf` : double inclusion par md5 + fonction commune (E-22) | 30 min | angles morts de comptage |
| **C1.3** | contrôle d'anachronisme des Monts réécrit (E-20) | 6 lignes | GEO-2026-II-01 |
| **C1.4** | ancres par identifiants `<!-- fig:… -->` (E-25) | 1 h | fragilité de titres-ancre |
| **C1.5** | trancher les 4 dates divergentes + l'ordinal du Dormeur + « saucière/Sauciériste » | 4 Avis | E-19, E-16 (à joindre au lot d'arbitrages) |
| **C2.1** | reprise des chiffres de diffusion (E-27) | 20 min | `gouvernance/index.html`, README |
| **C2.2** | R1.6 remesuré, maîtres hors dépôt (E-28) | 3 h | poids, et `git clone` de 250 Mo |

**Ordonnancement recommandé** : C0.1 avant tout — sans lui, E-19, E-22 et E-26 se produiront de
nouveau *en silence*, et le dispositif, qui se présente comme une démonstration, restera une
collection d'assertions de présence. Les correctifs sont d'outillage : ils ne touchent pas au texte
canonique, donc n'exigent aucun Avis, hors C1.5 et la nouvelle gravure de l'empreinte.

---

## 6. Suivi d'exécution — lot C0 appliqué le 29 août 2026

Le correctif est d'outillage : il ne touche pas une ligne du texte canonique, donc ne demande
aucun Avis — sauf la nouvelle gravure du contrat de fraîcheur, consignée ici et au CHANGELOG.

| Constat | Verdict | Mesure après correction |
|---|---|---|
| **E-18** · contrat insensible à l'affectation | ✅ **Clos** | Empreinte **ordonnée page à page** (`pdf_fingerprint.py`) + **appariement planche↔légende** (`check_pdf.py`, sur le md5 du dérivé réellement embarqué). P1 rejoué : *permutation de deux portraits → `make tout` échoue à `controle`, empreinte `a190819f…` contre `708776c8…` gravée* ; P1b, où le scribe réimprime sans re-sceller les maîtres → **bloqué par `make scelle`**. Contrat gravé à nouveau : `708776c8a6734880139a5b876f720949` (29 p., 24 ill., 25 placements). |
| **E-19** · données JSON sans contrôle | ✅ **Clos** | Nouveau `sources/check_canon.py`, branché sur `make controle` et sur la CI. Les deux mutations du tableau §3 (génération 7→8, population 9 000) **échouent désormais** ; idem pour une date de Chronologie décrochée (M15) et un événement hors corpus (M14). |
| **E-19.bis** · quatre fiches divergentes | ✅ **Aligné** | `canon/personnages.json` et `gouvernance/REGISTRE_DES_PERSONNAGES.md` ramené à 2026-I : Babette Ire **1804**–1892, Hortense **1840–1922**, Babette-Marine **1836**–1916, Irène **1882**–1966 ; « Babber ~~Ier~~ le Dormeur » ; la monnaie reprend les noms du canon (Six-Pack, Cuivre Populaire, Demi-Babber). *Deux sources canoniques concordantes — 2026-I et la Chronologie — appuyaient chaque correction ; l'archive gelée 2026-H dit pareil, ce qui ferme la question du sens.* |
| **E-19.ter** · affirmations sans source dans `canon/` | ✅ **Contractualisé** | Une donnée de `canon/` est **attestée** par le corpus ou **déclarée** : le champ `propositions_declarées` accueille désormais les 1 500 âmes de la forêt (chiffre de l'atlas, `geographie/ANALYSE.md`), la Paire de 2 Babetons (à frapper par le Grand Argentier), « La Caisse », « La Canette », l'alias « Le Quart de Babber » et le **12 octobre 1904** (Jour de l'Eau, né des chroniques). Le contrôle refuse aussi l'inverse : une déclaration devenue inutile. |
| **E-20** · anachronisme des Monts invérifiable | ✅ **Clos** | Règle réécrite **cellule par cellule** (un « Futur… » voisin, qui parle d'un autre personnage, n'absout plus rien — piège mesuré à la première version du correctif). M1 rejoué : *Monts affirmés en 1946 → `check_geography` échoue* ; la ligne légitime de 1912 (`Futur créateur des Monts Froissés`) passe, et une mention hors Chronologie ne déclenche **aucun faux positif**. |
| **E-21** · `make tout` se note lui-même | ✅ **Clos** | `tout: arbre pdf controle empreinte` ; le RITE de publication est réécrit en cinq étapes avec ce principe en exergue, et la CI ne grave jamais. |
| **E-22** · comptage, non identité | ✅ **Clos** | Double inclusion par contenu (chaque promesse doit être embarquée, tout flux doit être promis) + règle inverse dans `check_continuity` ; transformée d'image unique dans `sources/babberland_images.py`, partagée générateur/contrôles (fin de la double définition des masques, du cache `stem+.jpg`, de la normalisation divergente). P2 rejoué : *planche de plus sans promesse du canon → bloqué, même volume réimprimmé et scellés re-scellés*. |
| **E-23** · CI inerte, scellé non vérifié | 🟡 **Clos côté gabarit, ouvert côté poussage** | Le modèle `sources/github_actions_continuite.yml` passe à **13 étapes** (parité des données, artéfact apparié, les deux scellés), YAML validé à la main (PyYAML) et chaque étape rejouée localement ; `make workflows` l'installe, le talon invalide `main.yml` est retiré de l'arbre de travail ; `make scelle` est devenu la sixième étape du contrôle local. **Ce que la machine n'a pas pu faire** : pousser `.github/workflows/*` — GitHub refuse ce chemin à un jeton d'App sans le droit `workflows` (E-17, qui n'est donc pas un constat clos mais une permission à accorder). L'installation reste un acte humain : merge du gabarit et de sa copie, ou `make workflows` poussé par un compte habilité. |
| **E-24** · faux promesse du Serment | ✅ **Clos** | `SILENCE`/`SILENCE_EVENEMENTS` dans `check_continuity.py` : naissance chiffrée du Déchiré ou de Roger Bontemps, heure sur la Transparence brune ou la première pierre, grammage de la recette → échec explicite « silence sanctifié percé ». P3 rejoué : *Bontemps né en 1802 → bloqué* (auparavant : trois contrôles verts). |
| **E-25** · titres comme ancres | ⏳ **Ouvert** | Le correctif léger (marqueurs `<!-- fig:… -->`) reste à faire : il touche au Markdown canonique, donc relève d'un Avis. La règle inverse d'E-22 en diminue la portée (une ancre qui casse ne fait plus disparaître une planche dans le silence). |
| **E-26** · dates non recoupées, successions non calculées | ✅ **Clos** | `check_canon.py` §F : durée annoncée = soustraction des bornes pour les **6 règnes** du tableau §IX, chaîne continue sans trou ni chevauchement, mort du souverain = fin de règne. M3 rejoué : *1959 → 1958 dans 2026-I seul → bloqué*. |
| **E-27** · diffusion en retard d'une campagne | ✅ **Repris** | `gouvernance/index.html` resynchronisé (29 p. · 24 ill. · 23 légendes · 7,0 Mio · `LICENSE` posée · empreinte `708776c8…` · poids réel 78,2 Mo) ; README : « quatorze illustrations » → vingt-quatre promises, 4 hors-volume par statut ; « 9 étapes » → 13. |
| **E-28** · poids, R1.6 | 🟠 **Mesuré, non décidé** | Rééchantillonnage consigné : 78,2 Mo de PNG, JPEG q90 @ ≤1500 px ≈ **14 %** (≈ 11 Mo) sans effet sur l'impression, `prepared_image()` bornant déjà à 1500×900 q78. La décision (maîtres hors dépôt, LFS ou Release) reste à prendre : elle regrave `ICONOGRAPHIE.sha256` **et** l'empreinte, donc un Avis. |

### Ce qui reste vrai après correction

* **Un résidu assumé** : réimprimer *et* re-sceller les deux scellés après une permutation rend le
  volume auto-cohérent — aucune machine ne peut savoir que ce visage n'est pas celui du Fou.
  Le correctif ne prétend pas à l'impossible : il transforme la faute en **acte éditorial visible**
  (une ligne de `gouvernance/ICONOGRAPHIE.sha256`, un Avis, un diff lisible). C'est la frontière
  honnête entre un contrôle et un serment.
* **Chaîne verte** après correction : `make tout` (arbre → PDF → six contrôles → gravure) passe,
  avec `24 flux embarqués pour 24 promesses`, `23 légendes appariées à leur flux sur la même page`,
  `28 maîtres conformes`, archives intactes — et le régénéré est **neutre** : pages, texte et
  disposition par page identiques à l'artefact d'avant refactor (`ca8121b6…` / `cd6fdb58…`).
* **Batterie** : 15 scénarios, 15 conformes (13 fautes bloquées, 2 éditions justes vertes — dont
  l'ajout d'une planche promise, ancrée et scellée, qui passe sans toucher au canon).

---

## Annexe A — Table des mutations injectées (état **avant** correction ; §6 donne le résultat après)

| # | faute injectée | attendue bloquée | résultat | commentaire |
|---|---|---|---|---|
| M1 | Monts Froissés cités en 1847 (Chronologie) | oui | 🔴 **non détecté** | E-20 |
| M2 | McBabber's ouvert en 1987 (Chronologie) | oui | ✅ bloqué (`continuite`) | date maîtresse épinglée |
| M3 | mort du Dormeur 1959 → 1958 (2026-I seul) | oui | 🔴 **non détecté** | E-26 |
| M4 | 1 Babber = 25 Babetons | oui | ✅ bloqué (`continuite`) | |
| M5 | Pabst City à 3 800 âmes | oui | ✅ bloqué (`geographie`) | |
| M6 | renvoi d'illustration retiré du canon | oui | ✅ bloqué (`pdf`, 23≠24) | |
| M7 | titre de Livre renommé | — | non détecté (bénin) | l'invariant est une regex de liste |
| M8 | ordre de succession inversé | oui | ✅ bloqué (`continuite`) | par chaîne exacte : fragile dans les deux sens |
| M9 | Ti-Babber en 8ᵉ génération (`personnages.json`) | oui | 🔴 **non détecté** | E-19 |
| M10 | `population_totale: 9000` (`lieux.json`) | oui | 🔴 **non détecté** | E-19 |
| M11 | archive H modifiée | oui | ✅ bloqué (scellé) | mais **seulement** si l'on lance `sha256sum --check` : E-23.1 |
| M12 | chronique sans bandeau « proposé, non décrété » | oui | ✅ bloqué (`continuite`) | |
| M13 | Irène préside l' Babbersgate (régression E-01) | oui | ✅ bloqué (`continuite`) | la fermeture d'E-01 tient |
| **P1** | deux portraits intervertis + `make tout` | oui | 🔴 **vert, empreinte inchangée** | E-18 |
| **P2** | planche non consentie (doublon d'octets) ajoutée au PDF | oui | 🔴 **vert** | E-22 |
| **P3** | date de naissance imposée à Roger Bontemps (silence n° 2) | oui | 🔴 **vert** | E-24 |

**Bilan : 8 bloquées / 13 fautes canoniques ; 3 scénarios d'artefact sur 3 non perçus.**
Reproduction : chaque commande est donnée dans le constat correspondant ; les six contrôles
s'exécutent par `make PY=python3 controle` dans une copie hors dépôt.

## Annexe B — Environnement de mesure

Python 3.11 · dépendances de `requirements.txt` installées telles quelles dans un venv
(reportlab 5.0.1, pillow 12.3.0, pypdf 6.16.2) · `make env` et `make controle` exécutés depuis
le dépôt, `make tout` exécuté dans `/tmp/mut6` · aucune écriture dans le dépôt de référence,
hors le présent fichier.

*Rapport clos le 29 août 2026, à la Chancellerie de Pabst City. Ce document ne décrète rien :
il constate, mesure et propose. Chaque correctif devient canonique par Avis, selon le rite en
vigueur — dont le §IV est à corriger (E-21).*
