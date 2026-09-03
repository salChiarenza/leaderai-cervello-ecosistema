# Manifest LeaderAI Cervello + Ecosistema

## Obiettivo

Portare una cartella cliente a uno standard minimo operativo:

1. Fase 1 - Cervello: istruzioni, memoria unica, log tecnico e agenti.
2. Fase 2 - Ecosistema: fonti reali, processi, limiti, decisioni.

## Ruolo del Manifest

Questo file e' lo standard di conformita' della repo `salChiarenza/leaderai-cervello-ecosistema`.

La cartella viva del cliente e' il caso reale. Il checkup non giudica a
sensazione: confronta il caso reale con questo Manifest, con
`templates/AGENTS.md`, `templates/STANZA_AGENTS.md`,
`templates/STANZA_FONTE.md` e con le istruzioni
operative della repo. Se qualcosa manca, e' fuori standard: l'agente lo ripara,
lo prova e aggiorna la fonte proprietaria.

`install_contract.json` traduce questo standard nel contratto macchina del
nucleo d'installazione. La procedura manuale, `leaderai_setup.py`, l'Ispettore
e il collaudo non mantengono liste concorrenti. Browser, launcher e backup
remoto sono controlli d'ambiente dichiarati nel contratto: si provano sulla
macchina cliente e restano `DA COLLAUDARE` nel gate anonimo.

## Regola

L'agente non deve fare un esame al cliente.

Deve:

1. leggere questa repo;
2. montare i pezzi standard mancanti;
3. non sovrascrivere cio' che esiste;
4. collaudare;
5. salvare i fatti nelle fonti proprietarie e chiudere con una conferma unica.

## Contratto architetturale adattivo

La repo insegna **come leggere e governare** un Ecosistema. Il nome e il numero
delle stanze nascono dal lavoro reale del proprietario.

### Telaio universale

Restano stabili in ogni installazione:

- una sola cartella madre viva;
- `AGENTS.md` alla radice come mappa e router comune;
- `CLAUDE.md` sempre presente come ponte di una riga (`@AGENTS.md`);
- memoria indicizzata, log e registri di fonti, asset, processi e limiti;
- calchi locali `ecosistema/STANZA_AGENTS.md` e
  `ecosistema/STANZA_FONTE.md` per creare stanze complete senza dipendere da
  un percorso esterno;
- Ispettore Ecosistema richiamabile dall'agente attivo;
- guardiano deterministico di chiusura, comune ai due agenti: la casa pulita
  chiude in silenzio; un percorso fuori contratto obbliga l'agente a
  continuare una volta e il secondo passaggio non crea un ciclo infinito;
- audit comportamentale delle istruzioni con una sola variazione per volta,
  due sessioni nuove e classificazione non distruttiva del blocco;
- ingresso verificato: cartella madre come progetto primario/CWD e nuova
  task/sessione che legge la mappa prima del lavoro;
- istruzioni globali dell'agente attivo su ogni computer (`~/.claude/CLAUDE.md`
  per Claude Code, `~/.codex/AGENTS.md` per Codex) con il blocco `LEADERAI-CASA`:
  nominano la cartella madre e fanno rispondere `FUORI DAL CERVELLO` a una
  sessione nata altrove;
- anagrafe dei soggetti giuridici in `ecosistema/SOGGETTI.md`: piu' soggetti,
  una casa, stanze per funzione;
- fase del percorso guidato dichiarata nella mappa madre (`Fase del percorso:
  N`): 1 Cervello, 2 Censimento, 3 Prima stanza, 4 Ispettore e consegna; sale
  di un passo alla volta con la missione che chiude il passo e sotto il 3 il
  guardiano blocca ogni stanza di lavoro;
- chat di gruppo letta all'avvio e handoff tracciati tra sessioni distinte;
- versione del metodo applicato e prove di collaudo.

La versione installata vive nell'`AGENTS.md` della cartella madre. Ogni
Ispettore legge anche il `VERSION` della repo ufficiale aggiornata e blocca il
verdetto se non puo' confrontare i due valori o se non coincidono.

Per Claude Code esiste una sola memoria. `autoMemoryDirectory` viene impostato
nelle **user settings** di ciascun computer (`~/.claude/settings.json`), oppure
da policy o `--settings`: la documentazione ufficiale non accetta questa chiave
nelle settings project/local. La documentazione ammette due forme, "an absolute
path or start with `~/`": **lo standard LeaderAI prescrive la forma `~/`**, per
esempio `~/OneDrive/Desktop/<Cartella madre>/_claude-memory`. Una sola stringa
vale su tutte le postazioni del cliente e si risolve sull'utente del computer
corrente. `/memory` deve confermare la destinazione su ogni postazione. Se
esiste una memoria auto esterna, le voci si confrontano e si uniscono prima di
cambiare il percorso.

### Percorsi d'ambiente: forma portabile, mai copiati da un'altra macchina

Vale per ogni percorso, nome utente, lettera di disco o valore di ambiente che
finisce in un'istruzione, una missione, un'email o una configurazione destinata
al computer del cliente.

- Si usa la forma che si risolve sull'ambiente corrente: `~/` nelle settings
  degli agenti, `%USERPROFILE%` su Windows, `$HOME` su Unix.
- Un percorso assoluto si scrive solo dopo averlo letto sulla macchina di
  destinazione, dichiarando a quale macchina appartiene.
- **Divieto:** riproporre su una macchina un percorso letto su un'altra. Il
  segmento utente, la lettera di disco e la radice del cloud cambiano per
  computer, e installazioni su cloud sincronizzato con utenti diversi sono la
  norma.
- Prima di dettare un percorso, l'agente apre i file dell'ambiente che gia'
  contengono la risposta: `.claude/settings.local.json`, `ecosistema/FONTI.md`,
  i log di installazione.

Motivo: un percorso sbagliato non produce alcun errore visibile. La memoria
punta a una cartella inesistente, l'agente riparte vuoto e il cliente scopre il
guasto da una risposta sbagliata. Caso di origine anonimizzato: due postazioni
con nomi utente diversi e percorso assoluto replicato sul portatile.

### Forma adattiva

Prima di creare, rinominare, fondere o spostare una cartella, l'agente censisce
l'ambiente e classifica ogni elemento rilevante come:

- `STANZA`: responsabilita' business stabile riconosciuta dal proprietario,
  che mantiene stato, decisioni e lavoro corrente;
- `FONTE`: luogo da cui si leggono dati o documenti;
- `OUTPUT`: risultato prodotto da una o piu' stanze;
- `CAPACITA`: skill, script, agente, connettore, modulo o procedura;
- `INFRASTRUTTURA`: supporto tecnico del Cervello;
- `ARCHIVIO`: materiale storico non operativo;
- `SOSPETTA`: elemento ancora da chiarire.

Piu' soggetti giuridici, una casa: societa', cooperative, associazioni ed enti
governati dal proprietario vivono come righe di `ecosistema/SOGGETTI.md`. Le
stanze seguono le funzioni del lavoro, non i soggetti; un soggetto separa una
stanza in sottocartelle dichiarate solo dove la legge o il lavoro lo impongono,
e ottiene una stanza propria soltanto con processi che nessuna stanza
funzionale puo' ospitare.

La cartella `ecosistema/` e' l'armadio comune della casa, non una stanza
business: contiene soltanto i registri e i calchi installati dal contratto.
Piani, bozze, asset visivi, progetti e cartelle operative vivono nella stanza
proprietaria, allo stesso livello di `ecosistema/`. Qualunque elemento diverso
dai percorsi ammessi da `install_contract.json` blocca il collaudo.

L'insieme forma un organigramma. La cartella madre e' governata dal **Boss
dell'Ecosistema**, che instrada richieste, coordina i passaggi tra settori e
verifica il risultato. Ogni `STANZA` e' un ramo organizzativo governato dal
proprio **Amministratore di settore** e riporta al Boss. La regola vale sia per
i rami nuovi sia per quelli gia' esistenti scoperti dall'Ispettore. Cartelle di
supporto, skill, fonti e output restano subordinate al settore proprietario e
non ricevono un amministratore artificiale.

Una vera stanza passa il contratto quando:

1. dichiara quale responsabilita' business possiede, quali decisioni mantiene
   e quale stato operativo governa;
2. dichiara il proprio Amministratore di settore e il collegamento gerarchico
   al Boss dell'Ecosistema;
3. e' raggiungibile dalla mappa madre;
4. nasce come prefabbricato completo: `AGENTS.md`, ponte `CLAUDE.md`, una
   fonte operativa nominata e compilata, riga nella mappa madre e collaudo;
5. dichiara nella mappa ogni sottocartella diretta e la sua funzione;
6. dichiara collegamenti a monte e a valle solo per processi reali;
7. usa una sola fonte di verita' per ogni dato o stato;
8. registra le capacita' che la servono e la prova che funzionano.

Script, skill, modelli, fonti e output possono formare una pipeline completa
senza costituire una stanza. Descrivono **come** si esegue un lavoro; la stanza
descrive **chi possiede la responsabilita' business**. Un nome di prodotto o
di lavorazione, per esempio `Portafoglio Modello`, resta `CAPACITA` o
`SOSPETTA` finche' il proprietario non dimostra che e' anche una funzione
business autonoma con stato e decisioni propri. In dubbio il gate e'
`NON PASSA`: l'agente non crea la mappa locale e non inventa una stanza.

Ogni casa ha la stanza standard `Ecosystem Check`, installata accanto a
`ecosistema/`: mantiene stato e decisioni dei controlli, separa osservazione,
intervento e verifica finale e conserva un registro compatto. Una casa semplice
puo' avere **zero stanze business oltre a Ecosystem Check**. Quando una capacita', fonte o
output non appartiene a una responsabilita' business autonoma, la cartella
madre puo' possederlo direttamente: lo registra nell'`AGENTS.md` radice e in
`ecosistema/ASSET.md` o `ecosistema/FONTI.md`. Una casa consolidata (statuti
propri nati prima dello standard) dichiara `- Contratto di stanza: consolidato`
e tiene le sue mappe: l'Ispettore controlla ponte, mappa e riga madre, non il
calco a 14 sezioni. Una casa consolidata che ha gia'
un'anagrafe propria dichiara nella mappa madre `- Registro di dettaglio canonico:
`percorso.md`` e usa quella, senza creare registri doppi. In questo caso non nasce una
mappa locale. Il percorso e' un elemento visibile direttamente nella radice,
l'uso e' compilato e non collide con il telaio o con una stanza. La crescita
futura puo' promuoverlo a stanza solo quando emerge
una responsabilita' business reale approvata dal proprietario.

Il contratto macchina vive in
`install_contract.json -> inspection_policies -> room_lifecycle`. I calchi
repo `templates/STANZA_AGENTS.md` e `templates/STANZA_FONTE.md` vengono
installati nell'armadio comune; `templates/ecosystem-check/` e' il prefabbricato
della stanza di controllo. Una stanza e' valida soltanto quando l'intero
prefabbricato e' presente nello stesso salvataggio; una nascita parziale viene
annullata o resta `NON PASSA`.
Lo stesso contratto viene controllato a ogni chiusura da
`.agent/hooks/guardiano_stanze.sh`, registrato una sola volta nel ramo attivo.
I JSON di Codex e Claude vengono uniti alle configurazioni del cliente e non
le sostituiscono. Codex richiede la verifica e l'autorizzazione del project
hook da `/hooks`; Claude deve mostrarlo da `/hooks` con origine `Project`.
Le cartelle ordinarie non ricevono mappe inutili: vivono sotto la stanza che le
governa. Una cartella generica, vuota, concorrente o senza proprietario blocca
il collaudo.

Le cartelle ordinarie non diventano automaticamente stanze. Skill, script e
moduli restano capacita' collegate alla cartella madre o alla stanza
proprietaria. Una nuova stanza viene proposta solo quando emerge una
responsabilita' business autonoma con stato e decisioni propri.

Riparazioni meccaniche come ponti rotti, puntatori mancanti e registri non
allineati possono essere applicate e provate. Spostamenti, fusioni, nuove
stanze, eliminazioni e cambi di proprieta' restano una `PROPOSTA STRUTTURALE`
da approvare.

### Unicita' delle fonti e ciclo di vita

- Stato business corrente, prossimo passo e scadenze vivono in testa al file
  proprietario della stanza; il diario viene dopo, dal piu' recente.
- `logs/install-log.md` registra soltanto installazione, versione e cambi
  strutturali. Non e' il diario della produzione business.
- Ogni missione aggiorna direttamente le fonti proprietarie: stato operativo,
  memoria stabile, asset, processi, limiti e storia tecnica restano separati.
- Tutti i Markdown vengono misurati con le soglie uniche di
  `install_contract.json`. Mappe e indici (`AGENTS.md`, `MEMORY.md`,
  `AGENT_CHAT.md`) restano router corti: oltre 350 righe o 24 KiB il gate e'
  `NON PASSA`. Gli altri documenti entrano in revisione oltre 800 righe o
  80 KiB: se restano una fonte unica e coerente possono essere mantenuti con
  un indice; se mescolano responsabilita' o duplicano stato vengono ricondotti
  alle fonti proprietarie.
- Il contenuto business modificabile vive in una fonte esterna al codice,
  dichiarata nella stanza. App e script generano PDF/Word come derivati e
  falliscono visibilmente se la fonte manca; nessuna copia hardcoded silenziosa.
- Configurazioni con credenziali, app password o token vivono in `.secrets/`.
  L'Ispettore controlla percorso, indice e history Git senza aprire il
  contenuto; propone rotazione quando l'esposizione non puo' essere esclusa.
- Firma, timbro e sigillo sono asset ad alto rischio: file protetto fuori Git,
  soli metadati e limiti in `ecosistema/ASSET.md`, uso sul singolo documento
  soltanto con conferma umana.

### Ciclo di apprendimento

Ogni installazione e checkup registra la versione letta da `VERSION`. Un errore
osservato sul cliente viene riparato nello stesso turno quando e' sicuro e
diventa una `LEZIONE CANDIDATA` in `ecosistema/PROCESSI.md`: caso, causa, riparazione, regola
generale e prova che avrebbe intercettato l'errore. LeaderAI valida la lezione,
aggiorna questa repo con regola e test e la rende disponibile ai checkup
successivi. In questo modo i problemi quotidiani gia' incontrati entrano nel
metro; un problema nuovo non viene finto come noto in anticipo.

## Contratto di consegna sicura

Per una nuova installazione l'agente usa la repo ufficiale come fonte di sola
lettura e applica i template nella cartella madre locale. Il clone della repo e
l'esecuzione di `leaderai_setup.py` richiedono una autorizzazione esplicita e
separata; non sono il percorso predefinito e non si attivano automaticamente se
la lettura web incontra un blocco.

Installazione manuale e setup tecnico devono produrre lo stesso telaio per la
stessa modalita'. Il rilascio lo prova in una cartella vuota con percorso
difficile, usando una sessione reale che riceve soltanto la procedura e lo
standard statico.

Ogni email operativa agente-agente apre con `SITUAZIONE IN BREVE`: `Cosa
funziona`, `Cosa completiamo`, `Cosa serve da te`, `Quando si chiude`. Le
classificazioni e le prove tecniche restano nelle fonti proprietarie. La
conferma finale vive nel messaggio conclusivo.

L'email della missione e' l'unico messaggio del ciclo ordinario. L'agente crea
e prova tutto nella casa del cliente, salva stato e prove nelle fonti
proprietarie e chiude localmente. Decisioni e gesti umani veri restano come
`DA DECIDERE IN CALL`; una conferma esterna parte soltanto quando Sal la
richiede nella missione.

Regola dell'unico passaggio umano: l'agente esegue istruzioni precise,
diagnostica, ripara, riprova e completa in autonomia. Si ferma una sola volta
soltanto quando serve un gesto che puo' compiere il proprietario. Nello stesso
canale scrive `SERVE UN TUO PASSAGGIO`, cosa ha gia' sistemato, il solo gesto
richiesto e `Appena lo fai: riprendo e completo il lavoro.` Dopo la risposta
riprende la stessa missione. Le classificazioni tecniche restano nella casa.

Un primo tentativo fallito non autorizza il passaggio del lavoro alla persona.
Prima di dichiarare un limite l'agente separa capacita', autorizzazione e
perimetro predefinito, controlla le fonti vive della casa, diagnostica e
riprova. Un `non posso` valido registra percorso provato, data e prova
osservabile; una prova successiva che lo smentisce rende il verdetto storico
`SUPERATO` e aggiorna la fonte proprietaria.

Se Sal richiede espressamente una conferma finale, parte una volta sola quando
tutti i criteri sono completati e provati. La
conferma apre con `Perfetto, l'ho fatto. Tutto completato e funzionante.`; ogni
stato intermedio resta nella casa del cliente.

Il modello unico della prima email vive in `EMAIL_CONSEGNA.md`; procedure,
README e Manifest lo richiamano senza duplicarne il corpo.

## Modalita' agente

La repo resta unica. La cartella madre e ogni vera stanza mantengono sempre il
telaio comune `AGENTS.md` + `CLAUDE.md`. La modalita' seleziona soltanto la
configurazione specifica dell'agente reale del cliente:

- Claude Code -> `--agent claude`
- Codex -> `--agent codex`
- Entrambi -> `--agent both`, solo su richiesta esplicita LeaderAI

`--agent claude` governa `.claude/`, `--agent codex` governa `.codex/` e
`--agent both` governa entrambe. Nessuna modalita' rimuove o rende facoltativo
il telaio comune.

## Standard minimo

Il target passa solo se esistono:

- `.gitignore` che esclude i segreti (`.secrets/`, `*.env`, token, chiavi, credenziali)
- la cartella madre e' un repository git (nella posizione scelta col cliente, locale o cloud; sul cloud vale l'avviso sul rischio corruzione)
- `AGENTS.md`
- `CLAUDE.md` (ponte di una riga `@AGENTS.md`, sempre presente)
- `memory/MEMORY.md`
- `logs/install-log.md`
- `AGENT_CHAT.md` (chat di gruppo degli agenti della casa)
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `ecosistema/SOGGETTI.md`
- `ecosistema/STANZA_AGENTS.md`
- `ecosistema/STANZA_FONTE.md`

Lo standard statico necessario alla procedura senza esecuzione di codice e'
esposto in `templates/` e la sua versione e' dichiarata in `VERSION`.

Per Claude Code:

- `.claude/README.md`
- `.claude/skills/ispettore-ecosistema/SKILL.md`
- `.claude/skills/manutentore-ecosistema/SKILL.md`
- `autoMemoryDirectory` nelle user settings di ogni computer
  (`~/.claude/settings.json`), **in forma portabile `~/`** verso la memoria
  canonica dichiarata nella mappa madre, con prova `/memory` su ogni postazione
- blocco `LEADERAI-CASA` in `~/.claude/CLAUDE.md` di ogni computer, con il
  percorso della cartella madre e il gate `FUORI DAL CERVELLO`, provato da una
  cartella estranea

Per Codex:

- `.codex/README.md`
- `.agents/skills/ispettore-ecosistema/SKILL.md`
- `.agents/skills/manutentore-ecosistema/SKILL.md`
- Codex Desktop con cartella madre come progetto locale primario oppure Codex
  CLI avviato con la cartella madre come `-C`/directory corrente
- blocco `LEADERAI-CASA` in `~/.codex/AGENTS.md` (o `AGENTS.override.md` se
  esiste) di ogni computer, provato da una cartella estranea

## Gate di rilascio del prodotto

La suite deterministica passa soltanto con almeno un test eseguito, zero errori
e zero test saltati. Il gate completo richiede inoltre:

1. una sessione Codex reale e una sessione Claude Code reale;
2. due richieste business anonime senza suggerire file o percorsi;
3. instradamento dalla mappa madre alla stanza, alla fonte e all'output;
4. nessuna contaminazione tra stanze o scrittura nella fonte storica;
5. installazione manuale reale per entrambi gli agenti, senza clone, Python o
   `leaderai_setup.py`;
6. cartella finale conforme, repository Git pulito e prove conservate;
7. stato bloccante per CLI assente, login mancante, timeout o oracolo fallito.
8. richiesta esatta `Crea la Brand Identity`, senza indizi tecnici nel prompt,
   con fonte brand reale e output nella responsabilita' proprietaria.

I controlli macchina `default_browser`, `desktop_launcher`, `remote_backup` e
`user_instructions_gate`
sono dichiarati in `install_contract.json`. Il gate anonimo verifica che
restino esplicitamente `DA COLLAUDARE`; il loro `OK` nasce soltanto dalla prova
sulla macchina cliente.

Comando unico:

```bash
python3 -m tests.gate --release --agents codex,claude
```

## Moduli professionali

I moduli entrano nel target soltanto quando LeaderAI li assegna al cliente.
`MODULO_CALENDARIO_OPERATIVO.md` e il Sistema Portafogli sono capacita'
opzionali: non fanno parte del telaio minimo.

### Sistema Portafogli Core-Satellite

Sorgente: `moduli/portafogli/`.

Il modulo passa quando:

- viene integrato nella cartella madre o nella stanza proprietaria scelta dopo
  il censimento;
- richiede conferma esplicita per creare una stanza quando emerge una nuova
  responsabilita' business autonoma;
- preserva `METODO.md`, `FONTI.md` e `CORE.md` ai rilanci;
- riusa una capacita' esistente quando copre gia' il lavoro; una nuova skill si
  installa solo dopo una scelta esplicita di nome e perimetro;
- registra l'asset e il processo nell'Ecosistema cliente;
- applica `VERIFICA_FINANZIARIA.md` ogni volta che compaiono numeri finanziari
  o strumenti e separa stato del prodotto da collocabilita';
- calcola pesi, drift, riallineamento, alert e backtest dai CSV normalizzati;
- blocca target fuori universo e serie mensili incomplete;
- produce `ESITO SOSPESO` quando identita', stato, collocabilita', fonte o
  calcolo di un elemento critico non sono verificati;
- produce un dossier tracciabile che il banker valida prima del report cliente.

## Fonti ufficiali da tenere vive

Le tre fonti principali sono dichiarate anche in
`install_contract.json -> official_sources`: fanno parte del metro macchina
dell'Ispettore. A ogni checkup l'agente le apre, raggiunge le pagine tecniche
pertinenti e registra regola, stato osservato, scostamento, riparazione e prova.
Queste fonti vanno riverificate quando si aggiorna lo standard:

- Claude Code, panoramica ufficiale:
  [https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)
- ChatGPT, documentazione ufficiale:
  [https://learn.chatgpt.com/docs](https://learn.chatgpt.com/docs)
- OpenAI Academy, Codex per il lavoro:
  [https://openai.com/it-IT/academy/codex-for-work/](https://openai.com/it-IT/academy/codex-for-work/)
- Claude Code, indice completo per agenti: `https://code.claude.com/docs/llms.txt`
  (ogni pagina in markdown puro col suffisso `.md` — e' il meccanismo usato da
  `CHECKUP.md` per confrontare il setup con la doc viva)
- OpenAI Codex AGENTS.md: `https://developers.openai.com/codex/guides/agents-md`
- OpenAI Codex hooks: `https://developers.openai.com/codex/hooks`
- Claude Code memory: `https://code.claude.com/docs/en/memory`
- Claude Code hooks: `https://code.claude.com/docs/en/hooks`

## Criterio di finito

Il pacchetto e' pronto quando:

- crea una cartella target da zero;
- puo' essere rilanciato senza duplicare file;
- produce il log tecnico e aggiorna le fonti proprietarie;
- i test automatici passano;
- la cartella madre e ogni vera stanza hanno `AGENTS.md` + `CLAUDE.md`, con
  `CLAUDE.md` ridotto al solo ponte `@AGENTS.md`;
- una nuova chat dell'agente sa leggere la mappa e dove salvare memoria, stato e prove.
- la mappa madre raggiunge ogni stanza operativa e nessuna capacita' resta
  isolata o promossa a stanza per abitudine.
- il Boss dell'Ecosistema e' dichiarato alla radice e ogni ramo organizzativo,
  nuovo o vecchio, ha un Amministratore di settore che riporta al Boss;
- l'Ispettore ha censito ogni cartella e file visibile nella home e non restano
  percorsi senza classe e proprietario, cartelle generiche o vuote, doppioni,
  stanze senza mappa o file sciolti senza casa;
- la versione installata coincide con il `VERSION` vivo e Claude usa una sola
  memoria;
- le istruzioni globali dell'agente attivo nominano la cartella madre e la
  prova da cartella estranea risponde `FUORI DAL CERVELLO`;
- i soggetti giuridici del proprietario hanno una riga in
  `ecosistema/SOGGETTI.md` e nessuna stanza nasce per replicare l'organigramma
  giuridico;
- la conferma finale, quando richiesta, parte soltanto con verdetto `PASSA`
  pieno: con `PASSA CON ATTENZIONE` resta nella casa e chiede al massimo un
  passaggio umano;
- contenuti business modificabili, credenziali, firma/timbro e file progetto
  rispettano il contratto di unicita', protezione e ordine;
- mappe e indici Markdown rispettano le soglie macchina; ogni documento esteso
  e' stato ricondotto a una sola responsabilita' e fonte viva;
- almeno due prove di instradamento partono dalla radice e arrivano alla
  madre/stanza, alla fonte e all'output corretti senza suggerire il percorso
  all'agente.
- ogni blocco di istruzioni sospetto e' confrontato, uno alla volta, tra
  contesto completo e alleggerito; il log tecnico misura gli effetti e li classifica
  senza rimuovere automaticamente sicurezza, privacy, autorizzazione o
  integrita';
- le fonti proprietarie registrano versione del metodo, classificazione delle
  stanze, collegamenti e possibili lezioni candidate;
- lo stato distingue Fase 1 Cervello creata/testata da Fase 2 Ecosistema da
  collegare con fonti reali;
- ogni nuovo asset operativo ha casa/fonte vera, riga in `ecosistema/ASSET.md`
  e solo i processi/limiti necessari aggiornati.
- `AGENTS.md` include la mappa comunicazione:
  procedure e stato business nei file proprietari, storia tecnica nel log,
  asset in `ecosistema/ASSET.md`, chat solo temporanea e sync dedicato solo se
  esistono due agenti.
- `ecosistema/ASSET.md` mantiene una mappa moduli con stato per PEC/email certificata,
  email/calendario, calendario operativo, Drive/OneDrive, CRM/gestionale,
  plugin, skill, agenti, guardiani/hook, ronde, voce/dettatura e
  compliance/privacy/AI Act.
- l'agente chiude l'ambiente operativo usato: email/notifiche lavorate
  archiviate nello stesso giro o dichiarate in handoff, pagine web/tab/form/preview/login/app
  aperti da lui chiusi se non servono piu'.
