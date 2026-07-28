# Changelog

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
