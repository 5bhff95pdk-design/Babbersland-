# 🕯️ LE RITE DE PUBLICATION DE LA CHANCELLERIE
## PROCÉDURE STANDARDISÉE D'INCORPORATION CANONIQUE (Ticket R3.6)

**Chancellerie royale · Pabst City**  
**Guide opérationnel à l'usage des scribes et des agents automatisés**

---

> « Toute parole royale mérite cinq étapes de vérification avant de devenir parchemin. »  
> — Luc Foster, Chancelier

---

## Les Cinq Étapes du Rite

```
   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ 1. ÉCRIRE│ ──> │2.CONTRÔLE│ ──> │3.COMPILER│ ──> │4.VÉRIFIER│ ──> │ 5.GRAVER │
   │  Source  │     │ Sources  │     │make pdf  │     │controle  │     │ + SCELLER│
   └──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
```

> **L'ordre est un contrôle, pas une commodité** (constat E-21 de RC-2026-III-01) : graver
> l'empreinte *avant* de la vérifier rend la vérification infaillible par construction.
> La gravure ferme donc le rite ; elle ne l'ouvre plus.

### Étape 1 · Rédaction & Respect du Statut
* Tout nouvel écrit historique doit porter explicitement son statut : **Canonique** (2026-I), **Proposé** (Chroniques et Lois) ou **Archivé** (G et H).
* Aucune contradiction d'âge, de filiation ou de titre ne doit être introduite.
* Une donnée nouvelle qui ne figure pas dans 2026-I s'inscrit dans `propositions_declarées` de son fichier de `canon/` (contrat de parité, `check_canon.py`).

### Étape 2 · Contrôles préalables (sources)
```bash
python sources/check_continuity.py    # canon, chronologie, chroniques, ancres, cinq silences
python sources/check_canon.py         # parité des données JSON · arithmétique des successions
python sources/check_geography.py     # atlas contre canon, anachronismes datés
```

### Étape 3 · Génération des Artefacts
```bash
make arbre                            # PNG généalogique, déterministe au bit près
make pdf                              # volume 2026-I
make iconographie                       # nouveaux maîtres seulement : re-sceller les maîtres
```

### Étape 4 · Vérification de l'artéfact — sans rien graver
```bash
make controle                         # six contrôles : sources, données, PDF, fraîcheur,
                                      # géographie, scellés (archives G/H + maîtres d'illustration)
```
`check_pdf.py` apparie **planche à légende, page à page** : une image perdue, déplacée ou
ajoutée sans promesse du canon fait échouer cette étape (constats E-18, E-22).

### Étape 5 · Gravure, scellement et archivage
* Si, et seulement si, `make controle` est vert : `make empreinte` grave le contrat de fraîcheur.
* **Et `make manifest` re-grave le manifeste des livrables (R1.3)** — dès que le TEXTE du canon
  change, pas seulement quand on touche aux images. Trouvé le 2 septembre 2026 en rejouant la
  batterie : les scénarios légitimes V2 et R1 réimprimaient le volume et re-gravaient l'empreinte
  **sans** re-graver le manifeste, et échouaient depuis l'entrée de `check_manifest.py` dans la
  chaîne. Un rite qui oublie une gravure n'est pas un rite allégé : c'est un rite faux.
* Empreinte, manifeste ou scellé modifié = acte assumé : le consigner à l'Avis dans
  `gouvernance/REGISTRE_DES_AVIS_ROYAUX.md`.
* **Réimpression du volume = variante CI périmée** : la charge du PDF dépend du texte. Après
  `make empreinte`, le runner refusera au premier run ; on lit son annotation et l'on accepte la
  charge à la main (`pdf_fingerprint.py --accepter '<charge>' <étiquette>`). Deux poussées par
  changement de contenu : le prix connu de R1.4.g tant que R1.2 n'existe pas.
* Mettre à jour `README.md` et `CHANGELOG.md`, committer, puis reposer l'étiquette `v2026-…` et publier la Release (R1.5).
