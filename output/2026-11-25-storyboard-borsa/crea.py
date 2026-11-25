#!/usr/bin/env python3
"""Storyboard a mano (6 scene) per lo spot della borsa in vernice testa di moro."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

QUI = Path(__file__).resolve().parent
RADICE = QUI.parents[1]
sys.path.insert(0, str(RADICE / "studio"))
import genera as g  # noqa: E402

ST = dict(g.STILE_BASE)
NERO, BIANCO, GRIGIO = g.colore("#111111"), g.colore("#FFFFFF"), g.colore("#6B6B6B")
BORSA = RADICE / "foto/outfit/borsa-vernice-moro.jpg"

PW, PH = 360, 640           # riquadro 9:16
COL, RIGHE = 3, 2
MX, TOP = 50, 210
TXT_H = 330
W = MX * 2 + COL * PW + (COL - 1) * 40
H = TOP + RIGHE * (PH + TXT_H + 40) + 60


def ritaglio(percorso, box, contieni=False, size=(PW, PH)):
    im = ImageOps.exif_transpose(Image.open(percorso)).convert("RGB")
    w, h = im.size
    c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    if contieni:
        fondo = c.getpixel((5, 5))
        c.thumbnail(size, Image.LANCZOS)
        tela = Image.new("RGB", size, fondo)
        tela.paste(c, ((size[0] - c.width) // 2, (size[1] - c.height) // 2))
        return tela.convert("RGBA")
    return ImageOps.fit(c, size, Image.LANCZOS).convert("RGBA")


def finale():
    im = Image.new("RGBA", (PW, PH), BIANCO)
    b = ritaglio(BORSA, (0.14, 0.26, 0.86, 0.73), contieni=True, size=(PW - 40, 330))
    im.alpha_composite(b, (20, 170))
    lg = g.logo(ST, False, 170)
    im.alpha_composite(lg, ((PW - lg.width) // 2, 50))
    t = g.blocco_testo("VIA CAVOUR 7 · VIMERCATE", ST["font_testo"], 17, NERO, PW - 40, spaziatura=2)
    im.alpha_composite(t, ((PW - t.width) // 2, PH - 90))
    return im


SCENE = [
    dict(t="0:00–0:02", titolo="1 · Il gancio", img=ritaglio(BORSA, (0.18, 0.55, 0.55, 0.78)),
         ripresa="Macro sulla vernice: il telefono scorre lento da sinistra a destra e la luce "
                 "corre sul riflesso della pelle.",
         testo="«Questa luce…»", audio="Primo colpo della musica"),
    dict(t="0:02–0:05", titolo="2 · La rivelazione", img=ritaglio(BORSA, (0.14, 0.26, 0.86, 0.73), contieni=True),
         ripresa="Una mano la sfila dal ripiano del negozio e la alza verso la camera, "
                 "che indietreggia: si vede la forma intera.",
         testo="Nuova collezione", audio="Musica in crescendo"),
    dict(t="0:05–0:08", titolo="3 · In spalla", img=ritaglio(RADICE / "foto/outfit/trench-pelle-pantalone-bordeaux.jpg",
                                                            (0.15, 0.25, 0.85, 0.95)),
         ripresa="Camera a mano dietro di lei: mette la borsa in spalla e cammina tra gli "
                 "stand fino allo specchio (riferimento: questo look).",
         testo="—", audio="Passi, musica"),
    dict(t="0:08–0:10", titolo="4 · Il dettaglio", img=ritaglio(BORSA, (0.28, 0.33, 0.42, 0.47)),
         ripresa="Primissimo piano: le dita regolano la fibbia dorata del manico, "
                 "con un leggero fuoco morbido.",
         testo="Dettagli dorati", audio="Click della fibbia"),
    dict(t="0:10–0:13", titolo="5 · Il look allo specchio",
         img=ritaglio(RADICE / "foto/outfit/abito-nero-ecopelle-stivali.jpg", (0.0, 0.05, 1.0, 0.95)),
         ripresa="Selfie allo specchio del camerino con abito nero e stivali, borsa in spalla; "
                 "una piccola rotazione del busto.",
         testo="Abbinala così", audio="Musica"),
    dict(t="0:13–0:16", titolo="6 · Il finale", img=finale(),
         ripresa="La borsa viene appoggiata sul bancone bianco, la camera sale lenta; "
                 "compaiono il logo e l'indirizzo.",
         testo="Ti aspettiamo da Pakima", audio="Ultimo accordo, sfuma"),
]


def main():
    tela = Image.new("RGBA", (W, H), g.colore("#F6F4F1"))
    d = ImageDraw.Draw(tela)
    t = g.blocco_testo("Storyboard · Borsa in vernice testa di moro", ST["font_titolo"], 54, NERO, W - 100)
    tela.alpha_composite(t, (MX - 4, 50))
    s = g.blocco_testo("SPOT A MANO · REEL E TIKTOK 9:16 · 16 SECONDI · GIRATO COL TELEFONO",
                       ST["font_forte"], 20, GRIGIO, W - 100, spaziatura=3)
    tela.alpha_composite(s, (MX, 140))
    for i, sc in enumerate(SCENE):
        x = MX + (i % COL) * (PW + 40)
        y = TOP + (i // COL) * (PH + TXT_H + 40)
        d.rounded_rectangle((x - 6, y - 6, x + PW + 6, y + PH + 6), 14, fill=NERO)
        tela.alpha_composite(sc["img"], (x, y))
        tc = g.pillola(sc["t"], ST["font_forte"], 18, NERO, BIANCO)
        tela.alpha_composite(tc, (x + 12, y + 12))
        yy = y + PH + 22
        for testo, font, dim, col in [(sc["titolo"], "font_titolo", 30, NERO),
                                      ("RIPRESA", "font_forte", 15, GRIGIO),
                                      (sc["ripresa"], "font_testo", 18, NERO),
                                      ("TESTO A SCHERMO", "font_forte", 15, GRIGIO),
                                      (sc["testo"], "font_corsivo", 22, NERO),
                                      ("AUDIO", "font_forte", 15, GRIGIO),
                                      (sc["audio"], "font_testo", 18, NERO)]:
            b = g.blocco_testo(testo, ST[font], dim, col, PW, allinea="sinistra",
                               spaziatura=2 if font == "font_forte" else 0, max_righe=6)
            tela.alpha_composite(b, (x - 4, int(yy)))
            yy += b.height + (2 if font == "font_forte" else 8)
    tela.convert("RGB").save(QUI / "storyboard-borsa.png")
    print("ok", W, H)


if __name__ == "__main__":
    main()
