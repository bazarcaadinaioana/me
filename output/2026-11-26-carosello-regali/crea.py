#!/usr/bin/env python3
"""Carosello continuo di Natale "It's timeeee…": la scritta prosegue da una slide all'altra.

Slide 1: "It's time" + scia di "e" (stesso carattere, scende morbida poi va dritta), alberello luminoso
di particelle dorate, palline appese, fiocchi dorati. Slide 2-3: la scia ondeggia e fa un giro.
Slide 4: "to find you the perfect gift" + 3 polaroid regalo.
"""
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
ROSSO = (150, 16, 24)
BIANCO = (255, 255, 255)
CREMA = (250, 244, 236)
ORO = (240, 196, 120)
F_SANS = str(RADICE / "studio/font/Montserrat-SemiBold.ttf")
F_TIT = F_CORS_T = None
F_CORS = str(RADICE / "studio/font/PlayfairDisplay-Italic.ttf")


def font(p, s):
    return ImageFont.truetype(p, int(s))


# ---------------------------------------------------------------- decori

def sfondo():
    """Lo sfondo rosso con fiocchi e stelline della titolare, su ogni slide (una si, una no specchiato)."""
    bg = Image.open(RADICE / "foto/ai/natale-sfondo-fiocchi.png").convert("RGBA")
    bg = ImageOps.fit(bg, (W, H), Image.LANCZOS)
    tela = Image.new("RGBA", (TOT, H))
    for k in range(N):
        tela.paste(bg if k % 2 == 0 else ImageOps.mirror(bg), (k * W, 0))
    return tela


def decoro(tela, file, larg, x, y):
    im = Image.open(RADICE / file).convert("RGBA")
    im = im.resize((larg, int(im.height * larg / im.width)), Image.LANCZOS)
    tela.alpha_composite(im, (int(x), int(y)))
    return im.size


def fiocco(d, cx, cy, r, col, w=2):
    for k in range(6):
        a = math.radians(60 * k)
        d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], fill=col, width=w)
        for f in (0.45, 0.7):
            bx, by = cx + r * f * math.cos(a), cy + r * f * math.sin(a)
            for s in (-1, 1):
                b = a + s * math.radians(40)
                d.line([(bx, by), (bx + r * 0.25 * math.cos(b), by + r * 0.25 * math.sin(b))], fill=col, width=w)


def fiocchi(tela, n, seme, zone_vietate):
    random.seed(seme)
    lay = Image.new("RGBA", tela.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    messi = 0
    while messi < n:
        x, y = random.randint(40, TOT - 40), random.randint(40, H - 40)
        if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in zone_vietate):
            continue
        r = random.choice([14, 18, 24, 34, 46])
        fiocco(d, x, y, r, ORO + (int(random.uniform(45, 95)),), 2 if r < 30 else 3)
        messi += 1
    tela.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))


def alberello(tela, apex_x, apex_y, altezza, base_w, seme=5):
    """Albero luminoso fatto di particelle dorate, con bagliore e bokeh alla base."""
    random.seed(seme)
    K = 2
    lw, lh = int(base_w * 1.7), int(altezza * 1.3)
    lay = Image.new("RGBA", (lw * K, lh * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, top = lw * K / 2, 40 * K

    def punto(x, y, r, a):
        c = (255, random.randint(205, 235), random.randint(140, 190), int(max(0, min(255, a))))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)

    for _ in range(2600):  # spirale di luci attorno al cono
        t = random.random() ** 0.8
        y = top + t * altezza * K
        ang = t * 9 * math.pi + random.uniform(-0.35, 0.35)
        x = cx + t * base_w / 2 * K * math.sin(ang) + random.gauss(0, 6 * K)
        prof = (math.cos(ang) + 1) / 2
        punto(x, y + random.gauss(0, 4 * K), random.choice([1, 1, 1.5, 2, 2.5, 3]) * K * (0.6 + 0.6 * prof),
              random.uniform(90, 255) * (0.45 + 0.55 * prof))
    for _ in range(2200):  # riempimento morbido del cono
        t = random.random() ** 0.7
        punto(cx + random.uniform(-1, 1) * t * base_w / 2 * K, top + t * altezza * K,
              random.choice([0.8, 1, 1.4]) * K, random.uniform(40, 150))
    for _ in range(1400):  # polvere dorata alla base
        punto(cx + random.gauss(0, base_w * 0.55) * K, top + altezza * K + abs(random.gauss(0, 30)) * K - 10 * K,
              random.choice([1, 1.5, 2, 3]) * K, random.uniform(60, 220))
    bok = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    db = ImageDraw.Draw(bok)
    for _ in range(40):  # bokeh
        t = random.random()
        x = cx + random.uniform(-1, 1) * (t * base_w / 2 + 60) * K
        y = top + t * altezza * K + random.uniform(-20, 60) * K
        r = random.uniform(5, 14) * K
        db.ellipse((x - r, y - r, x + r, y + r), fill=(255, 215, 150, random.randint(40, 110)))
    bok = bok.filter(ImageFilter.GaussianBlur(3 * K))
    glow = lay.filter(ImageFilter.GaussianBlur(9 * K))
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(glow)
    out.alpha_composite(bok)
    out.alpha_composite(lay)
    ds = ImageDraw.Draw(out)  # stella-scintilla in cima
    r = 26 * K
    for a, l in [(0, 1), (90, 1.2), (45, 0.45), (135, 0.45)]:
        aa = math.radians(a)
        dx, dy = math.cos(aa) * r * l, math.sin(aa) * r * l
        ds.line([(cx - dx, top - dy), (cx + dx, top + dy)], fill=(255, 240, 210, 255), width=2 * K)
    out = out.resize((lw, lh), Image.LANCZOS)
    tela.alpha_composite(out, (int(apex_x - lw / 2), int(apex_y - 40)))


def pallina(tela, cx, y_centro, r, tipo):
    """Pallina di Natale appesa a un filo, con riflesso e ombra."""
    K = 3
    S = int(r * 2 * K + 40 * K)
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c, R = S / 2, r * K
    base = {"oro": (200, 148, 62), "perla": (226, 216, 200), "rossa": (110, 8, 18)}[tipo]
    luce = {"oro": (255, 240, 190), "perla": (255, 255, 252), "rossa": (235, 95, 105)}[tipo]
    for i in range(80, 0, -1):
        f = i / 80
        col = tuple(int(base[j] * f + luce[j] * (1 - f)) for j in range(3))
        rr = R * f
        ox, oy = -R * 0.32 * (1 - f), -R * 0.36 * (1 - f)
        d.ellipse((c + ox - rr, c + oy - rr, c + ox + rr, c + oy + rr), fill=col + (255,))
    bordo = Image.new("L", (S, S), 0)
    ImageDraw.Draw(bordo).ellipse((c - R, c - R, c + R, c + R), outline=110, width=int(R * 0.16))
    scuro = Image.new("RGBA", (S, S), (50, 12, 10, 255))
    scuro.putalpha(bordo.filter(ImageFilter.GaussianBlur(R * 0.1)))
    lay.alpha_composite(scuro)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((c - R, c - R, c + R, c + R), fill=255)
    lay.putalpha(mask)
    dc = ImageDraw.Draw(lay)  # cappuccio dorato
    dc.rounded_rectangle((c - R * 0.22, c - R - R * 0.2, c + R * 0.22, c - R + R * 0.08), R * 0.05, fill=(205, 165, 90, 255))
    lay = lay.resize((S // K, S // K), Image.LANCZOS)
    om = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    om.putalpha(lay.getchannel("A").point(lambda v: int(v * 0.45)))
    om = om.filter(ImageFilter.GaussianBlur(10))
    ImageDraw.Draw(tela).line([(cx, 0), (cx, y_centro - r * 1.15)], fill=(225, 190, 130, 255), width=2)
    tela.alpha_composite(om, (int(cx - lay.width / 2 + 8), int(y_centro - lay.height / 2 + 14)))
    tela.alpha_composite(lay, (int(cx - lay.width / 2), int(y_centro - lay.height / 2)))


# ---------------------------------------------------------------- scia di "e"

def catmull(pts, n=50):
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
    """Scende morbida subito dopo "time", poi dritta; onda nella slide 2, giro nella 3, arrivo nella 4."""
    c = [(x0, y0), (x0 + 110, y0 + 28), (x0 + 240, y0 + 90), (x0 + 390, y0 + 125), (x0 + 560, y0 + 138), (x0 + 720, y0 + 140),
         (1300, y0 + 150), (1500, y0 + 230), (1720, y0 + 250), (1930, y0 + 150), (2150, y0 + 90),
         (2380, y0 + 140), (2600, y0 + 170), (2800, y0 + 40), (2770, y0 - 190), (2580, y0 - 240),
         (2440, y0 - 90), (2560, y0 + 110), (2790, y0 + 180), (3030, y0 + 120), (3200, y0 - 40),
         (3320, 440), (3375, 420)]
    return catmull(c, 70)


def scia(tela, f, x0, y0):
    base = Image.new("RGBA", (220, 240), (0, 0, 0, 0))
    ImageDraw.Draw(base).text((10, 0), "e", font=f, fill=BIANCO)
    base = base.crop(base.getbbox())
    larg = f.getlength("e")
    pts = percorso(x0 + larg / 2, y0)
    acc, prossimo = 0.0, 0.0
    for i in range(1, len(pts)):
        (x1, y1), (x2, y2) = pts[i - 1], pts[i]
        acc += math.hypot(x2 - x1, y2 - y1)
        if acc >= prossimo:
            ang = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            r = base.rotate(ang, resample=Image.BICUBIC, expand=True)
            tela.alpha_composite(r, (int(x2 - r.width / 2), int(y2 - r.height / 2)))
            prossimo = acc + larg * 0.98


# ---------------------------------------------------------------- polaroid

def polaroid(percorso_foto, w, h, didascalia, ang):
    pad, basso = 22, 92
    card = Image.new("RGBA", (w + 2 * pad, h + pad + basso), CREMA + (255,))
    im = ImageOps.exif_transpose(Image.open(RADICE / percorso_foto)).convert("RGB")
    card.paste(ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.45)), (pad, pad))
    d = ImageDraw.Draw(card)
    f = font(F_CORS, 40)
    tw = d.textlength(didascalia, font=f)
    d.text(((card.width - tw) / 2, h + pad + 18), didascalia, font=f, fill=(40, 30, 30))
    ombra = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    ombra.paste(Image.new("RGBA", card.size, (0, 0, 0, 110)), (30, 38))
    ombra = ombra.filter(ImageFilter.GaussianBlur(14))
    ombra.alpha_composite(card, (30, 30))
    return ombra.rotate(ang, resample=Image.BICUBIC, expand=True)


# ---------------------------------------------------------------- composizione

def main():
    tela = sfondo()
    x4 = 3 * W

    # slide 1
    f1 = font(F_CORS, 160)
    d = ImageDraw.Draw(tela)
    tela.alpha_composite(g.logo(g.STILE_BASE, True, 340), (70, 90))
    y_its = 420
    d.text((110, y_its), "It's", font=font(F_CORS, 120), fill=BIANCO)
    y_time = y_its + 130
    d.text((110, y_time), "time", font=f1, fill=BIANCO)
    x_fine = 110 + d.textlength("time", font=f1)
    bb = f1.getbbox("e")
    scia(tela, f1, x_fine + 4, y_time + (bb[1] + bb[3]) / 2)
    decoro(tela, "foto/ai/natale-palline-trasp.png", 400, W - 400 + 10, -30)
    decoro(tela, "foto/ai/natale-albero-dorato-trasp.png", 580, -80, H - 580 * 1312 / 1199 + 40)

    # slide 4
    for j, riga in enumerate(["to find you", "the perfect gift"]):
        d.text((x4 + 160 + j * 40, 320 + j * 110), riga, font=font(F_CORS, 100), fill=BIANCO)
    foto = [("foto/ai/regalo-maglione-nero-paillettes.png", "un maglione", 6, (x4 + 40, 610)),
            ("foto/ai/regalo-borsa-beige.png", "una borsa", -4, (x4 + 370, 570)),
            ("foto/ai/regalo-collane-cristalli.png", "un gioiello", 5, (x4 + 700, 625))]
    for p, nome, ang, (px, py) in foto:
        tela.alpha_composite(polaroid(p, 250, 300, nome, ang), (px - 30, py))
    fv = font(F_SANS, 30)
    t, sp = "PAKIMA · VIA CAVOUR 7 · VIMERCATE", 5
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
