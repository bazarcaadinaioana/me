#!/usr/bin/env python3
"""Voce fuori campo gratuita per Pakima (gira su questo computer, senza crediti).

Uso (con l'ambiente della voce):
    .venv-voce/bin/python studio/voce.py testo.txt uscita.mp3 [--prove 3] [--espressivita 0.6]

- Il testo va scritto una frase per riga (ogni riga = una frase detta con una piccola pausa dopo).
- Per ogni frase genera più "prove" e tiene quella che il riconoscimento vocale capisce meglio:
  così si scartano le pronunce sbagliate.
- Se esiste studio/brand/voce-riferimento.wav (10–20 s di una voce italiana registrata con il permesso
  di chi parla, es. la titolare), la voce generata la imita: accento italiano naturale e timbro di Pakima.
- Parole straniere: scrivile come si pronunciano se serve (es. "Blèck Fràidei"), o lasciale in inglese:
  il controllo automatico scarta le prove pronunciate male.

Installazione dell'ambiente (una volta):
    uv venv -p 3.12 .venv-voce && VIRTUAL_ENV=.venv-voce uv pip install chatterbox-tts "setuptools<81" faster-whisper num2words
"""
import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

QUI = Path(__file__).resolve().parent
RIFERIMENTO = QUI / "brand" / "voce-riferimento.wav"


def normalizza(t):
    from num2words import num2words
    t = t.lower().replace("%", " per cento ")
    t = re.sub(r"\d+", lambda m: " " + num2words(int(m.group()), lang="it") + " ", t)
    t = re.sub(r"[^a-zàèéìòóù0-9 ]", " ", t)
    return " ".join(t.split())


def somiglianza(a, b):
    return difflib.SequenceMatcher(None, normalizza(a), normalizza(b)).ratio()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("testo", help="file .txt, una frase per riga (oppure il testo tra virgolette)")
    ap.add_argument("uscita", help="file .mp3 o .wav")
    ap.add_argument("--prove", type=int, default=3, help="versioni per frase (default 3)")
    ap.add_argument("--espressivita", type=float, default=0.6, help="0.3 calma … 0.9 molto espressiva")
    ap.add_argument("--pausa", type=float, default=0.35, help="secondi di pausa tra le frasi")
    ap.add_argument("--riferimento", help="wav di una voce italiana da imitare (default studio/brand/voce-riferimento.wav)")
    a = ap.parse_args()

    p = Path(a.testo)
    testo = p.read_text(encoding="utf-8") if p.exists() else a.testo
    frasi = [r.strip() for r in testo.splitlines() if r.strip()]

    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from faster_whisper import WhisperModel
    torch.manual_seed(7)
    tts = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    rif = a.riferimento or (str(RIFERIMENTO) if RIFERIMENTO.exists() else None)
    if rif:
        print(f"Imito la voce di riferimento: {rif}")

    sr = tts.sr
    pezzi = []
    for f in frasi:
        migliore, voto_m = None, -1
        for k in range(a.prove):
            kw = dict(language_id="it", exaggeration=a.espressivita, cfg_weight=0.4 if a.espressivita > 0.5 else 0.5,
                      temperature=0.8)
            if rif:
                kw["audio_prompt_path"] = rif
            w = tts.generate(f, **kw).squeeze(0).numpy()
            a16 = np.interp(np.arange(0, len(w), sr / 16000), np.arange(len(w)), w).astype(np.float32)
            segs, _ = asr.transcribe(a16, language="it")
            capito = " ".join(s.text.strip() for s in segs)
            voto = somiglianza(f, capito)
            print(f"  prova {k + 1}: {voto:.2f} — {capito}")
            if voto > voto_m:
                migliore, voto_m = w, voto
            if voto >= 0.97:
                break
        print(f"✓ {f}  (scelta con voto {voto_m:.2f})")
        # taglia i silenzi iniziali/finali della frase
        soglia = 0.01 * np.abs(migliore).max()
        idx = np.where(np.abs(migliore) > soglia)[0]
        if len(idx):
            migliore = migliore[max(idx[0] - int(0.03 * sr), 0): idx[-1] + int(0.08 * sr)]
        pezzi += [migliore, np.zeros(int(sr * a.pausa), dtype=np.float32)]

    audio = np.concatenate(pezzi)
    audio = audio / max(np.abs(audio).max(), 1e-6) * 0.89
    tmp = Path(a.uscita).with_suffix(".tmp.wav")
    import soundfile as sf
    sf.write(tmp, audio, sr)
    # rifinitura: leggera compressione, presenza e loudness da social (-14 LUFS)
    filtri = ("highpass=f=70,equalizer=f=200:t=q:w=1:g=1.5,equalizer=f=3500:t=q:w=1.2:g=2,"
              "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-14:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-af", filtri, "-ar", "44100",
                    *(["-b:a", "192k"] if a.uscita.endswith(".mp3") else []), a.uscita], check=True)
    tmp.unlink()
    print(f"Voce creata: {a.uscita} ({len(audio) / sr:.1f} s)")


if __name__ == "__main__":
    sys.exit(main())
