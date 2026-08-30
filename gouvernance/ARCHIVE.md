# 🗄️ POLITIQUE D'ARCHIVAGE DU ROYAUME DU BABBERLAND

**Référence** : GOU-2026-II-01 · complémentaire du rapport `RAPPORT_ANALYSE_2026_II.md` (constats E-12, E-13)
**Liste de contrôle machine** : `gouvernance/ARCHIVE.sha256` — vérifiée à chaque push par la CI

## Principe

Un document **changé d'état** (une édition remplacée par une consolidation) devient une **archive close** : il ne se corrige plus. Il reste consultable, il reste prouvable, il ne bouge plus.

Cette règle répond à un risque propre au projet : l'édition consolidée 2026-I reprend **95 % des lignes narratives du supplément 2026-H** (mesure : 155 des 164 lignes longues). Deux textes éditables racontent donc la même histoire. Sans gel, une retouche d'un seul côté créerait une divergence que plus rien ne signalerait — et le statut même d'archive, qui est la garantie que l'on peut comparer un état antérieur à l'état canonique, deviendrait une simple déclaration d'intention.

## Décision éditoriale ultérieure : Livre II

Le même principe a permis de documenter, sans la prolonger, la coexistence temporaire de deux rédactions du Livre II : *Les Bâtisseurs* et *Le Silence et l'Aqueduc*. Cette coexistence appartient désormais à l'historique de travail, non à l'état éditorial courant. Le **30 août 2026**, les deux textes ont été fusionnés dans `chroniques/LIVRE_II_LES_BATISSEURS.md`, qui porte seul le titre *Livre II — Les Bâtisseurs*, le sous-titre *Le Silence et l'Aqueduc* et le compte retenu de **quarante-deux bancs**.

Le fichier de travail `chroniques/LIVRE_II_LE_SILENCE_ET_L_AQUEDUC.md` a été intégré puis supprimé ; Git conserve la trace de cette étape, mais aucun document courant ne doit le traiter comme une version concurrente. Cette résolution éditoriale ne constitue pas une ratification canonique du Livre II : elle signifie seulement qu'aucun futur Avis n'aura à choisir entre deux rédactions.

## Documents actuellement scellés

| Document | Rôle | Scellé parce que |
|---|---|---|
| `Royaume_du_Babberland_Encyclopedie_Officielle_2026.pdf` (2026-G) | État antérieur à la proclamation de Ti-Babber : six générations, Série B, visite de 1980 | **Aucune source ni générateur ne correspondent à ce volume dans le dépôt** : il est régénérable par rien. Le haché est la seule preuve d'intégrité disponible (E-12). |
| `HISTOIRE_OFFICIELLE_ET_GENEALOGIE_REVISEE_2026.md` (2026-H) | Supplément extraordinaire du 26 août 2026 : Génération VII, filiation du Déchiré, McBabber's corrigé, série métallique | Tout son contenu utile est passé dans 2026-I ; son en-tête porte déjà son statut archivistique. Le gel évite la double édition (E-13). |

## Ce qui n'est PAS gelé

- `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md` — **la** référence courante : elle se corrige, et `make pdf` produit alors un nouveau volume légitime.
- `CHRONOLOGIE_MAITRESSE_1847_2026.md` — registre de travail des dates, aligné sur 2026-I.
- `chroniques/` — hors canon, par nature ouvert (bandeau « proposés, non décrétés »).
- Les illustrations et les scripts.

## Dégeler : la procédure

Retirer une ligne de `ARCHIVE.sha256` exige, **dans le même commit** :

1. un **Avis du Grand Argentier** numéroté, motivant la substitution (quel document remplace lequel, et pourquoi l'archive écartée mérite d'être consultée plus tard) ;
2. la mise à jour de la table des documents archivés du `README.md` ;
3. l'ajout du nouveau document à la liste des scellés, avec son haché.

Le but n'est pas la bureaucratie : c'est que l'historique Git reste lisible comme une suite d'actes, et qu'une correction ne puisse pas se déguiser en coquille. Tant que l'Avis n'existe pas, `sha256sum --check` est censé échouer — c'est le signal, pas un accident.

## Vérification

```bash
sha256sum --check gouvernance/ARCHIVE.sha256      # les archives sont intactes
make controle                                      # continuité, artefact, empreinte
```
