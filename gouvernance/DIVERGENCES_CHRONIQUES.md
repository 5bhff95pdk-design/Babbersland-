# ⚖️ REGISTRE DES DIVERGENCES DES CHRONIQUES

**Chancellerie royale · Pabst City** — établi le 29 août 2026, à la suite du rapatriement de
l'audit `RAPPORT_AUDIT_2026_III.md` (constats **F-02** et **F-03**, restés dans une pull request en
conflit) et de la revue du corpus du 29 août 2026. **Révisé le 30 août 2026** : l'édition fusionnée
unique du Livre II (quarante-deux bancs retenus, `LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` intégré puis
supprimé) a modifié le champ d'observation — dix déclarations devenues inexactes ont été relues,
les sept collisions intra-fusion levées, les deux collisions encore observées (G-1, P-3) tenues,
et l'arithmétique des bancs re-constatée sur le corpus fusionné.

---

## I · La règle

Les Chroniques sont **proposées, non décrétées**. Elles peuvent taire ; elles ne peuvent pas se
contredire entre elles ni contredire 2026-I sans que la contradiction soit **écrite quelque part**.

Même contrat que `propositions_declarées` (E-19) : une divergence est **résolue** ou **déclarée**.
`check_chroniques.py` relève trois choses :

| Objet | Ce qui est vérifié |
|---|---|
| **Grandeurs chiffrées** | bancs, canaux, arches, villes, régions, kilomètres, population — un même objet compté différemment d'un volume à l'autre |
| **Cotes d'archives** | la même cote (`Q-3`, `A-34`…) désignant deux documents différents dans deux volumes |
| **Déclarations** | une déclaration qui ne correspond plus à aucune divergence observée est une **faute** : le registre n'accrédite pas des conflits disparus |

Le bloc `json` ci-dessous est la source que lit le contrôle. Le reste du document l'explique.

---

## II · Les divergences déclarées

### 1. Les bancs du Double Aqueduc — la divergence 40/42 est résolue ; l'arithmétique reste constatée

| Valeur observée par le contrôle | Où | Ce que c'est |
|---|---|---|
| **42** | Livre II (édition fusionnée), Livre III, Livre IV | les bancs officiels de l'aqueduc — « un par année de règne du fondateur » |
| **3** | Livre IV et canon | *les trois bancs publics* financés par l'amende du tribunal — homonyme, un autre objet |
| **82** | Livre II, Note de consolidation (l. 11) | **artefact de lecture, pas un troisième comptage** : la note dit « choisir entre *quarante et quarante-deux bancs* » ; le contrôle lit l'énumération française comme un composé numéral et somme 40 + 42 |

La divergence 40/42 elle-même a été **résolue par la fusion du 30 août 2026** : l'édition unique
retient **quarante-deux** (« Il n'existe plus de version concurrente à consulter »), et les Livres
III et IV disent quarante-deux. Une divergence résolue ne se déclare plus — mais le contrôle
continue d'observer les valeurs 3, 42 et 82 au-dessus du seuil de divergence, et ce bloc en tient
lieu écrit : la 82 y est consignée comme artefact, afin que personne ne « corrige » une note qui
ne dit rien de faux, et que la lecture de la machine reste contrôlable. Les bancs d'essai (47 posés
à l'été 1892, « pas les bancs de l'ouvrage ») et le banc supplémentaire non numéroté, dit *le banc
de la cave*, ne comptent pas : le contrôle exclut explicitement les bancs d'essai, et le banc de la
cave n'est cité qu'avec l'article (« un banc »), jamais dénombré.

### 2. La population — une courbe qui n'est consignée nulle part

| Valeur | Où | Époque et portée |
|---|---|---|
| 11 | Livre I | la cérémonie de 1847 |
| 214 | Livres II, III, IV | recensement de 1850, « que personne n'avait eu le courage de corriger » — encore officiel en 1959 |
| 5 | Livre V | une délégation, en 2004 |
| 800 / 1 200 / 3 500 | **2026-I** | Port Babette, Grass City, Pabst City |
| 7 000 | Livre VI | le Royaume entier, en 2026 |

**Constats attachés** :

1. la **courbe démographique n'existe pas** — rien ne relie 214 (1850) à 7 000 (2026) ;
2. le **total national de 7 000 âmes ne figure pas dans 2026-I**, qui ne donne que trois villes
   (5 500 âmes urbaines). Le chiffre le plus cité du Royaume — il est dans le résumé exécutif et
   dans l'atlas — repose sur une chronique proposée, non décrétée.

À consigner par l'Avis royal n° 7, ou à déclarer perpétuellement non consigné.

### 3. Les cotes d'archives en collision (F-02, révisé au 30 août 2026)

L'état du 29 août déclarait **huit cotes** : six collisions entre les deux rédactions du Livre II
(**A-41, A-44, M-1, P-1, Q-2, Q-3**), une collision inter-volumes que F-02 n'avait pas relevée
(**G-1**, Livre III contre Livre IV), et une variante jugée complémentaire plutôt que
contradictoire (**L-13** : le même avènement de 1892, deux registres).

La fusion du 30 août a **levé par décision éditoriale** les sept cotes intra-fusion : l'annexe du
Livre II unique porte désormais une entrée par cote, et la déclaration des conflits disparus serait
elle-même une faute (règle du § I). Il reste **deux collisions observées** :

| Cote | Où | Ce que c'est |
|---|---|---|
| **G-1** | Livre III l. 798 — Premier registre de Grass City (1920) · Livre IV l. 729 — feuille de chanvre de Linéa (1974) | collision inter-volumes, non relevée par F-02 |
| **P-3** | Livre II l. 1194 — Registre de la Remise aux Plans, futur Palais royal (1892) · Livre III l. 797 — Registre du phare : « Allumé. Personne à prévenir. » (1916) | **née de la fusion** : l'annexe de l'édition fusionnée a hérité du P-3 de la rédaction *Le Silence et l'Aqueduc*, alors que le Livre III donne déjà P-3 au phare. Les deux documents sont complémentaires, la collision est formelle |

Remède, quand l'Avis n° 7 parlera : trancher cote par cote, ou attribuer des namespaces distincts
(`P-3 (Bât.)` / `P-3 (III)`), ou bien la Chancellerie déclare la collision sans effet — au choix,
mais écrit.

---

## III · Hors contrôle automatique

Une divergence est connue du registre sans être décelable par la machine :

**F-03 — la généalogie castorale.** `LIVRE_II_LES_BATISSEURS.md` l. 499 (1896, passage conservé par
la fusion) présente le vieux témoin adjoint comme « **fils du signataire de 1847, petit-fils de
l'ami du béret** », alors que `LIVRE_I_LES_FONDATIONS.md` l. 381 identifie formellement le
signataire de 1847 **et** l'ami du béret en un seul castor, mort au printemps 1859. Deux castors
contre un : les deux volumes ne peuvent pas avoir raison. Correction minimale proposée par
l'audit — un mot : *« petit-fils du signataire de 1847 (l'ami du béret) »*. Renvoyée à l'Avis n° 7 :
la Chancellerie ne corrige pas la prose d'une chronique par décret d'outillage.

---

## IV · Déclarations (source lue par `check_chroniques.py`)

```json
[
{"type":"chiffre","grandeur":"bancs","valeurs":[3,42,82],"documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_III_LAGE_HORIZONTAL.md","LIVRE_IV_LERE_BALNEAIRE.md","canon"],"motif":"40/42 résolu par la fusion (42 retenu) ; 3 = trois bancs publics (homonyme) ; 82 = artefact de la Note de consolidation, l'énumération « quarante et quarante-deux » somme 40+42 dans la lecture du contrôle — déclaré pour que la machine reste vérifiable","attend":"Avis royal n° 7 (harmonisation des cotes d'annexe, cote P-3)"},
{"type":"chiffre","grandeur":"population","valeurs":[5,11,214,800,1200,3500,7000],"documents":["LIVRE_III_LAGE_HORIZONTAL.md","LIVRE_II_LES_BATISSEURS.md","LIVRE_IV_LERE_BALNEAIRE.md","LIVRE_I_LES_FONDATIONS.md","LIVRE_VI_LE_SIECLE_QUI_LOUCHE.md","LIVRE_V_LUNION_DES_REGNES.md","canon"],"motif":"époques et échelles différentes : 11 (1847), 214 (recensement de 1850), 5 (délégation de 2004), 800/1200/3500 (villes du canon), 7000 (total de 2026, absent de 2026-I)","attend":"Avis royal n° 7"},
{"type":"cote","cote":"G-1","documents":["LIVRE_III_LAGE_HORIZONTAL.md","LIVRE_IV_LERE_BALNEAIRE.md"],"motif":"collision inter-volumes non relevée par F-02 : registre de Grass City (1920) contre feuille de chanvre de Linéa (1974)","attend":"Avis royal n° 7"},
{"type":"cote","cote":"P-3","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_III_LAGE_HORIZONTAL.md"],"motif":"née de la fusion du 30 août 2026 : registre de la Remise aux Plans (1892) contre registre du phare (1916) — documents complémentaires, collision formelle","attend":"Avis royal n° 7"}
]
```

Une divergence nouvelle qui n'apparaîtrait pas ici fait échouer `make controle`. Une ligne de ce bloc
qui ne décrit plus rien d'observable le fait échouer aussi.
