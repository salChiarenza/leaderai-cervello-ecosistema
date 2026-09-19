# Cervello LeaderAI - Passo 1

Versione corrente: `0.7.10`

## Prima cosa: guarda dove sei (lo decidi tu, assistente)

Il proprietario non deve dirti in che stato e' la sua casa: lo vedi tu. Nella
cartella aperta, o in quella che ti indica, cerca `VERSION` e i documenti del
contratto.

- li trovi: e' una casa gia' installata, vai a `Hai gia' la casa: come si
  aggiorna` e non scaricare il pacchetto;
- non li trovi ma la cartella e' viva lo stesso - documenti compilati, memoria
  scritta, registri, lavoro del proprietario, sue cartelle - allora e' una casa
  nata con una versione precedente, quando quei due file non c'erano ancora. E'
  comunque una casa gia' installata: vai all'aggiornamento, non scaricare il
  pacchetto, e come primo gesto scrivile il file della versione con il numero
  qui sopra. Non crearne mai una seconda accanto;
- non li trovi e la cartella e' vuota: e' una prima installazione, prosegui da qui.

Se hai un dubbio, dillo in una riga con quello che hai visto e proponi il ramo
che ritieni giusto.

## Il risultato

Alla fine hai una sola cartella di lavoro con nove documenti ordinari: memoria,
fonti, strumenti, processi, limiti, soggetti, chat e registro di installazione.
Il pacchetto non contiene programmi e non cambia le impostazioni di Claude o
Codex. Skill, controlli automatici e attivita' programmate appartengono al
Passo 4 e richiedono una scelta separata.

## Da adesso: apri sempre la tua AI dentro la cartella

Ogni volta che parli con la tua AI, aprila dentro la cartella della casa, la
stessa che hai usato per installare. Da una chat nuova, aperta senza cartella,
non vede i suoi file: risponde a vuoto o si blocca. Vale per Claude, Codex e
ChatGPT Work. Se ti risponde `FUORI DAL CERVELLO`, hai aperto la chat nel posto
sbagliato: chiudila e riaprila dalla cartella.

## Cosa scaricare

Nella stessa cartella Drive di questa guida trovi `Cervello.zip`. Dentro devono
esserci soltanto:

- `VERSION` e `install_contract.json`;
- file Markdown nei percorsi indicati dal contratto;
- nessun file eseguibile e nessuna cartella di configurazione dell'assistente.

Se il contenuto e' diverso, fermati e segnalalo a LeaderAI.

## Installazione semplice

1. Scarica `Cervello.zip` e decomprimilo.
2. Rinomina la cartella `Cervello` con il nome della tua attivita'.
3. Spostala nella posizione in cui vuoi lavorare.
4. Apri quella cartella come progetto locale in Claude Code o Codex.
5. Invia all'assistente il messaggio qui sotto.

```text
Questa e' la mia cartella di lavoro LeaderAI. Leggi README.md,
install_contract.json e i documenti presenti. Verifica che il pacchetto
contenga soltanto file Markdown e JSON nei percorsi dichiarati.

Poi sostituisci nei documenti solo questi dati:
- {{client_name}} = [scrivi qui il tuo nome o quello dell'attivita']
- {{date}} = [data di oggi]
- {{version}} = il valore del file VERSION

Non aggiungere skill, programmi, collegamenti ad account, configurazioni
dell'assistente o attivita' programmate. Non sovrascrivere eventuali documenti
gia' compilati: se ne trovi, mostrami il conflitto.

Alla fine mostrami: percorso della cartella, versione e lista dei nove
documenti. Il risultato e' corretto solo se tutti esistono e i segnaposto sono
stati sostituiti.
```

## Verifica visibile

La cartella e' pronta quando:

- `VERSION` mostra `0.7.10`;
- esistono tutti i nove documenti elencati in `install_contract.json`;
- nei documenti non restano `{{client_name}}`, `{{date}}` o `{{version}}`;
- non sono comparse cartelle nascoste di configurazione o file eseguibili.

## Hai gia' la casa: come si aggiorna

Sei qui perche' hai trovato una casa gia' installata. Non scaricare il
pacchetto: si aggiorna quella. App, dati e documenti gia' compilati non si
toccano. Il proprietario deve scegliere una cosa sola, la cartella delle copie di
sicurezza: tutto il resto lo porti a termine tu.

Cosa cambia con questa versione:

- la casa non tiene piu' il registro delle modifiche;
- al suo posto una copia di sicurezza datata della casa, ripetuta ogni giorno,
  con le ultime sette conservate; restano fuori i segreti e gli archivi
  dichiarati protetti. Orario, cartella e modo di fermarla stanno nelle
  istruzioni collegate qui sotto;
- controllo, Ispettore, Manutentore e guardiano si aggiornano dalla cartella
  `4 Gestione dell'ecosistema` del prodotto,
  <https://drive.google.com/drive/folders/1wdSNouSCbuF7G8Ab_m8R_Kw0uGnphc2Q>,
  leggibile senza account Google.

Passaggi per l'assistente, in quest'ordine:

1. leggi `CHECKUP.md` e le istruzioni di Ispettore, Manutentore e guardiano
   nella cartella collegata;
2. chiedi al proprietario in quale cartella tenere le copie di sicurezza e
   attendi la risposta;
3. crea subito la prima copia datata della casa, lasciando fuori segreti e
   archivi protetti;
4. soltanto dopo che quella copia esiste, togli dalla casa il registro delle
   modifiche;
5. attiva la copia giornaliera come descritto nelle istruzioni collegate,
   conservando le ultime sette;
6. aggiorna soltanto i file del controllo, conservando stato e registri gia'
   compilati dal proprietario;
7. ripeti il controllo e misura quanto dura;
8. verifica senza modificare dati che le app e i documenti gia' presenti
   continuino ad aprirsi.

Una capacita' nuova non entra in automatico: si presenta con effetto, percorso e
modo di disattivarla, e la sceglie il proprietario.

L'aggiornamento e' concluso quando nella casa non c'e' piu' il registro delle
modifiche, una copia datata esiste nella cartella scelta dal proprietario, la
copia giornaliera e' attiva, il controllo arriva a un verdetto e le app di prima
funzionano come prima.

Questo chiude il Passo 1. Il Passo 2 serve a compilare la mappa del lavoro con
fonti e processi reali.
