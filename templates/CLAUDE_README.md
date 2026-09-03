# Claude Code

Claude Code deve partire dalla root cliente e leggere `CLAUDE.md` / `AGENTS.md`.

## Gate di ingresso

Avvia Claude Code dal terminale con la cartella madre come directory corrente,
poi crea una nuova sessione. `/context` deve mostrare `CLAUDE.md` e
`AGENTS.md`; `/memory` deve mostrare la memoria canonica dichiarata dalla casa.

Prima di lavorare Claude Code mostra:

- directory corrente;
- conferma che `CLAUDE.md` importa `@AGENTS.md`;
- tre regole lette dalla mappa.

Percorso diverso, ponte assente o mappa non caricata = `FUORI DAL CERVELLO`:
nessuna scrittura, un solo gesto preciso per entrare nella cartella, poi nuova
sessione.

Questo gate funziona anche quando la sessione nasce altrove perche' le
istruzioni utente di Claude Code (`~/.claude/CLAUDE.md`, lette in ogni
sessione) portano il blocco `LEADERAI-CASA` con il percorso della cartella
madre. Senza quel blocco l'agente aperto da un'altra cartella parte cieco.
L'Ispettore lo verifica e lo ripara.

Per il controllo completo il proprietario puo' dire `lancia l'Ispettore` o
usare `/ispettore-ecosistema`. La skill apre la procedura unica `CHECKUP.md`
della repo `salChiarenza/leaderai-cervello-ecosistema`.

La memoria canonica e' dichiarata nell'`AGENTS.md` radice. Su ogni computer,
`~/.claude/settings.json` deve impostare `autoMemoryDirectory` con forma `~/...`
quando la memoria e' sotto la home di quella macchina. Il percorso assoluto si
usa soltanto se il target e' stato letto sulla stessa macchina e vive fuori
dalla home. La chiave non e' accettata nelle settings project/local. Dopo il
trust del workspace, `/memory` deve mostrare la stessa destinazione prima del
verdetto `PASSA`.
