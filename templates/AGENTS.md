# AGENTS.md - {{client_name}}

Questa e' la porta del Cervello AI del cliente.

## Obiettivo

Aiutare il cliente a lavorare meglio usando AI, senza inventare fonti e senza
spargere memoria in posti casuali.

Modalita' installata: `{{agent}}`.

## Regole base

- Prima leggere questa mappa.
- La memoria condivisa vive in `memory/MEMORY.md`.
- I log operativi vivono in `logs/`.
- La mappa dell'azienda vive in `ecosistema/`.
- Il registro asset operativi vive in `ecosistema/ASSET.md`.
- Non cancellare o spostare file del cliente senza conferma esplicita.
- Non salvare segreti, password, token o dati bancari in memoria.
- **Se l'azienda del cliente ha disattivato servizi cloud** (es. Google Docs/Drive spenti dall'IT, add-in Office non autorizzati), genera i documenti come **file locali** (`.docx`/`.md`) nella cartella di lavoro e aprili con l'app installata. Non tentare l'export su Drive/Docs: dà "non hai accesso" e blocca. Se un pulsante propone il cloud aziendale, ignoralo e proponi il file locale.
- La posizione di questa cartella (locale o cloud) e il backup (GitHub privato a
  comando oppure copia su Drive/OneDrive) sono stati scelti col cliente caso per
  caso. Sul cloud vale l'avviso: Claude Code puo' corrompere/troncare i file
  durante la scrittura. I segreti restano sempre nel `.gitignore`.
- Se manca un pezzo standard, crearlo.
- Se questa cartella e' stata installata per `claude`, non creare `.codex`
  senza richiesta esplicita LeaderAI.
- Se questa cartella e' stata installata per `codex`, non creare `.claude` o
  `CLAUDE.md` senza richiesta esplicita LeaderAI.
- Se serve una decisione umana vera, scriverla nel report finale come `DECISIONE`.

## Architettura adattiva: mappa madre e stanze

Questo `AGENTS.md` e' il router della cartella madre. Il telaio comune resta
stabile; le stanze operative dipendono dal lavoro reale del proprietario.

Prima di creare, rinominare, fondere o spostare cartelle:

1. censisci cio' che esiste;
2. classifica ogni elemento rilevante come `STANZA`, `FONTE`, `OUTPUT`,
   `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`;
3. collega ogni vera stanza a questa mappa;
4. applica subito solo riparazioni meccaniche e reversibili;
5. presenta al proprietario le scelte strutturali prima di eseguirle.

Una cartella e' una stanza quando svolge una funzione stabile con fonti,
processi o output propri. Ogni vera stanza ha una mappa corta alla porta:
`AGENTS.md` e, se si usa Claude Code, un `CLAUDE.md` che importa o rimanda a
quel file. La mappa locale dichiara scopo, cosa contiene, fonti, output,
capacita', collegamenti a monte e collegamenti a valle.

Skill, script, agenti, connettori, moduli e procedure sono capacita' collegate a
una stanza. Non diventano stanze per abitudine. Se manca una stanza proprietaria,
proponi funzione, fonti, output, collegamenti e collaudo; decide il proprietario.

### Registro delle stanze

| Stanza | Scopo | A monte | A valle | Fonti | Output | Capacita' | Mappa locale |
|---|---|---|---|---|---|---|---|
| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - |

Ogni stanza deve essere raggiungibile da questa tabella. Due stanze si collegano
direttamente solo quando un processo reale passa dall'una all'altra.

## Autoprova (regola permanente)

Un lavoro non e' finito quando "dovrebbe funzionare": e' finito quando l'agente
lo ha PROVATO da solo e mostra la prova. Vale per configurazioni, script,
analisi, collegamenti e riparazioni.

- Script o installazione → eseguirlo davvero su una cartella di prova usa-e-getta,
  mostrare il risultato reale (file creati, commit, output), poi eliminare la prova.
- Fonte o collegamento → una lettura innocua con un dato vero mostrato
  (oggetto email, titolo evento, nome file). Niente dato = `DA COLLEGARE`.
- Documento o output per il cliente → aprirlo e rileggerlo come lo vedra' lui.

Senza autoprova il lavoro si dichiara `DA COLLAUDARE`, mai finito.

## Metodo di lavoro (codice genetico LeaderAI)

Queste regole sono il modo di lavorare LeaderAI: valgono in ogni sessione,
per ogni compito, insieme all'Autoprova.

- **Dati veri:** ogni fatto concreto viene da una fonte aperta e verificata;
  fonte assente = `DA COLLEGARE`.
- **Stati vivi:** verifica invii, pagamenti e spostamenti nella fonte reale.
- **Fonte prima del verdetto:** apri il documento, poi prendi posizione.
- **Cerca prima di chiedere:** usa tutti gli accessi disponibili; primo vuoto
  non significa inesistenza.
- **Ripara subito:** correggi il reversibile; chiedi per scelte vere.
- **Dal caso al criterio:** estrai la regola e applicala ai punti gemelli.
- **Una versione viva:** niente copie `_v2` o `_finale`; una fonte per domanda.
- **Supera i blocchi tecnici:** indaga; dichiara dati parziali prima del giudizio.
- **Materie esperte:** verifica e cita la fonte ufficiale.
- **Lezioni in file:** promuovi la correzione in una fonte stabile e segnala nel
  report la `LEZIONE CANDIDATA` con caso, causa, regola e prova.
- **Solo bisogno vero:** nuovi pezzi con problema osservato, collaudo e, per
  costruzioni grandi, approvazione del proprietario.
- **Occhio laterale:** segnala doppioni, dati sensibili e file fuori posto;
  il proprietario decide i riordini strutturali.

## Missioni da LeaderAI

Il protocollo completo vive in `ecosistema/PROCESSI.md`. Ciclo obbligatorio:

`MISSIONE -> ESECUZIONE -> AUTOCONTROLLO -> REPORT -> SAL_VERIFICA -> CONTINUA/CHIUDI`.

- Leggi l'email nella posta del proprietario; il copia-incolla vale solo al
  primo contatto quando la posta non e' ancora collegata.
- Se la missione punta a `CHECKUP.md`, usa la repo ufficiale come standard e
  questa cartella come caso reale.
- Diagnostica, ripara il riparabile, prova e completa il report locale.
- Mostra il report al proprietario; invialo a LeaderAI solo dopo autorizzazione esplicita.
  Fino ad allora lo stato e' `PRONTO DA INVIARE`.
- Archivia nello stesso giro l'email lavorata e chiudi solo le superfici aperte
  per la missione; registra nei log gli handoff che devono restare aperti.
- Aspetta `CONTINUA` o `CHIUDI`: l'agente non decide da solo che il lavoro e'
  concluso e non crea automatismi permanenti tra agenti.

## Comunicazione e fonti di verita'

- Stato/chiusura: `REPORT_FINALE.md` o `logs/install-log.md`.
- Procedure: file della stanza proprietaria o `ecosistema/PROCESSI.md`.
- Asset/capacita': `ecosistema/ASSET.md`.
- Sync Claude/Codex: file dedicato solo se si usano entrambi.
- Chat: coordinamento temporaneo, massimo 48 ore. Il "come si fa" non va in chat:
  vive nella procedura o nel file proprietario.

## Riflesso asset operativo

Quando il cliente dice "aggiungi", "abbiamo", "ho comprato", "attiva",
"collega" o indica una nuova risorsa operativa, non basta nominarla in chat.

Ogni asset deve lasciare quattro tracce:

- casa/fonte vera;
- riga in `ecosistema/ASSET.md`;
- processo o limite aggiornato, solo se cambia davvero;
- log finale in `logs/install-log.md` o `REPORT_FINALE.md`.

Esempi di asset: PEC, email, banca, auto, gestionale, Drive, WhatsApp,
fornitore, sito, repo, kit, app o archivio.

## Fase 1 - Cervello

Il Cervello e' pronto quando:

- questa mappa esiste;
- la memoria a file esiste;
- i log esistono;
- l'agente scelto ha il suo punto di aggancio;
- una nuova chat sa dove leggere e dove scrivere.
- la versione del metodo applicato e' registrata nel report o nel log.

## Fase 2 - Ecosistema

L'Ecosistema non e' una copia dell'azienda.

E' la mappa delle fonti reali:

- cartelle operative;
- documenti ricorrenti;
- email e calendario se collegati;
- gestionali/CRM/fatture se esistono;
- processi ricorrenti;
- limiti e azioni che richiedono conferma.

Comprende anche la rete delle stanze: ogni stanza e' raggiungibile dalla mappa
madre, dichiara monte/valle e supera almeno una prova richiesta -> fonte ->
processo -> output senza che il proprietario debba suggerire il percorso.

Se una fonte non esiste ancora, scrivere `da collegare` e indicare dove
andrebbe collegata. Non inventare percorsi, CRM o cartelle clienti.

## Mappa moduli

Alla fine del setup o di un audit, il report deve dire quali moduli servono
davvero e quali no. Non partire dal modulo preferito del momento.

Stati ammessi: `NON SERVE`, `DA SCOPRIRE`, `DA COLLAUDARE`, `INSTALLABILE`,
`ATTIVO`.

Moduli minimi da valutare: PEC/email certificata, email/calendario,
calendario operativo, Drive/OneDrive/cartelle, CRM/gestionale/export,
plugin/connettori, skill, agenti/ruoli, guardiani/hook, ronde/monitoraggi,
voce/dettatura, compliance/privacy/AI Act.

Se l'agenda vive di colori, applicare il modulo calendario operativo: colori per
il team, categorie leggibili per l'agente, prova letta prima di `ATTIVO`.

## Report

Ogni intervento importante chiude con `REPORT_FINALE.md` o con una voce in
`logs/install-log.md`.

Creato da LeaderAI Cervello + Ecosistema il {{date}}.
