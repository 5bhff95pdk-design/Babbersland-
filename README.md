# Royaume du Babberland

Archives narratives et iconographiques du Royaume du Babberland.

## Référence officielle actuelle

1. **`Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf`** — encyclopédie illustrée consolidée et référence canonique autonome.
2. **`ENCYCLOPEDIE_CONSOLIDEE_2026_I.md`** — source éditoriale du volume 2026-I.
3. **`CHRONOLOGIE_MAITRESSE_1847_2026.md`** — registre chronologique détaillé, avec règnes, sources et contrôles de continuité.
4. **`images/`** — portraits, numismatique et arbre généalogique illustré.

L’édition **2026-I** intègre directement les corrections et ne nécessite aucune règle de préséance documentaire.

## Chroniques narratives (hors canon)

- `chroniques/LIVRE_I_LES_FONDATIONS.md` — *Les Chroniques de l'Ancien, Livre I : Les Fondations (1798–1889)* : histoire du premier roi racontée en sept tranches. Éléments nouveaux **proposés, non décrétés** ; toute addition au canon devra passer par décret et mise à jour de 2026-I.

## Documents archivés

- `Royaume_du_Babberland_Encyclopedie_Officielle_2026.pdf` — ancien volume 2026-G ;
- `HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md` — ancien supplément 2026-H.

Ils sont conservés pour l’historique éditorial. Pour les comparer entre eux seulement, 2026-H corrige 2026-G ; pour toute consultation actuelle, utiliser **2026-I**.

## Points de continuité fixés

- En 1984–1986, Babber le Louche est encore **prince** ; Babber II le Piscineux règne et ratifie la création de McBabber’s.
- Babber le Fou, né le jour de l’ouverture en 1986, ne participe pas à la fondation du restaurant.
- Ginette, née en 1988, hérite plus tard de la garde de la sauce ; Linéa tient ce rôle à l’origine.
- Irène des Érables, morte en 1966, ne préside pas le Babbersgate de 1991 : Colette-Pabst dirige la commission.
- Babber le Déchiré appartient à une branche collatérale issue de Babette-Marine ; Babber le Fou reste fils unique du Louche et de Linéa.
- Babber le Fou demeure premier dans l’ordre de succession ; Ti-Babber est deuxième.
- Dans « Babber VII », **VII désigne la septième génération**, pas un septième règne.

## Régénération de l’encyclopédie PDF

```bash
python -m pip install reportlab pillow
python sources/generate_encyclopedie_2026_i.py
```

Le générateur ajoute la couverture, le sommaire, les signets PDF, les en-têtes, la pagination, les tableaux et les illustrations.

## Validation de la continuité

```bash
python sources/check_continuity.py
```

Ce contrôle vérifie les titres historiques, l’ordre de succession, les sept livres, les équivalences monétaires, les dates maîtresses et tous les liens d’illustrations.

## Régénération de l’arbre

L’arbre dispose d’une maquette vectorielle éditable (`sources/arbre_genealogique_complet.svg`) et d’un générateur PNG déterministe (`sources/generate_genealogy.py`).

```bash
python -m pip install pillow
python sources/generate_genealogy.py
```
