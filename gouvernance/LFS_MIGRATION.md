# 📦 PASSAGE EN GIT LFS — RUNBOOK (R1.6)

**Chancellerie royale · Pabst City** — mesuré le 30 août 2026. Ce document est la procédure
complète pour sortir les binaires lourds du magasin Git, telle qu'elle est **prête à exécuter en
une commande par machine**, avec le blocage mesuré à l'appui.

---

## 1 · Ce qui pèse, au 30 août 2026

| Contenu | Fichiers | Poids | Dans la chaîne ? |
|---|---|---|---|
| `images/realistes/*.png` (galerie 2026-V) | 77 | **220,1 Mio** | Non — le portail n'affiche que les vignettes (`images/vignettes/`), les maîtres restent en lightbox |
| `images/*.png` (28 maîtres scellés + planches de chantier, arbre) | 29 | **78,2 Mio** | Oui — 24 maîtres sont embarqués dans le PDF 2026-I ; scellés par `ICONOGRAPHIE.sha256` |
| `*.pdf` (2026-I et archive 2026-G) | 2 | **22,9 Mio** | Oui — l'artéfact publié et son empreinte sémantique |
| `audio/*` (hymne WAV + 2 MP3 de récitation) | 3 | **4,0 Mio** | Oui — le WAV se régénère au bit près (`make hymne`) |
| `images/vignettes/*.webp` | 77 | **4,7 Mio** | Oui — régénérées par `make vignettes` |
| **Total candidat** | **198** | **≈ 330 Mio** | |

Le dépôt pèse ≈ 340 Mio dans son intégralité (binaires + 240 Ko de sources et de textes).

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

### Option B — LFS + réécriture de l'historique (allègement réel)

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

## 5 · Statut

**Prêt, non exécuté** : la mesure du 30 août bloque l'upload des objets depuis l'environnement
d'agent (tableau § 2). À exécuter (Option A′ ou B) depuis une machine avec accès au CDN GitHub,
après avis pour l'Option B. Quand l'environnement aura accès au CDN, `make lfs` (ci-après)
résume l'Option A′.
