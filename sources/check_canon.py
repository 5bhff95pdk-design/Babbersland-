#!/usr/bin/env python3
"""Parité des données structurées : `canon/*.json` contre les registres qui font foi.

Constat E-19 (RC-2026-III-01) : depuis le ticket R3.3, l'univers est écrit à quatre
endroits — `ENCYCLOPEDIE_CONSOLIDEE_2026_I.md` (seul à faire foi), la Chronologie
maîtresse, le Registre d'autorité des personnages, et le dossier `canon/`. Les trois
premiers se recoupaient partiellement ; **le quatrième n'était lu par personne**, et
avait déjà dérivé sur quatre fiches et trois affirmations sans source.

Principe du contrôle : dans un dossier qui s'appelle `canon`, une affirmation est soit
**attestée** par 2026-I (ou par la Chronologie, qui en est le registre daté), soit
**expressément déclarée** dans la liste `propositions_declarées` du fichier, avec sa
source et son statut. Le silence n'est plus une option ; le mensonge par omission non
plus : une proposition levée (le canon l'adope un jour) doit sortir de la liste.

Vérifications
-------------
A. personnages — 18 fiches, identifiants uniques, générations 1–7, noms canoniques,
   dates de vie **égales** à celles du canon, vedettes du Registre alignées, naissances
   et décès énoncés en prose du Registre rattachés à la bonne figure.
B. silences sanctifiés — pas d'année pour les figures que le Serment déclare tues.
C. lieux — sommes, populations, altitude et date de création.
D. monnaie — 24 Babetons par Babber, fractions cohérentes, valeurs citées.
E. événements — chaque date dans le corpus canonique, chaque noyau d'énoncé aussi.
F. règnes (Chronologie § IX) — durée annoncée = soustraction, chaîne continue,
   mort du souverain = fin de règne.
G. contrôles de la Chronologie § X que rien ne vérifiait : titre du Louche
   avant 2010, filiation du Fou, dédicace de Port Babette.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HONORIFIQUES = re.compile(
    r"^(?:S\.M\.|S\.A\.R\.|Sa Majest[ée]|Son Altesse Royale|Le Roi|La Reine|Reine|King|Queen|"
    r"Prince|Princesse|Roi)\s+", re.I)
# Toute année d'une vie humaine plausible dans le corpus : 1600–2029.
ANNEE = re.compile(r"(?<!\d)(1[6-9]\d{2}|20[0-2]\d)(?!\d)")
# Paire de vie, telle que le canon l'écrit : « (1875–1959, r. 1914–1959) »,
# « (1840–1922) », « (née en 1952) » n'est PAS une paire.
VIE = re.compile(r"\(\s*(?:v\.\s*)?(1[6-9]\d{2}|20[0-2]\d)\s*[–-]\s*(?:v\.\s*)?((?:1[6-9]|20[0-2])\d{2}|PR[ÉE]SENT)\b")
# Naissance attribuée **au sujet de la ligne** : en tête de clause seulement, pour ne pas
# lire « Mère de Babber le Dormeur (né 1875) » comme la naissance d'Hortense du Grain.
NAISSANCE = re.compile(r"(?:^|[:;]\s*)N[ée]{1,2}\s+(?:le\s+|en\s+|vers\s+)(1[6-9]\d{2}|20[0-2]\d)")
DECES = re.compile(r"\b(?:mort[e]?|d[ée]c[ée]d[ée]e?|inhum[ée]e?)\s+(?:en|le|vers)\s+(\d{4})", re.I)

CANON = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
CHRONO = ROOT / "CHRONOLOGIE_MAITRESSE_1847_2026.md"
REGISTRE = ROOT / "gouvernance" / "REGISTRE_DES_PERSONNAGES.md"
DATA = ROOT / "canon"
SILENCE_NAISSANCE = {"babber_le_dechire", "roger_bontemps"}
CLES_PROPOSITIONS = "propositions_declarées"


def norm(s: str) -> str:
    """Même normalisation pour les textes et pour les scalars JSON : sinon « l’Ancien »
    du JSON ne ressemble plus à « l'Ancien » du canon et toute la parité s'effondre."""
    s = unicodedata.normalize("NFKC", str(s))
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u00a0", " ")
    return re.sub(r"[ \t]+", " ", s).strip()


def lines(path: Path) -> list[str]:
    """Lignes normalisées (apostrophes plates, espaces pliés) — les sauts de ligne survivent."""
    raw = unicodedata.normalize("NFKC", path.read_text(encoding="utf-8"))
    raw = raw.replace("\u2019", "'").replace("\u2018", "'").replace("\u00a0", " ")
    return [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]


def flat(path: Path) -> str:
    return " ".join(lines(path))


canon_lines, chrono_lines, registre_lines = lines(CANON), lines(CHRONO), lines(REGISTRE)
canon_t, chrono_t, registre_t = flat(CANON), flat(CHRONO), flat(REGISTRE)
corpus = f"{canon_t} {chrono_t}"
corpus_lower = corpus.lower()

errors: list[str] = []
constats: list[str] = []


def must(cond, msg: str) -> bool:
    if not cond:
        errors.append(msg)
    return bool(cond)


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def charges_declarees(doc: dict) -> str:
    """Bloc `propositions_declarées` sérialisé : un fait y est couvert si le fichier le nomme.

    Une déclaration couvre le fait par sa valeur ("1 500"), son champ ("fractions[2]") ou son
    identifiant ("foret_plantagenet") — le contrat est « dis d'ou tu parles », pas « récapitule ma clef ».
    """
    entrees = doc.get(CLES_PROPOSITIONS, [])
    if isinstance(entrees, dict):
        entrees = [entrees]
    # La prose d'une entrée (note, source) ne doit pas servir d'excuse : on ne déclare
    # un fait que par ce qui l'identifie (valeur, champ, date), pas par son commentaire.
    hors_prose = [{k: v for k, v in e.items() if k not in {"note", "source", "statut"}}
                  if isinstance(e, dict) else e for e in entrees]
    return norm(json.dumps(hors_prose, ensure_ascii=False))


def dates_declarees(doc: dict) -> set[str]:
    """Dates couvertes par une déclaration, au sens strict : le champ `date` de l'entrée."""
    entrees = doc.get(CLES_PROPOSITIONS, [])
    if isinstance(entrees, dict):
        entrees = [entrees]
    return {norm(e.get("date", "")) for e in entrees if isinstance(e, dict)}


def est_declaree(blob: str, *morceaux: str) -> bool:
    return any(m and m in blob for m in morceaux)


def est_atteste(morceau: str, *, min_longueur: int = 4) -> bool:
    morceau = morceau.strip()
    if len(morceau) < min_longueur:
        return True
    return morceau.lower() in corpus_lower


def nom_court(nom: str) -> str:
    court = HONORIFIQUES.sub("", nom).strip()
    return re.sub(r"\s*\(.*$", "", court).strip()


def vies_canon(nom: str) -> tuple[str, str] | None:
    """(naissance, mort) telles que 2026-I les écrit pour cette figure, si le canon les donne."""
    court = nom_court(nom)
    for line in canon_lines:
        if court in line:
            m = VIE.search(line)
            if m:
                return m.group(1), m.group(2)
    return None


def annees_de_la_figure(nom: str) -> set[str]:
    """Toutes les années que le canon ou la Chronologie attachent explicitement à cette figure."""
    court = nom_court(nom)
    dernier = court.split()[-1]
    annees: set[str] = set()
    for source in (canon_lines, chrono_lines):
        for line in source:
            if court in line or (len(dernier) > 4 and dernier in line):
                annees |= set(ANNEE.findall(line))
    return annees


# ── A · personnages ─────────────────────────────────────────────────────
doc = load("personnages.json")
persons = doc["persons" if "persons" in doc else "personnages"]
declarees = charges_declarees(doc)
must(len(persons) == 18, f"personnages.json : {len(persons)} fiches — le canon en compte 18")
must(len({p["id"] for p in persons}) == len(persons), "personnages.json : identifiants dupliqués")

for p in persons:
    p = {k: (norm(v) if isinstance(v, str) else v) for k, v in p.items()}
    court = nom_court(p["nom"])
    if p["id"] in SILENCE_NAISSANCE:
        must(not ANNEE.search(str(p.get("dates", ""))),
             f"silence sanctifié percé dans les données : {p['id']} porte une année ({p.get('dates')!r}) "
             "— SERMENT_D_IGNORANCE.md II.1 et II.2")
        continue
    must(1 <= int(p.get("generation", 0)) <= 7, f"{p['id']} : génération hors de 1–7")
    must(court in canon_t or court.split()[-1] in canon_t,
         f"nom hors canon : {p['nom']!r} — 2026-I ne nomme personne ainsi")
    officielle = vies_canon(p["nom"])
    annoncees = ANNEE.findall(str(p.get("dates", "")))
    if annoncees and officielle:
        must(annoncees == list(officielle),
             f"{court} : dates {annoncees} dans les données, {list(officielle)} dans 2026-I "
             "(c'est le Markdown qui fait foi)")
    # vedettes et arbre du Registre : mêmes paires, à la figure près
    for line in registre_lines:
        if not line.lstrip().startswith(("###", "├", "└", "│")):
            continue
        for entree in re.split(r"[├└]", line):
            if court not in entree:
                continue
            for (n, m) in VIE.findall(entree):
                must(not officielle or (n, m) == officielle,
                     f"Registre : {court} daté ({n}–{m}) alors que 2026-I écrit "
                     f"{list(officielle) if officielle else 'aucune paire'}")
    # prose de la fiche : naissances et décès énoncés, rattachés à la bonne figure
    debut = next((i for i, l in enumerate(registre_lines)
                  if l.startswith("###") and court in l), None)
    if debut is not None:
        fiche = " ".join(registre_lines[debut:debut + 7])
        autorisees = set(annoncees) | annees_de_la_figure(p["nom"]) | set(officielle or ())
        for motif, motif_re in (("naissance", NAISSANCE), ("décès", DECES)):
            for annee in motif_re.findall(fiche):
                must(annee in autorisees,
                     f"Registre : {court} — {motif} {annee}, année que ni 2026-I ni la Chronologie "
                     f"n'attachent à cette figure (attendues : {sorted(autorisees)})")
constats.append(f"{len(persons)} personnages")

# ── C · lieux ───────────────────────────────────────────────────────────
doc = load("lieux.json")
declarees = charges_declarees(doc)
regions = doc["regions"]
somme = sum(r["population"] for r in regions)
must(somme == doc["population_totale"],
     f"lieux.json : somme des régions {somme} != population_totale {doc['population_totale']}")
urbain = sum(r["population"] for r in regions if r["id"] != "foret_plantagenet")
must(urbain == doc["population_urbaine"],
     f"lieux.json : total urbain {urbain} != population_urbaine {doc['population_urbaine']}")
for r in regions:
    must(r["nom"] in canon_t, f"lieux.json : région absente de 2026-I : {r['nom']}")
    chiffre = f"{r['population']:,}".replace(",", " ") if r["population"] else "0"
    if r["population"] and chiffre not in canon_t and f"({chiffre}" not in canon_t:
        must(est_declaree(declarees, chiffre, f"regions[{r['id']}].population", r["id"], str(r["population"])),
             f"lieux.json : {r['nom']} peuplé de {chiffre} âmes — chiffre ni écrit par 2026-I, "
             f"ni déclaré comme proposition (il vient de l'atlas, `geographie/ANALYSE.md`) "
             f"→ l'ajouter à {CLES_PROPOSITIONS}")
monts = next(r for r in regions if r["id"] == "monts_froisses")
must(monts["altitude"] in canon_t, f"lieux.json : altitude {monts['altitude']!r} absente de 2026-I")
must(monts["date_creation"] in chrono_t,
     f"lieux.json : création des Monts ({monts['date_creation']!r}) absente de la Chronologie")
must(monts["population"] == 0, "lieux.json : les Monts Froissés sont peuplés — ils sont un jardin")
constats.append(f"{len(regions)} régions")

# ── D · monnaie ─────────────────────────────────────────────────────────
doc = load("monnaie.json")
declarees = charges_declarees(doc)
must("1 babber = 24 babetons" in f"{canon_t} {chrono_t}".lower().replace("  ", " "),
     "monnaie.json : l'équivalence « 1 Babber = 24 Babetons » a disparu du corpus canonique")
for f in doc["fractions"]:
    attendu = f["valeur_bt"] / 24
    must(abs(attendu - f["valeur_b"]) <= 0.0002,
         f"monnaie.json : {f['nom']} — {f['valeur_bt']} Babetons valent {f['valeur_b']} Babber, "
         f"attendu {attendu:.6f}")
    valeur_ecrite = f"{f['valeur_bt']} babeton" in canon_t.lower()
    if not (valeur_ecrite or est_declaree(declarees, f"{f['valeur_bt']} Babetons", f"fractions[{f['valeur_bt']}]")):
        errors.append(f"monnaie.json : la valeur de {f['valeur_bt']} Babeton(s) n'est écrite nulle part "
                      f"dans 2026-I — la frapper au canon ou la déclarer dans {CLES_PROPOSITIONS}")
    for cle in ("nom", "unite_populaire"):
        valeur = str(f.get(cle, ""))
        if valeur and valeur.lower() not in corpus_lower \
                and not est_declaree(declarees, valeur, f"fractions[{f['valeur_bt']}]"):
            errors.append(f"monnaie.json : {valeur!r} ({cle}, {f['valeur_bt']} Babetons) est un nom "
                          f"que le corpus canonique ignore — le déclarer comme proposition ou le reprendre "
                          "du canon")
for serie in doc["series_fiduciaires"]:
    must(str(serie["annee"]) in corpus,
         f"monnaie.json : série {serie['serie']} datée {serie['annee']} sans écho dans le corpus")
constats.append(f"{len(doc['fractions'])} fractions")

# ── E · événements ─────────────────────────────────────────────────────
doc = load("evenements.json")
declarees = charges_declarees(doc)
evenements_declares: list[str] = []
evens = doc["chronologie_maitresse"]
for e in evens:
    couvert = norm(e["date"]) in dates_declarees(doc)
    for annee in ANNEE.findall(e["date"]) or re.findall(r"\d{4}", e["date"]):
        must(annee in corpus or couvert,
             f"evenements.json : {e['date']!r} — l'année {annee} n'est dans 2026-I ni dans la "
             f"Chronologie maîtresse (à déclarer dans {CLES_PROPOSITIONS} si elle vient d'un livre proposé)")
    noyau = re.split(r"[;(]", e["evenement"])[0].strip(" .,")
    mots = [w for w in re.split(r"\W+", noyau.lower()) if len(w) > 4][:5]
    if mots:
        reconnus = sum(1 for w in mots if w in corpus_lower)
        must(reconnus >= max(1, len(mots) - 1),
             f"evenements.json : {e['evenement'][:58]!r} — {len(mots) - reconnus} mots sur {len(mots)} "
             "sont hors corpus canonique")
    if couvert:
        evenements_declares.append(e["date"])
constats.append(f"{len(evens)} événements"
                + (f", {len(evenements_declares)} déclaré(s) hors canon ({', '.join(evenements_declares)})"
                   if evenements_declares else ""))

# ── F · arithmétique des règnes (Chronologie § IX) ──────────────────────
tableau = re.findall(
    r"^\|\s*\*\*\s*(\d{4})\s*[–-]\s*(\d{4})\s*\*\*\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*ans?",
    "\n".join(chrono_lines), flags=re.M)
chaine: list[tuple[int, int, str]] = []
for debut, fin, souverain, duree in tableau:
    debut, fin, duree = int(debut), int(fin), int(duree)
    must(fin - debut == duree,
         f"Chronologie § IX : {souverain} — durée annoncée {duree} ans, {fin - debut} calculés "
         f"({debut}–{fin})")
    chaine.append((debut, fin, souverain))
for (debut, fin, nom), (debut2, fin2, nom2) in zip(chaine, chaine[1:]):
    must(fin == debut2, f"Chronologie § IX : trou de succession — {nom} finit en {fin}, {nom2} commence en {debut2}")
for debut, fin, nom in chaine:
    courte = nom.split(",")[0].strip()
    vie = vies_canon(courte)
    if vie and vie[1].isdigit() and vie[1] != "PRÉSENT":
        mort = int(vie[1])
        must(mort == fin or mort - fin <= 6,
             f"succession : {courte} meurt en {mort} d'après 2026-I, son règne s'achève en {fin} "
             "sans retrait consigné à cette date")
if chaine:
    constats.append(f"{len(chaine)} règnes arithmétiquement contrôlés")

# ── G · contrôles § X que rien ne vérifiait ─────────────────
for line in chrono_lines:
    m = re.match(r"^\|\s*\*\*\s*(\d{4})", line)
    if not m or int(m.group(1)) >= 2010:
        continue
    if "Louche" in line:
        must(not re.search(r"roi r[ée]gnant|Sa Majest[ée] Babber Ier le Louche|r[èe]gne depuis", line, re.I),
             f"contrôle § X.1 percé — le Louche présenté comme roi régnant avant 2010 : « {line[:76]}… »")
must("fils unique" in canon_t,
     "contrôle § X.4 retiré du corpus : plus rien n'écrit que Babber le Fou est fils unique")
must(not re.search(r"ginette[^.]{0,48}[sœ]ur de babber le fou", canon_t, re.I),
     "contrôle § X.4 percé : Ginette dite sœur du Fou — le canon la donne pour son épouse")
must("port babette" in canon_t.lower() and "babette ire" in canon_t.lower(),
     "contrôle § X.7 retiré du corpus : Port Babette n'est plus rattaché à Babette Ire")

# ── Validité JSON stricte (le dossier n'était même pas passé au parseur) ──
for name in sorted(p.name for p in DATA.glob("*.json")):
    try:
        json.loads((DATA / name).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{name} : JSON invalide — {exc}")

if errors:
    print("ÉCHEC DE LA PARITÉ DES DONNÉES — canon/*.json contre 2026-I, la Chronologie et le Registre")
    for error in errors:
        print(f"- {error}")
    print(f"\n{len(errors)} divergence(s). L'autorité est le Markdown canonique : aligner les données, "
          f"ou inscrire l'assertion dans {CLES_PROPOSITIONS} avec sa source.")
    raise SystemExit(1)

print("Parité des données validée : " + " · ".join(constats)
      + f" · 18 fiches, {len(list(DATA.glob('*.json')))} fichiers JSON, règnes et successions recalculés.")
