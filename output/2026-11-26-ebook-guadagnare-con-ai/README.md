# Ebook "Guadagnare con l'Intelligenza Artificiale" / "Make Money with Artificial Intelligence"

Due edizioni complete (italiana e inglese) di una guida premium per principianti, con copertine, immagini promozionali, descrizioni commerciali e parole chiave SEO. Informazioni su piattaforme, prezzi e regole verificate a **novembre 2026**.

## Consegna (`consegna/`)

| # | Richiesto | File |
|---|---|---|
| 1 | Ebook italiano in PDF | `consegna/Guadagnare-con-AI-IT.pdf` |
| 2 | Ebook inglese in PDF | `consegna/Make-Money-with-AI-EN.pdf` |
| 3 | Versioni EPUB | `consegna/Guadagnare-con-AI-IT.epub`, `consegna/Make-Money-with-AI-EN.epub` |
| 4 | Copertina italiana | `copertine/copertina-it.png` (2:3) · `copertine/copertina-it-kindle-1600x2560.png` (formato consigliato da KDP) |
| 5 | Copertina inglese | `copertine/copertina-en.png` · `copertine/copertina-en-kindle-1600x2560.png` |
| 6 | Immagini promozionali Etsy e Amazon | `promo/` — per lingua: 3 immagini Etsy 2000×1500 (hero, piano 30 giorni, prompt), Amazon A+ 970×600, post social 1080×1080 |
| 7 | Descrizione commerciale italiana | `consegna/descrizioni-e-seo-IT.md` |
| 8 | Descrizione commerciale inglese | `consegna/descriptions-and-seo-EN.md` |
| 9 | Parole chiave SEO | Negli stessi due file (7 campi KDP, categorie, 13 tag Etsy, parole chiave generali) |

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

1. **Nome dell'autore.** Non ho inserito un autore. Aggiungi il tuo nome o pseudonimo in `build/build.py` (campo `author`) e, se vuoi, in copertina (`build/grafiche.py`), poi ricostruisci.
2. **Etsy: attenzione alla regola del 22 ottobre 2026.** Etsy ora vieta le "guide funzionali" (istruzioni, ricette, schemi) generate con l'AI, anche se dichiarate. Questo libro è una guida pratica realizzata con l'AI: **pubblicarlo su Etsy così com'è rischia la rimozione dell'inserzione**. Consiglio: vendilo su Payhip, Gumroad o sul tuo sito; su Etsy solo dopo una tua revisione e riscrittura sostanziale, e dopo aver riletto le regole ufficiali.
3. **Amazon KDP: dichiarazione AI obbligatoria.** Il testo è stato generato con l'AI (italiano scritto da Claude, inglese adattato con GPT-5.5 e poi controllato): in fase di pubblicazione va selezionato "contenuto generato dall'AI".
4. **Revisione umana.** Il libro dichiara nel colophon una supervisione editoriale umana: falla davvero (lettura completa di almeno un'edizione, controllo dei prezzi alla data di uscita).
5. **Prezzi degli strumenti.** Alcuni derivano da fonti di terze parti (segnalato nel libro). Ricontrolla le pagine ufficiali prima dell'uscita.

## Ricostruire i file

```bash
python3 build/diagrammi.py immagini      # diagrammi SVG
python3 build/grafiche.py                # copertine e promo
python3 build/build.py it                # PDF + EPUB italiano
python3 build/build.py en                # PDF + EPUB inglese
```

Sorgenti modificabili in `sorgenti/it/` e `sorgenti/en/` (Markdown). Dipendenze: pandoc, weasyprint, beautifulsoup4, playwright (Chromium già presente).

## Chi ha fatto cosa

Questa richiesta non riguarda il negozio, quindi non ho coinvolto la squadra di agenti: scrittura, ricerca, impaginazione e grafica sono state fatte direttamente in questa sessione. L'edizione inglese è un adattamento editoriale prodotto con l'API OpenAI (GPT-5.5) a partire dal testo italiano, con istruzioni di conservare tutti i fatti, e poi controllato (struttura, numeri, link).
