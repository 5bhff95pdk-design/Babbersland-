# 📜 JOURNAL DES MODIFICATIONS (CHANGELOG)

Toutes les modifications notables apportées au dépôt du **Royaume du Babberland** sont consignées dans ce document.

## Rotation du journal

Le journal conserve les **cinq passes courantes** (2026-XV à 2026-XIX). Les quatorze premières
(2026-I à 2026-XIV, 26 août → 1er septembre) sont archivées telles quelles dans
`docs/clos/CHANGELOG_2026_I-XIV.md` — mêmes titres, mêmes ancres, aucune réécriture.
*Motif : le journal avait grandi plus vite que le corpus (9 800 mots, soit plus que le Livre VI
entier). Un compte rendu qui déborde le livre qu'il compte n'est plus un compte rendu.*

---

## [2026-XIX] — 2026-09-02 (Avis royal n° 10 : les lacunes sont closes, bornées, et gardées)

Le cycle des Chroniques étant homogène depuis 2026-XVIII, la session s'attaque au ticket que la
ROADMAP appelait « décision structurante » : **R2.7, fermeture des lacunes volontaires**. Elle
devait trancher entre décret de fixation et serment d'ignorance. Elle a d'abord découvert que la
question était mal posée depuis le 30 août.

### Trouvé — la promesse du Serment n'était tenue qu'à moitié, et trois listes se contredisaient

`gouvernance/SERMENT_D_IGNORANCE.md` (30 août) proclamait **cinq silences** et affirmait au § III
que « les scripts de validation rejettent toute tentative d'imposer une fixation arbitraire ».
Relu pièce en main :

| Écart | Mesure |
|---|---|
| **Trois inventaires, un seul registre** | le Serment dit cinq, la ROADMAP (R2.7) cinq autres, la Chronologie maîtresse (§ VIII) une troisième. Deux lacunes du Serment sont inconnues de la Chronologie ; deux de la Chronologie sont inconnues du Serment. |
| **La machine ne gardait pas ce que le Serment jurait** | sur les cinq silences proclamés, **deux** seulement avaient un garde dans `check_continuity.py`. La première année de la Transparence brune — proclamée par les trois listes — pouvait être fixée en toutes lettres sans qu'aucun contrôle ne bronche. |
| **Une lacune portait sur un fait inexistant** | le Serment jurait de taire l'heure de la pose de la première pierre du port ; or le registre **P-1** ne consigne aucune première pierre, ni ruban, ni discours, et le Livre II le dit expressément (tranche 5, *Le port qui n'a pas d'inauguration*). La Chancellerie avait inventé un mystère là où le corpus avait un fait. |

La leçon est celle du constat E-24, une seconde fois : **une promesse de contrôle sans contrôle
n'est pas une promesse, c'est de la rhétorique.**

### Décrété — Avis royal n° 10 · *De la Clôture des Lacunes*

* **Art. 1 — Inventaire arrêté à sept**, réconciliation faite des trois listes (tableau au registre).
* **Art. 2 — La règle de partage** : une lacune se juge à sa **portée**. Elle est **jurée** quand
  rien n'en dépend, **fixée** quand une pièce du corpus en dépend, **requalifiée** quand le fait
  dont on taisait la circonstance n'a pas eu lieu. Corollaire : **un silence juré est borné** —
  ce qui est su est dit, ce qui est tu est tu ; la borne distingue le mystère du trou.
* **Art. 3 — Une seule fixation** : le Déchiré est rattaché à Babette-Marine **au quatrième
  degré** (Gén. II → Gén. VI). Fixé parce que **l'arbre officiel en dépend** : le trait pointillé
  traverse quatre bandes sans s'arrêter sur un nom ; nommer un porteur obligerait à redessiner
  l'arbre. Les noms, eux, demeurent jurés.
* **Art. 4 — Sept silences jurés et bornés** (S1 à S7).
* **Art. 5 — Requalification** du silence de la première pierre en **silence d'inexistence** :
  il n'y a pas d'heure à taire d'une cérémonie qui n'a pas eu lieu. **C'est le Serment qui se
  trompait, et il le dit.**
* **Art. 6 — Le garde** (ci-dessous).
* **Art. 7 — Anti-dette** : toute formule du canon ou de la Chronologie qui avoue un manque doit
  être couverte par un silence décrété ou une dispense écrite. **On ne taire plus sans décréter.**
* **Art. 8 — Non-annexion** : les 7 000 âmes ne sont pas une lacune mais une proposition en
  instance de l'Avis n° 7 ; l'Avis n° 10 refuse de l'absorber.
* **Art. 9 — Exécution** : le décret touche au canon, donc il imprime (rite de publication).

### Ajouté — le registre et son garde

* **`canon/silences.json`** (nouveau, 5ᵉ fichier du dossier) — source unique : 7 silences, 1
  fixation, 16 gardes, leurs bornes, les marqueurs de lacune et les dispenses.
* **`sources/check_silences.py`** (nouveau, sans dépendance) — cinq vérifications :
  *A* registre complet et **silences bornés** ; *B* **parité registre ↔ Serment dans les deux
  sens** (un silence hors registre est une lacune non décrétée, un registre hors Serment est une
  cérémonie oubliée) ; *C* **perce-ment** sur le canon et la Chronologie ; *D* **fixation
  attestée** au canon *et* **rétro-contrôle arithmétique** (Gén. VI − Gén. II = 4) ; *E* **chasse
  aux lacunes non décrétées** (art. 7).
* **Délégation** — `check_continuity.py` ne *définit* plus les silences (deux figures en dur, deux
  motifs d'événements) : il les **applique** au canon via le registre. Une seule source, un seul
  endroit où l'on se trompe.
* Branché à **`make controle`** et à une **21ᵉ étape CI bloquante** (modèle et copie installée
  resynchronisés, parité R1.8 tenue).

### Éprouvé — douze fautes refusées, une lacune décrétée acceptée

Rejoué sur copies isolées avant livraison : naissance imposée à Bontemps ou au Déchiré, lieu de
naissance, âge, porteur intermédiaire nommé, année de la première Transparence brune, date de la
transmission de la sauce, grammage des aromates, heure donnée à une première pierre, fixation
retirée du canon, écart des générations faussé (5 ou 7), silence retiré du Serment, silence
ajouté au registre sans décret — **12/12 refusées**. La batterie en reprend trois (S5, F1, E1)
jugés par `check_silences` **seul**, selon la leçon de R1.9 : un scénario de garde-fou doit être
refusé par le mécanisme qu'il prouve, pas par un voisin.

### Corrigé — un défaut préexistant de la batterie (V2 et R1 échouaient déjà sur `HEAD`)

En rejouant `make batterie`, les scénarios légitimes **V2** et **R1** — ceux qui ajoutent une
planche promise, ancrée et scellée — échouaient. Vérifié sur `git archive HEAD` : **ils
échouaient avant tout changement de cette session.** Cause : R1.3 a mis
`check_manifest.py --check` dans la chaîne le 1ᵉʳ septembre, et `regenerer()` réimprimait le
volume et re-gravait l'empreinte **sans re-graver le manifeste** — scellé du texte depuis R1.3.
La batterie prouvait donc la chaîne d'avant R1.3. `regenerer()` suit désormais le rite entier
(compiler, vérifier, **graver**, sceller). Leçons E-13 et E-21, appliquées à la batterie
elle-même : un garde-fou qui ne suit pas le rite prouve le rite d'hier.

### Rejoué — le rite de publication, puisque le canon a changé

Art. 9 : *un décret qui n'imprime pas n'a pas eu lieu.* La fixation est inscrite à 2026-I
(Génération VI, § 2) ; le volume est réimprimé, l'empreinte sémantique regravée
(`e1168ee0…` → **`566914094df86c169cfb14ab8ebd66a2`**), et le **manifeste** rescellé avec la
Chronologie, dont le § VIII est mis en conformité (*Dates non consignées par décret*, sept
entrées cotées S1–S7 + F1). `make controle` **vert** — 13 vérifications, 4 empreintes, 4 scellés.
`make batterie` **31/31** (27 → 31 scénarios).

### Suivi — une variante de rendu à réaccepter (connu, documenté, tracé — **exécuté le jour même**)

La réimpression du volume **périme la variante PDF acceptée** `ci-ubuntu-24.04-py3.12`
(`fingerprint:1a76a0e8…`, R1.4.g) : la charge d'un rendu dépend du texte, et le texte a changé.
Le runner refusera au premier run, et c'est le comportement voulu — la cérémonie d'acceptation
existe pour ça (`pdf_fingerprint.py --accepter '<charge>' <étiquette>`, lue dans l'annotation du
run). Consigné dans `gouvernance/CI_LIMITES.md`. Ce n'est pas une régression : c'est le prix
connu, deux poussées par changement de contenu, tant que R1.2 (matrice multi-OS) n'existe pas.

**Fait le jour même** : run **#33644149960** refusé comme annoncé, annotation lue
(`nature=EMBALLAGE` — texte et pagination conformes, seuls les octets JPEG diffèrent), charge
acceptée à la main. Seconde poussée : **run #33644538835, CI verte, 21 étapes**, garde des
silences comprise.

### Docs

`gouvernance/SERMENT_D_IGNORANCE.md` (refondu, miroir lisible du registre),
`gouvernance/REGISTRE_DES_AVIS_ROYAUX.md` (Avis n° 10), `CHRONOLOGIE_MAITRESSE_1847_2026.md`
(§ VIII), `canon/personnages.json` (fiche du Déchiré + déclaration attestée),
`sources/check_canon.py` (message : 4 → 5 fichiers JSON, le compte est calculé, plus écrit),
`ROADMAP_2026_II.md` (R2.7 ✅), `gouvernance/CI_LIMITES.md`, `README.md`.

---

## [2026-XVIII] — 2026-09-02 (Livre VI — le dernier moignon du cycle, et quatre écarts au canon)

Suite immédiate de 2026-XVII. Le Livre VI était le second synopsis du corpus ; il est le
dernier. Les six Livres sont désormais au même standard, et **le premier grand cycle
(1798–2026) est homogène**.

### Étoffé — `chroniques/LIVRE_VI_LE_SIECLE_QUI_LOUCHE.md` (171 → 517 lignes)

* **Écrit** : les deux sillons de patin sur les dalles de la cour d'honneur et le laissez-passer
  du mobilier ; l'épreuve du stéthoscope appliqué à la joue et non au fromage, et les quatre
  articles du Label qui ne définissent qu'une **durée** ; les dix-neuf formulations écartées des
  moulins, l'avis de la Banque sur la lavande (*« un billet qui sent bon revient plus vite en
  circulation »*), la démonstration de Linéa faisant le tour de la table, et le billet de 50
  qui ne représente personne ; les huit secondes de viscosité et les trois mille relevés de
  fûts du Prince Héritier ; le flacon de ketchup posé au centre et auquel personne ne touche,
  la clause de la demande expresse, les rideaux tirés sur la visite pontificale ; les
  trente-neuf minutes d'attente avant la cloche ; la nuit des cuisines, la délibération en
  pantoufles et le dernier servi.

### Corrigé — quatre écarts au canon, relevés en lisant 2026-I avant d'écrire

Une chronique **peut taire, elle ne peut pas contredire**. Le texte existant contredisait :

| Écart | Ce que disait le Livre VI | Ce que dit 2026-I |
|---|---|---|
| **Le faux fromage** | trois tonnes de cubes plastiques importés, refusant de fondre | l'inspection « démontra qu'il s'agissait **bien de fromage**, mais d'un fromage si timide qu'il se cachait sous la sauce » |
| **Le Label 2018** | distance de charrette, fabrication avant l'aube, chargement transformé en bouchons | le Label mesure **une durée de fonte**, rien d'autre ; la peine fut une tranche gratuite pendant un mois |
| **Les séries fiduciaires** | la Série A décrite comme du chanvre indéchirable | **Série A = 2023** (chanvre + lin) ; **Série B = 2026** (chanvre pur, indéchirable). Le 1 Babber de la B reprend le recto de type A |
| **La Nuit des Sept Mille** | deux cornichons distribués à **chaque** citoyen | **un seul** burger — le sept-millième — en reçut deux ; les **6 999** autres furent distribués normalement, et le fautif mis sous cloche au musée |

Le quatrième écart était le plus coûteux : il effaçait l'anecdote qui **fonde** la Fête de la
Double Garniture. La tranche 7 la restitue, cloche de verre comprise, et l'annonce en note de
tête pour couper court à l'embellissement oral.

### Tenu — continuité et contraintes mécaniques

* **Avis royal n° 5** rappelé en tête et respecté sur sept tranches : le chiffre **VII** marque la
  **septième génération**, non un septième règne ; le Louche règne toujours, le Fou est premier
  successible, Ti-Babber second. Le roi exige d'ailleurs, dans la proclamation, que le mot
  *génération* figure dans la phrase — « afin qu'aucun chroniqueur ne pût, plus tard, lire un
  règne dans un chiffre ».
* **Lacunes volontaires gardées ouvertes et dites** : le total de 7 000 âmes est signalé comme
  proposition en attente de l'Avis n° 7 ; l'année de la première Journée de la Transparence
  brune n'est pas fixée ; la valeur chiffrée de la Parité Poutine reste tue — le billet de 50
  « qui la montre, se garde bien de la dire ».
* **Grandeurs chiffrées** : relevé inchangé, `population = {7000}` pour ce volume. Les 6 999
  burgers ne sont pas un dénombrement d'âmes et n'ont pas fait dériver le contrôle.
* **Cotes** : 6 ajoutées (`KOUIK-2018`, `MOUL-2020`, `CHAI-2016`, les *bis*…), choisies hors des
  cotes déjà prises — **85 cotes relevées, aucune collision nouvelle**, les deux connues
  (G-1, P-3) restant seules déclarées.
* `make controle` **vert** — 12 vérifications, 4 empreintes, 4 scellés. Aucun artéfact régénéré.

---

## [2026-XVII] — 2026-09-02 (Livre V — rendre au récit ce que la gouvernance lui prenait)

Le § 5 de la note d'audit, réécrit le matin même, constatait que l'appareil critique pesait
plus lourd que l'œuvre. Cette entrée est la première à faire l'inverse : **aucun contrôle
ajouté, aucun scellé regravé, 417 lignes de chronique**.

### Étoffé — `chroniques/LIVRE_V_LUNION_DES_REGNES.md` (194 → 611 lignes)

* **Le manque, mesuré** : le Livre V annonçait sept tranches et n'en développait qu'une
  section chacune — un synopsis, pas une chronique. Il expédiait en 194 lignes ce à quoi le
  Livre II consacre 1266 lignes pour un seul aqueduc. Le Livre VI (171 lignes) est dans le
  même état ; il reste à faire.
* **Ce qui est écrit** : la règle des jours pairs et impairs et ses quatre lignes de
  règlement (**UR-1998**), le fauteuil du plateau resté vide douze ans, la fiole de sable
  d'Henri-Grain et l'heure du Grain ; l'affaire de la taupe et les trois journées de sieste
  officielle ; la propagation du Pabstgate, la doctrine de la preuve qui se réchauffe,
  l'étalonnage sur le thermomètre de 1898 et le sort du garçon de salle ; la méthode du
  canif et le triple refus de 2006 ; la barricade de pots, les deux affiches et les quatre
  articles du Traité du Vinaigre Doux ; le dernier 31 décembre et la fiole vidée ;
  l'objection écrite du Grand Argentier et le registre du thermomètre maître.
* **Continuité tenue** : le rappel en tête de volume impose le titre de *prince* à Babber le
  Louche jusqu'au 2 janvier 2010 (règle n° 1 de la chronologie maîtresse) ; le volume s'y
  astreint sur sept tranches. Les lacunes volontaires du canon restent ouvertes et **dites** —
  `COL-2006` va jusqu'à enregistrer que la Chancellerie *refuse* de préciser les degrés de la
  branche collatérale.
* **Contraintes mécaniques respectées, et c'était l'essentiel** : `check_chroniques.py`
  échoue sur toute grandeur chiffrée nouvelle. Le relevé du volume est resté à `population
  = {5}` (la délégation de 2004), et le texte ne dénombre ni bancs, ni canaux, ni arches, ni
  villes, ni régions, ni kilomètres. Les douze cotes ajoutées (`UR-1999`, `ZINC-2004`,
  `CRIS-2010`…) ont été choisies hors des 77 cotes déjà prises par le corpus : **79 cotes
  relevées, aucune collision nouvelle**, les deux connues (G-1, P-3) restant seules déclarées.
* `make controle` **vert** — 12 vérifications, 4 empreintes, 4 scellés. Aucun artéfact
  régénéré, aucune empreinte regravée : une chronique ne touche pas au canon.

### Corrigé — une analyse fausse, dite ici pour mémoire

L'analyse du dépôt affirmait que le corpus narratif se réduisait à « un seul Livre de
chroniques ». **C'était faux** : les six Livres existent (3 918 lignes), le README les liste
tous, et le Livre II — donné pour manquant — est le plus abouti de l'ensemble. Le manque réel
était l'inégalité de traitement entre les volumes I–IV et les volumes V–VI. Écrire un
« Livre II » aurait écrasé le meilleur texte du fonds.

---

## [2026-XVI] — 2026-09-02 (R1.6 — le poids des images : une décision, pas un runbook qui traîne)

Le constat C2 de la note d'audit (« 119 Mio d'images committés ») était ouvert depuis le
30 août, avec un runbook complet en face — et personne pour trancher. Un runbook « prêt, non
exécuté » qui survit à deux campagnes n'est plus une procédure : c'est une dette qui se
raconte des histoires. Cette entrée ferme la question par un décret, sans déplacer un octet.

### Décrété — Avis royal n° 9, transport des images lourdes
* **Variante A′ retenue** : `images/realistes/*.png` (227 Mio, 83 clichés), `images/vignettes/*.webp`
  et `audio/*` passent au transport Git LFS — ≈ 236 Mio sortis du magasin Git à terme.
* **Option B écartée** : la réécriture de l'historique de `main` aurait ramené le dépôt sous
  5 Mio, mais brisé tout clone et toute branche en cours. Le principe l'emporte sur les octets —
  *le passé du Royaume ne se réécrit pas*, dans la ligne du scellement des archives G/H (Avis n° 6).
* **Restent en Git** : les 28 maîtres scellés (75 Mio) et les 2 PDF (22 Mio) — dans la chaîne,
  déjà dans l'historique, rien à gagner à les en sortir.
* **Aucun plafond de poids institué** (art. 6) : la garde coûterait en cérémonie ce qu'elle
  épargnerait en octets. La croissance des images reste un jugement éditorial.

### Mesuré — le blocage réseau tient, la migration ne s'exécute pas ici
* Sondes reconduites le 2 septembre, identiques au 30 août : `api.github.com` → **200**,
  `github-cloud.s3.amazonaws.com` et `uploads.github.com` → **SSL_ERROR_SYSCALL**, `git-lfs` absent.
* Conséquence gravée aux art. 3 et 4 : **défense d'engager la migration depuis l'environnement
  d'agent**, et **aucun filtre LFS n'est inscrit à `.gitattributes`** avant téléversement possible.
  Un filtre posé d'avance transformerait le prochain commit binaire en pointeur orphelin —
  dépôt intact ici, en ruine pour tous les autres. `.gitattributes` reste à ses deux lignes `binary`.

### Corrigé — la documentation avait une campagne de retard (passe 2, même jour)

Même classe de dérive que E-27, appliquée cette fois aux documents *méta* — ceux que la chaîne
ne contrôle pas, faute de pouvoir contrôler de la prose.

* **`README.md` — les 24/28 illustrations n'étaient pas contradictoires, mais indistinctes** :
  « 28 maîtres du volume 2026-I » laissait croire que les 28 entrent dans le PDF, alors que
  **24 y entrent** et que **4 planches de chantier** restent hors volume par statut. La phrase
  dit désormais 28 scellés dont 24 embarqués, ce qui réconcilie avec le § « vingt-quatre
  illustrations promises » et avec `check_pdf.py`.
* **`docs/clos/ANALYSE_ET_PROPOSITIONS_2026.md` — deux constats périmés donnaient une image fausse** :
  C3 affirmait encore « la CI n'est pas installée, `.github/` absent » alors qu'elle tourne,
  verte, depuis le 1ᵉʳ septembre (PR #22, `9f527f3`) ; C2 chiffrait les images à 119 Mio, soit
  **presque trois fois moins que la réalité** (334 Mio hors `.git`). Les deux sont remesurés,
  datés et marqués — clos pour C3, décrété pour C2 — le texte d'origine restant lisible comme
  mémoire de l'instruction. Tableau récapitulatif doté d'une colonne **Statut**, synthèse § 5
  réécrite.
* **Fausse piste évitée, et consignée** : un `grep '^      - name:'` comptait 18 étapes de CI
  et faisait croire à une erreur dans le « 20 » du README. Le compte **au parseur YAML** donne
  bien **20** (18 nommées + `actions/checkout` + `actions/setup-python`) — convention que
  `CI_LIMITES.md` énonce explicitement : « le compte est pris au parseur, pas au grep ». La
  correction a été annulée et le README précise maintenant la ventilation, pour que le prochain
  lecteur ne refasse pas le trajet.

### Corrigé — le runbook avait une campagne de retard
* § 1 remesuré : la galerie était comptée **77 clichés / 220 Mio**, elle en pèse **83 / 227 Mio** ;
  les vignettes ont suivi (77 → 83). Le « 29 maîtres » de la première mesure était faux : il y en
  a **28**, conformément à `ICONOGRAPHIE.sha256`.
* § 3 réordonné (arbitrage rendu en tête, Option B marquée écartée), § 5 réécrit en fiche de
  statut décrété. `README.md` référence désormais le runbook et l'Avis n° 9.
* Aucun fichier de la chaîne n'est touché : `make controle` reste vert, scellés inchangés.

---

## [2026-XV] — 2026-09-01 (R1.3 — le manifeste des livrables, ce que rien ne scellait par octets)

Addenda à la vague R1.4 : le ticket de fond R1.3 était resté ouvert, plus petit que
ses voisins mais du même grain — un corpus sans scellé, un acte d'assentiment à rendre
lisible. Il est livré le même jour, sans toucher à la matrice multi-OS (qui reste R1.2).

### Ajouté — `gouvernance/MANIFEST.sha256`, le manifeste du corpus canonique livré
* **Le trou, mesuré par R0.5 et par l'audit (E-12/E-13)** : le dépôt scellait ses archives
  G/H (`ARCHIVE.sha256`), ses 28 maîtres (`ICONOGRAPHIE.sha256`), ses 77 clichés
  réalistes (`GALERIE.sha256`) et signait le PDF *sémantiquement* (`pdf_fingerprint.txt`).
  Mais le **texte qui fait foi** (2026-I), la **chronologie maîtresse** et la **source
  vectorielle de l'arbre** n'avaient aucun scellé par octets : une retouche silencieuse
  de l'un d'eux ne laissait aucune trace mécanique.
* Le périmètre initial du ticket (« 2 PDF + 14 PNG = 16 lignes ») datait de l'audit et
  **recouvrait des corpus déjà scellés** ; le manifeste scelle donc ce qui ne l'était pas :
  `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`, `CHRONOLOGIE_MAITRESSE_1847_2026.md`,
  `sources/arbre_genealogique_complet.svg`. Le PDF reste délégué à sa fraîcheur sémantique
  (ses octets ne sont pas déterministes), les images à `ICONOGRAPHIE`/`GALERIE`.
* Gravé par le but **`make manifest`** (`sources/make_manifest.py`), vérifié par
  `sources/check_manifest.py --check` — brancheé dans `make controle` **et** en CI
  (`check_manifest.py --check`, étape bloquante dédiée).

### Vérifié — le scellé mord, et il reste compatible
* `make controle` **vert** (12 vérifications + scellés + **manifeste vérifié**).
* Un ajout de ligne à 2026-I fait **échouer** `check_manifest.py --check` (exit 1) et
  `sha256sum --check` (même verdict), puis repasse vert une fois restauré : le re-grave
  explicite est bien le seul passage, pas une tolérance silencieuse.

### Mis à jour
* `Makefile` (buts `manifest` ; `controle` appelant `check_manifest.py --check`),
  `sources/github_actions_continuite.yml` **et sa copie installée** (resynchronisée par
  `make workflows`, la parité R1.8 l'exige), `README.md` (table de gouvernance, buts,
  validation), `gouvernance/CI_LIMITES.md` (état courant : **20 étapes, 0 tolérante**),
  `ROADMAP_2026_II.md` (R1.3 ✅, retiré de « Reste ouvert »).
* `make controle` rejoué après coup : la chaîne reste verte, la parité des workflows (R1.8)
  aussi.

---
