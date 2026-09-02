# 📊 RAPPORT D'ANALYSE DU PROJET — ROYAUME DU BABBERLAND

**Référence** : RA-2026-IV-01 · Analyse technique, éditoriale et de gouvernance
**Date d'examen** : 1ᵉʳ septembre 2026
**Périmètre** : dépôt à `main` — commit `6aecaa5` (PR #27, 22:59 UTC), branche de travail `arena/01a05f35-babbersland`
**Méthode** : exécution réelle de tous les contrôles annoncés (`make controle`), batterie de mutations sur copies isolées (`make batterie`), installation du venv épinglé, vérification des scellés et des empreintes, examen du workflow CI et de l'état distant GitHub (runs, PR, tags, issues). Aucune régénération d'artefact n'a été lancée (elle graverait l'empreinte et modifierait des binaires scellés — principe E-21 respecté).

---

## 1. Synthèse

| Axe | Verdict | Éléments vérifiés |
|---|---|---|
| **Intégrité du canon 2026-I** | ✅ **Conforme** | Continuité, parité des données (18 personnages · 5 régions · 5 fractions · 20 événements), 6 règnes recalculés, 0 anomalie |
| **Artéfact PDF canonique** | ✅ **Conforme** | 29 pages, **24 illustrations** promises **et** servies, 23 légendes appariées planche à planche, empreinte à jour (`e1168ee0…`) |
| **Contrôles embarqués** | ✅ **12/12 verts** | `make controle` complet : sources, continuité, canon, chroniques, PDF, fraîcheur, géographie, portail, Atlas, Arbre, scellés |
| **Capacité à refuser** (les contrôles « mordent ») | ✅ **20/20** | Batterie : 16 mutations refusées, 4 éditions légitimes acceptées |
| **Gel des archives** (G, H, 28 maîtres) | 🟠 **En défaut d'application en CI** | Scellés intacts et vérifiés **localement** ; l'étape CI correspondante ne peut **pas échouer** (constat C-01) |
| **CI GitHub** | ✅ **Active et verte** | 18 étapes ; 6 derniers runs sur `main` en succès ; 25 PR mergées ; mais 6/18 étapes encore tolérantes (R1.4, documenté) |
| **Documentation** | 🟡 **1 dérive** | Le README annonce encore « 7 étapes » en `continue-on-error` : il en reste 6 (constat C-02) |
| **Avis d'ensemble** | ✅ **FAVORABLE, UNE RÉSERVE** — technique (C-01), deux dérives mineures, un point de veille | |

**En une phrase** : le projet est dans l'état le plus sain de son historique — canon, artéfacts, contrôles et CI s'accordent ; la seule faiblesse réelle est que le contrat « dur » de gel des archives n'est, en CI, qu'un avertissement, pas une barrière.

---

## 2. Le projet en chiffres

| Domaine | Mesure |
|---|---|
| Contenu éditorial | ~117 000 mots de Markdown (23 documents racine, 6 chroniques, 17 documents de gouvernance, 5 géographie) |
| Canon structuré | 4 fichiers JSON (`personnages`, `lieux`, `monnaie`, `evenements`) : 18 personnages, 5 régions, 5 fractions monétaires, 20 événements datés, 1 proposition déclarée (12 octobre 1904) |
| Production | 20 scripts Python (4 006 lignes), Makefile, `requirements.txt` épinglé (reportlab 5.0.1 · pillow 12.3.0 · pypdf 6.16.2) |
| Artéfacts | PDF canonique 2026-I (29 pages, 7,3 Mo) · PDF archive 2026-G (15,6 Mo) · 28 maîtres PNG · 77 photographies réalistes (211 Mo) · 77 vignettes WebP (4,6 Mo) · 3 fichiers audio (3,7 Mo) |
| Poids | Dépôt GitHub ≈ 318 Mio · `.git` local 311 Mio — objets lourds encore dans Git (R1.6, migration LFS bloquée côté CDN, documenté) |
| Gouvernance | 25 PR mergées, 2 PR fermées, 0 issue ouverte, tag annoté `v2026-I`, CI active (18 étapes + 6 en `continue-on-error`) |

**Univers canonique** : micronation narrative fondée le 12 octobre 1847 par Babber Ier l'Ancien ; 7 générations de règnes (1847 → 2026) ; devise « Une Pabst, une poutine, et on relaxe » ; capitale Pabst City (3 500 âmes) ; 7 000 âmes sur 5 régions ; Monts Froissés culminant à 1,20 m depuis le 15 juillet 1962.

---

## 3. Ce qui a été vérifié et trouvé conforme

### 3.1 Exécution des contrôles (`make controle` — 10 contrôles, 0 échec)

| Contrôle | Résultat mesuré |
|---|---|
| `py_compile sources/*.py` | ✅ compiles |
| `check_continuity.py` | ✅ « 2026-I, supplément H, chronologie, chroniques, ancres du générateur (23 illustrations) et fichiers d'images concordent » |
| `check_canon.py` | ✅ « 18 personnages · 5 régions · 5 fractions · 20 événements, 1 déclaré hors canon (12 octobre 1904) · 6 règnes arithmétiquement contrôlés » |
| `check_chroniques.py` | ✅ « 7 grandeurs confrontées, 71 cotes d'archives, 4 divergences déclarées, toutes observées » |
| `check_pdf.py` | ✅ « 29 pages, 24 flux embarqués pour 24 illustrations promises, 23 légendes appariées, aucun renvoi orphelin, aucune planche non consentie » |
| `pdf_fingerprint.py --check` | ✅ empreinte `e1168ee0842c0f1472bee0939045323a` à jour |
| `check_geography.py` | ✅ 5 régions, 5 500 âmes urbaines, Monts nés en 1962, total proposé 7 000 |
| `check_portal.py` | ✅ 18 fiches ↔ 18 du canon, dates couvertes |
| `empreinte_atlas.py --check` | ✅ SVG `fe1e95c5…` · PNG `354e0fe5…` · HTML `d34401c3…` |
| `empreinte_arbre.py --check` | ✅ conforme à la variante « reference-locale » (1600×1000, 16×16box `45e876bf…`, encre 0.131) |
| `make scelle` | ✅ archives 2026-G/H intactes · 28 maîtres conformes au scellé |

### 3.2 Reproductibilité clé en main (constat E-11 des rapports précédents : résolu)

`python3 -m venv .venv && pip install -r requirements.txt` réussit sur Python 3.11.2 (PEP 668 contourné comme documenté) ; les versions épinglées s'installent à l'identique. Le README est désormais **exécutable ailleurs que chez son auteur**.

### 3.3 La batterie prouve que les contrôles ont des dents — 20/20

| Famille | Scénarios | Résultat |
|---|---|---|
| **Fautes — la chaîne doit refuser** | 16 mutations : portraits intervertis, planche sans promesse, silences percés, Monts debout en 1946, mort décalée, génération promotionnée, population truquée, archive raturée, événement inventé, date décrochée, syntaxe cassée, chronique non décrétée, banc de plus, cote réattribuée, déclaration obsolète… | ✅ **16/16 refusées**, chacune par le bon contrôle |
| **Éditions légitimes — la chaîne doit laisser passer** | 4 scénarios (dépôt tel quel, planche promise/ancrée/scellée, re-scellé assumé, divergence déclarée) | ✅ **4/4 acceptées** |

### 3.4 État distant (GitHub)

- **CI** : workflow `continuite.yml` actif ; derniers runs sur `main` (PR #22 → #27) tous en **success** (~50 s à 7 min).
- **PR** : 25 mergées (#12 → #27), 2 fermées sans fusion (#11 audit, #16 gabarit), 0 ouverte.
- **Pas d'issue ouverte** — les tickets vivent dans `ROADMAP_2026_II.md` (convention du projet).
- **Tag** `v2026-I` présent (annoté, commit `36353048…`).

---

## 4. Constats

### 🟠 C-01 · L'étape CI « Gel des archives » est non bloquante en pratique

**Fait.** L'étape « Gel des archives (G et H intacts) et des maîtres d'illustration » (`.github/workflows/continuite.yml`, lignes 143–150) s'exécute ainsi :

```yaml
run: |
  (sha256sum --check gouvernance/ARCHIVE.sha256 || echo "::warning::ARCHIVE.sha256 a des écarts")
  (sha256sum --check gouvernance/ICONOGRAPHIE.sha256 || echo "::warning::ICONOGRAPHIE.sha256 a des écarts")
```

Le commentaire affirme « **PAS de `continue-on-error` ici : c'est le contrat canonique, dur** », mais les deux parenthèses se terminent par `echo` (code de sortie 0) : **le statut de l'étape est toujours `success`**, même si un scellé est cassé — une altération des archives ou d'un maître d'illustration ne produit qu'un message d'avertissement dans le log.

**Vérification complémentaire** : aucun contrôleur Python ne vérifie ces scellés (`grep sha256` sur `check_continuity.py`, `check_canon.py`, `check_pdf.py`, `pdf_fingerprint.py`, `check_geography.py`, `check_portal.py`, `check_chroniques.py` — 0 occurrence). La seule vérification réellement **bloquante** est `make scelle`, c'est-à-dire **locale uniquement**.

**Impact.** Le contrat de gel — présenté dans le README comme « le contrat canonique, dur » — n'est en CI qu'une alerte. C'est précisément la classe de défaut (silence de la chaîne) que les audits précédents (E-07, E-09, E-21) ont successivement fermée ailleurs : le dernier verrou reste de facto ouvert.

**Remède (2 minutes, 2 lignes)** : retirer les `|| echo "::warning::…"` de l'étape (elle devient réellement bloquante) ; ou, mieux, déplacer la vérification dans `check_continuity.py` (hashlib, sans dépendance) afin qu'un scellé cassé fasse échouer l'étape « Continuité » dès maintenant. Le commentaire du workflow annonce d'ailleurs ce retrait (« une fois la cause identifiée, on retire le `|| true` ») — la cause est identifiée depuis plusieurs jours, l'étape ne l'a pas été.

### 🟡 C-02 · Le README annonce 7 étapes tolérantes ; il en reste 6

**Fait.** `README.md` contient encore, en deux endroits (tableau de gouvernance, ligne ~36, et § statut CI, ligne ~149) : « **7 étapes** sur 18 portent `continue-on-error: true` ». Le workflow réel en compte **6** (Atlas, Hymne, Vignettes, Régénération PDF, Artéfact, Fraîcheur — l'Arbre est devenu bloquant avec R1.4.b). `gouvernance/CI_LIMITES.md`, le CHANGELOG [2026-XI] et le message du commit #27 (« il en reste réellement 6 ») sont corrects — **le rectificatif #27 n'a pas touché le README**.

**Impact.** Faible (documentaire), mais dans un projet où la précision des comptes est elle-même un contrôle, la dérive est à corriger au prochain passage.

### 🟡 C-03 · Comptages inexpliqués : « 22 sous-étapes » et « 4 post-step »

**Fait.** `CI_LIMITES.md` parle de « 22 sous-étapes » et le README de « 18 étapes + 4 post-step ». Le workflow contient exactement 18 étapes, aucune section `post:` (vérifié par grep). L'origine des « 4 post-step » et des « 22 sous-étapes » n'est pas documentée.

**Impact.** Faible ; à clarifier ou à retirer pour éviter qu'un futur audit rejoue le débat de comptage (le précédent des « 6 vs 7 » étapes a déjà coûté une PR).

### ⚪ C-04 · DeprecationWarning Pillow dans `empreinte_atlas.py`

**Fait.** L'exécution de `empreinte_atlas.py --check` émet : `DeprecationWarning: Image.Image.getdata is deprecated … will be removed in Pillow 14 (2027-10-15)`. La version est épinglée (`pillow==12.3.0`), donc **aucun impact aujourd'hui** ; mais le retrait est daté (2027) — pile dans la fenêtre de l'horizon 3 de la roadmap (diffusion 2027).

**Remède** : remplacer `getdata()` par `get_flattened_data()` (ou normaliser via `tobytes()`) lors du prochain passage sur ce script.

---

## 5. Risques connus et points de vigilance (existants, rappelés)

1. **Exposition de la CI aux artefacts binaires** : 6/18 étapes sont tolérantes, et **5 d'entre elles couvrent toute la chaîne du PDF** (régénération → appariement → fraîcheur). La CI peut donc être verte alors que le PDF publié serait stale ou cassé ; la garantie forte vient aujourd'hui de `make controle` local. Priorité : R1.4.c–h puis l'image Docker épinglée (R1.4.a-v3).
2. **Poids du dépôt** : ≈ 318 Mio, objet lourd = galerie réaliste (211 Mio). La migration LFS (R1.6, variante A′) est écrite et mesurée mais **bloquée par l'upload CDN depuis l'environnement d'agent** — à exécuter par un acteur disposant du réseau GitHub complet. Tant qu'elle n'est pas faite, chaque clone transporte ~318 Mio.
3. **Accès aux journaux CI** : les logs d'étapes passent par Azure Blob, injoignables depuis l'environnement d'agent — c'est ce qui a retardé R1.4.a et conduit au contournement par annotations de check-run. Le palliatif fonctionne ; la cause racine (lecture des logs) reste traitée à la marge.

---

## 6. Recommandations (par priorité)

| # | Action | Effort | Rattachement |
|---|---|---|---|
| 1 | Rendre l'étape « Gel des archives » bloquante (retirer les `|| echo`) ou déplacer la vérification sha256 dans `check_continuity.py` | 2 min | C-01 |
| 2 | Corriger le README : « 7 étapes » → « 6 étapes » (2 occurrences) et harmoniser le compte « 18 étapes » | 5 min | C-02 |
| 3 | Clarifier ou supprimer « 22 sous-étapes / 4 post-step » | 5 min | C-03 |
| 4 | Poursuivre R1.4.a-v3 (image Docker épinglée) pour rendre l'Atlas bloquant | ½ journée | R1.4 |
| 5 | Remplacer `getdata()` de `empreinte_atlas.py` avant Pillow 14 | 5 min | C-04 |

---

## 7. Conclusion

**FAVORABLE, une réserve technique (C-01).** Au terme de cette passe :

- le **canon** est cohérent, chiffré et contrôlé (0 anomalie sur 6 règnes, 24 illustrations, 71 cotes, 18 fiches) ;
- les **artéfacts** publiés correspondent à leurs promesses (verbatim : « 24 flux embarqués pour 24 illustrations promises ») ;
- les **contrôles** sont démontrés capables de refuser (16/16 mutations) et d'accepter (4/4 éditions légitimes) ;
- la **CI** est active, verte et décrite avec une honnêteté documentaire rare (limites chiffrées, causes, hypothèses non vérifiées).

Le seul verrou qui n'était pas fermé est le dernier : le gel des archives n'était, en CI, qu'un avertissement. C'est une correction d'une ligne — **faite le soir même** : voir le suivi d'exécution ci-dessous. Le niveau de tenue global de ce dépôt — un univers fictionnel gouverné comme un projet logiciel audité — reste objectivement supérieur à celui de la plupart des productions éditoriales versionnées.

---

## 8. Suivi d'exécution — C-01 corrigé (R1.4.h, même jour)

| Élément | État |
|---|---|
| Étape de gel restaurée en mode strict (`sha256sum --check --quiet` sur `ARCHIVE.sha256` et `ICONOGRAPHIE.sha256`, `\|\| echo` supprimés) | ✅ Fait |
| Étape déplacée **en tête de chaîne** (après `py_compile`, avant toute régénération) | ✅ Fait — condition du strict, voir ci-dessous |
| Modèle `sources/github_actions_continuite.yml` | ✅ Synchronisé avec la copie installée (diff vide) |
| Documentation (README « 7 → 6 étapes », ROADMAP R1.4.h ✅, CI_LIMITES § R1.4.h, CHANGELOG 2026-XII) | ✅ Fait |
| Contrôles locaux (`make controle`) | ✅ 12/12 verts après changement |
| CI sur la branche de travail | ✅ **Verte** — run pull_request `33569884539` (2e5a2bd) : étape 7 « Gel des archives » (strict, avant régénération) **success**, étape 13 « Arbre » (bloquante) **success**, aucune annotation `a des écarts` ; les seules annotations restantes sont la dépréciation Node.js 20 et le notice `charge=… connue=ci-ubuntu-24.04-py3.12` (conformité R1.4.b) |

**Pourquoi le déplacement en tête de chaîne, et pas seulement le retrait du `|| echo` ?** La correction naïve — retirer les `|| echo` sans bouger l'étape — aurait rendu la CI **rouge permanente** : le runner régénère l'arbre généalogique (couvert par `ICONOGRAPHIE.sha256`) dans une variante de rendu légitime (FreeType 2.13, 3 cellules/256 — mesure R1.4.b), et la vérification post-régénération comparait donc un fichier différent du scellé. Mesure à l'appui : l'annotation `ICONOGRAPHIE.sha256 a des écarts` est présente sur **chaque run, y compris les verts** (vérifié sur le run #33568899178). Le contrat du gel (E-18) porte sur les octets **commités**, pas sur le rendu régénéré — l'étape doit donc le vérifier **avant** que la chaîne ne touche aux fichiers. Le rendu régénéré a son propre contrat bloquant : `empreinte_arbre.py --check` (R1.4.b).

---

---

## 9. Suivi d'exécution — recommandations 2, 3, 4 et 5 (vague « verrouiller », 1ᵉʳ septembre 2026, dernière heure)

| # | Recommandation | État |
|---|---|---|
| 1 | Rendre l'étape « Gel des archives » bloquante | ✅ **Fait le jour même** (§ 8, R1.4.h) |
| 2 | README : « 7 étapes » → « 6 » | ✅ **Fait** (C-02, PR #28) — puis rendu caduc par la suite : il reste **0** étape tolérante |
| 3 | Clarifier ou supprimer « 22 sous-étapes / 4 post-step » | ✅ **Fait** — **suppression**, pas réexplication (C-03). Mesure au parseur YAML : `continuite.yml` = **18 étapes** (16 nommées + `actions/checkout` + `actions/setup-python`), **aucune** section `post:`. Les sous-étapes créées par le runner ne sont pas une grandeur du projet : un compte invérifiable est un compte qui mentira tout seul |
| 4 | Poursuivre R1.4.a-v3 pour rendre l'Atlas bloquant | ✅ **Fait, par un autre chemin que celui prévu.** Le ticket proposait (a) image Docker épinglée, (b) empreinte normalisée, (c) régénération + gravure. **Aucune** de ces trois voies n'a été prise : (a) gèle une machine pour un problème de sens, (b) cherche un seuil que la mesure R1.4.b a montré inexistant, (c) graverait en CI (E-21). Le défaut réel était ailleurs : **l'étape n'appelait jamais l'empreinte** — elle régénérait, vérifiait les données, et jetait. R1.4.a-v3 branche `empreinte_atlas.py --check` dans l'étape, remplace l'échantillonnage NEAREST 16×16 par le moyennage BOX de l'Arbre, et adopte les variantes acceptées. La cause racine de la non-reproductibilité **reste non identifiée** et n'est plus une condition de rien |
| 5 | `getdata()` de `empreinte_atlas.py` avant Pillow 14 | ✅ **Fait** (C-04) — éliminé par la réécriture (`tobytes()`), sans attendre 2027 |

**Élargi au périmètre annoncé (les six sous-tickets R1.4 restants), livré le même soir :**

| Constat / risque du rapport | Ce qui a été fait |
|---|---|
| Risque n° 1 — « 5 des 6 étapes tolérantes couvrent toute la chaîne du PDF ; la CI peut être verte alors que le PDF publié serait périmé » | **R1.4.e, f, g** : les trois `continue-on-error` retirés. La régénération, qui ne comparait rien (un générateur qui plante passait), échoue désormais le run ; `check_pdf.py` et la fraîcheur deviennent bloquants. Le PDF reçoit une section de **variantes d'environnement** (`PDF CANONIQUE`), hiérarchisée : `pdf_fingerprint.txt` reste LE contrat canonique |
| « La garantie forte vient aujourd'hui de `make controle` local » | **`gouvernance/CI_LIMITES.md`** n'a plus de sens comme distinction : la garantie locale et la garantie GitHub sont désormais la même chaîne, 18 étapes bloquantes. `make controle` compte **douze** vérifications (contre dix avant ce soir) dont **quatre sceaux d'artéfacts**, plus les scellés |
| Cause racine non identifiée (polices, locale, Pillow) | Traitées **par construction** : plus aucune étape ne compare des octets d'artéfact régénéré. Le bruit de rendu d'un environnement se **grave** (`--accepter`, assentiment tracé), il ne se tolère plus en silence |
| La batterie, seule preuve que les contrôles mordent, locale et volontaire | **Nouveau workflow `batterie.yml`** : lundi 03:17 UTC + `workflow_dispatch`. Vingt-cinq scénarios (20 fautes refusées, 5 éditions acceptées) depuis le garde-fou P1c sur copies isolées, puis preuve que l'arbre de référence est resté intact (`git diff --quiet`) et que les scellés n'ont pas bougé. Un contrôle émasculé — la classe C-01, qui a survécu à quatre audits — ne survit plus à une semaine |
| Constats nouveaux non demandés, découverts en route | **Déclarés en tickets, pas en notes** : R1.8 (parité modèle `sources/github_actions_*.yml` ↔ workflow installé — rien ne la vérifie) et R1.9 (`images/realistes/`, 211 Mio, scellé par rien : `ICONOGRAPHIE.sha256` ne couvre que les 28 maîtres de `images/`) |

**Verdict après suivi** : la réserve technique C-01 est close **et** sa classe de défaut est close — non par un correctif de plus, mais parce qu'il ne reste plus une seule étape qui puisse avertir au lieu d'échouer.

**Mesures consignées** : `make controle` **12/12 + scellés, 0 échec** ; `make batterie` **24/24 en 2 min 26 s** (puis **25/25 en 2 min 29 s** après le canari du PDF et son garde-fou P1c, §R1.4.g de `CI_LIMITES.md`) ; charges mesurées sur les trois fautes nouvelles (Atlas : `16x16box` + `encre` ; hymne : `profil` + `pcm8`, `frames` intact ; vignettes : `grilles`) ; section `ARBRE GÉNÉALOGIQUE` du scellé **inchangée octet pour octet** après passage sur la mécanique commune `sources/sceaux.py`.

*Rapport rédigé le 1ᵉʳ septembre 2026 — dépôt `5bhff95pdk-design/Babbersland-`, commit `6aecaa5`. Toutes les mesures citées ont été exécutées dans ce clone : `make controle` (12/12), `make batterie` (20/20), installation du venv épinglé, inspection du workflow et interrogation de l'API GitHub (`gh`).*  
*§ 9 ajouté le 1ᵉʳ septembre 2026, dernière heure (session `arena/01a05f55-babbersland`) : R1.4 clos, CI intégralement bloquante, batterie à horaires.*
