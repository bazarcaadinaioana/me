# Generatore di foto e video

Crea reel, storie e post a partire dalle **foto vere** del negozio, con testi animati,
movimento sulle foto, dissolvenze, nome del negozio, etichette ("Novità", "-20%") e musica.
Gratis e senza limiti: usa solo Python (Pillow) e ffmpeg.

```bash
python3 studio/genera.py video   scheda.json   # → scheda.mp4 + scheda-copertina.jpg
python3 studio/genera.py grafica scheda.json   # → scheda.png
```

## Scheda video (JSON)
| Campo | Valori |
|---|---|
| `formato` | `reel` / `storia` (9:16), `post` (4:5), `quadrato` (1:1) |
| `marchio` | nome del negozio, in alto su ogni scena con foto |
| `musica`, `voce` | file audio facoltativi (mp3/wav); la musica sfuma alla fine |
| `stile` | colori e font: `sfondo`, `testo`, `accento`, `chiaro`, `font_titolo`, `font_testo` |
| `scene` | elenco di scene (sotto) |

Ogni scena:
| Campo | Valori |
|---|---|
| `tipo` | `foto` (foto a tutto schermo), `pannello` (foto sopra + riquadro colorato col testo), `testo` (solo testo) |
| `foto` | percorso della foto (es. `foto/cappotto.jpg`) |
| `effetto` | `zoom-in`, `zoom-out`, `pan-destra`, `pan-sinistra`, `pan-alto`, `pan-basso` |
| `fuoco` | `alto` / `centro` / `basso`: dove tenere l'inquadratura (es. `alto` se c'è un viso) |
| `testo`, `sottotesto` | titolo e riga piccola in maiuscolo |
| `etichetta` | bollino colorato, es. `Novità`, `-20%`, `Ultimi pezzi` |
| `posizione` | `basso` (default), `alto`, `centro` |
| `durata` | secondi (consigliati 2,5–3,5) |

La scheda grafica usa gli stessi campi di una scena più `formato` e `marchio`.
Esempi pronti in `studio/esempi/`.

## Regole
- Testi e bollini restano fuori dalle zone coperte dall'interfaccia di Instagram/TikTok.
- Reel ideale: 3–6 scene, 8–20 secondi, gancio nella prima scena.
- Musica: usa solo brani senza diritti oppure esporta senza musica e aggiungi l'audio di tendenza
  direttamente dall'app di Instagram/TikTok (spesso funziona meglio).
- Font: Playfair Display e Montserrat (licenza SIL Open Font), in `studio/font/`.
