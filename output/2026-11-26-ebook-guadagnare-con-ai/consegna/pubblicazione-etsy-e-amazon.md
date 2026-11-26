# Pubblicare su Etsy (e un domani su Amazon KDP): uso dell'AI

Autrice: **Irina B.** · Regole verificate a novembre 2026. Prima di pubblicare rileggi sempre le pagine ufficiali (indirizzi in fondo).

## 1. Come è stato realizzato il libro (versione veritiera da tenere a mente)

| Elemento | Come è stato creato | Etsy | Amazon KDP |
|---|---|---|---|
| Testo italiano | Generato con un assistente AI (Claude) su un progetto editoriale, con verifica delle fonti | Da dichiarare | "Generato dall'AI": **sì** |
| Testo inglese | Adattamento dal testo italiano con un assistente AI (GPT-5.5), poi controllato | Da dichiarare | Traduzione generata dall'AI: **sì** |
| Copertina, diagrammi, immagini promo | Grafica tipografica generata da codice scritto da un assistente AI (nessuna foto o illustrazione da generatore di immagini) | Da dichiarare | Immagini generate dall'AI: **sì** (scelta prudente) |

La definizione di KDP è ampia: è "generato dall'AI" anche ciò che è stato poi modificato in modo sostanziale. Per questo, anche dopo la revisione di Irina, **su KDP la risposta resta "sì"**.

## 2. Etsy: il punto critico

Dal **22 ottobre 2026** Etsy vieta le **"guide funzionali" generate con l'AI** (istruzioni, ricette, schemi), e la dichiarazione non basta a renderle ammesse. Gli ebook restano ammessi quando il venditore ha un **ruolo creativo chiaro** e dichiara l'uso dell'AI.

Questo libro è una guida pratica: per venderlo su Etsy in modo corretto, **il contributo di Irina deve essere reale e sostanziale**. Non è una formalità da aggirare: se l'inserzione venisse segnalata (Etsy ha introdotto anche la segnalazione da parte degli acquirenti), servirebbe poter dimostrare quel contributo.

### Checklist di revisione di Irina (da completare prima di pubblicare su Etsy)

- [ ] Leggere tutto il libro, almeno nell'edizione che si vende per prima.
- [ ] Riscrivere con la propria voce l'introduzione e la conclusione.
- [ ] Aggiungere in almeno 10 capitoli un riquadro "**L'esperienza di Irina**" con osservazioni, prove o casi personali **veri** (anche piccoli: uno strumento provato, un errore fatto, un risultato misurato).
- [ ] Provare personalmente almeno 15 prompt della Parte 6 e correggere quelli che non rendono.
- [ ] Svolgere almeno una settimana del piano di 30 giorni e annotare cosa cambiare.
- [ ] Ricontrollare i prezzi degli strumenti sulle pagine ufficiali alla data di uscita.
- [ ] Tagliare o modificare ciò che non condivide.
- [ ] Conservare le prove del lavoro: file con le modifiche, note, date, versioni. Il repository git registra già le versioni dei sorgenti.

Le modifiche si fanno nei file `sorgenti/it/*.md` (testo semplice). Poi si ricostruisce il PDF con `python3 build/build.py it`.

### Moduli dell'inserzione Etsy

- **Chi l'ha realizzato:** Irina (io). Nella classificazione di Etsy è un prodotto **progettato dalla venditrice** (*Designed by*).
- **Che cos'è:** prodotto digitale (download istantaneo).
- **Uso dell'AI:** se il modulo lo chiede, indicare che sono stati usati strumenti di AI generativa.
- **Anteprima:** Etsy chiede che i download digitali includano un'anteprima o un estratto → usa `consegna/anteprima/` (pagine interne ed estratto PDF).

### Testo da inserire nella descrizione Etsy (IT)

> **Come è stato realizzato questo ebook.** Il testo, i diagrammi e la copertina sono stati creati con l'aiuto di strumenti di intelligenza artificiale, a partire da un mio progetto editoriale. Ho definito struttura e contenuti, ho rivisto il libro e verificato su fonti ufficiali prezzi e regole delle piattaforme (aggiornati a novembre 2026). Non contiene promesse di guadagno: gli esempi economici sono ipotetici e dichiarati come tali.

### Text for the Etsy description (EN)

> **How this ebook was made.** The text, diagrams and cover were created with the help of artificial intelligence tools, based on my own editorial project. I defined the structure and content, reviewed the book and checked platform prices and rules against official sources (updated November 2026). It contains no income promises: financial examples are hypothetical and clearly labeled.

Usa questi testi **dopo** aver completato la checklist: descrivono il lavoro di Irina e devono essere veri.

## 3. Amazon KDP (quando vorrai pubblicare)

Il libro è già impostato per KDP:

- formato interno **6 × 9 pollici** (formato standard KDP), indice cliccabile, EPUB pronto per il caricamento come ebook Kindle;
- copertina Kindle **1600 × 2560 px** (`copertine/copertina-*-kindle-1600x2560.png`);
- dichiarazione AI già presente nel colophon e nell'introduzione;
- descrizione, 7 parole chiave e categorie in `descrizioni-e-seo-*.md`.

**Nel modulo KDP, sezione contenuti AI:**

| Domanda | Risposta |
|---|---|
| Il libro contiene testo generato dall'AI? | **Sì** — indica che il testo è stato generato con l'AI e poi rivisto e modificato dall'autrice |
| Contiene immagini generate dall'AI? | **Sì** (copertina e diagrammi realizzati con strumenti AI) |
| Contiene traduzioni generate dall'AI? | Edizione inglese: **sì** · Edizione italiana: no |

Altre note per KDP:

- **Esclusiva:** se un giorno iscrivi l'ebook a **KDP Select / Kindle Unlimited**, per la durata dell'iscrizione l'ebook deve essere venduto in digitale **solo** su Amazon: andrebbe tolto da Etsy. Senza KDP Select puoi vendere su entrambe.
- **Prezzo:** l'ebook a 70% richiede un prezzo entro la fascia stabilita da Amazon; usa il calcolatore di royalty.
- **Cartaceo:** per una versione stampata serve un PDF senza la copertina come prima pagina e una copertina completa (fronte, dorso, retro) calcolata con lo strumento di KDP: si può preparare quando serve.
- **Nome autore:** "Irina B." è accettato come pseudonimo; usalo uguale su tutte le edizioni.

## 4. Pagine ufficiali da rileggere prima di pubblicare

- Etsy — Standard di creatività: etsy.com/legal/creativity
- Etsy — Regole della casa e politica sui contenuti AI (Seller Handbook)
- Amazon KDP — Linee guida sui contenuti (sezione contenuti generati dall'AI): kdp.amazon.com/help
- Amazon KDP — Esclusività di KDP Select
