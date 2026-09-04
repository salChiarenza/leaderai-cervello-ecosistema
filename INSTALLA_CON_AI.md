# Autoconfigurazione sicura - Cervello + Ecosistema

Questa e' la procedura unica per una nuova installazione cliente. L'Ecosistema
Base su Google Drive e' lo standard LeaderAI corrente; l'agente del cliente lo
legge in sola lettura e applica localmente i file nella cartella madre.

Percorso predefinito: lettura del Base, creazione locale e collaudo. GitHub non
e' una fonte del cliente e non serve alcun clone. `leaderai_setup.py` resta un
attrezzo LeaderAI utilizzabile soltanto nella copia di lavoro locale.

REGOLA PER CHI CONSEGNA (LeaderAI): l'email di consegna e' corta e punta a
questa procedura. L'agente crea e prova tutto nella casa del cliente, promuove
stato e prove nelle fonti proprietarie e chiude localmente. Il ciclo ordinario
produce zero aggiornamenti intermedi. Quando la missione richiede una conferma
finale, ne parte una sola dopo il collaudo completo.

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
   Le regole `managed_text` devono coincidere col template; le regole
   `merge_hooks_json` uniscono il solo guardiano LeaderAI al JSON esistente,
   preservano tutte le altre chiavi e impediscono doppioni.
4. La fotografia puo' avere file protetti in sola lettura. La fonte resta
   intoccabile; dopo la copia rendi scrivibili soltanto i file creati nella
   cartella madre, prima di personalizzarli. Non cambiare mai i permessi della
   fotografia standard.
5. Per Claude in un collaudo isolato non toccare le user settings: registra
   `autoMemoryDirectory` come `DA COLLAUDARE`. Sulla macchina cliente lo
   configuri e lo provi seguendo la Fase 4. Lo stesso vale per le istruzioni
   globali dell'agente (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`): nel
   collaudo isolato restano `DA COLLAUDARE`, sulla macchina cliente si
   scrivono e si provano.
6. Inizializza Git locale. Prima del commit usa la allowlist dei file standard
   del contratto, rileggi lo staging e controlla nomi e contenuti per segreti.
   Il primo messaggio contiene la frase `installazione iniziale`.
7. Registra in `logs/install-log.md` standard/versione, modalita', prove
   strutturali e limiti. Le prove macchina differite restano nelle fonti
   proprietarie con il prossimo passo preciso.
8. Registra `default_browser`, `desktop_launcher`, `remote_backup` e
   `user_instructions_gate` come
   `DA COLLAUDARE` o `DA COLLEGARE` nel collaudo anonimo. Sulla macchina
   cliente diventano `OK` soltanto dopo prova reale.
9. Tratta `ecosistema/` come armadio comune ermetico: ammette soltanto i
   registri e i due calchi dichiarati dal contratto. I calchi
   `STANZA_AGENTS.md` e `STANZA_FONTE.md` restano file locali, integri e
   identici ai template della fotografia; nessun piano, bozza, asset o
   sottocartella operativa entra nell'armadio. Installa `ecosystem-check/`
   accanto all'armadio come prima stanza standard, completa di mappa, stato,
   standard, registro e ruoli; non inventare altre stanze business.
10. Verifica file obbligatori, file vietati del ramo opposto, ponte, memoria,
   log tecnico, commit iniziale e fotografia standard intatta. Prova anche il
   guardiano: casa pulita silenziosa, file di prova fuori posto bloccato e poi
   rimosso. In Codex esamina e autorizza il project hook da `/hooks`; in Claude
   verifica da `/hooks` che l'origine sia `Project`. La prova diretta dello
   script dimostra il controllo; soltanto questa verifica nella nuova sessione
   dimostra che l'agente lo ha realmente caricato.
11. Il nucleo passa solo con repository locale pulito e nessun file della copia di lavoro
   copiato nella casa.

<!-- END_NUCLEO_INSTALLAZIONE -->

## Missione operativa letta dall'agente

```text
Voglio configurare il mio Cervello + Ecosistema LeaderAI usando l'Ecosistema
Base su Google Drive come standard di sola lettura.

Ecosistema Base da usare:
https://drive.google.com/drive/folders/1POU01Ph15M1feSD_fRLQquZ1WbKjmfu6

Procedura da aprire:
https://drive.google.com/file/d/19l_f_VViewXaVVhq3in9KBnnqkoRyh7E/view

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
contiene gia' le "scelte fatte con Sal", applica direttamente le scelte e
registrale nelle fonti proprietarie. Se una scelta manca, usa il default
sicuro senza fermarti (cartella madre su disco locale; backup = repository
git locale, quello remoto si aggiunge dopo; niente seconda postazione) e
registra nello stato che il default e' modificabile. Le domande si fanno solo
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

Fase 3 - leggi lo standard corrente in sola lettura
1. Apri dall'Ecosistema Base su Google Drive questi file:
   - `VERSION`
   - `install_contract.json`
   - `MANIFEST.md`
   - `templates/AGENTS.md`
   - `templates/STANZA_AGENTS.md`
   - `templates/STANZA_FONTE.md`
   - `templates/ISPETTORE_SKILL.md`
   - `templates/MANUTENTORE_SKILL.md`
   - `templates/MEMORY.md`
   - `templates/ASSET.md`
   - `templates/GITIGNORE.txt`
   - `templates/CLAUDE.md`
   - `templates/CLAUDE_README.md`
   - `templates/CODEX_README.md`
   - `templates/FONTI.md`
   - `templates/PROCESSI.md`
   - `templates/LIMITI.md`
   - `templates/SOGGETTI.md`
   - `templates/CLAUDE_USER.md`
   - `templates/CODEX_USER_AGENTS.md`
   - `templates/INSTALL_LOG.md`
   - `templates/AGENT_CHAT.md`
   - `templates/GUARDIANO_STANZE.sh`
   - `templates/GUARDIANO_STANZE_WINDOWS.ps1`
   - `templates/CODEX_HOOKS.json`
   - `templates/CLAUDE_SETTINGS.json`
2. Registra nel log tecnico la versione letta. Se un file non e' leggibile, chiedi
   soltanto l'autorizzazione per l'accesso web di sola lettura e riprova.
3. Il percorso predefinito termina qui per la fonte: niente GitHub, niente clone
   e niente esecuzione di codice scaricato.

Fase 4 - monta localmente il Cervello
1. Crea le cartelle `memory/`, `logs/` ed `ecosistema/` nella cartella madre.
2. Usa `install_contract.json` come lista macchina unica dei template, dei file
   obbligatori e del ramo agente. Applica localmente i template, sostituendo
   `{{client_name}}`, `{{date}}`, `{{agent}}` e `{{version}}` con i dati reali
   letti dal Base:
   - `templates/AGENTS.md` -> `AGENTS.md`
   - `templates/MEMORY.md` -> `memory/MEMORY.md`
   - `templates/ASSET.md` -> `ecosistema/ASSET.md`
   - `templates/GITIGNORE.txt` -> `.gitignore`
   - `templates/FONTI.md` -> `ecosistema/FONTI.md`
   - `templates/PROCESSI.md` -> `ecosistema/PROCESSI.md`
   - `templates/LIMITI.md` -> `ecosistema/LIMITI.md`
   - `templates/SOGGETTI.md` -> `ecosistema/SOGGETTI.md`
   - `templates/STANZA_AGENTS.md` -> `ecosistema/STANZA_AGENTS.md`
   - `templates/STANZA_FONTE.md` -> `ecosistema/STANZA_FONTE.md`
   - `templates/INSTALL_LOG.md` -> `logs/install-log.md`
   - `templates/CLAUDE.md` -> `CLAUDE.md` (ponte, sempre)
   - `templates/AGENT_CHAT.md` -> `AGENT_CHAT.md` (chat di gruppo: bacheca
     comune di tutti gli agenti della casa, regole d'uso dentro al file)
   - `templates/GUARDIANO_STANZE.sh` ->
     `.agent/hooks/guardiano_stanze.sh`
   - `templates/GUARDIANO_STANZE_WINDOWS.ps1` ->
     `.agent/hooks/guardiano_stanze_windows.ps1`
   - modalita' Claude -> unisci `templates/CLAUDE_SETTINGS.json` a
     `.claude/settings.json`, senza cancellare chiavi o hook esistenti
   - modalita' Codex -> unisci `templates/CODEX_HOOKS.json` a
     `.codex/hooks.json`, senza cancellare chiavi o hook esistenti
   - modalita' Claude -> `templates/ISPETTORE_SKILL.md` in
     `.claude/skills/ispettore-ecosistema/SKILL.md`
   - modalita' Codex -> `templates/ISPETTORE_SKILL.md` in
     `.agents/skills/ispettore-ecosistema/SKILL.md`
   - modalita' both -> entrambe le skill, identiche e puntate allo stesso
     `CHECKUP.md`
   - allo stesso modo `templates/MANUTENTORE_SKILL.md` in
     `.claude/skills/manutentore-ecosistema/SKILL.md` (Claude) e/o
     `.agents/skills/manutentore-ecosistema/SKILL.md` (Codex): il Manutentore
     misura la casa ogni giorno con `guardiano_stanze.sh --misura`, ripara il
     meccanico (archivi datati, chat oltre 48 ore, skill gemelle) e riporta
   - crea l'automazione giornaliera `manutenzione-ecosistema` (07:45 locali,
     modello leggero) che invoca la skill `manutentore-ecosistema`: per Claude
     Code un task programmato, per Codex un'automazione; una sola sessione che
     chiude da sola
3. Crea SEMPRE `CLAUDE.md` dal template: e' il ponte di una riga (`@AGENTS.md`)
   che fa leggere la mappa anche a Claude Code, qualunque agente sia in uso
   oggi (Claude Code legge `CLAUDE.md`, Codex legge `AGENTS.md`). Poi la
   configurazione per agente: modalita' Claude -> `.claude/README.md`;
   modalita' Codex -> `.codex/README.md`. Usa entrambe le configurazioni solo
   se LeaderAI lo ha chiesto esplicitamente.
   Il guardiano di chiusura e' obbligatorio nel ramo attivo: una sola
   registrazione `Stop`, mai una seconda configurazione parallela.
3-bis. Su Windows, dopo ogni scrittura automatica dei registri, cerca nei file
   creati i percorsi `%USERPROFILE%\...` e verifica che i backslash siano
   intatti: gli strumenti di testo POSIX (sed, awk) li perdono in silenzio.
   Registra la prova nel log tecnico (caso reale del 03/09/2026).
4. Se Claude Code e' attivo, configura `autoMemoryDirectory` nelle user
   settings di ogni computer (`~/.claude/settings.json`) con la forma portabile
   `~/...` della memoria canonica dichiarata nell'`AGENTS.md` quando vive sotto
   la home di quella macchina. Usa un percorso assoluto soltanto dopo averlo
   letto sulla stessa macchina e soltanto se la memoria vive fuori dalla home.
   La chiave non e' valida nelle settings project/local. Accetta il trust del
   workspace e verifica ogni postazione con `/memory`. Se trovi una memoria
   auto esterna gia' piena, confronta e unisci le voci prima di cambiare il
   percorso.
4-bis. Istruzioni globali dell'agente attivo, su ogni computer del cliente:
   Claude Code legge `~/.claude/CLAUDE.md` in ogni sessione, Codex legge
   `~/.codex/AGENTS.md` (o `AGENTS.override.md` se esiste) in ogni task.
   Inserisci li' il blocco `LEADERAI-CASA` dal calco `templates/CLAUDE_USER.md`
   o `templates/CODEX_USER_AGENTS.md`, con il percorso portabile della
   cartella madre: se il file esiste, aggiungi o aggiorna soltanto il blocco
   tra i due marcatori e lascia intatto il resto. Senza questo blocco l'agente
   aperto da un'altra cartella non sa che la casa esiste e non puo' rispondere
   `FUORI DAL CERVELLO`. Prova subito: apri l'agente da una cartella estranea
   e verifica che rifiuti di scrivere e chieda di aprire la cartella madre.
5. Aggiorna direttamente le fonti proprietarie: stato operativo, memoria,
   asset, processi, limiti e storia tecnica restano nei rispettivi file.
6. Integra le sezioni mancanti dei file vivi e registra nel log tecnico cosa
   era gia' presente, cosa hai creato e cosa hai aggiornato.
7. Verifica che `.gitignore` escluda `.secrets/`, file `.env`, token, chiavi,
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

Prima di aggiungere una struttura business, costruisci la mappa dell'ambiente
reale come organigramma. L'agente nella cartella madre e' il Boss
dell'Ecosistema; ogni ramo organizzativo e' una stanza con il proprio
Amministratore di settore, subordinato al Boss:

1. censisci le cartelle, le fonti, gli output, le skill, gli script, gli agenti,
   i connettori, le procedure e gli archivi gia' presenti;
2. classifica ogni elemento rilevante come `STANZA`, `FONTE`, `OUTPUT`,
   `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`;
3. riconosci come stanza solo una responsabilita' business stabile con stato e
   decisioni propri;
4. aggiorna il registro delle stanze in `AGENTS.md`, assegna a ogni ramo il suo
   Amministratore di settore e collegalo al Boss dell'Ecosistema;
5. per ogni vera stanza crea nello stesso salvataggio `AGENTS.md` da
   `ecosistema/STANZA_AGENTS.md`, `CLAUDE.md` come ponte di una riga, una fonte
   operativa dal calco `ecosistema/STANZA_FONTE.md` con nome reale e la riga
   nella mappa madre; compila tutto e dichiara ogni sottocartella diretta;
6. collega direttamente due stanze solo quando un processo reale passa tra le
   due;
7. ripara ponti e puntatori tecnici rotti; per creare, fondere, rinominare,
   spostare o eliminare stanze presenta una proposta e attendi la decisione del
   proprietario. Finche' il percorso guidato LeaderAI e' `IN CORSO` (dalla
   installazione fino alla riga `PERCORSO GUIDATO CHIUSO` in
   `logs/install-log.md`), quella decisione si prende nella sessione con il
   consulente: la proposta resta nella fonte proprietaria come `DA DECIDERE IN
   CALL`, anche se il proprietario e' entusiasta.

Piu' soggetti giuridici, una casa. Se il proprietario governa piu' societa',
cooperative, associazioni o enti, censiscili in `ecosistema/SOGGETTI.md`, una
riga per soggetto: cosa fa davvero, chi lo amministra, quante persone, dove
vivono i documenti, se riceve fatture, stato. Compilare quella tabella con il
proprietario e' la prima discovery. Le stanze seguono le funzioni del lavoro
(amministrazione, personale, commerciale, progetti), non i soggetti: dentro
una stanza il soggetto diventa una sottocartella dichiarata solo dove la legge
o il lavoro lo separano davvero (fatture, dipendenti, bilanci). Una stanza per
soggetto nasce soltanto se quel soggetto ha processi propri che nessuna stanza
funzionale puo' ospitare. Sei societa' non fanno sei case ne' sei stanze.

Skill, script, agenti, connettori, moduli e procedure sono capacita' della
stanza che li usa. Se una capacita' e' gia' coperta, integrala o riusala. Una
nuova stanza nasce solo quando nessuna stanza esistente puo' possedere quella
funzione e il proprietario approva la proposta.

`ecosistema/` resta l'armadio comune: contiene soltanto i registri e i due
calchi dichiarati da `install_contract.json`. Le stanze e i loro materiali
business vivono accanto a esso. Un piano, una bozza, un asset o una cartella
operativa dentro `ecosistema/` blocca il collaudo.

Ogni cartella nuova passa lo stesso ciclo prima del salvataggio: classe,
proprietario, eventuale mappa locale, collegamento alla radice e prova. Nomi
generici come `documenti`, `output`, `exports`, `varie`, `misc`, `temp` o
`nuova cartella` restano `SOSPETTA` finche' non vengono ricondotti alla stanza
proprietaria. Un residuo vuoto o inutile creato dall'agente nello stesso
lavoro viene rimosso prima del commit; contenuti preesistenti si spostano,
fondono o eliminano solo dopo conferma.

La mappa madre nasce con `- Fase del percorso: 1 (Cervello)`. Non alzarla in
questa missione: la alza la missione LeaderAI che chiude ogni passo, di uno
alla volta (2 Censimento, 3 Prima stanza, 4 Ispettore e consegna). Sotto il
passo 3 il guardiano blocca ogni stanza di lavoro: oggi si censisce, non si
costruisce.

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
- OUTPUT NELLA CASA PROPRIETARIA: ogni analisi o documento finale vive nella
  stanza responsabile del processo e usa la casa esistente;
- CONTENUTI BUSINESS FUORI DAL CODICE: testi e regole che devo poter correggere
  vivono in una fonte esterna al codice; app e script la leggono e generano
  PDF/Word come derivati. Se la fonte manca, falliscono in modo visibile.

Mantieni anche la sezione "Comunicazione e fonti di verita'":
- gli agenti non si parlano direttamente, leggono e scrivono file condivisi;
- stato corrente, prossimo passo e scadenze: in testa al file proprietario
  della stanza; diario sotto, dal piu' recente;
- storia tecnica/strutturale: soltanto `logs/install-log.md`;
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
   Questa risposta arriva soltanto se le istruzioni globali del punto 4-bis
   sono al loro posto: un agente che da fuori casa lavora come se niente
   fosse dimostra che il blocco `LEADERAI-CASA` manca.
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
   ecosistema/LIMITI.md, ecosistema/SOGGETTI.md, logs/install-log.md.
   Verifica anche che ogni vera stanza abbia `AGENTS.md` + `CLAUDE.md` e che
   ogni `CLAUDE.md` contenga soltanto `@AGENTS.md`. Verifica che la mappa madre
   dichiari il Boss dell'Ecosistema e che ogni ramo, nuovo o preesistente,
   dichiari il proprio Amministratore di settore subordinato al Boss.
   `.claude/README.md` esiste solo in modalita' Claude o both;
   `.codex/README.md` esiste solo in modalita' Codex o both.
   Verifica anche le skill `ispettore-ecosistema` e `manutentore-ecosistema`
   nel percorso dell'agente attivo: `.claude/skills/` per Claude Code,
   `.agents/skills/` per Codex, entrambe in modalita' both; e l'automazione
   giornaliera `manutenzione-ecosistema` attiva.
   Se Claude e' attivo, verifica anche le user settings di ogni computer, trust
   del workspace e `/memory` sulla memoria canonica.
   Verifica su ogni computer le istruzioni globali dell'agente attivo
   (`~/.claude/CLAUDE.md` o `~/.codex/AGENTS.md`): blocco `LEADERAI-CASA`
   presente, percorso della cartella madre corretto, prova da cartella
   estranea superata.
2. Verifica che la cartella madre sia un repository git (esiste `.git`), che
   `.gitignore` escluda `.secrets/`, `*.env`, token, chiavi e credenziali, e che
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
9. Lancia l'Ispettore sul risultato, in una NUOVA sessione nata dalla cartella
   madre: e' l'ultimo passo obbligatorio dell'installazione, non un compito
   da rimandare alla prossima volta. La sessione che ha montato la casa chiude
   con lo stato salvato; quella nuova esegue l'Ispettore, prova le tre domande
   senza indizi e solo allora l'installazione e' chiusa. Censisci ogni
   cartella e file visibile nella home, classifica i percorsi, ripara i buchi
   sicuri e blocca il verdetto se restano cartelle generiche, vuote, doppie,
   tecniche, senza proprietario o stanze senza mappa. Registra la tabella
   `percorso | classe | amministratore | riporta al | mappa locale |
   collegamento radice | azione | prova`.
10. Confronta la versione in `AGENTS.md` con il `VERSION` appena letto: senza
    confronto o con valori diversi il verdetto e' `NON PASSA`.
11. Verifica: memoria unica; contenuti
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
  documenti, CRM/gestionale);
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

Per `compliance/privacy/AI Act`, censisci un sistema alla volta. Per ciascuno
registra nome, fornitore, uso previsto, ruolo dell'azienda e di LeaderAI,
persone coinvolte, preparazione di chi lo opera, eventuale decisione supportata, classe di rischio e obblighi
di trasparenza. Apri il Controllo di conformita' della Commissione e conserva
in `ecosistema/LIMITI.md` data, esito e presidio applicato. Un esito di pratica vietata, alto
rischio o dubbio sostanziale resta `NON PASSA` e blocca la consegna fino
all'approfondimento competente. `AI_ACT_CHECK_OK` vale soltanto per il sistema
e l'uso realmente esaminati.

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

Controlli di chiusura obbligatori, salvati nelle fonti proprietarie:
- `SITUAZIONE IN BREVE` in apertura, con `Cosa funziona`, `Cosa
  completiamo`, `Cosa serve da te` e `Quando si chiude` in parole semplici;
- cartella madre scelta e sua posizione (locale o cloud, come da Domanda 1);
- standard applicato: Ecosistema Base + versione letta;
- versione metodo registrata e versione precedente trovata, se esiste;
- modalita' accesso standard: sola lettura / percorso tecnico autorizzato;
- modalita' scelta: claude / codex / both;
- file creati;
- cartella madre = repository git si/no;
- `.gitignore` esclude i segreti si/no;
- memoria unica e, per Claude, prova `autoMemoryDirectory` + `/memory`;
- istruzioni globali dell'agente attivo con blocco `LEADERAI-CASA`, percorso
  della cartella madre e prova da cartella estranea (`user_instructions_gate`);
- soggetti giuridici censiti in `ecosistema/SOGGETTI.md`, stanze per funzione;
- guardiano di chiusura presente una sola volta, visibile in `/hooks`, con
  prova pulita e prova bloccante;
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
- per ogni sistema AI consegnato: controllo separato, ruolo, uso, persone
  coinvolte, preparazione di chi lo opera, classe di rischio, trasparenza,
  data, esito e presidio; il gate
  `AI_ACT_CHECK_OK` non viene riusato su sistemi o usi diversi;
- codice esterno eseguito: no / si con autorizzazione esplicita e prova;
- chiusura ambiente: email/browser/tab/app chiusi oppure handoff dichiarato;
- cosa resta da collegare e dove;
- `LEZIONE CANDIDATA`: nessuna oppure caso, causa, regola generale e prova che
  avrebbe intercettato l'errore;
- verdetto: PASSA / PASSA CON ATTENZIONE / NON PASSA.

Chiusura locale della missione:
1. Verifica il risultato che il proprietario vedra' e le prove salvate nelle
   fonti proprietarie.
2. Mostra al proprietario la conferma finale in parole comuni; il verdetto
   tecnico resta nelle fonti proprietarie.
3. Salva stato, prove, prossimo passo e scadenze nelle fonti proprietarie.
   Registra i gesti umani come `DA DECIDERE IN CALL`.
4. Archivia l'email della missione e chiudi pagine, tab, finestre e strumenti
   aperti per il lavoro.

Prima della chiusura fai `AUTOCONTROLLO`: rileggi missione, azioni fatte, prove,
file toccati, blocchi umani veri e superfici aperte da te (email, browser, tab,
form, preview, login, app temporanee). L'email della missione avvia un ciclo
che si chiude localmente; una conferma esterna parte soltanto quando Sal la
richiede nella missione.

La missione deve darti istruzioni precise, fonti, risultato atteso, azioni
autorizzate e criteri di riuscita. Esegui, diagnostica, ripara, riprova e
completa in autonomia, evitando aggiornamenti di avanzamento e richieste a
puntate. Fermati una sola volta soltanto quando serve un gesto che puo'
compiere il proprietario. Nel messaggio visibile scrivi:

`SERVE UN TUO PASSAGGIO`

`Ho gia' sistemato: [cosa e' stata completata]`

`Mi serve da te: [un solo dato, accesso, permesso o decisione]`

`Appena lo fai: riprendo e completo il lavoro.`

Dopo la risposta riprendi la stessa missione e completala. Le classificazioni
tecniche restano nelle fonti della casa.

Quando Sal richiede espressamente una conferma finale, inviala una volta sola
quando tutti i criteri della missione, compreso il processo reale e la
riapertura del contesto, sono completati e provati, cioe' soltanto con
verdetto `PASSA` pieno. Apri con
`Perfetto, l'ho fatto. Tutto completato e funzionante.` e aggiungi le prove
essenziali. Con `PASSA CON ATTENZIONE` la conferma non parte: lo stato resta
nella casa e, se serve un gesto del proprietario, il solo messaggio ammesso
e' `SERVE UN TUO PASSAGGIO`. Un rapporto lungo con collaudo incompleto non e'
una conferma. Ogni stato intermedio resta nella casa e alimenta
l'auto-riparazione della stessa missione.

Regola stabile: ogni email di missione da LeaderAI si ESEGUE, si ripara tutto
cio' che si puo' riparare, si prova, si fa autocontrollo, si salva nella casa e
si chiude localmente.
`PASSA CON ATTENZIONE` contiene soltanto decisioni o gesti umani veri: ogni
azione eseguibile dall'agente viene completata e provata prima della chiusura.
La missione inizia con `SITUAZIONE IN BREVE`; le classificazioni e i dettagli
tecnici restano nelle fonti della casa.
```
