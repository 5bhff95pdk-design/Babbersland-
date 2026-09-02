# 🔍 RAPPORT D'AUDIT COMPLET — ROYAUME DU BABBERLAND

> **Note de la Chancellerie (29 août 2026).** Ce rapport dormait dans la **pull request #11**, en
> conflit avec `main` : il est rapatrié ici pour que l'archive ne perde pas un document qu'elle cite.
> Il décrit l'état du dépôt au commit `4757a76` (28 août) ; plusieurs constats ont depuis été traités
> par la contre-expertise RC-2026-III-01 et par la PR #16. Il est donc **historique** : on le lit
> pour la méthode et pour ce qui reste ouvert, pas pour l'état courant.
>
> * **F-01** (workflow CI invalide, gabarit non installé) → PR #16 : gabarit porté à 15 étapes,
>   installation toujours bloquée par le droit `workflows` de l'App (E-17).
> * **F-02** (cotes d'archives en collision) et **F-03** (généalogie castorale) → renvoyés à l'Avis
>   royal n° 7 par le `gouvernance/DIVERGENCES_CHRONIQUES.md`, et désormais **contrôlés** :
>   `sources/check_chroniques.py` relève les collisions de cotes, plus une que F-02 n'avait pas vue.

**Référence** : AUD-2026-III · audit indépendant de troisième passe
**Date d'examen** : 28 août 2026 · état du dépôt : branche `arena/01a049ea-babbersland`, commit `4757a76` (fusion PR #10)
**Version 1.1** (seconde passe, 28 août 2026) : F-22 et F-23 ajoutées ; F-02 affinée (cotes partiellement déclarées en roadmap) ; iconographie vérifiée visuellement sur les fichiers ; liste « vérifié conforme » étendue (Lois fondamentales, article par article, archive G).
**Version 1.2** (28 août 2026) : corrections appliquées à la suite du rapport — état exécuté en § 5bis.
**Périmètre** : intégralité du dépôt — canon 2026-I, chronologie maîtresse, archives scellées 2026-G (PDF) et 2026-H (MD), cinq volumes de chroniques (dont deux rédactions du Livre II), atlas géographique (analyse, gazetteer, générateur), quatre contrôleurs + générateurs Python, Makefile, workflows CI, inventaires, rapports et roadmaps antérieurs.
**Méthode** : lecture intégrale de chaque document narratif ; recalcul à la main de tous les âges, durées et arithmétiques ; vérification des jours de semaine (calendrier grégorien prolongé) ; confrontations croisées canon ↔ chronologie ↔ archives G/H ↔ chroniques ↔ atlas ↔ générateurs ; exécution de `make controle` et `make tout` (régénération complète) dans un venv épinglé (reportlab 5.0.1 · pillow 12.3.0 · pypdf 6.16.2) ; vérification des scellés `sha256sum --check` ; extraction et lecture des deux PDF scellés/publiés.

---

## 1. Synthèse

| Axe | Verdict |
|---|---|
| **Canon 2026-I (texte)** | ✅ Aucune contradiction interne trouvée (dates, règnes, âges, arithmétique, filiation, ordinaux) |
| **Contrôles embarqués** | ✅ 4/4 verts ; `make tout` reproductible (arbre au bit près, atlas au bit près, empreinte sémantique identique ; PDF ± 4 octets — écart E-10 connu, absorbé par l'empreinte) |
| **Archives scellées** | ✅ Scellés 2026-G et 2026-H intacts ; 2026-H conforme à 2026-I |
| **CI GitHub** | 🔴 **Défaut majeur (F-01)** : le workflow commité est invalide ; le workflow documenté n'est pas installé |
| **Chroniques (hors canon)** | 🟠 10 défauts de contenu (F-03 à F-14), dont une contradiction inter-volumes (F-03) |
| **Atlas (proposé)** | 🟠 3 erreurs de datation (F-15 à F-17) |
| **Documentation** | 🟡 5 défauts (F-18 à F-21, F-23) |
| **Iconographie** | ⚪ défauts de lettrage : 5 déclarés confirmés + 6 non listés (F-22) |
| **Dossiers ouverts antérieurs** | ⏸ 6 points de E-14/E-15/E-16 toujours en attente d'arbitrage (§3) |

**En une phrase** : l'univers canonique est rigoureux et les chaînes de contrôle font leur travail ; les défauts subsistants se concentrent hors du canon — un workflow CI commité qui est en réalité une URL collée, un espace de cotes d'archives utilisé de façon contradictoire par les deux rédactions du Livre II, une dizaine de coquilles arithmétiques dans les chroniques (proposées, non décrétées), trois datations erronées de l'atlas, et quelques obsolétesses du README.

---

## 2. Constats

Gravité : 🔴 majeur (bloque) · 🟠 moyen · 🟡 mineur · ⚪ cosmétique.

### A. Infrastructure

#### 🔴 F-01 · Le workflow CI commité est invalide ; le workflow documenté n'est pas installé

**Fait.** `.github/workflows/main.yml` contient exactement 25 octets :

```
github.com/settings/apps
```

Ce n'est pas un workflow : pas de `name`, pas de `on`, pas de `jobs`. GitHub Actions ne peut pas le parser — chaque push sur `main` et chaque pull request produit une erreur de configuration plutôt que les contrôles.

Pendant ce temps, le workflow réellement documenté (`sources/github_actions_continuite.yml`, 9 étapes : dépendances épinglées, polices, continuité, atlas, arbre au bit près, régénération, artéfact, empreinte, scellés, pièce jointe) **n'est pas installé** : le fichier `.github/workflows/continuite.yml` n'existe pas dans le dépôt, alors que :

- le but `make workflows` du `Makefile` est précisément censé le créer ;
- le commentaire de `gouvernance/ARCHIVE.sha256` annonce « Étape bloquante de la CI : `.github/workflows/continuite.yml` » ;
- le README affirme « Les mêmes contrôles sont enchaînés à chaque push sur `main` et à chaque pull request par le workflow `sources/github_actions_continuite.yml` ».

**Conséquence.** Le scellé des archives G/H, la parité bit-à-bit de l'arbre, la fraîcheur du PDF et la continuité des sources ne sont vérifiés nulle part automatiquement ; le seul workflow actif est en échec permanent.

**Cause probable.** L'activation manuelle promise par RA-2026-II (constat E-17 : le jeton d'application n'avait pas la permission `workflows`) s'est faite depuis `github.com/settings/apps` — et l'URL a été collée à la place du YAML.

**Correctif.** 1) supprimer (ou remplacer par un workflow valide) `.github/workflows/main.yml` ; 2) `make workflows` puis commit de `continuite.yml` ; 3) vérifier une exécution verte. Effort : 1 commit, ~5 minutes.

---

### B. Structure éditoriale

#### 🟠 F-02 · Huit cotes d'archives en collision entre les deux rédactions du Livre II

Les deux rédactions, conservées côte à côte dans `chroniques/` (statut « proposé, non décrété » pour les deux), attribuent la **même cote à des documents différents** :

| Cote | 1ʳᵉ rédaction (*Les Bâtisseurs*) | 2ᵉ rédaction (*Le Silence et l'Aqueduc*) |
|---|---|---|
| **A-34** | Rapport castoral de l'automne 1891 : « Il mesure. Il ne creuse pas. Il apprend. » (l. 980) | Rapports castoraux de la régence 1889–1892 ; « silence, correct, pour, cause » (l. 31) |
| **A-37** | Le dos de castor, verdict « Deux coups. » (1897) (l. 987) | Rapport de la soirée de la régence : « Elle tient encore. » (l. 61) |
| **P-1** | Premier registre du port : « Port Babette. » (1893) et « Fleuve Babber. » (1896) (l. 989) | Marché de la Remise aux Plans, futur Palais royal (1892) (l. 533) |
| **Q-2** | Plan d'exécution du Double Aqueduc, bancs en trait plein (1892) (l. 983) | Registres du chantier du Double Aqueduc (1893–1904) (l. 536) |
| **Q-3** | Le plan des bancs, annexe (1893) — *un document* (l. 985) | La première motte — *un objet sous verre* (l. 537) |
| **A-41** | Expertise de la Grande Fuite (1901) (l. 991) | Rapport castoral sur la reprise du chantier de la digue (1893–1896) (l. 211) |
| **A-44** | Procès-verbal de la première audience horizontale, 3 mai 1910 (l. 995) | Rapport de contrôle de la digue : « Un coup. » (1896) (l. 243) |
| **M-1** | Journal de la malterie (l. 999) | Journal de la Brasserie Haute (depuis 1896) (l. 251) |

Le README ne déclare que la divergence sur le nombre de bancs (« elles divergent, **entre autres**, sur le nombre de bancs : quarante contre quarante-deux »). La `ROADMAP_2026_II.md` (suivi R2.8) mentionne bien les « cotes d'archives » parmi les divergences des deux rédactions — la collision est donc **connue**, mais nulle part chiffrée ni énumérée. Aucune vérification (`check_continuity.py` inclus) ne compare les deux tables de cotes : elle est structurellement invisible des contrôles.

**Correctif suggéré.** L'Avis qui mariera les rédactions devra trancher cote par cote ; à défaut, namespaces distincts (ex. `A-34 (Bât.)` / `A-34 (Sil.)`) tant que les deux volumes cohabitent.

---

### C. Chroniques (hors canon — défauts de contenu)

#### 🟠 F-03 · La généalogie castorale de la 2ᵉ rédaction contredit le Livre I

- `chroniques/LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` l. 241 (1896) : « Le vieux témoin adjoint — **fils du signataire de 1847, petit-fils de l'ami du béret** — monta sur l'ouvrage… »
- `chroniques/LIVRE_I_LES_FONDATIONS.md` l. 381 : « le vieux castor de la grande digue — **l'ami du béret, le signataire d'octobre**… ne sortirait plus » (mort au printemps 1859).

Le Livre I identifie formellement le signataire de 1847 **et** l'ami du béret (un seul castor, mort en 1859). La 2ᵉ rédaction fait du signataire de 1847 le **fils** de l'ami du béret (deux castors distincts). Les deux volumes ne peuvent pas avoir raison. Correctif minimal : « petit-fils du signataire de 1847 (l'ami du béret) » — un mot.

#### 🟠 F-04 · « Cinquante ans d'ingénieur » (2ᵉ rédaction, tranche 7 §7)

`LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` l. 473 : « Il avait quatre-vingt-deux ans, **dont cinquante d'ingénieur** et vingt-deux de roi ». 82 ✓ (1832→1914) et 22 ✓, mais « 50 d'ingénieur » place le début de carrière en 1864 — date que rien ne fixe : l'école des castors est en 1853–1855 (diplôme ~1855, red. 1), les deux sillons en 1860, les plans officiels en 1882 (« prince et ingénieur »). Compté depuis 1882, ce sont 32 ans. L'audit d'arithmétique de la 2ᵉ rédaction (« 18 calculs, 0 erreur », annexe B) ne couvre pas ce chiffre.

#### 🟠 F-05 · « Le premier chantier du Royaume depuis 1914 » (Livre IV, tranche 5 §3)

`LIVRE_IV_LERE_BALNEAIRE.md` l. 491 (chantier de McBabber's, 1985) — contredit par le creusement de la piscine (1958–1962) racontée dans le même volume : croquis de décembre 1958 sur la dernière page de **C-19**, délibération du 3 juillet 1962, « procès-verbal de creusement (1962) » (annexe du même livre). La formule correcte est « depuis 1962 ».

#### 🟡 F-06 · « Vrai pendant neuf ans encore » — la reine Colette (Livre IV, tranche 7 §4)

`LIVRE_IV_LERE_BALNEAIRE.md` l. 713 : au retrait de mars 1998, Colette « s'en occuperait jusqu'au bout, ce qui fut vrai pendant **neuf ans encore** ». L'unique « bout » du corpus est sa mort, **2011** (canon) : 1998 → 2011 = **13 ans**, pas 9 (2007 n'est qu'une année sans événement marquant pour elle).

#### 🟡 F-07 · L'énumération des « quatre fils » ne tient pas (Livre IV, épilogue)

`LIVRE_IV_LERE_BALNEAIRE.md` l. 707 : « **quatre fils**, dont l'un régnait déjà, dont un autre refuserait de régner, et dont le dernier, né l'après-midi des montagnes, garderait le fleuve ». Les quatre fils sont les jumeaux, le Louche et Rambo. « L'un régnait déjà » = les jumeaux (1998) ✓ ; « refuserait de régner » **et** « le dernier… garderait le fleuve » désignent tous deux Rambo (2026-G : « Rambo ayant refusé le trône » ; Prince du Fleuve). Rambo est compté deux fois et le Louche (régnant depuis 2010) manque à l'énumération.

#### 🟡 F-08 · « Cinq tombes, quatre générations » (Livre III, tranche 7 §4)

`LIVRE_III_LAGE_HORIZONTAL.md` l. 741 : « auprès de Babber, Babette, François, Babette-Marine et Hortense — **cinq tombes, quatre générations** ». Les cinq tombes citées couvrent **deux** générations (I : Babber, Babette ; II : François, Babette-Marine, Hortense) ; y ajoutant le Dormeur lui-même, le chêne comptait **trois** générations. « Quatre » ne fonctionne sous aucune lecture.

#### 🟡 F-09 · Comptage des témoins « depuis 1892 » (1ʳᵉ rédaction)

`LIVRE_II_LES_BATISSEURS.md` l. 823 (1913) : « le témoin adjoint, qui était **le quatrième depuis 1892** » ; l. 876 (table 1914) : « Les témoins royaux adjoints **depuis 1892 | 4** » ; l. 916 : « le quatrième témoin depuis 1892 ». Or la succession racontée depuis 1892 est : témoin de 1889 (mort à l'automne 1893, l. 417) → témoin de 1893 (l. 155) → témoin de 1913 = **trois** relais, pas quatre. Le « 4 » est correct comme numéro d'ordre **global** (le premier témoin étant mort en 1859), mais le libellé « depuis 1892 » mélange les deux comptages. Le Livre III réutilise le même libellé lâche (« le cinquième depuis 1892 » en 1919, « le sixième » en 1945, « le septième » en 1959 — numéros globaux #5/#6/#7), ce qui reste lisible, mais la table de 1914 ne l'est pas.

#### 🟡 F-10 · « 18 barges au Jour de l'Eau » non étayé (2ᵉ rédaction)

`LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` l. 570 (annexe B, audit n° 13) : « 12 barges à l'hiver 1889–1890, **18 au Jour de l'Eau (proposé)** ». Rien dans la 2ᵉ rédaction ne narre une extension de la flottille, et le chiffre entre en conflit avec la 1ʳᵉ rédaction (12 actives jusqu'en 1910, +4 = 16, l. 477 ; « les seize barges » en 1914, l. 916 ; Livre III 1916 : « Les seize barges de la flottille »). Le « (proposé) » atténue, mais c'est le seul chiffre de l'audit « 0 erreur » qui ne repose sur aucun récit.

#### 🟡 F-11 · « 16 barges, dont trois sous l'eau » (1ʳᵉ rédaction, table 1914)

`LIVRE_II_LES_BATISSEURS.md` l. 876 : « Les barges de la flottille | **16**, dont trois sous l'eau pour toujours ». Le texte distingue nettement (l. 477) les barges **actives** (12 jusqu'en 1910, puis 16) des **trois coulées** (1897–1899, « le registre tint les morts à leur place »). « 16, dont trois » confond les deux populations : au plus 16 actives + 3 coulées = 19 au total ; les « seize barges » qui sonnent leurs cloches en 1914 (l. 916) confirment que les 16 sont les actives.

#### 🟡 F-12 · « Dix-huit mois » pour le coussin de la Lecture (Livre III, tranche 3 §3)

`LIVRE_III_LAGE_HORIZONTAL.md` l. 362 : « La reine mit **dix-huit mois** et trois essais à le convaincre » — mais le journal de la malterie cité aussitôt donne : **mai 1927** (premier essai), **novembre 1927** (deuxième), **mars 1928** (troisième, « il reste ») : ≈ 10–12 mois, pas 18.

#### ⚪ F-13 · « Cent soixante-seize ans de délibération » (Livre I, tranche 4 §3)

`LIVRE_I_LES_FONDATIONS.md` l. 327, section « **1849** · La commission monétaire » : le billet arrive en 2023. 2023−1847 = 176 ✓ (compté depuis la fondation), mais la *délibération* de la section commence avec la commission de **1849** : 2023−1849 = 174. RA-2026-II (§2.3) avait validé le calcul 1847→2023 ; l'ambiguïté n'est pas levée dans le texte.

#### 🟡 F-14 · Divergences entre les deux rédactions du Livre II au-delà du nombre de bancs

Le README ne déclare que « quarante contre quarante-deux » bancs. Les deux rédactions divergent aussi sur :

| Point | 1ʳᵉ rédaction | 2ᵉ rédaction |
|---|---|---|
| Premier coup de pelle | un lundi de mai **1892**, 9 h | « le premier jeudi sans gel de **1893** » (chantier « ouvert onze ans ») |
| Mort de François-Babber | « à l'automne, avant le premier gel » (1914) | « au premier chaud de **mai 1914**, sur le banc nº 22, au matin » |
| Nom d'« l'Aqueducien » | adopté **1892** (assemblée, « si l'eau arrive ») | reçu par acclamation le **12 octobre 1904** |
| Mise en eau | eau pure **printemps 1899** (4 jours) ; bière **mai 1905** | les deux canaux le **12 octobre 1904** (1 h 20, 25 m/min) |
| Palais | extension de la Chancellerie (maison louée **1890**), nommé **1904** | la Remise aux Plans (**1892**), nommé **1902** |
| Flottille | 12 → 16 (1910) | 12 → « 18 (proposé) » en 1904 |
| Cuvée du Canal | — (absente) | brassée **1890**, ouverte 1904, « quatorze ans de garde » |

Ces divergences sont *acceptées* en principe (deux rédactions proposées, « l'Avis choisira ou mariera ») mais doivent être **énumérées intégralement** dans cet Avis — la liste ci-dessus est celle que l'audit a relevée.

---

### D. Atlas géographique (proposé, non décrété)

#### 🟡 F-15 · La Banque nationale « depuis 1892 » — et « jamais décrite »

`sources/geographie.py` l. 212–214 : gazetteer « Banque nationale, **depuis: 1892** » + note « Cité au Livre I, **jamais décrite** (lacune R2.1) ». Les deux affirmations sont fausses au regard des chroniques : la fondation est fixée à **1897** (« C'est de cette paye que naquit, **en 1897**, la Banque nationale », red. 1 ; Livre III 1919 : « une Banque nationale qui gardait du fromage **depuis 1897** » ; 1897+126 = 2023 ✓), et la banque est décrite dans la 1ʳᵉ rédaction (maison de pierre à deux portes, « BANQUE NATIONALE · RÉSERVE ET PARITÉ »).

#### 🟠 F-16 · L'aqueduc « en service en 1914 », « chantier 1892–1914 »

`sources/generate_map.py` l. 206–207 (couches : plans 1882 → chantier 1892–**1914** → trait plein **depuis 1914**) ; `sources/geographie.py` l. 224 (« chantier 1892–1914 ») et l. 417 (époque « **1914** · Aqueduc en service — Les deux canaux coulent »). Les deux rédactions du Livre II contredisent cette datation : red. 1 = chantier 1892–1898, eau **1899**, bière **1905** ; red. 2 = chantier 1893–**1904** (11 ans de creusage), les deux canaux le **12 octobre 1904**. Le « 1914 » correspond à la mort de l'Aqueducien, pas à la mise en service. L'ambiguïté d'origine est la ligne de la chronologie « 1892–1914 · Mise en service et consolidation du Double Aqueduc » (synthèse du règne, non une date de service). `check_geography.py` ne contrôle pas cette date.

#### 🟡 F-17 · Le phare « depuis 1916 »

`sources/geographie.py` l. 250–253 : « Phare blanc couronné, **depuis: 1916** » (« Érigé par Babette-Marine ; elle le laisse à sa mort en 1916 »). 1916 est la **première mise à feu** (Livre III) et la mort de Babette-Marine ; la 1ʳᵉ rédaction fixe la tour en **1905** (« la tour du phare figure au registre de 1905 parce qu'on y monte ») et la lanterne en **1912**. L'atlas fait exister l'ouvrage à partir de sa mise à feu.

---

### E. Documentation & outillage

#### 🟡 F-18 · README : « les quatorze illustrations du dossier iconographique »

`README.md` l. 54 (points de continuité) — alors que la même page annonce l. 9 « **24** illustrations après la campagne 2026-II » et que le dossier du Livre V de 2026-I est bien de 24 planches. Nombre obsolète (pré-2026-II).

#### 🟡 F-19 · README : commandes cassées « python .venv/bin/python … » (× 3)

`README.md` l. 71 (« `make pdf` # équivalent de : **python .venv/bin/python** sources/generate_encyclopedie_2026_i.py »), l. 86–88 (validation de la continuité) et l. 118 (« `make arbre` # équivalent de : **python .venv/bin/python** … »). Le `python` initial en trop rend la commande fausse (on tenterait d'exécuter l'interpréteur du venv comme script). Il faut `.venv/bin/python sources/…`.

#### ⚪ F-20 · README : « `make controle` — les trois contrôles » (l. 63)

Il y en a **quatre** : `check_continuity.py`, `check_pdf.py`, `pdf_fingerprint.py --check`, `check_geography.py`.

#### ⚪ F-21 · `INVENTAIRE_ICONOGRAPHIQUE.md` anachronique

Daté « 27 août 2026 · Campagne 2026-II », il consigne pourtant les quatre planches des chroniques « **ajoutées le 28 août 2026** ». Le document décrit un état postérieur à sa date (probablement mis à jour sans re-dater).

#### ⚪ F-22 · Iconographie : lettrages — 5 défauts déclarés confirmés, 6 défauts non listés découverts

Inspection visuelle des fichiers (seconde passe). Les cinq défauts que l'`INVENTAIRE_ICONOGRAPHIQUE.md` (§ IV) déclare « non bloquants » sont **tous bien présents** :

| Réf. | Image | Défaut déclaré | Statut visuel |
|---|---|---|---|
| I-01 | `mcbabbers_enseigne_royale.png` | « McBABBBER'S » (un B de trop) | ✅ confirmé — l'enseigne lit bien « McBABBBER'S » |
| I-03 | `mcbabbers_menu_pabst.png` | légendes « Pabstus Rex », « raevas » | ✅ confirmé — « PABSTUS REX » × 3, « juicy beef & raevas » |
| I-05 | `roger_bontemps.png` | cartouche « GRANO BOUFFON » | ✅ confirmé — « ROYAL JESTER & GRANO BOUFFON OF BABBBERLAND » |
| I-06 | `pieces_monnaie_babberland_coffret.png` | légende « ESHFTY » (1 Babber) | ✅ confirmé — légende corrompue sur la pièce de 1 Babber |
| I-11 | `babbersgate_scandale_sauce.png` | cadre médiéval, billet américain, Louche couronné | ✅ confirmé — salle médiévale pour un événement de 1991, billets en dollars, couronne sur le Louche (prince en 1991) |

Mais l'inspection révèle des **lettrages corrompus non listés** par l'inventaire, alors même que sa consigne de campagne est « **aucun lettrage dans l'image** » :

- « **Pabt** » sur les deux canettes (planche I-01) ;
- « **BABBERLAND** » (un B de trop) sur les légendes des quatre pièces et « **ROI BABBBER** » (I-06) ;
- « **Régent de Babberie** » et « **wipie syrup de mapie** » (I-03) ;
- « **SECRET ACCOUNT BOOK** » et une note manuscrite en anglais (I-11) ;
- « **OFFICIAL COLLECTOR PROOF SET** » en anglais (I-06).

Tout comme les cinq déclarés, ces lettrages concernent des planches « proposées, non décrétées » : **non bloquant**, mais l'inventaire § IV est **incomplet** (il ne recense que 5 défauts de lettrage sur 11 observés).

**Correctif suggéré.** Prolonger l'inventaire des lettrages non listés (10 min) ; la régénération sans lettrage reste possible — la consigne est déjà écrite.

#### ⚪ F-23 · `ROADMAP_2026_II.md` : l'indicateur « Contrôles en CI » décrit un état qui n'existe pas

La table « Indicateurs après Horizon 0 » affiche « Contrôles en CI : **0 → 5 + scellé d'archives** » comme acquis. Or, dans le même document, R0.4 est **« Bloqué par un droit »** (E-17 : le jeton d'application n'avait pas la permission `workflows`) — et l'unique workflow commité est invalide (F-01) : **aucun contrôle CI n'a jamais tourné**. L'indicateur décrit l'état cible, pas l'état atteint ; reléguer la valeur « 5 + scellé » en colonne « cible » évitera de le lire comme un fait accompli.

---

## 3. Dossiers ouverts antérieurs (déjà signalés, toujours en attente)

Constatés par RA-2026-II, classés « en attente d'arbitrage » — l'audit confirme qu'ils sont **toujours présents** dans l'état examiné :

| Réf. | Point | État |
|---|---|---|
| E-16.a | Le symbole `B$` n'apparaît qu'une fois (« 1 B$ (Caisse) ») ; aucun tableau de symboles monétaires | Ouvert |
| E-16.b | Chronologie § V « Union des Règnes (**1998–2009**) » vs tableau IX « **1998–2010** · 12 ans » | Ouvert |
| E-16.d | Le béret : « promesse de **trente** ans » (Livre I, tranche 1) puis « **trente et un** ans plus tôt » (tranche 3) — l'intervalle 1816→1847 vaut 31 | Ouvert |
| E-16.e | « inscrit dans le premier registre **cinquante ans plus tard** » (Livre I, tranche 1) — 1798→1847 = 49 | Ouvert |
| E-14.2 | Le tag `v2026-I` posé sur le parent de fusion (commit de branche) plutôt que sur `main` — « à faire hors dépôt » ; non vérifiable depuis ce clone (depth 1) | Ouvert |
| E-15 | L'arbre est encodé deux fois (script PNG + SVG vectoriel main) sans contrôle de parité — horizon 1 (R1.7) | Ouvert |

À noter également : les en-têtes de sections de la chronologie (« II. … (1847–1891) », « III. … (1892–1958) », « IV. … (1959–1997) », « VI. … (2010–2025) ») suivent une convention de découpe cohérente (chaque section s'arrête l'année qui précède la première date de la suivante) — ce n'est pas une erreur, mais les bornes des titres peuvent induire (dernier événement de la section II : 1889 ; de la section IV : 1991–93).

---

## 4. Vérifié et trouvé conforme (inventaire explicite)

Pour que le lecteur ne relise pas ces points, ils ont été examinés et **tenus pour sains** :

- **Canon 2026-I** : aucun défaut interne. Règnes 42 / 3 / 22 / 45 / 39 / 12 ans + Louche « en cours » (tableau IX) ; 47 dégustations = 1 + 46 ; 6 999 = 7 000 − 1 ; 316/317 pots ; 1 Babber = 24 Babetons, 12 = demi-Babber, 6 = six-pack, 1 = canette ; 126 ans de Banque (1897→2023) ; 58 ans de hamac (1856→1914) ; 31 ans de béret (1816+31 = 1847) ; 42 jours d'hommage = 42 ans de règne de l'Ancien ; 69 lectures = 68 annuelles + 1 extraordinaire ; 214 humains (1850) constants ; 7 000 = 3 500 + 1 200 + 800 + 1 500 + 0 ; Monts Froissés 1,20 m / 4 secondes / 15 juillet 1962 ; filiation directe et collatérale, « VII » = génération, ordinaux, succession (Fou 1ᵉʳ, Ti-Babber 2ᵉ) ; les dix contrôles de continuité (chronologie § X) respectés dans **tous** les documents, y compris les deux chroniques de 2026-II.
- **Jours de semaine** : 12 octobre 1847 = **mardi** ✓ (Livre I, tranche 3) ; 12 octobre 1904 = **mercredi** ✓ (2ᵉ rédaction, tranche 5) ; « un vendredi soir de juillet 2004 » (Pabstgate) : juillet 2004 a bien des vendredis, aucune date précise avancée ✓.
- **Âges des chroniques** : tous les âges cités dans les quatre volumes (Livre I : François 15/28/57/60/82, Babette 26/88, Babette-Marine 16/33/56/78, Hortense 7/23/65/74, le Dormeur 14/17/26/33/39, Irène 25/30/32 ; Livre II red. 1 et red. 2 : annexe B recalculée en 18 items ; Livre III : jumeaux 26/18/63 (1938), 34/26/71 (1946), 80/41/16/9/3/73 (1955), 84 (1959), 47 (1959), 11 (1997) ; Livre IV : 50 (1962), 42 (1962), 4 (1966), 84/52 (1966), 22 (1968), 26/32 (1978), 71 (1991), 84/86 (1996–98), 74 (1986), 90 (2002)) sont justes — hors les F-04, F-06, F-08, F-12 ci-dessus.
- **Archive 2026-G (PDF, 41 pages)** : périmètre conforme à son état antérieur ; contient bien la visite « du Colonel Kadhafi (12 mai 1980) » (item 15 + chronologie interne) — la chronique Livre IV qui s'y appuie est donc **vérifiée** ; « Rambo du Fjord est le frère cadet du Roi, non son fils » ✓ ; « 1 B$ = 24 Babetons » ✓. Seconde passe : items généalogiques revus un à un — Rambo #7 « Prince du Fleuve, quatrième fils de Babber II, frère cadet du Roi, né le 15 juillet 1962 — le jour où l'on creusa les Monts Froissés. Ce n'est ni un ancêtre, ni un mercenaire » ✓ ; Babber le Fou #8 « héritier, fils unique de Sa Majesté et de la reine Linéa, né le 1er avril 1986 » ✓ ; la « Signature de la Nappe Sacrée (1847) » ✓ ; le « double ordinal Ier » (Article 5) cohérent avec la succession du Louche ✓.
- **Les cinq Lois fondamentales** (canon « Lois fondamentales ») correspondent **article par article** aux « Lois fondamentales » de l'archive scellée 2026-G : 1 Droit au hamac · 2 **Obligation thermique de la Pabst** (l'Article 2 existe bel et bien, identique dans les deux documents : G ajoute l'amende de deux poutines et la Police royale de la Fraîcheur au thermomètre laser, I ajoute la clause mineurs/conducteurs — variantes compatibles) · 3 Écoute contemplative des érables · 4 Sacralité de la sieste 13 h–15 h · 5 Infaillibilité souveraine. Le Livre III (1955) : « cinq articles dont deux portaient la signature d'un règne couché » = articles 1 et 4 ✓. Aucun article de la Constitution n'est absent du corpus.
- **Archive 2026-H** : conforme à 2026-I (les 95 % de duplication sont assumés ; le scellé protège).
- **Scellés** : `sha256sum --check gouvernance/ARCHIVE.sha256` → G et H **OK** ; empreinte sémantique du PDF publié `a129fa3f…` conforme (29 pages, 24 images).
- **Chaîne de production** : `make controle` → 4/4 verts ; `make tout` → arbre régénéré **identique au bit près**, atlas (SVG/PNG/HTML) **identique**, empreinte **identique** ; le seul écart est le PDF (± 4 octets = horodatage, écart E-10 documenté, absorbé par le contrat d'empreinte).
- **Iconographie** : 28 PNG = 14 d'origine + 10 portraits 2026-II + 4 planches des chroniques ; 24 servies dans le PDF = 23 ancres `IMAGE_AFTER` + l'arbre généalogique (couverture + bloc du Livre V) ; aucune image orpheline, aucune référence cassée ; les 4 planches `aqueduc_*.png` sont référencées uniquement par la 2ᵉ rédaction (Annexe C) et l'inventaire — « hors volume par statut », cohérent.
- **Le « 23 légendes » de `check_pdf.py`** n'est pas un manquant : la 24ᵉ image (l'arbre) porte sa légende propre (« Arbre généalogique officiel consolidé. ») insérée dans le bloc généalogique, hors de la table des 23 ancres.
- **`make propre`** ne supprime que `sources/__pycache__` (pas d'artefact canonique en jeu).

---

## 5. Plan de remédiation recommandé

| Pri. | Action | Concerne | Effort |
|---|---|---|---|
| **P1** | Remplacer/supprimer `.github/workflows/main.yml`, installer `continuite.yml` (`make workflows` + commit), vérifier une exécution verte | F-01 | 1 commit, ~5 min |
| **P2** | Avis n° 7 sur le Livre II : trancher la liste complète des divergences (F-14) **et** les cotes en collision (F-02) | F-02, F-14 | décision éditoriale |
| **P2** | Corriger la généalogie castorale de la 2ᵉ rédaction (« petit-fils du signataire de 1847 (l'ami du béret) ») | F-03 | 1 phrase |
| **P3** | Corrections arithmétiques/logiques des chroniques : F-04 (50 ans d'ingénieur), F-05 (« depuis 1962 »), F-06 (13 ans), F-07 (énumération), F-08 (deux/trois générations), F-09 (comptage des témoins), F-10 (18 barges), F-11 (« 16 actives + 3 coulées »), F-12 (12 mois) | F-04 à F-12 | 1 mot à 1 phrase chacun |
| **P3** | Atlas : Banque 1897 + note corrigée (F-15) ; couches aqueduc alignées sur la rédaction retenue (F-16) ; phare 1905/1912/1916 distingués (F-17) | F-15 à F-17 | quelques lignes dans `geographie.py` + `generate_map.py`, puis `make carte` |
| **P4** | README : « vingt-quatre » (F-18), commandes `.venv/bin/python` (F-19), « quatre contrôles » (F-20) ; re-dater l'inventaire (F-21) | F-18 à F-21 | 10 minutes |
| **P4** | Iconographie : prolonger l'inventaire des lettrages non listés (F-22) ; `ROADMAP_2026_II.md` : passer l'indicateur « Contrôles en CI » en cible (F-23) | F-22, F-23 | 15 minutes |
| **P4** | Trancher les E-16.a/b/d/e ouverts (4 arbitrages d'une ligne chacun) | §3 | décision éditoriale |

### 5bis. Corrections appliquées (28 août 2026)

À la demande du porteur du dépôt, les correctifs ci-dessous ont été **exécutés** le 28 août 2026 sur la branche `arena/01a049ea-babbersland`, puis validés par `make tout` (4/4 contrôles verts, nouvelle empreinte sémantique `89f33845847d92ca645004f3157e845b` gravée dans `gouvernance/pdf_fingerprint.txt`, scellés des archives G/H intacts) :

| Constat | Correction apportée |
|---|---|
| **F-01** | `.github/workflows/main.yml` (URL de 25 octets) **supprimé** ; `continuite.yml` **installé** (`make workflows`) et validé (YAML parsable). Poussée refusée par le remote le 28/08 : l'App Arena n'a pas la permission `workflows` (**E-17 confirmé en situation**) — le correctif demeure en arborescence, prêt à pousser dès que le scope sera accordé (procédure déjà documentée dans le Makefile : « à committer avec un jeton tenant workflows ») |
| **F-03** | 2ᵉ rédaction l. 241 : « petit-fils du signataire de 1847 (l'ami du béret) » |
| **F-04** | 2ᵉ rédaction l. 473 : « trente-deux d'ingénieur » (1882→1914) |
| **F-05** | Livre IV l. 491 : « premier chantier du Royaume depuis **1962** » |
| **F-06** | Livre IV l. 713 : « **treize** ans encore » (1998→2011) |
| **F-07** | Livre IV l. 707 : « quatre fils, dont **trois tenaient le trône — les jumeaux d'abord, le Louche ensuite —**, et dont le dernier… refuserait de régner et garderait le fleuve » |
| **F-08** | Livre III l. 741 : « cinq tombes, **trois** générations » |
| **F-09** | 1ʳᵉ rédaction × 3 (l. 823, 876, 916) : « depuis **1847** » (premier témoin = le signataire de 1847, mort en 1859) |
| **F-10** | 2ᵉ rédaction l. 570 : « **12** au Jour de l'Eau » (aucune extension n'est narree avant 1910) |
| **F-11** | 1ʳᵉ rédaction l. 877 : « **16** actives (les trois coulées comptées à part, sous l'eau pour toujours) » |
| **F-12** | Livre III l. 362 : « **dix** mois et trois essais » (mai 1927 → mars 1928) |
| **F-13** | Livre I l. 327 : « **cent soixante-quatorze** ans de délibération » (commission de 1849) |
| **F-15** | `geographie.py` : Banque « depuis: **1897** », note corrigée (« citée aux chroniques, décrite en maison de pierre à deux portes ») |
| **F-16** | `geographie.py` + `generate_map.py` : époque 1914 renommée « **Consolidation** de l'aqueduc » ; note « chantier 1892/1893–1904/1905 (selon rédaction), mise en eau 1899–1905 » ; trait plein de la carte à partir de **1905** (service effectif commun aux deux rédactions) — le choix de rédaction reste à l'Avis n° 7 |
| **F-17** | `geographie.py` : phare « depuis: **1905** » (tour), note « lanterne 1912, mise à feu 1916 » |
| **F-18** | README : « les **vingt-quatre** illustrations » |
| **F-19** | README × 4 : « **.venv/bin/python** sources/… » (plus de `python` initial) |
| **F-20** | README : « les **quatre** contrôles » |
| **F-21** | Inventaire re-daté « **28** août 2026 » avec note de re-dation |
| **F-22** | Inventaire § IV : lettrages non listés consignés sous les ids **I-12 → I-16** |
| **F-23** | `ROADMAP_2026_II.md` : indicateur « Contrôles en CI » qualifié **cible — non atteint** (E-17) |
| **E-16.a** | Canon, Livre VI « Système monétaire » : notation **B$** (Babber-dollar) définie |
| **E-16.b** | Chronologie § V : « Union des Règnes (**1998–2010**) » |
| **E-16.d** | Livre I l. 57 : « promesse de **trente et un** ans » (1816→1847) |
| **E-16.e** | Livre I l. 31 : « **quarante-neuf** ans plus tard » (1798→1847) |

**Reste ouvert** (arbitrage éditorial, hors portée d'une correction mécanique) : **F-02** et **F-14** (l'Avis n° 7 mariera les deux rédactions du Livre II — cotes et divergences), **E-14.2** (tag `v2026-I` : à poser hors dépôt, sur le remote), **E-15** (source unique de l'arbre, ticket R1.7).

---

## 6. Conclusion

Le Royaume du Babberland tient, sur le plan canonique, un niveau de tenue remarquable : sept générations, sept règnes, un système monétaire et deux archives réconciliées **sans contradiction interne détectée**, des générateurs déterministes et des contrôles qui font ce qu'ils promettent. Les défauts réels de l'état examiné se concentraient **hors du canon** (état exécuté du 28 août 2026 en § 5bis — il ne reste ouvert que l'Avis n° 7, le tag hors dépôt et le ticket R1.7) :

1. **un workflow CI commité qui est une URL** (F-01) — le seul défaut « bloquant », car il désactive l'ensemble des garde-fous automatiques que le dépôt s'est donné la peine de construire ;
2. **un espace de cotes d'archives contradictoire** entre les deux rédactions du Livre II (F-02), à trancher avec les divergences déclarées ;
3. **une contradiction inter-volumes** sur la lignée des castors (F-03) et **neuf coquilles** arithmétiques ou logiques dans les chroniques (F-04 à F-12, F-13) — toutes dans du texte « proposé, non décrété », donc sans risque canonique, mais à corriger avant tout décret d'incorporation ;
4. **trois datations d'atlas** (F-15 à F-17) qui s'écartent des chroniques ;
5. **cinq obsolétesses de documentation** (F-18 à F-21, F-23) et des **lettrages corrompus** sur les planches iconographiques, 5 déclarés et 6 non listés (F-22) — tous dans du « proposé, non décrété ».

> *« Une Pabst, une poutine, un workflow, et on corrige l'URL. »*
> — Note de l'auditeur, versée aux Archives

---

*Rapport établi le 28 août 2026 · Auditeur : agent Arena.ai · Toutes les commandes citées sont reproductibles via `make controle` / `make tout` dans le venv épinglé (`make env`).*
