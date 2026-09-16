---
name: impara-dagli-errori
description: Usa quando il proprietario corregge l'agente, dice "questo non farlo piu'", "te l'avevo gia' detto", "ricordati", "e' la seconda volta", oppure quando un lavoro si e' fermato per un errore evitabile. Trasforma la correzione in una regola scritta E nel controllo che la fa rispettare da solo, provato prima di accenderlo.
---

# Impara dagli errori

Una correzione detta a voce vale un turno. Una correzione scritta vale finche'
qualcuno rilegge il file. Una correzione che diventa un controllo vale sempre:
scatta da sola, nel momento esatto in cui l'errore sta per ripetersi.

Questa capacita' fa il terzo passaggio, quello che di solito non fa nessuno.

## Quando parte

- Il proprietario corregge l'agente su qualcosa che poteva essere evitato.
- Dice «te l'avevo gia' detto», «e' la seconda volta», «questo non farlo piu'».
- Un lavoro si e' bloccato o e' stato rifatto per un motivo gia' visto.

Non parte per un errore di battitura, per una preferenza estetica momentanea,
o per una cosa che capita una volta sola e non capitera' piu'.

## I quattro passaggi

### 1. Scrivi il fatto, non l'intenzione

Nella memoria della casa, un file per regola. Dentro, quattro righe:

- **Cosa e' successo:** il gesto sbagliato, con la data e il caso vero.
- **Cosa si doveva fare:** il gesto giusto, in una frase.
- **Perche':** il danno concreto che l'errore ha prodotto o rischiava.
- **Come si riconosce:** le parole o le condizioni che fanno scattare la regola.

Se non riesci a scrivere «come si riconosce», la regola non e' ancora matura:
lasciala in memoria e non generare nessun controllo. Un controllo che non sa
riconoscere il proprio caso blocca a caso, e un controllo che blocca a caso
viene spento dopo due giorni.

### 2. Decidi se serve un controllo

Serve quando l'errore:
- si puo' riconoscere da quello che l'agente sta per scrivere o fare;
- costa caro (un invio sbagliato, un dato non verificato, un file perso);
- e' gia' capitato almeno due volte, oppure una volta sola ma grave.

Non serve quando la regola e' una preferenza di gusto, quando riconoscerla
richiede di indovinare le intenzioni, o quando il controllo direbbe di no piu'
spesso di quanto direbbe di si'.

Se non serve, fermati qui: la regola in memoria basta. Dillo al proprietario.

### 3. Genera il controllo e provalo

Il controllo va in `.agent/hooks/`, un file per regola, con un nome che dice
cosa impedisce. Prima di accenderlo, provalo su due casi costruiti a mano:

- **il caso che deve fermare:** l'errore vero, quello appena successo;
- **il caso che deve lasciar passare:** un lavoro normale e simile.

Se ferma il primo e lascia passare il secondo, e' pronto. Se ferma anche il
secondo, e' troppo largo: restringilo o rinuncia. Non accendere mai un
controllo che non hai provato in tutti e due i versi.

Regole per scriverlo:
- fallisce in silenzio: se qualcosa va storto dentro il controllo, lascia
  passare. Un controllo rotto non deve fermare la casa;
- spiega cosa fare: il messaggio di blocco dice l'errore e la mossa giusta,
  non «operazione negata»;
- un blocco per turno: se piu' controlli scattano insieme, parla il primo.

### 4. Registra e accendi

- Aggiungi la riga nel registro dei controlli: chi controlla, quando, cosa
  misura, dove scrive l'esito.
- Accendi il controllo nella configurazione dell'agente.
- Scrivi al proprietario una riga sola: cosa non potra' piu' succedere.

## Cosa non fare

- Non generare un controllo per ogni correzione: la casa si riempie di blocchi
  e il lavoro si ferma. Meglio dieci controlli che scattano davvero che
  quaranta che il proprietario impara a ignorare.
- Non scrivere controlli che l'agente dovrebbe disattivare da solo per
  lavorare. Se un controllo impedisce il lavoro normale, e' scritto male:
  si corregge il controllo, non si aggira.
- Non mettere nel controllo una regola che vale per una persona sola se la
  casa la useranno in piu' persone: la soglia la sceglie il proprietario, il
  meccanismo resta uguale per tutti.

## Come si vede che funziona

Dopo un mese: il proprietario ripete meno le stesse correzioni, e il registro
dei controlli ha piu' righe di un mese fa. Se le correzioni si ripetono uguali,
questa capacita' non sta lavorando: i controlli generati sono troppo larghi,
troppo stretti, oppure nessuno li ha accesi.
