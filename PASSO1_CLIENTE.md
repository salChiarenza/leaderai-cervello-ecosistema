# Cervello LeaderAI - installazione e aggiornamento

Versione corrente: `0.7.12`

## Un solo percorso

Il proprietario non deve sapere se la casa e' nuova, vecchia o rimasta a meta'.
Lo decide l'assistente guardando la cartella reale. Scarica sempre il pacchetto
corrente come riferimento; non estrarlo mai sopra la casa del proprietario.

Scarica `Cervello.zip` da qui:
<https://drive.google.com/file/d/1KG_zPed0quUpFHOWrNsLfJaHLoSQE9-Y/view>.
Sta anche nella cartella `1 Cervello`:
<https://drive.google.com/drive/folders/1SzRA4SCSyXw_PnHWP7ouGeNzUv6Wcl1L>.

Il pacchetto contiene soltanto Markdown e JSON. Non installa programmi, skill,
ganci o attivita' e non cambia le impostazioni di Claude, Codex o ChatGPT Work.

## Messaggio da dare all'assistente

Apri Claude Code, Codex o ChatGPT Work nella cartella che deve contenere il
Cervello e incolla:

```text
Apri il pacchetto Cervello.zip che ho scaricato e leggi README.md,
install_contract.json e PACKAGE_VERSION. Il pacchetto e' solo il riferimento:
non copiarlo sopra questa cartella.

Guarda cosa esiste qui e decidi tu se e' una prima installazione, un
aggiornamento o una ripresa. Prima di modificare qualsiasi documento crea o
leggi logs/install-state.json. Conserva tutti i contenuti gia' compilati, crea
solo i file mancanti e aggiorna solo i blocchi LeaderAI delimitati nel
contratto. Dopo ogni file aggiorna lo stato, cosi' una sessione nuova puo'
riprendere dal punto esatto.

Scrivi VERSION con il valore di PACKAGE_VERSION soltanto dopo aver verificato
che tutti i file richiesti esistono e che i contenuti precedenti sono rimasti.
Alla fine mostrami una sola frase: installato, aggiornato oppure ripreso e
completato; versione; eventuali conflitti lasciati intatti.
```

## Come decide l'assistente

- Cartella vuota: crea i file dichiarati dal contratto.
- Casa esistente: conserva tutto, aggiunge i file mancanti e aggiorna soltanto
  i blocchi LeaderAI marcati.
- Stato `IN_PROGRESS` o `INTERRUPTED`: riparte dal primo elemento non completato.
- File esistente senza blocco LeaderAI: non lo sostituisce.
- Conflitto: conserva il file e lo elenca nello stato; non inventa una fusione.

Una casa vecchia senza `VERSION` resta una casa vecchia: non diventa corrente
scrivendo subito un numero. La versione viene dichiarata soltanto dopo il
controllo finale.

## Windows

Il pacchetto corrente contiene i file direttamente alla radice. Dopo
**Estrai tutto**, la cartella corretta e' la prima che mostra subito
`PACKAGE_VERSION`, `README.md` e `install_contract.json`.

Se stai usando un vecchio pacchetto e trovi `Cervello` dentro `Cervello`, usa
la cartella interna che mostra quei tre file. Non lavorare nell'involucro
esterno e non creare un'altra casa.

## Piu' caselle Gmail

Nel file `ecosistema/FONTI.md` ogni Gmail ha una riga distinta. Il proprietario
usa **Aggiungi un altro account** dal menu Google e completa accesso e verifica;
l'assistente prova ogni casella separatamente. Un account aggiunto al browser
non autorizza automaticamente gli altri collegamenti.

## Se l'assistente si ferma

Una sessione nuova deve aprire la stessa cartella e leggere
`logs/install-state.json`: continua dal primo elemento non completato.

Se lo stesso passaggio fallisce due volte, prepara questa email senza inserire
dati personali, percorsi o registri tecnici:

```text
A che punto sono: [passaggio]
Che cosa manca: [ostacolo in parole semplici]
Che computer e assistente uso: [Mac o Windows; Claude, Codex o ChatGPT Work]
```

<mailto:info@salchiarenza.com?subject=Sono%20fermo%20-%20installazione%20Cervello>

## Risultato corretto

- una sola cartella viva;
- tutti i file richiesti dal contratto;
- contenuti precedenti conservati;
- `logs/install-state.json` con stato `COMPLETED`;
- `VERSION` uguale a `PACKAGE_VERSION` soltanto alla fine.

Da quel momento apri sempre la tua AI dentro la cartella della casa: una chat
aperta altrove non vede i documenti appena installati.
