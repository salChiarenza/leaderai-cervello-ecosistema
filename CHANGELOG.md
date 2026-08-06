# Changelog

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
