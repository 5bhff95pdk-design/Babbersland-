#!/usr/bin/env python3
"""Génère le PDF consolidé 2026-I depuis sa source Markdown.

Dépendances : reportlab et Pillow.
"""
from __future__ import annotations

import html
import re
import tempfile
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Preformatted, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ENCYCLOPEDIE_CONSOLIDEE_2026_I.md"
OUTPUT = ROOT / "Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf"
NAVY = colors.HexColor("#132A44")
GOLD = colors.HexColor("#B78A35")
CREAM = colors.HexColor("#F6EEDB")
INK = colors.HexColor("#29251F")
MUTED = colors.HexColor("#6E624F")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")

styles = getSampleStyleSheet()
BODY = ParagraphStyle("BodyI", parent=styles["BodyText"], fontName="DejaVu", fontSize=9.2,
    leading=13.2, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
H1 = ParagraphStyle("Heading1I", parent=styles["Heading1"], fontName="DejaVu-Bold", fontSize=20,
    leading=24, textColor=NAVY, spaceAfter=12, spaceBefore=3, keepWithNext=True)
H2 = ParagraphStyle("Heading2I", parent=styles["Heading2"], fontName="DejaVu-Bold", fontSize=14,
    leading=18, textColor=colors.HexColor("#744A15"), spaceBefore=12, spaceAfter=7, keepWithNext=True)
H3 = ParagraphStyle("Heading3I", parent=styles["Heading3"], fontName="DejaVu-Bold", fontSize=11,
    leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4, keepWithNext=True)
H4 = ParagraphStyle("Heading4I", parent=H3, fontSize=9.6, leading=12, textColor=colors.HexColor("#744A15"))
QUOTE = ParagraphStyle("QuoteI", parent=BODY, leftIndent=16, rightIndent=12, borderColor=GOLD,
    borderWidth=0, borderLeft=True, borderPadding=8, textColor=MUTED, fontSize=9, leading=13)
LIST = ParagraphStyle("ListI", parent=BODY, leftIndent=17, firstLineIndent=-9, alignment=TA_LEFT, spaceAfter=3)
CAPTION = ParagraphStyle("CaptionI", parent=BODY, fontSize=7.5, leading=9.5, textColor=MUTED,
    alignment=TA_CENTER, spaceAfter=8)
TABLE_CELL = ParagraphStyle("TableCellI", parent=BODY, fontSize=7.1, leading=9, alignment=TA_LEFT, spaceAfter=0)
TABLE_HEAD = ParagraphStyle("TableHeadI", parent=TABLE_CELL, fontName="DejaVu-Bold", textColor=colors.white)
CODE = ParagraphStyle("CodeI", fontName="DejaVu-Mono", fontSize=5.6, leading=7, textColor=INK,
    backColor=CREAM, borderPadding=7)

EMOJI_RE = re.compile("[\U00010000-\U0010ffff]|[♛👑📜🌲🍔🍟💰🏛🖼🪙🍷👶🍲⚖️]")

def clean_heading(text: str) -> str:
    return re.sub(r"\s+", " ", EMOJI_RE.sub("", text)).strip()

def rich(text: str) -> str:
    """Convertit le petit sous-ensemble Markdown utilisé vers le balisage ReportLab."""
    text = re.sub(r"\s*\(`images/[^`]+`\)", "", text)
    text = re.sub(r"\s*`images/[^`]+`", "", text)
    stash: list[str] = []
    def hold(pattern: str, opening: str, closing: str, value: str) -> str:
        def repl(m):
            stash.append(f"<{opening}>{html.escape(m.group(1))}</{closing}>")
            return f"@@{len(stash)-1}@@"
        return re.sub(pattern, repl, value)
    text = hold(r"\*\*(.+?)\*\*", "b", "b", text)
    text = hold(r"(?<!\*)\*(.+?)\*(?!\*)", "i", "i", text)
    text = hold(r"`(.+?)`", "font name=\"DejaVu-Mono\"", "font", text)
    text = html.escape(EMOJI_RE.sub("", text))
    for i, item in enumerate(stash):
        text = text.replace(f"@@{i}@@", item)
    return text

IMAGE_AFTER = {
    "GÉNÉRATION II : LES BÂTISSEURS (1892–1914)": ("images/hortense_du_grain.png", "Hortense du Grain, grande maîtresse de la malterie."),
    "GÉNÉRATION III : L’ÂGE HORIZONTAL (1914–1959)": ("images/irene_des_erables.png", "Irène des Érables, gardienne des érablières."),
    "2. S.A.R. le Prince Babber le Déchiré (date de naissance non consignée ; majeur attesté en 2007)": ("images/babber_le_dechire.png", "Portrait officiel du Prince Babber le Déchiré."),
    "3. S.A.R. la Princesse Ginette de Port Babette (née en 1988)": ("images/ginette_de_port_babette.png", "La Princesse Ginette et le Grand Sauciériste d’Or."),
    "LE CORPS D'ÉTAT : ROGER BONTEMPS, LE GRAND BOUFFON ROYAL": ("images/roger_bontemps.png", "Roger Bontemps, Grand Bouffon royal."),
    "GÉNÉRATION VII : L’AVÈNEMENT DU SAUVEUR DYNASTIQUE": ("images/ti_babber_generation_7.png", "Ti-Babber dans le Berceau-Hamac royal."),
    "HISTOIRE NATIONALE : LA FONDATION DE McBABBER’S": ("images/mcbabbers_enseigne_royale.png", "Le premier McBabber’s de Pabst City."),
    "Le menu canonique de McBabber’s": ("images/mcbabbers_menu_pabst.png", "Le menu royal de McBabber’s."),
    "Le Babbersgate : le scandale de la sauce secrète (1991–1993)": ("images/babbersgate_scandale_sauce.png", "La commission d’enquête du Babbersgate."),
    "LES PIÈCES DE MONNAIE OFFICIELLES (ÉMISSION MÉTALLIQUE 2026)": ("images/pieces_monnaie_babberland_coffret.png", "Coffret métallique officiel 2026."),
}

class RoyalDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, rightMargin=1.7*cm, leftMargin=1.7*cm,
            topMargin=1.75*cm, bottomMargin=1.6*cm,
            title="Encyclopédie officielle consolidée du Royaume du Babberland — 2026-I",
            author="Luc Foster, Grand Argentier", creator="Chancellerie royale de Pabst City",
            subject="Histoire, généalogie, institutions et chronologie canoniques du Babberland",
            keywords="Babberland, encyclopédie 2026-I, généalogie, McBabber’s, Pabst City")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="royal", frames=frame, onPage=self._decorate))
        self._bookmark_id = 0

    def _decorate(self, canvas, doc):
        if doc.page == 1:
            return
        canvas.saveState()
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.7)
        canvas.line(self.leftMargin, A4[1]-1.18*cm, A4[0]-self.rightMargin, A4[1]-1.18*cm)
        canvas.setFont("DejaVu", 7.2); canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, A4[1]-0.92*cm, "ROYAUME DU BABBERLAND · ENCYCLOPÉDIE 2026-I")
        canvas.drawRightString(A4[0]-self.rightMargin, A4[1]-0.92*cm, "ARCHIVES OFFICIELLES")
        canvas.line(self.leftMargin, 1.12*cm, A4[0]-self.rightMargin, 1.12*cm)
        canvas.drawCentredString(A4[0]/2, 0.72*cm, str(doc.page))
        canvas.restoreState()

    def beforeDocument(self):
        # multiBuild effectue plusieurs passes pour stabiliser le sommaire.
        self._bookmark_id = 0
        self._outline_started = False

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in {"Heading1I", "Heading2I"}:
            level = 0 if flowable.style.name == "Heading1I" else 1
            # La déclaration éditoriale (H2) précède le premier Livre (H1).
            if not self._outline_started:
                level = 0
            self._outline_started = True
            text = flowable.getPlainText()
            key = f"h{self._bookmark_id}"; self._bookmark_id += 1
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))

def prepared_image(relpath: str, tmp: Path, max_w=16.3*cm, max_h=8.8*cm) -> Image:
    src = ROOT / relpath
    out = tmp / (src.stem + ".jpg")
    if not out.exists():
        with PILImage.open(src) as pic:
            pic = pic.convert("RGB")
            pic.thumbnail((1500, 900), PILImage.Resampling.LANCZOS)
            pic.save(out, "JPEG", quality=78, optimize=True, progressive=True)
    with PILImage.open(out) as pic:
        w, h = pic.size
    scale = min(max_w/w, max_h/h)
    return Image(str(out), width=w*scale, height=h*scale)

def make_table(rows: list[list[str]]) -> Table:
    n = len(rows[0])
    widths = {
        2: [4.1*cm, 12.2*cm],
        3: [2.2*cm, 7.1*cm, 7.0*cm],
        4: [2.6*cm, 4.6*cm, 5.3*cm, 3.8*cm],
        5: [2.1*cm, 3.7*cm, 5.0*cm, 2.0*cm, 3.5*cm],
        6: [2.0*cm, 3.3*cm, 3.0*cm, 4.1*cm, 1.4*cm, 2.5*cm],
    }.get(n, [16.3*cm/n]*n)
    data=[]
    for r, row in enumerate(rows):
        style = TABLE_HEAD if r == 0 else TABLE_CELL
        data.append([Paragraph(rich(c.strip()), style) for c in row])
    table=Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#BBAA87")),
        ("VALIGN",(0,0),(-1,-1),"TOP"), ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4), ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,CREAM]),
    ]))
    return table

def parse_markdown(tmp: Path) -> list:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    # La couverture remplace l'en-tête Markdown.
    start = next(i for i,x in enumerate(lines) if x.startswith("## DÉCLARATION"))
    lines = lines[start:]
    story=[]; i=0; first_h1=True
    while i < len(lines):
        raw=lines[i].rstrip(); stripped=raw.strip()
        if not stripped: i+=1; continue
        if stripped.startswith("|") and i+1 < len(lines) and re.match(r"^\|[\s:|\-]+\|$",lines[i+1].strip()):
            rows=[]; rows.append([x.strip() for x in stripped.strip("|").split("|")]); i+=2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([x.strip() for x in lines[i].strip().strip("|").split("|")]); i+=1
            story.extend([make_table(rows),Spacer(1,7)]); continue
        if stripped.startswith("```"):
            code=[]; i+=1
            while i<len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i+=1
            i+=1
            if any("GÉNÉRATION I" in x for x in code):
                img=prepared_image("images/arbre_genealogique_complet.png",tmp,max_h=10.2*cm)
                story.extend([img,Paragraph("Arbre généalogique officiel consolidé.",CAPTION)])
            else: story.append(Preformatted("\n".join(code),CODE))
            continue
        if stripped == "---": story.append(Spacer(1,5)); i+=1; continue
        hm=re.match(r"^(#{1,4})\s+(.+)$",stripped)
        if hm:
            level=len(hm.group(1)); title=clean_heading(hm.group(2))
            if level==1:
                if not first_h1: story.append(PageBreak())
                first_h1=False; style=H1
            elif level==2: style=H2
            elif level==3: style=H3
            else: style=H4
            story.append(Paragraph(rich(title),style))
            if title in IMAGE_AFTER:
                path,cap=IMAGE_AFTER[title]; img=prepared_image(path,tmp)
                story.append(KeepTogether([img,Paragraph(cap,CAPTION)]))
            i+=1; continue
        if stripped.startswith(">"):
            parts=[]
            while i<len(lines) and lines[i].strip().startswith(">"):
                parts.append(lines[i].strip()[1:].strip()); i+=1
            story.append(Paragraph(rich(" ".join(parts)),QUOTE)); continue
        lm=re.match(r"^(\s*)([*-]|\d+\.)\s+(.+)$",raw)
        if lm:
            indent=len(lm.group(1)); mark=lm.group(2); bullet="•" if mark in {"*","-"} else mark
            style=ParagraphStyle(f"List{indent}",parent=LIST,leftIndent=17+indent*5)
            story.append(Paragraph(rich(lm.group(3)),style,bulletText=bullet)); i+=1; continue
        # paragraphe : joindre les lignes jusqu'au prochain bloc
        parts=[stripped]; i+=1
        while i<len(lines):
            nxt=lines[i].strip()
            if not nxt or nxt.startswith(("#","|",">","```","---")) or re.match(r"^(\s*)([*-]|\d+\.)\s+",lines[i]): break
            parts.append(nxt); i+=1
        story.append(Paragraph(rich(" ".join(parts)),BODY))
    return story

def cover(tmp: Path) -> list:
    hero=prepared_image("images/arbre_genealogique_complet.png",tmp,max_w=17.0*cm,max_h=9.5*cm)
    title=Paragraph("ROYAUME DU BABBERLAND",ParagraphStyle("CoverTitle",fontName="DejaVu-Bold",fontSize=25,
        leading=30,textColor=NAVY,alignment=TA_CENTER,spaceAfter=12))
    sub=Paragraph("ENCYCLOPÉDIE OFFICIELLE<br/><font size=20>CONSOLIDÉE 2026-I</font>",ParagraphStyle(
        "CoverSub",fontName="DejaVu-Bold",fontSize=15,leading=24,textColor=colors.HexColor("#744A15"),alignment=TA_CENTER))
    meta=Paragraph("Chancellerie royale · Pabst City<br/>Édition intégrale du 26 août 2026<br/><br/><i>Luc Foster, Grand Argentier, Chancelier et Archiviste royal</i>",
        ParagraphStyle("CoverMeta",fontName="DejaVu",fontSize=10,leading=15,textColor=MUTED,alignment=TA_CENTER))
    return [Spacer(1,1.3*cm),title,sub,Spacer(1,0.9*cm),hero,Spacer(1,0.7*cm),meta,PageBreak()]

def build():
    with tempfile.TemporaryDirectory(prefix="babberland-i-") as d:
        tmp=Path(d)
        toc=TableOfContents(); toc.levelStyles=[
            ParagraphStyle("TOC1",fontName="DejaVu-Bold",fontSize=10,leading=14,leftIndent=0,textColor=NAVY,spaceBefore=4),
            ParagraphStyle("TOC2",fontName="DejaVu",fontSize=8,leading=11,leftIndent=15,textColor=INK),
        ]
        toc_title_style=ParagraphStyle("TocTitleI",parent=H1)
        toc_title=Paragraph("SOMMAIRE",toc_title_style)
        story=cover(tmp)+[toc_title,toc,PageBreak()]+parse_markdown(tmp)
        doc=RoyalDocTemplate(str(OUTPUT)); doc.multiBuild(story)
    print(f"PDF créé : {OUTPUT} ({OUTPUT.stat().st_size/1024/1024:.1f} Mio)")

if __name__ == "__main__": build()
