# Codex

Codex deve partire dalla root cliente e leggere `AGENTS.md`.

## Gate di ingresso

In Codex Desktop la cartella madre deve essere il progetto locale primario:
usa `Ctrl+O` / **Add new project**, seleziona la cartella madre, conferma il
trust solo dopo aver verificato provenienza e configurazioni, quindi crea una
nuova task. Come scorciatoia da terminale si puo' usare
`codex app "<CARTELLA_MADRE>"`.

In Codex CLI avvia con `codex -C "<CARTELLA_MADRE>"` oppure entra prima nella
cartella madre. Una email aperta, un allegato o una task precedente non
sostituiscono il progetto.

Prima di lavorare Codex mostra:

- percorso del progetto primario/directory corrente;
- conferma che quel percorso contiene `AGENTS.md`;
- tre regole lette dalla mappa.

Percorso diverso o mappa non caricata = `FUORI DAL CERVELLO`: nessuna
scrittura, un solo gesto preciso per aprire la cartella, poi nuova task.

Questo gate funziona anche quando la task nasce altrove perche' l'`AGENTS.md`
globale di Codex (`~/.codex/AGENTS.md`, oppure `AGENTS.override.md` se
esiste, letto in ogni task) porta il blocco `LEADERAI-CASA` con il percorso
della cartella madre. Senza quel blocco l'agente aperto da un'altra cartella
parte cieco. L'Ispettore lo verifica e lo ripara.

Per il controllo completo il proprietario puo' dire `lancia l'Ispettore` o
richiamare `$ispettore-ecosistema`. La skill apre la procedura unica
`CHECKUP.md` della repo `salChiarenza/leaderai-cervello-ecosistema`.
