# Studio di agenti — contenuti social per il negozio

Questo repository è lo "studio" di una squadra di agenti che produce contenuti social
per un negozio di abbigliamento. Lavora sempre in **italiano**.

## Prima di tutto
1. Leggi `negozio.md` (identità del negozio, tono, pubblico, canali). Ogni contenuto deve rispettarlo.
2. Leggi `STATO.md` per sapere cosa è già stato fatto.

## La squadra (`.claude/agents/`)
| Agente | Compito |
|---|---|
| `coordinatore` | Legge le richieste, divide il lavoro, assembla il risultato finale |
| `trend-scout` | Cerca tendenze moda e social del momento |
| `stratega` | Piano editoriale: cosa pubblicare, dove, quando, perché |
| `copywriter` | Caption, hook, testi per reel/storie, hashtag, call to action |
| `visual-designer` | Brief visivi: foto da scattare, inquadrature, prompt immagini, grafiche |
| `revisore` | Controllo qualità finale: tono, errori, coerenza con `negozio.md` |

## Flusso di lavoro
1. Le richieste arrivano come file `.md` in `richieste/` (una richiesta = un file).
2. Per ogni richiesta nuova il coordinatore attiva gli agenti necessari, in quest'ordine tipico:
   trend-scout → stratega → copywriter + visual-designer → revisore.
3. Il risultato va in `output/AAAA-MM-GG-<titolo-breve>/` con un file `README.md` che riassume
   tutto (pronto da copiare e incollare) più eventuali file di dettaglio.
4. La richiesta completata si sposta in `richieste/fatte/`.
5. Aggiorna `STATO.md` con una riga per lavoro svolto (data, richiesta, cartella di output).

## Senza richieste nuove
Se `richieste/` è vuota, il coordinatore prepara comunque il **piano dei prossimi 3 giorni**
(post + storie) in `output/AAAA-MM-GG-piano/`, salvo che esista già un piano per quelle date.

## Regole
- Niente promesse su prezzi, sconti o disponibilità che non siano scritte in `negozio.md` o nella richiesta.
- Non pubblicare nulla sui social: gli agenti preparano, la titolare approva e pubblica.
- Alla fine, commit e push sul branch di lavoro con un messaggio chiaro.
