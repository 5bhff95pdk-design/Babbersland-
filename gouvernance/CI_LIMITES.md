# 🔧 Limites connues de la CI de continuité

**Référence** : CI-2026-I · diagnostic des étapes en `continue-on-error: true`
**Établi le** : 1ᵉʳ septembre 2026 · **dernier état** : 1ᵉʳ septembre 2026 (R1.3 — manifeste des livrables — ajouté à la CI, après R1.4, R1.8 et R1.9)
**Ticket de durcissement** : R1.4 (sous-tickets R1.4.a à R1.4.h) — **les huit sont livrés** ; les bornes nées en route (R1.8, R1.9) le sont aussi, et R1.3 (manifeste des livrables) a rejoint la chaîne

**État mesuré le 1ᵉʳ septembre 2026, tard en soirée** : `sources/github_actions_continuite.yml` compte
**20 étapes** (18 nommées + `actions/checkout` + `actions/setup-python`), **0** portant
`continue-on-error`. Le **manifeste des livrables** (R1.3, `check_manifest.py --check`) a
rejoint la chaîne entre le gel en tête et la parité modèle ↔ workflow installé (R1.8) ; la
**parité** reste d'actualité, simplement précédée de cette nouvelle vérification. Le gel en tête
couvre, lui, aussi `gouvernance/GALERIE.sha256` (R1.9). Le compte est pris au parseur YAML, pas
au grep : une étape tolérante de trop dans ce document coûterait moins cher qu'une étape
tolérante de trop dans le workflow.

---

## Contexte

La CI de continuité (`.github/workflows/continuite.yml`) est **active et verte** depuis le 1ᵉʳ septembre 2026 (PR #22, livraison R0.4, 18 étapes à l'époque). Elle en compte **20** depuis R1.3 (manifeste des livrables).

**Historique du comptage** (le constat C-03 de RA-2026-IV-01 mérite sa ligne, parce que
le débat des « 6 contre 7 » a déjà coûté une PR) : ce document parlait de « 22
sous-étapes » et le README de « 18 étapes + 4 post-step ». **Les deux formulations sont
retirées** : le workflow ne contient aucune section `post:` et le nombre de sous-étapes
n'a jamais été une grandeur du projet — un runner peut en créer, les supprimer ne dépend
pas de nous. On compte donc les étapes, point final : 18, dont 7 tolérantes à la
livraison R0.4, 6 après R1.4.b (Arbre bloquant), **0 après R1.4.a-v3 et R1.4.c–g**.
Les sections qui suivent gardent la trace des comptages successifs : c'est un journal de
limites, pas un tableau de bord.

---

## Statut R1.4.a-v2 (1ᵉʳ septembre 2026) — empreinte sémantique créée, mais NON intégrée

**L'empreinte sémantique `sources/empreinte_atlas.py` est LIVRÉE**, mais l'étape Atlas **reste en `continue-on-error: true`**.

**Implémentation livrée** :
- `sources/empreinte_atlas.py` (60 lignes) : calcule trois empreintes SHA-256 sémantiques (SVG : viewBox/ids/data-since/classes/toponymes ; PNG : dimension/mode/perceptual hash 16×16 NEAREST ; HTML : ids/classes/h1/h2/dates).
- `gouvernance/ARTIFACT_SIGNATURES.sha256` (nouveau) : stockage des empreintes. Section Atlas ajoutée.
- `Makefile` : nouveau but `make empreinte-atlas` ; ajout dans `make controle`.

**Pourquoi l'étape n'est PAS devenue bloquante ?**

L'empreinte sémantique fonctionne parfaitement en local (deux runs successifs donnent la même empreinte ; un changement structurel est détecté). En CI (PR #25, runs #16 à #22), l'étape **échoue toujours**, sans qu'on puisse récupérer la cause exacte :

- Les logs Azure Blob ne sont pas accessibles depuis l'environnement d'agent (erreur `EOF` systématique, constaté à plusieurs reprises)
- Les artifacts non plus (même erreur)
- La sortie de l'étape, qui devrait indiquer la nature de la divergence, est invisible

**Hypothèses sur la cause non vérifiable** :
1. Pillow différent sur le runner : malgré `requirements.txt`, le binaire compilé peut varier (architecture, optimisations C).
2. Locale / timezone : Pillow écrit des métadonnées EXIF en fonction de l'environnement.
3. PNG perceptual hash : la résolution 16×16 NEAREST peut quand même être sensible à des variations de 1-2 octets par pixel dues à un encoding différent.

**Décision pragmatique** : **rétablir `continue-on-error: true`**, documenter honnêtement l'état, et reporter R1.4.a à une session future avec accès aux logs Azure Blob.

**Valeur apportée malgré tout** :
- `sources/empreinte_atlas.py` reste **un outil disponible** : `python sources/empreinte_atlas.py [--write|--check]` peut être utilisé manuellement pour vérifier l'Atlas.
- Le fichier `gouvernance/ARTIFACT_SIGNATURES.sha256` est créé : le pattern est en place pour les R1.4.b–g à venir.
- Le Makefile a un but `make empreinte-atlas` documenté.
- L'investigation a été **honnête** : trois approches testées (MD5, perceptual 8×8 Lanczos, perceptual 16×16 NEAREST), aucune ne résout la CI sans accès aux logs.

**R1.4.a-v3 à faire** :
- Avoir accès aux logs Azure Blob (sortir de l'environnement d'agent, ou configurer un autre canal de logs)
- Une fois la cause identifiée, choisir entre :
  (a) **image Docker épinglée** (la solution propre : `python:3.12-slim-bookworm` avec Pillow précompilé)
  (b) **ajustement de l'empreinte** (par exemple : normaliser l'image en niveaux de gris avant le hash pour éliminer les variations RGB)
  (c) **stratégie « régénération + gravure »** (comme `pdf_fingerprint.py` : on regenère le PNG en CI, on écrit un `atlas.sha256` à part, et on le commit)

**Devenu (1ᵉʳ septembre 2026)** : aucune des trois options ci-dessus n'a été prise.
La voie (a) gèle une machine pour un problème de sens ; la (b) cherche un seuil qui,
mesure R1.4.b à l'appui, n'existe pas ; la (c) grave en CI, ce que E-21 interdit.
R1.4.a-v3 a fait le (d) : le modèle de R1.4.b — **variantes acceptées**, diagnostic par
annotation, et l'empreinte **enfin appelée par l'étape** (voir la section ci-dessous).

---

## Statut R1.4.b (1ᵉʳ septembre 2026) — Arbre durci, étape BLOQUANTE (modèle « variantes acceptées »)

**Première mesure réelle du runner CI, obtenue grâce aux annotations de check-run.** Les journaux d'étape transitent par Azure Blob (`productionresultssa*.blob.core.windows.net`), injoignable depuis l'environnement d'agent — c'est ce qui a bloqué l'investigation R1.4.a-v2. Le script d'empreinte émet donc son diagnostic sous forme d'annotations de workflow (`::notice`, `::error`), que l'API Checks (`/check-runs/{id}/annotations`) sert depuis GitHub.

**La mesure (PR #26)** : entre la machine de référence et le runner `ubuntu-latest`, la grille moyennée 16×16 quantifiée en 16 niveaux diverge sur **3 cellules sur 256, chacune d'un seul niveau** (~16 unités RVB) — cellules dans les zones de texte, assises sur une frontière de quantification. Cause : versions FreeType différentes (2.12 / Debian 12 ↔ 2.13 / Ubuntu 24.04), l'antialiasing des glyphes décale quelques pixels. Par ailleurs une mutation témoin « titre d'un nœud gommé » ne bouge que **2 cellules d'un niveau**. **Bruit de rendu légitime et retouche de contenu se chevauchent : aucun seuil de tolérance (≤ N cellules à Δ ≤ 1) ne les sépare sans rendre le contrôle aveugle aux retouches fines.**

**Modèle retenu — variantes acceptées** : on grave dans `gouvernance/ARTIFACT_SIGNATURES.sha256` **l'ensemble des chaînes de rendu observées** (`size|mode|16x16box-md5|ink-millième`) :

- `arbre_variante_reference-locale` — machine de référence (bac à sable de l'agent) ;
- `arbre_variante_ci-ubuntu-24.04-py3.12` — runner CI (charge copiée depuis l'annotation du run) ;
- `arbre_png` — sha256 de l'ensemble trié (tête de contrat à une ligne).

`--check` exige l'**appartenance exacte** à l'ensemble : retouche de contenu (même 2 cellules) → variante inédite → **échec** ; nouveau FreeType légitime → variante inédite → échec **diagnostiqué par annotation** (grille complète incluse), puis accepté explicitement par `empreinte_arbre.py --accepter '<charge>' <étiquette>` — acte d'assentiment tracé dans git. Jamais de bascule silencieuse ; jamais d'aveuglement.

**Validation (rejouée sur le modèle final)** : régénération conforme à « reference-locale » (code 0) ; mutations « nœud ajouté » (8 cellules) et « titre gommé » (2 cellules) détectées (code 1) — y compris le titre gommé, qu'une tolérance chiffrée aurait laissé passer ; 1 pixel et bruit ±2 sur 300 px conformes (même grille — la protection bit à bit du fichier tracké reste celle d'`ICONOGRAPHIE.sha256`, E-18) ; charge mal formée refusée par `--accepter` (code 1).

**Intégration** : étape CI bloquante (`continue-on-error` retiré, `empreinte_arbre.py --check` remplace `git diff --exit-code`) ; but `make empreinte-arbre` (acte d'assentiment, variante `reference-locale`) ; `--check` dans `make controle`.

**Cérémonie lors d'un changement de contenu** : éditer `generate_genealogy.py` → `make arbre` → `make empreinte-arbre` → pousser → lire l'annotation CI → `--accepter` la charge du runner → pousser. Deux poussées par changement de contenu : c'est le prix, connu, de l'assentiment double-machine tant que R1.2 (matrice multi-OS) n'existe pas.

**Ce que R1.4.b apporte aussi à R1.4.a-v3** : le canal annotation + grille détaillée est directement réutilisable pour diagnostiquer l'Atlas (même douleur d'investigation). — **chose faite le 1ᵉʳ septembre 2026**, voir la section suivante.

---

## Statut R1.4.a-v3 (1ᵉʳ septembre 2026) — Atlas : empreinte branchée en CI, étape BLOQUANTE

**Le défaut n'était pas la fragilité de l'empreinte, c'est qu'elle n'était pas appelée.**
L'étape CI se bornait à `generate_map.py` puis `check_geography.py`, sous
`continue-on-error`. Autrement dit : la CI régénérait la carte, vérifiait ses données,
et jetait le résultat — sans jamais consulter le contrat gravé. C'est la classe exacte
du constat E-09 (une vérification qui ne vérifie rien), et le `|| echo` de C-01 en
mieux : là, rien n'était même tenté.

**Trois changements, un seul objectif — que l'étape puisse échouer pour les bonnes raisons :**

1. **L'étape appelle le contrat** : `empreinte_atlas.py --check` s'ajoute aux deux
   commandes existantes.
2. **La charge devient une somme de composantes nommées**
   (`svg:…|html:…|taille:…|mode:…|16x16box:…|encre:…`), et le PNG est comparé par
   **moyennage BOX 16×16 quantifié sur 16 niveaux**, comme l'Arbre — l'échantillonnage
   NEAREST de v2 lisait un pixel sur cent et survécut mal au passage du NEAREST à
   n'importe quel décalage d'un pixel : c'est la cause probable des échecs de PR #25,
   et elle n'avait pas besoin d'être comprise pour être remplacée.
3. **Le contrat est un ensemble de variantes observées**, plus une valeur unique. Une
   charge inédite bloque, et l'annotation dit **quelle composante** a bougé :
   `svg` ou `html` = la carte a changé (délibération d'Avis, puis re-gravure) ;
   seul `16x16box`/`encre` = bruit de rendu d'un environnement (acceptation après
   lecture de la grille). Le diagnostic ne demande plus de deviner.

**Migration assumée** : l'ancienne section du scellé (`atlas_svg`, `atlas_png`,
`atlas_html` en empreintes SHA-256 nues) est **remplacée** par
`atlas_lot` + `atlas_variante_reference-locale`. Le contrat de v2 n'a jamais été
appliqué par la chaîne : il n'y a donc pas de compatibilité à maintenir, et l'histoire
est dans ce fichier.

**Mesure en CI, canari du 1ᵉʳ septembre 2026 (runs #33573944229 puis #33574049627)** — et
c'est exactement ce que le dispositif est là pour rendre lisible :

- le runner a produit `svg:d6aab963c7ea953c` `html:10ab30af34f9c925`
  `taille:1600x1100` `mode:RGB` `encre:0.325` — **les cinq composantes structurelles
  identiques à `reference-locale`**. La carte n'a pas changé.
- seule `16x16box` divergeait. La grille ayant été ajoutée au diagnostic (commit suivant du
  même soir), la divergence est **comptée** et non plus devinée : **3 cellules sur 256,
  chacune d'un seul niveau de quantification** (lignes 1-2 colonne 6 — la zone du titre — et
  ligne 14 colonne 5 — les étiquettes de la forêt), encre inchangée. Signature identique à la
  mesure de l'Arbre en R1.4.b : FreeType 2.12 ↔ 2.13, antialiasing des glyphes. Le PNG pèse
  99 129 o sur le runner contre 98 814 o ici — même rendu, autre compresseur.
- la mutation témoin **A2** de la batterie (un rectangle noir de 200×80 px, une région noyée)
  déplace **4 cellules, d'amplitudes 2, 6 et 7 niveaux**, et bouge l'encre. Les deux
  distributions se touchent en **nombre** de cellules (3 contre 4) et ne se touchent pas en
  **amplitude** : c'est la démonstration, pour l'Atlas aussi, qu'aucun seuil ne sépare le
  bruit du contenu — d'où le refus d'une tolérance chiffrée.
- la variante du runner a donc été **acceptée à la main** sous l'étiquette
  `ci-ubuntu-24.04-py3.12`, dans le même format que l'Arbre, et le run vert qui suit est la
  preuve bloquante demandée. Deux poussées : c'est le prix, connu, de l'assentiment
  double-machine tant que R1.2 (matrice ou image épinglée) n'existe pas.

**Ce que le canari a aussi montré, qui n'était pas gagné** : une étape bloquante **arrête la
chaîne**. Sur les deux runs rouges, l'Atlas échouant en position 9, les étapes 10 à 16
(Arbre, Hymne, Vignettes, régénération, artéfact, fraîcheur) **ne se sont pas exécutées** :
elles n'étaient pas conformes, elles n'avaient pas tourné. Le verdict attendu est le run
vert complet, dont chaque `::notice charge=… connue=…` consignera la charge du runner pour
les quatre sceaux à la fois.

**Le run vert est venu (#33575391219, 1ᵉʳ septembre 2026) — 18 étapes sur 18, aucune
tolérante, et les cinq annotations qui valent preuve :**

```
empreinte-atlas     : … 16x16box:00eaea478bdf40bb…|encre:0.325      connue=ci-ubuntu-24.04-py3.12
empreinte-arbre     : … 16x16box:a586e3355260ebe4…|ink:0.131        connue=ci-ubuntu-24.04-py3.12
empreinte-hymne     : frames:1598625|…|pcm8:b8c8b6db…|crete:0.720   connue=reference-locale
empreinte-vignettes : nb:77|largeur:640|grilles:b0bb7402eac27fb3…   connue=reference-locale
empreinte-pdf       : fingerprint:1a76a0e8ee10dec6…|pages:29|…      connue=variante-acceptee:ci-ubuntu-24.04-py3.12
```

Deux lectures à en tirer, et elles ne sont pas symétriques. **Là où la charge compare du
contenu décodé** (hymne, vignettes), le runner donne **la charge de la référence locale**,
sans variante à graver : le contrat est machine-indépendant, ce qui était le but de R1.4.a–d.
**Là où la charge compare un raster** (Atlas, Arbre) ou un fichier conteneur (PDF), le runner
donne une charge d'environnement **acceptée nommément** — pas tolérée, pas ignorée : gravée,
étiquetée, et révisable par `make pdf` + `make empreinte` sur la machine de référence.
Un `::warning::` qui dit « ce n'est pas grave » est un contrôle sans dents ; une variante
nommée dit **quelle** divergence est tenue pour du rendu, par qui, et depuis quand.
---

## Statut R1.4.c et R1.4.d (1ᵉʳ septembre 2026) — Hymne et Vignettes : charges sémantiques

**Point commun aux deux étapes** : elles comparaient des **octets** avec
`git diff --exit-code`, ce qui est à la fois trop fragile (un environnement qui encode
autrement rend la CI rouge) et trop lâche (le `git diff` ne compare que ce qui est
*commité* : l'artéfact périmé que la machine de référence reproduit à l'identique
passe comme une lettre). Les deux défauts ont la même racine : on comparait le conteneur
au lieu de comparer le contenu.

**R1.4.c — l'hymne** (`sources/empreinte_hymne.py`). La charge compare ce qui
s'entend : géométrie du signal (`frames`/`rate`/`bits`/`chan` — 72,5 s à 22 050 Hz,
16 bits, mono, soit les promesses du dossier officiel § V), **enveloppe** RMS par
fenêtre de 250 ms quantifiée sur 8 bits, PCM entier replié sur 8 bits (sensible à
l'ordre des notes, insensible à un ULP de libm), amplitude crête au millième.
L'audit RIFF promis par le ticket est fait et **branché** : `--chunks` énumère les
chunks ; le WAV de référence ne contient que `fmt ` et `data`, aucun horodatage. Tout
chunk ajouté par une future version de `wave` est ignoré par la charge **et signalé**
au diagnostic — une tolérance doit rester nommée.

**R1.4.d — les vignettes** (`sources/empreinte_vignettes.py`). 77 WebP dérivés de
`images/realistes/*.png`. La charge compare le **contenu décodé** : grille 8×8 moyennée
et quantifiée par vignette, lot haché, plus `nb`, `largeur` (promesses du diffuseur) et
`octets` (mesure de diffusion signalée, non contractée). Un ré-encodage libwebp
différent ne bouge pas ; un maître oublié de régénérer bouge.

**Ce que R1.4.d révèle au passage** : `images/realistes/` (211 Mio, 77 pièces) n'était
**scellé par rien** — `ICONOGRAPHIE.sha256` couvre `images/*.png`, les 28 maîtres du
volume. La galerie du portail n'avait donc d'autre garde-fou de contenu que l'empreinte des
vignettes, qui ne la protège qu'à moitié (une photographie retouchée dont on oublie de
régénérer les vignettes passe ; retouchée **et** régénérée, elle bloque). La batterie le
démontrait : scénario J1, refusé **uniquement** par `empreinte_vignettes`.

**Fermé le 1ᵉʳ septembre 2026 (R1.9)** : `gouvernance/GALERIE.sha256` (77 lignes, gravé
par `make galerie`) est vérifié par `make scelle` — donc par `make controle` et par
l'étape de gel en tête de chaîne, avant toute régénération, comme les deux autres scellés.
Coût mesuré, conforme au ticket : +77 lignes de scellé, 0 octet de plus en CI (les
fichiers sont déjà dans le checkout ; `sha256sum` les lit en ~1,3 s). Preuve : scénario
**J1bis** de la batterie — la même retouche que J1, vignettes PAS régénérées, refusée par
`scelle` seul (`vue_scelle`, le juge à un seul œil, pour que le mécanisme visé soit bien
celui qui bronche).

---

## Statut R1.4.e, R1.4.f, R1.4.g (1ᵉʳ septembre 2026) — la chaîne du PDF, bloquante

**Le motif invoqué ne les concernait pas.** Les trois étapes portaient
`continue-on-error: true  # R1.4 — voir note Atlas` : un héritage de formulation, pas
une mesure. La non-reproductibilité binaire qui a motivé le mode tolérant de l'Atlas ne
s'applique pas ici, puisque ces étapes ne comparent pas des octets :

| Étape | Ce qu'elle faisait | Ce qui bloquait vraiment |
|---|---|---|
| Régénération de l'encyclopédie | régénérer, sans rien comparer | **un générateur qui plante passait** |
| Artéfact publié (`check_pdf.py`) | comparer pages, flux, légendes | rien — le `continue-on-error` était gratuit |
| Fraîcheur (`pdf_fingerprint.py --check`) | comparer l'empreinte ordonnée | rien (l'empreinte est sémantique depuis R1.1) |

**Corrections** : les trois `continue-on-error` sont retirés. La régénération ne
prétend plus vérifier quoi que ce soit, mais son échec devient une faute. La fraîcheur
reste un `--check` et **jamais** une gravure (E-21 respecté à l'identique).

**R1.4.g — le PDF a désormais lui aussi ses variantes acceptées**, dans la section
`PDF CANONIQUE` de `gouvernance/ARTIFACT_SIGNATURES.sha256`, avec une hiérarchie
explicite et non négociable : `gouvernance/pdf_fingerprint.txt` **reste** le contrat
canonique (seule la machine de référence le re-grave, par `make empreinte`) ; la section
de variantes n'excuse qu'un **rendu** observé ailleurs (runner d'abord, matrice
multi-OS de R1.2 ensuite). `--check` pose son `::notice charge=… connue=…` à chaque
run : la divergence du runner est mesurée, pas supposée.

**Mesure du canari (run #33574438077)** — le PDF était le seul des sept artéfacts dont
la chaîne n'avait pas encore lu le runner. Deux poussées ont été nécessaires pour obtenir
le verdict, et c'est le bon prix : la première n'aurait autorisé qu'une inférence.

| | référence locale | runner `ubuntu-24.04 / py3.12` |
|---|---|---|
| `pages` · `images` · `placements` | 29 · 24 · 25 | **identiques** |
| `texte` — md5 du texte extrait, normalisé | `8296cf53ba12…` | **identique** |
| `disposition` — md5 des hachés de flux, ordonnés | `cd6fdb581a48…` | `7f47b59780a5…` |
| `fingerprint` — l'empreinte, qui combine tout | `e1168ee0842c…` | `1a76a0e8ee10…` |

**Ce que la table établit** : le volume que le runner imprime porte le **même texte**, aux
**mêmes pages**, avec les **mêmes planches aux mêmes endroits** — c'est mesuré, pas supposé.
**Ce qu'elle n'établit pas** : l'identité des *pixels*. Les hachés de flux embarquent le
bitstream JPEG, donc la libjpeg de l'environnement (`derive_bytes()` encode en
`quality=78, optimize=True, progressive=True`), et l'on sait par le canari de l'Atlas que les
rasters des deux machines ne sont pas bit à bit identiques. La divergence de `disposition` est
**cohérente** avec un simple ré-encodage ; elle n'en est pas la preuve.

**Deux actes, distincts et tous deux tracés :**

1. **Contrat durci là où c'était gratuit** : `texte` entre dans `gouvernance/pdf_fingerprint.txt`
   comme champ **comparé** (il est machine-indépendant — la table le prouve) ; `disposition` y est
   consignée en **commentaire**, informative, jamais comparée. Un écart est alors **nommé** :
   `CONTENU : le texte extrait du volume a changé — à corriger, pas à accepter`, ou
   `EMBALLAGE : … seules les octets des flux diffèrent`. **Accepter une variante ne peut plus
   effacer une dérive de texte**, même cachée dans l'empreinte combinée.
2. **Variante acceptée sur mesure** : `pdf_variante_ci-ubuntu-24.04-py3.12`, charge
   `fingerprint:1a76a0e8ee10dec621d0534e4612b01b|pages:29|images:24|placements:25`.

**Ce qui reste ouvert, loyalement** : l'empreinte du PDF retient le nombre de pages — une
pagination divergente (métriques de police) se tratarait de la même façon, mesurer puis accepter
ou corriger. Deux voies rendraient la variante inutile en amont : **R1.2** (image épinglée ou
matrice multi-OS), ou **R1.10** (déclarée ci-dessous, non livrée) : signer le volume par
**identité de planches** — l'image décodée résolue contre les maîtres — plutôt que par le haché
de leurs octets, ce qui est machine-indépendant par construction, comme le sont devenus les
vignettes. Ce que R1.10 coûterait est écrit là, pas ici : une retouche de pixels re-scellée ne
bougerait plus l'empreinte du volume.

---

## Statut R1.4.h (1ᵉʳ septembre 2026) — Gel des archives : mode strict restauré, vérifié AVANT régénération

**Mesure préalable (annotation de check-run)** : l'étape « Gel des archives » émettait sur **chaque run
— y compris les verts** — l'avertissement `ICONOGRAPHIE.sha256 a des écarts`. Cause identifiée : le scellé
couvre `images/arbre_genealogique_complet.png` (28 maîtres), le runner régénère cet arbre **avant** le gel
(étape R1.4.b) dans une variante de rendu **légitime** (FreeType 2.13, 3 cellules/256 — mesure R1.4.b),
et la vérification après régénération comparait donc le rendu du runner au scellé du maître commité.
Le mode diagnostic (`|| echo "::warning::…"`) masquait ce faux positif **et** rendait inopérante la
détection d'une altération réelle : un scellé cassé passait inaperçu, la CI restait verte.

**Correctif (R1.4.h)** :
- `sha256sum --check --quiet` restauré sur `gouvernance/ARCHIVE.sha256` et `gouvernance/ICONOGRAPHIE.sha256` — **un écart fait échouer le run** ;
- étape **déplacée en tête de chaîne** (après `py_compile`, avant toute régénération) : elle valide l'arbre
  de travail **tel que commité**, ce qui est le contrat du gel (E-18) ;
- sans `|| echo`, `sha256sum` imprime déjà l'écart complet dans le log — le silence n'est plus payé d'aveuglement.

**Ce que le gel ne fait pas** : il ne compare pas le rendu régénéré (les variantes légitimes du runner sont
régies par `empreinte_arbre.py`, étape bloquante, R1.4.b). Le scellé protège les octets commités ; l'empreinte
sémantique protège le contenu régénéré. Les deux contrats sont désormais **tous deux bloquants**.

**R1.4.h livré par anticipation de R1.4.a–g** : le durcissement du gel est orthogonal à la
non-reproductibilité binaire (il ne compare que des fichiers statiques, machine-indépendants), il n'y avait
donc rien à attendre.

**Observation (hors R1.4)** : les annotations de run signalent la dépréciation de Node.js 20 (`actions/checkout@v4`,
`actions/setup-python@v5`, `actions/upload-artifact@v4` forcés sur Node 24 — [changelog GitHub, 19 sept. 2025](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)).
À surveiller pour la mise à jour des actions (aucune action requise aujourd'hui).

---

## Mémoire : pourquoi ces étapes étaient tolérantes (état du 1ᵉʳ septembre 2026)

Le pipeline repose sur le postulat que **les binaires régénérés doivent être identiques au bit près à ceux trackés dans git** (sinon `git diff --exit-code` échoue et la CI devient rouge). C'est une garantie forte, mais elle n'est **pas tenable** dans la situation actuelle, pour les raisons suivantes.

### Cause racine : non-reproductibilité multi-machines

Les artéfacts régénérés (Atlas SVG/PNG/HTML, Arbre PNG, Hymne WAV, PDF encyclopédique) sont **reproductibles par run** sur une même machine — deux invocations successives sur la même machine donnent le même SHA. Mais ils ne sont **pas garantis bit-à-bit identiques** entre machines :

| Machine | Pillow | ReportLab | Système | SHA des artéfacts |
|---|---|---|---|---|
| Agent Arena (Linux, dev) | 12.3.0 | 5.0.1 | Ubuntu 24.04 | `d2acccea…` (Atlas SVG) |
| Runner GitHub Actions (Ubuntu 24.04) | 12.3.0 | 5.0.1 | Ubuntu 24.04 | `84463bc9…` (Atlas SVG) |
| MacOS du mainteneur (théorique) | ? | ? | Darwin | inconnu |

Les causes précises (à investiguer en R1.4) sont probablement :

> **Post-scriptum du 1ᵉʳ septembre 2026** : les causes 1, 2, 5 et 6 se sont résolues sans
> être investiguées — la charge sémantique les ignore par construction (on ne compare
> plus les octets). 3 et 4 étaient déjà traitées par `pdf_fingerprint.py` depuis R1.1,
> pour le seul artéfact où l'empreinte avait été pensée d'emblée comme sémantique.

1. **Métadonnées EXIF des PNG** — Pillow écrit la date de génération dans le PNG
2. **Ordre des éléments dans le SVG** — selon l'ordre d'itération d'un `set` ou `dict`
3. **Noms `FormXob.*` aléatoires** dans le PDF — ReportLab ne le contrôle pas (`rl_config.invariant=1` testé sans effet, cf. R0.1)
4. **Paddings de blocs dans ReportLab** — sensibles à la largeur de police, qui dépend du système
5. **Header RIFF du WAV** — possible timestamp
6. **Compression WebP des vignettes** — paramètres par défaut de Pillow

**Important** : la situation est **identique sur la machine de l'agent et sur le runner CI** (mêmes versions épinglées dans `requirements.txt`). La différence provient probablement de l'ordre de génération de Pillow ou de l'environnement système (locale, timezone, polices chargées par défaut par Pillow).

---

## État des sept artéfacts régénérés (au 1ᵉʳ septembre 2026)

| Étape | Binaire | Contrat | Statut | Ticket |
|---|---|---|---|---|
| Atlas géographique | `sources/carte_royaume.svg`, `geographie/carte_royaume.png`, `geographie/index.html` | charge composée `svg\|html\|taille\|mode\|16x16box\|encre` | ✅ **bloquant**, empreinte appelée en CI | R1.4.a-v3 — livré |
| Arbre généalogique | `images/arbre_genealogique_complet.png` | `size\|mode\|16x16box\|ink`, variantes gravées | ✅ **bloquant** | R1.4.b — livré |
| Hymne national | `audio/hymne_national_babberland.wav` | `frames\|rate\|bits\|chan\|profil\|pcm8\|crete` + audit RIFF | ✅ **bloquant** | R1.4.c — livré |
| Vignettes du portail | `images/vignettes/*.webp` (77 fichiers) | `nb\|largeur\|grilles` sur contenu décodé (poids signalé, non contracté) | ✅ **bloquant** | R1.4.d — livré |
| Régénération encyclopédie | `Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf` | (aucune comparaison : l'étape produit) | ✅ **bloquant** sur échec du générateur | R1.4.e — livré |
| Artéfact publié (planches) | dérivée du PDF | pages, flux, légendes, appariement | ✅ **bloquant** | R1.4.f — livré |
| Fraîcheur du PDF | dérivée de l'empreinte sémantique | `pdf_fingerprint.txt` (+ `texte` comparé) et variantes `PDF CANONIQUE` | ✅ **bloquant**, variante du runner gravée sur mesure | R1.4.g — livré ; R1.10 déclarée |

**Aucune des 19 étapes du workflow ne porte plus `continue-on-error`** (18 à la clôture
de R1.4 ; la parité modèle ↔ installé de R1.8 fait la 19ᵉ, bloquante d'emblée). Le durcissement
a une contrepartie, déclarée : la chaîne peut désormais être rouge pour un rendu
d'environnement. La procédure est la même pour les sept artéfacts — lire l'annotation
(`charge=… connue=NON`), juger si la composante fautive est du bruit ou du contenu, puis
`--accepter` (rendu) ou régénérer et re-graver (contenu). Deux poussées par
changement de contenu : c'est le prix, connu, de l'assentiment double-machine.

**Et pour que la tolérance ne revienne pas par l'usure** : le workflow `batterie.yml`
exécute la batterie de mutations à horaire (lundi 03:17 UTC) et à la demande
(`workflow_dispatch`), et vérifie après coup que l'arbre de référence est resté intact.
Un contrôle émasculé — la classe C-01, qui avait survécu à quatre audits — ne survivra
pas à une semaine.

---

## Pourquoi pas comparer bit-à-bit ?

**Comparaison bit-à-bit** (la stratégie naïve `git diff --exit-code`) impose une coïncidence parfaite entre la machine qui a généré les maîtres commités et toutes les machines qui les régénèrent ensuite. C'est :

- **Fragile** : un changement de version de Pillow (même mineur) suffit à casser
- **Coûteux** : il faudrait geler l'environnement entier (Docker image, par exemple), pas seulement les versions Python
- **Inutile** : ce qui compte pour le canon, c'est le **contenu sémantique** (texte, pages, planches, scellés), pas la disposition exacte des octets

## La bonne politique (R1.4)

Pour chaque étape, R1.4 mettra en place un **scellement sémantique** analogue à `pdf_fingerprint.py` (qui compare `md5(nb_pages ‖ texte normalisé ‖ tri(hachés des flux image))`, déjà livré en R1.1 par anticipation). Le principe :

1. **Calculer une empreinte** de l'artéfact qui ne dépend PAS de l'ordre des octets, mais de son **contenu signifiant**
2. **Stocker l'empreinte** dans `gouvernance/ARTIFACT_SIGNATURES.sha256` (à créer)
3. **Vérifier** en CI que `empreinte(généré) == empreinte(commise)` sans exiger d'égalité binaire

Pour chaque sous-ticket, le travail consiste à :
- Identifier la source de non-déterminisme (Pillow EXIF, ReportLab, etc.)
- Choisir une fonction d'empreinte sémantique qui l'ignore
- Ajouter un script `sources/empreinte_<artéfact>.py` analogue à `pdf_fingerprint.py`
- Retirer le `continue-on-error: true` et basculer sur la vérification sémantique

---

## Le « Gel des archives » : un cas à part

L'étape **« Gel des archives (G et H intacts) et des maîtres d'illustration »** est **sans** `continue-on-error: true` depuis le 30 août 2026 (cf. RAPPORT_DE_CONTRE_EXPERTISE_2026_III.md, constat E-23). Elle est passée **provisoirement en mode diagnostic** dans la livraison R0.4 finale, pour permettre de lire le diff exact sans bloquer la CI.

**Statut au 1ᵉʳ septembre 2026** : `gouvernance/ARCHIVE.sha256` valide sur la machine de l'agent. Le diagnostic en CI (run #8) a montré qu'il validait également après que les 6 régénérations eurent tourné. **L'hypothèse principale est que les 6 régénérations modifient les maîtres PNG trackés (cf. section précédente), et que le scellé `ICONOGRAPHIE.sha256` n'est pas impacté** (puisque les fichiers trackés sont restés intacts — c'est le SHA qui changeait).

**Action R1.4.h** : basculer le Gel des archives en vérification stricte (`sha256sum --check --quiet`) une fois que R1.4.a–g sont résolus.

---

## Pourquoi cette politique est honnête

Le canon du Babberland protège ce qui est **éditorialement signifiant** : les textes, les dates, les noms, les affiliations, les symboles monétaires, les planches annoncées. Le SHA exact d'un PNG intermédiaire n'en fait pas partie.

La situation est analogue à un wiki : on ne « gèle » pas un export PDF en vérifiant son MD5 — on gèle **le contenu** qu'il contient. La feuille de route l'avait anticipé (R1.1, « Empreinte sémantique ») ; R1.4 étend ce principe aux autres artéfacts.

---

*Document établi à Pabst City, le 1ᵉʳ septembre 2026, par l'agent Arena.ai (session `arena/01a05e26-babbersland`).*  
*Statut R1.4.b ajouté le même jour (session `arena/01a05f15-babbersland`) : l'Arbre est durci et bloquant via empreinte sémantique tolérante.*  
*Statuts R1.4.a-v3 et R1.4.c–g ajoutés le 1ᵉʳ septembre 2026 (session `arena/01a05f55-babbersland`) : les sept artéfacts régénérés ont un contrat sémantique en variantes acceptées, la CI les appelle tous, et **plus aucune étape n'est tolérante**. La batterie de mutations, elle, a trouvé un horaire : workflow `batterie.yml`.*  
*Statuts R1.8 et R1.9 ajoutés le 1ᵉʳ septembre 2026 (session `arena/01a05f96-babbersland`) : les deux bornes nées de la vague R1.4 sont fermées — la galerie photoréaliste est scellée (`GALERIE.sha256`, 77 lignes, vérifiée en tête de chaîne) et la parité modèle ↔ workflow installé est une étape bloquante (19ᵉ du workflow). Batterie portée à **27 scénarios** (J1bis, W1), chacun jugé par le seul mécanisme qu'il prouve.*  \n*Statut R1.3 ajouté le 1ᵉʳ septembre 2026 (session `arena/01a05fce-babbersland`) : le manifeste des livrables (`gouvernance/MANIFEST.sha256`, `make manifest`, `check_manifest.py --check`) scelle les octets du corpus canonique livré — 2026-I, la chronologie maîtresse et la source vectorielle de l'arbre — que rien ne scellait ; le PDF et les images restent délégués à leurs contrats sémantiques et à `ICONOGRAPHIE`/`GALERIE`. Étape CI bloquante dédiée ; le workflow passe de 19 à **20 étapes, 0 tolérante.***
