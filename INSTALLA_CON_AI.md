# Autoconfigurazione sicura - Cervello + Ecosistema

Questa e' la procedura unica per una nuova installazione cliente. La repo
ufficiale resta lo standard LeaderAI verificabile; l'agente del cliente la
legge in sola lettura e applica localmente i file nella cartella madre.

Percorso predefinito: lettura della repo ufficiale, creazione locale e
collaudo. Il clone della repo e l'esecuzione di `leaderai_setup.py` sono un
percorso tecnico opzionale: si usano solo dopo una richiesta separata e una
autorizzazione esplicita del proprietario.

REGOLA PER CHI CONSEGNA (LeaderAI): l'email di consegna e' corta e punta a
questa procedura. L'installazione produce prima un report locale verificato;
l'invio del report a LeaderAI avviene poi con autorizzazione esplicita del
proprietario.

Modello email di consegna (da compilare).
Oggetto: `Installazione Cervello + Ecosistema`

  Ciao [NOME], di' al tuo agente (Claude Code o Codex) di eseguire questo:

  Apri in sola lettura la procedura ufficiale:
  https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/main/INSTALLA_CON_AI.md
  Leggi anche `VERSION`, `MANIFEST.md` e i file indicati in `templates/`, poi
  applica lo standard direttamente nella cartella madre locale con questi dati:
  cliente: [NOME] - [AZIENDA]; cartella di lavoro: [CARTELLA]; agente:
  claude (o codex).

  Scelte gia' fatte con Sal (non fare le domande guidate, usa queste):
  posizione cartella madre: [locale / cloud]; backup: [GitHub privato /
  copia su Drive / locale per ora]; seconda postazione: [si / no].

  Usa accesso web di sola lettura alla repo. Il percorso standard non richiede
  clone della repo ne' esecuzione di codice scaricato. Prima diagnostica,
  crea o integra i file mancanti, fai le prove e completa `REPORT_FINALE.md`.
  Mostrami il verdetto locale. L'invio a sal@salchiarenza.ai sara' un secondo
  gesto, dopo la mia autorizzazione esplicita.

  Sal & Claude

## Testo da copiare

```text
Voglio configurare il mio Cervello + Ecosistema LeaderAI usando la repo
ufficiale come standard di sola lettura.

Repo da usare:
https://github.com/salChiarenza/leaderai-cervello-ecosistema

Procedura da aprire:
https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/main/INSTALLA_CON_AI.md

Obiettivo finale:
creare o aggiornare UNA cartella madre (il cervello) sul mio computer. Dove
metterla la decidi con me, con le domande guidate qui sotto: la posizione
giusta dipende da come lavoro io, non da una regola fissa. Le opzioni sono disco
locale oppure cartella sincronizzata (OneDrive / Google Drive). Per ognuna ci
sono pro, contro e un avviso: me li spieghi e scelgo io.

[NOME CLIENTE]
[AZIENDA]
[CARTELLA DI LAVORO]

Modalita':
sto lavorando da Claude Code. Quindi configura la modalita' Claude:
--agent claude

Se invece questa istruzione viene incollata in Codex, cambia la modalita' in:
--agent codex

Usa --agent both solo se LeaderAI/Sal lo chiede esplicitamente.
Non creare la configurazione dell'altro agente per prudenza.

Agisci tu, senza chiedermi istruzioni tecniche. Chiedimi solo scelte umane vere
o permessi che non puoi concedere al posto mio.

Regola sulle domande guidate (Domanda 1, 2 e 3): se l'email di consegna
contiene gia' le "scelte fatte con Sal", NON rifare quelle domande: applica
le scelte e dichiarale nel report. Se una scelta manca, usa il default
sicuro senza fermarti (cartella madre su disco locale; backup = repository
git locale, quello remoto si aggiunge dopo; niente seconda postazione) e
segnala nel report che il default e' modificabile. Le domande si fanno solo
se il cliente stesso chiede di decidere.

Fase 1 - autodiagnosi
1. Dimmi sistema operativo, utente corrente, cartelle trovate, presenza di Git e agente attivo.
   Se il computer ha PIU' account utente (su Windows capita spesso: uno per
   persona o per reparto), elencali e chiedimi da quale account lavoro davvero:
   la cartella madre deve vivere nell'account che uso io, altrimenti da un altro
   profilo sembra vuota o invisibile.
2. Cerca una cartella di lavoro gia' viva, sia su disco locale sia dentro
   OneDrive / Google Drive. Se ne trovi una che sembra gia' usata per il lavoro
   (per esempio una cartella [CARTELLA DI LAVORO] o EcosistemaAI-...), proponila
   come possibile cartella madre. Non creare doppioni.
   Il nome non basta: la cartella viva puo' chiamarsi in qualunque modo
   (nome azienda, progetto, reparto, cartella AI, casa AI, workspace). Guardala
   dai segnali di vita: `memory/MEMORY.md compilata`, `logs/ con attivita'`,
   `REPORT_FINALE.md compilato`, `ecosistema/ASSET.md`, `commit git`, file di
   lavoro recenti o connettori provati. Se una cartella ha questi segnali, non
   creare una nuova cartella solo perche' il nome non e' quello atteso.
3. DOMANDA 1 - dove mettere la cartella madre (il cervello). [UMANO]
   Presentami le due opzioni con pro/contro in una riga ciascuna:
   - Disco locale: scrittura sicura, nessun rischio di corruzione; pero' sta su
     un solo computer, il backup e la seconda postazione vanno impostati a parte
     (Domanda 2 e 3).
   - Cartella sincronizzata (OneDrive / Google Drive): comoda per usarla da piu'
     PC subito; pero' c'e' un avviso serio.
   AVVISO da dire chiaro (e' un avviso, non un divieto): Claude Code, mentre
   scrive, puo' corrompere o troncare i file su cartelle cloud con file
   "on-demand" (bug noti). Se scelgo il cloud, accetto questo rischio in cambio
   della comodita'.
   Fammi scegliere. Se trovi gia' una cartella viva, dimmi dov'e' (locale o
   cloud) e chiedimi se confermarla o spostarla.
4. Crea la cartella madre solo dopo la mia scelta. Se non trovo nulla di gia'
   vivo, proponi un nome:
   - Mac/Linux: ~/EcosistemaAI-[AZIENDA]
   - Windows: %USERPROFILE%\EcosistemaAI-[AZIENDA]
   nella posizione che ho scelto alla Domanda 1.

Fase 2 - prepara la cartella madre e Git locale
1. Se Git manca ed e' installabile, installalo o guidami solo nel click/permesso
   necessario. Python non serve nel percorso standard.
2. Crea o usa la cartella madre scelta nella Fase 1. Inizializzala come repository
   git locale, senza collegarla automaticamente a repository esterne.
3. Prima di aggiungere file, controlla cosa esiste gia'. Integra i pezzi mancanti
   e conserva il contenuto vivo del cliente.

Fase 3 - leggi lo standard ufficiale in sola lettura
1. Apri dalla repo GitHub ufficiale questi file, tutti dal branch `main`:
   - `VERSION`
   - `MANIFEST.md`
   - `templates/AGENTS.md`
   - `templates/MEMORY.md`
   - `templates/ASSET.md`
   - `templates/GITIGNORE.txt`
   - `templates/CLAUDE.md`
   - `templates/CLAUDE_README.md`
   - `templates/CODEX_README.md`
   - `templates/FONTI.md`
   - `templates/PROCESSI.md`
   - `templates/LIMITI.md`
   - `templates/INSTALL_LOG.md`
2. Registra nel report la versione letta. Se un file non e' leggibile, chiedi
   soltanto l'autorizzazione per l'accesso web di sola lettura e riprova.
3. Il percorso predefinito termina qui per la repo: niente clone e niente
   esecuzione di codice scaricato.

Fase 4 - monta localmente il Cervello
1. Crea le cartelle `memory/`, `logs/` ed `ecosistema/` nella cartella madre.
2. Applica localmente i template, sostituendo `{{client_name}}`, `{{date}}` e
   `{{agent}}` con i dati reali:
   - `templates/AGENTS.md` -> `AGENTS.md`
   - `templates/MEMORY.md` -> `memory/MEMORY.md`
   - `templates/ASSET.md` -> `ecosistema/ASSET.md`
   - `templates/GITIGNORE.txt` -> `.gitignore`
   - `templates/FONTI.md` -> `ecosistema/FONTI.md`
   - `templates/PROCESSI.md` -> `ecosistema/PROCESSI.md`
   - `templates/LIMITI.md` -> `ecosistema/LIMITI.md`
   - `templates/INSTALL_LOG.md` -> `logs/install-log.md`
3. Se la modalita' e' Claude, crea `CLAUDE.md` e `.claude/README.md` dai relativi
   template. Se e' Codex, crea `.codex/README.md`. Usa entrambi solo se LeaderAI
   lo ha chiesto esplicitamente.
4. Crea `REPORT_FINALE.md` seguendo il Manifest e le sezioni richieste in fondo
   a questa procedura.
5. Non sovrascrivere file vivi: integra le sezioni mancanti e registra nel report
   cosa era gia' presente, cosa hai creato e cosa hai aggiornato.
6. Verifica che `.gitignore` escluda `.secrets/`, file `.env`, token, chiavi,
   password e credenziali prima del primo commit.

Percorso tecnico opzionale:
`leaderai_setup.py` resta un attrezzo LeaderAI per collaudi o installazioni
esplicitamente autorizzate. Se LeaderAI propone di usarlo, presenta prima al
proprietario repo, comando, file che saranno creati e permessi richiesti; procedi
solo dopo la sua autorizzazione esplicita. Questo percorso non si attiva come
ripiego automatico.

Fase 5 - personalizza il Cervello
Dopo l'installazione, apri i file creati nella cartella madre e aggiorna solo i
punti necessari, senza cancellare il resto.

In `AGENTS.md` aggiungi una sezione "Regole [NOME CLIENTE]" con le mie regole reali:
- chi sono e cosa faccio [AZIENDA];
- rispondi in italiano, chiaro e operativo;
- cosa ti chiedo di supportare (ricerca, analisi, organizzazione fonti, bozze);
- eventuali vincoli del mio settore: se il mio lavoro e' regolamentato, non
  generi l'output finale; ogni output e' una bozza che rivedo e firmo io;
- non inviare email, non cancellare file, non spostare cartelle vive e non usare
  dati sensibili senza mia conferma esplicita;
- SALVATAGGIO AUTOMATICO: alla fine di ogni sessione di lavoro fai da solo
  `git add -A` + `git commit` con un messaggio chiaro, senza che io lo chieda.
  Se il backup remoto (GitHub) e' configurato, fai anche `git push`. Io non
  devo ricordarmi di salvare: ci pensi tu, sempre;
- TUTTO NASCE NELLA CASA: ogni file, app, documento o nota che crei nasce
  dentro la cartella madre, mai sul Desktop o altrove. L'agente si apre
  sempre da questa cartella;
- NIENTE MANI DENTRO LA CASA: dentro la cartella madre non si cancella e non
  si sposta nulla a mano da Esplora file/Finder. Si chiede all'agente, cosi'
  il salvataggio git resta coerente e nulla si perde;
- RESOCONTI IN UNA STANZA SOLA: i resoconti e i report nascono in una
  sottocartella `resoconti/` (creala se manca), mai sparsi nella radice.

Mantieni anche la sezione "Comunicazione e fonti di verita'":
- gli agenti non si parlano direttamente, leggono e scrivono file condivisi;
- stato e chiusure lavoro: `REPORT_FINALE.md` o `logs/install-log.md`;
- procedure e "come si fa": file dell'area che le usa, non chat;
- asset/capacita' nuove: `ecosistema/ASSET.md`;
- coordinamento temporaneo sullo stesso file: chat solo se serve evitare
  collisioni e massimo 48 ore;
- problema di allineamento Claude/Codex: sync dedicato solo se il cliente usa
  entrambi gli agenti.

In `memory/MEMORY.md` aggiungi i puntatori:
- `AGENTS.md` - regole operative ed eventuali vincoli del settore.
- `ecosistema/FONTI.md` - fonti autorizzate e cartelle reali.
- `ecosistema/ASSET.md` - asset operativi: canali, fornitori, gestionali, repo,
  app, archivi e risorse da usare o rispettare.
- `ecosistema/PROCESSI.md` - lavori ricorrenti.
- `ecosistema/LIMITI.md` - azioni vietate o da confermare.

In `ecosistema/FONTI.md` registra quello che esiste davvero:
- cartella madre usata (con la posizione scelta: locale o cloud);
- documenti di business: restano dove sono gia' (Drive/OneDrive/server) e si
  LEGGONO via connettore, non si copiano nella cartella madre;
- eventuali output gia' prodotti in Claude/Codex.
Non inventare percorsi: se una fonte non e' presente, scrivi "da collegare".

In `ecosistema/ASSET.md` registra ogni risorsa operativa che emerge:
- email/PEC, banca, gestionale, WhatsApp, Drive, fornitore, sito, repo, kit,
  app, archivio o servizio esterno;
- per ogni asset indica casa/fonte vera, uso, stato, archivio/prove e limiti;
- se il cliente dice "aggiungi", "abbiamo", "ho comprato", "attiva" o
  "collega" una nuova risorsa, aggiorna questo registro e poi solo i processi o
  limiti collegati che servono davvero.

Per PEC/email certificata chiedi sempre:
- il cliente ha una PEC/email certificata?
- vuole solo registrarla come asset o anche leggerla/inviarla con agenti?
- qual e' il provider e dove si controlla davvero?
- esistono ricevute o archivi da conservare?
- ci sono credenziali dedicate o app password? Se si', devono stare solo in
  `.secrets/`, mai in Git, memoria o chat.
Non segnare la PEC `ATTIVO` senza una prova reale di login o lettura/invio.
Ogni invio a terzi richiede conferma umana esplicita.

In `ecosistema/PROCESSI.md` aggiungi i miei processi ricorrenti reali, con input
e output attesi (lascia "da definire" dove non e' ancora chiaro).

In `ecosistema/LIMITI.md` aggiungi:
- eventuali output che non posso generare in automatico (se il settore lo vieta);
- nessun invio a terzi senza la mia conferma;
- nessun uso di file non autorizzati;
- nessuna modifica/cancellazione di dati originali.

Fase 5-ter - browser giusto (obbligatoria)
Chiedi al cliente quale browser usa davvero (di solito Chrome) e verifica
quale e' il browser predefinito di Windows/Mac. Se non coincidono, sistemalo
TU: imposta il browser che il cliente usa come predefinito (se il sistema
protegge il passaggio finale, apri tu la schermata giusta e digli solo dove
fare un click). Poi prova reale: apri un link e conferma che si apre nel
browser giusto. Serve perche' login e autorizzazioni (GitHub, Google,
Claude) si aprono nel predefinito: se e' quello sbagliato, il cliente si
ritrova su un browser dove non e' loggato.

Fase 5-bis - apertura sempre giusta (obbligatoria)
Il rischio piu' frequente e' che io apra l'agente nella cartella sbagliata e
il lavoro finisca altrove. Chiudilo cosi':
1. Crea sul Desktop un collegamento/launcher che apre l'agente DIRETTAMENTE
   dentro la cartella madre (Windows: collegamento o script .bat/.ps1 che fa
   `cd` nella cartella madre e lancia l'agente; Mac: comando rapido o alias).
   Dagli un nome chiaro, per esempio "Apri il mio Ecosistema AI".
2. Dimmi di usare SEMPRE quel collegamento per aprire l'agente.
3. Provalo davvero: aprilo, verifica che l'agente legga AGENTS.md della
   cartella madre, e mostrami la prova.

Fase 6 - collaudo
1. Verifica che nella cartella madre esistano:
   AGENTS.md, .gitignore, memory/MEMORY.md,
   ecosistema/FONTI.md, ecosistema/ASSET.md, ecosistema/PROCESSI.md,
   ecosistema/LIMITI.md, logs/install-log.md, REPORT_FINALE.md.
   Nota: `CLAUDE.md` e `.claude/README.md` devono esistere solo in modalita'
   Claude o both; `.codex/README.md` solo in modalita' Codex o both.
2. Verifica che la cartella madre sia un repository git (esiste `.git`), che
   `.gitignore` escluda `.secrets/`, `*.env`, token, chiavi e credenziali, e che
   esista il primo commit (`git log` mostra "installazione iniziale"). Il setup
   lo crea da solo a fine corsa: se manca, fallo tu con `git add -A` +
   `git commit`, altrimenti il backup della Fase 7 parte da un repository vuoto.
3. Prova delle fonti (obbligatoria). Per ogni fonte disponibile fai una prova
   innocua di SOLA LETTURA e mostrami il dato vero appena letto:
   - email: oggetto e mittente di una mail recente, senza inviare nulla;
   - calendario: titolo e data di un evento vero, senza modificarlo;
   - Drive/OneDrive/cartelle: nome di un file vero, senza aprire dati sensibili;
   - gestionale/export: una riga vera dell'export, senza modificarlo.
   Segna la fonte `OK` SOLO se mi mostri quel dato reale. Senza dato mostrato la
   fonte e' `DA CONFERMARE` o `DA COLLEGARE`. Non dedurre un collegamento, non
   fidarti del fatto che "di solito c'e'": su una installazione nuova i connettori
   spesso non ci sono ancora, quindi in dubbio e' `DA COLLEGARE`, non `OK`.
4. Leggi `AGENTS.md` e dimmi in 5 righe:
   - chi sono;
   - dove sta la cartella madre e perche' (locale o cloud, scelta alla Domanda 1);
   - quali fonti vedi, con lo stato e la prova del dato letto per ogni `OK`;
   - cosa puoi fare;
   - cosa NON puoi fare.
5. Prepara una prova piccola, senza dati sensibili, coerente col mio lavoro
   (per esempio una bozza vuota di un documento ricorrente, con campi da
   compilare e, se il settore lo richiede, un disclaimer "bozza da rivedere").
6. Se qualcosa non passa, correggi e riprova.

Fase 7 - backup e seconda postazione (scelta guidata)
Serve a non perdere il lavoro e a usare l'Ecosistema da piu' di un computer.
Anche qui decidi con me, non con una regola fissa: la via giusta dipende da cosa
gia' uso.
1. Conferma che la cartella madre e' un repository git e che `.gitignore`
   esclude i segreti. Se manca, crealo prima di proseguire. Questo vale sempre.
2. DOMANDA 2 - come fare il backup. [UMANO]
   Presentami le due opzioni e fammi scegliere:
   - GitHub privato: copia su una repo privata. Sicuro, ma serve un account
     GitHub. Una volta configurato, il push lo fa l'agente da solo a fine
     sessione (regola del salvataggio automatico), non devo ricordarmene io.
   AUTENTICAZIONE GITHUB - REGOLA FISSA: si usa SOLO GitHub CLI con login dal
   browser (`gh auth login` → GitHub.com → HTTPS → login via web browser: il
   cliente clicca Autorizza e basta). VIETATO far creare, copiare o incollare
   token (ghp_...), password o chiavi al cliente: e' una procedura da
   sviluppatori. Se `gh` manca, l'agente lo installa (es. winget/brew).
   - Copia/sincronizzazione su Drive o OneDrive: uso quello che ho gia'; comodo,
     ma la sincronizzazione continua puo' corrompere i file mentre l'agente
     scrive. Meglio come copia di backup, non come cartella di lavoro viva.
   L'account e l'autorizzazione (GitHub o cloud) li attivo io: tu guidami a voce,
   non creare account ne' inserire password al posto mio.
3. DOMANDA 3 - seconda postazione, se mi serve. [UMANO]
   Coerente con la Domanda 2:
   - se ho scelto GitHub: sull'altro PC si fa `clone` della stessa repo e si
     tiene allineata con `pull` e `push` (copia locale vera, scrittura sicura);
   - se ho scelto Drive/OneDrive: si usa la cartella condivisa, ricordando di non
     aprirla viva da due PC nello stesso momento per non corromperla.
   Se non mi serve una seconda postazione, salta questo punto.
4. Su ogni PC i connettori (Gmail, Calendar, Drive, Meta) si ri-autorizzano con
   un login: le chiavi restano per-macchina, non viaggiano nel backup. Confermalo.
5. I documenti di business (report, anagrafiche, file pesanti) non vanno nel
   backup del cervello: restano su Drive/OneDrive/server e si leggono via
   connettore da qualsiasi PC.
Se non voglio impostare il backup adesso, lascia comunque la cartella come
repository git in locale e segnala che il backup remoto resta da fare. Non
bloccare il setup.

Fase 8 - cosa collegare dopo
Non chiudere con "installato" e basta.
Dimmi in modo operativo:
- Cervello: cosa e' stato creato e testato, e dove vive (locale o cloud);
- Ecosistema: quali fonti reali hai trovato e con quale prova;
- Asset: quali risorse operative hai registrato in `ecosistema/ASSET.md`;
- Da collegare: dove vanno collegate le mie fonti che oggi mancano (cartelle,
  report, CRM/gestionale);
- Blocchi: cosa manca perche' non esiste ancora o richiede me/Sal.

Fase 9 - mappa moduli da installare o lasciare fuori
Non limitarti alla PEC o al primo asset emerso. Prima di chiudere, crea una
mappa moduli con una riga per ogni area sotto. Per ogni modulo usa uno stato
obbligatorio: `NON SERVE`, `DA SCOPRIRE`, `DA COLLAUDARE`, `INSTALLABILE`,
`ATTIVO`.

Moduli da valutare:
- PEC/email certificata;
- email e calendario (accesso e prova fonte);
- calendario operativo (calendari separati, colori, regole evento);
- Drive/OneDrive/cartelle operative;
- CRM/gestionale/export;
- plugin/connettori;
- skill per lavori ripetuti;
- agenti/ruoli dedicati;
- guardiani/hook;
- ronde/monitoraggi;
- voce/dettatura;
- compliance/privacy/AI Act.

Regola: se non hai una fonte reale o una prova, non scrivere `ATTIVO`. Scrivi
`DA SCOPRIRE` o `DA COLLEGARE` nel dettaglio. Se il modulo non serve al lavoro
del cliente, scrivi `NON SERVE`. Il prossimo passo deve nascere da questa mappa,
non dalla memoria di chi sta seguendo la consegna.

Se il cliente usa l'agenda soprattutto tramite colori, leggi
`MODULO_CALENDARIO_OPERATIVO.md` prima di proporre o creare calendari. Il primo
blocco crea solo eventi test o nuovi eventi approvati: non migrare eventi vecchi
senza conferma esplicita.

Report finale obbligatorio:
- cartella madre scelta e sua posizione (locale o cloud, come da Domanda 1);
- standard applicato: repo ufficiale + versione letta;
- modalita' accesso standard: sola lettura / percorso tecnico autorizzato;
- modalita' scelta: claude / codex / both;
- file creati;
- cartella madre = repository git si/no;
- `.gitignore` esclude i segreti si/no;
- backup scelto: GitHub privato / copia su Drive-OneDrive / da fare (Domanda 2);
- seconda postazione impostata si/no/non serve;
- Cervello verificato si/no;
- prova piccola completata si/no;
- Ecosistema: fonti trovate, con stato (OK / DA CONFERMARE / DA COLLEGARE) e per ogni OK la prova del dato letto;
- Asset registrati in `ecosistema/ASSET.md`;
- Mappa moduli con stato per ogni modulo;
- codice esterno eseguito: no / si con autorizzazione esplicita e prova;
- chiusura ambiente: email/browser/tab/app chiusi oppure handoff dichiarato;
- cosa resta da collegare e dove;
- verdetto: PASSA / PASSA CON ATTENZIONE / NON PASSA.

Consegna del report e ciclo tra agenti:
1. Completa e collauda `REPORT_FINALE.md` nella cartella madre.
2. Mostra al proprietario verdetto, prove e blocchi reali.
3. Chiedi: `Autorizzi l'invio del report a sal@salchiarenza.ai?`
4. Solo dopo un si' esplicito, invia davvero il report. Una bozza non conta come
   consegna. Se Gmail non e' collegata, conserva il report locale come
   `PRONTO DA INVIARE` e dichiara il blocco senza simulare l'invio.

Prima del report fai `AUTOCONTROLLO`: rileggi missione, azioni fatte, prove,
file toccati, blocchi umani veri e superfici aperte da te (email, browser, tab,
form, preview, login, app temporanee). Dopo il report vai in `SAL_VERIFICA`:
non archiviare subito e non decidere tu che e' finita. Se LeaderAI risponde
`CONTINUA`, lavori ancora sulla stessa missione, rifai autocontrollo e mandi un
report aggiornato. Se LeaderAI risponde `CHIUDI` o conferma che va bene, allora
ARCHIVIA l'email di missione ricevuta, chiudi le pagine/app aperte da te e
annota la chiusura nei log.

Regola stabile: ogni email di missione da LeaderAI si ESEGUE, si ripara tutto
cio' che si puo' riparare, si prova, si fa autocontrollo, si risponde con un
resoconto finale, poi si aspetta `CONTINUA` o `CHIUDI`.
```
