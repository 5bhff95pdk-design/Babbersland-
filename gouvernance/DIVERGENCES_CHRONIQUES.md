# ⚖️ REGISTRE DES DIVERGENCES DES CHRONIQUES

**Chancellerie royale · Pabst City** — établi le 29 août 2026, à la suite du rapatriement de
l'audit `RAPPORT_AUDIT_2026_III.md` (constats **F-02** et **F-03**, restés dans une pull request en
conflit) et de la revue du corpus du 29 août 2026.

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

### 1. Les bancs du Double Aqueduc — 40 contre 42

| Valeur | Où | Ce que c'est |
|---|---|---|
| **40** | Livre II réd. 1 (*Les Bâtisseurs*), Livre III, Livre IV | les bancs de l'aqueduc |
| **42** | Livre II réd. 2 (*Le Silence et l'Aqueduc*) | les bancs de l'aqueduc, « un par année de règne du fondateur » |
| **3** | 2026-I et Livre IV | *les trois bancs publics* financés par l'amende du tribunal — homonyme |
| **2** | Livre II réd. 1, l. 831 | *deux bancs* fabriqués par les écoliers — homonyme |

La vraie divergence est 40/42 : elle est connue (suivi R2.8 de la roadmap) et **attend l'Avis royal
n° 7**, qui choisira ou mariera les deux rédactions du Livre II. Les valeurs 2 et 3 ne comptent pas
le même objet : le registre les déclare pour que le contrôle ne les signale plus à chaque exécution.

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

### 3. Les cotes d'archives en collision (F-02)

Huit cotes portent la même référence dans deux volumes différents :

| Cote | Livre II réd. 1 | Livre II réd. 2 | Livre III | Livre IV |
|---|---|---|---|---|
| **A-41** | Expertise de la Grande Fuite (1901) | Reprise castorale de la digue (1893–1896) | | |
| **A-44** | Procès-verbal de la première audience horizontale (1910) | La Grande Pluie (1896) | | |
| **M-1** | Journal de la malterie | Journal de la Brasserie Haute (depuis 1896) | | |
| **P-1** | Premier registre du port (1893) | Marché de la Remise aux Plans (1892) | | |
| **Q-2** | Plan d'exécution du Double Aqueduc (1892) | Registres du chantier (1893–1904) | | |
| **Q-3** | Le plan des bancs, annexe (1893) | La première motte (objet sous verre) | | |
| **G-1** | | | Premier registre de Grass City (1920) | Feuille de chanvre de Linéa (1974) |
| **L-13** | Acte d'avènement et refus de l'ordinal (1892) | Procès-verbal d'avènement : les trois raisons (1892) | | |

Six vraies collisions de rédaction (**A-41, A-44, M-1, P-1, Q-2, Q-3**), une collision inter-volumes
que F-02 n'avait pas relevée (**G-1**, Livre III contre Livre IV), et une variante que la Chancellerie
juge complémentaire plutôt que contradictoire (**L-13** : le même avènement, deux registres).

Remède, quand l'Avis n° 7 parlera : trancher cote par cote, ou attribuer des namespaces distincts
(`Q-3 (Bât.)` / `Q-3 (Sil.)`) tant que les deux rédactions coexistent.

---

## III · Hors contrôle automatique

Une divergence est connue du registre sans être décelable par la machine :

**F-03 — la généalogie castorale.** `LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` l. 241 (1896) présente le
vieux témoin adjoint comme « **fils du signataire de 1847, petit-fils de l'ami du béret** », alors que
`LIVRE_I_LES_FONDATIONS.md` l. 381 identifie formellement le signataire de 1847 **et** l'ami du béret
en un seul castor, mort au printemps 1859. Deux castors contre un : les deux volumes ne peuvent pas
avoir raison. Correction minimale proposée par l'audit — un mot : *« petit-fils du signataire de 1847
(l'ami du béret) »*. Renvoyée à l'Avis n° 7 : la Chancellerie ne corrige pas la prose d'une chronique
par décret d'outillage.

---

## IV · Déclarations (source lue par `check_chroniques.py`)

```json
[
{"type":"chiffre","grandeur":"bancs","valeurs":[2,3,40,42],"documents":["LIVRE_III_LAGE_HORIZONTAL.md","LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md","LIVRE_IV_LERE_BALNEAIRE.md","canon"],"motif":"40 contre 42 entre les deux rédactions du Livre II (Avis n° 7) ; 2 et 3 sont des homonymes (bancs d'écoliers, bancs publics de l'amende)","attend":"Avis royal n° 7"},
{"type":"chiffre","grandeur":"population","valeurs":[5,11,214,800,1200,3500,7000],"documents":["LIVRE_III_LAGE_HORIZONTAL.md","LIVRE_II_LES_BATISSEURS.md","LIVRE_IV_LERE_BALNEAIRE.md","LIVRE_I_LES_FONDATIONS.md","LIVRE_VI_LE_SIECLE_QUI_LOUCHE.md","LIVRE_V_LUNION_DES_REGNES.md","canon"],"motif":"époques et échelles différentes : 11 (1847), 214 (recensement de 1850), 5 (délégation de 2004), 800/1200/3500 (villes du canon), 7000 (total de 2026, absent de 2026-I)","attend":"Avis royal n° 7"},
{"type":"cote","cote":"A-41","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"F-02 : Grande Fuite (1901) contre reprise de la digue (1893-1896)","attend":"Avis royal n° 7"},
{"type":"cote","cote":"A-44","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"F-02 : audience horizontale de 1910 contre la Grande Pluie de 1896","attend":"Avis royal n° 7"},
{"type":"cote","cote":"M-1","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"F-02 : journal de la malterie contre journal de la Brasserie Haute","attend":"Avis royal n° 7"},
{"type":"cote","cote":"P-1","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"F-02 : registre du port contre marché de la Remise aux Plans","attend":"Avis royal n° 7"},
{"type":"cote","cote":"Q-2","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"F-02 : plan d'exécution contre registres du chantier","attend":"Avis royal n° 7"},
{"type":"cote","cote":"Q-3","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"F-02 : plan des bancs contre la première motte","attend":"Avis royal n° 7"},
{"type":"cote","cote":"G-1","documents":["LIVRE_III_LAGE_HORIZONTAL.md","LIVRE_IV_LERE_BALNEAIRE.md"],"motif":"collision inter-volumes non relevée par F-02 : registre de Grass City (1920) contre feuille de chanvre de Linéa (1974)","attend":"Avis royal n° 7"},
{"type":"cote","cote":"L-13","documents":["LIVRE_II_LES_BATISSEURS.md","LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md"],"motif":"non-collision déclarée : le même avènement de 1892, deux registres et deux formulations complémentaires","attend":"Avis royal n° 7"}
]
```

Une divergence nouvelle qui n'apparaîtrait pas ici fait échouer `make controle`. Une ligne de ce bloc
qui ne décrit plus rien d'observable le fait échouer aussi.
