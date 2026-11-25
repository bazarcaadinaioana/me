#!/usr/bin/env python3
"""Generatore di video e grafiche per i social di Pakima.

Uso:
    python3 studio/genera.py video   scheda-video.json   [-o uscita.mp4]
    python3 studio/genera.py grafica scheda-grafica.json [-o uscita.png]

Le schede sono file JSON (vedi studio/esempi/ e studio/LEGGIMI.md).
Serve solo Python con Pillow e ffmpeg: niente crediti, niente limiti.
Lo stile del marchio (colori, font, logo) è in studio/brand/stile.json.
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
BRAND = QUI / "brand"

FORMATI = {
    "storia": (1080, 1920),   # reel, storie, TikTok
    "reel": (1080, 1920),
    "tiktok": (1080, 1920),
    "post": (1080, 1350),     # post Instagram 4:5
    "quadrato": (1080, 1080),
}

STILE_BASE = {
    "sfondo": "#FFFFFF",        # fondo chiaro (pannelli, scene di testo, prodotti)
    "scuro": "#0E0E0E",         # fondo scuro
    "testo": "#111111",         # testo su fondo chiaro
    "chiaro": "#FFFFFF",        # testo su foto e su fondo scuro
    "accento": "#111111",       # bollini, linee
    "font_titolo": "PlayfairDisplay-SemiBold.ttf",
    "font_corsivo": "PlayfairDisplay-Italic.ttf",
    "font_testo": "Montserrat-Regular.ttf",
    "font_forte": "Montserrat-SemiBold.ttf",
    "logo_scuro": "studio/brand/logo-nero.png",     # da usare su fondo chiaro
    "logo_chiaro": "studio/brand/logo-bianco.png",  # da usare su foto e fondo scuro
}
if (BRAND / "stile.json").exists():
    STILE_BASE.update(json.loads((BRAND / "stile.json").read_text(encoding="utf-8")))

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
    return ImageFont.truetype(str(p), max(8, int(dim)))


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
    """Immagine RGBA con il testo a capo; riduce il font se non ci sta."""
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
    h = h_riga * (len(righe) - 1) + asc + desc + 2 * pad
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

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
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(dim * 0.12)))
    disegna(ImageDraw.Draw(img), fill)
    return img


def pillola(testo, nome_font, dim, fondo, colore_testo, spaziatura=0, maiuscolo=False):
    """Bollino arrotondato (es. 'NOVITÀ', '-20%', 'fino al 29 novembre')."""
    t = testo.upper() if maiuscolo else testo
    f = font(nome_font, dim)
    tw = larghezza(t, f, spaziatura)
    asc, desc = f.getmetrics()
    px, py = dim * 0.95, dim * 0.42
    w, h = int(tw + 2 * px), int(asc + desc + 2 * py)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=fondo)
    x = px
    for ch in t:
        d.text((x, py), ch, font=f, fill=colore_testo)
        x += f.getlength(ch) + spaziatura
    return img


def sfumatura(w, h, alto, forza=0.72):
    """Velo scuro graduale per rendere leggibile il testo sopra la foto."""
    g = Image.new("L", (1, 256))
    for y in range(256):
        v = (y / 255) if not alto else (1 - y / 255)
        g.putpixel((0, y), int(255 * forza * ease_in_out(v) ** 1.3))
    velo = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    velo.putalpha(g.resize((w, h)))
    return velo


def logo(stile, chiaro, larghezza_px, ombra=False):
    img = Image.open(trova_file(stile["logo_chiaro" if chiaro else "logo_scuro"], RADICE)).convert("RGBA")
    h = int(img.height * larghezza_px / img.width)
    img = img.resize((int(larghezza_px), h), Image.LANCZOS)
    if ombra:
        pad = int(larghezza_px * 0.08)
        tela = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sh.putalpha(img.getchannel("A").point(lambda v: int(v * 0.6)))
        tela.alpha_composite(sh, (pad, pad))
        tela = tela.filter(ImageFilter.GaussianBlur(larghezza_px * 0.012))
        tela.alpha_composite(img, (pad, pad))
        img = tela
    return img


def stella(d, cx, cy, r, fill):
    """Stellina a quattro punte (✦)."""
    k = r * 0.28
    d.polygon([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
               (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], fill=fill)


# ---------------------------------------------------------------- cornice animata

class Cornice:
    """Bordo nero con scritta che scorre (es. 'BLACK FRIDAY ✦ BLACK FRIDAY ✦')."""

    def __init__(self, testo, W, H, stile, spessore=None):
        self.W, self.H = W, H
        self.s = s = spessore or int(W * 0.085)
        fondo, chiaro = colore(stile["scuro"]), colore(stile["chiaro"])
        f = font(stile["font_forte"], s * 0.42)
        sp = s * 0.05
        tw = larghezza(testo.upper(), f, sp)
        asc, desc = f.getmetrics()
        gap = s * 0.55
        modulo = int(tw + 2 * gap + s * 0.3)
        self.modulo = modulo
        n = math.ceil(max(W, H) / modulo) + 2
        striscia = Image.new("RGBA", (modulo * n, s), fondo)
        d = ImageDraw.Draw(striscia)
        for i in range(n):
            x = i * modulo
            stella(d, x + gap / 2 + s * 0.15, s / 2, s * 0.17, chiaro)
            x += gap + s * 0.3
            for ch in testo.upper():
                d.text((x, (s - asc - desc) / 2 + s * 0.02), ch, font=f, fill=chiaro)
                x += f.getlength(ch) + sp
        self.striscia = striscia
        self.striscia_v = striscia.rotate(-90, expand=True)
        self.angolo = Image.new("RGBA", (s, s), fondo)
        ImageDraw.Draw(self.angolo)
        stella(ImageDraw.Draw(self.angolo), s / 2, s / 2, s * 0.2, chiaro)
        self.filo = max(2, int(W * 0.003))
        self.chiaro = chiaro

    def applica(self, fr, t, velocita=70):
        W, H, s, m = self.W, self.H, self.s, self.modulo
        off = int(t * velocita) % m
        fr.alpha_composite(self.striscia.crop((off, 0, off + W - 2 * s, s)), (s, 0))
        fr.alpha_composite(self.striscia.crop((m - off, 0, m - off + W - 2 * s, s)), (s, H - s))
        fr.alpha_composite(self.striscia_v.crop((0, off, s, off + H - 2 * s)), (0, s))
        fr.alpha_composite(self.striscia_v.crop((0, m - off, s, m - off + H - 2 * s)), (W - s, s))
        for x, y in ((0, 0), (W - s, 0), (0, H - s), (W - s, H - s)):
            fr.alpha_composite(self.angolo, (x, y))
        # filo sottile interno, come nelle grafiche del negozio
        d = ImageDraw.Draw(fr)
        g = int(s * 0.18)
        d.rectangle((s + g, s + g, W - s - g, H - s - g), outline=colore("#111111"), width=self.filo)


# ---------------------------------------------------------------- foto in movimento

class FotoMobile:
    """Effetto 'Ken Burns': zoom e panoramica lenti su una foto."""

    def __init__(self, percorso, w, h, effetto="zoom-in", fuoco="centro", contieni=False, fondo=None):
        img = ImageOps.exif_transpose(Image.open(percorso)).convert("RGB")
        self.w, self.h, self.effetto = w, h, effetto
        margine = 1.16
        if contieni:  # il capo intero dentro il riquadro, con fondo uniforme attorno
            scala = min(w / img.width, h / img.height)
            pic = img.resize((int(img.width * scala), int(img.height * scala)), Image.LANCZOS)
            tela = Image.new("RGB", (int(w * margine), int(h * margine)), fondo[:3] if fondo else (255, 255, 255))
            tela.paste(pic, ((tela.width - pic.width) // 2, (tela.height - pic.height) // 2))
            self.img = tela
        else:
            scala = max(w * margine / img.width, h * margine / img.height)
            self.img = img.resize((math.ceil(img.width * scala), math.ceil(img.height * scala)), Image.LANCZOS)
        self.fy = fuoco if isinstance(fuoco, (int, float)) else {"alto": 0.3, "basso": 0.7}.get(fuoco, 0.5)

    def frame(self, p):
        bw, bh = self.img.size
        e = self.effetto
        z, cx, cy = 1.0, 0.5, self.fy
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
        if cw / ch > self.w / self.h:
            cw = ch * self.w / self.h
        else:
            ch = cw * self.h / self.w
        x0 = min(max(cx * bw - cw / 2, 0), bw - cw)
        y0 = min(max(cy * bh - ch / 2, 0), bh - ch)
        return self.img.transform((self.w, self.h), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch),
                                  Image.BILINEAR).convert("RGBA")


class ClipVideo:
    """Una clip video (es. una signora animata) usata come sfondo di una scena; letta in streaming."""

    def __init__(self, percorso, w, h, inizio=0.0, velocita=1.0):
        self.w, self.h, self.vel = w, h, velocita
        self.cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(inizio), "-i", str(percorso), "-vf",
                    f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={FPS}",
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        self.proc, self.n, self.ultimo = None, -1, None

    def frame(self, t):
        if self.proc is None:
            self.proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE)
        voluto = int(t * self.vel * FPS)
        while self.n < voluto:
            raw = self.proc.stdout.read(self.w * self.h * 3)
            if len(raw) < self.w * self.h * 3:
                break  # clip finita: resta sull'ultimo fotogramma
            self.ultimo = Image.frombytes("RGB", (self.w, self.h), raw)
            self.n += 1
        return self.ultimo.convert("RGBA")


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
            img = img.copy()
            img.putalpha(self.img.getchannel("A").point(lambda v: int(v * k)))
        frame.alpha_composite(img, (self.x, self.y + int(self.salita * (1 - k))))


class Scena:
    """Tipi: foto | pannello | prodotto | testo.  Campi: vedi studio/LEGGIMI.md."""

    def __init__(self, dati, W, H, stile, base, video=True, cornice=False):
        self.W, self.H, self.stile = W, H, stile
        self.durata = float(dati.get("durata", 3))
        self.tipo = dati.get("tipo", "foto")
        self.elementi, self.foto, self.sfondo, self.velo_alto = [], None, None, None
        self.pos_foto = (0, 0)
        effetto = dati.get("effetto", "zoom-in") if video else "fermo"
        scuro = dati.get("fondo") == "scuro"
        col_fondo = colore(stile["scuro"] if scuro else stile["sfondo"])
        U = W / 1080

        verticale = H > W * 1.5
        s = int(W * 0.085) if cornice else 0
        alto_sicuro = max(int(H * (0.11 if verticale else 0.07)), s + int(60 * U))
        basso_sicuro = max(int(H * (0.20 if verticale else 0.08)), s + int(60 * U))
        margine = int(W * 0.08) + s
        max_w = W - 2 * margine

        titolo = dati.get("testo", "")
        sopra = dati.get("sopratitolo", "")
        sotto = dati.get("sottotesto", "")
        nota = dati.get("pillola", "")
        badge = dati.get("etichetta", "")
        usa_logo = dati.get("logo", False)
        marchio = dati.get("marchio", "")
        posizione = dati.get("posizione", "basso")

        if self.tipo == "clip":
            self.foto = ClipVideo(trova_file(dati["clip"], base), W, H, dati.get("inizio", 0), dati.get("velocita", 1.0))
            self.tipo_sfondo = "foto"
        if self.tipo in ("foto", "clip"):
            if self.tipo == "foto":
                self.foto = FotoMobile(trova_file(dati["foto"], base), W, H, effetto, dati.get("fuoco", "centro"))
            if titolo or sotto or nota:
                self.sfondo = sfumatura(W, H, alto=(posizione == "alto"))
            su_foto, col = True, colore(stile["chiaro"])
            self.tipo = "foto" if self.tipo == "clip" else self.tipo
        elif self.tipo == "pannello":
            hf = int(H * dati.get("altezza_foto", 0.62)) - s
            self.foto = FotoMobile(trova_file(dati["foto"], base), W - 2 * s, hf, effetto, dati.get("fuoco", "centro"))
            self.pos_foto = (s, s)
            self.sfondo = Image.new("RGBA", (W, H), col_fondo)
            su_foto, col = True, colore(stile["chiaro"] if scuro else stile["testo"])
        elif self.tipo == "prodotto":
            # foto di catalogo (capo su fondo bianco): intera, centrata, con zoom lento
            self.sfondo = Image.new("RGBA", (W, H), col_fondo)
            area_h = int(H * dati.get("altezza_foto", 0.6))
            area_w = int(W - 2 * s)
            top = alto_sicuro + (int(90 * U) if usa_logo or marchio else 0)
            self.foto = FotoMobile(trova_file(dati["foto"], base), area_w, area_h, effetto,
                                   contieni=True, fondo=col_fondo)
            self.pos_foto = (s, top)
            su_foto, col = False, colore(stile["chiaro"] if scuro else stile["testo"])
            posizione = "sotto-foto"
            self._sotto_foto = top + area_h
        else:  # testo
            self.sfondo = Image.new("RGBA", (W, H), col_fondo)
            su_foto, col = False, colore(stile["chiaro"] if scuro else stile["testo"])
            posizione = dati.get("posizione", "centro")

        testo_su_pannello = self.tipo in ("pannello",)
        col_testo = col if not testo_su_pannello else colore(stile["chiaro"] if scuro else stile["testo"])
        ombra = self.tipo == "foto"

        dim_tit = dati.get("dimensione", 92) * U
        parti = []
        if sopra:
            parti.append(blocco_testo(sopra, stile["font_corsivo"], dati.get("dimensione_sopratitolo", min(dim_tit * 0.5, 50)) * (U if "dimensione_sopratitolo" in dati else 1), col_testo, max_w, ombra=ombra))
        if titolo:
            parti.append(blocco_testo(titolo, stile["font_titolo"], dim_tit, col_testo, max_w, ombra=ombra,
                                      interlinea=dati.get("interlinea", 1.12)))
        if self.tipo in ("testo", "pannello", "prodotto") and titolo and sotto:
            parti.append(Image.new("RGBA", (int(70 * U), max(2, int(3 * U))), col_testo))
        if sotto:
            parti.append(blocco_testo(sotto.upper(), stile["font_forte" if dati.get("sottotesto_forte") else "font_testo"],
                                      dati.get("dimensione_sottotesto", 34) * U, col_testo, max_w,
                                      spaziatura=4 * U, interlinea=1.45, ombra=ombra))
        if nota:
            chiara = su_foto and not testo_su_pannello or scuro
            parti.append(pillola(nota, stile["font_corsivo"], 40 * U,
                                 colore(stile["chiaro"] if chiara else stile["scuro"]),
                                 colore(stile["testo"] if chiara else stile["chiaro"])))

        gap = int(26 * U)
        tot_h = sum(p.height for p in parti) + gap * (len(parti) - 1)
        if self.tipo == "pannello":
            top_pann = int(H * dati.get("altezza_foto", 0.62))
            spazio = H - basso_sicuro - top_pann
            y = top_pann + max((spazio - tot_h) // 2, int(20 * U))
        elif posizione == "sotto-foto":
            spazio = H - basso_sicuro - self._sotto_foto
            y = self._sotto_foto + max((spazio - tot_h) // 2, int(10 * U))
        elif posizione == "alto":
            y = alto_sicuro + int(110 * U)
        elif posizione == "centro":
            y = (H - tot_h) // 2
        else:
            y = H - basso_sicuro - tot_h
        ritardo = 0.25 if video else 0
        for p in parti:
            self.elementi.append(Elemento(p, (W - p.width) / 2, y, ritardo, 0.65 if video else 0))
            y += p.height + gap
            ritardo += 0.2

        logo_chiaro = su_foto or scuro
        if usa_logo or marchio:
            if usa_logo:
                lw = dati.get("larghezza_logo", 0.30) * W
                m = logo(stile, logo_chiaro, lw, ombra=(self.tipo == "foto" or self.tipo == "pannello"))
            else:
                m = blocco_testo(marchio.upper(), stile["font_forte"], 28 * U,
                                 colore(stile["chiaro"] if logo_chiaro else stile["testo"]), max_w,
                                 spaziatura=8 * U, ombra=su_foto)
            self.elementi.append(Elemento(m, (W - m.width) / 2, alto_sicuro - int(30 * U), 0, 0))
            if su_foto:
                self.velo_alto = sfumatura(W, int(H * 0.24), alto=True, forza=0.45)
        if badge:
            chiaro_b = not (su_foto or scuro)
            b = pillola(badge, stile["font_forte"], 36 * U,
                        colore(stile["scuro"] if chiaro_b else stile["chiaro"]),
                        colore(stile["chiaro"] if chiaro_b else stile["testo"]), spaziatura=3 * U, maiuscolo=True)
            by = alto_sicuro + (int(130 * U) if (usa_logo or marchio) else 0)
            self.elementi.append(Elemento(b, margine, by, 0.1 if video else 0, 0.5 if video else 0, salita=-20))

    def frame(self, t):
        p = ease_in_out(t / self.durata) if self.durata else 0
        if self.tipo == "foto":
            fr = self.foto.frame(t if isinstance(self.foto, ClipVideo) else p)
            if self.sfondo:
                fr.alpha_composite(self.sfondo)
        else:
            fr = self.sfondo.copy()
            if self.foto:
                fr.paste(self.foto.frame(p), self.pos_foto)
        if self.velo_alto is not None:
            fr.alpha_composite(self.velo_alto)
        for e in self.elementi:
            e.applica(fr, t)
        return fr


def prepara(dati, base, video):
    W, H = FORMATI[dati.get("formato", "reel" if video else "post")]
    stile = {**STILE_BASE, **dati.get("stile", {})}
    cornice = Cornice(dati["cornice"], W, H, stile) if dati.get("cornice") else None
    comuni = {k: dati[k] for k in ("logo", "marchio") if k in dati}
    return W, H, stile, cornice, comuni


# ---------------------------------------------------------------- video

def genera_video(scheda_path, uscita=None):
    scheda_path = Path(scheda_path)
    dati = json.loads(scheda_path.read_text(encoding="utf-8"))
    base = scheda_path.parent
    W, H, stile, cornice, comuni = prepara(dati, base, True)
    scene = [Scena({**comuni, **s}, W, H, stile, base, cornice=bool(cornice)) for s in dati["scene"]]

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
            vol = dati.get("volume_musica", 0.3 if "voce" in audio else 0.9) if chiave == "musica" else 1.0
            ritardo = int(float(dati.get("ritardo_voce", 0.3)) * 1000) if chiave == "voce" else 0
            filtri.append(f"[{i}:a]adelay={ritardo}|{ritardo},volume={vol},"
                          f"afade=t=out:st={max(totale - 1.2, 0):.2f}:d=1.2[a{i}]")
            etichette.append(f"[a{i}]")
        filtri.append("".join(etichette) + f"amix=inputs={len(etichette)}:duration=longest:normalize=0,"
                      f"apad,atrim=0:{totale:.2f}[aout]")
        cmd += ["-filter_complex", ";".join(filtri), "-map", "0:v", "-map", "[aout]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{totale:.2f}", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-t", f"{totale:.2f}", "-movflags", "+faststart", str(uscita)]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    copertina = None
    t_cop = min(1.4, scene[0].durata - TRANSIZIONE)
    for i in range(n_frame):
        t = i / FPS
        attive = [k for k, s0 in enumerate(inizi) if s0 <= t < s0 + scene[k].durata] or [len(scene) - 1]
        k = attive[0]
        fr = scene[k].frame(t - inizi[k])
        if len(attive) > 1:
            k2 = attive[1]
            fr = Image.blend(fr, scene[k2].frame(t - inizi[k2]), ease_in_out((t - inizi[k2]) / TRANSIZIONE))
        if cornice:
            cornice.applica(fr, t)
        if copertina is None and t >= t_cop:
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
    W, H, stile, cornice, comuni = prepara(dati, scheda_path.parent, False)
    scena = Scena({**dati, "durata": 1}, W, H, stile, scheda_path.parent, video=False, cornice=bool(cornice))
    img = scena.frame(0)
    if cornice:
        cornice.applica(img, 0)
    uscita = Path(uscita) if uscita else scheda_path.with_suffix(".png")
    img.convert("RGB").save(uscita)
    print(f"Grafica creata: {uscita} ({W}x{H})")
    return uscita


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cosa", choices=["video", "grafica"])
    ap.add_argument("scheda")
    ap.add_argument("-o", "--uscita")
    a = ap.parse_args()
    (genera_video if a.cosa == "video" else genera_grafica)(a.scheda, a.uscita)
