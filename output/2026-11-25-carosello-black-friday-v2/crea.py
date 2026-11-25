#!/usr/bin/env python3
"""Carosello Black Friday Pakima (4 slide 4:5) nello stile delle grafiche del negozio."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

QUI = Path(__file__).resolve().parent
RADICE = QUI.parents[1]
sys.path.insert(0, str(RADICE / "studio"))
import genera as g  # noqa: E402

W, H = 1080, 1350
ST = {**g.STILE_BASE}
NERO, BIANCO = g.colore("#0E0E0E"), g.colore("#FFFFFF")
ROSSO = g.colore("#9E1B2F")
S = int(W * 0.085)                 # spessore cornice
IN = S + int(S * 0.18) + 14        # margine interno al filo sottile


def base():
    img = Image.new("RGBA", (W, H), BIANCO)
    return img


def chiudi(img, nome):
    g.Cornice("Black Friday", W, H, ST).applica(img, 0.6)
    img.convert("RGB").save(QUI / f"{nome}.png")
    print("ok", nome)


def centra(img, el, y):
    img.alpha_composite(el, ((W - el.width) // 2, int(y)))
    return y + el.height


def testo(t, font, dim, col=NERO, sp=0, max_w=W - 2 * IN - 40):
    return g.blocco_testo(t, ST[font], dim, col, max_w, spaziatura=sp, interlinea=1.05)


def foto(percorso, w, h, centro=(0.5, 0.5), sfondo_bianco=False):
    im = ImageOps.exif_transpose(Image.open(RADICE / percorso)).convert("RGB")
    if sfondo_bianco:  # contieni il capo intero su bianco
        im.thumbnail((w, h), Image.LANCZOS)
        tela = Image.new("RGB", (w, h), "white")
        tela.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
        return tela.convert("RGBA")
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=centro).convert("RGBA")


def arrotonda(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    return out


def bollino(t, dim=30, fondo=NERO, col=BIANCO):
    return g.pillola(t, ST["font_forte"], dim, fondo, col, spaziatura=2, maiuscolo=True)


def stelline(img, punti):
    d = ImageDraw.Draw(img)
    for x, y, r in punti:
        g.stella(d, x, y, r, NERO)


def logo(img, y, larg=230):
    return centra(img, g.logo(ST, False, larg), y)


# ---------------------------------------------------------------- 1 copertina
def slide1():
    img = base()
    y = logo(img, IN + 18, 210) + 10
    y = centra(img, testo("BLACK", "font_titolo", 170, sp=6), y - 10)
    y = centra(img, testo("Friday", "font_corsivo", 120), y - 40) + 6
    ph = foto("foto/ai/capi-senza-manichini.png", W - 2 * IN - 40, 560, centro=(0.5, 0.45))
    img.alpha_composite(arrotonda(ph, 18), ((W - ph.width) // 2, y))
    y += ph.height
    b = bollino("-20% su tutto l'abbigliamento", 30)
    img.alpha_composite(b, ((W - b.width) // 2, y - b.height // 2))
    stelline(img, [(IN + 70, 250, 22), (W - IN - 70, 300, 16), (W - IN - 110, 210, 10)])
    chiudi(img, "1-copertina")


# ---------------------------------------------------------------- 2 la selezione
def slide2():
    img = base()
    y = IN + 30
    y = centra(img, testo("la nostra selezione", "font_corsivo", 54), y)
    y = centra(img, testo("-20% su tutto", "font_titolo", 96), y) + 26
    capi = [("foto/prodotti/nhebyna-piumino-nero-pelliccia.png", "Piumino"),
            ("foto/prodotti/nhebyna-maglione-rombi-marrone.png", "Maglieria"),
            ("foto/prodotti/nhebyna-pantalone-velluto-verde.png", "Pantaloni"),
            ("foto/outfit/borsa-vernice-moro-ritaglio.jpg", "Borse")]
    gap = 18
    cw = (W - 2 * IN - 40 - gap) // 2
    ch = (H - y - IN - 40 - gap) // 2
    for i, (p, nome) in enumerate(capi):
        cx = IN + 20 + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ch + gap)
        cella = Image.new("RGBA", (cw, ch), g.colore("#F4F2EF"))
        ph = foto(p, cw - 30, ch - 70, sfondo_bianco=True)
        ph = ph.copy()
        # rende il fondo bianco della foto uguale alla cella
        px = ph.load()
        for yy in range(ph.height):
            for xx in range(ph.width):
                r, gg, b, a = px[xx, yy]
                if min(r, gg, b) > 205 and max(r, gg, b) - min(r, gg, b) < 14:
                    px[xx, yy] = (244, 242, 239, 255)
        cella.alpha_composite(ph, (15, 12))
        et = testo(nome.upper(), "font_forte", 24, sp=4)
        cella.alpha_composite(et, ((cw - et.width) // 2, ch - 52))
        img.alpha_composite(arrotonda(cella, 14), (cx, cy))
        b = bollino("-20%", 26)
        img.alpha_composite(b, (cx + cw - b.width - 12, cy + 12))
    chiudi(img, "2-selezione")


# ---------------------------------------------------------------- 3 fino al 30%
def fiocco(d, cx, cy, s, col):
    d.polygon([(cx, cy), (cx - s, cy - s * 0.6), (cx - s, cy + s * 0.6)], fill=col)
    d.polygon([(cx, cy), (cx + s, cy - s * 0.6), (cx + s, cy + s * 0.6)], fill=col)
    d.polygon([(cx - s * 0.15, cy), (cx - s * 0.55, cy + s * 1.3), (cx - s * 0.2, cy + s * 1.2)], fill=col)
    d.polygon([(cx + s * 0.15, cy), (cx + s * 0.55, cy + s * 1.3), (cx + s * 0.2, cy + s * 1.2)], fill=col)
    d.ellipse((cx - s * 0.22, cy - s * 0.22, cx + s * 0.22, cy + s * 0.22), fill=col)


def slide3():
    img = base()
    ph = foto("foto/outfit/maglia-intarsio-jeans-panna.jpg", W - 2 * IN - 40, 600, centro=(0.5, 0.62))
    img.alpha_composite(arrotonda(ph, 18), ((W - ph.width) // 2, IN + 24))
    y = IN + 24 + ph.height + 24
    y = centra(img, testo("e fino al", "font_corsivo", 64), y - 6)
    y = centra(img, testo("-30%", "font_titolo", 190), y - 30)
    y = centra(img, testo("SU UNA SELEZIONE DI CAPI, ANCHE JEANS", "font_forte", 26, sp=3), y - 4) + 16
    b = g.pillola("cerca il fiocco rosso sulla gruccia", ST["font_corsivo"], 34, ROSSO, BIANCO)
    bx = (W - b.width) // 2
    img.alpha_composite(b, (bx, y))
    fiocco(ImageDraw.Draw(img), W - IN - 80, IN + 70, 34, ROSSO)
    chiudi(img, "3-fino-al-30")


# ---------------------------------------------------------------- 4 domenica aperti
def slide4():
    img = base()
    y = logo(img, IN + 30, 240) + 40
    y = centra(img, testo("domenica", "font_corsivo", 90), y)
    y = centra(img, testo("29", "font_titolo", 330), y - 60)
    y = centra(img, testo("NOVEMBRE", "font_forte", 44, sp=14), y - 40) + 50
    y = centra(img, testo("Siamo aperti", "font_titolo", 100), y) + 24
    b = g.pillola("ultimo giorno di Black Friday", ST["font_corsivo"], 38, NERO, BIANCO)
    y = centra(img, b, y) + 40
    centra(img, testo("VIA CAVOUR 7 · VIMERCATE", "font_testo", 26, sp=4), y)
    stelline(img, [(IN + 80, 480, 20), (W - IN - 80, 520, 26), (W - IN - 130, 430, 12)])
    chiudi(img, "4-domenica-aperti")


if __name__ == "__main__":
    slide1(); slide2(); slide3(); slide4()
