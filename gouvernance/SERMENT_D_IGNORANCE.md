# 🤫 LE SERMENT D'IGNORANCE
## DÉCLARATION OFFICIELLE SUR LES LACUNES VOLONTAIRES DU CANON

**Chancellerie royale · Pabst City**
**Établi sous le sceau de Sa Majesté Babber Ier le Louche et du Chancelier Luc Foster**
*Référence : RM-2026-II / Ticket R2.7*
*Édition du 30 août 2026, **refondue le 2 septembre 2026 par l'Avis royal n° 10***
*Statut : Acte d'autorité scellant les silences du registre — **7 silences jurés**, 1 fixation*

---

> « Ce que l'histoire ne dit pas n'est pas un oubli ; c'est une politesse envers le mystère. »
> — Luc Foster, Grand Archiviste

> « Encore faut-il que la politesse soit décrétée. Un oubli qu'on n'a pas choisi
> reste un oubli, même signé. »
> — Avis royal n° 10, considérant

---

## I. Préambule — ce que l'édition du 30 août promettait, et ce qu'elle tenait

Dans toute œuvre de mémoire nationale, la tentation existe de tout dater, de tout mesurer et de tout consigner jusqu'à l'indiscrétion. Le Royaume du Babberland a fait le choix constitutionnel de maintenir certaines portes entrouvertes. Ce choix est sain ; la manière dont il fut d'abord consigné ne l'était pas.

Le Serment du 30 août proclamait **cinq silences** et affirmait, au § III, que « les générateurs automatiques et les scripts de validation reconnaissent ces lacunes comme conformes au canon et rejettent toute tentative d'imposer une fixation arbitraire ». Relu le 2 septembre, ce § III se révélait trois fois trop généreux :

1. **La liste n'était pas la bonne liste.** Le Serment disait cinq ; la ROADMAP (ticket R2.7) en disait cinq autres, et la Chronologie maîtresse (§ VIII) une troisième. Les trois se recouvraient partiellement : deux lacunes figurant au Serment étaient inconnues de la Chronologie, deux lacunes de la Chronologie étaient inconnues du Serment, et aucune des trois ne mentionnait la population.
2. **La machine ne gardait pas ce que le Serment jurait.** Sur les cinq silences proclamés, deux seulement avaient un garde effectif dans `check_continuity.py` ; la première année de la Transparence brune — proclamée par les trois listes — pouvait être fixée en toutes lettres sans qu'aucun contrôle ne bronche.
3. **Un silence portait sur une chose qui n'existe pas.** Le Serment jurait de taire l'heure de la pose de la première pierre du port ; or le registre **P-1** ne consigne aucune première pierre, ni ruban, ni discours, et le Livre II des Chroniques le dit expressément (tranche 5, *Le port qui n'a pas d'inauguration*). On ne peut taire l'heure d'une cérémonie qui n'a pas eu lieu : ce n'était pas un silence du registre, c'était une invention de la Chancellerie.

Le présent Serment, refondu par l'**Avis royal n° 10**, corrige les trois points. Il est désormais le **miroir lisible** du registre `canon/silences.json` : l'un ne va plus sans l'autre, et `sources/check_silences.py` le vérifie à chaque `make controle`.

---

## II. La règle de partage

Une lacune ne se juge pas à son mystère, mais à sa **portée**.

* Elle **porte** — un âge, un rang, une durée, un trait de l'arbre officiel en dépendent → elle est **FIXÉE** par décret, portée au canon, et le contrôle en réclame l'attestation.
* Elle ne **porte** rien — aucune pièce du corpus n'en dépend → elle est **JURÉE**, et le contrôle interdit de la combler.
* Elle ne porte rien **et le fait dont on taisait la circonstance n'a pas eu lieu** → elle est **REQUALIFIÉE en silence d'inexistence** : ce que le registre tait, c'est l'événement lui-même.

**Corollaire, et c'est le cœur du présent acte : un silence juré est *borné*.** Ce qui est su est dit ; ce qui est tu est tu ; la borne est ce qui distingue le mystère du trou. Une lacune sans borne n'est pas un silence, c'est une distraction.

Enfin : **nul ne peut plus taire sans décréter.** Toute lacune nouvelle doit être inscrite au registre dans la session même qui la découvre. Une lacune non décrétée est une dette, non un mystère (art. 7 de l'Avis royal n° 10).

---

## III. Les 7 silences jurés

> Chaque silence porte un identifiant, une borne, une teneur et un garde. Le garde est
> tenu par `sources/check_silences.py` d'après `canon/silences.json` : le présent
> document n'est pas la source de la machine, il en est la lecture — et la parity
> entre les deux est vérifiée dans les deux sens.

### S1 · La naissance de Babber le Déchiré

* **Borne (ce qui est su)** — Cousin collatéral de Génération VI ; majeur attesté en 2007 ; médiateur de la Guerre des Cornichons (2007–2009).
* **Tu** — Le jour, le mois, l'année et le lieu de sa naissance. Lui-même prétend être né *« un mardi où les truites mordaient bien »*. Le registre respecte cette réponse.
* **Garde** — Aucune date de naissance, aucun lieu de naissance, aucune paire d'années, aucun âge ne peut être attaché à son nom dans 2026-I ni dans la Chronologie.

### S2 · Les porteurs intermédiaires de la branche collatérale

* **Borne** — **Quatre degrés** séparent Babette-Marine (Génération II) du Déchiré (Génération VI) : c'est la fixation **F1**, ci-après.
* **Tu** — Le nom, le sexe, les dates et le nombre de porteurs de ces degrés. Le trait pointillé vert de l'arbre officiel descend de la bande II à la bande VI **sans s'arrêter sur aucun nom** : ce n'est pas un oubli de dessin, c'est la notation graphique du silence, et il ne sera pas complété.
* **Garde** — Aucune filiation directe (fils, fille, petit-fils, neveu, descendant) ne peut être écrite entre le Déchiré et une figure nommée, hormis la branche, la lignée, la rive, le fleuve et Babette-Marine elle-même.

### S3 · La naissance et l'état civil de Roger Bontemps

* **Borne** — Adulte attesté lors de la fondation de McBabber's (1984–1986) ; greffier de la commission Colette-Pabst en 1991.
* **Tu** — Ses dates d'état civil, son âge et sa famille. Roger Bontemps n'a pas d'âge : il apparaît dès que la table est mise et que la première canette est ouverte.
* **Garde** — Aucune date ni aucun lieu de naissance, aucune paire d'années, aucun âge ne peut lui être attaché dans 2026-I ni dans la Chronologie.

### S4 · La date de la transmission de la sauce, de Linéa à Ginette

* **Borne** — Le fait est canon : Linéa garda d'abord la recette, puis la transmit à la princesse Ginette **après la majorité de celle-ci**. La recette n'a jamais été écrite.
* **Tu** — L'année, le jour et l'heure de la transmission. L'acte fut de la main et de la cuillère, non du papier ; le papier n'en garde donc rien.
* **Garde** — Aucune année ne peut figurer à portée du mot de transmission dans 2026-I ni dans la Chronologie.

### S5 · La première année de la Journée de la Transparence brune

* **Borne** — Elle se tient chaque **17 mai** ; elle est postérieure au Décret de la Sauce ouverte (1991–1993).
* **Tu** — L'année civile de la première célébration. Le canon écrit *« Chaque 17 mai, le Royaume célèbre depuis… »* : il dit la récurrence, il ne dit pas le commencement.
* **Garde** — Aucune année ne peut être attachée à la première célébration, ni par « depuis », ni par un tour de phrase équivalent. C'est le silence que les trois listes proclamaient et qu'aucune machine ne gardait : il est gardé désormais.

### S6 · Le grammage des trois aromates de la sauce royale

* **Borne** — La composition générale est connue, ainsi que le temps d'écoulement à la cuillère d'argent : **huit secondes**.
* **Tu** — Le grammage au milligramme des trois aromates. Linéa cuisinait *« à l'œil, au nez et à la quantité de frites »* ; une recette jamais écrite est la seule recette vraiment secrète.
* **Garde** — Aucune quantité chiffrée (grammes, cuillerées, pincées, millilitres) ne peut être attachée à la sauce, à la recette ou aux aromates.

### S7 · L'heure et la date de la pose de la première pierre du port

*Silence d'inexistence — requalifié par l'Avis royal n° 10, art. 5.*

* **Borne** — La pierre du quai porte une phrase de la Princesse ; le registre **P-1** consigne des ouvrages entrés en service, jamais une inauguration.
* **Tu** — Il n'y a pas d'heure à taire. Le port de Port Babette n'a eu ni première pierre solennelle, ni ruban, ni discours : les ouvrages y paraissent au registre le jour où ils servent, et pas avant. Le Serment de 2026 croyait cacher une circonstance ; le corpus, lui, nie la cérémonie. **C'est le Serment qui se trompait, et il le dit.**
* **Garde** — Aucune date ni aucune heure ne peut être attachée à une première pierre ou à une inauguration du port — la négation, elle, demeure permise, puisqu'elle est la vérité du registre.

---

## IV. La fixation

### F1 · Le nombre de degrés de la branche collatérale : quatre

* **Valeur fixée** — Le Prince Babber le Déchiré est, **au quatrième degré**, l'héritier de la branche collatérale fondée par la Princesse Babette-Marine (Génération II), dont il est le descendant en Génération VI.
* **Pourquoi fixer celui-là et pas les autres** — Parce que l'arbre officiel en dépend. Le trait pointillé traverse quatre bandes de générations : nommer un seul porteur intermédiaire obligerait à redessiner l'arbre, donc à regraver son empreinte et son manifeste. Le nombre de degrés, lui, ne se discute plus ; les noms, eux, demeurent jurés (S2).
* **Contre-épreuve** — `check_silences.py` réclame l'attestation de la fixation dans 2026-I **et** recalcule l'écart des générations dans `canon/personnages.json` : un décret qui ne serait pas écrit là où il s'applique est une opinion, un décret qui contredirait l'arithmétique est une erreur.

---

## V. Dispositif de protection

Le Serment ne promet plus : il instrumente.

| Pièce | Rôle |
|---|---|
| `canon/silences.json` | **Source unique.** Sept silences, une fixation, leurs gardes, leurs bornes. |
| `gouvernance/SERMENT_D_IGNORANCE.md` | Le miroir lisible. Aucun silence n'existe hors des deux, dans un sens comme dans l'autre. |
| `sources/check_silences.py` | Le garde. Perce-ment, attestation des fixations, rétro-contrôle arithmétique, chasse aux lacunes non décrétées. |
| `make controle` | Le garde y est branché, comme les douze autres vérifications. |
| CI `continuite.yml` | Une étape bloquante dédiée, fidèle à son modèle (R1.8). |
| `make batterie` | Deux scénarios prouvent que le garde a des dents : une date imposée à Bontemps, une année imposée à la Transparence brune. |

**Chasse aux lacunes non décrétées** (art. 7). Le garde relève, dans 2026-I et dans la Chronologie, toute formule qui avoue un manque — « non consignée », « ne précise pas », « sans en donner la date », « reste ouverte » — et exige que chacune soit couverte par un silence décrété ou par une dispense écrite au registre. Une lacune que la machine trouve et que personne n'a décrétée fait échouer le contrôle : c'est la seule façon qu'a le Royaume de ne plus se raconter d'histoires.

---

## VI. Ce que le présent Serment ne fait pas

* **Il n'annexe pas la démographie.** Le total de 7 000 âmes n'est pas une lacune du registre : c'est une proposition en instance de l'**Avis royal n° 7**. L'Avis n° 10 refuse de l'absorber — une lacune et une proposition en attente ne se soignent pas de la même manière, et les confondre est le début des dettes.
* **Il ne rouvre pas 2026-I en silence.** La fixation F1 est inscrite au canon ; le volume est réimprimé, l'empreinte regravée et le manifeste rescellé dans la même session, selon le Rite de publication. Un décret qui n'imprime pas n'a pas eu lieu.
* **Il n'interdit pas les lacunes futures.** Il exige seulement qu'elles soient décrétées, bornées et gardées dans la session qui les ouvre. Formule : *objet, borne, teneur, garde, cote.*

---

*Refondu à Pabst City le 2 septembre 2026, sans aucune hâte, par l'Avis royal n° 10.*
*Édition précédente : 30 août 2026 — cinq silences proclamés, deux gardés, une lacune inventée. Les trois fautes sont corrigées et dites.*

**« Une Pabst, une poutine, et on relaxe. »**
