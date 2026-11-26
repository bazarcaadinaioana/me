# Ebook "Guadagnare con l'Intelligenza Artificiale" / "Make Money with Artificial Intelligence"

Due edizioni complete (italiana e inglese) di una guida premium per principianti, con copertine, immagini promozionali, descrizioni commerciali e parole chiave SEO. Informazioni su piattaforme, prezzi e regole verificate a **novembre 2026**.

## Consegna (`consegna/`)

Autrice: **Irina B.**

| # | Richiesto | File |
|---|---|---|
| 1 | Ebook italiano in PDF (236 pagine) | `consegna/Guadagnare-con-AI-IT.pdf` |
| 2 | Ebook inglese in PDF (231 pagine) | `consegna/Make-Money-with-AI-EN.pdf` |
| 3 | Versioni EPUB | `consegna/Guadagnare-con-AI-IT.epub`, `consegna/Make-Money-with-AI-EN.epub` |
| 4 | Copertina italiana | `copertine/copertina-it.png` (2:3) · `copertine/copertina-it-kindle-1600x2560.png` (formato consigliato da KDP) |
| 5 | Copertina inglese | `copertine/copertina-en.png` · `copertine/copertina-en-kindle-1600x2560.png` |
| 6 | Immagini promozionali Etsy e Amazon | `promo/`: per lingua 3 immagini Etsy 2000×1500 (presentazione, piano 30 giorni, prompt), Amazon A+ 970×600, post social 1080×1080 · `consegna/anteprima/`: pagine interne 2000×1500 ed estratto PDF di 16 pagine (Etsy chiede un'anteprima per i download digitali) |
| 7 | Descrizione commerciale italiana | `consegna/descrizioni-e-seo-IT.md` |
| 8 | Descrizione commerciale inglese | `consegna/descriptions-and-seo-EN.md` |
| 9 | Parole chiave SEO | Negli stessi due file: titolo SEO e 13 tag per Etsy, 7 campi parole chiave e categorie per KDP, parole chiave generali |
| + | Guida alla pubblicazione con AI | `consegna/pubblicazione-etsy-e-amazon.md`: cosa dichiarare su Etsy e KDP, checklist di revisione di Irina, testi di trasparenza |

### Titoli (ottimizzati per la ricerca, conformi alle regole KDP)

- **IT:** *Guadagnare con l'Intelligenza Artificiale*. *La guida pratica per principianti: guadagnare online con l'AI, creare prodotti digitali e avviare un business digitale anche partendo da zero*
- **EN:** *Make Money with Artificial Intelligence*. *A Practical Beginner's Guide to Making Money Online with AI, Creating Digital Products and Starting a Digital Business from Scratch*

Su KDP titolo e sottotitolo devono coincidere con la copertina e non possono essere un elenco di parole chiave: le parole chiave sono inserite in modo naturale nel sottotitolo e nei 7 campi dedicati. Su Etsy il titolo dell'inserzione è più ricco di parole chiave (vedi file SEO).

## Contenuto dei libri

Struttura identica nelle due lingue: introduzione, 8 parti, 40 capitoli, conclusione, glossario, fonti ufficiali.

- **Parte 1** (cap. 1–6): cos'è l'AI, come funziona, strumenti principali, prompt (metodo RCOFE), uso senza competenze tecniche, opportunità e rischi.
- **Parte 2** (cap. 7–18): i 12 modi per guadagnare, ciascuno con tutti i 15 punti richiesti (strumenti gratuiti/a pagamento, tempi, competenze, investimento, procedura, primi clienti, prezzi, prima vendita, errori, esempio completo, esercizio, piano di 7 giorni).
- **Parte 3** (cap. 19): guida agli strumenti per 10 categorie, con prezzi verificati e alternative gratuite.
- **Parte 4** (cap. 20–31): i 12 passi per costruire un business digitale, con un caso conduttore.
- **Parte 5** (cap. 32–36): 5 tutorial completi dall'idea al lancio.
- **Parte 6** (cap. 37): 55 prompt professionali in 10 categorie, ognuno con "quando usarlo".
- **Parte 7** (cap. 38): piano operativo di 30 giorni (obiettivo, attività, strumenti, tempo, risultato).
- **Parte 8** (cap. 39–40): truffe, copyright, privacy, AI Act, verifica delle informazioni, fisco, indipendenza dagli strumenti, aggiornamento.

Ogni capitolo termina con: cosa abbiamo imparato, errori da evitare, esercizio pratico, checklist di verifica. Tutte le simulazioni economiche sono dichiarate ipotetiche; i personaggi degli esempi sono immaginari; nessuna statistica, testimonianza o caso di successo è inventato.

Impaginazione: formato 6 × 9 pollici, indice cliccabile con numeri di pagina, testatine, numerazione, 5 diagrammi originali, tabelle, riquadri (consiglio / attenzione / esempio ipotetico). Font con licenza libera OFL (Fraunces, Source Serif 4, Inter).

## ⚠️ Da fare prima di pubblicare

1. **Revisione di Irina (indispensabile per Etsy).** Dal 22 ottobre 2026 Etsy vieta le "guide funzionali" generate con l'AI, anche se dichiarate. Il libro è stato generato con l'AI: per venderlo correttamente su Etsy serve un contributo reale e sostanziale di Irina. Segui la checklist in `consegna/pubblicazione-etsy-e-amazon.md` (riquadri "L'esperienza di Irina", prova dei prompt, riscrittura di introduzione e conclusione) e conserva le prove del lavoro.
2. **Dichiarazioni AI.** Sono già nel colophon e nell'introduzione, pensate per essere valide su Etsy e su KDP. Su KDP rispondi "sì" a testo e immagini generati con l'AI (e a traduzione per l'edizione inglese).
3. **KDP Select.** Se un giorno iscrivi l'ebook a KDP Select, durante l'iscrizione non potrà essere venduto in digitale su Etsy.
4. **Prezzi degli strumenti.** Alcuni derivano da fonti di terze parti (segnalato nel libro). Ricontrolla le pagine ufficiali alla data di uscita.

## Ricostruire i file

```bash
python3 build/diagrammi.py immagini      # diagrammi SVG
python3 build/grafiche.py                # copertine e promo
python3 build/build.py it                # PDF + EPUB italiano
python3 build/build.py en                # PDF + EPUB inglese
```

Sorgenti modificabili in `sorgenti/it/` e `sorgenti/en/` (Markdown). Dipendenze: pandoc, weasyprint, beautifulsoup4, playwright (Chromium già presente).

## Chi ha fatto cosa

Questa richiesta non riguarda il negozio, quindi non ho coinvolto la squadra di agenti: ricerca, scrittura delle due edizioni, impaginazione e grafica sono state fatte in questa sessione con Claude. Un primo tentativo di far adattare l'inglese a GPT-5.5 tramite API non è partito per credito esaurito: l'edizione inglese è stata quindi scritta direttamente e verificata, con un controllo automatico sulla struttura (titoli, tabelle, prompt, riquadri, esercizi e checklist identici all'italiano).
