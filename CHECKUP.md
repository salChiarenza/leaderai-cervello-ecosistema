# Checkup — il Cervello a confronto con i docs ufficiali

Missione per l'agente del proprietario (Claude Code o Codex). Si lancia
dicendo all'agente: "esegui il checkup LeaderAI" (questo file, `CHECKUP.md`,
nella repo gia' presente o letta come standard LeaderAI). Si puo' rifare ogni
volta che serve: dopo un aggiornamento, ogni tot settimane, o quando qualcosa
non torna.

Nota per chi mantiene LeaderAI: la sorgente del metodo e'
`leaderai/leaderai-ecosistema/setup/AUDIT_FASE_1_CERVELLO.md`. Ogni modifica
li' si specchia qui nello stesso turno.

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

Oggetto: `Missione Ecosistema LeaderAI #N - Checkup`

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

Fai diagnosi, ripara gli scostamenti riparabili, prova quello che dichiari,
fai autocontrollo e manda solo il report finale a LeaderAI.

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

## Passo 1 — Apri la doc ufficiale viva (obbligatorio, mai a memoria)

Le docs cambiano: il confronto si fa con la pagina di OGGI, non con quello che
ricordi. La documentazione Claude Code e' fatta per gli agenti:

- indice completo: <https://code.claude.com/docs/llms.txt>
- ogni pagina in markdown puro aggiungendo `.md` all'URL
  (es. `https://code.claude.com/docs/en/memory.md`)

Pagine minime da aprire per questo checkup, con cosa guardarci:

| Pagina (`/en/…` + `.md`) | Cosa controllare li' |
|---|---|
| `memory` | CLAUDE.md e auto-memory: soglie, import, symlink |
| `claude-directory` | cosa va dove dentro `.claude/` e nella root |
| `settings` | scope project/local/user, struttura settings.json |
| `permissions` | sintassi allow/ask/deny, anchor dei path, deny sui segreti |
| `skills` | formato SKILL.md, description, invocazione |
| `hooks` | struttura evento→matcher→hooks, exit code, placeholder |
| `sub-agents` | frontmatter name/description, tools, model |
| `mcp` | scope dei server, segreti via `${VAR}`, approvazioni |
| `best-practices` | potatura CLAUDE.md, loop di verifica |
| `costs` | consumo: server inutili, modelli leggeri, contesto |

Se l'agente del proprietario e' **Codex**: stesso metodo, fonti sue —
`https://developers.openai.com/codex/guides/agents-md` e
`https://developers.openai.com/codex/hooks`; le case sono `.codex/`,
`config.toml`, `AGENTS.md` e la memoria Codex.

## Passo 1 — Diagnosi e riparazione del Cervello

Confronta l'ambiente con le pagine appena lette. Controlla, e ripara dove
puoi:

1. **Cartella di lavoro stabile** — non `Downloads`, `Desktop`, cartelle
   temporanee o di conversazione. `AGENTS.md`/`CLAUDE.md` nella radice.
2. **Istruzioni** — `CLAUDE.md` esiste, e' letto, e' CORTO (indicativamente
   sotto le ~200 righe da doc): ogni riga passa il test "toglierla causerebbe
   errori?". Roba usata solo a volte → skill o rules, non nel file globale.
   Se c'e' anche `AGENTS.md`, i due devono coincidere (symlink o copia
   coerente).
3. **Settings e permessi** — `.claude/settings.json` con permessi in sintassi
   valida (regole `Tool(specifier)` come da doc `permissions`); file
   sensibili (`.env`, `.secrets/`) coperti da deny in lettura;
   `settings.local.json` fuori da git; niente segreti in chiaro da nessuna
   parte.
4. **Memoria** — auto-memory agganciata, `memory/MEMORY.md` presente e
   indice snello (le soglie di caricamento sono nella doc `memory`); niente
   file inventati che la duplicano (`MEMORIA.md`, diari paralleli).
5. **Skill, subagent, hook** — sono opzionali: se non c'e' un bisogno reale,
   la loro assenza NON e' un errore. Se esistono: ogni skill ha `SKILL.md`
   con description che dice quando usarla e corpo conciso; ogni subagent ha
   frontmatter `name`/`description` e modello leggero se fa lavori semplici;
   ogni hook usa `${CLAUDE_PROJECT_DIR}` (non path assoluti), matcher validi
   e (se deve bloccare) exit code 2.
6. **Connettori/MCP** — elenca le fonti collegate (email, calendario, Drive,
   gestionale…). Segreti solo via variabili `${VAR}`, mai in chiaro nella
   config; server configurati ma mai usati → proponi di spegnerli (consumo).
   Se una fonte manca, scrivi `DA COLLEGARE`: non inventare accessi.
7. **Loop di verifica** — esiste almeno un controllo eseguibile (test,
   script, comando) con cui l'agente puo' provare il proprio lavoro?
8. **Pezzi inventati o doppioni** — file/cartelle che duplicano funzioni
   ufficiali o si contraddicono. Doppione trovato = segnala; cancelli solo
   cio' che hai creato tu, mai file del proprietario senza ok.

## Passo 2 — Ecosistema (solo se il Passo 1 passa)

Dai soli file dell'ambiente, in una sessione nuova, sapresti: chi e' il
proprietario e come lavora; dove stanno i dati dei lavori ricorrenti; cosa
NON toccare/inviare senza chiedere; quali fonti rispondono davvero (prova
innocua in sola lettura su ognuna)? Scegli 2 richieste realistiche per la sua
attivita' e verifica se le eseguiresti senza fargli ripetere tutto. Dove ti
blocchi, li' c'e' il buco.

## Output (dopo le riparazioni, non prima)

```text
CHECKUP LEADERAI — [data]
Doc ufficiale letta: [pagine aperte oggi]
STANDARD APPLICATO: repo salChiarenza/leaderai-cervello-ecosistema;
MANIFEST.md; templates/AGENTS.md; docs ufficiali vive per la parte tecnica.
Verdetto: PASSA / PASSA CON ATTENZIONE / NON PASSA

SCOSTAMENTI DALLO STANDARD:
- [area] trovato nella cartella viva -> standard richiesto -> azione fatta /
  blocco umano vero.

Cartella stabile        OK / RIPARATO / DA FARE (umano) - ...
Istruzioni (CLAUDE.md)  OK / RIPARATO / DA FARE - ...
Settings e permessi     OK / RIPARATO / DA FARE - ...
Memoria                 OK / RIPARATO / DA FARE - ...
Skill/subagent/hook     OK / RIPARATO / DA FARE / NON NECESSARI - ...
Connettori/MCP          OK / RIPARATO / DA COLLEGARE - ...
Loop di verifica        OK / RIPARATO / DA FARE - ...
Pezzi inventati/doppi   OK / RIPARATO / PROPOSTA - ...

RIPARATO OGGI: per ogni voce — cosa era rotto → cosa ho fatto → prova.
RESTA ALL'UMANO: solo permessi/accessi/scelte, col gesto preciso richiesto.
```

Se l'ambiente e' quasi vuoto, non dare una pagella piena di rossi: proponi di
partire dall'installazione (`INSTALLA_CON_AI.md`).

## Protocollo missione chiusa

Una missione LeaderAI non finisce quando mandi il primo report. Finisce solo
quando arriva la risposta di verifica da LeaderAI oppure quando LeaderAI dice
esplicitamente di chiudere.

Stati della missione:

1. `MISSIONE` - leggi l'email numerata, apri il link o file indicato e segui lo
   schema indicato. Se la missione punta a `CHECKUP.md`, questo file e' lo
   schema da seguire.
2. `ESECUZIONE` - fai le azioni richieste: diagnosi, correzione, riparazione,
   prove. Non chiedere "cosa faccio?" se puoi agire.
3. `AUTOCONTROLLO` - prima di scrivere a Sal, attiva un autocontrollo interno:
   rileggi la missione, confronta cosa chiedeva con cosa hai fatto, verifica
   prove, file modificati, cartella usata, errori rimasti, punti che richiedono
   umano vero e superfici aperte da te (email, browser, tab, form, preview, app
   temporanee).
4. `REPORT` - archivia la email già gestita, poi invia a `sal@salchiarenza.ai`
   il report finale della missione,
   mantenendo il numero nell'oggetto o nello stesso thread. Il report contiene:
   azioni fatte, prove, cosa hai riparato, cosa resta solo per umano vero e
   stato di chiusura ambiente.
5. `SAL_VERIFICA` - dopo il report resta in attesa della risposta LeaderAI; la
   email lavorata è già archiviata e lo stato resta nei log/report.
6. `CONTINUA` - se LeaderAI risponde con nuove azioni o correzioni, lavori
   ancora sulla stessa missione, fai un nuovo autocontrollo e mandi un nuovo
   report.
7. `CHIUDI` - se LeaderAI conferma che va bene o dice di chiudere, chiudi
   pagine/app aperte da te e annota la chiusura nei log.

Questo autocontrollo e' temporaneo e legato alla missione. Non creare un
automatismo permanente tra agenti: ogni giro parte da una missione umana o da
una risposta esplicita di LeaderAI.

Regola breve: Non chiudere la missione dopo il primo report.

## Chiusura (ciclo resoconti)

1. Invia il resoconto a `sal@salchiarenza.ai` solo a lavoro finito. Rispondi
   nello stesso thread della missione numerata; se devi creare una nuova email,
   usa lo stesso numero: `Missione Ecosistema LeaderAI #N - Resoconto finale`.
2. Archivia la missione nello stesso giro in cui la leggi e la gestisci: Inbox
   pulita, stato e storia restano nei file.
3. Chiudi l'ambiente operativo usato per la missione: pagine web, tab browser,
   form, preview, login e app temporanee aperte da te. Non chiudere pagine
   personali del proprietario o superfici che deve decidere lui: dichiarale come
   handoff nel report.
