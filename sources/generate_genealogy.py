"""Génère l'arbre officiel en PNG (dépendance: Pillow)."""
from PIL import Image, ImageDraw, ImageFont
from random import Random

W,H=1600,1000
rng=Random(1847)
im=Image.new('RGB',(W,H),'#20180e'); d=ImageDraw.Draw(im)
# cadre et parchemin
d.rounded_rectangle((28,28,1572,972),22,fill='#a87525',outline='#e0bd62',width=8)
d.rounded_rectangle((55,55,1545,945),12,fill='#f5e6bd',outline='#59320b',width=5)
d.rectangle((77,77,1523,923),outline='#b88735',width=2)
# texture très légère
for _ in range(7000):
    x=rng.randrange(60,1540); y=rng.randrange(60,940); c=rng.choice(['#ead7a8','#f8eccb','#dfc990'])
    d.point((x,y),fill=c)
font='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def F(size,b=False): return ImageFont.truetype(bold if b else font,size)
def center(text,xy,size=19,color='#3a2109',b=True):
    box=d.textbbox((0,0),text,font=F(size,b)); d.text((xy[0]-(box[2]-box[0])/2,xy[1]-(box[3]-box[1])/2),text,font=F(size,b),fill=color)
def node(box,title,detail,kind='main'):
    fills={'main':'#fff8df','current':'#f1d989','collateral':'#edf2da'}; outlines={'main':'#9d6b26','current':'#6f430b','collateral':'#718043'}
    d.rounded_rectangle(box,16,fill=fills[kind],outline=outlines[kind],width=4 if kind=='current' else 3)
    cx=(box[0]+box[2])/2; cy=(box[1]+box[3])/2
    center(title,(cx,cy-12),18 if len(title)>35 else 19)
    center(detail,(cx,cy+16),14,'#70481c',False)
def line(points,color='#815318',width=4): d.line(points,fill=color,width=width,joint='curve')
def gen(text,y): d.text((90,y),text,font=F(16,True),fill='#7c4b14')
center('MAISON ROYALE DE BABBER',(800,115),42,'#512b08')
center('Arbre généalogique officiel révisé · Document 2026-H',(800,154),22,'#76501e',False)
# connexions
line([(800,243),(800,270),(455,270),(455,300)]); line([(800,270),(1265,270),(1265,300)])
line([(455,370),(455,410)]); line([(455,480),(455,520)])
line([(455,590),(455,620),(800,620),(800,650)])
line([(455,620),(300,620),(300,650)]); line([(455,620),(530,620),(530,650)]); line([(455,620),(1070,620),(1070,650)])
line([(800,720),(800,760)]); line([(900,830),(900,845)])
# branche collatérale pointillée
for y in range(370,755,18): line([(1265,y),(1265,min(y+10,760))],'#718043',4)
line([(1265,760),(1250,760)],'#718043',4)
# générations et nœuds
gen('GÉNÉRATION I',205); node((570,185,1030,243),'Babber Ier l’Ancien  ═  Babette Ire de Plantagenet','Fondateurs · 1847')
gen('GÉNÉRATION II',320); node((270,300,640,370),'François-Babber l’Aqueducien','═ Hortense du Grain'); node((1080,300,1450,370),'Princesse Babette-Marine','Branche collatérale · Port Babette','collateral')
gen('GÉNÉRATION III',430); node((270,410,640,480),'Babber le Dormeur','═ Irène des Érables')
gen('GÉNÉRATION IV',540); node((250,520,660,590),'Babber II le Piscineux','═ Colette-Pabst de Grass City')
gen('GÉNÉRATION V',672); node((210,650,390,720),'Honoré-Pabst','Union 1998–2010'); node((440,650,620,720),'Henri-Grain','Union 1998–2010'); node((645,650,955,720),'Babber Ier le Louche','═ Linéa · roi depuis 2010','current'); node((960,650,1180,720),'Rambo du Fjord','Prince du Fleuve')
gen('GÉNÉRATION VI',787); node((675,760,1125,830),'Babber le Fou  ═  Princesse Ginette','Héritier présomptif · Dame de la Sauce'); node((1250,760,1495,830),'Babber le Déchiré','Cousin collatéral','collateral')
gen('GÉNÉRATION VII',858); node((725,845,1075,905),'Ti-Babber · né le 26 août 2026','« VII » désigne la 7e génération','current')
d.text((105,908),'Traits pleins : filiation directe  ·  Pointillés verts : branche collatérale  ·  ═ : union',font=F(16),fill='#563714')
im.save('images/arbre_genealogique_complet.png',optimize=True)
