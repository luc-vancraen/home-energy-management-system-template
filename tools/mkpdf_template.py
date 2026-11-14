import re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D="/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", D+"DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", D+"DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", D+"DejaVuSansMono.ttf"))
from reportlab.lib.fonts import addMapping
addMapping("DV",0,0,"DV"); addMapping("DV",1,0,"DVB")
src, out = sys.argv[1], sys.argv[2]
body = ParagraphStyle("b", fontName="DV", fontSize=9.5, leading=13.5, spaceAfter=5)
h1 = ParagraphStyle("h1", fontName="DVB", fontSize=16, leading=20, spaceAfter=10)
h2 = ParagraphStyle("h2", fontName="DVB", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=5, textColor="#1f3a5f", keepWithNext=1)
h3 = ParagraphStyle("h3", fontName="DVB", fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3, keepWithNext=1)
note = ParagraphStyle("n", parent=body, fontSize=8.5, textColor="#555555")
def fmt(t):
    t = t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    t = re.sub(r"`([^`]+)`", r'<font name="DVM">\1</font>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t
story=[]
bullets=[]   # [[tekst, [(teken, tekst), ...]], ...]: opsomming met ingesprongen subpunten
sub = ParagraphStyle("s", parent=body, leftIndent=16, bulletIndent=2, spaceAfter=3)
def flush():
    global bullets
    if bullets:
        items=[]
        for b, kids in bullets:
            fl=[Paragraph(fmt(b), body)]+[Paragraph(fmt(t), sub if m else ParagraphStyle("c", parent=body, spaceAfter=3), bulletText=m) for m, t in kids]
            items.append(ListItem(fl, leftIndent=12))
        story.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=12, bulletFontName="DV"))
        bullets=[]
for line in open(src, encoding="utf-8").read().splitlines():
    if line[:1].isspace() and line.strip() and bullets:          # ingesprongen regel onder een opsommingspunt
        t=line.strip(); m=re.match(r"(\d+\.) (.*)", t)
        if m: bullets[-1][1].append((m.group(1), m.group(2)))
        elif t.startswith("- "): bullets[-1][1].append(("–", t[2:]))
        else: bullets[-1][1].append((None, t))
        continue
    line=line.strip() if line[:1].isspace() else line
    if line.startswith("- "): bullets.append([line[2:], []]); continue
    flush()
    if not line.strip(): continue
    if line.startswith("### "): story.append(Paragraph(fmt(line[4:]), h3))
    elif line.startswith("## "): story.append(Paragraph(fmt(line[3:]), h2))
    elif line.startswith("# "): story.append(Paragraph(fmt(line[2:]), h1))
    else:
        story.append(Paragraph(fmt(line), body))
flush()
def footer(c, d):
    c.setFont("DV",8); c.setFillColor("#777777"); c.drawRightString(A4[0]-2*cm, 1.2*cm, f"{d.page}")
SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm, title=next((l[2:].strip() for l in open(src, encoding="utf-8") if l.startswith("# ")), "HEMS template"), author="luc-vancraen").build(story, onFirstPage=footer, onLaterPages=footer)
