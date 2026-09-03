# Ispettore Ecosistema — checkup, riparazione e collaudo delle strade

Missione per l'agente del proprietario (Claude Code o Codex). Si lancia
dicendo all'agente `lancia l'Ispettore`, `esegui il checkup LeaderAI`,
`controlla l'Ecosistema`, `verifica le strade` o `cerca doppioni`. La skill
`ispettore-ecosistema` porta sempre a questo file, che resta la fonte unica
della procedura. Si puo' rifare dopo un aggiornamento, un cambiamento
strutturale, periodicamente o quando qualcosa non torna.

L'Ispettore non e' una pagella. Censisce la casa viva, classifica ogni
percorso, ripara i difetti sicuri, prova gli instradamenti e blocca la chiusura
finche' restano cartelle senza proprietario, stanze senza mappa, doppioni,
residui tecnici o percorsi che l'agente non sa seguire.

Nota per chi mantiene LeaderAI: questo `CHECKUP.md` versionato e' la fonte
unica della procedura. Nel workspace interno
`leaderai/leaderai-ecosistema/setup/AUDIT_FASE_1_CERVELLO.md` resta soltanto un
puntatore a questa versione pubblicata.

## Scelta del controllo

- **Checkup completo.** Si usa su un Cervello + Ecosistema cliente gia'
  installato o quando il proprietario chiede il controllo completo della casa.
  Applica l'intero standard e produce il verdetto complessivo.
- **CONTROLLO FOCALIZZATO - ISTRUZIONI.** Si usa quando la richiesta riguarda
  soltanto istruzioni, capacita' o passaggi manuali, anche in una casa che non
  adotta il telaio cliente. Esegue il Passo 2-ter, confronta fonti e prove vive
  e corregge soltanto le istruzioni autorizzate. Non emette il verdetto
  complessivo PASSA / PASSA CON ATTENZIONE / NON PASSA, non crea, rinomina o
  rimodella stanze e non tratta le differenze strutturali come errori.

Il controllo focalizzato dichiara sempre il proprio perimetro nell'uscita. Non
puo' essere usato per dichiarare conforme l'intera casa.

## Regola madre - standard contro caso reale

La repo GitHub `salChiarenza/leaderai-cervello-ecosistema` e' lo standard
LeaderAI. La cartella viva del cliente e' il caso reale.

Regola breve: non riparare a sentimento. `CHECKUP.md` non ripara a sentimento:

- `MANIFEST.md` e' lo standard di conformita';
- `templates/AGENTS.md` e' il comportamento atteso dell'agente nella cartella
  cliente;
- `templates/STANZA_AGENTS.md` e' il contratto locale di ogni vera stanza;
- `templates/STANZA_FONTE.md` e' il calco della sua fonte operativa nominata;
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
SITUAZIONE IN BREVE
Cosa funziona: il checkup e' pronto per essere eseguito sull'ambiente reale.
Cosa completiamo: diagnosi, riparazioni e prove finali.
Cosa serve da te: soltanto eventuali permessi, accessi o decisioni personali.
Quando si chiude: dopo il collaudo completo dell'ambiente e del processo reale.

ISTRUZIONI PER L'AGENTE
Questa missione e' per l'agente AI che lavora sull'ambiente del cliente.

Usa la repo GitHub `salChiarenza/leaderai-cervello-ecosistema`.
Se la repo e' gia' presente sul computer, aggiornala e apri `CHECKUP.md`.
Se la repo locale non e' presente, usa GitHub come riferimento di lettura per
`CHECKUP.md`, `MANIFEST.md`, `templates/AGENTS.md`,
`templates/STANZA_AGENTS.md`, `templates/STANZA_FONTE.md` e
`templates/ISPETTORE_SKILL.md`. Crea un clone
tecnico temporaneo solo dopo conferma esplicita.

Usa `MANIFEST.md` come standard di conformita'. La cartella viva del cliente e'
il caso reale: confrontala con lo standard della repo e con
`templates/AGENTS.md`, `templates/STANZA_AGENTS.md` e
`templates/STANZA_FONTE.md`.

Prima di dichiarare che non ci sono doppioni o cartelle tecniche fuori posto,
fai la ricerca estesa obbligatoria: cerca anche nomi non standard, nomi
brandizzati e typo come `LeaderAI`, `Leader AI`, `leaderai`, `leader ai`,
`leder ai`, `cervello`, `ecosistema`, `_leaderai`, `install`, `setup`, `repo`,
`clone`. Ogni risultato va classificato e spiegato.

Fai diagnosi, ripara gli scostamenti riparabili, prova quello che dichiari e
salva stato, prove, prossimo passo e scadenze nelle fonti proprietarie della
casa. Se trovi il residuo legacy `REPORT_FINALE.md`, promuovi i fatti ancora
correnti e spostalo nel Cestino nello stesso giro. Archivia l'email della
missione e chiudi localmente.
```

Sei l'agente AI sul computer del proprietario. Fai la diagnosi della
configurazione, la confronti con la documentazione UFFICIALE VIVA e **ripari
da solo quello che trovi rotto o mancante, nello stesso turno**. Regola
LeaderAI (autodiagnosi + auto-riparazione): il proprietario interviene soltanto
su login, permessi, hardware e scelte vere. La conferma finale mostra quello
che HAI GIA' sistemato, con la prova.

L'ordine obbligatorio e':
diagnosi -> riparazione -> prova -> salvataggio nella casa -> chiusura locale.
Permessi, login, hardware o scelte di business vengono registrati come
`DA DECIDERE IN CALL`, con il gesto preciso.

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

Leggi davvero `VERSION` e `CHANGELOG.md`. La versione installata si legge prima
dall'`AGENTS.md` della cartella viva e poi dal solo `logs/install-log.md`.
`REPORT_FINALE.md` e' un residuo legacy da migrare nelle fonti proprietarie e
spostare nel Cestino.
Registra il confronto `installata -> standard vivo`, applica tutte le lezioni
compatibili emerse dopo la versione installata e aggiorna `AGENTS.md` soltanto
dopo aver ripetuto i collaudi.

Ordine obbligatorio dell'aggiornamento: **prima i file gestiti dallo standard**
(guardiano di chiusura `.agent/hooks/guardiano_stanze.sh` con la variante
Windows, ruoli di `ecosystem-check/`, skill dell'Ispettore), sostituiti con le
copie della release e riprovati (casa pulita -> silenzio, file fuori posto ->
blocco); poi registri e calchi nuovi. Il guardiano della versione precedente
non conosce i file che la versione nuova rende obbligatori e li blocca: caso
reale del 03/09/2026, anagrafe dei soggetti con il guardiano 0.6.6 ancora
installato.

Se non riesci a leggere il `VERSION` corrente della repo ufficiale, se non
riesci a determinare la versione installata o se i due valori non coincidono,
il gate e' `NON PASSA`. Non si puo' certificare una 0.3.0 contro se stessa
quando lo standard vivo e' gia' successivo.

Se la repo locale non e' presente, usa GitHub come riferimento di lettura per i
file standard (`CHECKUP.md`, `install_contract.json`, `MANIFEST.md`,
`templates/AGENTS.md`, `templates/STANZA_AGENTS.md`,
`templates/STANZA_FONTE.md`, `templates/ISPETTORE_SKILL.md`, `AGENTS.md`,
`README.md`) tramite WebFetch/browser o strumento equivalente. Se non puoi
leggerli online, chiedi una sola conferma per creare un clone tecnico
temporaneo in cartella temporanea di sistema. Il checkup di un ambiente gia'
installato parte dalla cartella viva del cliente, non dalla creazione di nuove
cartelle tecniche.

## Passo 0-bis - Apri il metro di giudizio

Prima di diagnosticare la cartella viva, apri nella repo aggiornata:

- `install_contract.json`, inclusa la lista macchina `official_sources`;
- `MANIFEST.md`;
- `templates/AGENTS.md`;
- `templates/STANZA_AGENTS.md`;
- `templates/STANZA_FONTE.md`;
- `templates/SOGGETTI.md`;
- `templates/CLAUDE_USER.md` e `templates/CODEX_USER_AGENTS.md`;
- `templates/ISPETTORE_SKILL.md`;
- `AGENTS.md`;
- `README.md`.

Da questo momento il lavoro non e' "controllare un po' di file". Il lavoro e':
confrontare la cartella viva del cliente contro lo standard LeaderAI scritto in
questa repo. File obbligatori e rami dell'agente si ricavano dal contratto
macchina; le liste narrative lo spiegano e non lo sostituiscono.

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
  `logs/` o `.git`; la presenza di `REPORT_FINALE.md` segnala un residuo legacy.

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
- `logs/ con attivita'`;
- `ecosistema/ASSET.md`, `FONTI.md`, `PROCESSI.md`, `LIMITI.md` o `SOGGETTI.md`
  con contenuto del proprietario;
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
| Codex | `AGENTS.md` + `.codex/README.md` + `.agents/skills/ispettore-ecosistema/SKILL.md` | `.codex/config.toml` se esiste o se servono impostazioni di progetto; blocco `LEADERAI-CASA` in `~/.codex/AGENTS.md` (o `AGENTS.override.md`) di ogni PC |
| Claude Code | `CLAUDE.md` + `.claude/README.md` + `.claude/skills/ispettore-ecosistema/SKILL.md` | `autoMemoryDirectory` nelle user settings di ogni PC (`~/.claude/settings.json`) sulla memoria canonica della casa; blocco `LEADERAI-CASA` in `~/.claude/CLAUDE.md` di ogni PC; altre settings solo se servono |
| Entrambi | entrambi gli agganci | entrambi i rami, senza duplicare le istruzioni comuni |

La modalita' `both` vale solo se risultano entrambi realmente attivi oppure se
LeaderAI l'ha richiesta esplicitamente. Il checkup non crea la configurazione
dell'altro agente per prudenza.

### Fonti ufficiali verificate nel checkup

Le docs cambiano: apri oggi le fonti del ramo attivo, registra URL e data nel
log tecnico e usa le fonti correnti. Le tre fonti dichiarate in
`install_contract.json -> official_sources` sono obbligatorie in ogni checkup:

- Claude Code, panoramica ufficiale:
  <https://code.claude.com/docs/en/overview>
- ChatGPT, documentazione ufficiale:
  <https://learn.chatgpt.com/docs>
- OpenAI Academy, Codex per il lavoro:
  <https://openai.com/it-IT/academy/codex-for-work/>

Non sono link informativi. Usale come fonti vive di confronto:

1. apri oggi ciascuna fonte e, dagli indici ufficiali, raggiungi le pagine
   tecniche pertinenti al ramo attivo;
2. estrai soltanto regole e capacita' applicabili all'ambiente osservato;
3. registra `fonte -> regola ufficiale -> stato osservato -> scostamento ->
   riparazione -> prova`;
4. applica le riparazioni tecniche sicure e ripeti la prova;
5. usa `Codex per il lavoro` come fonte di pratica operativa: non puo'
   sostituire una specifica tecnica per decidere file, percorsi o settings.

Se una delle tre fonti non e' leggibile o il confronto non arriva a una prova,
il ramo interessato e' `NON PASSA`; non inventare il contenuto mancante.

Fonti comuni minime:

- Claude Code, `CLAUDE.md`, import `@AGENTS.md` e comportamento su Windows:
  <https://code.claude.com/docs/en/memory>
- Claude Code, auto memory, `autoMemoryDirectory`, scope e trust del workspace:
  <https://code.claude.com/docs/en/memory#storage-location>
- OpenAI Codex, caricamento gerarchico di `AGENTS.md`, override vicini al
  lavoro e tetto `project_doc_max_bytes` (32 KiB di default):
  <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- OpenAI Codex, skill condivise di progetto in `.agents/skills/`:
  <https://learn.chatgpt.com/docs/build-skills>
- Claude Code, skill di progetto in `.claude/skills/`:
  <https://code.claude.com/docs/en/slash-commands>
- Anthropic, criteri di scrittura delle istruzioni per i modelli di
  generazione 5 (metro del Passo 2-ter):
  <https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models>

Se e' attivo **Codex**, apri inoltre:

- configurazione di base e `.codex/config.toml`:
  <https://learn.chatgpt.com/docs/config-file/config-basic>
- riferimento di configurazione:
  <https://learn.chatgpt.com/docs/config-file/config-reference>
- hook, solo se presenti:
  <https://learn.chatgpt.com/docs/hooks>

Se e' attivo **Claude Code**, apri inoltre:

- indice ufficiale per agenti: <https://code.claude.com/docs/llms.txt>
- directory `.claude/`: <https://code.claude.com/docs/en/claude-directory>
- settings: <https://code.claude.com/docs/en/settings>
- permessi: <https://code.claude.com/docs/en/permissions>
- riferimento chiavi settings, per riconoscere una chiave inventata:
  <https://code.claude.com/docs/en/settings-reference>
- configurazione di auto mode e scope da cui il classificatore la legge:
  <https://code.claude.com/docs/en/auto-mode-config>
- hook, skill, subagent e MCP solo se presenti nell'ambiente.

## Passo 1-bis — Diagnosi e riparazione del Cervello

Confronta l'ambiente con `MANIFEST.md`, i template e le pagine ufficiali appena
aperte. Controlla e ripara nello stesso turno dove puoi.

### A. Telaio comune — sempre

1. **Gate di ingresso reale** — prima di leggere altri file dichiara superficie
   e ambiente (Codex Desktop/CLI o Claude Code; Windows nativo/WSL/macOS),
   progetto primario o directory corrente, percorso della cartella madre e
   istruzioni caricate. La task/sessione deve essere nuova e nata dalla
   cartella madre. Mostra tre regole lette da `AGENTS.md`; una email o un
   documento aperto altrove non costituiscono accesso al Cervello. Percorso
   diverso = `FUORI DAL CERVELLO`, nessuna scrittura e un solo gesto preciso
   per aprire la cartella madre.
1-bis. **Istruzioni globali dell'agente attivo** — Claude Code legge
   `~/.claude/CLAUDE.md` in ogni sessione, Codex legge `~/.codex/AGENTS.md`
   (o `AGENTS.override.md` se esiste) in ogni task. Su ogni computer del
   proprietario quel file porta il blocco `LEADERAI-CASA` con il percorso
   della cartella madre e il gate `FUORI DAL CERVELLO`. Se manca o non
   nomina la casa, aggiungi o aggiorna soltanto il blocco dal calco
   ufficiale (`templates/CLAUDE_USER.md`, `templates/CODEX_USER_AGENTS.md`)
   senza toccare il resto del file, poi prova da una cartella estranea: la
   risposta deve essere `FUORI DAL CERVELLO` senza scritture. Finding
   macchina: `USER_INSTRUCTIONS_MISSING`, `USER_INSTRUCTIONS_WITHOUT_HOUSE`
   (bloccanti), `USER_INSTRUCTIONS_WITHOUT_GATE` (attenzione).
1-ter. **Fase del percorso** — la mappa madre porta la riga `- Fase del percorso:
   N (nome)`: 1 Cervello, 2 Censimento, 3 Prima stanza, 4 Ispettore e consegna.
   La alza soltanto la missione LeaderAI che chiude il passo, di uno alla volta.
   Sotto il 3 nessuna stanza di lavoro: il guardiano di chiusura blocca ogni
   stanza registrata prima del passo 3 e l'Ispettore emette
   `ROOM_BEFORE_STEP_3`. Riga assente in una casa nata prima di questo standard:
   aggiungila con il passo reale, provato dai fatti (stanze vive = almeno 3).
2. **Cartella di lavoro stabile** — fuori da `Downloads`, `Desktop`, cartelle
   temporanee o cartelle tecniche dell'agente.
3. **Mappa comune** — `AGENTS.md` esiste alla radice, e' leggibile e indica
   dove stanno memoria, log ed Ecosistema.
4. **Ponte Claude universale** — `CLAUDE.md` esiste alla radice come file
   regolare e contiene esattamente `@AGENTS.md` seguito da una nuova riga.
   Converti i symlink legacy; una copia indipendente non e' conforme.
5. **Chat di gruppo** — `AGENT_CHAT.md` e' presente nella cartella madre
   (template `templates/AGENT_CHAT.md`). Se manca, creala dal template. Ogni
   nuova sessione legge tutto il log; ogni handoff dichiara ID missione,
   proprietario, stato, base Git, prove e prossimo agente. Le note oltre 48 ore
   vanno promosse nei file proprietari e tolte dalla chat.
6. **Memoria unica** — la mappa madre dichiara `Memoria canonica` e quella
   directory contiene `MEMORY.md` come indice snello; `memory/` e' il nome
   predefinito per le nuove installazioni, mentre una casa esistente puo'
   conservare un nome consolidato. Niente duplicati inventati come
   `MEMORIA.md`, diari paralleli o memoria auto dell'agente lasciata in
   un'altra directory. Due memorie divergenti bloccano il verdetto finche' non
   vengono riconciliate.
7. **Segreti** — `.gitignore` copre `.env`, `.secrets/`, token, chiavi,
   password e credenziali prima di qualunque commit.

### B. Ramo Codex — solo se Codex e' attivo

1. Verifica `.codex/README.md`: deve dichiarare che Codex usa `AGENTS.md` come
   istruzione comune e non deve duplicarne il contenuto. In Desktop la cartella
   madre e' il progetto locale primario; in CLI e' la directory scelta con
   `-C` o quella corrente. Dopo ogni correzione apri una nuova task.
2. Verifica `.agents/skills/ispettore-ecosistema/SKILL.md`: deve essere
   richiamabile e puntare alla procedura unica `CHECKUP.md`.
3. Verifica `.codex/hooks.json`: un solo handler `Stop` deve richiamare
   `guardiano_stanze`, con variante Windows. Apri `/hooks`, esamina e autorizza
   la definizione corrente; poi prova casa pulita e file temporaneo fuori
   posto, che deve impedire la chiusura. Elimina la prova subito dopo.
4. Se esiste `.codex/config.toml`, validane sintassi, percorsi e impostazioni;
   le configurazioni di progetto vengono caricate solo in un progetto trusted.
5. Se servono impostazioni Codex di progetto e `.codex/config.toml` manca,
   crealo con il minimo necessario e senza segreti.
6. Le altre skill, hook, MCP e agenti specializzati sono opzionali. Se
   presenti, confrontali con la documentazione ufficiale, prova il caso reale e
   rimuovi dal verdetto ogni presunzione non verificata.

### C. Ramo Claude Code — solo se Claude Code e' attivo

1. Verifica `.claude/README.md`: deve dichiarare che Claude Code entra dal
   ponte `CLAUDE.md` e non deve duplicare `AGENTS.md`.
2. Verifica `.claude/skills/ispettore-ecosistema/SKILL.md`: deve essere
   richiamabile e puntare alla procedura unica `CHECKUP.md`.
3. Apri `/memory` senza modificare nulla e confronta la destinazione con la
   memoria canonica dichiarata nell'`AGENTS.md`. Le user settings di ogni
   computer (`~/.claude/settings.json`) impostano `autoMemoryDirectory` sul
   percorso portabile `~/...` quando la memoria e' sotto la home di quella
   macchina. Un percorso assoluto e' valido soltanto se e' stato letto sulla
   stessa macchina e la memoria vive fuori dalla home. La chiave e' letta da
   ogni scope di settings (user, project, local, policy, `--settings`); nelle
   settings di progetto o locali il valore vale solo dopo il trust del
   workspace, come gli hook. Lo standard LeaderAI resta le user settings,
   perche' la memoria segue la macchina e non la copia della repo.
4. Se esiste una memoria auto esterna con contenuti diversi, confronta le due
   fonti, unisci le voci uniche nella `memory/` della casa, prova `/memory` e
   solo dopo cambia il percorso. Non svuotare o abbandonare la memoria esterna
   prima della prova.
5. Se esiste `.claude/settings.json`, validane struttura, scope e permessi.
   Nessun segreto in chiaro. Deve contenere un solo handler `Stop` per
   `guardiano_stanze`; `/hooks` lo mostra con origine `Project`. Prova casa
   pulita e file temporaneo fuori posto, poi elimina subito la prova.
6. Se servono impostazioni Claude di progetto e `.claude/settings.json` manca,
   crealo con il minimo necessario e senza segreti.
7. **Chiave di permesso nel posto sbagliato.** Ogni chiave dei settings va
   confrontata con la pagina ufficiale che la definisce, non con la sua forma
   plausibile: una chiave inventata o annidata sotto il blocco sbagliato viene
   scartata in silenzio e lascia il proprietario convinto di aver autorizzato
   qualcosa. Controlla in particolare `autoMode`, che sta al primo livello del
   file e non dentro `permissions`, e che il classificatore legge soltanto da
   `~/.claude/settings.json`, dalle managed settings e da `--settings`: un
   blocco `autoMode` in `.claude/settings.json` o `.claude/settings.local.json`
   non ha effetto. Ogni autorizzazione trovata in una chiave inerte si riporta
   come permesso non attivo, con la riga esatta e la fonte ufficiale, e si
   sposta solo dopo conferma del proprietario: rimetterla in funzione allarga
   davvero cio' che l'agente puo' fare da solo.
8. Le altre skill, rule, hook, subagent e MCP sono opzionali. Se presenti,
   verifica sintassi e comportamento contro le pagine ufficiali vive; se devono
   bloccare un'azione, prova davvero il blocco.

### D. Prove comuni

1. **Connettori/MCP** — elenca le fonti collegate e prova una lettura innocua
   con un dato reale. Se manca la fonte, scrivi `DA COLLEGARE`.
2. **Loop di verifica** — esegui almeno un controllo ripetibile che provi
   mappa, ponte e aggancio dell'agente attivo.
3. **Pezzi inventati o doppioni** — segnala file o cartelle che duplicano
   funzioni ufficiali. Elimina solo cio' che hai creato tu; per i file del
   proprietario serve conferma.
4. **Brand Identity senza indizi** — in una nuova task/sessione nata dalla
   cartella madre esegui la richiesta esatta `Crea la Brand Identity`.
   Il prompt non contiene percorsi, nomi file, stanze, fonti, skill o output.
   Registra il percorso autonomo `madre/stanza -> fonte brand -> output`.
5. **Continuita' `both`** — Codex lascia in `AGENT_CHAT.md` un handoff con ID
   missione; una nuova sessione Claude Code lo prende in carico e continua;
   una nuova task Codex rilegge e chiude. Una sola casa e tre sessioni
   distinte.

## Gate di conformita' — verdetto bloccante

Il verdetto e' obbligatoriamente `NON PASSA` se, dopo le riparazioni:

- `install_contract.json -> official_sources` non e' stato letto, una delle
  fonti ufficiali dichiarate non e' stata aperta oggi, oppure il log tecnico
  non collega la regola ufficiale allo stato osservato e alla prova;
- una guida operativa e' stata usata come specifica tecnica per creare o
  modificare file senza una pagina tecnica ufficiale che sostenga la modifica;
- il `VERSION` corrente della repo ufficiale non e' stato letto, la versione
  installata non e' determinabile o le due versioni non coincidono;
- manca `AGENTS.md`;
- la task/sessione non e' nata dalla cartella madre, il progetto primario/CWD
  non coincide, oppure non sono state mostrate tre regole lette da `AGENTS.md`;
- manca `CLAUDE.md` oppure il ponte non risolve a `AGENTS.md`;
- manca `AGENT_CHAT.md`;
- la modalita' attiva non e' stata rilevata e dichiarata;
- manca `.codex/README.md` quando Codex e' attivo;
- manca `.claude/README.md` quando Claude Code e' attivo;
- manca `.agents/skills/ispettore-ecosistema/SKILL.md` quando Codex e' attivo;
- manca `.claude/skills/ispettore-ecosistema/SKILL.md` quando Claude Code e'
  attivo;
- manca il guardiano comune, manca la configurazione `Stop` del ramo attivo,
  l'handler e' duplicato, non e' autorizzato/visibile in `/hooks` oppure la
  prova bloccante non continua il lavoro;
- in modalita' `both` manca uno dei due agganci;
- la prova `Crea la Brand Identity` contiene indizi tecnici, non raggiunge una
  fonte brand reale o scrive l'output fuori dalla responsabilita' proprietaria;
- in modalita' `both` il passaggio Codex -> Claude Code -> Codex non e' stato
  eseguito con un solo ID missione e sessioni nuove;
- Claude Code e' attivo ma `autoMemoryDirectory` nelle user settings non punta
  alla memoria canonica della casa, il trust non e' confermato o esistono due
  memorie divergenti non riconciliate;
- le istruzioni globali dell'agente attivo mancano o non nominano la cartella
  madre (`USER_INSTRUCTIONS_MISSING`, `USER_INSTRUCTIONS_WITHOUT_HOUSE`),
  oppure la prova da cartella estranea non risponde `FUORI DAL CERVELLO`;
- manca `ecosistema/SOGGETTI.md` oppure un soggetto giuridico nominato dal
  proprietario non ha la sua riga nell'anagrafe;
- una stanza di lavoro esiste mentre la mappa madre dichiara `Fase del
  percorso` 1 o 2 (`ROOM_BEFORE_STEP_3`);
- una configurazione necessaria all'agente attivo e' assente, non valida o
  contiene segreti.
- una prova di processo o di fonte e' circolare, inventata durante il checkup
  oppure creata soltanto per far passare il checkup;
- una fonte operativa e' dichiarata attiva usando l'email della missione o del
  checkup invece della fonte usata nel lavoro quotidiano.
- esiste una cartella visibile non classificata o senza proprietario nella
  cartella madre o in una stanza;
- `ecosistema/` contiene piani, bozze, asset, progetti o cartelle diversi dai
  registri e calchi ammessi dal contratto macchina;
- una vera stanza non e' collegata alla mappa madre, non ha `AGENTS.md` e
  `CLAUDE.md`, non ha la fonte operativa dichiarata e completa, conserva campi
  del calco non compilati oppure ha sottocartelle dirette non dichiarate;
- la mappa madre non dichiara il Boss dell'Ecosistema, oppure un ramo
  organizzativo nuovo o preesistente non ha un Amministratore di settore e una
  catena esplicita che riporta al Boss;
- una cartella e' stata dichiarata stanza soltanto perche' contiene skill,
  script, modelli, fonti o output, senza una responsabilita' business
  riconosciuta, stato operativo e decisioni proprie;
- restano cartelle generiche, vuote, concorrenti o tecniche presentate come
  lavoro vivo;
- due stanze rispondono alla stessa funzione;
- un file sciolto nella home non ha un proprietario dichiarato;
- un percorso della casa, dotfile esclusi, porta un flag di invisibilita'
  (macOS `chflags hidden`, Windows attributo `Hidden`) che nasconde al
  proprietario cio' che l'agente vede;
- una mappa o un indice Markdown (`AGENTS.md`, `MEMORY.md`, `AGENT_CHAT.md`)
  supera i limiti macchina di righe o byte senza essere stato alleggerito e
  ricondotto alle fonti proprietarie;
- `REPORT_FINALE.md` e' ancora presente invece di essere stato migrato nelle
  fonti proprietarie e spostato nel Cestino;
- un contenuto business modificabile ha due padroni, e' hardcoded nel codice o
  produce derivati senza fallire visibilmente quando la fonte manca;
- una configurazione credenziali vive fuori `.secrets/`, oppure la sua presenza
  in indice/history Git non e' stata esclusa senza aprirne il contenuto;
- firma, timbro o sigillo non sono protetti fuori Git, registrati per metadati
  in `ASSET.md` e limitati da conferma umana sul singolo uso;
- un file progetto non porta in testa stato corrente, prossimo passo e
  scadenze, oppure il diario non e' sotto e ordinato dal piu' recente;
- una delle due prove di instradamento non arriva dalla radice all'output.

`PASSA CON ATTENZIONE` e `PASSA` sono ammessi solo dopo aver superato questo
gate. Un ramo inattivo puo' restare assente e va riportato come `NON ATTIVO`,
mai come errore.

### Voce che segnala e lascia passare il verdetto

L'elenco qui sopra raccoglie le sole condizioni bloccanti. Accanto a quelle
vive una voce di segnalazione: uno strumento risultato collegato e funzionante
alle prove tecniche del Passo 1-bis, e assente da tutte le giornate di lavoro
osservate al Passo 1-quinquies, si riporta come `NON USATO NEL PERIODO
OSSERVATO`. L'etichetta e' legata alla finestra dichiarata, non a un giudizio
definitivo: fuori da quel periodo lo strumento potrebbe essere usato. E' un
fatto su come si lavora nel periodo coperto: entra nel rapporto con la sua
prova, resta fuori dall'elenco bloccante e lascia il verdetto deciso dalle sole
condizioni tecniche qui sopra.

## Passo 1-ter — Censimento e rete delle stanze

Il checkup non verifica solo file tecnici. Costruisce la mappa del sistema reale.

1. Censisci gli elementi rilevanti e classificali come `STANZA`, `FONTE`,
   `OUTPUT`, `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`.
   Parti da tutte le cartelle e dai file visibili nella home, poi apri l'albero
   a due livelli delle voci non standard. Nessun percorso resta fuori dalla
   tabella di censimento.
   Confronta cio' che vede l'agente con cio' che vede il proprietario: nessun
   percorso della casa, dotfile esclusi, deve portare un flag di invisibilita'
   (macOS `ls -lO` -> `chflags hidden`; Windows attributo `Hidden`). Una
   cartella che il proprietario non vede nel Finder/Explorer per lui non
   esiste: togli il flag nello stesso turno e registra chi o cosa lo aveva
   messo, se ricostruibile.
   Il guardiano di chiusura (`guardiano_stanze`) ripete lo stesso controllo a
   ogni `Stop`: una modifica "di scena" ordinata dal proprietario si annulla
   nello stesso turno, senza aspettare un secondo segnale.
   Tratta `ecosistema/` come armadio comune riservato: confronta ricorsivamente
   il suo contenuto con i soli percorsi ammessi da `install_contract.json`.
   Casa consolidata: una casa nata prima dello standard, con statuti di reparto
   propri e funzionanti, dichiara nella mappa madre `- Contratto di stanza:
   consolidato` e, sotto quella riga, `- Chat di gruppo: \`percorso\``,
   `- Guardiano di chiusura: \`percorso\`` (registrato come hook Stop
   dell'agente attivo) e `- Registro di dettaglio canonico: \`percorso.md\``.
   Con questo contratto restano obbligatori per ogni stanza il ponte
   `CLAUDE.md`, la mappa leggibile e la riga completa nella mappa madre (nome,
   scopo, amministratore, catena al Boss); il calco a 14 sezioni, la sezione
   Dentro, la profondita' massima e la fonte business per stanza valgono solo
   per il contratto completo delle case nuove. Visibilita', segreti, testi
   business nel codice e igiene dei router restano uguali per tutti.
   Ambienti tecnici (`.venv`, `node_modules`, `site-packages`, cache, cartelle
   con `pyvenv.cfg`, `.playwright-cli`) e le dotdir di editor o strumenti non
   sono contenuto del proprietario: restano fuori dal censimento dei file e non
   richiedono una classe. Una casa consolidata puo' dichiarare nella mappa madre
   `- Registro di dettaglio canonico: \`percorso.md\`` e usare quel registro al
   posto di `ecosistema/ASSET.md` e `ecosistema/FONTI.md`, senza creare doppioni.
1-bis. Censisci i soggetti giuridici che il proprietario governa da questa
   casa in `ecosistema/SOGGETTI.md`, una riga per soggetto, con stato
   `DA CENSIRE`, `ATTIVO`, `CONTENITORE` o `CHIUSO`. Le stanze seguono le
   funzioni del lavoro, non i soggetti: sei societa' non fanno sei case ne'
   sei stanze. Dentro una stanza il soggetto e' una sottocartella dichiarata
   solo dove la legge o il lavoro lo separano; una stanza per soggetto nasce
   soltanto se ha processi propri che nessuna stanza funzionale puo' ospitare.
   Durante un percorso guidato LeaderAI `IN CORSO` la decisione resta
   `DA DECIDERE IN CALL` nella sessione con il consulente.
2. Una stanza e' una responsabilita' business stabile riconosciuta dal
   proprietario. Mantiene stato operativo, decisioni e lavoro corrente. Una
   skill, uno script, un agente, un connettore, un modulo, un modello o una
   procedura e' una capacita' della cartella madre o della stanza che lo usa.
   Una cartella piena di fonti e output puo' essere una pipeline tecnica, non una stanza.
   Prima di scrivere `STANZA`, rispondi con prove a cinque domande:
   - quale responsabilita' business possiede;
   - quale stato e quali decisioni mantiene;
   - quale Amministratore di settore la governa e come riporta al Boss
     dell'Ecosistema;
   - quale lavoro riceve a monte e quale risultato consegna a valle;
   - se il proprietario usa davvero quel nome per la funzione, oppure e' solo
     il nome di un prodotto, progetto, modello, script o output.
   Se una risposta manca, classifica `CAPACITA` o `SOSPETTA` e assegna la
   cartella alla madre o a una stanza gia' riconosciuta. Verifica sempre la
   stanza standard `Ecosystem Check`, accanto a `ecosistema/`, con mappa, stato,
   standard, registro e ruoli. Una casa semplice puo' avere zero stanze business
   oltre a questa: l'`AGENTS.md` radice registra direttamente capacita',
   fonti e output, senza altre mappe locali. Porta una `PROPOSTA STRUTTURALE` solo
   quando emerge una responsabilita' business autonoma. Caso di regressione:
   `Portafoglio Modello` con motori, skill, fonti e documenti non e' di per se'
   una stanza; e' una capacita' posseduta dalla madre finche' la
   responsabilita' business non viene dimostrata.
3. Tratta la cartella madre come vertice dell'organigramma: l'agente che vi
   opera e' il `Boss dell'Ecosistema`, instrada il lavoro e coordina tutti gli
   Amministratori di settore. Ogni ramo organizzativo, vecchio o nuovo, e' una
   vera stanza: deve avere un Amministratore di settore esplicito e riportare al
   Boss. Una sottocartella di supporto non e' un ramo e resta subordinata al
   proprio amministratore.
4. Verifica che ogni stanza sia raggiungibile dall'`AGENTS.md` della cartella
   madre e abbia un prefabbricato completo costruito o integrato da
   `ecosistema/STANZA_AGENTS.md` (calco locale installato dalla fonte repo
   `templates/STANZA_AGENTS.md`) e `ecosistema/STANZA_FONTE.md`: mappa locale,
   ponte `CLAUDE.md`, fonte operativa nominata e completa, riga alla radice e
   prova. La mappa dichiara ogni sottocartella diretta. La fonte porta in testa
   `Stato corrente`, `Prossimo passo`, `Decisioni` e `Scadenze`; dichiara anche
   collegamenti a monte e collegamenti a valle soltanto quando sono reali.
5. Verifica che ogni collegamento corrisponda a un processo reale, che ogni
   capacita' abbia come proprietario la madre o una stanza e che due stanze non
   rispondano alla stessa funzione.
6. Ripara e prova i difetti meccanici: mappe locali, Amministratori di settore
   o collegamenti al Boss mancanti per stanze gia' riconosciute, ponti, link,
   puntatori e registri rotti. Elimina i residui
   vuoti o inutili creati dall'agente nella missione corrente. Per fusioni,
   spostamenti, eliminazioni, nuove stanze o cambi di proprieta' che toccano
   contenuti preesistenti scrivi una `PROPOSTA STRUTTURALE` con causa, impatto
   e collaudo; decide il proprietario.
7. Tratta nomi generici come `documenti`, `output`, `exports`, `varie`, `misc`,
   `temp` o `nuova cartella` come `SOSPETTA` finche' contenuti e proprietario
   non sono chiari. Una cartella generica non passa perche' contiene file.
8. Confronta le nuove cartelle col salvataggio precedente: nessun percorso
   creato nel lavoro corrente entra nel commit senza classe, proprietario e
   prova.

Tabella obbligatoria del censimento:

`percorso | classe | responsabilita business | amministratore | riporta al | mappa locale | collegamento radice | azione | prova`

Se la repo ufficiale e' gia' presente localmente e il proprietario autorizza
l'esecuzione del controllo tecnico, `ecosistema_inspector.py --target
<cartella-viva>` fornisce il preflight deterministico. Il preflight non
sostituisce il giudizio dell'agente sui processi e non cancella dati. Se la
repo non e' locale, esegui gli stessi controlli con gli strumenti file
disponibili senza creare un clone automatico.

La fonte macchina di questi blocchi e'
`install_contract.json -> inspection_policies -> room_lifecycle`.

## Passo 1-quater — Unicita', protezione e ordine operativo

Questi controlli usano le case gia' esistenti. Non creare una cartella
`istituzionali/`, un nuovo registro o un secondo stato per chiuderli.

1. **Stato e diario.** Per ogni file progetto, porta in testa stato corrente,
   prossimo passo e scadenze con data/responsabile/azione. Il diario resta
   sotto, dal piu' recente. `logs/install-log.md` registra soltanto
   installazione, aggiornamenti versione e cambi di struttura; non tutta la
   produzione business.
2. **Residuo legacy.** Se esiste `REPORT_FINALE.md`, promuovi i soli fatti
   ancora veri nelle fonti proprietarie, rimuovilo dall'indice Git se
   necessario e spostalo nel Cestino.
3. **Igiene Markdown.** Misura righe e byte di tutti i file `.md`, esclusi Git
   e case protette. Le soglie sono una sola fonte macchina in
   `install_contract.json -> inspection_policies -> markdown_hygiene`:
   `AGENTS.md`, `MEMORY.md` e `AGENT_CHAT.md` bloccano il verdetto oltre 350
   righe o 24 KiB; gli altri documenti entrano in revisione oltre 800 righe o
   80 KiB. La soglia non ordina tagli ciechi: verifica prima se il file risponde
   a una sola domanda. Se una mappa o un indice e' cresciuto troppo, promuovi i
   dettagli nelle fonti proprietarie gia' esistenti e lascia soltanto ingresso,
   indice e collegamenti. Se un documento esteso e' coerente e unico, mantienilo
   con indice leggibile; se mescola responsabilita' o duplica stato, separa il
   contenuto nelle case proprietarie senza creare copie parallele. Ripara nello
   stesso turno tutto cio' che e' sicuro e reversibile, poi ripeti la misura.
4. **Contenuto business.** Cerca testi o regole editabili duplicati tra Word,
   Markdown, database e codice. La fonte modificabile vive fuori dal codice,
   e' registrata nella stanza e viene letta dall'app; PDF e Word generati sono
   derivati. Se la fonte manca o non e' valida, l'app fallisce in modo visibile
   e non usa una copia hardcoded.
5. **Credenziali per percorso, non per contenuto.** Individua dai soli nomi e
   metadati configurazioni di posta, PEC, SMTP, OAuth, token e app password
   fuori `.secrets/`; non aprirle. Controlla `git ls-files` e la history del
   solo percorso. Se l'esposizione non puo' essere esclusa, blocca l'uso e
   proponi rotazione; altrimenti sposta la configurazione, aggiorna il puntatore
   dell'app e riprova.
6. **Asset ad alto rischio.** Firma, timbro e sigillo vivono in `.secrets/` o
   altra casa protetta fuori Git. In `ecosistema/ASSET.md` registra soltanto
   metadati, casa protetta, uso e limite; ogni applicazione o invio richiede
   conferma umana sul documento preciso.

## Passo 1-quinquies — Come si lavora davvero qui dentro

I passi precedenti misurano com'e' fatta la casa: file, mappe, stanze,
collegamenti. Questo passo misura come la casa viene usata nelle giornate di
lavoro reali. Un Cervello puo' mostrare dieci collegamenti provati e attivi
mentre il proprietario continua a fare a mano lo stesso lavoro: qui quel fatto
diventa visibile e scritto.

Lavora sulle tracce che la macchina conserva gia': registro delle sessioni
dell'agente attivo, cronologia dei file toccati nella cartella madre, `logs/`,
diario in coda ai file progetto, `AGENT_CHAT.md`, `MEMORY.md` e storia Git
della casa. Apri la sezione dichiarando quali tracce hai letto, da quale
macchina arrivano e quale periodo coprono davvero.

**Finestra e postazione.** Le tracce vivono sulla macchina dell'agente, mentre
la casa puo' stare su Drive/OneDrive/SharePoint condivisa fra piu' computer.
Dichiara sempre da quale macchina leggi. Se la casa risulta condivisa fra piu'
postazioni e le tracce arrivano da una sola, l'osservazione copre una
postazione sola: usa lo stato `OSSERVAZIONE PARZIALE - UNA POSTAZIONE` e non
concludere che uno strumento non e' usato quando potrebbe esserlo sull'altra
macchina.

**Un episodio conta uno.** Lo stesso gesto lascia spesso piu' tracce: un commit
in Git, una nota in `AGENT_CHAT.md`, una riga di diario. Prima di contare,
deduplica per identita' di episodio: lo stesso episodio presente in Git, chat e
diario vale uno, non tre. L'identita' e' l'episodio, non il testo del gesto: due
episodi distinti contano due anche con lo stesso gesto e nello stesso giorno, e
lo stesso gesto ripetuto in giorni diversi conta una volta per giorno. Le tracce
ammesse sono quelle elencate qui sopra — registro sessioni, cronologia file,
`logs/`, diario, `AGENT_CHAT.md`, `MEMORY.md`, storia Git — con vocabolario
canonico nel contratto (`dedup_sources`). La regola deterministica e'
`adoption_rule.py -> classify_adoption`, con verdetti e tracce ammesse in
`install_contract.json -> inspection_policies -> adoption_observation`, unica
fonte macchina: se il contratto manca, non e' valido o la policy e' incompleta,
la regola fallisce in modo visibile. Il rapporto la rispetta a mano.

1. **Strumenti vivi.** Elenca gli strumenti, i connettori e le capacita' che
   compaiono nelle giornate di lavoro. Per ognuno riporta la frequenza
   approssimativa osservata (ricorrente, saltuario, una volta sola), i lavori
   su cui compare e la prova: file letto, riga di log, data osservata. Conta
   gli episodi deduplicati, non le tracce.
2. **`NON USATO NEL PERIODO OSSERVATO`.** Elenca cio' che risulta installato,
   collegato o previsto dalla mappa della casa e resta assente da tutte le
   tracce del periodo osservato. Per ognuno riporta lo stato tecnico gia'
   rilevato al Passo 1-bis punto D.1, le tracce consultate, la macchina da cui
   arrivano e la prova che coprono il periodo dichiarato. L'etichetta e' legata
   a quella finestra e a quella postazione, non a un mancato uso definitivo.
3. **Lavori ancora a mano.** Elenca i lavori che il proprietario continua a
   svolgere a mano mentre la casa tiene gia' pronto e provato il collegamento
   che li coprirebbe. La sola presenza di un file non basta: e' un indizio. La
   prova richiede il gesto manuale esplicito: il messaggio scritto a mano, il
   file creato a mano al posto del connettore, la riga di diario che racconta il
   gesto, con data. Per ognuno riporta il lavoro, il collegamento disponibile e
   quella prova.

Ogni voce vive di una prova concreta e citabile. Quando le tracce locali
risultano assenti o troppo povere per rispondere, scrivi `TRACCE ASSENTI`,
indica quale traccia servirebbe (registro sessioni attivo, diario aggiornato in
testa ai file progetto, `logs/` alimentato dal lavoro quotidiano) e proponi il
gesto che inizia a raccoglierla. Con tracce insufficienti l'esito e' `TRACCE
ASSENTI`, mai un giudizio di mancato uso. Ogni numero che entra nel rapporto
nasce da una riga letta e citata.

Il perimetro di questo passo e' l'uso: quali strumenti entrano nelle giornate e
quali restano fermi. La misura della spesa e del consumo appartiene al prodotto
`Il Consigliere` (repo `salChiarenza/il-consigliere`).

## Passo 2 — Ecosistema (solo se il Passo 1 passa)

Dai soli file dell'ambiente, in una sessione nuova, sapresti: chi e' il
proprietario e come lavora; dove stanno i dati dei lavori ricorrenti; cosa
NON toccare/inviare senza chiedere; quali fonti rispondono davvero (prova
innocua in sola lettura su ognuna)? Scegli 2 richieste realistiche per la sua
attivita' e verifica se le eseguiresti senza fargli ripetere tutto. Dove ti
blocchi, li' c'e' il buco.

Per ciascuna prova registra il percorso effettivo:

`richiesta -> madre/stanza -> fonte -> capacita'/processo -> output`.

Le due prove partono dalla radice senza suggerire all'agente la cartella o la
skill. Se l'instradamento fallisce, correggi mappa o collegamenti e riprova.

## Passo 2-bis — Gate anti-collaudo circolare

Una prova reale deve esistere prima del checkup ed essere indipendente dalla
missione che lo avvia.

Non contano come prova operativa:

- l'email della missione o del checkup usata per dimostrare che la
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

## Passo 2-ter — Audit delle istruzioni che stringono troppo

Controlla anche se `AGENTS.md`, il ponte/import `CLAUDE.md`, skill, rule o hook
stanno riducendo qualita' o autonomia. Lunghezza e ripetizione sono indizi; la
prova e' il comportamento. I casi anonimi iniziali sono in
`install_contract.json -> inspection_policies -> instruction_audit`: fonte non
verificata, casa sbagliata, doppione, eccesso di regole/file, conflitto,
verifica finale mancante e dati disponibili richiesti inutilmente all'utente.

### Lettura veloce prima della prova

La prova comportamentale costa due sessioni per blocco: si spende soltanto sui
casi che restano dubbi dopo la lettura. Apri prima i criteri ufficiali del ramo
attivo (articolo Anthropic sui modelli di generazione 5 per Claude Code, pagina
`agents-md` per Codex) e passa il file cercando questi segnali:

1. **Ordine stretto al posto del criterio.** Una regola che vieta o impone una
   forma esatta dove basterebbe il criterio di scelta. Segnala `RISCRIVI` con
   la riformulazione proposta.
2. **Ovvieta'.** Istruzioni che descrivono comportamenti che il modello attivo
   tiene gia' da solo. Restano dentro le eccezioni, le trappole e le
   convenzioni proprie di quella casa. Segnala `CANDIDATA ALLA RIMOZIONE` e
   manda alla prova solo se il blocco tocca una semantica protetta.
3. **Procedura lunga nel file sempre letto.** Una sequenza di passi dentro
   `AGENTS.md` o `CLAUDE.md` va in una skill, che si carica alla chiamata
   invece di pesare a ogni messaggio. Segnala `SPOSTA NELLA PROCEDURA/SKILL
   GIUSTA` con la destinazione.
4. **Doppione tra livelli.** Stessa istruzione in file globale, file di
   progetto, skill o hook. Segnala `ACCORPA` indicando quale copia resta.
5. **Memoria scritta a mano.** Righe che duplicano cio' che l'agente salva gia'
   da solo nella sua memoria.
6. **Fusione di memorie.** Prima di archiviare le voci sorelle, il file che
   resta dichiara nel frontmatter `replaces:` con tutti gli stem sostituiti.
   Aggiorna ogni wikilink interno che li nomina e prova con prompt diretti tutti
   gli inneschi ereditati dal meccanismo di richiamo attivo della casa. Indice
   snello e `trigger:` presente non bastano: una fusione che rende irraggiungibile
   una regola o la lascia passiva e' un errore di integrita'. L'Ispettore blocca
   i rimandi rimasti agli stem dichiarati in `replaces:`.
7. **Peso misurato.** Per Codex confronta la dimensione di `AGENTS.md` con il
   tetto `project_doc_max_bytes` (32 KiB di default) e riporta il valore. Per
   Claude Code riporta l'esito di `/doctor` sul costo della configurazione.
8. **Falsa uscita manuale.** Se una istruzione dice che l'agente non puo'
   caricare, allegare, inviare, selezionare un file o usare un collegamento,
   separa **capacita', autorizzazione e perimetro predefinito**. Il primo
   tentativo fallito non dimostra che l'agente non puo' farlo. Prima di
   coinvolgere la persona controlla le capacita' e le fonti vive della casa,
   diagnostica e riprova sullo stesso percorso. Una dichiarazione negativa e'
   valida soltanto se registra percorso provato, data e prova osservabile. Se
   una prova reale successiva la smentisce, correggi la fonte proprietaria e
   marca il verdetto storico `SUPERATO` invece di lasciarlo come istruzione.

La lettura veloce produce segnalazioni, mai rimozioni. I blocchi che restano
dubbi, e tutti quelli su semantica protetta, passano alla prova sotto.

Per ogni blocco sospetto:

1. assegna ID, file, scopo, agente, rischio e semantica protetta;
2. cambia una istruzione o un gruppo coerente: contesto completo contro
   alleggerito, nessun'altra differenza e nessuna modifica alla casa viva;
3. esegui la stessa missione in due task/sessioni nuove su copie usa-e-getta e
   passa soltanto il compito aziendale, senza suggerire cartella, fonte,
   procedura o risultato atteso;
4. misura esito osservabile, fonti corrette, instradamento, completamento,
   richieste/correzioni umane, tempo, consumo quando esposto e sicurezza.
   Conserva transcript/output/diff senza correzioni nel mezzo; se il risultato
   non distingue i contesti, ripeti un secondo caso. Un solo caso non puo'
   produrre `CANDIDATA ALLA RIMOZIONE`.

Il collaudo ripetibile vive in `behavior_harness.py compare-context`: crea due
target distinti, avvia sessioni effimere e salva `full/`, `lighter/` e
`comparison.json`. I blocchi sono input temporanei locali; il consumo assente
resta `N/D`.

Classifica ogni blocco: `MANTIENI` se peggiora una metrica; `ACCORPA` se la
forma breve assorbe ripetizioni; `SPOSTA NELLA PROCEDURA/SKILL GIUSTA` se il
dettaglio serve solo all'attivazione; `RISCRIVI` se il testo crea un blocco;
`CANDIDATA ALLA RIMOZIONE` se casi sufficienti non mostrano rischi.

Sicurezza, privacy, autorizzazione e integrita' sono semantiche protette: non
si eliminano automaticamente. L'Ispettore propone diff e prova; nessuna
modifica distruttiva ai file vivi avviene senza approvazione del proprietario.

## Output (dopo le riparazioni, non prima)

```text
SITUAZIONE IN BREVE
Cosa funziona: [cosa e' stato concluso e provato]
Cosa completiamo: [lavoro che l'agente porta a termine]
Cosa serve da te: [un solo gesto richiesto oppure tutto gestito dall'agente]
Quando si chiude: [condizione concreta di chiusura]

DETTAGLI TECNICI
CHECKUP LEADERAI — [data]
Doc ufficiale letta: [pagine aperte oggi]
FONTI UFFICIALI CONFRONTATE
fonte | ruolo | regola/capacita' confrontata | stato osservato | scostamento/riparazione | prova | data
STANDARD APPLICATO: repo salChiarenza/leaderai-cervello-ecosistema;
MANIFEST.md; templates/AGENTS.md; templates/STANZA_AGENTS.md;
templates/STANZA_FONTE.md; templates/ISPETTORE_SKILL.md; docs ufficiali vive
per la parte tecnica.
VERSIONE METODO: installata [x] -> verificata oggi [y].
VERDETTO CONFORMITA': PASSA / PASSA CON ATTENZIONE / NON PASSA
  (com'e' fatta la casa: telaio, stanze, collegamenti, condizioni bloccanti)
ADOZIONE OSSERVATA: ADOZIONE OSSERVATA / OSSERVAZIONE PARZIALE - UNA POSTAZIONE
  / TRACCE ASSENTI - (come si lavora davvero: uso reale nel periodo coperto)
  I due esiti sono separati: la casa puo' passare mentre l'uso resta parziale o
  non misurabile, e viceversa. Uno non decide l'altro.

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
Memoria Claude unica    OK / RIPARATO / NON PASSA - path + prova /memory...
Istruzioni globali      OK / RIPARATO / NON PASSA - file utente, casa nominata, gate provato da fuori...
Soggetti giuridici      OK / RIPARATO / DA CENSIRE - anagrafe ecosistema/SOGGETTI.md, stanze per funzione...
Fase del percorso       OK / RIPARATO / NON PASSA - riga nella mappa madre, stanze coerenti con il passo...
Skill/subagent/hook     OK / RIPARATO / DA FARE / NON NECESSARI - ...
Audit istruzioni        OK / DA COLLAUDARE / PROPOSTA - blocco, confronto, metriche, classificazione...
Connettori/MCP          OK / RIPARATO / DA COLLEGARE - ...
Uso reale quotidiano    ADOZIONE OSSERVATA / OSSERVAZIONE PARZIALE - UNA POSTAZIONE / TRACCE ASSENTI - tracce lette, macchina, periodo coperto...
Non usato nel periodo   NESSUNO / [elenco] - segnala e lascia passare il verdetto...
Lavori ancora a mano    NESSUNO / [elenco] - lavoro, collegamento pronto, prova del gesto manuale...
Loop di verifica        OK / RIPARATO / DA FARE - ...
Pezzi inventati/doppi   OK / RIPARATO / PROPOSTA - ...
Percorsi censiti        OK / RIPARATO / NON PASSA - nessun percorso escluso...
Classificazione         OK / RIPARATO / NON PASSA - ...
Mappa stanze            OK / RIPARATO / PROPOSTA STRUTTURALE - ...
Organigramma            OK / RIPARATO / NON PASSA - Boss + amministratori + catena gerarchica...
Collegamenti monte/valle OK / RIPARATO / PROPOSTA - ...
Capacita' isolate       OK / RIPARATO / PROPOSTA - ...
Cartelle generiche/vuote OK / RIPARATO / NON PASSA - ...
File sciolti in home    OK / RIPARATO / NON PASSA - ...
Stato/memoria/log       OK / RIPARATO / NON PASSA - una domanda, una fonte...
Fonti business/codice   OK / RIPARATO / NON PASSA - fonte + derivati...
Credenziali/history     OK / RIPARATO / NON PASSA - soli percorsi/metadati...
Firma/timbro            OK / RIPARATO / NON PASSA - ASSET + casa + limite...
File progetto           OK / RIPARATO / NON PASSA - stato/prossimo/scadenze...
Igiene Markdown         OK / RIPARATO / ATTENZIONE / NON PASSA - file, righe, byte, fonte proprietaria...
Skill Ispettore         OK / RIPARATO / NON PASSA - agente attivo...
Prove di instradamento  OK / RIPARATO / NON PASSA - ...
GATE ANTI-CIRCOLARE     PASSA / NON PASSA - ...

PROVENIENZA PROVE:
- prova [1]: esisteva prima del checkup [SI/NO] - fonte/account - data/contesto.
- prova [2]: esisteva prima del checkup [SI/NO] - fonte/account - data/contesto.

COME SI LAVORA QUI DENTRO:
- tracce lette: [registro sessioni, cronologia file, logs/, diario,
  AGENT_CHAT.md, storia Git] - macchina [quale PC] - periodo coperto [dal ... al ...].
- adozione osservata: ADOZIONE OSSERVATA / OSSERVAZIONE PARZIALE - UNA
  POSTAZIONE / TRACCE ASSENTI (episodi deduplicati, stesso gesto in Git/chat/diario conta uno).
- usati davvero: strumento -> frequenza osservata -> lavoro -> prova.
- NON USATO NEL PERIODO OSSERVATO: strumento -> stato tecnico -> tracce
  consultate -> macchina -> prova che coprono il periodo. Segnala e lascia
  passare il verdetto.
- ancora a mano: lavoro -> collegamento gia' pronto -> prova del gesto manuale
  esplicito (non la sola presenza del file).
- TRACCE ASSENTI: [voce] -> traccia che servirebbe -> gesto che la avvia.

RIPARATO OGGI: per ogni voce — cosa era rotto → cosa ho fatto → prova.
RESTA ALL'UMANO: solo permessi/accessi/scelte, col gesto preciso richiesto.
LEZIONE CANDIDATA: nessuna oppure caso -> causa -> riparazione -> regola
generale -> prova che avrebbe intercettato l'errore. Ogni problema ripetibile
va restituito a LeaderAI: dopo validazione entra nella repo con regola e test e
diventa un controllo dei checkup successivi.
```

Se l'ambiente e' quasi vuoto, non dare una pagella piena di rossi: proponi di
partire dall'installazione (`INSTALLA_CON_AI.md`).

## Protocollo missione chiusa

Una missione LeaderAI finisce sulla macchina del cliente quando il lavoro
eseguibile e' completo, provato, salvato nelle fonti proprietarie e l'ambiente
e' stato chiuso. L'email della missione e' l'unico messaggio del ciclo
ordinario: zero aggiornamenti intermedi. Quando la missione richiede una
conferma finale, ne parte una sola dopo il collaudo completo.

Stati della missione:

1. `MISSIONE` - leggi l'email con oggetto concreto, apri il link o file indicato e segui lo
   schema indicato. Se la missione punta a `CHECKUP.md`, questo file e' lo
   schema da seguire.
2. `ESECUZIONE` - fai le azioni richieste: diagnosi, correzione, riparazione,
   prove. Non chiedere "cosa faccio?" se puoi agire.
3. `AUTOCONTROLLO` - attiva un autocontrollo interno:
   rileggi la missione, confronta cosa chiedeva con cosa hai fatto, verifica
   prove, file modificati, cartella usata, errori rimasti, punti che richiedono
   umano vero e superfici aperte da te (email, browser, tab, form, preview, app
   temporanee).
4. `SALVATAGGIO NELLA CASA` - aggiorna i file proprietari con stato, prove,
   prossimo passo e scadenze.
5. `CHIUSURA LOCALE` - usa
   `logs/install-log.md` soltanto se e' cambiata la struttura/installazione,
   archivia l'email della missione e chiudi pagine, tab, finestre e strumenti
   aperti da te.

`PASSA CON ATTENZIONE` contiene soltanto permessi, accessi, hardware,
decisioni o gesti realmente umani. Completa e prova ogni azione eseguibile
dall'agente prima della chiusura. Registra ogni blocco umano come
`DA DECIDERE IN CALL`, con il gesto preciso.

### Un solo passaggio umano, scritto in parole comuni

La missione deve indicare istruzioni precise, fonti, risultato atteso, azioni
autorizzate e criteri di riuscita. Esegui, diagnostica, ripara, riprova e
completa in autonomia, evitando aggiornamenti di avanzamento e richieste a
puntate. Fermati una sola volta soltanto quando serve un gesto che puo'
compiere il proprietario. Nel messaggio visibile scrivi:

```text
SERVE UN TUO PASSAGGIO
Ho gia' sistemato: [cosa e' stata completata]
Mi serve da te: [un solo dato, accesso, permesso o decisione]
Appena lo fai: riprendo e completo il lavoro.
```

Le classificazioni tecniche restano nelle fonti della casa. Ricevuta la
risposta, riprendi la stessa missione e arriva alla fine.

Quando Sal richiede espressamente una conferma finale, inviala una volta sola
quando tutti i criteri della missione sono completati e provati, compreso il
processo reale e la riapertura del contesto, cioe' soltanto con verdetto
`PASSA` pieno. Apri con
`Perfetto, l'ho fatto. Tutto completato e funzionante.` e riporta le prove
essenziali. Con `PASSA CON ATTENZIONE` la conferma non parte: se serve un
gesto del proprietario, il solo messaggio ammesso e' `SERVE UN TUO
PASSAGGIO`. Un rapporto lungo con collaudo incompleto non e' una conferma.
Gli esiti intermedi restano nella casa e alimentano la stessa missione.

## Chiusura locale

1. Promuovi stato, prove, prossimo passo e scadenze nelle fonti proprietarie.
2. Archivia l'email della missione.
3. Chiudi l'ambiente operativo usato per la missione: pagine web, tab browser,
   form, preview, login e app temporanee aperte da te. Non chiudere pagine
   personali del proprietario o superfici che deve decidere lui: dichiarale come
   `DA DECIDERE IN CALL` nella fonte proprietaria.
