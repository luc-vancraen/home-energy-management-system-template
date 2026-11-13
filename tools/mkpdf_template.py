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
bullets=[]
def flush():
    global bullets
    if bullets:
        story.append(ListFlowable([ListItem(Paragraph(fmt(b), body), leftIndent=12) for b in bullets], bulletType="bullet", start="•", leftIndent=12, bulletFontName="DV"))
        bullets=[]
for line in [l.strip() if re.match(r"\s+\d+\. ", l) or l.startswith("  ") else l for l in open(src, encoding="utf-8").read().splitlines()]:
    if line.startswith("- "): bullets.append(line[2:]); continue
    flush()
    if not line.strip(): continue
    if line.startswith("### "): story.append(Paragraph(fmt(line[4:]), h3))
    elif line.startswith("## "): story.append(Paragraph(fmt(line[3:]), h2))
    elif line.startswith("# "): story.append(Paragraph(fmt(line[2:]), h1))
    else:
        m=re.match(r"(\d+)\. (.*)", line)
        story.append(Paragraph(fmt(line if not m else f"{m.group(1)}. {m.group(2)}"), body))
flush()
def footer(c, d):
    c.setFont("DV",8); c.setFillColor("#777777"); c.drawRightString(A4[0]-2*cm, 1.2*cm, f"{d.page}")
SimpleDocTemplate(out, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm, title=next((l[2:].strip() for l in open(src, encoding="utf-8") if l.startswith("# ")), "HEMS template"), author="luc-vancraen").build(story, onFirstPage=footer, onLaterPages=footer)
