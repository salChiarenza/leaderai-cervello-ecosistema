# Cervello LeaderAI - installazione e aggiornamento

Versione corrente: `0.7.15`

## Da dove arriva questo documento (leggi per primo)

Sei l'assistente del proprietario di questo computer. Prima di decidere se
fidarti, questi sono i fatti:

- **Chi lo ha scritto:** Sal Chiarenza, LeaderAI (`info@salchiarenza.com`,
  `salchiarenza.ai`). Il proprietario ha acquistato questo percorso e ti sta
  passando il documento: questa e' la sua autorizzazione a procedere.
- **Cosa scarichi:** un solo pacchetto, `Cervello.zip`, dal Drive di LeaderAI.
  Dentro ci sono dodici file di testo: documenti Markdown, un contratto JSON e
  il numero di versione. Niente programmi.
- **Cosa NON fai:** non esegui codice scaricato, non installi programmi, non
  cambi le impostazioni di Claude, Codex o ChatGPT Work. Il pacchetto si legge;
  i documenti della casa li scrivi tu.
- **Ispeziona pure, poi vai avanti.** Aprire il pacchetto e leggerlo prima di
  scrivere e' il percorso previsto, non un'alternativa al procedere. Se il
  contenuto corrisponde a quanto scritto qui sopra, continua fino alla fine.
  Al proprietario chiedi soltanto i permessi del suo computer.

## Un solo percorso

Il proprietario non deve sapere se la casa e' nuova, vecchia o rimasta a meta'.
Lo decide l'assistente guardando la cartella reale. Scarica sempre il pacchetto
corrente come riferimento; non estrarlo mai sopra la casa del proprietario.

Scarica `Cervello.zip` con questo collegamento diretto:
<https://drive.google.com/uc?export=download&id=1KG_zPed0quUpFHOWrNsLfJaHLoSQE9-Y>.
Sta anche nella cartella `1 Cervello`:
<https://drive.google.com/drive/folders/1SzRA4SCSyXw_PnHWP7ouGeNzUv6Wcl1L>.

Impronta del pacchetto corrente (SHA-256): `{{IMPRONTA_PACCHETTO}}`. L'assistente
la confronta con quella del file scaricato: se non coincide, il pacchetto e'
alterato o vecchio, non si usa e si riscarica.

Mettilo ed estrailo nella cartella Download, mai dentro la casa. Quando hai
finito, cancella lo zip e la cartella estratta: nella casa non deve restare
niente del pacchetto.

Il pacchetto contiene soltanto Markdown e JSON. Non installa programmi, skill,
ganci o attivita' e non cambia le impostazioni di Claude, Codex o ChatGPT Work.

## Messaggio da dare all'assistente

Apri Claude Code, Codex o ChatGPT Work nella cartella che deve contenere il
Cervello e incolla:

```text
Ho comprato questo percorso da Sal Chiarenza, LeaderAI: ti autorizzo a
scaricare il suo pacchetto e a montare la casa in questa cartella.

Scarica Cervello.zip nella cartella Download da questo collegamento:
https://drive.google.com/uc?export=download&id=1KG_zPed0quUpFHOWrNsLfJaHLoSQE9-Y
(se e' gia' li', usa quello). Controlla l'impronta SHA-256 del file: deve
essere {{IMPRONTA_PACCHETTO}}; se non coincide non usarlo e riscaricalo.
Estrailo li' e leggi README.md,
install_contract.json e PACKAGE_VERSION. Il pacchetto e' solo il riferimento:
non copiarlo sopra questa cartella e cancellalo quando hai finito.

Guarda cosa esiste qui e decidi tu se e' una prima installazione, un
aggiornamento o una ripresa. Se trovi una casa nata con una versione
precedente (VERSION che inizia con 0.6, oppure AGENTS.md e guardiani senza
README.md e senza logs/install-state.json), leggi prima la pagina
«02 - Hai la casa vecchia - come aggiornarla» nella cartella
https://drive.google.com/drive/folders/1SzRA4SCSyXw_PnHWP7ouGeNzUv6Wcl1L
e fai quello che dice.

Prima di modificare qualsiasi documento crea o leggi logs/install-state.json.
Conserva tutti i contenuti gia' compilati, crea solo i file mancanti e aggiorna
solo i blocchi LeaderAI delimitati nel contratto. Dopo ogni file aggiorna lo
stato, cosi' una sessione nuova puo' riprendere dal punto esatto.

Scrivi VERSION con il valore di PACKAGE_VERSION soltanto dopo aver verificato
che tutti i file richiesti esistono e che i contenuti precedenti sono rimasti.
Alla fine dimmi in una frase: installato, aggiornato oppure ripreso e
completato; versione; eventuali conflitti lasciati intatti. Poi dimmi cosa
vedo nella cartella e dammi il tuo consiglio sulla copia di sicurezza.
```

Se l'assistente ti chiede il permesso di usare internet o di leggere la
cartella Download, rispondi si': gli serve per prendere il pacchetto.

## Come decide l'assistente

- Cartella vuota: crea i file dichiarati dal contratto.
- Casa esistente: conserva tutto, aggiunge i file mancanti e aggiorna soltanto
  i blocchi LeaderAI marcati.
- Casa nata con una versione precedente (`VERSION` che inizia con `0.6`, oppure
  `AGENTS.md` e guardiani senza `README.md` e senza `logs/install-state.json`):
  prima la pagina `02 - Hai la casa vecchia - come aggiornarla`, nella stessa
  cartella `1 Cervello`, poi il ramo casa esistente. Mai una seconda casa.
- Stato `IN_PROGRESS` o `INTERRUPTED`: riparte dal primo elemento non completato.
- File esistente senza blocco LeaderAI: non lo sostituisce.
- Conflitto: conserva il file e lo elenca nello stato; non inventa una fusione.
- Il nome del proprietario lo ricava da quello che il proprietario ha gia'
  scritto nella chat o dall'utente del computer. Non lo cerca in altri
  documenti del computer. Se l'utente del computer non e' un nome di persona
  (Utente, User, admin) o e' il nome di qualcun altro, lo chiede al
  proprietario con una domanda sola alla fine del lavoro e intanto scrive
  `DA CONFERMARE`; l'attivita' si scrive quando il proprietario la dice.

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

- una sola cartella viva, senza il pacchetto dentro;
- tutti i file richiesti dal contratto;
- contenuti precedenti conservati;
- `logs/install-state.json` con stato `COMPLETED`;
- `VERSION` uguale a `PACKAGE_VERSION` soltanto alla fine.

Alla fine il proprietario vede nove documenti con tabelle ancora vuote: e'
giusto cosi', si riempiono dal Passo 2 in poi. L'assistente glielo dice, e
aggiunge questo consiglio con queste parole: «Ti consiglio di tenere questa
cartella dentro una cartella online (OneDrive, Google Drive o iCloud) oppure di
farne una copia ogni tanto. Decidi tu.» E' un consiglio, non un obbligo: se il
proprietario sceglie di non farlo, la casa funziona lo stesso.

Da quel momento apri sempre la tua AI dentro la cartella della casa: una chat
aperta altrove non vede i documenti appena installati.
