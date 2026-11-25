#!/usr/bin/env python3
"""Anima una foto: la signora cammina, si gira, il capo si muove. Gratis, senza account.

Usa il modello video open source LTX-Video (Lightricks) sulle schede grafiche gratuite di Hugging Face.

Uso (con l'ambiente della voce, che contiene gradio_client):
    .venv-voce/bin/python studio/anima.py foto.jpg "descrizione del movimento in inglese" uscita.mp4 [--secondi 3]

Consigli per il prompt (in inglese, breve e concreto):
- descrivi UN movimento semplice: "she walks slowly towards the camera", "she turns to look at the shop window",
  "she adjusts her coat and smiles", "slow camera push-in"
- aggiungi la camera: "handheld camera follows her", "slow dolly in"
- niente azioni complicate (mani che toccano oggetti, più persone): aumentano gli errori.
Il risultato è 512x768: lo script lo porta a 1080x1920 con un ingrandimento di qualità.
Genera 2–3 versioni e tieni la migliore (mani, volto, capo identico).
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NEGATIVO = ("worst quality, inconsistent motion, blurry, jittery, distorted, deformed hands, extra fingers, "
            "morphing face, changing clothes, text, watermark")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("foto")
    ap.add_argument("prompt")
    ap.add_argument("uscita")
    ap.add_argument("--secondi", type=float, default=3)
    ap.add_argument("--seed", type=int, default=0, help="0 = casuale")
    a = ap.parse_args()

    from gradio_client import Client, handle_file
    from PIL import Image, ImageOps

    # prepara la foto in 2:3 verticale (512x768) centrata
    tmp = Path(tempfile.mkdtemp())
    img = ImageOps.exif_transpose(Image.open(a.foto)).convert("RGB")
    img = ImageOps.fit(img, (1024, 1536), Image.LANCZOS, centering=(0.5, 0.4))
    src = tmp / "in.jpg"
    img.save(src, quality=95)

    c = Client("Lightricks/ltx-video-distilled", verbose=False)
    v, seed = c.predict(a.prompt, NEGATIVO, handle_file(str(src)), None, 768, 512, "image-to-video",
                        a.secondi, 9, a.seed or 42, a.seed == 0, 1, True, api_name="/image_to_video")
    grezzo = v["video"] if isinstance(v, dict) else v
    # ingrandisce a 1080x1920 (9:16) con un leggero ritocco di nitidezza
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", grezzo, "-vf",
                    "scale=1080:1620:flags=lanczos,pad=1080:1920:0:150:black,crop=1080:1620:0:150,"
                    "scale=1080:1920:flags=lanczos:force_original_aspect_ratio=increase,crop=1080:1920,"
                    "unsharp=5:5:0.6", "-r", "30", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-an", a.uscita], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Clip creata: {a.uscita} (seed {seed})")


if __name__ == "__main__":
    sys.exit(main())
