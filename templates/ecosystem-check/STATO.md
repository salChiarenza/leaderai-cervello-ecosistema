# Ecosystem Check - fonte operativa

## Stato corrente

Stanza installata per `{{client_name}}` con lo standard LeaderAI
`{{version}}`. Il controllo iniziale non e' ancora stato eseguito.

## Prossimo passo

Eseguire il controllo iniziale sulla cartella madre, registrare la situazione
di partenza e chiudere o assegnare ogni problema provato.

## Decisioni

- Un solo orchestratore assegna i controlli e unisce i risultati.
- Struttura, istruzioni e continuita' vengono controllate separatamente.
- Chi applica una correzione non esegue la verifica finale.
- Il registro conserva un riepilogo per ciclo, non i dettagli duplicati.
- La cadenza periodica verra' attivata soltanto dopo il primo collaudo reale.

## Scadenze

- Controllo iniziale: prima sessione successiva all'installazione.
- Controllo periodico: ogni 7 giorni dopo la situazione iniziale; avvio manuale
  finche' l'automazione non viene attivata e collaudata.

## Lavori aperti

Questa tabella e' il ponte fra chi ripara e chi controlla. La manutenzione
scrive qui ogni mattina cosa ha fatto; il controllo del lunedi' chiude o boccia
quelle stesse righe. Nessuno cancella la riga di un altro.

| Cosa | Chiesto da | Fatto il | Prova | Stato | Detto dal controllo |
|---|---|---|---|---|---|
| Situazione iniziale della casa | controllo | - | - | DA FARE | - |

Chi comanda il lavoro e' il controllo della casa: il lunedi' guarda tutto e
lascia qui le righe `DA FARE`, con scritto cosa togliere, cosa sistemare e cosa
non si tocca. La manutenzione, ogni mattina, esegue quelle prima delle sue.
Chi ha eseguito non giudica il proprio lavoro.

Gli stati sono cinque e basta:
- `DA FARE`: lo ha chiesto il controllo. Ha la precedenza su tutto.
- `DA VERIFICARE`: la manutenzione l'ha riparato, nessuno l'ha ancora ricontrollato.
- `CHIUSO`: il controllo ha riaperto il file e il lavoro regge. Resta in tabella
  sette giorni, poi sparisce: il registro conserva il numero, non la riga.
- `BOCCIATO`: il controllo ha guardato e non regge, col motivo scritto accanto.
  La mattina dopo la manutenzione riparte da qui, prima di qualunque cosa nuova.
- `AL PROPRIETARIO`: bocciato due volte. Solo queste righe arrivano a te.

Una riga senza prova non puo' essere `CHIUSO`. Una riga che nessuno tocca da
quattordici giorni diventa `AL PROPRIETARIO` da sola.

## Diario

### {{date}}

- Creata la stanza Ecosystem Check.
- Automazioni ricorrenti non attivate.
