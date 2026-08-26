# Royaume du Babberland

Archives narratives et iconographiques du Royaume du Babberland.

## Sources officielles

1. **`Royaume_du_Babberland_Encyclopedie_Officielle_2026.pdf`** — volume de référence, document 2026-G.
2. **`HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md`** — supplément 2026-H, plus récent et prioritaire pour la Génération VII, McBabber’s et les nouvelles filiations.
3. **`images/`** — portraits, numismatique et arbre généalogique illustré.

En cas d’écart narratif, l’ordre de préséance est : **2026-H > 2026-G > chroniques populaires**.

## Points de continuité désormais fixés

- En 1984–1986, Babber le Louche est encore **prince** ; Babber II le Piscineux règne et ratifie la création de McBabber’s.
- Babber le Fou, né le jour de l’ouverture en 1986, ne participe pas à la fondation du restaurant.
- Ginette, née en 1988, hérite plus tard de la garde de la sauce ; Linéa tient ce rôle à l’origine.
- Irène des Érables, morte en 1966, ne préside pas le Babbersgate de 1991 : Colette-Pabst dirige la commission.
- Babber le Déchiré appartient à une branche collatérale issue de Babette-Marine ; Babber le Fou reste fils unique du Louche et de Linéa.
- Dans « Babber VII », **VII désigne la septième génération**, pas un septième règne.

## Régénération de l’arbre

L’arbre dispose d’une maquette vectorielle éditable (`sources/arbre_genealogique_complet.svg`) et d’un générateur PNG déterministe (`sources/generate_genealogy.py`). Pour régénérer l’image publiée :

```bash
python -m pip install pillow
python sources/generate_genealogy.py
```
