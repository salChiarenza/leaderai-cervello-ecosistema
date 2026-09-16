---
name: manutentore-ecosistema
description: Usa quando l'utente dice fai manutenzione, lancia il Manutentore, pulisci la casa, i file sono troppo grandi, archivia il vecchio, oppure quando l'automazione giornaliera di manutenzione parte. Riconcilia le fonti, riprende gli incarichi interrotti e porta le riparazioni alla verifica.
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
reversibili e restano nella casa. Per tutti i ruoli vale il mandato comune in
`ecosystem-check/STANDARD_REPARTO.md`, «Autonomia operativa»: l'incarico iniziale
include riparazione, verifica e ripresa, non un nuovo consenso a ogni passaggio.

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
   aprire incarichi: riprendi quello aperto per lo stesso difetto. Rileggi gli
   incarichi aperti anche a misura vuota: «assegnato» con esecutore finito o mai
   avviato richiede ripresa nello stesso incarico se eseguibile. IN ATTESA/BLOCCATA:
   attendi il cambiamento della dipendenza o la riverifica prevista, senza rilanci identici.
5. All'evento nascita/modifica il medesimo giro avviene nella sessione che sta
   lavorando, prima della chiusura. Completa mappa e collegamenti gia autorizzati;
   non aspettare il giorno dopo. Il guardiano Stop ferma una nascita incompleta.
   Per cambi realizzati fuori dall'agente, la misura giornaliera recupera i difetti.

## 2. Ripara e semplifica

Leggi integralmente le sezioni «Autonomia operativa» e «Igiene dei file» di
`ecosystem-check/STANDARD_REPARTO.md` prima di intervenire: sono il mandato
comune e il metodo per manutenzione di contenuti, memoria e collegamenti.
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
Se hai corretto qualcosa, avvia l'Ispettore con `Agent`/`Task` in Claude oppure
`spawn_agent` in Codex, secondo il mandato comune, e attendi il suo risultato.
Fornisci le fonti e il difetto originale; il revisore ripete il percorso reale.
«Non disponibile» richiede uno strumento realmente assente o un avvio fallito,
mai un'ipotesi. Senza quella verifica lo stesso incarico resta DA VERIFICARE,
non CHIUSO: ripresa alla regia nella routine esistente, non controllo al titolare.

## 3. Rimisura

Rilancia `guardiano_stanze.sh --misura`. La scomparsa del segnale non prova
la riparazione: riapri la fonte e ripeti il percorso che falliva. I problemi
rimasti tornano al responsabile e alla regia nello stesso incarico.
Al proprietario arrivano solo decisioni e limiti reali fuori dal mandato.

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
- Rileggi `ecosystem-check/CONTROLLI.md`: ogni riga `MANCA` deve avere un incarico
  con responsabile, prova attesa e ripresa; non ripetere allarmi invariati al
  proprietario e non renderla `ATTIVO` per il solo fatto che e' stata assegnata.

## 5. Riporta

Il resoconto ordinario resta nella fonte. Notifica il proprietario soltanto per
problemi gravi, decisioni o gesti umani reali: al massimo 5 righe con fatto,
conseguenza e scelta necessaria. Nessun allarme invariato. Niente percorsi lunghi,
niente sigle. Poi chiudi ogni superficie aperta e termina la sessione.

## Automazione

Mandato iniziale da salvare nel campo prompt della routine, non soltanto come
rimando a questa skill (la piattaforma deve ricevere anche l'incarico al revisore):

> Esegui la manutenzione ordinaria con la skill manutentore-ecosistema e usa un verificatore distinto per le correzioni. Riprendi gli incarichi autorizzati fino alla prova del risultato, mantenendo i limiti del titolare.

L'installazione crea l'automazione giornaliera `manutenzione-ecosistema`
(ore 07:45 locali, modello leggero) che invoca questa skill. Chi la apre la
chiude: una sola sessione, nessun accumulo. La sua cartella di lavoro e' la
cartella madre, con il percorso completo: senza cartella di lavoro parte dalla
cartella predefinita del sistema e il controllo FUORI DAL CERVELLO la ferma a
ogni giro. Se manca, l'installatore riprende
l'installazione autorizzata sul runtime disponibile: niente seconda automazione.
Prova un'esecuzione nativa e la ripresa di un incarico interrotto; non attestare
autonomia continua dalla sola configurazione. Host o applicazione spenti e
permessi mancanti restano limiti espliciti, mai aggirati.

Creato da LeaderAI Cervello + Ecosistema il {{date}} per {{client_name}}
(standard {{version}}).

Il guardiano scrive una sola ricevuta `.agent/guardiano-ultimo-evento.json`
quando riceve Stop con sessione e casa: data, esito e impronte del codice.
`--misura` non la produce; un lancio manuale con payload puo produrla e non
prova l'origine automatica. L'Ispettore incrocia sessione e cronologia nativa,
controlla l'assenza di simulazioni manuali e confronta la ricevuta con
configurazione e codice attuali e distingue assenza, esito BLOCCO e prova
eseguita prima dell'ultima modifica; non dichiara un avvio da un file presente.
