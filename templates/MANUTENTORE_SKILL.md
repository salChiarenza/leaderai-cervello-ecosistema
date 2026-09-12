---
name: manutentore-ecosistema
description: Usa quando l'utente dice fai manutenzione, lancia il Manutentore, pulisci la casa, i file sono troppo grandi, archivia il vecchio, oppure quando l'automazione giornaliera di manutenzione parte. Misura tutta la casa con il guardiano, ripara da solo le cose meccaniche e reversibili, riporta al proprietario il resto.
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

## 2. Ripara (solo queste cose, per ogni stanza)

Ammesso, senza chiedere:

- **Gancio standard mancante o scollegato**: confronta lo script e la
  configurazione della versione gia installata, poi ripristina soltanto quel
  componente e il suo collegamento. Preserva gli altri hook e impostazioni.
  Ripeti il controllo e verifica la ricevuta del successivo evento Stop;
  non attribuire un guasto di codice sconosciuto a una semplice configurazione.
  Se la piattaforma richiede fiducia o un permesso nuovo, registra quel gesto
  umano; non inventare un'avvenuta attivazione. Nessuna routine aggiuntiva.

- **Documento oltre 800 righe o 80 KiB** (file diverso da mappe e chat): sposta
  le sezioni datate (`## gg/mm/aaaa ...` o `## aaaa-mm-gg ...`) piu' vecchie di
  7 giorni in `<nome>_archivio_<aaaa-mm-gg>.md` nella stessa cartella, in cima
  al file di archivio, con una riga di intestazione che dice da dove vengono e
  quando. Nel file vivo lascia una riga `> Archivio: <nome file>`. Se il file
  non ha sezioni datate, non toccarlo: segnalalo al proprietario.
- **Mappa oltre 350 righe** (`AGENTS.md`, `MEMORY.md`): non tagliare. Segnala
  al proprietario con il numero di righe: una mappa si accorpa con giudizio.
- **`AGENT_CHAT.md` oltre 350 righe o con note piu' vecchie di 48 ore**: sposta
  le note vecchie in `AGENT_CHAT_archivio_<aaaa-mm-gg>.md` accanto, lasciando
  in chat le note delle ultime 48 ore e la riga `> Note piu' vecchie: <file>`.
- **Percorso nascosto al proprietario**: rendilo visibile (`chflags nohidden`
  su Mac, `attrib -h` su Windows).
- **Skill gemelle diverse** (`.claude/skills/X/SKILL.md` e
  `.agents/skills/X/SKILL.md`): confronta la fonte comune e correggi solo
  divergenze accertate, preservando gli adattamenti nativi; il file piu recente
  non e automaticamente quello giusto.

Vietato, sempre: eliminare file o cartelle, riscrivere contenuti, spostare
file fuori dalla loro stanza, toccare `.secrets/`, `.git/`, `logs/`, inviare
email o messaggi, creare copie `_v2`/`_finale`, creare nuove stanze. Cartelle
vuote, copie parallele e classi ambigue richiedono una decisione del
responsabile. Per una stanza gia richiesta, completare i pezzi mancanti
rientra nel mandato originario: non serve un secondo consenso.
Contraddizioni non risolvibili dalle fonti restano aperte con le due righe
in conflitto e il responsabile; non riscrivere alla cieca.

## 3. Rimisura

Rilancia `guardiano_stanze.sh --misura`. Le righe sparite sono riparazioni
riuscite; quelle rimaste sono per il proprietario.

## 4. Scrivi

- Negli `Esiti` dichiarati dalla mappa del reparto: data, evento, perimetro,
  riscontro, correzione, prova riletta e residui con responsabile. Per nascita
  registra il primo passaggio richiesta -> fonte -> output -> reparto a valle;
  una connessione esterna e attiva solo dopo una lettura riuscita autorizzata.
- In `ecosystem-check/STATO.md`, sezione `## Manutenzione giornaliera`, in cima:
  data, quante cose trovate, quante riparate (cosa e dove), quante restano e a
  chi. Massimo 5 righe, massimo 7 giornate conservate: le piu' vecchie si
  tolgono.
- Se hai riparato almeno una cosa, una riga in
  `ecosystem-check/REGISTRO_CONTROLLI.md` con data, perimetro, trovati,
  chiusi, aperti, esito `MANUTENZIONE`, prova (il file di archivio creato).
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
