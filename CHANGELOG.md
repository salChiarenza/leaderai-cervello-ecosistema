# Changelog

## 0.6.8 - 03/09/2026

- Ordine dell'aggiornamento nel checkup: prima i file gestiti dallo standard
  (guardiano di chiusura e variante Windows, ruoli di Ecosystem Check, skill
  dell'Ispettore), sostituiti con le copie della release e riprovati; poi i
  registri e i calchi nuovi. Un guardiano della versione precedente non conosce
  i file resi obbligatori dalla versione nuova e li blocca (caso reale
  03/09/2026: anagrafe dei soggetti con il guardiano 0.6.6). Regola in
  `CHECKUP.md` Passo 0 e nella skill dell'Ispettore, con test.


## 0.6.7 - 03/09/2026

- Istruzioni globali dell'agente attivo (caso reale Pastore, 03/09/2026: casa
  installata, ma Claude Code aperto da un'altra cartella non sapeva che la casa
  esistesse). Lo standard ora scrive il blocco marcato `LEADERAI-CASA` nelle
  istruzioni lette in ogni sessione: `~/.claude/CLAUDE.md` per Claude Code
  (calco `templates/CLAUDE_USER.md`), `~/.codex/AGENTS.md` o
  `AGENTS.override.md` per Codex (calco `templates/CODEX_USER_AGENTS.md`).
  Il blocco si aggiunge o si aggiorna senza toccare il resto del file. Nuovi
  effetti esterni `claude_user_instructions` e `codex_user_instructions`, nuovo
  controllo ambiente `user_instructions_gate` (prova da cartella estranea ->
  `FUORI DAL CERVELLO`). `leaderai_setup.py` li applica solo con un percorso
  letto sulla macchina (`--claude-user-instructions`,
  `--codex-user-instructions`); senza, non tocca la home. L'Ispettore emette
  `USER_INSTRUCTIONS_MISSING` e `USER_INSTRUCTIONS_WITHOUT_HOUSE` (bloccanti) e
  `USER_INSTRUCTIONS_WITHOUT_GATE` (attenzione); accetta il percorso della casa
  in forma assoluta, `~/`, `$HOME/` o `%USERPROFILE%\`.
- Fonti ufficiali obbligatorie in ogni checkup: la pagina memory di Claude Code
  (scope dei `CLAUDE.md`) e la pagina `AGENTS.md` di Codex (caricamento
  gerarchico, override, tetto di byte).
- Anagrafe dei soggetti giuridici: nuovo calco `templates/SOGGETTI.md` ->
  `ecosistema/SOGGETTI.md`, obbligatorio nell'armadio comune (contratto,
  guardiano, harness). Regola "piu' soggetti, una casa": stanze per funzione,
  sottocartelle per soggetto solo dove la legge o il lavoro lo impongono,
  stanza per soggetto solo con processi propri. Caso reale: sei enti dichiarati
  dopo una proposta costruita su tre attivita'.
- Percorso guidato LeaderAI: finche' `logs/install-log.md` non registra
  `PERCORSO GUIDATO CHIUSO`, creare, fondere, spostare o eliminare stanze si
  decide nella sessione con il consulente (`DA DECIDERE IN CALL`), anche se il
  proprietario approva a voce. Riga aggiunta in `ecosistema/LIMITI.md`.
- Ispettore come ultimo passo obbligatorio dell'installazione, in una nuova
  sessione nata dalla cartella madre: la sessione che monta la casa non chiude
  l'installazione.
- Criterio della conferma finale reso esplicito ovunque: parte soltanto con
  verdetto `PASSA` pieno; con `PASSA CON ATTENZIONE` resta nella casa e, se
  serve un gesto umano, il solo messaggio ammesso e' `SERVE UN TUO PASSAGGIO`.
  Caso reale: rapporto di nove sezioni partito con collaudo incompleto.
- Lezione candidata promossa: su Windows i comandi di testo POSIX (sed, awk)
  perdono i backslash dei percorsi `%USERPROFILE%\...`; dopo ogni scrittura
  automatica dei registri si verifica con una ricerca e si registra la prova.
- Risolto un avviso di sintassi nell'Ispettore (sequenza di escape in una
  stringa) che sarebbe diventato errore nelle prossime versioni di Python.


## 0.6.6 - 02/09/2026

- Contratto di stanza "consolidato": una casa nata prima dello standard, con
  statuti di reparto propri e provati (caso reale: la casa madre LeaderAI, tre
  prove di instradamento su tre), dichiara `- Contratto di stanza: consolidato`
  nella mappa madre e, sotto, `Chat di gruppo`, `Guardiano di chiusura` e
  `Registro di dettaglio canonico`. Restano obbligatori ponte, mappa leggibile e
  riga completa nella mappa madre; il calco a 14 sezioni, la sezione Dentro, la
  profondita' massima e la fonte business per stanza valgono per il contratto
  completo delle case nuove. Il guardiano di chiusura applica lo stesso
  contratto e accetta i registri canonici.
- Nuovi finding `CONSOLIDATED_CHAT_MISSING`, `CONSOLIDATED_GUARDIAN_MISSING`,
  `CONSOLIDATED_GUARDIAN_NOT_HOOKED`; test dedicati per Ispettore e guardiano.
- Casa del prodotto: Ecosistema Base su Google Drive (cartella madre "LeaderAI
  Ecosystem", accanto a "Ecosistema di Sal"); la repo resta backup tecnico e
  numerazione delle versioni. La release viene ricostruita dal Drive file per
  file (`leaderai-ecosistema/tools/ecosistema_base_drive.py` nella casa LeaderAI).


## 0.6.5 - 02/09/2026

- Precisione dei rilevatori sul banco LeaderAI: immagini, note Markdown,
  documenti e media non sono piu' candidati "configurazione credenziali"
  (una schermata `credential-cards` o una nota sul cambio password non
  contengono segreti). Gli asset di firma, timbro e sigillo sono soltanto le
  immagini o i certificati sorgente: un contratto gia' firmato e' un output, uno
  script o una nota che parlano di firma non sono l'asset.
- Gli asset ad alto rischio possono essere registrati anche nel registro di
  dettaglio canonico dichiarato dalla mappa madre (casa consolidata), non solo
  in `ecosistema/ASSET.md`.


## 0.6.4 - 02/09/2026

- Il guardiano di chiusura (`guardiano_stanze.sh`) ripete a ogni `Stop` il
  controllo dei percorsi invisibili al proprietario (macOS `chflags hidden`,
  Windows attributo Hidden): caso reale LeaderAI 01/09/2026, tre cartelle
  nascoste "per una scena video" e mai fatte ricomparire. L'Ispettore le vedeva
  (0.6.2), il guardiano no. Test dedicato su macOS.
- `ecosistema_inspector.py` esclude dal censimento dei file gli ambienti tecnici
  (`.venv`, `node_modules`, `site-packages`, cache, cartelle con `pyvenv.cfg`,
  `.playwright-cli`): sul banco LeaderAI producevano oltre 1.600 finding di
  business, credenziali, asset e Markdown che non erano contenuto del
  proprietario. Le dotdir di editor e strumenti (`.obsidian`, `.vscode`, ...)
  non richiedono una classe; ogni altra dotdir alla radice resta da classificare.
- Casa consolidata: la mappa madre puo' dichiarare
  `- Registro di dettaglio canonico: \`percorso.md\`` e usare un registro proprio al
  posto di `ecosistema/ASSET.md` e `ecosistema/FONTI.md`, senza creare doppioni.
  Una cartella dal nome generico dichiarata e registrata dalla madre resta una
  segnalazione, non un blocco, e non deve avere la mappa di una stanza.
- `.mcp.json` (configurazione MCP di progetto di Claude Code) e' un file di
  radice ammesso.


## 0.6.3 - 01/09/2026

- L'Ispettore ora protegge le fusioni della memoria: il file consolidato
  dichiara nel frontmatter `replaces:` gli stem superati e il controllo blocca
  ogni wikilink interno ancora rivolto a una di quelle voci. Una memoria fusa
  senza contratto `replaces:` non passa il collaudo.
- Il Passo 2-ter richiede anche la prova diretta degli inneschi ereditati dal
  richiamo attivo della casa: avere un `trigger:` sintatticamente valido non
  dimostra che le parole operative rimangano raggiungibili.

## 0.6.2 - 01/09/2026

- Nuovo controllo del censimento: nessun percorso della casa, dotfile esclusi,
  puo' portare un flag di invisibilita' (macOS `chflags hidden`, Windows
  attributo `Hidden`). Il caso reale sul banco LeaderAI: `memory/`, `docs/` e
  `console/` invisibili nel Finder — per il proprietario "mai esistite" mentre
  l'agente le usava ogni giorno. Il censimento ora confronta cio' che vede
  l'agente con cio' che vede il proprietario; il flag si toglie nello stesso
  turno.
- `ecosistema_inspector.py`: finding bloccante `HIDDEN_FROM_OWNER` con test
  dedicati (flag su cartella di radice; i dotfile restano esclusi).

## 0.6.1 - 29/08/2026

- Corretta una regola tecnica superata sul ramo Claude Code: `autoMemoryDirectory`
  e' letta da ogni scope di settings (user, project, local, policy, `--settings`),
  non solo dalle user settings. Nelle settings di progetto o locali il valore vale
  dopo il trust del workspace. Lo standard LeaderAI resta le user settings, ma ora
  per la ragione giusta: la memoria segue la macchina, non la copia della repo.
- Nuovo controllo C.7 del ramo Claude Code: la chiave di permesso nel posto
  sbagliato. Una chiave inventata o annidata sotto il blocco sbagliato viene
  scartata in silenzio e lascia il proprietario convinto di aver autorizzato
  qualcosa. Il controllo nomina il caso trovato sul banco di collaudo LeaderAI:
  `autoMode` sta al primo livello del file, non dentro `permissions`, e il
  classificatore lo legge solo da `~/.claude/settings.json`, dalle managed
  settings e da `--settings`.
- Aggiunte alle fonti Claude Code del Passo 1 la pagina di riferimento delle
  chiavi settings e quella di configurazione di auto mode.

## 0.6.0 - 28/08/2026

- Nasce `Ecosystem Check`, prima stanza standard installata in ogni casa
  accanto a `ecosistema/`: mappa, stato, standard di reparto, registro dei
  controlli e sei ruoli separati per assegnazione, controllo, intervento e
  verifica finale.
- Il prefabbricato ora distingue la stanza comune di controllo dalle stanze
  business adattive del cliente. Una casa puo' avere zero stanze business, ma
  non resta senza il reparto che verifica struttura, istruzioni e continuita'.
- Il registro conserva un riepilogo per ciclo; il controllo iniziale precede
  l'eventuale attivazione della cadenza settimanale.
- L'Ispettore distingue capacita', autorizzazione e perimetro predefinito:
  un primo tentativo fallito non diventa piu' automaticamente un limite o un
  lavoro manuale scaricato sulla persona.
- Ogni `non posso` deve indicare percorso provato, data e prova osservabile;
  prima l'agente controlla le capacita' vive, diagnostica e riprova. I verdetti
  smentiti da una prova successiva vengono marcati `SUPERATO` e corretti nella
  fonte proprietaria.
- LeaderAI diventa il banco di collaudo reale dell'Ispettore: la fonte resta
  questa repo, i test automatici girano qui e la prova d'uso avviene nella casa
  `/Users/sal/leaderai`; le lezioni tornano nel prodotto prima del rilascio.
- Aggiunto il controllo focalizzato sulle istruzioni: puo' essere usato anche
  in una casa che non adotta il telaio cliente, senza imporre stanze, registri
  o verdetto di conformita' complessivo.

## 0.5.8 - 27/08/2026

- Il contratto delle stanze non dipende piu' soltanto dall'Ispettore avviato a
  richiesta: un project hook `Stop` controlla automaticamente ogni chiusura di
  Codex e Claude Code.
- Il guardiano blocca materiali business dentro `ecosistema/`, elementi
  sciolti senza proprietario, stanze senza mappa o ponte, copie `_v2`/`_finale`,
  cartelle vuote e router oltre 350 righe o 24 KiB. Il secondo passaggio non
  crea un ciclo infinito.
- Una mappa presente soltanto di nome non basta: registri, celle obbligatorie,
  sezioni compilate, fonte operativa, fonte business e sottocartelle dichiarate
  devono coincidere con percorsi reali. Testo di esempio, prefissi simili e
  istruzioni del calco non possono produrre un verde falso.
- Il ramo Codex include anche il comando Windows; Claude usa Git Bash su
  Windows come previsto dalla documentazione ufficiale. Le configurazioni JSON
  vengono unite senza cancellare chiavi o hook del cliente e senza duplicare
  il guardiano.
- Setup, Ispettore e collaudo manuale verificano contenuto degli script, una
  sola registrazione `Stop`, variante Windows e prove reali pulita/bloccante.
  Un JSON cliente non valido viene preservato e produce un blocco esplicito
  prima di qualsiasi altra scrittura; un hook cliente dal nome simile resta
  intatto.
- Le specifiche ufficiali degli hook Codex e Claude Code sono entrate nelle
  fonti vive del contratto. Il template della mappa madre e' stato alleggerito
  da 350 a 325 righe per lasciare spazio al lavoro reale senza superare da solo
  il proprio limite.

## 0.5.7 - 27/08/2026

- `ecosistema/` diventa un armadio comune riservato: contiene soltanto i
  registri e i calchi dichiarati dal contratto. Piani, bozze, asset e cartelle
  operative al suo interno bloccano il collaudo.
- Ogni vera stanza nasce come prefabbricato atomico: mappa `AGENTS.md`, ponte
  `CLAUDE.md`, fonte operativa nominata e compilata, riga nella mappa madre e
  prova. Il nuovo `STANZA_FONTE.md` porta in testa stato, prossimo passo,
  decisioni e scadenze.
- La policy macchina `inspection_policies -> room_lifecycle` governa classi,
  file, sezioni, organigramma e profondita' del controllo. L'Ispettore blocca
  campi incompleti, fonti assenti/vuote/illeggibili, sottocartelle fantasma,
  generiche, vuote, non dichiarate o collegate fuori casa e classi inventate.
- Il metro di controllo non puo' essere indebolito dal contratto: classi,
  registri, calchi, sezioni, termini, profondita' e nomi sono canonici. Anche
  due destinazioni che differiscono soltanto per maiuscole vengono fermate,
  per evitare collisioni silenziose su Windows.
- La riga madre e la mappa locale devono coincidere in tutti i dieci campi;
  una seconda fonte operativa, un elemento madre assente dal registro di
  dettaglio, una frase che nega il ruolo dichiarato o un file portante non
  leggibile producono un blocco esplicito, mai un verde falso o un crash.
- Il caso anonimo di uno studio cliente, con materiale marketing collocato
  dentro `ecosistema/`, e' diventato una regressione deterministica. La stessa
  legge e' scritta in Manifest, installazione, checkup, skill e mappe dei due
  agenti.

## 0.5.6 - 21/08/2026

- Il checkup guadagna il Passo 1-quinquies "Come si lavora davvero qui dentro":
  dalle tracce gia' presenti sulla macchina (registro sessioni, cronologia dei
  file toccati, `logs/`, diario dei file progetto, `AGENT_CHAT.md`, `MEMORY.md`
  e storia Git) l'agente ricostruisce quali strumenti entrano davvero nelle
  giornate di lavoro, con quale frequenza e su quali lavori. La sezione dichiara
  quali tracce ha letto, da quale macchina arrivano e quale periodo coprono.
- L'etichetta e' legata al periodo: uno strumento provato e funzionante che
  resta assente dalle tracce del periodo osservato si riporta come `NON USATO
  NEL PERIODO OSSERVATO`, non come un mancato uso definitivo. Entra nel rapporto
  con la sua prova, vive accanto all'elenco bloccante del gate e lascia il
  verdetto deciso dalle sole condizioni tecniche.
- Un episodio conta uno: le tracce dello stesso episodio (Git, chat, diario)
  vengono deduplicate per identita' di episodio, non per solo testo del gesto.
  Due episodi distinti contano due anche con lo stesso gesto e nello stesso
  giorno; lo stesso gesto ripetuto in giorni diversi conta una volta per giorno.
  Regola deterministica `adoption_rule.py -> classify_adoption`, con verdetti e
  tracce ammesse in `install_contract.json -> inspection_policies ->
  adoption_observation`, fonte macchina obbligatoria: contratto mancante, JSON
  non valido o policy incompleta fanno fallire la regola in modo visibile, senza
  default locali. Le tracce ammesse coprono tutte quelle del Passo 1-quinquies
  (sessioni, cronologia file, `logs/`, diario, chat, `MEMORY.md`, Git) con
  vocabolario canonico nel contratto. La validazione richiede ora l'intero set
  canonico: una policy che dichiara solo una parte delle tracce (es. il solo
  Git) viene fermata con l'elenco delle mancanti, misurando la completezza sul
  glossario del contratto stesso, senza una seconda lista divergente. Fixture di
  prova per: stesso episodio in piu' sorgenti (uno), stesso gesto in due episodi
  distinti (due), stesso gesto in due giorni (due), sorgenti sessioni/log/file
  ammesse, tracce assenti, copertura parziale, contratto
  mancante/malformato/incompleto, sorgenti parziali non canoniche.
- Osservazione parziale: le tracce vivono sulla macchina dell'agente mentre la
  casa puo' stare su Drive/OneDrive condivisa fra piu' PC. Se la casa e'
  condivisa e le tracce arrivano da una sola postazione, l'esito e'
  `OSSERVAZIONE PARZIALE - UNA POSTAZIONE`; `TRACCE ASSENTI` resta al caso in cui
  il registro manchi davvero. Con tracce insufficienti non si giudica l'uso.
- Il gesto manuale chiede una prova esplicita: la sola presenza di un file e' un
  indizio, la prova e' il gesto (messaggio scritto a mano, file creato a mano,
  riga di diario) con data.
- L'Output separa `VERDETTO CONFORMITA'` (com'e' fatta la casa) da `ADOZIONE
  OSSERVATA` (come si lavora davvero): uno non decide l'altro. Il rapporto porta
  le righe `Uso reale quotidiano`, `Non usato nel periodo` e `Lavori ancora a
  mano`, piu' il blocco `COME SI LAVORA QUI DENTRO` con tracce, macchina e
  periodo coperto.
- Confine di prodotto scritto dentro il passo: il checkup dice cosa si usa; la
  misura della spesa e del consumo appartiene al prodotto `Il Consigliere`
  (repo `salChiarenza/il-consigliere`).

## 0.5.5 - 06/08/2026

- Le comunicazioni visibili a Sal e al cliente usano ora un riepilogo in
  parole comuni: `Cosa funziona`, `Cosa completiamo`, `Cosa serve da te` e
  `Quando si chiude`.
- Le classificazioni tecniche restano nelle fonti della casa e non compaiono
  nelle email. Quando serve davvero un gesto umano, il messaggio apre con
  `SERVE UN TUO PASSAGGIO`, indica il solo gesto richiesto e promette la
  ripresa immediata della stessa missione.
- Il contratto di consegna rifiuta email che espongono a Sal o al cliente le
  etichette tecniche `NON PASSA` e `BLOCCO REALE`.

## 0.5.4 - 06/08/2026

- Le missioni cliente continuano nella stessa casa fino a completamento e
  prova di tutti i criteri, compreso il processo reale e la continuita' dopo la
  riapertura.
- Gli stati intermedi restano locali. Quando Sal richiede una conferma finale,
  parte una volta sola, soltanto con esito `PASSA`, e apre con `Perfetto, l'ho
  fatto. Tutto completato e funzionante.`.
- Scritta la legge dell'unico `BLOCCO REALE`: una domanda unica soltanto dopo
  tentativi sicuri falliti; ricevuta la risposta, l'agente riprende la stessa
  missione. Vietati avanzamenti e istruzioni a puntate.
- Rimossi dal contratto operativo i cicli di rapporti intermedi,
  `SAL_VERIFICA`, `CONTINUA` e `CHIUDI`.
- Il setup e il collaudo non creano piu' `REPORT_FINALE.md`: stato e prove
  vengono salvati direttamente nelle fonti proprietarie. L'Ispettore riconosce
  il vecchio file come residuo da migrare e spostare nel Cestino.
- Il ciclo produce zero aggiornamenti intermedi; quando la missione richiede
  una conferma finale, ne parte una sola dopo il collaudo completo.

## Non pubblicato - 05/08/2026

- Il Passo 2-ter guadagna una lettura veloce prima della prova comportamentale:
  sei segnali letti sul file (ordine stretto al posto del criterio, ovvieta',
  procedura lunga dentro il file sempre letto, doppione tra livelli, memoria
  scritta a mano, peso misurato) filtrano i blocchi prima di spendere due
  sessioni ciascuno. La lettura produce segnalazioni; le rimozioni restano
  legate alla prova e all'approvazione del proprietario.
- Il metro ufficiale del Passo 2-ter entra tra le fonti comuni: articolo
  Anthropic "The new rules of context engineering for Claude 5 generation
  models" (24/07/2026) per il ramo Claude Code, pagina `agents-md` di OpenAI
  per il ramo Codex, con il tetto `project_doc_max_bytes` a 32 KiB citato come
  misura.
- Aggiornati i quattro indirizzi della documentazione Codex citati nel
  checkup: `developers.openai.com/codex/...` rimanda oggi a
  `learn.chatgpt.com`. Verificato il 05/08/2026 su tutti e quattro; il
  redirect risponde, quindi il checkup non falliva, e ora i link puntano
  diretti alla casa attuale.

## Non pubblicato - 02/08/2026

- "Chi apre chiude" ed "email lavorata = email archiviata" salgono nelle Regole
  base delle istruzioni installate al cliente: prima vivevano solo nel capitolo
  delle missioni LeaderAI, quindi l'agente del cliente le applicava alle
  missioni e le ignorava nel lavoro quotidiano (caso reale rilevato il
  04/08/2026 sull'installazione di Massimiliano Caporali). La chiusura
  ambiente in `PROCESSI.md` vale ora per ogni lavoro e precisa che si chiude
  solo cio' che ha aperto l'agente.

- Il ciclo ordinario di una missione ora si chiude nella casa del cliente:
  esecuzione, prova, salvataggio nelle fonti proprietarie e chiusura ambiente.
- L'email della missione e' l'unico messaggio: zero report di ritorno;
  decisioni e gesti umani restano come `DA DECIDERE IN CALL`.

- Ogni consegna richiede ora `AI_ACT_CHECK_OK` per il sistema e l'uso concreti:
  ruolo, persone coinvolte, rischio, trasparenza, data, esito e presidio.
- Pratiche vietate, alto rischio e dubbi sostanziali bloccano la consegna; il
  controllo di un sistema non viene riusato automaticamente per un altro.

- L'Ispettore confronta un blocco di istruzioni alla volta tra contesto attuale
  e alleggerito, in due sessioni pulite e su copie temporanee.
- Le prove ricevono soltanto il compito aziendale: nessun indizio su cartella,
  fonte, procedura o risultato atteso puo' mascherare l'effetto del contesto.
- Il rapporto misura esito, fonti, instradamento, completamento, richieste
  umane, tempo, consumo quando disponibile e sicurezza; errori tecnici restano
  `DA COLLAUDARE`.
- Un solo caso non puo' candidare una rimozione. Sicurezza, privacy,
  autorizzazione e integrita' non vengono eliminate automaticamente.
- I casi di prova e i riferimenti storici pubblici sono anonimizzati.

## 0.5.3 - 31/07/2026

- La pagina iniziale della repo espone i riferimenti ufficiali per Claude Code,
  ChatGPT e Codex per il lavoro.
- Le stesse guide entrano in `ecosistema/FONTI.md`, quindi restano disponibili
  anche nella casa installata del cliente.
- `install_contract.json` le rende parte del metro macchina: l'Ispettore deve
  aprirle, confrontare regola e stato reale, riparare e mostrare la prova.
- Il comando `lancia l'Ispettore` avvia il checkup senza una seconda domanda.
- Il Cervello e' ora verificato come organigramma: Boss dell'Ecosistema alla
  radice e un Amministratore di settore per ogni ramo organizzativo, nuovo o
  preesistente. L'Ispettore blocca mappe prive della catena verso il Boss.
- L'Ispettore misura tutti i Markdown: mappe e indici oltre le soglie macchina
  bloccano il verdetto; i documenti estesi vengono controllati per fonti
  duplicate o responsabilita' mescolate e poi alleggeriti senza perdere dati.
- Ogni problema ripetibile porta nel report causa, riparazione, prova e lezione
  candidata, cosi' puo' diventare regola e test dei checkup successivi.
- I test impediscono a una versione futura di consegnare il pacchetto senza i
  collegamenti o senza il contratto di confronto.

## 0.5.2 - 30/07/2026

- Ogni email operativa agente-agente apre con `STATO PER LE PERSONE`: fatto,
  manca, prossimo passo e intervento umano, in parole semplici.
- Il formato vale in entrambe le direzioni: missione LeaderAI al cliente e
  rapporto dell'agente del cliente verso LeaderAI.
- `REPORT_FINALE.md`, modello di consegna, checkup e processi installati portano
  lo stesso riepilogo prima dei dettagli tecnici.

## 0.5.1 - 29/07/2026

- Corretto il gate Windows: i finti agenti Python vengono avviati tramite il
  runtime Python invece di essere trattati come eseguibili Win32.
- I test della memoria Claude ora rispettano la stessa regola del prodotto:
  quando la memoria vive sotto la home, `autoMemoryDirectory` usa la forma
  portabile `~/...` anche su Windows.
- La regressione sul repository Git mancante non tenta piu' di cancellare
  oggetti Git protetti in sola lettura su Windows; sposta la cartella `.git`
  fuori dal target e verifica lo stesso blocco dell'Ispettore.

## 0.5.0 - 29/07/2026

- L'ingresso nel Cervello e' ora un gate: ogni nuova task/sessione nasce dalla
  cartella madre come progetto primario/CWD, dichiara il percorso e mostra tre
  regole lette da `AGENTS.md`. Una task aperta altrove resta
  `FUORI DAL CERVELLO`.
- Aggiunta la prova esatta `Crea la Brand Identity` senza percorsi, file,
  stanze, fonti o output suggeriti. Il gate osserva instradamento autonomo,
  fonte brand reale e output nella responsabilita' proprietaria.
- La chat di gruppo porta ID missione, agente proprietario, base Git, prove e
  prossimo agente; in modalita' `both` il collaudo richiede il passaggio
  Codex -> Claude Code -> Codex su tre sessioni distinte.
- L'email operativa distingue `INSTALLA` e `CONTINUA`, usa link di release
  immutabili e verifica mittente, thread e autorizzazione del proprietario.
- `INSTALLA_CON_AI.md` espone un nucleo deterministico delimitato: il gate
  manuale prova il telaio senza consumare l'intera procedura di
  personalizzazione, che resta nello stesso file ufficiale.
- Aggiunto `install_contract.json`, fonte macchina unica per installazione
  manuale, setup tecnico, Ispettore e collaudo.
- Il setup Claude configura davvero `autoMemoryDirectory` nelle user settings,
  preserva le altre chiavi e blocca una seconda casa gia' configurata invece di
  sovrascriverla.
- Il verdetto del setup deriva dall'Ispettore: versione vecchia, memoria non
  collegata, ramo agente incoerente o baseline Git assente non possono piu'
  produrre `PASSA`.
- I cambi Codex/Claude sono espliciti: `both` mantiene i due rami;
  `--migrate-agent` rimuove soltanto file standard riconosciuti e si ferma
  davanti a contenuti del cliente.
- Aggiunto il gate deterministico `python3 -m tests.gate --quick`: zero test,
  test saltati, errori o fallimenti bloccano il rilascio.
- Aggiunti due harness con prove conservate. Il primo avvia agenti reali su una
  casa anonima e verifica instradamento, fonte corretta, output e isolamento tra
  stanze. Il secondo ripete l'installazione manuale dalla sola procedura, senza
  clone, Python o setup tecnico.
- Il gate completo `python3 -m tests.gate --release --agents codex,claude`
  richiede entrambi gli agenti reali e tratta CLI assente, login mancante,
  timeout o oracolo fallito come blocchi.
- Aggiunta CI deterministica su macOS e Windows con percorsi contenenti spazi,
  accenti e apostrofi; il live resta su runner autenticato dedicato.

## 0.4.5 - 29/07/2026

- **MUST percorsi d'ambiente in forma portabile.** `autoMemoryDirectory` si
  scrive nella forma `~/`, non piu' come percorso assoluto: una sola stringa
  vale su tutte le postazioni del cliente e si risolve sull'utente del computer
  corrente. La 0.4.3 prescriveva il percorso assoluto locale.
- Nuova sezione del Manifest: percorsi, nomi utente, lettere di disco e valori
  d'ambiente destinati a un'altra macchina si scrivono in forma portabile
  oppure si leggono dalla fonte di quella macchina. Vietato riproporre altrove
  un percorso letto su un computer diverso.
- L'Ispettore segnala `CLAUDE_MEMORY_NOT_PORTABLE` quando `autoMemoryDirectory`
  usa un percorso assoluto dentro la home dell'utente corrente. E' un avviso,
  non un blocco: il verdetto diventa `PASSA CON ATTENZIONE`.
- Due regressioni coprono il caso: percorso assoluto sotto la home segnalato,
  forma `~/` pulita.
- Origine anonimizzata: ambiente con due postazioni e nomi utente diversi. Il
  percorso assoluto replicato sul portatile avrebbe rotto la memoria senza
  alcun errore visibile.

## 0.4.4 - 28/07/2026

- L'email operativa dichiara un solo lettore reale. Il modello corrente usa
  `AGENTE_CON_POSTA`: l'agente collegato alla casella del cliente riceve la
  missione direttamente dalla prima riga.
- Il proprietario compare nei soli gesti umani che l'agente gli presenta al
  momento corretto; il report viene mostrato localmente e parte dopo il suo
  comando `manda`.
- Aggiunta una regressione che blocca il passaggio circolare `apri Claude e
  digli di leggere questa email`.

## 0.4.3 - 28/07/2026

- Una casa semplice puo' avere zero stanze: capacita', fonti e output possono
  essere posseduti direttamente dalla cartella madre e registrati nella mappa
  radice, senza creare `AGENTS.md` e `CLAUDE.md` locali inutili.
- Aggiunto il registro degli elementi posseduti dalla madre e il relativo
  controllo deterministico. La regressione prova che `Portafoglio Modello`
  passa come `CAPACITA` della madre senza essere promosso a stanza.
- Corretto lo scope Claude Code: `autoMemoryDirectory` vive nelle user settings
  di ogni computer (`~/.claude/settings.json`), con percorso assoluto locale e
  prova `/memory`; le settings project/local vengono segnalate come invalide.
- La memoria canonica e' dichiarata nella mappa madre. Un ambiente esistente
  puo' conservare il proprio nome e percorso consolidato, anche su OneDrive,
  dopo riconciliazione e prova su tutte le postazioni.

## 0.4.2 - 28/07/2026

- Aggiunto il gate anti-falsa-stanza: una cartella e' `STANZA` solo quando
  possiede una responsabilita' business riconosciuta, mantiene stato e
  decisioni e governa lavoro corrente.
- Script, skill, modelli, fonti e output possono formare una pipeline completa
  senza creare una stanza; in caso ambiguo la classe resta `CAPACITA` o
  `SOSPETTA` e il verdetto e' `NON PASSA`.
- Aggiunta la regressione `Portafoglio Modello`: il nome di un prodotto o di
  una lavorazione non dimostra una funzione aziendale autonoma.
- Il contratto locale e l'Ispettore richiedono ora una sezione esplicita
  `Responsabilita business`; il preflight blocca placeholder e dichiarazioni
  non risolte.
- Gli esempi del modulo Portafogli usano una stanza business neutra e non
  insegnano piu' a trattare `Portafoglio Modello` come stanza.

## 0.4.1 - 28/07/2026

- Il modulo Portafogli include il gate unico `VERIFICA_FINANZIARIA.md`, attivo
  su numeri finanziari, fondi, ETF, titoli, ISIN e richieste sullo stato di uno
  strumento.
- La skill distingue identita' e stato corrente del prodotto dalla sua
  collocabilita' nel catalogo autorizzato.
- Ogni numero materiale porta fonte, data/ora, valuta, periodo, formula e
  ricalcolo; ogni strumento porta identificativo, classe, valuta e stato tra
  attivo, chiuso, sospeso, incorporato, rinominato, liquidato o non verificato.
- Il secondo controllo cerca anche evidenze contrarie alla prima risposta; il
  consenso tra modelli resta una revisione aggiuntiva e non sostituisce la
  fonte primaria.
- Un elemento critico privo di prova produce `ESITO SOSPESO`; il report cliente
  nasce soltanto dal gate `PASSA` validato dal banker.

## 0.4.0 - 28/07/2026

- Il gate legge obbligatoriamente il `VERSION` vivo e lo confronta con la
  versione installata registrata in `AGENTS.md`: assenza o differenza =
  `NON PASSA`.
- Il `CHECKUP.md` e' ora l'Ispettore Ecosistema richiamabile con frasi naturali
  come `lancia l'Ispettore`, senza creare una seconda procedura concorrente.
- Ogni nuova cartella passa un ciclo obbligatorio: classificazione, stanza
  proprietaria, eventuale mappa locale, collegamento alla radice e prova.
- Aggiunto `templates/STANZA_AGENTS.md`, installato anche come calco locale
  `ecosistema/STANZA_AGENTS.md`: ogni vera stanza dichiara scopo, contenuto,
  fonti, output, capacita', monte, valle e dove scrivere; il ponte locale resta
  `CLAUDE.md` con il solo `@AGENTS.md`.
- L'installazione monta la skill `ispettore-ecosistema` nel percorso
  dell'agente attivo: `.claude/skills/` per Claude Code, `.agents/skills/` per
  Codex, entrambe soltanto in modalita' `both`.
- Il gate blocca cartelle visibili senza classe o proprietario, stanze senza
  mappa, cartelle generiche, vuote, doppie o tecniche, file sciolti nella home e
  instradamenti che non arrivano all'output.
- Aggiunto `ecosistema_inspector.py`, preflight deterministico e in sola
  lettura; il giudizio sui processi e le riparazioni restano all'agente guidato
  dal `CHECKUP.md`.
- Claude Code usa la stessa `memory/` della casa tramite
  `.claude/settings.local.json:autoMemoryDirectory`, fuori Git e attiva dopo
  trust; due memorie divergenti bloccano il verdetto finche' non vengono unite.
- Stato business, storia tecnica e report non sono piu' intercambiabili: stato
  e scadenze nel file proprietario, `install-log` solo per struttura,
  `REPORT_FINALE.md` temporaneo, datato, ignorato da Git ed eliminato a
  `CHIUDI`.
- I contenuti business modificabili vivono fuori dal codice; app e script
  producono derivati e falliscono visibilmente quando la fonte manca.
- L'Ispettore rileva configurazioni credenziali fuori `.secrets/` senza
  leggerle, controlla indice/history Git e richiede rotazione solo se
  l'esposizione non e' esclusa.
- Firma, timbro e sigillo sono asset ad alto rischio: file protetto fuori Git,
  soli metadati in `ASSET.md`, conferma umana per ogni uso.
- I file progetto portano in testa stato corrente, prossimo passo e scadenze;
  il diario resta sotto e ordinato dal piu' recente.
- Aggiunti test reali su una casa simulata: cartella `documenti` generica,
  stanza senza mappe, stanza conforme, funzioni duplicate, file sciolto e skill
  dell'agente mancante; aggiunta anche la regressione integrale della revisione
  operativa a sei giorni.

## 0.3.8 - 27/07/2026

- Aggiunto il gate anti-collaudo circolare: una prova operativa deve esistere
  prima del checkup ed essere indipendente dalla missione che lo avvia.
- L'email di installazione, checkup o report non puo' dimostrare il collegamento
  della casella usata nel lavoro quotidiano; una richiesta inventata durante il
  checkup non puo' dimostrare un processo reale.
- Il report registra ora la provenienza di ogni prova. Se manca una richiesta o
  una fonte preesistente, il processo resta `DA COLLAUDARE` e il gate e'
  obbligatoriamente `NON PASSA`.
- Aggiunto un test di regressione nato dal caso Sansone, nel quale una checklist
  inventata e l'email del checkup erano state accettate come prove reali.

## 0.3.7 - 27/07/2026

- Contratto universale chiuso e provato: ogni `AGENTS.md` versionato ha accanto
  un `CLAUDE.md` Windows-safe con il solo import `@AGENTS.md`, anche quando il
  cliente usa soltanto Codex. Le cartelle `.codex/` e `.claude/` restano invece
  legate agli agenti realmente attivi.
- Installatore reso conservativo sulle case gia' vive: `--force` ripara
  esclusivamente il ponte canonico, non sovrascrive i file del cliente, blocca
  target e registri attraversati da symlink, rifiuta file/directory del tipo
  sbagliato e chiude le regole `.gitignore` sensibili in fondo al file, cosi'
  una negazione precedente non puo' riaprire segreti.
- Git locale reso prevedibile: primo commit solo sulle nuove installazioni,
  nessuno staging/commit automatico nelle repo esistenti e rilanci identici
  senza nuovi log o commit. Report e log dichiarano l'esito reale anche quando
  il commit fallisce.
- Checkup riscritto con rami Codex/Claude separati, gate bloccante verificabile,
  uscita CLI non-zero sui blocchi, report aggiornabile senza verdetti obsoleti
  e autorizzazione esplicita prima di qualunque invio.
- Modulo Portafogli allineato allo stesso contratto, inclusi ponte locale,
  rilevamento reale della configurazione Claude, preflight dei tipi e
  protezione di percorsi, registri e backup da symlink. Ogni contenuto diverso
  sostituito conserva un backup univoco, anche nelle riparazioni successive.
- `EMAIL_CONSEGNA.md` e' la fonte unica dell'email operativa; la prova del
  destinatario viene registrata solo dopo la verifica della versione pubblica.

## 0.3.6 - 27/07/2026

- Il ponte `CLAUDE.md` (`@AGENTS.md`, una riga) c'e' SEMPRE nella cartella
  madre, qualunque agente sia in uso: Claude Code legge `CLAUDE.md`, Codex
  legge `AGENTS.md`. Fonti ufficiali verificate 27/07/2026:
  code.claude.com/docs/en/memory#agents-md (import consigliato, su Windows
  preferito al symlink) e learn.chatgpt.com/docs/agent-configuration/agents-md.
- `.claude/` e `.codex/` restano legate all'agente realmente in uso.
- Telaio, installatore, setup tecnico e contratto della casa allineati.

## 0.3.5 - 27/07/2026

- Il contratto degli agenti della casa (`templates/AGENTS.md`) ora nomina
  `AGENT_CHAT.md` come chat di gruppo: gli agenti sanno dove coordinarsi
  leggendo le regole della casa, senza doverlo scoprire.

## 0.3.4 - 27/07/2026

- Chat di gruppo nella casa cliente: `AGENT_CHAT.md` entra nel telaio
  (template, installazione, setup tecnico e checkup). Tutti gli agenti della
  casa si coordinano li', con regole di disciplina dentro al file.

## 0.3.3 - 27/07/2026

- L'ecosistema vive a se' nel PC: percorso standard `EcosistemaAI-[AZIENDA]`
  nel profilo utente, fuori dalle cartelle di agenti e programmi.
- Permesso di scrittura limitato alla cartella dell'agente = gesto umano:
  l'agente si fa concedere l'accesso al percorso scelto invece di ripiegare
  dentro la propria cartella (caso reale: casa creata in Documenti\Codex
  perche' la sessione scriveva solo li').

## 0.3.2 - 27/07/2026

- La cartella madre porta il nome dell'azienda e vive fuori da cartelle
  intitolate a un agente o a un programma: la casa resta valida quando cambia
  l'agente.
- L'email di consegna indica il percorso completo della cartella madre invece
  della sola scelta locale/cloud.
- L'agente rileva sulla macchina quale assistente gira davvero e lo dichiara nel
  report, invece di riceverlo scritto a distanza.

## 0.3.1 - 17/07/2026

- Il modulo Portafogli riusa anche la convenzione esistente dei casi; una
  struttura minima nuova resta una proposta da approvare.
- L'installer ripara i registri standard mancanti, registra la stanza nella
  tabella canonica della mappa madre e non crea una seconda mappa parallela.
- Puntatori Portafogli univoci vengono auto-riparati; i casi ambigui restano una
  decisione del banker.
- Installazione, checkup e modulo usano ora gli stessi stati email: report
  locale `PRONTO DA INVIARE`, invio solo dopo autorizzazione, poi
  `SAL_VERIFICA` con email archiviata.
- Il checkup accetta `CLAUDE.md` solo come ponte/import o symlink verso
  `AGENTS.md`, non come copia indipendente soggetta a drift.

## 0.3.0 - 17/07/2026

- Lo standard distingue il telaio universale dalla forma aziendale adattiva:
  prima censisce e classifica l'ambiente reale, poi collega le stanze gia' vive.
- Ogni stanza operativa deve essere raggiungibile dalla mappa madre e dichiarare
  fonti, output, capacita', collegamenti a monte e collegamenti a valle.
- Skill, script e moduli sono capacita' di una stanza; diventano una nuova stanza
  solo dopo una proposta motivata e l'approvazione del proprietario.
- Il checkup verifica ora grafo, collegamenti e prove di instradamento, oltre ai
  file tecnici e alle fonti.
- Il modulo Portafogli richiede la stanza proprietaria scelta dopo il censimento;
  non crea piu' `Costruzione Portafogli/` o una skill Claude per default.
- Ogni report registra la versione del metodo e le lezioni candidate emerse sul
  caso reale, cosi' LeaderAI puo' trasformarle in regole e test della repo.

## 0.2.0 - 16/07/2026

- Nuova installazione cliente tramite lettura della repo ufficiale e applicazione
  locale dello standard.
- Clone della repo ed esecuzione di `leaderai_setup.py` spostati nel percorso
  tecnico opzionale, attivabile solo con autorizzazione esplicita.
- Report creato e collaudato localmente prima dell'eventuale invio email.
- File statici dello standard esposti in `templates/`, cosi' l'agente del cliente
  puo' montarli senza eseguire codice scaricato.
