# 📦 PASSAGE EN GIT LFS — RUNBOOK (R1.6)

**Chancellerie royale · Pabst City** — mesuré le 30 août 2026. Ce document est la procédure
complète pour sortir les binaires lourds du magasin Git, telle qu'elle est **prête à exécuter en
une commande par machine**, avec le blocage mesuré à l'appui.

---

## 1 · Ce qui pèse, **remesuré le 2 septembre 2026**

| Contenu | Fichiers | Poids | Dans la chaîne ? | Sort en LFS (A′) ? |
|---|---|---|---|---|
| `images/realistes/*.png` (galerie 2026-V) | **83** | **227 Mio** | Non — le portail n'affiche que les vignettes (`images/vignettes/`), les maîtres restent en lightbox | ✅ |
| `images/*.png` (maîtres scellés, planches de chantier, arbre) | **28** | **75 Mio** | Oui — embarqués dans le PDF 2026-I ; scellés par `ICONOGRAPHIE.sha256` | ❌ (art. 2) |
| `*.pdf` (2026-I et archive 2026-G) | 2 | **22 Mio** | Oui — l'artéfact publié et son empreinte sémantique | ❌ (art. 2) |
| `images/vignettes/*.webp` | **83** | **5,0 Mio** | Oui — régénérées par `make vignettes` | ✅ |
| `audio/*` (hymne WAV + 2 MP3 de récitation) | 3 | **3,7 Mio** | Oui — le WAV se régénère au bit près (`make hymne`) | ✅ |
| **Total hors `.git`** | | **334 Mio** | | **≈ 236 Mio partent** |

Le magasin `.git` pèse à lui seul **329 Mio** — c'est lui que l'Option B aurait vidé, et c'est
lui que l'Avis n° 9 choisit de laisser intact.

> *Écart avec la mesure du 30 août* : la galerie est passée de 77 à 83 clichés (+7 Mio), les
> vignettes ont suivi. Le comptage « 29 maîtres » de la première mesure était erroné : il y en
> a 28, conformément à `ICONOGRAPHIE.sha256`.

## 2 · Ce qui a été mesuré le 30 août 2026 (depuis l'environnement d'agent)

| Sonde | Résultat |
|---|---|
| `git push` (protocole git vers `github.com`) | ✅ passe (commits normaux) |
| API `api.github.com` (PR, releases, LFS batch) | ✅ passe |
| Batch LFS `POST /info/lfs/objects/batch` | ✅ **HTTP 200** — l'API LFS répond, un URL d'upload signé est émis |
| Upload d'objet LFS vers `github-cloud.s3.amazonaws.com` | ❌ **SSL_ERROR_SYSCALL** — le CDN/S3 de GitHub est inaccessible depuis cet environnement |
| Upload d'asset de Release vers `uploads.github.com` | ❌ **EOF** — idem, domaine bloqué |

**Conséquence** : depuis cet environnement, le dépôt peut recevoir des commits (pointeurs compris)
mais **aucun octet binaire ne peut rejoindre le stockage LFS ou Releases de GitHub**. Exécuter la
migration ici produirait un dépôt cassé pour tous les autres (pointeurs sans objets) : c'est
pourquoi la migration n'est **pas** engagée par cet environnement. Elle attend une machine avec
accès au CDN GitHub — ou la levée du blocage réseau.

## 3 · La migration — une commande, une machine, un avis

> **Arbitrage rendu.** L'Avis royal n° 9 (2 septembre 2026) retient la **variante A′** et écarte
> l'Option B. Les descriptions ci-dessous sont conservées pour la mémoire de l'instruction :
> seule A′ a force exécutoire.

### Option A — LFS prospectif (sans réécriture de l'historique)

Les binaires courants deviennent des pointeurs ; l'historique conserve les vieux blobs.

```bash
git lfs install
git lfs track "*.png" "*.webp" "*.pdf" "*.wav" "*.mp3"   # règle .gitattributes
git add -u .gitattributes
git commit -m "LFS : pointeurs pour les binaires (R1.6)"
git push                                                # téléverse ≈ 330 Mio d'objets
```

- **Effet** : le clone shallow (`--depth 1`) et l'interface web s'allègent immédiatement ; toute
  croissance future suit LFS. Le clone complet (historique) ne change pas.
- **Coût GitHub (plan gratuit)** : 1 Gio de stockage LFS (≈ 330 Mio, ça passe) et **1 Gio de
  bande passante par mois** — chaque exécution de la CI (18 étapes, checkout complet) téléverse
  les objets : ≈ 3 exécutions/mois au plan gratuit. Au-delà : plan payant ou étroitement
  sélectionner ce qui part en LFS (voir variante A′).
- **Variante A′ (recommandée si plan gratuit)** : LFS pour `images/realistes/` (220 Mio — hors
  chaîne, le portail n'a besoin que des vignettes) + `images/vignettes/` + `audio/` ; les 28
  maîtres scellés (78 Mio) et les 2 PDF restent en Git, où ils sont de toute façon déjà dans
  l'historique. Bande passante CI ≈ 230 Mio/exécution.

```bash
git lfs install
git lfs track "images/realistes/*.png" "images/vignettes/*.webp" "audio/*"
git add -u .gitattributes
git commit -m "LFS : galerie 2026-V, vignettes et audio hors Git (R1.6, variante A′)"
git push
```

### Option B — LFS + réécriture de l'historique (allègement réel) · ❌ **ÉCARTÉE (Avis n° 9, art. 1er)**

```bash
git lfs install
git lfs migrate import --include-ref=refs/heads/main \
  --include="images/realistes/*.png,images/vignettes/*.webp,*.pdf,audio/*,images/*.png"
git push --force origin main
```

- **Effet** : le dépôt passe de ≈ 340 Mio à **< 5 Mio** ; tout clone (même complet) devient
  léger.
- **Conditions** : réécriture de l'historique de `main` = **acte éditorial structurant**
  (toutes les branches de PR et les clones existants sont invalidés, les branches `arena/*`
  devront être rebasées ou abattues) ; à décider par avis, comme tout ce qui touche aux
  archives. Les scellés `sha256` (ARCHIVE, ICONOGRAPHIE) et l'empreinte sémantique du PDF sont
  **fondés sur le contenu**, pas sur l'historique : ils restent valables après migration
  (à rejouer par `make scelle` et `make controle` post-push, comme tout acte de publication).

## 4 · Ce qui ne change pas pour la chaîne

- `make tout`, `make controle`, `make batterie` : la chaîne lit les **fichiers du répertoire de
  travail** ; un clone avec `git lfs install` (+ `git lfs pull` automatique au checkout) les
  matérialise avant le moindre contrôle. La CI (actions/checkout@v4) matérialise les objets LFS
  par défaut — aucune modification du gabarit.
- Les scellés par haché de contenu (`gouvernance/*.sha256`, `pdf_fingerprint.txt`) sont
  insensibles au transport Git vs LFS.
- Le portail : vignettes en grille, maîtres en lightbox — inchangé.

## 5 · Statut — **décrété le 2 septembre 2026 (Avis royal n° 9)**

Le runbook n'est plus une hypothèse : la Chancellerie a tranché.

| | |
|---|---|
| **Option retenue** | **A′** — LFS pour `images/realistes/*.png`, `images/vignettes/*.webp`, `audio/*` |
| **Option écartée** | **B** — la réécriture de l'historique de `main` est refusée (Avis n° 9, considérant 3 et art. 1er) : le passé du Royaume ne se réécrit pas, fût-ce pour gagner 325 Mio |
| **Restent en Git** | les 28 maîtres scellés et les 2 PDF (art. 2) |
| **Plafond de poids** | aucun, délibérément (art. 6) |
| **Exécution** | **en attente d'une machine** ayant accès au CDN GitHub |

### Pourquoi ce n'est toujours pas exécuté

Mesure **reconduite le 2 septembre 2026** depuis l'environnement d'agent, identique à celle du
30 août :

```
api.github.com                      → 200
github-cloud.s3.amazonaws.com:443   → SSL_ERROR_SYSCALL
uploads.github.com:443              → SSL_ERROR_SYSCALL
git-lfs                             → absent de l'environnement
```

Le blocage n'a pas bougé. Y engager la migration téléverserait des **pointeurs sans objets** :
un dépôt intact pour l'agent, en ruine pour tous les autres. L'art. 3 de l'Avis n° 9 en fait
donc une **défense expresse**, et l'art. 4 interdit d'inscrire par avance le moindre filtre LFS
à `.gitattributes` — un filtre posé sans téléversement possible transforme le prochain commit
binaire en pointeur orphelin. `.gitattributes` reste donc à ses deux lignes `binary`.

### La commande, le jour venu

Sur une machine avec `git-lfs` et l'accès au CDN, depuis un clone à jour :

```bash
make lfs        # = git lfs install + track (A′) + commit de .gitattributes
git push        # téléverse ≈ 232 Mio d'objets
make controle   # rejoué après publication, comme tout acte de la chaîne
```

Puis consigner l'exécution en § 5 et au registre, sous l'Avis n° 9.
