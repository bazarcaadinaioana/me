#!/usr/bin/env python3
"""Generatore di video e grafiche per i social del negozio.

Uso:
    python3 studio/genera.py video  scheda-video.json   [-o uscita.mp4]
    python3 studio/genera.py grafica scheda-grafica.json [-o uscita.png]

Le schede sono file JSON (vedi studio/esempi/ e studio/LEGGIMI.md).
Serve solo Python con Pillow e ffmpeg: niente crediti, niente limiti.
"""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent
FONT = QUI / "font"

FORMATI = {
    "storia": (1080, 1920),   # reel, storie, TikTok
    "reel": (1080, 1920),
    "post": (1080, 1350),     # post Instagram 4:5
    "quadrato": (1080, 1080),
}

STILE_BASE = {
    "sfondo": "#F3EDE4",   # colore dei pannelli e delle scene di solo testo
    "testo": "#2A2522",    # testo sui pannelli chiari
    "accento": "#A8744F",  # etichette, linee
    "chiaro": "#FFFFFF",   # testo sopra le foto
    "font_titolo": "PlayfairDisplay-SemiBold.ttf",
    "font_testo": "Montserrat-Regular.ttf",
    "font_forte": "Montserrat-SemiBold.ttf",
}

FPS = 30
TRANSIZIONE = 0.45  # secondi di dissolvenza tra le scene


# ---------------------------------------------------------------- utilità

def colore(c, alpha=255):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def font(nome, dim):
    p = FONT / nome
    if not p.exists():
        p = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(str(p), int(dim))


def trova_file(percorso, base):
    for cand in (base / percorso, RADICE / percorso, Path(percorso)):
        if cand.exists():
            return cand
    sys.exit(f"File non trovato: {percorso}")


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def larghezza(testo, f, spaziatura=0):
    if not testo:
        return 0
    return f.getlength(testo) + spaziatura * (len(testo) - 1)


def a_capo(testo, f, max_w, spaziatura=0):
    righe = []
    for paragrafo in str(testo).split("\n"):
        parole, riga = paragrafo.split(), ""
        for p in parole:
            prova = (riga + " " + p).strip()
            if larghezza(prova, f, spaziatura) <= max_w or not riga:
                riga = prova
            else:
                righe.append(riga)
                riga = p
        righe.append(riga)
    return righe


def blocco_testo(testo, nome_font, dim, fill, max_w, allinea="centro",
                 interlinea=1.18, spaziatura=0, max_righe=4, ombra=False):
    """Crea un'immagine RGBA con il testo a capo; riduce il font se non ci sta."""
    while True:
        f = font(nome_font, dim)
        righe = a_capo(testo, f, max_w, spaziatura)
        if (len(righe) <= max_righe and all(larghezza(r, f, spaziatura) <= max_w for r in righe)) or dim < 20:
            break
        dim *= 0.92
    asc, desc = f.getmetrics()
    h_riga = int((asc + desc) * interlinea)
    pad = int(dim * 0.6) if ombra else 4
    w = int(max(larghezza(r, f, spaziatura) for r in righe)) + 2 * pad
    h = h_riga * len(righe) + 2 * pad
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def disegna(dr, col):
        for i, r in enumerate(righe):
            rw = larghezza(r, f, spaziatura)
            x = pad + {"sinistra": 0, "destra": w - 2 * pad - rw}.get(allinea, (w - 2 * pad - rw) / 2)
            y = pad + i * h_riga
            if spaziatura:
                for ch in r:
                    dr.text((x, y), ch, font=f, fill=col)
                    x += f.getlength(ch) + spaziatura
            else:
                dr.text((x, y), r, font=f, fill=col)

    if ombra:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        disegna(ImageDraw.Draw(sh), (0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(dim * 0.12))
        img = Image.alpha_composite(img, sh)
        d = ImageDraw.Draw(img)
    disegna(d, fill)
    return img


def etichetta(testo, stile, dim):
    f = font(stile["font_forte"], dim)
    sp = dim * 0.12
    tw = larghezza(testo.upper(), f, sp)
    asc, desc = f.getmetrics()
    px, py = dim * 0.9, dim * 0.55
    w, h = int(tw + 2 * px), int(asc + desc + 2 * py)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=colore(stile["accento"]))
    x = px
    for ch in testo.upper():
        d.text((x, py), ch, font=f, fill=colore(stile["chiaro"]))
        x += f.getlength(ch) + sp
    return img


def sfumatura(w, h, alto, forza=0.72):
    """Velo scuro graduale per rendere leggibile il testo sopra la foto."""
    g = Image.new("L", (1, 256))
    for y in range(256):
        v = (y / 255) if not alto else (1 - y / 255)
        g.putpixel((0, y), int(255 * forza * ease_in_out(v) ** 1.3))
    g = g.resize((w, h))
    velo = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    velo.putalpha(g)
    return velo


# ---------------------------------------------------------------- foto in movimento

class FotoMobile:
    """Effetto 'Ken Burns': zoom e panoramica lenti su una foto."""

    def __init__(self, percorso, w, h, effetto="zoom-in", fuoco="centro"):
        img = ImageOps.exif_transpose(Image.open(percorso)).convert("RGB")
        self.w, self.h, self.effetto = w, h, effetto
        margine = 1.16
        scala = max(w * margine / img.width, h * margine / img.height)
        self.img = img.resize((math.ceil(img.width * scala), math.ceil(img.height * scala)), Image.LANCZOS)
        self.fy = {"alto": 0.3, "basso": 0.7}.get(fuoco, 0.5)

    def frame(self, p):
        bw, bh = self.img.size
        e = self.effetto
        z = 1.0
        cx, cy = 0.5, self.fy
        if e == "zoom-in":
            z = 1.0 + 0.15 * p
        elif e == "zoom-out":
            z = 1.15 - 0.15 * p
        elif e in ("pan-destra", "pan-sinistra"):
            z = 1.06
            cx = 0.35 + 0.3 * p if e == "pan-destra" else 0.65 - 0.3 * p
        elif e in ("pan-alto", "pan-basso"):
            z = 1.06
            cy = 0.65 - 0.3 * p if e == "pan-alto" else 0.35 + 0.3 * p
        cw, ch = bw / z, bh / z
        # mantiene le proporzioni del riquadro di uscita
        if cw / ch > self.w / self.h:
            cw = ch * self.w / self.h
        else:
            ch = cw * self.h / self.w
        x0 = min(max(cx * bw - cw / 2, 0), bw - cw)
        y0 = min(max(cy * bh - ch / 2, 0), bh - ch)
        return self.img.transform((self.w, self.h), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BILINEAR).convert("RGBA")


# ---------------------------------------------------------------- scene

class Elemento:
    def __init__(self, img, x, y, ritardo, durata=0.6, salita=36):
        self.img, self.x, self.y = img, int(x), int(y)
        self.ritardo, self.durata, self.salita = ritardo, durata, salita

    def applica(self, frame, t):
        k = ease_out((t - self.ritardo) / self.durata) if self.durata else 1
        if k <= 0:
            return
        img = self.img
        if k < 1:
            a = img.getchannel("A").point(lambda v: int(v * k))
            img = img.copy()
            img.putalpha(a)
        frame.alpha_composite(img, (self.x, self.y + int(self.salita * (1 - k))))


class Scena:
    def __init__(self, dati, W, H, stile, base, video=True):
        self.W, self.H, self.stile = W, H, stile
        self.durata = float(dati.get("durata", 3))
        self.tipo = dati.get("tipo", "foto")
        self.elementi = []
        self.foto = None
        self.sfondo = None
        self.velo_alto = None
        effetto = dati.get("effetto", "zoom-in") if video else "fermo"

        # margini "sicuri": nei reel le scritte di Instagram coprono sopra e sotto
        alto_sicuro = int(H * 0.11) if H > W * 1.5 else int(H * 0.07)
        basso_sicuro = int(H * 0.20) if H > W * 1.5 else int(H * 0.08)
        margine = int(W * 0.08)
        max_w = W - 2 * margine
        U = W / 1080  # unità di scala

        titolo = dati.get("testo", "")
        sotto = dati.get("sottotesto", "")
        badge = dati.get("etichetta", "")
        marchio = dati.get("marchio", "")
        posizione = dati.get("posizione", "basso")

        if self.tipo == "foto":
            self.foto = FotoMobile(trova_file(dati["foto"], base), W, H, effetto, dati.get("fuoco", "centro"))
            if titolo or sotto:
                self.sfondo = sfumatura(W, H, alto=(posizione == "alto"))
            col = colore(stile["chiaro"])
            ombra = True
        elif self.tipo == "pannello":
            hf = int(H * dati.get("altezza_foto", 0.62))
            self.foto = FotoMobile(trova_file(dati["foto"], base), W, hf, effetto, dati.get("fuoco", "centro"))
            self.sfondo = Image.new("RGBA", (W, H), colore(stile["sfondo"]))
            col = colore(stile["testo"])
            ombra = False
        else:  # testo
            self.sfondo = Image.new("RGBA", (W, H), colore(stile["sfondo"]))
            col = colore(stile["testo"])
            ombra = False
            posizione = "centro"

        dim_tit = dati.get("dimensione", 92) * U
        b_tit = blocco_testo(titolo, stile["font_titolo"], dim_tit, col, max_w, ombra=ombra) if titolo else None
        b_sot = blocco_testo(sotto.upper(), stile["font_testo"], 34 * U, col, max_w,
                             spaziatura=4 * U, interlinea=1.45, ombra=ombra) if sotto else None
        linea = None
        if self.tipo in ("testo", "pannello") and titolo and sotto:
            linea = Image.new("RGBA", (int(70 * U), max(2, int(3 * U))), colore(stile["accento"]))

        parti = [p for p in (b_tit, linea, b_sot) if p is not None]
        gap = int(26 * U)
        tot_h = sum(p.height for p in parti) + gap * (len(parti) - 1)
        if self.tipo == "pannello":
            top_pann = int(H * dati.get("altezza_foto", 0.62))
            spazio = H - basso_sicuro - top_pann
            y = top_pann + max((spazio - tot_h) // 2, int(20 * U))
        elif posizione == "alto":
            y = alto_sicuro + int(60 * U)
        elif posizione == "centro":
            y = (H - tot_h) // 2
        else:
            y = H - basso_sicuro - tot_h
        ritardo = 0.25 if video else 0
        for p in parti:
            self.elementi.append(Elemento(p, (W - p.width) / 2, y, ritardo if video else 0, 0.65 if video else 0))
            y += p.height + gap
            ritardo += 0.22

        if badge:
            b = etichetta(badge, stile, 30 * U)
            by = alto_sicuro + (int(70 * U) if marchio else 0)
            self.elementi.append(Elemento(b, margine, by, 0.1 if video else 0, 0.5 if video else 0, salita=-20))
        if marchio:
            su_foto = self.tipo in ("foto", "pannello")
            col_m = colore(stile["chiaro"]) if su_foto else colore(stile["testo"])
            m = blocco_testo(marchio.upper(), stile["font_forte"], 28 * U, col_m, max_w,
                             spaziatura=8 * U, ombra=su_foto)
            if su_foto:
                hv = int(H * 0.22)
                self.velo_alto = sfumatura(W, hv, alto=True, forza=0.45)
            self.elementi.append(Elemento(m, (W - m.width) / 2, alto_sicuro - int(20 * U), 0, 0))

    def frame(self, t):
        p = ease_in_out(t / self.durata) if self.durata else 0
        if self.tipo == "foto":
            fr = self.foto.frame(p)
            if self.sfondo:
                fr.alpha_composite(self.sfondo)
        else:
            fr = self.sfondo.copy()
            if self.foto:
                fr.paste(self.foto.frame(p), (0, 0))
        if self.velo_alto is not None:
            fr.alpha_composite(self.velo_alto)
        for e in self.elementi:
            e.applica(fr, t)
        return fr


# ---------------------------------------------------------------- video

def genera_video(scheda_path, uscita=None):
    scheda_path = Path(scheda_path)
    dati = json.loads(scheda_path.read_text(encoding="utf-8"))
    base = scheda_path.parent
    W, H = FORMATI[dati.get("formato", "reel")]
    stile = {**STILE_BASE, **dati.get("stile", {})}
    marchio = dati.get("marchio", "")
    scene = []
    for s in dati["scene"]:
        if marchio and "marchio" not in s and s.get("tipo", "foto") != "testo":
            s = {**s, "marchio": marchio}
        scene.append(Scena(s, W, H, stile, base))

    inizi, t = [], 0.0
    for s in scene:
        inizi.append(t)
        t += s.durata - TRANSIZIONE
    totale = t + TRANSIZIONE
    n_frame = int(round(totale * FPS))

    uscita = Path(uscita) if uscita else scheda_path.with_suffix(".mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    audio = []
    for chiave in ("musica", "voce"):
        if dati.get(chiave):
            cmd += ["-i", str(trova_file(dati[chiave], base))]
            audio.append(chiave)
    if audio:
        filtri, etichette = [], []
        for i, chiave in enumerate(audio, start=1):
            vol = dati.get("volume_musica", 0.35 if "voce" in audio else 0.9) if chiave == "musica" else 1.0
            filtri.append(f"[{i}:a]volume={vol},afade=t=out:st={max(totale - 1.5, 0):.2f}:d=1.5[a{i}]")
            etichette.append(f"[a{i}]")
        filtri.append("".join(etichette) + f"amix=inputs={len(etichette)}:duration=longest:normalize=0,"
                      f"atrim=0:{totale:.2f}[aout]")
        cmd += ["-filter_complex", ";".join(filtri), "-map", "0:v", "-map", "[aout]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{totale:.2f}", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-t", f"{totale:.2f}", "-movflags", "+faststart", str(uscita)]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    copertina = None
    for i in range(n_frame):
        t = i / FPS
        attive = [k for k, s0 in enumerate(inizi) if s0 <= t < s0 + scene[k].durata]
        k = attive[0]
        fr = scene[k].frame(t - inizi[k])
        if len(attive) > 1:
            k2 = attive[1]
            fr2 = scene[k2].frame(t - inizi[k2])
            fr = Image.blend(fr, fr2, ease_in_out((t - inizi[k2]) / TRANSIZIONE))
        if copertina is None and t >= min(1.3, scene[0].durata - TRANSIZIONE):
            copertina = fr.convert("RGB")
        proc.stdin.write(fr.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg ha dato errore")
    if copertina is not None:
        copertina.save(uscita.with_name(uscita.stem + "-copertina.jpg"), quality=92)
    print(f"Video creato: {uscita} ({totale:.1f} s, {W}x{H})")
    return uscita


# ---------------------------------------------------------------- grafica

def genera_grafica(scheda_path, uscita=None):
    scheda_path = Path(scheda_path)
    dati = json.loads(scheda_path.read_text(encoding="utf-8"))
    W, H = FORMATI[dati.get("formato", "post")]
    stile = {**STILE_BASE, **dati.get("stile", {})}
    scena = Scena({**dati, "durata": 1}, W, H, stile, scheda_path.parent, video=False)
    img = scena.frame(0).convert("RGB")
    uscita = Path(uscita) if uscita else scheda_path.with_suffix(".png")
    img.save(uscita)
    print(f"Grafica creata: {uscita} ({W}x{H})")
    return uscita


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cosa", choices=["video", "grafica"])
    ap.add_argument("scheda")
    ap.add_argument("-o", "--uscita")
    a = ap.parse_args()
    (genera_video if a.cosa == "video" else genera_grafica)(a.scheda, a.uscita)
