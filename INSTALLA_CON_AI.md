# Autoconfigurazione sicura - Cervello + Ecosistema

Questa e' la procedura unica per una nuova installazione cliente. La repo
ufficiale resta lo standard LeaderAI verificabile; l'agente del cliente la
legge in sola lettura e applica localmente i file nella cartella madre.

Percorso predefinito: lettura della repo ufficiale, creazione locale e
collaudo. Il clone della repo e l'esecuzione di `leaderai_setup.py` sono un
percorso tecnico opzionale: si usano solo dopo una richiesta separata e una
autorizzazione esplicita del proprietario.
Il percorso standard non richiede clone della repo.

REGOLA PER CHI CONSEGNA (LeaderAI): l'email di consegna e' corta e punta a
questa procedura. L'installazione produce prima un report locale verificato;
l'invio del report a LeaderAI avviene poi con autorizzazione esplicita del
proprietario.

Il modello unico, versionato e collaudabile e'
[`EMAIL_CONSEGNA.md`](EMAIL_CONSEGNA.md). Questa procedura non mantiene una
seconda copia dell'email.

## Nucleo deterministico di installazione

Questa sezione delimitata e' il percorso minimo verificabile per montare il
telaio. Il collaudo di rilascio legge questo nucleo, `install_contract.json` e
i template; la missione cliente continua poi con le fasi successive per
personalizzazione, fonti reali e prove macchina.

<!-- START_NUCLEO_INSTALLAZIONE -->

1. Leggi `VERSION`, `install_contract.json` e i template dichiarati dal
   contratto. La fotografia standard resta in sola lettura.
2. Usa o crea una sola cartella madre nel percorso gia' deciso. Non creare
   stanze, fonti, asset o connettori inventati.
3. Applica le regole `common` del contratto e soltanto il ramo `codex`,
   `claude` o `both` richiesto. Sostituisci `{{client_name}}`, `{{date}}`,
   `{{agent}}` e `{{version}}`; `CLAUDE.md` resta il ponte esatto
   `@AGENTS.md`. In una casa nuova usa copia e sostituzione meccanica in batch
   dai template: non riscrivere i file uno alla volta.
4. La fotografia puo' avere file protetti in sola lettura. La fonte resta
   intoccabile; dopo la copia rendi scrivibili soltanto i file creati nella
   cartella madre, prima di personalizzarli. Non cambiare mai i permessi della
   fotografia standard.
5. Per Claude in un collaudo isolato non toccare le user settings: registra
   `autoMemoryDirectory` come `DA COLLAUDARE`. Sulla macchina cliente lo
   configuri e lo provi seguendo la Fase 4.
6. Inizializza Git locale. Prima del commit usa la allowlist dei file standard
   del contratto, rileggi lo staging e controlla nomi e contenuti per segreti.
   Il primo messaggio contiene la frase `installazione iniziale`.
7. Crea `REPORT_FINALE.md` temporaneo e ignorato da Git con `VALIDO AL`,
   `STATO MISSIONE: APERTA`, standard/versione, modalita', prove, limiti e una
   sezione `## Verdetto`. Nel collaudo anonimo usa `PASSA CON ATTENZIONE`
   quando il telaio e' completo e restano soltanto prove macchina differite;
   usa `NON PASSA` per ogni difetto del telaio. Il report apre con `STATO PER
   LE PERSONE`: `Fatto`, `Manca`, `Prossimo passo`, `Intervento umano`; solo
   dopo vengono i dettagli tecnici.
8. Registra `default_browser`, `desktop_launcher` e `remote_backup` come
   `DA COLLAUDARE` o `DA COLLEGARE` nel collaudo anonimo. Sulla macchina
   cliente diventano `OK` soltanto dopo prova reale.
9. Verifica file obbligatori, file vietati del ramo opposto, ponte, memoria,
   report fuori Git, commit iniziale e fotografia standard intatta.
10. Il nucleo passa solo con repository pulito e nessun file della repo tecnica
   copiato nella casa.

<!-- END_NUCLEO_INSTALLAZIONE -->

## Missione operativa letta dall'agente

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
La modalita' governa solo le cartelle di configurazione `.claude/` e `.codex/`.
Il contratto comune `AGENTS.md` + `CLAUDE.md` esiste sempre.

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
   `ecosistema/ASSET.md`, `commit git`, file di
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
5. La cartella madre sta FUORI dalle cartelle degli agenti e dei programmi
   (`Codex`, `Claude`, `ChatGPT`, cartelle di installazione): l'ecosistema
   vive a se' nel PC e gli agenti ci entrano. Se il tuo permesso di
   scrittura copre solo la cartella dell'agente, NON ripiegare li' dentro:
   dichiaralo, fatti concedere l'accesso al percorso scelto [UMANO] e crea
   la casa solo dove deve vivere.

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
   - `install_contract.json`
   - `MANIFEST.md`
   - `templates/AGENTS.md`
   - `templates/STANZA_AGENTS.md`
   - `templates/ISPETTORE_SKILL.md`
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
   - `templates/AGENT_CHAT.md`
2. Registra nel report la versione letta. Se un file non e' leggibile, chiedi
   soltanto l'autorizzazione per l'accesso web di sola lettura e riprova.
3. Il percorso predefinito termina qui per la repo: niente clone e niente
   esecuzione di codice scaricato.

Fase 4 - monta localmente il Cervello
1. Crea le cartelle `memory/`, `logs/` ed `ecosistema/` nella cartella madre.
2. Usa `install_contract.json` come lista macchina unica dei template, dei file
   obbligatori e del ramo agente. Applica localmente i template, sostituendo
   `{{client_name}}`, `{{date}}`, `{{agent}}` e `{{version}}` con i dati reali
   letti dalla repo:
   - `templates/AGENTS.md` -> `AGENTS.md`
   - `templates/MEMORY.md` -> `memory/MEMORY.md`
   - `templates/ASSET.md` -> `ecosistema/ASSET.md`
   - `templates/GITIGNORE.txt` -> `.gitignore`
   - `templates/FONTI.md` -> `ecosistema/FONTI.md`
   - `templates/PROCESSI.md` -> `ecosistema/PROCESSI.md`
   - `templates/LIMITI.md` -> `ecosistema/LIMITI.md`
   - `templates/STANZA_AGENTS.md` -> `ecosistema/STANZA_AGENTS.md`
   - `templates/INSTALL_LOG.md` -> `logs/install-log.md`
   - `templates/CLAUDE.md` -> `CLAUDE.md` (ponte, sempre)
   - `templates/AGENT_CHAT.md` -> `AGENT_CHAT.md` (chat di gruppo: bacheca
     comune di tutti gli agenti della casa, regole d'uso dentro al file)
   - modalita' Claude -> `templates/ISPETTORE_SKILL.md` in
     `.claude/skills/ispettore-ecosistema/SKILL.md`
   - modalita' Codex -> `templates/ISPETTORE_SKILL.md` in
     `.agents/skills/ispettore-ecosistema/SKILL.md`
   - modalita' both -> entrambe le skill, identiche e puntate allo stesso
     `CHECKUP.md`
3. Crea SEMPRE `CLAUDE.md` dal template: e' il ponte di una riga (`@AGENTS.md`)
   che fa leggere la mappa anche a Claude Code, qualunque agente sia in uso
   oggi (Claude Code legge `CLAUDE.md`, Codex legge `AGENTS.md`). Poi la
   configurazione per agente: modalita' Claude -> `.claude/README.md`;
   modalita' Codex -> `.codex/README.md`. Usa entrambe le configurazioni solo
   se LeaderAI lo ha chiesto esplicitamente.
4. Se Claude Code e' attivo, configura `autoMemoryDirectory` nelle user
   settings di ogni computer (`~/.claude/settings.json`) con la forma portabile
   `~/...` della memoria canonica dichiarata nell'`AGENTS.md` quando vive sotto
   la home di quella macchina. Usa un percorso assoluto soltanto dopo averlo
   letto sulla stessa macchina e soltanto se la memoria vive fuori dalla home.
   La chiave non e' valida nelle settings project/local. Accetta il trust del
   workspace e verifica ogni postazione con `/memory`. Se trovi una memoria
   auto esterna gia' piena, confronta e unisci le voci prima di cambiare il
   percorso.
5. Crea `REPORT_FINALE.md` come output temporaneo della missione con
   `VALIDO AL` e `STATO MISSIONE: APERTA`; `.gitignore` lo esclude. Non e' una
   fonte di stato e viene eliminato dopo `CHIUDI`.
6. Non sovrascrivere file vivi: integra le sezioni mancanti e registra nel report
   cosa era gia' presente, cosa hai creato e cosa hai aggiornato.
7. Verifica che `.gitignore` escluda `.secrets/`, file `.env`, token, chiavi,
   password, credenziali e
   `REPORT_FINALE.md` prima del primo commit.

Percorso tecnico opzionale:
`leaderai_setup.py` resta un attrezzo LeaderAI per collaudi o installazioni
esplicitamente autorizzate. Se LeaderAI propone di usarlo, presenta prima al
proprietario repo, comando, file che saranno creati e permessi richiesti; procedi
solo dopo la sua autorizzazione esplicita. Questo percorso non si attiva come
ripiego automatico.

Fase 5 - personalizza il Cervello
Dopo l'installazione, apri i file creati nella cartella madre e aggiorna solo i
punti necessari, senza cancellare il resto.

Prima di aggiungere una struttura business, costruisci la mappa dell'ambiente
reale come organigramma. L'agente nella cartella madre e' il Boss
dell'Ecosistema; ogni ramo organizzativo e' una stanza con il proprio
Amministratore di settore, subordinato al Boss:

1. censisci le cartelle, le fonti, gli output, le skill, gli script, gli agenti,
   i connettori, le procedure e gli archivi gia' presenti;
2. classifica ogni elemento rilevante come `STANZA`, `FONTE`, `OUTPUT`,
   `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`;
3. riconosci come stanza solo una funzione operativa stabile con fonti,
   processi o output propri;
4. aggiorna il registro delle stanze in `AGENTS.md`, assegna a ogni ramo il suo
   Amministratore di settore e collegalo al Boss dell'Ecosistema;
5. per ogni vera stanza crea o integra `AGENTS.md` da
   `ecosistema/STANZA_AGENTS.md` e `CLAUDE.md` come ponte di una riga
   (`@AGENTS.md`), con scopo, contenuto, fonti, output, capacita',
   collegamenti a monte e collegamenti a valle, dove scrivere, amministratore e
   relazione gerarchica con il Boss;
6. collega direttamente due stanze solo quando un processo reale passa tra le
   due;
7. ripara ponti e puntatori tecnici rotti; per creare, fondere, rinominare,
   spostare o eliminare stanze presenta una proposta e attendi la decisione del
   proprietario.

Skill, script, agenti, connettori, moduli e procedure sono capacita' della
stanza che li usa. Se una capacita' e' gia' coperta, integrala o riusala. Una
nuova stanza nasce solo quando nessuna stanza esistente puo' possedere quella
funzione e il proprietario approva la proposta.

Ogni cartella nuova passa lo stesso ciclo prima del salvataggio: classe,
proprietario, eventuale mappa locale, collegamento alla radice e prova. Nomi
generici come `documenti`, `output`, `exports`, `varie`, `misc`, `temp` o
`nuova cartella` restano `SOSPETTA` finche' non vengono ricondotti alla stanza
proprietaria. Un residuo vuoto o inutile creato dall'agente nello stesso
lavoro viene rimosso prima del commit; contenuti preesistenti si spostano,
fondono o eliminano solo dopo conferma.

In `AGENTS.md` aggiungi una sezione "Regole [NOME CLIENTE]" con le mie regole reali:
- chi sono e cosa faccio [AZIENDA];
- rispondi in italiano, chiaro e operativo;
- cosa ti chiedo di supportare (ricerca, analisi, organizzazione fonti, bozze);
- eventuali vincoli del mio settore: se il mio lavoro e' regolamentato, non
  generi l'output finale; ogni output e' una bozza che rivedo e firmo io;
- non inviare email, non cancellare file, non spostare cartelle vive e non usare
  dati sensibili senza mia conferma esplicita;
- SALVATAGGIO AUTOMATICO: alla fine di ogni sessione di lavoro prepara da solo
  il primo commit con una allowlist dei file standard dichiarati in
  `install_contract.json`, rileggi i nomi in staging e controlla che non
  contengano segreti. Non usare `git add -A` come scorciatoia. Crea il commit
  con un messaggio chiaro, senza che io lo chieda.
  Se il backup remoto (GitHub) e' configurato, dimmi se esistono commit da
  pubblicare; esegui `git push` soltanto dopo il mio comando. Il salvataggio
  locale resta automatico;
- TUTTO NASCE NELLA CASA: ogni file, app, documento o nota che crei nasce
  dentro la cartella madre, mai sul Desktop o altrove. L'agente si apre
  sempre da questa cartella;
- NIENTE MANI DENTRO LA CASA: dentro la cartella madre non si cancella e non
  si sposta nulla a mano da Esplora file/Finder. Si chiede all'agente, cosi'
  il salvataggio git resta coerente e nulla si perde;
- OUTPUT NELLA CASA PROPRIETARIA: ogni resoconto o report vive nella stanza
  responsabile del processo. Prima usa la casa esistente; non creare una
  cartella `resoconti/` per abitudine;
- CONTENUTI BUSINESS FUORI DAL CODICE: testi e regole che devo poter correggere
  vivono in una fonte esterna al codice; app e script la leggono e generano
  PDF/Word come derivati. Se la fonte manca, falliscono in modo visibile.

Mantieni anche la sezione "Comunicazione e fonti di verita'":
- gli agenti non si parlano direttamente, leggono e scrivono file condivisi;
- stato corrente, prossimo passo e scadenze: in testa al file proprietario
  della stanza; diario sotto, dal piu' recente;
- storia tecnica/strutturale: soltanto `logs/install-log.md`;
- `REPORT_FINALE.md`: output temporaneo e datato della missione aperta;
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
- firma, timbro e sigillo sono asset ad alto rischio: file in `.secrets/` o
  altra casa protetta fuori Git, soli metadati qui e conferma umana sul singolo
  documento prima di applicarli o inviarli;
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
  Controlla indice e history Git del solo percorso senza aprire il contenuto;
  se l'esposizione non e' esclusa, blocca l'uso e proponi rotazione.
Non segnare la PEC `ATTIVO` senza una prova reale di login o lettura/invio.
Ogni invio a terzi richiede conferma umana esplicita.

In `ecosistema/PROCESSI.md` aggiungi i miei processi ricorrenti reali, con input
e output attesi (lascia "da definire" dove non e' ancora chiaro).

In `ecosistema/LIMITI.md` aggiungi:
- eventuali output che non posso generare in automatico (se il settore lo vieta);
- nessun invio a terzi senza la mia conferma;
- nessun uso di file non autorizzati;
- nessuna modifica/cancellazione di dati originali.

Fase 5-ter - browser giusto (obbligatoria sulla macchina cliente)
Chiedi al cliente quale browser usa davvero (di solito Chrome) e verifica
quale e' il browser predefinito di Windows/Mac. Se non coincidono, sistemalo
TU: imposta il browser che il cliente usa come predefinito (se il sistema
protegge il passaggio finale, apri tu la schermata giusta e digli solo dove
fare un click). Poi prova reale: apri un link e conferma che si apre nel
browser giusto. Serve perche' login e autorizzazioni (GitHub, Google,
Claude) si aprono nel predefinito: se e' quello sbagliato, il cliente si
ritrova su un browser dove non e' loggato.
Nel gate anonimo di rilascio questa prova resta `DA COLLAUDARE`: richiede il
browser e le preferenze della macchina reale.

Fase 5-bis - apertura sempre giusta (obbligatoria sulla macchina cliente)
Il rischio piu' frequente e' che l'agente venga aperto nella cartella
sbagliata: vede la task o l'email, ma nasce senza Cervello ed Ecosistema.
Chiudilo cosi':
1. Rileva e dichiara la superficie reale: Codex Desktop, Codex CLI, Claude
   Code, Windows nativo, WSL o macOS. Non mescolare percorsi Windows e WSL.
2. Codex Desktop: apri la cartella madre come progetto locale primario con
   `Ctrl+O` / **Add new project**, seleziona la cartella e crea una nuova task.
   Dal terminale, se disponibile, `codex app "<CARTELLA_MADRE>"` e' una
   scorciatoia equivalente.
3. Codex CLI: usa `codex -C "<CARTELLA_MADRE>"` oppure avvialo da quella
   directory. Claude Code: entra nella cartella madre e avvia una nuova
   sessione; `/context` deve mostrare `CLAUDE.md` e `AGENTS.md`.
4. Prima del trust fai un inventario read-only di provenienza, `AGENTS.md`,
   `.codex/config.toml`, `.claude/settings*`, hook e skill. Una configurazione
   inattesa produce `BLOCCO`; il trust arriva dopo questa verifica.
5. Crea un launcher solo se serve davvero al cliente. Usa comandi che trattano
   il percorso come valore letterale e prova anche spazi, accenti, parentesi e
   `&`; conserva un launcher esistente diverso invece di sovrascriverlo.
6. Prova da una posizione estranea alla casa. La nuova task/sessione deve
   dichiarare percorso corrente, mappa caricata e tre regole lette da
   `AGENTS.md`. Percorso diverso = `FUORI DAL CERVELLO`, nessuna scrittura.
7. Esegui quindi, senza aggiungere percorsi o indizi, la richiesta esatta:
   `Crea la Brand Identity`. La prova passa solo se l'agente instrada dalla
   mappa madre alla responsabilita' proprietaria, apre fonti brand reali e
   crea o aggiorna l'output nella casa corretta.
Nel gate anonimo di rilascio il gesto Desktop resta `DA COLLAUDARE`: il gate
prova sessioni nuove dentro una casa anonima e conserva le evidenze.

Fase 6 - collaudo
1. Verifica che nella cartella madre esistano:
   AGENTS.md, CLAUDE.md, .gitignore, memory/MEMORY.md,
   ecosistema/FONTI.md, ecosistema/ASSET.md, ecosistema/PROCESSI.md,
   ecosistema/LIMITI.md, logs/install-log.md.
   Verifica anche che ogni vera stanza abbia `AGENTS.md` + `CLAUDE.md` e che
   ogni `CLAUDE.md` contenga soltanto `@AGENTS.md`. Verifica che la mappa madre
   dichiari il Boss dell'Ecosistema e che ogni ramo, nuovo o preesistente,
   dichiari il proprio Amministratore di settore subordinato al Boss.
   `.claude/README.md` esiste solo in modalita' Claude o both;
   `.codex/README.md` esiste solo in modalita' Codex o both.
   Verifica anche la skill `ispettore-ecosistema` nel percorso dell'agente
   attivo: `.claude/skills/` per Claude Code, `.agents/skills/` per Codex,
   entrambe in modalita' both.
   Se Claude e' attivo, verifica anche le user settings di ogni computer, trust
   del workspace e `/memory` sulla memoria canonica.
2. Verifica che la cartella madre sia un repository git (esiste `.git`), che
   `.gitignore` escluda `.secrets/`, `*.env`, token, chiavi, credenziali,
   `REPORT_FINALE.md`, e che
   esista il primo commit (`git log` mostra "installazione iniziale"). Il setup
   lo crea da solo a fine corsa: se manca, usa la allowlist del contratto,
   rileggi lo staging, esegui il controllo segreti e poi `git commit`.
   Altrimenti il backup della Fase 7 parte da un repository vuoto.
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
7. Collauda la rete delle stanze con almeno due richieste realistiche partendo
   dalla radice, senza suggerire il percorso. Per ciascuna registra:
   richiesta -> madre/stanza -> fonte -> capacita'/processo -> output. Se l'agente non
   trova il percorso, correggi mappa o collegamenti e riprova.
8. Verifica che ogni stanza sia raggiungibile dalla mappa madre, che nessuna
   capacita' sia isolata, che ogni amministratore riporti al Boss e che non
   esistano due stanze per la stessa funzione.
9. Lancia l'Ispettore sul risultato: censisci ogni cartella e file visibile
   nella home, classifica i percorsi, ripara i buchi sicuri e blocca il
   verdetto se restano cartelle generiche, vuote, doppie, tecniche, senza
   proprietario o stanze senza mappa. Registra la tabella
   `percorso | classe | amministratore | riporta al | mappa locale |
   collegamento radice | azione | prova`.
10. Confronta la versione in `AGENTS.md` con il `VERSION` appena letto: senza
    confronto o con valori diversi il verdetto e' `NON PASSA`.
11. Verifica: memoria unica; report temporaneo non versionato; contenuti
    business con una fonte esterna al codice; configurazioni credenziali in
    `.secrets/` e history controllata per percorso; firma/timbro registrati e
    protetti; file progetto con stato, prossimo passo e scadenze in testa.

Fase 7 - backup e seconda postazione (scelta guidata)
Serve a non perdere il lavoro e a usare l'Ecosistema da piu' di un computer.
Anche qui decidi con me, non con una regola fissa: la via giusta dipende da cosa
gia' uso.
1. Conferma che la cartella madre e' un repository git e che `.gitignore`
   esclude i segreti. Se manca, crealo prima di proseguire. Questo vale sempre.
2. DOMANDA 2 - come fare il backup. [UMANO]
   Presentami le due opzioni e fammi scegliere:
   - GitHub privato: copia su una repo privata. Sicuro, ma serve un account
     GitHub. Una volta configurato, l'agente salva localmente a fine sessione
     e propone il push quando esistono commit da pubblicare. Il push parte
     soltanto dopo un comando esplicito.
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
   Nel gate anonimo di rilascio il backup remoto resta `DA COLLAUDARE` perche'
   richiede una scelta e un account reali.
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

Ogni modulo `INSTALLABILE` o `ATTIVO` dichiara la cartella madre o la stanza
proprietaria. Prima riusa una capacita' equivalente gia' presente. La creazione
di una nuova stanza resta una decisione strutturale esplicita del proprietario.

Se il cliente usa l'agenda soprattutto tramite colori, leggi
`MODULO_CALENDARIO_OPERATIVO.md` prima di proporre o creare calendari. Il primo
blocco crea solo eventi test o nuovi eventi approvati: non migrare eventi vecchi
senza conferma esplicita.

Report temporaneo obbligatorio per la missione:
- `STATO PER LE PERSONE` in apertura, con `Fatto`, `Manca`, `Prossimo passo`
  e `Intervento umano` in parole semplici;
- cartella madre scelta e sua posizione (locale o cloud, come da Domanda 1);
- standard applicato: repo ufficiale + versione letta;
- versione metodo registrata e versione precedente trovata, se esiste;
- modalita' accesso standard: sola lettura / percorso tecnico autorizzato;
- modalita' scelta: claude / codex / both;
- file creati;
- cartella madre = repository git si/no;
- `.gitignore` esclude i segreti si/no;
- memoria unica e, per Claude, prova `autoMemoryDirectory` + `/memory`;
- backup scelto: GitHub privato / copia su Drive-OneDrive / da fare (Domanda 2);
- seconda postazione impostata si/no/non serve;
- Cervello verificato si/no;
- prova piccola completata si/no;
- ingresso reale: superficie, progetto primario/CWD, nuova task/sessione,
  `AGENTS.md` caricato e tre regole mostrate;
- prova senza indizi `Crea la Brand Identity`: percorso
  madre/stanza -> fonte brand -> output, con esito;
- continuita' chat di gruppo in modalita' `both`: Codex -> Claude Code ->
  Codex, con un solo ID missione e tre sessioni distinte;
- Ecosistema: fonti trovate, con stato (OK / DA CONFERMARE / DA COLLEGARE) e per ogni OK la prova del dato letto;
- Asset registrati in `ecosistema/ASSET.md`;
- classificazione dell'ambiente e mappa delle stanze con monte/valle;
- tabella Ispettore di ogni percorso visibile nella home;
- capacita' collegate a ogni stanza e possibili doppioni evitati;
- almeno due prove di instradamento richiesta -> madre/stanza -> fonte -> output;
- fonti business esterne al codice e derivati verificati;
- credenziali controllate per percorso/history senza leggere il contenuto;
- firma/timbro protetti, registrati e limitati;
- file progetto con stato/prossimo/scadenze in testa e diario ordinato;
- Mappa moduli con stato per ogni modulo;
- codice esterno eseguito: no / si con autorizzazione esplicita e prova;
- chiusura ambiente: email/browser/tab/app chiusi oppure handoff dichiarato;
- cosa resta da collegare e dove;
- `LEZIONE CANDIDATA`: nessuna oppure caso, causa, regola generale e prova che
  avrebbe intercettato l'errore;
- verdetto: PASSA / PASSA CON ATTENZIONE / NON PASSA.

Consegna del report e ciclo tra agenti:
1. Completa e collauda `REPORT_FINALE.md` temporaneo nella cartella madre, con
   `STATO PER LE PERSONE` prima dei dettagli tecnici, data/ora e stato missione.
2. Mostra al proprietario verdetto, prove e blocchi reali.
3. Mostra destinatario, oggetto, versione del report e azione esterna esatta.
   Chiedi: `Autorizzi l'invio del report in risposta allo stesso mittente
   LeaderAI verificato?`
   L'autorizzazione vale soltanto per questo specifico
   invio; parole come "manda avanti il lavoro" non autorizzano la posta.
4. Solo dopo un si' esplicito, invia davvero il report in risposta alla
   missione verificata. Una bozza non conta come consegna. Se Gmail non e'
   collegata, conserva il report locale come
   `PRONTO DA INVIARE` e dichiara il blocco senza simulare l'invio.

Prima del report fai `AUTOCONTROLLO`: rileggi missione, azioni fatte, prove,
file toccati, blocchi umani veri e superfici aperte da te (email, browser, tab,
form, preview, login, app temporanee). Il report locale resta
`PRONTO DA INVIARE` finche' il proprietario non autorizza l'invio. Dopo il suo
si', invia davvero, archivia l'email della missione nello stesso giro e passa a
   `SAL_VERIFICA`; lo stato resta nel report temporaneo, non nella Inbox. Se LeaderAI
risponde `CONTINUA`, lavori ancora sulla stessa missione, rifai autocontrollo,
aggiorni il report e chiedi una nuova autorizzazione prima di inviarlo. Se
   risponde `CHIUDI` o conferma che va bene, promuovi i fatti nel file
   proprietario della stanza, registra nel log solo gli eventuali cambi
   tecnici/strutturali, elimina `REPORT_FINALE.md` e chiudi le pagine/app aperte
   da te.

Regola stabile: ogni email di missione da LeaderAI si ESEGUE, si ripara tutto
cio' che si puo' riparare, si prova, si fa autocontrollo, si risponde con un
resoconto finale, poi si aspetta `CONTINUA` o `CHIUDI`.
Missione e risposta iniziano entrambe con `STATO PER LE PERSONE`; istruzioni e
dettagli tecnici vengono dopo.
```
