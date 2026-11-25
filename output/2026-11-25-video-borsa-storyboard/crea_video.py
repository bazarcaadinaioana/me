#!/usr/bin/env python3
"""Video 9:16 dallo storyboard della titolare (6 scene, 3 s l'una), effetto girato a mano."""
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

QUI = Path(__file__).resolve().parent
W, H, FPS, DUR = 1080, 1920, 30, 3.0
# movimento per scena: (zoom iniziale, zoom finale, spostamento x, spostamento y) in frazioni
MOVIMENTI = [(1.00, 1.05, 0.00, 0.00),   # 1 push-in sulla borsa
             (1.04, 1.00, -0.01, 0.00),  # 2 pull-back, la signora prende la borsa
             (1.00, 1.04, 0.01, 0.00),   # 3 la segue mentre si gira
             (1.04, 1.00, 0.01, 0.00),   # 4 scorre sul dettaglio
             (1.00, 1.04, -0.01, 0.00),  # 5 tracking in strada
             (1.00, 1.03, 0.00, 0.00)]   # 6 finale lento


def mano(t, s):
    dx = math.sin(t * 1.3 + s) * 6 + math.sin(t * 3.9 + 2 * s) * 2.5 + math.sin(t * 10.0 + s) * 1.0
    dy = math.cos(t * 1.1 + s) * 5 + math.sin(t * 4.4 + s) * 2.0 + math.cos(t * 8.7 + 3 * s) * 0.8
    rot = math.sin(t * 0.9 + s) * 0.35 + math.sin(t * 5.3 + s) * 0.1
    return dx, dy, rot


def prepara(p):
    im = Image.open(p).convert("RGB")
    grande = im.resize((W + 200, int((W + 200) * im.height / im.width)), Image.LANCZOS)
    grande = grande.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    sf = im.resize((int(H * im.width / im.height) + 40, H + 40), Image.LANCZOS)
    sf = sf.filter(ImageFilter.GaussianBlur(38))
    sf = ImageEnhance.Brightness(sf).enhance(0.55)
    x = (sf.width - W) // 2
    return grande, sf.crop((x, 20, x + W, 20 + H))


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def main():
    scene = [prepara(QUI / "scene" / f"scena{i}.png") for i in range(1, 7)]
    out = QUI / "video-borsa-storyboard.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-vf", "noise=alls=4:allf=t", "-map", "0:v", "-map", "1:a", "-shortest",
           "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i, (grande, sfondo) in enumerate(scene):
        z0, z1, mx, my = MOVIMENTI[i]
        for f in range(n):
            t = i * DUR + f / FPS
            p = ease(f / (n - 1))
            z = z0 + (z1 - z0) * p
            dx, dy, rot = mano(t, i * 1.7)
            # riquadro dentro l'immagine ingrandita (larga W+200)
            cw, ch = grande.width / z * 0.965, grande.height / z * 0.965
            cx = grande.width / 2 + mx * grande.width * (p - 0.5) * 2 + dx
            cy = grande.height / 2 + my * grande.height * (p - 0.5) * 2 + dy
            crop = grande.transform((W, int(W * ch / cw)), Image.EXTENT,
                                    (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
            crop = crop.rotate(rot, resample=Image.BICUBIC, expand=False)
            fr = sfondo.copy()
            fr.paste(crop, (0, (H - crop.height) // 2))
            if f < 3 and i > 0:  # taglio a mano con micro-flash
                fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), [0.22, 0.1, 0.04][f])
            if i == 5 and f > n - 12:  # dissolvenza finale
                fr = Image.blend(fr, Image.new("RGB", (W, H), (0, 0, 0)), (f - (n - 12)) / 12 * 0.0)
            proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    proc.wait()
    print("ok", out)


if __name__ == "__main__":
    main()
