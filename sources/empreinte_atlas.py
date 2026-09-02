#!/usr/bin/env python3
"""Empreinte sémantique de l'Atlas géographique — variantes acceptées (R1.4.a-v3).

L'Atlas est trois fichiers produits par `sources/generate_map.py` : le SVG
(`sources/carte_royaume.svg`, recopié dans `geographie/`), sa rastérisation PNG
(`geographie/carte_royaume.png`) et la page interactive (`geographie/index.html`).

Pourquoi une reprise (mesure). R1.4.a-v2 avait livré l'empreinte en trois SHA-256
graves en valeur unique, et **l'étape CI ne l'appelait pas** : elle se bornait à
régénérer et à lancer `check_geography.py`, sous `continue-on-error: true`. Bilan :
le contrat existait dans le dépôt, pas dans la chaîne — et le PNG, comparé par
échantillonnage **NEAREST** 16×16 (un pixel lu sur cent), était fragile au point
qu'on n'osait pas le brancher. Un point d'échantillonnage qui tombe sur un glyphe
antialiasé, et la charge bouge pour du vent.

Ce que la charge compare, aujourd'hui :

- `svg` / `html` : le **contenu structurel** — viewBox, `id`, `data-since`
  (couches temporelles), classes, présence des toponymes canoniques pour le SVG ;
  `id`, classes, `<h1>`/`<h2>`, dates maîtresses pour la page. Ces deux-là sont
  indépendants de la machine : ils ne bougent que si la carte change.
- `taille` / `mode` / `16x16box` / `encre` : le rendu, traité comme celui de
  l'arbre (R1.4.b) — moyennage **BOX** 16×16 puis quantification sur 16 niveaux,
  plus la proportion d'encre. Le BOX moyenne 100×69 pixels par cellule : le bruit
  d'antialiasing disparaît, la région supprimée ou le fond changé restent.

Et le modèle est celui de R1.4.b, parce que c'est lui qui a fait la preuve du
diagnostic : l'ensemble des charges **observées** est gravé, une charge inédite
bloque — avec, en annotation, la composante fautive. `svg` qui bouge = la carte a
changé (à assumer par un Avis) ; seul `16x16box` qui bouge = bruit de rendu d'une
nouvelle machine (à accepter).

Usage :
    python sources/empreinte_atlas.py                          # affiche la charge
    python sources/empreinte_atlas.py --write [--variante N]  # grave (acte d'assentiment)
    python sources/empreinte_atlas.py --accepter '<charge>' N  # accepte une charge de la CI
    python sources/empreinte_atlas.py --check                  # échoue si la charge est inédite
    python sources/empreinte_atlas.py --payloads               # détail lisible des composantes
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from sceaux import Sceau, sha256  # noqa: E402

SVG = ROOT / "sources" / "carte_royaume.svg"
PNG = ROOT / "geographie" / "carte_royaume.png"
HTML = ROOT / "geographie" / "index.html"

TOPONYMES = ("Pabst City", "Port Babette", "Grass City", "Forêt de Plantagenet", "Monts Froissés")
DATES_MAITRESSES = ("1847", "1962", "1986", "1991")

ENTETE = (
    "# Signé par sources/empreinte_atlas.py — modèle « variantes acceptées » (R1.4.a-v3).\n"
    "# Reprise de R1.4.a-v2, qui gravait trois SHA-256 en valeur unique sans que la CI\n"
    "# appelle le contrôle. La charge combine contenu structurel et rendu, et\n"
    "# s'appuie sur l'ensemble des charges OBSERVÉES (comme l'Arbre, R1.4.b) :\n"
    "#   svg      : md516 du contenu structurel du SVG (viewBox, ids, data-since,\n"
    "#              classes, toponymes canoniques) — indépendant de la machine ;\n"
    "#   html     : md516 du contenu structurel de la page (ids, classes, h1/h2,\n"
    "#              dates maîtresses) — indépendant de la machine ;\n"
    "#   taille/mode/16x16box/encre : le PNG, moyenné BOX 16x16 quantifié sur 16\n"
    "#              niveaux + proportion d'encre — tolère l'antialiasing, refuse la\n"
    "#              région manquante (le NEAREST 16x16 de v2 était trop fragile).\n"
    "# Une charge inédite bloque. Si seule `16x16box` (ou `encre`) bouge, c'est du\n"
    "# bruit de rendu d'un nouvel environnement : lire l'annotation, puis accepter.\n"
    "# Si `svg` ou `html` bouge, la carte a changé : cela se décrète, cela se grave.\n"
)

MOTIF = (r"svg:[0-9a-f]{16}\|html:[0-9a-f]{16}\|taille:\d+x\d+\|mode:\w+\|"
         r"16x16box:[0-9a-f]{32}\|encre:\d+(?:\.\d+)?")


def svg_payload() -> str:
    """Contenu structurel du SVG : viewBox, ids, couches temporelles, classes, toponymes."""
    texte = SVG.read_text(encoding="utf-8")
    viewbox = re.search(r'viewBox="([^"]+)"', texte)
    ids = sorted(set(re.findall(r'\bid="([^"]+)"', texte)))
    since = sorted(re.findall(r'data-since="([^"]+)"', texte))
    classes = sorted(set(re.findall(r'\bclass="([^"]+)"', texte)))
    topo = sorted(t for t in TOPONYMES if t in texte)
    return (f"viewBox:{viewbox.group(1) if viewbox else 'absent'}|ids:{','.join(ids)}"
            f"|since:{','.join(since)}|classes:{','.join(classes)}|topo:{','.join(topo)}")


def html_payload() -> str:
    """Contenu structurel de la page : ids, classes, titres, dates maîtresses."""
    texte = HTML.read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r'\bid="([^"]+)"', texte)))
    classes = sorted(set(re.findall(r'\bclass="([^"]+)"', texte)))
    h1 = sorted(re.findall(r'<h1[^>]*>([^<]+)</h1>', texte))
    h2 = sorted(re.findall(r'<h2[^>]*>([^<]+)</h2>', texte))
    dates = sorted(d for d in DATES_MAITRESSES if d in texte)
    return (f"ids:{','.join(ids)}|classes:{','.join(classes)}|h1:{','.join(h1)}"
            f"|h2:{','.join(h2)}|dates:{','.join(dates)}")


def png_charge() -> str | None:
    """Rendu du PNG : géométrie, grille BOX 16×16 quantifiée, encre. None si indisponible."""
    if not HAS_PIL or not PNG.is_file():
        return None
    img = Image.open(PNG).convert("RGB")
    w, h = img.size
    grille = bytes(v // 16 for v in img.resize((16, 16), Image.BOX).tobytes())
    gris = img.convert("L")
    encre = sum(v < 100 for v in gris.tobytes()) / (w * h)
    return (f"taille:{w}x{h}|mode:{img.mode}"
            f"|16x16box:{hashlib.md5(grille).hexdigest()}|encre:{encre:.3f}")


def charge_courante() -> str | None:
    if not (SVG.is_file() and HTML.is_file()):
        return None
    rendu = png_charge()
    if rendu is None:
        return None
    return (f"svg:{hashlib.md5(svg_payload().encode()).hexdigest()[:16]}"
            f"|html:{hashlib.md5(html_payload().encode()).hexdigest()[:16]}"
            f"|{rendu}")


def grille_quantifiee() -> str:
    """Grille 16×16 du rendu, lisible : c\'est elle qui distingue un bruit d\'une retouche.

    Repris tel quel de l\'Arbre (R1.4.b), où il a déjà prouvé son usage : la divergence
    se **mesure** (combien de cellules, de combien de niveaux) au lieu de se deviner.
    ~2,3 ko : tient dans une annotation de check-run, seul canal lisible ici.
    """
    if not HAS_PIL or not PNG.is_file():
        return "indisponible"
    data = Image.open(PNG).convert("RGB").resize((16, 16), Image.BOX).tobytes()
    return ",".join(f"{data[i] // 16}.{data[i + 1] // 16}.{data[i + 2] // 16}"
                    for i in range(0, len(data), 3))


def diagnostic() -> str:
    parts = [f"SVG {sha256(SVG)[:12]}… {len(SVG.read_bytes()):,} o" if SVG.is_file() else "SVG absent",
             f"HTML {sha256(HTML)[:12]}… {len(HTML.read_bytes()):,} o" if HTML.is_file() else "HTML absent"]
    if PNG.is_file():
        parts.append(f"PNG {sha256(PNG)[:12]}… {len(PNG.read_bytes()):,} o")
    payload = svg_payload()
    parts.append(f"payload SVG (extrait) : {payload[:700]}")
    parts.append(f"grille={grille_quantifiee()}")
    return " ; ".join(parts)


sceau = Sceau(marqueur="ATLAS GÉOGRAPHIQUE", prefixe="atlas", entete=ENTETE, motif=MOTIF,
              charge=charge_courante, diagnostic=diagnostic, ligne_tete="atlas_lot",
              libelle="Atlas")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if "--payloads" in argv:
        print(f"  svg  payload : {svg_payload()}")
        print(f"  html payload : {html_payload()}")
        return 0
    return sceau.main([a for a in argv if a != "--payloads"], descriptif=__doc__.splitlines()[0])


if __name__ == "__main__":
    raise SystemExit(main())
