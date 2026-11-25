# Studio di agenti — contenuti social

Una squadra di 6 agenti AI che prepara i contenuti social del negozio:
**coordinatore, trend-scout, stratega, copywriter, visual-designer, revisore**.

## Come si usa
1. **Una volta sola:** compila `negozio.md` (nome, stile, clienti, tono, canali).
2. **Chiedi qualcosa:** crea un file in `richieste/` (vedi l'esempio) oppure scrivilo direttamente in chat.
3. **Gli agenti lavorano:** a ogni giro programmato prendono le richieste nuove e
   mettono il risultato in `output/<data>-<titolo>/README.md`, pronto da copiare.
4. **Tu approvi e pubblichi.** Gli agenti non pubblicano nulla da soli.

Lo storico dei lavori è in `STATO.md`. Le istruzioni per gli agenti sono in `CLAUDE.md`
e in `.claude/agents/`.
