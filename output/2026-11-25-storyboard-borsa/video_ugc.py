#!/usr/bin/env python3
"""Video UGC 9:16 della borsa, che segue esattamente lo storyboard in 6 scene.

Effetto "girato col telefono": micro-tremolio della mano, deriva, zoom, messa a fuoco,
oscillazione; scritte in stile social. Solo la borsa, nessuna persona.
"""
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

QUI = Path(__file__).resolve().parent
RADICE = QUI.parents[1]
sys.path.insert(0, str(RADICE / "studio"))
import genera as g  # noqa: E402

W, H, FPS = 1080, 1920, 30
ST = dict(g.STILE_BASE)
SRC = ImageOps.exif_transpose(Image.open(RADICE / "foto/outfit/borsa-vernice-moro.jpg")).convert("RGB")
SW, SH = SRC.size
FONDO = SRC.getpixel((20, 20))


def mano(t, forza=1.0, seme=0.0):
    """Tremolio naturale della mano: somma di sinusoidi lente e veloci."""
    s = seme
    dx = (math.sin(t * 1.3 + s) * 7 + math.sin(t * 3.7 + 2 * s) * 3 + math.sin(t * 11.0 + s) * 1.2) * forza
    dy = (math.cos(t * 1.1 + s) * 6 + math.sin(t * 4.3 + s) * 2.5 + math.cos(t * 9.0 + 3 * s) * 1.0) * forza
    rot = (math.sin(t * 0.9 + s) * 0.45 + math.sin(t * 5.1 + s) * 0.12) * forza
    return dx, dy, rot


def inquadra(cx, cy, larg, t, forza=1.0, seme=0.0, extra_rot=0.0, img=None, fondo=FONDO):
    """Ritaglia un riquadro 9:16 largo `larg` px (nella foto) centrato su (cx, cy) con tremolio."""
    img = img or TELA
    dx, dy, rot = mano(t, forza, seme)
    alt = larg * H / W
    k = larg / W
    cx += dx * k * 2.2
    cy += dy * k * 2.2
    box = (cx - larg / 2, cy - alt / 2, cx + larg / 2, cy + alt / 2)
    pad = int(larg * 0.12)
    area = img.crop((int(box[0]) - pad, int(box[1]) - pad, int(box[2]) + pad, int(box[3]) + pad))
    if area.size != (int(box[2]) - int(box[0]) + 2 * pad, int(box[3]) - int(box[1]) + 2 * pad):
        pass
    area = area.rotate(rot + extra_rot, resample=Image.BICUBIC, fillcolor=fondo)
    area = area.crop((pad, pad, area.width - pad, area.height - pad))
    return area.resize((W, H), Image.BICUBIC)


def su_tela(img, fondo=FONDO):
    """Foto estesa con lo stesso fondo, così si può inquadrare oltre i bordi."""
    m = 1400
    tela = Image.new("RGB", (img.width + 2 * m, img.height + 2 * m), fondo)
    tela.paste(img, (m, m))
    return tela, m


TELA, M = su_tela(SRC)
# posizioni chiave nella foto (frazioni)
BORSA_C = (0.5 * SW + M, 0.50 * SH + M)       # centro borsa
VERNICE = (0.32 * SW + M, 0.66 * SH + M)      # riflessi lato sinistro
FIBBIA = (0.345 * SW + M, 0.40 * SH + M)      # fibbia dorata
MANICO = (0.5 * SW + M, 0.33 * SH + M)        # cima del manico


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def luce_che_corre(fr, p):
    """Riflesso di luce che scorre sulla vernice (scena 1)."""
    ov = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(ov)
    x = -400 + p * (W + 800)
    d.polygon([(x, 0), (x + 160, 0), (x - 340, H), (x - 500, H)], fill=70)
    ov = ov.filter(ImageFilter.GaussianBlur(60))
    bianco = Image.new("RGB", (W, H), (255, 255, 255))
    return Image.composite(bianco, fr, ov)


def scritta(testo, dim=64):
    """Scritta stile social: bianca, corsiva elegante, con ombra morbida."""
    return g.blocco_testo(testo, ST["font_corsivo"], dim, g.colore("#FFFFFF"), W - 160, ombra=True)


SCENE = [  # (durata, funzione(t, p) -> frame RGB, testo)
]


def s1(t, p):
    cx = VERNICE[0] - 90 + 180 * ease(p)
    fr = inquadra(cx, VERNICE[1], 430, t, 1.2, 0.3)
    return luce_che_corre(fr, p)


def s2(t, p):
    larg = 520 + (SW * 0.95 - 520) * ease(p * 1.15)
    cy = VERNICE[1] + (BORSA_C[1] - VERNICE[1]) * ease(p * 1.15)
    return inquadra(BORSA_C[0], cy, larg, t, 1.3, 1.1)


def s3(t, p):
    # mezzo giro attorno: spostamento laterale + leggera prospettiva + rotazione
    larg = SW * 0.82
    cx = BORSA_C[0] + (-120 + 240 * ease(p))
    fr = inquadra(cx, BORSA_C[1] + 60, larg, t, 1.4, 2.2, extra_rot=(-2 + 4 * ease(p)))
    sk = (0.5 - ease(p)) * 0.08
    return fr.transform((W, H), Image.AFFINE, (1, sk, -sk * H / 2, 0, 1, 0), resample=Image.BICUBIC, fillcolor=FONDO)


def s4(t, p):
    fr = inquadra(FIBBIA[0], FIBBIA[1], 300, t, 0.9, 3.3)
    sfoc = max(0.0, 6 * (1 - ease(p * 2.2)))  # messa a fuoco
    return fr.filter(ImageFilter.GaussianBlur(sfoc)) if sfoc > 0.2 else fr


def s5(t, p):
    # appesa che oscilla + camera che sale dal fondo al manico
    ang = math.sin(t * 2.4) * 2.2 * (1 - 0.5 * p)
    cy = (BORSA_C[1] + 260) + (MANICO[1] - (BORSA_C[1] + 260)) * ease(p)
    return inquadra(BORSA_C[0], cy, SW * 0.78, t, 1.0, 4.4, extra_rot=ang)


def s6(t, p):
    fr = Image.new("RGB", (W, H), (255, 255, 255))
    borsa = SRC.crop((int(0.12 * SW), int(0.25 * SH), int(0.88 * SW), int(0.74 * SH)))
    borsa = ImageOps.contain(borsa, (int(W * 0.86), int(H * 0.5)))
    # togli il grigio di fondo per fonderla col bianco
    px = borsa.load()
    for yy in range(borsa.height):
        for xx in range(borsa.width):
            r, gg, b = px[xx, yy]
            if min(r, gg, b) > 205 and max(r, gg, b) - min(r, gg, b) < 14:
                px[xx, yy] = (255, 255, 255)
    y = int(H * 0.30 - 60 * ease(p))
    fr.paste(borsa, ((W - borsa.width) // 2, y))
    dx, dy, rot = mano(t, 0.8, 5.5)
    fr = fr.rotate(rot, resample=Image.BICUBIC, fillcolor=(255, 255, 255), translate=(dx, dy))
    out = fr.convert("RGBA")
    lg = g.logo(ST, False, 360)
    a = ease((p - 0.15) / 0.4)
    if a > 0:
        lg2 = lg.copy(); lg2.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
        out.alpha_composite(lg2, ((W - lg.width) // 2, 230))
        ind = g.blocco_testo("VIA CAVOUR 7 · VIMERCATE", ST["font_forte"], 34, g.colore("#111111"), W - 120, spaziatura=6)
        ind2 = ind.copy(); ind2.putalpha(ind.getchannel("A").point(lambda v: int(v * a)))
        out.alpha_composite(ind2, ((W - ind.width) // 2, int(H * 0.30) + int(H * 0.5) + 10))
    return out.convert("RGB")


SCENE = [
    (2.0, s1, "Questa luce…"),
    (3.0, s2, "Nuova collezione"),
    (3.0, s3, "Linea morbida"),
    (2.0, s4, "Dettagli dorati"),
    (3.0, s5, "Testa di moro"),
    (3.0, s6, "Ti aspettiamo da Pakima"),
]


def main():
    out = QUI / "video-ugc-borsa.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-vf", "noise=alls=5:allf=t,eq=contrast=1.04:saturation=1.05",
           "-map", "0:v", "-map", "1:a", "-shortest",
           "-c:v", "libx264", "-b:v", "4500k", "-maxrate", "6000k", "-bufsize", "9000k", "-profile:v", "main", "-preset", "slow", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t_glob = 0.0
    for i, (dur, fn, testo) in enumerate(SCENE):
        n = int(dur * FPS)
        cap = scritta(testo, 70 if i < 5 else 62)
        for f in range(n):
            t = t_glob + f / FPS
            p = f / max(n - 1, 1)
            fr = fn(t, p).convert("RGBA")
            if i < 5:  # nel finale il testo lo fanno logo e indirizzo
                a = ease((f / FPS - 0.15) / 0.35)
                if a > 0:
                    c2 = cap.copy(); c2.putalpha(cap.getchannel("A").point(lambda v: int(v * a)))
                    fr.alpha_composite(c2, ((W - cap.width) // 2, int(H * 0.70)))
            else:
                a = ease((p - 0.35) / 0.35)
                if a > 0:
                    c2 = g.blocco_testo(testo, ST["font_corsivo"], 62, g.colore("#111111"), W - 160)
                    c3 = c2.copy(); c3.putalpha(c2.getchannel("A").point(lambda v: int(v * a)))
                    fr.alpha_composite(c3, ((W - c2.width) // 2, int(H * 0.86)))
            # taglio netto tra scene (stile UGC) con un micro flash nei primi 2 fotogrammi
            if f < 2 and i > 0:
                fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.25 if f == 0 else 0.1)
            proc.stdin.write(fr.convert("RGB").tobytes())
        t_glob += dur
    proc.stdin.close()
    proc.wait()
    print("ok", out)


if __name__ == "__main__":
    main()
