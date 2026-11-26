#!/usr/bin/env python3
"""Carosello continuo di Natale (trend "It's timeeee"): la scritta prosegue da una slide all'altra."""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

QUI = Path(__file__).resolve().parent
RADICE = QUI.parents[1]
sys.path.insert(0, str(RADICE / "studio"))
import genera as g  # noqa: E402

W, H, N = 1080, 1350, 4
TOT = W * N
ROSSO = (168, 18, 30)
BIANCO = (255, 255, 255)
CREMA = (250, 244, 236)
F_CORS = str(RADICE / "studio/font/PlayfairDisplay-Italic.ttf")
F_TIT = str(RADICE / "studio/font/PlayfairDisplay-SemiBold.ttf")
F_SANS = str(RADICE / "studio/font/Montserrat-SemiBold.ttf")


def font(p, s):
    return ImageFont.truetype(p, int(s))


def stella(d, cx, cy, r, col):
    k = r * 0.28
    d.polygon([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
               (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], fill=col)


def catmull(pts, n=40):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def percorso(x0, y0):
    """Scia di 'e': dritta nella slide 1, poi onda morbida, giro della morte, arrivo sul testo finale."""
    c = [(x0, y0), (700, y0), (1000, y0), (1150, y0 + 15),
         (1330, y0 + 110), (1530, y0 + 200), (1750, y0 + 170), (1950, y0 + 40), (2150, y0 - 10),
         (2380, y0 + 80), (2600, y0 + 150), (2800, y0 + 20), (2770, y0 - 230), (2580, y0 - 280),
         (2440, y0 - 120), (2560, y0 + 90), (2780, y0 + 170), (3020, y0 + 120), (3200, y0 - 60),
         (3320, 420), (3380, 395)]
    return catmull(c, 60)


def ricampiona(pts, passo):
    out, acc = [pts[0]], 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = math.hypot(x2 - x1, y2 - y1)
        while acc + seg >= passo:
            t = (passo - acc) / seg
            x1, y1 = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            out.append((x1, y1))
            seg = math.hypot(x2 - x1, y2 - y1)
            acc = 0.0
        acc += seg
    return out


def polaroid(percorso_foto, w, h, didascalia, ang):
    pad, basso = 22, 92
    card = Image.new("RGBA", (w + 2 * pad, h + pad + basso), CREMA + (255,))
    im = ImageOps.exif_transpose(Image.open(RADICE / percorso_foto)).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.45))
    card.paste(im, (pad, pad))
    d = ImageDraw.Draw(card)
    f = font(F_CORS, 40)
    tw = d.textlength(didascalia, font=f)
    d.text(((card.width - tw) / 2, h + pad + 18), didascalia, font=f, fill=(40, 30, 30))
    ombra = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    ombra.paste(Image.new("RGBA", card.size, (0, 0, 0, 110)), (30, 38))
    ombra = ombra.filter(ImageFilter.GaussianBlur(14))
    ombra.alpha_composite(card, (30, 30))
    return ombra.rotate(ang, resample=Image.BICUBIC, expand=True)


def disegna_natale(tela):
    K = 3
    lay = Image.new("RGBA", (W * K, 500 * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    B, ORO = (255, 255, 255, 255), (240, 205, 130, 255)
    # albero: tre livelli, tronco, stella, palline "bucate" nel colore dello sfondo
    tx, base_y = 250 * K, 470 * K
    d.rectangle((tx - 18 * K, base_y - 50 * K, tx + 18 * K, base_y), fill=B)
    for j, (w, h, y) in enumerate([(300, 150, 400), (230, 140, 300), (160, 130, 205)]):
        d.polygon([(tx - w / 2 * K, y * K), (tx + w / 2 * K, y * K), (tx, (y - h) * K)], fill=B)
    for (px, py) in [(-70, 375), (60, 360), (-20, 300), (50, 255), (-45, 230), (10, 180), (95, 385), (-110, 390)]:
        d.ellipse(((tx + px * K) - 11 * K, py * K - 11 * K, (tx + px * K) + 11 * K, py * K + 11 * K), fill=ROSSO + (255,))
    stella(d, tx, 70 * K, 34 * K, ORO)
    # renna (silhouette elegante, guarda a sinistra)
    ox, oy = 560 * K, 70 * K
    def P(x, y):
        return (ox + x * K, oy + y * K)
    def tratto(punti, w):
        q = [P(*p) for p in punti]
        d.line(q, fill=B, width=int(w * K), joint="curve")
        for (x, y) in (q[0], q[-1]):
            r = w * K / 2
            d.ellipse((x - r, y - r, x + r, y + r), fill=B)
    # corpo
    d.ellipse((*P(140, 215), *P(345, 305)), fill=B)
    d.ellipse((*P(130, 205), *P(215, 290)), fill=B)          # petto
    # collo slanciato e testa
    tratto([(175, 240), (150, 190), (125, 150)], 52)
    d.ellipse((*P(78, 118), *P(150, 168)), fill=B)            # testa
    tratto([(92, 150), (55, 160)], 30)                        # muso
    d.ellipse((*P(38, 150), *P(58, 170)), fill=ORO)           # naso
    d.ellipse((*P(100, 132), *P(111, 143)), fill=ROSSO + (255,))  # occhio
    d.polygon([P(140, 128), P(178, 108), P(150, 145)], fill=B)    # orecchio
    # corna ramificate
    for pts, w in [([(112, 122), (100, 80), (82, 45), (70, 15)], 9), ([(96, 72), (66, 62)], 8), ([(86, 52), (104, 22)], 8),
                   ([(128, 120), (140, 78), (158, 46), (180, 22)], 9), ([(141, 76), (176, 70)], 8), ([(153, 54), (148, 22)], 8)]:
        tratto(pts, w)
    # zampe (una sollevata, come in cammino)
    tratto([(170, 285), (158, 340), (164, 400)], 15)
    tratto([(200, 290), (214, 335), (196, 372), (186, 392)], 15)
    tratto([(305, 288), (318, 340), (312, 400)], 15)
    tratto([(330, 280), (352, 335), (348, 398)], 15)
    # zoccoli
    for (x, y) in [(164, 400), (186, 392), (312, 400), (348, 398)]:
        d.ellipse((*P(x - 11, y - 4), *P(x + 11, y + 10)), fill=ORO)
    # coda
    d.polygon([P(338, 225), P(372, 205), P(356, 240)], fill=B)
    lay = lay.resize((W, 500), Image.LANCZOS)
    tela.alpha_composite(lay, (0, 800))


def main():
    tela = Image.new("RGBA", (TOT, H), ROSSO + (255,))
    d = ImageDraw.Draw(tela)
    random.seed(3)
    # stelline sparse su tutto il carosello (anche a cavallo delle slide)
    for _ in range(46):
        x, y = random.randint(40, TOT - 40), random.randint(60, H - 60)
        if x > 3 * W + 100 and 280 < y < 600:
            continue
        if x < W and 430 < y < 790:
            continue
        stella(d, x, y, random.choice([6, 8, 10, 14]), (255, 225, 200, 255))

    # slide 1: testo iniziale
    f1 = font(F_CORS, 150)
    lg = g.logo(g.STILE_BASE, True, 260)
    tela.alpha_composite(lg, ((W - lg.width) // 2, 120))
    d.text((90, 470), "It's", font=font(F_CORS, 96), fill=BIANCO)
    d.text((90, 570), "Tim", font=f1, fill=BIANCO)
    x_fine = 90 + d.textlength("Tim", font=f1)
    y_o = 570 + 98  # centro verticale delle lettere minuscole

    # scia di "e": grande e dritta nella slide 1, poi piu piccola e fluida
    fo = font(F_CORS, 150)
    base = Image.new("RGBA", (120, 200), (0, 0, 0, 0))
    ImageDraw.Draw(base).text((10, 0), "e", font=fo, fill=BIANCO)
    base = base.crop(base.getbbox())
    dense = percorso(x_fine + base.width * 0.5, y_o)
    def scala(x):
        u = max(0.0, min(1.0, (x - 980) / 420))
        return 1 - 0.42 * (u * u * (3 - 2 * u))
    acc, prossimo = 0.0, 0.0
    for i in range(1, len(dense)):
        (x1, y1), (x2, y2) = dense[i - 1], dense[i]
        acc += math.hypot(x2 - x1, y2 - y1)
        if acc >= prossimo:
            sc = scala(x2)
            ang = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            e = base.resize((max(1, int(base.width * sc)), max(1, int(base.height * sc))), Image.LANCZOS)
            r = e.rotate(ang, resample=Image.BICUBIC, expand=True)
            tela.alpha_composite(r, (int(x2 - r.width / 2), int(y2 - r.height / 2)))
            prossimo = acc + base.width * sc * 0.82

    # albero di Natale e renna (slide 1, in basso)
    disegna_natale(tela)

    # slide 2 e 3: piccoli testi di accompagnamento
    pass

    # slide 4: arrivo
    x4 = 3 * W
    for j, riga in enumerate(["to find you", "the perfect gift"]):
        f = font(F_CORS, 96)
        d.text((x4 + 165 + j * 40, 330 + j * 110), riga, font=f, fill=BIANCO)
    foto = [("foto/ai/regalo-maglione-nero-paillettes.png", "un maglione", 6, (x4 + 40, 610)),
            ("foto/ai/regalo-borsa-beige.png", "una borsa", -4, (x4 + 370, 570)),
            ("foto/ai/regalo-collane-cristalli.png", "un gioiello", 5, (x4 + 700, 625))]
    for p, nome, ang, (px, py) in foto:
        c = polaroid(p, 250, 300, nome, ang)
        tela.alpha_composite(c, (px - 30, py))
    fv = font(F_SANS, 30)
    t = "PAKIMA · VIA CAVOUR 7 · VIMERCATE"
    sp = 5
    tw = sum(fv.getlength(ch) + sp for ch in t) - sp
    x = x4 + (W - tw) / 2
    for ch in t:
        d.text((x, 1205), ch, font=fv, fill=BIANCO)
        x += fv.getlength(ch) + sp

    for k in range(N):
        tela.crop((k * W, 0, (k + 1) * W, H)).convert("RGB").save(QUI / f"{k + 1}.png")
    tela.convert("RGB").resize((TOT // 4, H // 4)).save(QUI / "anteprima-intera.png")
    print("ok")


if __name__ == "__main__":
    main()
