---
name: manutentore-ecosistema
description: Usa quando l'utente dice fai manutenzione, lancia il Manutentore, pulisci la casa, i file sono troppo grandi, archivia il vecchio, oppure quando l'automazione giornaliera di manutenzione parte. Riconcilia e snellisce le fonti esistenti, ripara i collegamenti verificati e riporta al proprietario le eccezioni.
---

# Manutentore Ecosistema

Il Manutentore coordina la manutenzione degli Amministratori dei reparti.
Ogni reparto mantiene i suoi contenuti e collegamenti; le sottocartelle
ne ereditano il responsabile. Una sola routine legge le mappe correnti:
un reparto nuovo entra nel giro senza creare agenti o timer aggiuntivi.
L'Ispettore verifica esiti e prove, anche con un passaggio indipendente.

## Avvio senza doppio consenso

Se l'utente ha detto `fai manutenzione`, `lancia il Manutentore`, `pulisci la
casa`, `archivia il vecchio` o l'automazione giornaliera e' partita, comincia
subito. Non chiedere conferma per le riparazioni ammesse qui sotto: sono
reversibili e restano nella casa.

## 1. Misura

1. Posizionati nella cartella madre (quella con `AGENTS.md` e `.agent/hooks/`).
2. Esegui `bash .agent/hooks/guardiano_stanze.sh --misura` (su Windows:
   `powershell .agent/hooks/guardiano_stanze_windows.ps1 --misura`). Ogni riga
   stampata e' un problema con il suo percorso. Nessuna riga significa soltanto soglie e struttura verificate;
   controlla comunque le modifiche nei contenuti ai punti 3-5.
3. Rileggi il registro delle stanze e la sezione `Manutenzione` di ogni mappa:
   l'elenco non e' fisso. Raggruppa i problemi per responsabile, comprese le
   sottocartelle; infrastruttura comune, ganci, configurazioni e routine fanno
   capo a Ecosystem Check. Non leggere segreti per censirne la presenza.
4. Per ogni reparto con lavoro nuovo o difetti: leggi istruzioni, memoria e
   fonti coinvolte, cerca ripetizioni, regole contraddittorie, percorsi rotti,
   dati fuori posto e passaggi tra reparti incompleti. La misura numerica non
   sostituisce questo controllo del contenuto. Leggi gli Esiti prima di
   aprire incarichi: riprendi quello aperto per lo stesso difetto.
5. All'evento nascita/modifica il medesimo giro avviene nella sessione che sta
   lavorando, prima della chiusura. Completa mappa e collegamenti gia autorizzati;
   non aspettare il giorno dopo. Il guardiano Stop ferma una nascita incompleta.
   Per cambi realizzati fuori dall'agente, la misura giornaliera recupera i difetti.

## 2. Ripara e semplifica

Applica `ecosystem-check/STANDARD_REPARTO.md`, sezione «Igiene dei file»:
e' la fonte comune per manutenzione di contenuti, memoria e collegamenti.
Fa parte del mandato anche correggere e accorpare testi sulla base delle
prove, preservando obblighi, eccezioni, problemi aperti e storico utile.
Il precedente divieto generale di riscrivere contenuti e' sostituito da
questo criterio: dubbi non risolti dalle fonti vanno al responsabile.

Riusa fonti, registri, controlli e routine esistenti. Un nuovo guasto si
corregge prima nel componente che gia svolge quella funzione. Non aggiungere
un'altra regola o un altro guardiano per evitare di ripararlo.

Restano ammesse le riparazioni meccaniche:
- gancio scollegato: ripristina il collegamento alla fonte installata, preserva
  gli altri ganci e verifica l'evento successivo; non inventare permessi;
- skill gemelle: confronta la fonte comune, preserva differenze native;
- percorso nascosto: rendilo visibile al proprietario;
- chat oltre 48 ore: promuovi le decisioni valide e riassumi nello storico
  esistente. Non creare un archivio o un altro stato per far rientrare una soglia;
  spostare tutto altrove non e' snellimento. Il contenuto dubbio resta nella
  sua fonte e il problema resta aperto, senza una copia aggiuntiva.

Vietato, sempre: eliminare file o cartelle senza un mandato specifico;
modifiche business, accessi a segreti, invii o disattivazioni esterne non sono
impliciti nella pulizia.
`.secrets/`, `.git/` e prove tecniche originali restano protetti.
L'Ispettore verifica la semplificazione e ripete il passaggio reale.

## 3. Rimisura

Rilancia `guardiano_stanze.sh --misura`. Le righe sparite sono riparazioni
riuscite; quelle rimaste sono per il proprietario.

## 4. Scrivi

- Negli `Esiti` dichiarati dalla mappa del reparto: data, evento, perimetro,
  riscontro, correzione, prova riletta e residui con responsabile. Per nascita
  registra il primo passaggio richiesta -> fonte -> output -> reparto a valle;
  una connessione esterna e attiva solo dopo una lettura riuscita autorizzata.
- In `ecosystem-check/STATO.md`, sezione `## Misure giornaliere`, in cima:
  data, quante cose trovate, quante riparate (cosa e dove), quante restano e a
  chi. Massimo 5 righe, massimo 7 giornate conservate: le piu' vecchie si
  tolgono.
- Se hai riparato almeno una cosa, una riga in
  `ecosystem-check/REGISTRO_CONTROLLI.md` con data, perimetro, trovati,
  chiusi, aperti, esito `MANUTENZIONE`, prova nella fonte esistente.
- Rileggi `ecosystem-check/CONTROLLI.md`: ogni riga `MANCA` va ripetuta al
  proprietario finche' non diventa `ATTIVO`.

## 5. Riporta

Se nulla cambia e non serve una decisione, termina in silenzio.
Al proprietario al massimo 5 righe in parole normali: quante cose, cosa hai
sistemato, cosa resta a lui e dove sta il resoconto. Niente percorsi lunghi,
niente sigle. Poi chiudi ogni superficie aperta e termina la sessione.

## Automazione

L'installazione crea l'automazione giornaliera `manutenzione-ecosistema`
(ore 07:45 locali, modello leggero) che invoca questa skill. Chi la apre la
chiude: una sola sessione, nessun accumulo. Se l'automazione manca, il checkup
la segnala e la fa creare.

Creato da LeaderAI Cervello + Ecosistema il {{today}} per {{client_name}}
(standard {{version}}).

Il guardiano scrive una sola ricevuta `.agent/guardiano-ultimo-evento.json`
quando riceve Stop con sessione e casa: data, esito e impronte del codice.
`--misura` non la produce; un lancio manuale con payload puo produrla e non
prova l'origine automatica. L'Ispettore incrocia sessione e cronologia nativa,
controlla l'assenza di simulazioni manuali e confronta la ricevuta con
configurazione e codice attuali e distingue assenza, esito BLOCCO e prova
eseguita prima dell'ultima modifica; non dichiara un avvio da un file presente.
