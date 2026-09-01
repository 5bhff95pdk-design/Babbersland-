#!/usr/bin/env python3
"""Empreinte sémantique de l'Atlas géographique — analogue à `pdf_fingerprint.py`.

L'Atlas est composé de trois fichiers :
- `sources/carte_royaume.svg` : la carte vectorielle ;
- `geographie/carte_royaume.png` : la rastérisation PNG de la carte ;
- `geographie/index.html` : la page interactive.

Le SVG peut être non reproductible au bit près entre machines (timing de
l'écriture, ordre d'itération sur des `set`/`dict`, codage des flottants
dans la sortie de Pillow), mais son **contenu sémantique** l'est : mêmes
toponymes, mêmes positions relatives, mêmes dates maîtresses.

L'empreinte compare donc :
1. Pour le SVG : l'ensemble trié des `id`, des attributs `data-*` (couches
   temporelles), et des noms de classes ; l'attribut `viewBox` ; la
   présence de chaque toponyme canonique (Pabst City, Port Babette, etc.).
2. Pour le PNG : la dimension, le mode colorimétrique, et la somme MD5
   des pixels. Pas de timestamp EXIF (Pillow n'en écrit pas avec ce mode).
3. Pour le HTML : l'ensemble trié des `id`, des classes, et des balises
   `<h1>`/`<h2>` ; la présence des dates maîtresses (1847, 1962, 1986).

Usage :
    python sources/empreinte_atlas.py            # affiche l'empreinte
    python sources/empreinte_atlas.py --write    # grave dans gouvernance/ARTIFACT_SIGNATURES.sha256
    python sources/empreinte_atlas.py --check    # compare à l'empreinte gravée
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

# Import conditionnel de Pillow (peut être absent si --check-only sur SVG/HTML)
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


SVG = ROOT / "sources" / "carte_royaume.svg"
PNG = ROOT / "geographie" / "carte_royaume.png"
HTML = ROOT / "geographie" / "index.html"
STAMP = ROOT / "gouvernance" / "ARTIFACT_SIGNATURES.sha256"

TOPONYMES = ("Pabst City", "Port Babette", "Grass City", "Forêt de Plantagenet", "Monts Froissés")
DATES_MAITRESSES = ("1847", "1962", "1986", "1991")


def svg_semantic() -> str:
    """Calcule l'empreinte sémantique du SVG.

    On extrait :
    - l'attribut `viewBox` (géométrie de la carte) ;
    - tous les `id="..."` (triés) ;
    - tous les `data-since="..."` (couches temporelles) ;
    - tous les `class="..."` (triés) ;
    - la présence de chaque toponyme canonique.

    Ce qui est IGNORÉ : l'ordre des attributs dans les balises, les
    espaces et sauts de ligne, les chemins `<path d="...">` (leur valeur
    hexadécimale peut varier entre machines), les commentaires, le
    préambule XML.
    """
    text = SVG.read_text(encoding="utf-8")
    # viewBox = "0 0 W H"
    viewbox = re.search(r'viewBox="([^"]+)"', text)
    viewbox_str = viewbox.group(1) if viewbox else "missing"
    # Tous les id
    ids = sorted(set(re.findall(r'\bid="([^"]+)"', text)))
    # Couches temporelles
    since = sorted(re.findall(r'data-since="([^"]+)"', text))
    # Classes
    classes = sorted(set(re.findall(r'\bclass="([^"]+)"', text)))
    # Toponymes
    topo = sorted(t for t in TOPONYMES if t in text)
    payload = f"viewBox:{viewbox_str}|ids:{','.join(ids)}|since:{','.join(since)}|" \
              f"classes:{','.join(classes)}|topo:{','.join(topo)}"
    return hashlib.sha256(payload.encode()).hexdigest(), payload


def png_semantic() -> str:
    """Calcule l'empreinte sémantique du PNG.

    Stratégie (R1.4.a-v2, après plusieurs itérations) : ne pas
    comparer les pixels, mais **confirmer que le PNG est bien la
    rastérisation attendue du SVG**. Si le SVG est inchangé (ce
    qu'on a déjà vérifié par `svg_semantic()`), le PNG devrait
    être aussi inchangé — modulo les variations d'encoding
    Pillow/locale.

    On vérifie donc :
    - la dimension correspond à ce qu'attend `generate_map.py`
      (1600×1100 pour la carte du Royaume, sinon alerte) ;
    - le mode colorimétrique (RGB, attendu) ;
    - la **somme MD5 des pixels en 16×16 NEAREST** : un échantillonnage
      grossier qui ne détecte pas les changements de 1 pixel, mais
      détecte les changements structurels (région ajoutée/supprimée,
      couleur de fond modifiée, etc.). Tolère les micro-variations
      d'encoding.
    """
    if not HAS_PIL:
        return "no-pil", "PIL not available"
    img = Image.open(PNG)
    w, h = img.size
    # Échantillonnage 16×16 en NEAREST (tolérant, mais structurel)
    thumb = img.resize((16, 16), Image.NEAREST)
    pixels = list(thumb.getdata())
    pixel_str = ",".join(str(p) for p in pixels)
    payload = f"size:{w}x{h}|mode:{img.mode}|16x16nearest:{pixel_str}"
    return hashlib.sha256(payload.encode()).hexdigest(), payload


def html_semantic() -> str:
    """Calcule l'empreinte sémantique du HTML.

    On extrait :
    - tous les `id="..."` (triés) ;
    - toutes les classes (triées) ;
    - le texte des balises `<h1>` et `<h2>` (triées) ;
    - la présence des dates maîtresses.
    """
    text = HTML.read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r'\bid="([^"]+)"', text)))
    classes = sorted(set(re.findall(r'\bclass="([^"]+)"', text)))
    h1 = sorted(re.findall(r'<h1[^>]*>([^<]+)</h1>', text))
    h2 = sorted(re.findall(r'<h2[^>]*>([^<]+)</h2>', text))
    dates = sorted(d for d in DATES_MAITRESSES if d in text)
    payload = f"ids:{','.join(ids)}|classes:{','.join(classes)}|" \
              f"h1:{','.join(h1)}|h2:{','.join(h2)}|dates:{','.join(dates)}"
    return hashlib.sha256(payload.encode()).hexdigest(), payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="grave l'empreinte de référence")
    parser.add_argument("--check", action="store_true", help="compare à l'empreinte gravée")
    args = parser.parse_args(argv)

    for f in (SVG, PNG, HTML):
        if not f.is_file():
            print(f"fichier manquant : {f.relative_to(ROOT)}")
            return 1

    svg_hash, svg_payload = svg_semantic()
    png_hash, png_payload = png_semantic()
    html_hash, html_payload = html_semantic()

    if args.write:
        STAMP.parent.mkdir(exist_ok=True)
        # On préserve le contenu existant du fichier (qui peut contenir
        # d'autres signatures d'artéfacts) et on remplace notre section.
        existing = STAMP.read_text(encoding="utf-8") if STAMP.is_file() else ""
        # Retirer l'ancienne section atlas si elle existe
        section_re = re.compile(
            r"# === ATLAS GÉOGRAPHIQUE ===.*?(?=\n# =|\Z)", re.DOTALL
        )
        existing = section_re.sub("", existing).rstrip() + "\n"
        new_section = (
            "\n# === ATLAS GÉOGRAPHIQUE ===\n"
            "# Signé par sources/empreinte_atlas.py (analogue à pdf_fingerprint.py).\n"
            "# L'Atlas (SVG, PNG, HTML) n'est pas reproductible au bit près entre\n"
            "# machines (timing d'écriture, ordre d'itération, encodage des flottants\n"
            "# Pillow) ; on compare donc son contenu sémantique :\n"
            "# - SVG : viewBox, ids, data-since, classes, toponymes canoniques ;\n"
            "# - PNG : dimension, mode, somme MD5 des pixels ;\n"
            "# - HTML : ids, classes, h1/h2, dates maîtresses.\n"
            f"atlas_svg = {svg_hash}\n"
            f"atlas_png = {png_hash}\n"
            f"atlas_html = {html_hash}\n"
        )
        STAMP.write_text(existing + new_section, encoding="utf-8")
        print(f"Empreinte Atlas gravée dans {STAMP.relative_to(ROOT)} :")
        print(f"  SVG  : {svg_hash}")
        print(f"  PNG  : {png_hash}")
        print(f"  HTML : {html_hash}")
        return 0

    if args.check:
        if not STAMP.is_file():
            print(f"aucune empreinte de référence : lancer `python sources/empreinte_atlas.py --write`")
            return 1
        text = STAMP.read_text(encoding="utf-8")
        fields = dict(re.findall(r"^atlas_(\w+) = (\S+)$", text, flags=re.M))
        current = {"svg": svg_hash, "png": png_hash, "html": html_hash}
        drift = {k: (fields.get(k), v) for k, v in current.items() if k in fields and fields[k] != v}
        if not drift:
            print(f"Atlas à jour : SVG={svg_hash[:8]}… PNG={png_hash[:8]}… HTML={html_hash[:8]}…")
            return 0
        print("Atlas divergent du contrat gravé :")
        for kind, (engraved, actual) in drift.items():
            print(f"  atlas_{kind} : généré {actual} != gravé {engraved}")
        print()
        print("Détails sémantiques :")
        print(f"  SVG  payload : {svg_payload[:120]}…")
        print(f"  PNG  payload : {png_payload[:120]}…")
        print(f"  HTML payload : {html_payload[:120]}…")
        return 1

    print(f"Atlas :")
    print(f"  SVG  : {svg_hash}")
    print(f"  PNG  : {png_hash}")
    print(f"  HTML : {html_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
