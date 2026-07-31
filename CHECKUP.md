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

## Regola madre - standard contro caso reale

La repo GitHub `salChiarenza/leaderai-cervello-ecosistema` e' lo standard
LeaderAI. La cartella viva del cliente e' il caso reale.

Regola breve: non riparare a sentimento. `CHECKUP.md` non ripara a sentimento:

- `MANIFEST.md` e' lo standard di conformita';
- `templates/AGENTS.md` e' il comportamento atteso dell'agente nella cartella
  cliente;
- `templates/STANZA_AGENTS.md` e' il contratto locale di ogni vera stanza;
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
STATO PER LE PERSONE
Fatto: il checkup e' pronto per essere eseguito sull'ambiente reale.
Manca: diagnosi, riparazioni e prove finali.
Prossimo passo: l'agente esegue CHECKUP.md fino al rapporto conclusivo.
Intervento umano: solo permessi, accessi o decisioni che l'agente non puo' dare.

ISTRUZIONI PER L'AGENTE
Questa missione e' per l'agente AI che lavora sull'ambiente del cliente.

Usa la repo GitHub `salChiarenza/leaderai-cervello-ecosistema`.
Se la repo e' gia' presente sul computer, aggiornala e apri `CHECKUP.md`.
Se la repo locale non e' presente, usa GitHub come riferimento di lettura per
`CHECKUP.md`, `MANIFEST.md`, `templates/AGENTS.md`,
`templates/STANZA_AGENTS.md` e `templates/ISPETTORE_SKILL.md`. Crea un clone
tecnico temporaneo solo dopo conferma esplicita.

Usa `MANIFEST.md` come standard di conformita'. La cartella viva del cliente e'
il caso reale: confrontala con lo standard della repo e con
`templates/AGENTS.md` e `templates/STANZA_AGENTS.md`.

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

Leggi davvero `VERSION` e `CHANGELOG.md`. La versione installata si legge prima
dall'`AGENTS.md` della cartella viva e poi dal solo `logs/install-log.md`;
un vecchio `REPORT_FINALE.md` puo' essere un indizio, mai la fonte corrente.
Registra il confronto `installata -> standard vivo`, applica tutte le lezioni
compatibili emerse dopo la versione installata e aggiorna `AGENTS.md` soltanto
dopo aver ripetuto i collaudi.

Se non riesci a leggere il `VERSION` corrente della repo ufficiale, se non
riesci a determinare la versione installata o se i due valori non coincidono,
il gate e' `NON PASSA`. Non si puo' certificare una 0.3.0 contro se stessa
quando lo standard vivo e' gia' successivo.

Se la repo locale non e' presente, usa GitHub come riferimento di lettura per i
file standard (`CHECKUP.md`, `install_contract.json`, `MANIFEST.md`, `templates/AGENTS.md`,
`templates/STANZA_AGENTS.md`, `templates/ISPETTORE_SKILL.md`, `AGENTS.md`,
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
| Codex | `AGENTS.md` + `.codex/README.md` + `.agents/skills/ispettore-ecosistema/SKILL.md` | `.codex/config.toml` se esiste o se servono impostazioni di progetto |
| Claude Code | `CLAUDE.md` + `.claude/README.md` + `.claude/skills/ispettore-ecosistema/SKILL.md` | `autoMemoryDirectory` nelle user settings di ogni PC (`~/.claude/settings.json`) sulla memoria canonica della casa; altre settings solo se servono |
| Entrambi | entrambi gli agganci | entrambi i rami, senza duplicare le istruzioni comuni |

La modalita' `both` vale solo se risultano entrambi realmente attivi oppure se
LeaderAI l'ha richiesta esplicitamente. Il checkup non crea la configurazione
dell'altro agente per prudenza.

### Fonti ufficiali verificate nel checkup

Le docs cambiano: apri oggi le fonti del ramo attivo, registra URL e data nel
report e non rispondere a memoria. Le tre fonti dichiarate in
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
- OpenAI Codex, caricamento gerarchico di `AGENTS.md`:
  <https://developers.openai.com/codex/guides/agents-md>
- OpenAI Codex, skill condivise di progetto in `.agents/skills/`:
  <https://learn.chatgpt.com/docs/build-skills>
- Claude Code, skill di progetto in `.claude/skills/`:
  <https://code.claude.com/docs/en/slash-commands>

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

1. **Gate di ingresso reale** — prima di leggere altri file dichiara superficie
   e ambiente (Codex Desktop/CLI o Claude Code; Windows nativo/WSL/macOS),
   progetto primario o directory corrente, percorso della cartella madre e
   istruzioni caricate. La task/sessione deve essere nuova e nata dalla
   cartella madre. Mostra tre regole lette da `AGENTS.md`; una email o un
   documento aperto altrove non costituiscono accesso al Cervello. Percorso
   diverso = `FUORI DAL CERVELLO`, nessuna scrittura e un solo gesto preciso
   per aprire la cartella madre.
2. **Cartella di lavoro stabile** — fuori da `Downloads`, `Desktop`, cartelle
   temporanee o cartelle tecniche dell'agente.
3. **Mappa comune** — `AGENTS.md` esiste alla radice, e' leggibile e indica
   dove stanno memoria, log, Ecosistema e report.
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
   password, credenziali e
   `REPORT_FINALE.md` prima di qualunque commit.

### B. Ramo Codex — solo se Codex e' attivo

1. Verifica `.codex/README.md`: deve dichiarare che Codex usa `AGENTS.md` come
   istruzione comune e non deve duplicarne il contenuto. In Desktop la cartella
   madre e' il progetto locale primario; in CLI e' la directory scelta con
   `-C` o quella corrente. Dopo ogni correzione apri una nuova task.
2. Verifica `.agents/skills/ispettore-ecosistema/SKILL.md`: deve essere
   richiamabile e puntare alla procedura unica `CHECKUP.md`.
3. Se esiste `.codex/config.toml`, validane sintassi, percorsi e impostazioni;
   le configurazioni di progetto vengono caricate solo in un progetto trusted.
4. Se servono impostazioni Codex di progetto e `.codex/config.toml` manca,
   crealo con il minimo necessario e senza segreti.
5. Le altre skill, hook, MCP e agenti specializzati sono opzionali. Se
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
   stessa macchina e la memoria vive fuori dalla home. La chiave non e'
   accettata nelle settings project/local. Il valore e' attivo solo dopo il
   trust del workspace.
4. Se esiste una memoria auto esterna con contenuti diversi, confronta le due
   fonti, unisci le voci uniche nella `memory/` della casa, prova `/memory` e
   solo dopo cambia il percorso. Non svuotare o abbandonare la memoria esterna
   prima della prova.
5. Se esiste `.claude/settings.json`, validane struttura, scope e permessi.
   Nessun segreto in chiaro.
6. Se servono impostazioni Claude di progetto e `.claude/settings.json` manca,
   crealo con il minimo necessario e senza segreti.
7. Le altre skill, rule, hook, subagent e MCP sono opzionali. Se presenti,
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

- `install_contract.json -> official_sources` non e' stato letto, una delle tre
  fonti ufficiali obbligatorie non e' stata aperta oggi, oppure il report non
  collega la regola ufficiale allo stato osservato e alla prova;
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
- in modalita' `both` manca uno dei due agganci;
- la prova `Crea la Brand Identity` contiene indizi tecnici, non raggiunge una
  fonte brand reale o scrive l'output fuori dalla responsabilita' proprietaria;
- in modalita' `both` il passaggio Codex -> Claude Code -> Codex non e' stato
  eseguito con un solo ID missione e sessioni nuove;
- Claude Code e' attivo ma `autoMemoryDirectory` nelle user settings non punta
  alla memoria canonica della casa, il trust non e' confermato o esistono due
  memorie divergenti non riconciliate;
- una configurazione necessaria all'agente attivo e' assente, non valida o
  contiene segreti.
- una prova di processo o di fonte e' circolare, inventata durante il checkup
  oppure creata soltanto per far passare il checkup;
- una fonte operativa e' dichiarata attiva usando l'email della missione o del
  checkup invece della fonte usata nel lavoro quotidiano.
- esiste una cartella visibile non classificata o senza proprietario nella
  cartella madre o in una stanza;
- una vera stanza non e' collegata alla mappa madre, non ha `AGENTS.md` e
  `CLAUDE.md`, oppure la sua mappa locale non dichiara scopo, fonti, output,
  capacita', monte, valle e dove scrivere;
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
- una mappa o un indice Markdown (`AGENTS.md`, `MEMORY.md`, `AGENT_CHAT.md`)
  supera i limiti macchina di righe o byte senza essere stato alleggerito e
  ricondotto alle fonti proprietarie;
- `REPORT_FINALE.md` e' stantio, senza data/stato, versionato in Git o usato
  come fonte corrente insieme al log;
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

## Passo 1-ter — Censimento e rete delle stanze

Il checkup non verifica solo file tecnici. Costruisce la mappa del sistema reale.

1. Censisci gli elementi rilevanti e classificali come `STANZA`, `FONTE`,
   `OUTPUT`, `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`.
   Parti da tutte le cartelle e dai file visibili nella home, poi apri l'albero
   a due livelli delle voci non standard. Nessun percorso resta fuori dalla
   tabella di censimento.
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
   cartella alla madre o a una stanza gia' riconosciuta. Una casa semplice puo'
   avere zero stanze: l'`AGENTS.md` radice registra direttamente capacita',
   fonti e output, senza mappe locali. Porta una `PROPOSTA STRUTTURALE` solo
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
   madre e abbia una mappa locale costruita o integrata da
   `ecosistema/STANZA_AGENTS.md` (calco locale installato dalla fonte repo
   `templates/STANZA_AGENTS.md`): scopo, contenuto, fonti, output, capacita',
   collegamenti a monte e collegamenti a valle e dove scrivere. Ogni vera
   stanza mantiene il telaio comune: `AGENTS.md` locale e ponte `CLAUDE.md`
   verso quella mappa.
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

## Passo 1-quater — Unicita', protezione e ordine operativo

Questi controlli usano le case gia' esistenti. Non creare una cartella
`istituzionali/`, un nuovo registro o un secondo stato per chiuderli.

1. **Stato e diario.** Per ogni file progetto, porta in testa stato corrente,
   prossimo passo e scadenze con data/responsabile/azione. Il diario resta
   sotto, dal piu' recente. `logs/install-log.md` registra soltanto
   installazione, aggiornamenti versione e cambi di struttura; non tutta la
   produzione business.
2. **Report temporaneo.** Se `REPORT_FINALE.md` fotografa una missione vecchia,
   promuovi i soli fatti ancora veri nelle fonti proprietarie, rimuovilo
   dall'indice Git se necessario e crea il report corrente con `VALIDO AL` e
   `STATO MISSIONE`. Dopo `CHIUDI` viene eliminato.
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
STATO PER LE PERSONE
Fatto: [cosa e' stato concluso e provato]
Manca: [blocco residuo oppure niente]
Prossimo passo: [una sola azione concreta e chi la esegue]
Intervento umano: [gesto richiesto oppure nessuno]

DETTAGLI TECNICI
CHECKUP LEADERAI — [data]
Doc ufficiale letta: [pagine aperte oggi]
FONTI UFFICIALI CONFRONTATE
fonte | ruolo | regola/capacita' confrontata | stato osservato | scostamento/riparazione | prova | data
STANDARD APPLICATO: repo salChiarenza/leaderai-cervello-ecosistema;
MANIFEST.md; templates/AGENTS.md; templates/STANZA_AGENTS.md;
templates/ISPETTORE_SKILL.md; docs ufficiali vive per la parte tecnica.
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
Memoria Claude unica    OK / RIPARATO / NON PASSA - path + prova /memory...
Skill/subagent/hook     OK / RIPARATO / DA FARE / NON NECESSARI - ...
Connettori/MCP          OK / RIPARATO / DA COLLEGARE - ...
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
Stato/report/log        OK / RIPARATO / NON PASSA - una domanda, una fonte...
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
4. `REPORT` - crea o sostituisci il report locale temporaneo con `VALIDO AL`,
   `STATO MISSIONE`, azioni fatte, prove, cosa hai riparato, cosa resta solo
   per umano vero e stato di chiusura ambiente.
   Il report apre con `STATO PER LE PERSONE`: `Fatto`, `Manca`,
   `Prossimo passo`, `Intervento umano`, prima dei dettagli tecnici.
   Mostralo al proprietario e chiedi autorizzazione esplicita.
   Nessuna email parte automaticamente: l'invio e' un gesto separato, eseguito
   solo dopo un "manda" o autorizzazione equivalente riferita a quel testo.
5. `SAL_VERIFICA` - dopo l'invio resta in attesa della risposta LeaderAI; la
   email lavorata è già archiviata e lo stato resta nel report temporaneo. Se l'invio
   non e' ancora autorizzato, lo stato e' `PRONTO DA INVIARE`, non
   `SAL_VERIFICA`.
6. `CONTINUA` - se LeaderAI risponde con nuove azioni o correzioni, lavori
   ancora sulla stessa missione, fai un nuovo autocontrollo, aggiorni il report
   locale e lo lasci `PRONTO DA INVIARE`. Mostralo al proprietario e chiedi una
   nuova autorizzazione prima di ogni nuovo invio.
7. `CHIUDI` - se LeaderAI conferma che va bene o dice di chiudere, promuovi i
   fatti stabili nel file proprietario della stanza, usa
   `logs/install-log.md` soltanto se e' cambiata la struttura/installazione,
   elimina `REPORT_FINALE.md` e chiudi pagine/app aperte da te.

Questo autocontrollo e' temporaneo e legato alla missione. Non creare un
automatismo permanente tra agenti: ogni giro parte da una missione umana o da
una risposta esplicita di LeaderAI.

Regola breve: Non chiudere la missione dopo il primo report.

## Chiusura (ciclo resoconti)

1. Completa il resoconto locale solo a lavoro finito, mostralo al proprietario
   e chiedi l'autorizzazione esplicita all'invio. L'invio non e' parte
   automatica del checkup: dopo il si' esplicito, invialo davvero allo stesso
   mittente LeaderAI verificato nello stesso thread; se serve una nuova email usa
   l'oggetto concreto `Resoconto checkup Ecosistema`. L'email e il report
   iniziano con `STATO PER LE PERSONE`, prima dei dettagli tecnici.
2. Dopo l'invio archivia la missione: Inbox pulita, stato business nella fonte
   proprietaria, storia tecnica nel solo install-log. Il report resta soltanto
   finche' la missione non riceve `CHIUDI`.
3. Chiudi l'ambiente operativo usato per la missione: pagine web, tab browser,
   form, preview, login e app temporanee aperte da te. Non chiudere pagine
   personali del proprietario o superfici che deve decidere lui: dichiarale come
   handoff nel report.
