"""Costruisce PDF ed EPUB di un'edizione.
Uso (dalla cartella del progetto): python3 build/build.py it|en
"""
import sys, os, re, glob, subprocess, html
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

LANG = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build")
SRC = os.path.join(ROOT, "sorgenti", LANG)
OUT = os.path.join(ROOT, "consegna")
os.makedirs(OUT, exist_ok=True)

META = {
 "it": dict(
   title="Guadagnare con l'Intelligenza Artificiale",
   subtitle="La guida pratica per creare nuove opportunità di reddito, avviare un business digitale e monetizzare l'AI anche partendo da zero",
   part="Parte", chapter="Capitolo", toc="Indice", edition="Edizione italiana · 2026",
   author="",
   colophon=[
     "<strong>Guadagnare con l'Intelligenza Artificiale</strong><br/>Prima edizione digitale, novembre 2026.",
     "Informazioni su piattaforme, prezzi e normative verificate a novembre 2026. Prezzi e regole cambiano frequentemente: verifica sempre le fonti ufficiali indicate in appendice.",
     "Questo libro ha scopo esclusivamente informativo e didattico. Non costituisce consulenza fiscale, legale o finanziaria e non garantisce alcun risultato economico. Tutti gli esempi economici sono ipotetici; i personaggi degli esempi sono immaginari.",
     "Realizzato con il supporto di strumenti di intelligenza artificiale, sotto supervisione e revisione editoriale umana.",
     "I nomi di prodotti e servizi citati sono marchi dei rispettivi proprietari e sono usati a solo scopo descrittivo. Nessuna affiliazione o sponsorizzazione.",
     "© 2026 — Tutti i diritti riservati."],
   cover="copertine/copertina-it.png", out="Guadagnare-con-AI-IT"),
 "en": dict(
   title="Make Money with Artificial Intelligence",
   subtitle="The Practical Guide to Building Income Streams, Starting a Digital Business, and Monetizing AI from Scratch",
   part="Part", chapter="Chapter", toc="Contents", edition="English edition · 2026",
   author="",
   colophon=[
     "<strong>Make Money with Artificial Intelligence</strong><br/>First digital edition, November 2026.",
     "Information about platforms, prices and regulations was checked in November 2026. Prices and rules change often: always check the official sources listed in the appendix.",
     "This book is for information and educational purposes only. It is not tax, legal or financial advice and does not guarantee any financial result. All financial examples are hypothetical; the people in the examples are fictional.",
     "Created with the support of artificial intelligence tools, under human editorial supervision and review.",
     "Product and service names mentioned are trademarks of their respective owners and are used for descriptive purposes only. No affiliation or sponsorship is implied.",
     "© 2026 — All rights reserved."],
   cover="copertine/copertina-en.png", out="Make-Money-with-AI-EN"),
}[LANG]

files = sorted(glob.glob(os.path.join(SRC, "*.md")))
md = "\n\n".join(open(f, encoding="utf-8").read() for f in files)

# ---------- PDF ----------
frag = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none"],
                      input=md, capture_output=True, text=True, check=True, cwd=ROOT).stdout
soup = BeautifulSoup(frag, "html.parser")
for inp in soup.find_all("input", {"type": "checkbox"}):
    inp.replace_with(BeautifulSoup('<span class="cb"></span>', "html.parser"))

body = BeautifulSoup("", "html.parser")
sections, current = [], None
pn = cn = 0
toc = []
for el in list(soup.contents):
    if getattr(el, "name", None) == "h1":
        cls = el.get("class", [])
        kind = "part" if "part" in cls else "chapter" if "chapter" in cls else "appendix" if "appendix" in cls else "front"
        sid = el.get("id") or f"s{len(sections)}"
        sec = soup.new_tag("section", attrs={"class": kind, "id": sid})
        title = el.get_text()
        if kind == "part":
            pn += 1
            sec.append(BeautifulSoup(f'<div class="plabel">{META["part"]} {pn}</div>', "html.parser"))
            h = soup.new_tag("h1"); h.string = title; sec.append(h)
            sec.append(BeautifulSoup('<div class="prule"></div>', "html.parser"))
            toc.append(("part", sid, f'{META["part"]} {pn} · {title}', ""))
        else:
            hdr = soup.new_tag("header")
            if kind == "chapter":
                cn += 1
                hdr.append(BeautifulSoup(f'<div class="clabel">{META["chapter"]} {cn}</div>', "html.parser"))
                toc.append(("chapter", sid, title, str(cn)))
            else:
                toc.append(("front", sid, title, ""))
            h = soup.new_tag("h1"); h.string = title; hdr.append(h)
            if kind == "chapter":
                hdr.append(BeautifulSoup('<div class="crule"></div>', "html.parser"))
            sec.append(hdr)
        el.decompose()
        sections.append(sec); current = sec
    else:
        if current is not None:
            current.append(el)

toc_html = f'<nav class="toc"><h1>{META["toc"]}</h1><ul>'
for kind, sid, title, num in toc:
    toc_html += f'<li class="toc-{kind}"><a href="#{sid}" data-num="{num}">{html.escape(title)}</a></li>'
toc_html += "</ul></nav>"

colo = "".join(f"<p>{p}</p>" for p in META["colophon"])
doc = f"""<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{html.escape(META['title'])}</title>
</head><body>
<div class="cover"><img src="{META['cover']}" alt=""/></div>
<div class="front-page titlepage"><div class="ed">{META['edition']}</div><div class="rule"></div>
<div class="t1">{html.escape(META['title'])}</div><div class="t2">{html.escape(META['subtitle'])}</div><div class="rule"></div></div>
<div class="front-page colophon">{colo}</div>
{toc_html}
{''.join(str(s) for s in sections)}
</body></html>"""
open(os.path.join(B, f"libro-{LANG}.html"), "w", encoding="utf-8").write(doc)
pdf_path = os.path.join(OUT, META["out"] + ".pdf")
fc = FontConfiguration()
HTML(string=doc, base_url=ROOT).write_pdf(pdf_path, stylesheets=[CSS(filename=os.path.join(B, "libro.css"), font_config=fc)], font_config=fc)
print("PDF:", pdf_path)

# ---------- EPUB ----------
pn = cn = 0
def num(m):
    global pn, cn
    title, kind = m.group(1), m.group(2)
    if kind == "part":
        pn += 1; return f"# {META['part']} {pn} · {title} {{.part}}"
    cn += 1; return f"# {cn}. {title} {{.chapter}}"
md_epub = re.sub(r"^# (.+?) \{\.(part|chapter)\}\s*$", num, md, flags=re.M)
md_epub = re.sub(r"\{\.unnumbered \.(front|appendix)\}", r"{.\1}", md_epub)
open(os.path.join(B, f"epub-{LANG}.md"), "w", encoding="utf-8").write(md_epub)
epub_path = os.path.join(OUT, META["out"] + ".epub")
fonts = sorted(glob.glob(os.path.join(B, "fonts", "*.ttf")))
cmd = ["pandoc", os.path.join(B, f"epub-{LANG}.md"), "-o", epub_path, "--toc", "--toc-depth=1", "--split-level=1",
       "--css", os.path.join(B, "epub.css"), "--epub-cover-image", os.path.join(ROOT, META["cover"]),
       "--metadata", f"title={META['title']}", "--metadata", f"subtitle={META['subtitle']}",
       "--metadata", f"lang={LANG}",
       "--metadata", "date=2026-11", "--metadata", f"rights=© 2026",
       "--resource-path", ROOT]
for f in fonts:
    cmd += ["--epub-embed-font", f]
subprocess.run(cmd, check=True, cwd=ROOT)
print("EPUB:", epub_path)
