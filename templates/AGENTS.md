# AGENTS.md - {{client_name}}

Questa e' la porta del Cervello AI del cliente.

## Obiettivo

Aiutare il cliente a lavorare meglio usando AI, senza inventare fonti e senza
spargere memoria in posti casuali.

Modalita' installata: `{{agent}}`.
Versione standard applicata: `{{version}}`.

## Regole base

- Prima leggere questa mappa.
- La memoria condivisa vive in `memory/MEMORY.md`.
- Per Claude Code `autoMemoryDirectory` punta alla stessa `memory/`: due
  memorie attive sono un blocco, non due livelli complementari.
- `logs/install-log.md` registra solo installazione e cambi strutturali.
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
- `CLAUDE.md` c'e' SEMPRE ed e' solo il ponte di una riga (`@AGENTS.md`)
  verso questa mappa: Claude Code legge `CLAUDE.md`, Codex legge `AGENTS.md`
  (doc ufficiali verificate 27/07/2026). Se manca, crearlo dal template.
- Se questa cartella e' stata installata per `claude`, non creare `.codex`
  senza richiesta esplicita LeaderAI.
- Se Claude Code e' attivo, configura
  `.claude/settings.local.json:autoMemoryDirectory` sul percorso assoluto
  `memory/`, accetta il trust del workspace e verifica la destinazione con
  `/memory`. Prima di spostare una memoria esterna, confronta e unisci le voci:
  non perdere ne' duplicare apprendimenti.
- Se questa cartella e' stata installata per `codex`, non creare `.claude/`
  senza richiesta esplicita LeaderAI; il ponte `CLAUDE.md` resta comunque.
- Se serve una decisione umana vera, scriverla nel report finale come `DECISIONE`.

## Architettura adattiva: mappa madre e stanze

Questo `AGENTS.md` e' il router della cartella madre. Il telaio comune resta
stabile; le stanze operative dipendono dal lavoro reale del proprietario.

### Ciclo obbligatorio delle cartelle

Ogni volta che crei, rinomini, fondi, sposti o trovi una cartella nuova:

1. censisci cio' che esiste;
2. classifica ogni elemento rilevante come `STANZA`, `FONTE`, `OUTPUT`,
   `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`;
3. assegna un proprietario: nessuna cartella resta senza una stanza che la
   governa;
4. se e' una vera stanza, creala o integrala dal calco locale
   `ecosistema/STANZA_AGENTS.md`, aggiungi `CLAUDE.md` con il solo
   `@AGENTS.md` e collegala nel registro qui sotto;
5. se e' una sottocartella ordinaria, dichiarala nella mappa della stanza
   proprietaria senza trasformarla in una nuova stanza;
6. applica subito le riparazioni meccaniche e reversibili;
7. presenta al proprietario fusioni, spostamenti, eliminazioni o cambi di
   proprieta' che coinvolgono contenuti preesistenti.

Una cartella e' una stanza quando svolge una funzione stabile con fonti,
processi o output propri. Ogni vera stanza ha sempre una mappa corta alla
porta: `AGENTS.md` come fonte unica e `CLAUDE.md` come ponte di una riga
(`@AGENTS.md`). La mappa locale dichiara scopo, cosa contiene, fonti, output,
capacita', collegamenti a monte e collegamenti a valle.

Skill, script, agenti, connettori, moduli e procedure sono capacita' collegate a
una stanza. Non diventano stanze per abitudine. Se manca una stanza proprietaria,
proponi funzione, fonti, output, collegamenti e collaudo; decide il proprietario.

### Registro delle stanze

| Stanza | Scopo | A monte | A valle | Fonti | Output | Capacita' | Mappa locale |
|---|---|---|---|---|---|---|---|
| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - |

La prima cella di ogni stanza usa il formato `[Nome](percorso-relativo)`.
Ogni stanza deve essere raggiungibile da questa tabella. Due stanze si
collegano direttamente solo quando un processo reale passa dall'una all'altra.

### Ispettore Ecosistema

Se il proprietario dice `lancia l'Ispettore`, `controlla l'Ecosistema`,
`verifica le strade`, `cerca doppioni` o formule equivalenti, usa la skill
`ispettore-ecosistema` dell'agente attivo e applica il `CHECKUP.md` ufficiale.
La capacita' e' registrata in `ecosistema/ASSET.md`.

L'Ispettore e' obbligatorio anche dopo un cambiamento strutturale. Prima di
salvare verifica almeno:

- nessuna cartella visibile senza classe e proprietario;
- nessuna stanza senza `AGENTS.md`, `CLAUDE.md` e collegamento alla radice;
- nessuna cartella generica, vuota, doppia o tecnica rimasta come lavoro;
- nessun file sciolto nella home senza stanza proprietaria;
- nessuna memoria parallela o report temporaneo presentato come stato vivo;
- due percorsi reali `richiesta -> stanza -> fonte -> processo -> output`.

Un residuo vuoto o inutile creato dall'agente nel lavoro corrente viene
eliminato prima del salvataggio. I contenuti preesistenti del proprietario si
spostano, fondono o eliminano solo dopo conferma. Finche' resta uno di questi
buchi il verdetto e' `NON PASSA`.

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
- Mostra il report al proprietario; invialo a LeaderAI solo dopo
  autorizzazione esplicita per quello specifico invio.
  Fino ad allora lo stato e' `PRONTO DA INVIARE`.
- Archivia nello stesso giro l'email lavorata e chiudi solo le superfici aperte
  per la missione; registra nei log gli handoff che devono restare aperti.
- Aspetta `CONTINUA` o `CHIUDI`: con `CONTINUA` aggiorna il report e chiede una
  nuova autorizzazione prima dell'eventuale nuovo invio; l'agente non decide da solo
  che il lavoro e' concluso e non crea automatismi permanenti tra agenti.

## Comunicazione e fonti di verita'

- Stato business corrente: file proprietario della stanza, con stato, prossimo
  passo e scadenze in testa; diario sotto, dal piu' recente.
- Storia tecnica/strutturale: soltanto `logs/install-log.md`.
- `REPORT_FINALE.md`: output temporaneo e datato della missione aperta, mai
  fonte di stato. Dopo `CHIUDI` si promuovono i fatti nelle fonti proprietarie
  e il report si elimina.
- Procedure: file della stanza proprietaria o `ecosistema/PROCESSI.md`.
- Asset/capacita': `ecosistema/ASSET.md`.
- Sync Claude/Codex: file dedicato solo se si usano entrambi.
- Chat di gruppo: `AGENT_CHAT.md` nella cartella madre, bacheca comune di
  tutti gli agenti della casa. Prima di modificare file importanti si annuncia
  li'; note in cima, massimo 48 ore, poi si promuovono nel file proprietario.
  Il "come si fa" vive nella procedura o nel file proprietario, la chat porta
  solo il coordinamento.

## Riflesso asset operativo

Quando il cliente dice "aggiungi", "abbiamo", "ho comprato", "attiva",
"collega" o indica una nuova risorsa operativa, non basta nominarla in chat.

Ogni asset deve lasciare quattro tracce:

- casa/fonte vera;
- riga in `ecosistema/ASSET.md`;
- processo o limite aggiornato, solo se cambia davvero;
- log in `logs/install-log.md` solo se cambia installazione o struttura.

Esempi di asset: PEC, email, banca, auto, gestionale, Drive, WhatsApp,
fornitore, sito, repo, kit, app o archivio.

## Fase 1 - Cervello

Il Cervello e' pronto quando:

- questa mappa esiste;
- la memoria unica a file esiste e Claude Code, se attivo, usa la stessa
  directory tramite `autoMemoryDirectory`;
- i log esistono;
- l'agente scelto ha il suo punto di aggancio;
- una nuova chat sa dove leggere e dove scrivere.
- la versione del metodo applicato e' dichiarata in questa mappa e nel log
  tecnico.

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

## Contenuti business e derivati

Testi, regole, modelli e contenuti che il proprietario deve poter correggere
vivono in una fonte esterna al codice, dichiarata nella stanza proprietaria.
App e script leggono quella fonte e generano PDF, Word o altri derivati. Se la
fonte manca o non e' valida, l'elaborazione fallisce in modo visibile: vietato
usare una seconda copia hardcoded che diverge in silenzio.

## Report

Durante una missione si usa un solo `REPORT_FINALE.md`, con data/ora e stato
`APERTA` o `PRONTO DA INVIARE`. E' un output temporaneo ignorato da Git. Dopo
`CHIUDI`, i fatti stabili vengono promossi nel file proprietario o nel log
tecnico se riguardano la struttura, poi il report viene eliminato.

Creato da LeaderAI Cervello + Ecosistema il {{date}}.
