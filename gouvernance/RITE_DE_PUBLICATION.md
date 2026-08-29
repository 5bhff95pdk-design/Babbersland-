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
   │ 1. ÉCRIRE│ ──> │2.CONTRÔLE│ ──> │3. COMPIL │ ──> │4.GRAVURE │ ──> │5. SCELLÉ │
   │  Source  │     │Continuity│     │ make pdf │     │Empreinte │     │ Git Tag  │
   └──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
```

### Étape 1 · Rédaction & Respect du Statut
* Tout nouvel écrit historique doit porter explicitement son statut : **Canonique** (2026-I), **Proposé** (Chroniques et Lois) ou **Archivé** (G et H).
* Aucune contradiction d'âge, de filiation ou de titre ne doit être introduite.

### Étape 2 · Contrôles Préalables
Exécuter la suite de tests sans dépendance :
```bash
python sources/check_continuity.py
python sources/check_geography.py
```

### Étape 3 · Génération des Artefacts
Compiler le volume PDF et régénérer l'arbre généalogique si modifié :
```bash
make arbre
make pdf
```

### Étape 4 · Graver l'Empreinte Sémantique
Le PDF publié est figé sémantiquement dans le contrat de fraîcheur :
```bash
make empreinte
make controle
```

### Étape 5 · Scellement et Archivage
* Si un acte modifie le canon, consigner l'Avis dans `gouvernance/REGISTRE_DES_AVIS_ROYAUX.md`.
* Mettre à jour `README.md` et `CHANGELOG.md`.
* Committer les modifications avec un message explicite respectant le formalisme de la Chancellerie.
