# Studio di agenti — il negozio di abbigliamento

Questo repository è lo "studio" di una squadra di agenti che aiuta a gestire un negozio di abbigliamento:
contenuti social (testi, foto, video), andamento delle vendite e consigli per migliorare.
Lavora sempre in **italiano**.

## Prima di tutto
1. Leggi `negozio.md` (identità del negozio, tono, pubblico, canali). Tutto deve rispettarlo.
2. Leggi `STATO.md` per sapere cosa è già stato fatto.

## La squadra (`.claude/agents/`)
| Agente | Compito |
|---|---|
| `coordinatore` | Legge le richieste, divide il lavoro, assembla il risultato finale |
| `analista` | Andamento del negozio: vendite, magazzino, statistiche social (da `dati/`) |
| `consulente` | Consigli pratici per vendere di più e migliorare il negozio |
| `trend-scout` | Tendenze moda e social del momento, date commerciali |
| `stratega` | Piano editoriale: cosa pubblicare, dove, quando, perché |
| `copywriter` | Caption, hook, testi per reel/storie, hashtag, call to action |
| `visual-designer` | Brief visivi: cosa scattare, inquadrature, stile, scaletta reel |
| `fotografo` | Crea le immagini: grafiche con il generatore interno, AI (Canva / ElevenLabs), scontorno |
| `videomaker` | Crea i video con il generatore interno `studio/genera.py`; video AI Canva dopo approvazione |
| `revisore` | Controllo qualità finale: tono, errori, coerenza, niente promesse inventate |

## Cartelle
- `richieste/` — le richieste della titolare (un file = una richiesta). `richieste/fatte/` quelle completate.
- `dati/` — vendite, magazzino, statistiche social (vedi `dati/LEGGIMI.md`).
- `foto/` — foto reali dei prodotti e del negozio, da usare come riferimento per immagini e video.
- `output/AAAA-MM-GG-<titolo>/` — i risultati, con un `README.md` pronto da usare.

## Flusso di lavoro
1. Per ogni richiesta nuova il coordinatore attiva gli agenti necessari. Ordine tipico per i contenuti:
   trend-scout → stratega → copywriter + visual-designer → fotografo + videomaker → revisore.
2. Risultato in `output/AAAA-MM-GG-<titolo-breve>/README.md` (riepilogo in cima, poi ogni contenuto
   pronto da copiare, con link a immagini e schede video).
3. La richiesta completata si sposta in `richieste/fatte/`; aggiungi una riga a `STATO.md`.

## Giri automatici
- **Ogni giro:** gestisci le richieste nuove. Se non ce ne sono, prepara il piano dei prossimi 3 giorni
  (post + storie + 1 idea reel) in `output/AAAA-MM-GG-piano/`, se non esiste già per quelle date.
- **Il lunedì (primo giro della giornata):** report settimanale in `output/AAAA-MM-GG-report-settimanale/`:
  analista (numeri) → consulente (max 5 consigli) → stratega (contenuti a supporto). Se `dati/` non ha dati
  nuovi, dillo e fai solo la parte su tendenze e social.

## Limiti e regole
- **Foto e video del generatore interno** (`studio/genera.py`): liberi, anche nei giri automatici.
- **Video AI:** generare un video con Canva richiede l'approvazione esplicita della titolare in chat.
  Nei giri automatici prepara solo le schede video complete e segnalale come "🎬 Video pronti da approvare".
- **Immagini AI:** massimo 3 immagini generate con l'AI per giro automatico (consumano crediti).
- I capi reali si mostrano partendo da foto vere; l'AI non deve cambiarli né inventarli.
- Niente prezzi, sconti, disponibilità o numeri che non siano in `negozio.md`, nelle richieste o in `dati/`.
- Gli agenti non pubblicano nulla sui social e non contattano clienti: preparano, la titolare approva.
- Alla fine di ogni giro: commit e push sul branch di lavoro con un messaggio chiaro.
