"""Estratto PDF + immagini di anteprima delle pagine interne per le inserzioni Etsy.
Uso: python3 build/anteprime_etsy.py"""
import os, subprocess, tempfile, glob
from pypdf import PdfReader, PdfWriter
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "consegna", "anteprima"); os.makedirs(OUT, exist_ok=True)
BOOKS = {"it": ("Guadagnare-con-AI-IT", [12, 29, 46], "Estratto"), "en": ("Make-Money-with-AI-EN", [11, 29, 45], "Excerpt")}
def page_png(pdf, n, d):
    subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", "150", "-png", pdf, f"{d}/p{n}"], check=True)
    return Image.open(sorted(glob.glob(f"{d}/p{n}*.png"))[0]).convert("RGB")
for lang, (name, pages, label) in BOOKS.items():
    pdf = os.path.join(ROOT, "consegna", name + ".pdf")
    r = PdfReader(pdf); w = PdfWriter()
    for i in range(0, 16): w.add_page(r.pages[i])
    w.write(os.path.join(OUT, f"{name}-{label}.pdf"))
    d = tempfile.mkdtemp()
    ims = [page_png(pdf, n, d) for n in pages]
    W, H = 2000, 1500; bg = Image.new("RGB", (W, H), (243, 238, 228))
    ph = 880; pw = int(ims[0].width * ph / ims[0].height); gap = 45
    x0 = (W - (3 * pw + 2 * gap)) // 2; y0 = (H - ph) // 2
    for i, im in enumerate(ims):
        im = im.resize((pw, ph)); x = x0 + i * (pw + gap)
        sh = Image.new("RGBA", (pw + 60, ph + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([30, 40, pw + 30, ph + 40], fill=(20, 26, 38, 70))
        bg.paste(sh.filter(ImageFilter.GaussianBlur(14)), (x - 30, y0 - 30), sh.filter(ImageFilter.GaussianBlur(14)))
        bg.paste(im, (x, y0))
    bg.save(os.path.join(OUT, f"{lang}-etsy-pagine-interne-2000x1500.png"))
print(sorted(os.listdir(OUT)))
