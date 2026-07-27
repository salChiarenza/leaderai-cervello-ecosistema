# Checkup — il Cervello a confronto con i docs ufficiali

Missione per l'agente del proprietario (Claude Code o Codex). Si lancia
dicendo all'agente: "esegui il checkup LeaderAI" (questo file, `CHECKUP.md`,
nella repo gia' presente o letta come standard LeaderAI). Si puo' rifare ogni
volta che serve: dopo un aggiornamento, ogni tot settimane, o quando qualcosa
non torna.

Nota per chi mantiene LeaderAI: questo `CHECKUP.md` versionato e' la fonte
unica della procedura. Nel workspace interno
`leaderai/leaderai-ecosistema/setup/AUDIT_FASE_1_CERVELLO.md` resta soltanto un
puntatore a questa versione pubblicata.

## Regola madre - standard contro caso reale

La repo GitHub `salChiarenza/leaderai-cervello-ecosistema` e' lo standard
LeaderAI. La cartella viva del cliente e' il caso reale.

Regola breve: non riparare a sentimento. `CHECKUP.md` non ripara a sentimento:

- `MANIFEST.md` e' lo standard di conformita';
- `templates/AGENTS.md` e' il comportamento atteso dell'agente nella cartella
  cliente;
- `AGENTS.md` e `README.md` spiegano come usare la repo;
- la documentazione ufficiale viva Claude/Codex verifica solo la parte tecnica,
  non sostituisce lo standard LeaderAI.

Ogni diagnosi deve quindi dire: cosa c'e' nella cartella viva, cosa chiede lo
standard della repo, cosa ho riparato, cosa resta fuori standard e perche'.
Non basta trovare file rotti: devi portare il caso reale allo standard
LeaderAI, salvo blocchi umani veri.

## Modello email missione checkup

Oggetto: `Checkup Ecosistema`

```text
Questa missione e' per l'agente AI che lavora sull'ambiente del cliente.

Usa la repo GitHub `salChiarenza/leaderai-cervello-ecosistema`.
Se la repo e' gia' presente sul computer, aggiornala e apri `CHECKUP.md`.
Se la repo locale non e' presente, usa GitHub come riferimento di lettura per
`CHECKUP.md`, `MANIFEST.md` e `templates/AGENTS.md`. Crea un clone tecnico
temporaneo solo dopo conferma esplicita.

Usa `MANIFEST.md` come standard di conformita'. La cartella viva del cliente e'
il caso reale: confrontala con lo standard della repo e con
`templates/AGENTS.md`.

Prima di dichiarare che non ci sono doppioni o cartelle tecniche fuori posto,
fai la ricerca estesa obbligatoria: cerca anche nomi non standard, nomi
brandizzati e typo come `LeaderAI`, `Leader AI`, `leaderai`, `leader ai`,
`leder ai`, `cervello`, `ecosistema`, `_leaderai`, `install`, `setup`, `repo`,
`clone`. Ogni risultato va classificato e spiegato.

Fai diagnosi, ripara gli scostamenti riparabili, prova quello che dichiari e
completa il report finale locale. Mostralo al proprietario e chiedi la sua
autorizzazione esplicita prima di inviarlo a LeaderAI.

Dopo il report aspetta risposta LeaderAI: `CONTINUA` o `CHIUDI`.
```

Sei l'agente AI sul computer del proprietario. Fai la diagnosi della
configurazione, la confronti con la documentazione UFFICIALE VIVA e **ripari
da solo quello che trovi rotto o mancante, nello stesso turno**. Regola
LeaderAI (autodiagnosi + auto-riparazione): niente botta-risposta col
proprietario, niente referto con domande. Il proprietario riceve il resoconto
di quello che HAI GIA' sistemato, con la prova.

Non inviare report intermedi del tipo "dimmi cosa faccio / manca questo / cosa
non va". L'ordine obbligatorio e': diagnosi -> riparazione -> prova ->
resoconto finale. Restano fuori solo permessi, login, hardware o scelte di
business che non puoi decidere da solo.

Ripari da solo: file standard mancanti, frontmatter sbagliati, symlink/copie
disallineate, configurazioni errate, memoria non agganciata, permessi con
sintassi non valida, percorsi rotti. Chiedi SOLO dove serve davvero l'umano:
permessi di sistema, accessi/account, cancellazione di file creati dal
proprietario, scelte vere di business. Le istruzioni di business
(`AGENTS.md`/`CLAUDE.md` del proprietario) NON si riscrivono da soli: li' si
segnala e si propone.

## Passo 0 — Usa lo standard LeaderAI aggiornato

Se la repo standard `salChiarenza/leaderai-cervello-ecosistema` e' gia'
presente sul computer, entra nella cartella e aggiorna:

```
git pull --ff-only
```

Se `git pull` porta modifiche, **rileggi questo file dall'inizio**: potresti
star leggendo una versione superata.

Leggi `VERSION` e `CHANGELOG.md`. Cerca nel report o nei log della cartella viva
l'ultima versione del metodo applicata. Registra entrambe nel checkup e applica
le lezioni compatibili emerse dopo quella versione; aggiorna la versione
applicata solo dopo aver ripetuto i collaudi.

Se la repo locale non e' presente, usa GitHub come riferimento di lettura per i
file standard (`CHECKUP.md`, `MANIFEST.md`, `templates/AGENTS.md`, `AGENTS.md`,
`README.md`) tramite WebFetch/browser o strumento equivalente. Se non puoi
leggerli online, chiedi una sola conferma per creare un clone tecnico
temporaneo in cartella temporanea di sistema. Il checkup di un ambiente gia'
installato parte dalla cartella viva del cliente, non dalla creazione di nuove
cartelle tecniche.

## Passo 0-bis - Apri il metro di giudizio

Prima di diagnosticare la cartella viva, apri nella repo aggiornata:

- `MANIFEST.md`;
- `templates/AGENTS.md`;
- `AGENTS.md`;
- `README.md`.

Da questo momento il lavoro non e' "controllare un po' di file". Il lavoro e':
confrontare la cartella viva del cliente contro lo standard LeaderAI scritto in
questa repo.

## Passo 0-ter — Trova la cartella viva prima di giudicare

Se questa missione parla di diagnosi, checkup o correzione, parti dal
presupposto che l'ambiente AI sia gia' stato installato da qualche parte. Non
creare una nuova cartella per "fare ordine": prima devi trovare quella viva.

Il nome non basta. La cartella madre puo' chiamarsi in qualunque modo:
`EcosistemaAI-*`, nome azienda, nome proprietario, progetto interno, reparto,
cartella AI, casa AI, workspace, Studio, Investimenti o altro. Non promuovere o
scartare una cartella solo per il nome: riconoscila dai segnali di vita.

Fai un censimento in sola lettura delle candidate. Non limitarti al nome
atteso e non cercare solo la repo tecnica esatta: cerca anche nomi umani,
brandizzati, abbreviati o scritti male.

- cartella aperta ora dall'agente;
- home utente e, se leggibili, altri profili utente della stessa macchina;
- Desktop, Documenti, Downloads, OneDrive, Google Drive, iCloud Drive o cartelle
  aziendali sincronizzate;
- nomi tipo `EcosistemaAI-*`, nome azienda/proprietario, cartella AI, casa AI,
  workspace, reparto o progetto;
- varianti e typo legati a LeaderAI: `LeaderAI`, `Leader AI`, `leaderai`,
  `leader ai`, `leder ai`, `leader-ai`, `leader_ai`;
- parole tecniche o miste: `cervello`, `ecosistema`, `_ecosistema_setup`,
  `_leaderai`, `_leaderai_install` (legacy), `install`, `setup`, `standard`, `repo`, `clone`,
  `leaderai-cervello-ecosistema`;
- cartelle con `AGENTS.md`, `CLAUDE.md`, `memory/MEMORY.md`, `ecosistema/`,
  `logs/`, `REPORT_FINALE.md` o `.git`.

Su Windows, se puoi usare PowerShell, una ricerca minima accettabile e':

```powershell
$roots = @($env:USERPROFILE, "$env:USERPROFILE\Documents", "$env:USERPROFILE\Desktop", "$env:USERPROFILE\Downloads", "$env:USERPROFILE\OneDrive") | Where-Object { Test-Path $_ }
$rx = '(?i)(leader\s*ai|leaderai|leder\s*ai|leader[-_]ai|cervello|ecosistema|_leaderai|install|setup|repo|clone)'
Get-ChildItem -Path $roots -Directory -Recurse -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -match $rx } |
  Select-Object -ExpandProperty FullName
```

Se PowerShell non e' disponibile, fai comunque una ricerca equivalente con gli
strumenti del sistema. Se non fai questa ricerca, non puoi scrivere "nessuna cartella sospetta".

Segnali di vita da pesare piu' del nome:

- `memory/MEMORY.md compilata`, non solo file vuoto o template;
- `logs/ con attivita'` o resoconti gia' scritti;
- `REPORT_FINALE.md compilato`;
- `ecosistema/ASSET.md`, `FONTI.md`, `PROCESSI.md` o `LIMITI.md` con contenuto
  del proprietario;
- `commit git` oltre al primo commit tecnico;
- file di lavoro recenti, output, procedure, bozze o documenti davvero usati;
- connettori provati con un dato reale letto, non solo dichiarati.

Per ogni candidata scrivi una riga:

```text
[path] - VIVA / VUOTA / TECNICA-REPO / SBAGLIATA / SOSPETTA - prova osservata
```

Regole:

- `VIVA` = contiene segnali di vita: memoria compilata, log, istruzioni cucite,
  file di lavoro, commit, asset/fonti/processi, connettori provati o prove di
  uso reale.
- `VUOTA` = contiene solo scheletro o pochi file generati senza contenuto del
  proprietario.
- `TECNICA-REPO` = e' il clone tecnico della repo standard, non la cartella
  madre da diagnosticare; dovrebbe vivere solo in una cartella temporanea di
  sistema (`%TEMP%\ecosistema-ai-standard` o `/tmp/ecosistema-ai-standard`) oppure
  puo' comparire col vecchio nome legacy `_leaderai_install/leaderai-cervello-ecosistema`.
  Se non contiene dati cliente e non serve piu' per il lavoro corrente, proponi
  o fai la pulizia richiesta dalla missione: sul PC cliente non devono restare
  cartelle tecniche LeaderAI visibili come lavoro.
- `SOSPETTA` = nome o contenuto richiama LeaderAI/Cervello/Ecosistema ma non e'
  chiaro se sia cartella viva, repo tecnica, copia installatore o doppione. Non
  ignorarla: apri al massimo l'albero a 2 livelli, verifica se contiene `.git`,
  file standard o dati cliente, e spiega cosa c'entra.
- Se trovi piu' cartelle, scegli quella `VIVA` con la prova piu' forte e
  diagnosticane quella.
- Se trovi una cartella Ecosistema vuota e un'altra cartella viva, NON usare la
  vuota: segnala che probabilmente e' stata creata per errore e lavora sulla
  viva.
- Se non riesci a distinguere due cartelle vive, chiedi una sola scelta umana:
  "quale di queste due devo diagnosticare?". Non creare una terza cartella.
- Usa `INSTALLA_CON_AI.md` solo se, dopo il censimento, non esiste nessun
  ambiente installato o Sal/LeaderAI chiede esplicitamente un rimontaggio.

## Passo 1 — Contratto tecnico: telaio comune e rami attivi

Il Cervello ha un telaio comune indipendente dall'agente usato oggi:

- `AGENTS.md` esiste sempre alla radice ed e' la fonte unica delle istruzioni;
- `CLAUDE.md` esiste sempre alla radice ed e' il ponte verso `AGENTS.md`;
- il ponte conforme e Windows-safe e' un file regolare di una riga:
  `@AGENTS.md`; i symlink legacy vanno convertiti;
- il ponte/import e' l'unico collegamento conforme tra i due file;
- Una copia indipendente non e' conforme: duplicare `AGENTS.md` dentro
  `CLAUDE.md` crea drift;

Le configurazioni specifiche restano separate e si controllano solo per gli
agenti realmente attivi:

| Modalita' rilevata | Aggancio minimo obbligatorio | Configurazione tecnica da verificare |
|---|---|---|
| Codex | `AGENTS.md` + `.codex/README.md` | `.codex/config.toml` se esiste o se servono impostazioni di progetto |
| Claude Code | `CLAUDE.md` + `.claude/README.md` | `.claude/settings.json` e `.claude/settings.local.json` se esistono o se servono impostazioni di progetto |
| Entrambi | entrambi gli agganci | entrambi i rami, senza duplicare le istruzioni comuni |

La modalita' `both` vale solo se risultano entrambi realmente attivi oppure se
LeaderAI l'ha richiesta esplicitamente. Il checkup non crea la configurazione
dell'altro agente per prudenza.

### Fonti ufficiali verificate nel checkup

Le docs cambiano: apri oggi le fonti del ramo attivo, registra URL e data nel
report e non rispondere a memoria.

Fonti comuni minime:

- Claude Code, `CLAUDE.md`, import `@AGENTS.md` e comportamento su Windows:
  <https://code.claude.com/docs/en/memory>
- OpenAI Codex, caricamento gerarchico di `AGENTS.md`:
  <https://developers.openai.com/codex/guides/agents-md>

Se e' attivo **Codex**, apri inoltre:

- configurazione di base e `.codex/config.toml`:
  <https://developers.openai.com/codex/config-basic>
- riferimento di configurazione:
  <https://developers.openai.com/codex/config-reference>
- hook, solo se presenti:
  <https://developers.openai.com/codex/hooks>

Se e' attivo **Claude Code**, apri inoltre:

- indice ufficiale per agenti: <https://code.claude.com/docs/llms.txt>
- directory `.claude/`: <https://code.claude.com/docs/en/claude-directory>
- settings: <https://code.claude.com/docs/en/settings>
- permessi: <https://code.claude.com/docs/en/permissions>
- hook, skill, subagent e MCP solo se presenti nell'ambiente.

## Passo 1-bis — Diagnosi e riparazione del Cervello

Confronta l'ambiente con `MANIFEST.md`, i template e le pagine ufficiali appena
aperte. Controlla e ripara nello stesso turno dove puoi.

### A. Telaio comune — sempre

1. **Cartella di lavoro stabile** — fuori da `Downloads`, `Desktop`, cartelle
   temporanee o cartelle tecniche dell'agente.
2. **Mappa comune** — `AGENTS.md` esiste alla radice, e' leggibile e indica
   dove stanno memoria, log, Ecosistema e report.
3. **Ponte Claude universale** — `CLAUDE.md` esiste alla radice come file
   regolare e contiene esattamente `@AGENTS.md` seguito da una nuova riga.
   Converti i symlink legacy; una copia indipendente non e' conforme.
4. **Chat di gruppo** — `AGENT_CHAT.md` e' presente nella cartella madre
   (template `templates/AGENT_CHAT.md`). Se manca, creala dal template. Le note
   oltre 48 ore vanno promosse nei file proprietari e tolte dalla chat.
5. **Memoria** — `memory/MEMORY.md` esiste ed e' un indice snello; niente
   duplicati inventati come `MEMORIA.md` o diari paralleli.
6. **Segreti** — `.gitignore` copre `.env`, `.secrets/`, token, chiavi,
   password e credenziali prima di qualunque commit.

### B. Ramo Codex — solo se Codex e' attivo

1. Verifica `.codex/README.md`: deve dichiarare che Codex usa `AGENTS.md` come
   istruzione comune e non deve duplicarne il contenuto.
2. Se esiste `.codex/config.toml`, validane sintassi, percorsi e impostazioni;
   le configurazioni di progetto vengono caricate solo in un progetto trusted.
3. Se servono impostazioni Codex di progetto e `.codex/config.toml` manca,
   crealo con il minimo necessario e senza segreti.
4. Hook, skill, MCP e agenti specializzati sono opzionali. Se presenti,
   confrontali con la documentazione ufficiale, prova il caso reale e rimuovi
   dal verdetto ogni presunzione non verificata.

### C. Ramo Claude Code — solo se Claude Code e' attivo

1. Verifica `.claude/README.md`: deve dichiarare che Claude Code entra dal
   ponte `CLAUDE.md` e non deve duplicare `AGENTS.md`.
2. Se esiste `.claude/settings.json`, validane struttura, scope e permessi.
   `settings.local.json` resta locale e fuori da Git; nessun segreto in chiaro.
3. Se servono impostazioni Claude di progetto e `.claude/settings.json` manca,
   crealo con il minimo necessario e senza segreti.
4. Rule, hook, skill, subagent e MCP sono opzionali. Se presenti, verifica
   sintassi e comportamento contro le pagine ufficiali vive; se devono
   bloccare un'azione, prova davvero il blocco.

### D. Prove comuni

1. **Connettori/MCP** — elenca le fonti collegate e prova una lettura innocua
   con un dato reale. Se manca la fonte, scrivi `DA COLLEGARE`.
2. **Loop di verifica** — esegui almeno un controllo ripetibile che provi
   mappa, ponte e aggancio dell'agente attivo.
3. **Pezzi inventati o doppioni** — segnala file o cartelle che duplicano
   funzioni ufficiali. Elimina solo cio' che hai creato tu; per i file del
   proprietario serve conferma.

## Gate di conformita' — verdetto bloccante

Il verdetto e' obbligatoriamente `NON PASSA` se, dopo le riparazioni:

- manca `AGENTS.md`;
- manca `CLAUDE.md` oppure il ponte non risolve a `AGENTS.md`;
- manca `AGENT_CHAT.md`;
- la modalita' attiva non e' stata rilevata e dichiarata;
- manca `.codex/README.md` quando Codex e' attivo;
- manca `.claude/README.md` quando Claude Code e' attivo;
- in modalita' `both` manca uno dei due agganci;
- una configurazione necessaria all'agente attivo e' assente, non valida o
  contiene segreti.
- una prova di processo o di fonte e' circolare, inventata durante il checkup
  oppure creata soltanto per far passare il checkup;
- una fonte operativa e' dichiarata attiva usando l'email della missione o del
  checkup invece della fonte usata nel lavoro quotidiano.

`PASSA CON ATTENZIONE` e `PASSA` sono ammessi solo dopo aver superato questo
gate. Un ramo inattivo puo' restare assente e va riportato come `NON ATTIVO`,
mai come errore.

## Passo 1-ter — Censimento e rete delle stanze

Il checkup non verifica solo file tecnici. Costruisce la mappa del sistema reale.

1. Censisci gli elementi rilevanti e classificali come `STANZA`, `FONTE`,
   `OUTPUT`, `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`.
2. Una stanza e' una funzione operativa stabile con fonti, processi o output
   propri. Una skill, uno script, un agente, un connettore, un modulo o una
   procedura e' una capacita' della stanza che lo usa.
3. Verifica che ogni stanza sia raggiungibile dall'`AGENTS.md` della cartella
   madre e abbia una mappa locale corta con scopo, fonti, output, capacita',
   collegamenti a monte e collegamenti a valle. Ogni vera stanza mantiene il
   telaio comune: `AGENTS.md` locale e ponte `CLAUDE.md` verso quella mappa.
4. Verifica che ogni collegamento corrisponda a un processo reale, che nessuna
   capacita' sia isolata e che due stanze non rispondano alla stessa funzione.
5. Ripara e prova i difetti meccanici: ponti, link, puntatori e registri rotti.
   Per fusioni, spostamenti, eliminazioni, nuove stanze o cambi di proprieta'
   scrivi una `PROPOSTA STRUTTURALE` con causa, impatto e collaudo; decide il
   proprietario.

## Passo 2 — Ecosistema (solo se il Passo 1 passa)

Dai soli file dell'ambiente, in una sessione nuova, sapresti: chi e' il
proprietario e come lavora; dove stanno i dati dei lavori ricorrenti; cosa
NON toccare/inviare senza chiedere; quali fonti rispondono davvero (prova
innocua in sola lettura su ognuna)? Scegli 2 richieste realistiche per la sua
attivita' e verifica se le eseguiresti senza fargli ripetere tutto. Dove ti
blocchi, li' c'e' il buco.

Per ciascuna prova registra il percorso effettivo:

`richiesta -> stanza -> fonte -> capacita'/processo -> output`.

Le due prove partono dalla radice senza suggerire all'agente la cartella o la
skill. Se l'instradamento fallisce, correggi mappa o collegamenti e riprova.

## Passo 2-bis — Gate anti-collaudo circolare

Una prova reale deve esistere prima del checkup ed essere indipendente dalla
missione che lo avvia.

Non contano come prova operativa:

- l'email della missione, del checkup o del report usata per dimostrare che la
  casella di lavoro del cliente e' collegata;
- una richiesta inventata dall'agente durante il checkup e poi presentata come
  richiesta reale del cliente;
- un file o un output creato soltanto per far passare il checkup;
- una prova eseguita su account, cartella, fonte o agente diversi da quelli
  usati nel lavoro quotidiano.

Per ogni prova registra la provenienza: cosa esisteva prima del checkup, fonte o
account reale, data o contesto osservabile e motivo per cui appartiene al
processo quotidiano. Se una richiesta o una fonte indipendente non e'
disponibile, scrivi `DA COLLAUDARE`: il processo operativo e il gate
anti-circolare sono `NON PASSA`. Un test sintetico puo' dimostrare accesso
tecnico minimo, mai il funzionamento reale dell'Ecosistema.

## Output (dopo le riparazioni, non prima)

```text
CHECKUP LEADERAI — [data]
Doc ufficiale letta: [pagine aperte oggi]
STANDARD APPLICATO: repo salChiarenza/leaderai-cervello-ecosistema;
MANIFEST.md; templates/AGENTS.md; docs ufficiali vive per la parte tecnica.
VERSIONE METODO: installata [x] -> verificata oggi [y].
Verdetto: PASSA / PASSA CON ATTENZIONE / NON PASSA

SCOSTAMENTI DALLO STANDARD:
- [area] trovato nella cartella viva -> standard richiesto -> azione fatta /
  blocco umano vero.

Cartella stabile        OK / RIPARATO / DA FARE (umano) - ...
Telaio AGENTS+CLAUDE    OK / RIPARATO / NON PASSA - prova del ponte...
Modalita' attiva        CODEX / CLAUDE / BOTH - prova rilevata...
Ramo Codex              OK / RIPARATO / NON ATTIVO / NON PASSA - ...
Ramo Claude Code        OK / RIPARATO / NON ATTIVO / NON PASSA - ...
Settings e permessi     OK / RIPARATO / NON ATTIVO / NON PASSA - ...
Chat di gruppo          OK / RIPARATO / DA FARE - AGENT_CHAT.md presente e disciplinata
Memoria                 OK / RIPARATO / DA FARE - ...
Skill/subagent/hook     OK / RIPARATO / DA FARE / NON NECESSARI - ...
Connettori/MCP          OK / RIPARATO / DA COLLEGARE - ...
Loop di verifica        OK / RIPARATO / DA FARE - ...
Pezzi inventati/doppi   OK / RIPARATO / PROPOSTA - ...
Classificazione         OK / RIPARATO / DA CHIARIRE - ...
Mappa stanze            OK / RIPARATO / PROPOSTA STRUTTURALE - ...
Collegamenti monte/valle OK / RIPARATO / PROPOSTA - ...
Capacita' isolate       OK / RIPARATO / PROPOSTA - ...
Prove di instradamento  OK / RIPARATO / NON PASSA - ...
GATE ANTI-CIRCOLARE     PASSA / NON PASSA - ...

PROVENIENZA PROVE:
- prova [1]: esisteva prima del checkup [SI/NO] - fonte/account - data/contesto.
- prova [2]: esisteva prima del checkup [SI/NO] - fonte/account - data/contesto.

RIPARATO OGGI: per ogni voce — cosa era rotto → cosa ho fatto → prova.
RESTA ALL'UMANO: solo permessi/accessi/scelte, col gesto preciso richiesto.
LEZIONE CANDIDATA: nessuna oppure caso -> causa -> regola generale -> prova che
avrebbe intercettato l'errore.
```

Se l'ambiente e' quasi vuoto, non dare una pagella piena di rossi: proponi di
partire dall'installazione (`INSTALLA_CON_AI.md`).

## Protocollo missione chiusa

Una missione LeaderAI non finisce quando mandi il primo report. Finisce solo
quando arriva la risposta di verifica da LeaderAI oppure quando LeaderAI dice
esplicitamente di chiudere.

Stati della missione:

1. `MISSIONE` - leggi l'email con oggetto concreto, apri il link o file indicato e segui lo
   schema indicato. Se la missione punta a `CHECKUP.md`, questo file e' lo
   schema da seguire.
2. `ESECUZIONE` - fai le azioni richieste: diagnosi, correzione, riparazione,
   prove. Non chiedere "cosa faccio?" se puoi agire.
3. `AUTOCONTROLLO` - prima di scrivere a Sal, attiva un autocontrollo interno:
   rileggi la missione, confronta cosa chiedeva con cosa hai fatto, verifica
   prove, file modificati, cartella usata, errori rimasti, punti che richiedono
   umano vero e superfici aperte da te (email, browser, tab, form, preview, app
   temporanee).
4. `REPORT` - completa il report locale della missione con azioni fatte, prove,
   cosa hai riparato, cosa resta solo per umano vero e stato di chiusura ambiente.
   Mostralo al proprietario e chiedi autorizzazione esplicita.
   Nessuna email parte automaticamente: l'invio e' un gesto separato, eseguito
   solo dopo un "manda" o autorizzazione equivalente riferita a quel testo.
5. `SAL_VERIFICA` - dopo l'invio resta in attesa della risposta LeaderAI; la
   email lavorata è già archiviata e lo stato resta nei log/report. Se l'invio
   non e' ancora autorizzato, lo stato e' `PRONTO DA INVIARE`, non
   `SAL_VERIFICA`.
6. `CONTINUA` - se LeaderAI risponde con nuove azioni o correzioni, lavori
   ancora sulla stessa missione, fai un nuovo autocontrollo, aggiorni il report
   locale e lo lasci `PRONTO DA INVIARE`. Mostralo al proprietario e chiedi una
   nuova autorizzazione prima di ogni nuovo invio.
7. `CHIUDI` - se LeaderAI conferma che va bene o dice di chiudere, chiudi
   pagine/app aperte da te e annota la chiusura nei log.

Questo autocontrollo e' temporaneo e legato alla missione. Non creare un
automatismo permanente tra agenti: ogni giro parte da una missione umana o da
una risposta esplicita di LeaderAI.

Regola breve: Non chiudere la missione dopo il primo report.

## Chiusura (ciclo resoconti)

1. Completa il resoconto locale solo a lavoro finito, mostralo al proprietario
   e chiedi l'autorizzazione esplicita all'invio. L'invio non e' parte
   automatica del checkup: dopo il si' esplicito, invialo davvero a
   `sal@salchiarenza.ai` nello stesso thread; se serve una nuova email usa
   l'oggetto concreto `Resoconto checkup Ecosistema`.
2. Dopo l'invio archivia la missione: Inbox
   pulita, stato e storia restano nei file.
3. Chiudi l'ambiente operativo usato per la missione: pagine web, tab browser,
   form, preview, login e app temporanee aperte da te. Non chiudere pagine
   personali del proprietario o superfici che deve decidere lui: dichiarale come
   handoff nel report.
