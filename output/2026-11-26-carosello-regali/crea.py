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


def percorso(x0, y0):
    """Punti della scia di 'o': dritta, onda, giro della morte, salita verso il testo finale."""
    pts = []
    # 1) slide 1: dritta con leggera discesa
    for x in range(int(x0), 1250, 4):
        pts.append((x, y0 + 40 * math.sin((x - x0) / 260)))
    # 2) slide 2: onda
    ya = pts[-1][1]
    for x in range(1250, 2330, 4):
        u = (x - 1250) / 1080
        pts.append((x, ya + 230 * math.sin(u * 2 * math.pi) * (1 - 0.3 * u) + 120 * u))
    # 3) slide 3: giro della morte (cerchio pulito con leggera avanzata)
    xb, yb = pts[-1]
    for x in range(int(xb), 2560, 4):
        pts.append((x, yb + (x - xb) * 0.05))
    xb, yb = pts[-1]
    R, drift = 210, 55
    cx, cy = xb, yb - R
    for i in range(0, 361, 2):
        ph = math.radians(-90 + i)
        pts.append((cx + R * math.cos(ph) + drift * i / 360, cy - R * math.sin(ph)))
    # 4) verso la slide 4: risale dolcemente e finisce dove inizia "per trovare"
    xc, yc = pts[-1]
    xe, ye = 3240 + 110, 400
    for i in range(1, 161):
        u = i / 160
        e = u * u * (3 - 2 * u)
        pts.append((xc + (xe - xc) * u, yc + (ye - yc) * e))
    return pts


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


def main():
    tela = Image.new("RGBA", (TOT, H), ROSSO + (255,))
    d = ImageDraw.Draw(tela)
    random.seed(3)
    # stelline sparse su tutto il carosello (anche a cavallo delle slide)
    for _ in range(46):
        x, y = random.randint(40, TOT - 40), random.randint(60, H - 60)
        if x > 3 * W + 100 and 280 < y < 600:
            continue
        stella(d, x, y, random.choice([6, 8, 10, 14]), (255, 225, 200, 255))

    # slide 1: testo iniziale
    f1 = font(F_CORS, 150)
    lg = g.logo(g.STILE_BASE, True, 260)
    tela.alpha_composite(lg, ((W - lg.width) // 2, 120))
    d.text((90, 470), "È il", font=font(F_CORS, 96), fill=BIANCO)
    d.text((90, 570), "moment", font=f1, fill=BIANCO)
    x_fine = 90 + d.textlength("moment", font=f1)
    y_o = 570 + 98  # centro verticale delle lettere minuscole

    # scia di "o" che continua su tutte le slide
    fo = font(F_CORS, 150)
    o = Image.new("RGBA", (120, 200), (0, 0, 0, 0))
    ImageDraw.Draw(o).text((10, 0), "o", font=fo, fill=BIANCO)
    o = o.crop(o.getbbox())
    pts = ricampiona(percorso(x_fine + o.width * 0.55, y_o), o.width * 0.86)
    for i, (x, y) in enumerate(pts):
        if i + 1 < len(pts):
            ang = -math.degrees(math.atan2(pts[i + 1][1] - y, pts[i + 1][0] - x))
        r = o.rotate(ang, resample=Image.BICUBIC, expand=True)
        tela.alpha_composite(r, (int(x - r.width / 2), int(y - r.height / 2)))

    # slide 2 e 3: piccoli testi di accompagnamento
    pass

    # slide 4: arrivo
    x4 = 3 * W
    for j, riga in enumerate(["per trovare", "il regalo perfetto"]):
        f = font(F_CORS, 96)
        d.text((x4 + 165 + j * 40, 330 + j * 110), riga, font=f, fill=BIANCO)
    foto = [("foto/prodotti/maglia-nera-paillettes-lurex.jpg", "un maglione", 6, (x4 + 40, 610)),
            ("foto/accessori/borsa-camoscio-beige-chiusura-oro.jpg", "una borsa", -4, (x4 + 370, 570)),
            ("foto/accessori/aladdin-collana-cerchi-oro-cristalli-rossi-bracciale.jpg", "un gioiello", 5, (x4 + 700, 625))]
    for p, nome, ang, (px, py) in foto:
        c = polaroid(p, 250, 300, nome, ang)
        tela.alpha_composite(c, (px - 30, py))
    fv = font(F_SANS, 30)
    t = "DA PAKIMA · VIA CAVOUR 7 · VIMERCATE"
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
