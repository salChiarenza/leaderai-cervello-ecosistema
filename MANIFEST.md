# Manifest LeaderAI Cervello + Ecosistema

## Obiettivo

Portare una cartella cliente a uno standard minimo operativo:

1. Fase 1 - Cervello: istruzioni, memoria, log, agenti, report.
2. Fase 2 - Ecosistema: fonti reali, processi, limiti, decisioni.

## Ruolo del Manifest

Questo file e' lo standard di conformita' della repo `salChiarenza/leaderai-cervello-ecosistema`.

La cartella viva del cliente e' il caso reale. Il checkup non giudica a
sensazione: confronta il caso reale con questo Manifest, con
`templates/AGENTS.md`, `templates/STANZA_AGENTS.md` e con le istruzioni
operative della repo. Se qualcosa manca, e' fuori standard: l'agente lo ripara
se puo', lo prova e lo dichiara nel report.

## Regola

L'agente non deve fare un esame al cliente.

Deve:

1. leggere questa repo;
2. montare i pezzi standard mancanti;
3. non sovrascrivere cio' che esiste;
4. collaudare;
5. scrivere un report finale.

## Contratto architetturale adattivo

La repo insegna **come leggere e governare** un Ecosistema. Il nome e il numero
delle stanze nascono dal lavoro reale del proprietario.

### Telaio universale

Restano stabili in ogni installazione:

- una sola cartella madre viva;
- `AGENTS.md` alla radice come mappa e router comune;
- `CLAUDE.md` sempre presente come ponte di una riga (`@AGENTS.md`);
- memoria indicizzata, log e registri di fonti, asset, processi e limiti;
- Ispettore Ecosistema richiamabile dall'agente attivo;
- versione del metodo applicato e prove di collaudo.

### Forma adattiva

Prima di creare, rinominare, fondere o spostare una cartella, l'agente censisce
l'ambiente e classifica ogni elemento rilevante come:

- `STANZA`: funzione operativa stabile, con fonti o processi propri;
- `FONTE`: luogo da cui si leggono dati o documenti;
- `OUTPUT`: risultato prodotto da una o piu' stanze;
- `CAPACITA`: skill, script, agente, connettore, modulo o procedura;
- `INFRASTRUTTURA`: supporto tecnico del Cervello;
- `ARCHIVIO`: materiale storico non operativo;
- `SOSPETTA`: elemento ancora da chiarire.

Una vera stanza passa il contratto quando:

1. e' raggiungibile dalla mappa madre;
2. ha una mappa corta alla porta: `AGENTS.md` come fonte unica e `CLAUDE.md`
   come ponte `@AGENTS.md`, con scopo, fonti, output e modo di muoversi;
3. dichiara collegamenti a monte e a valle solo per processi reali;
4. usa una sola fonte di verita' per ogni dato o stato;
5. registra le capacita' che la servono e la prova che funzionano.

Il contratto locale nasce da `templates/STANZA_AGENTS.md`. Ogni cartella nuova
viene classificata e assegnata a una stanza proprietaria prima del salvataggio.
Le cartelle ordinarie non ricevono mappe inutili: vivono sotto la stanza che le
governa. Una cartella generica, vuota, concorrente o senza proprietario blocca
il collaudo.

Le cartelle ordinarie non diventano automaticamente stanze. Skill, script e
moduli restano capacita' collegate alla stanza proprietaria. Se nessuna stanza
esistente puo' possederli, l'agente presenta una proposta con funzione, fonti,
output, collegamenti e collaudo; il proprietario decide se nasce una stanza.

Riparazioni meccaniche come ponti rotti, puntatori mancanti e registri non
allineati possono essere applicate e provate. Spostamenti, fusioni, nuove
stanze, eliminazioni e cambi di proprieta' restano una `PROPOSTA STRUTTURALE`
da approvare.

### Ciclo di apprendimento

Ogni installazione e checkup registra la versione letta da `VERSION`. Un errore
osservato sul cliente diventa una `LEZIONE CANDIDATA` nel report: caso, causa,
regola generale e prova che avrebbe intercettato l'errore. LeaderAI valida la
lezione, aggiorna questa repo con regola e test e la rende disponibile ai
checkup successivi.

## Contratto di consegna sicura

Per una nuova installazione l'agente usa la repo ufficiale come fonte di sola
lettura e applica i template nella cartella madre locale. Il clone della repo e
l'esecuzione di `leaderai_setup.py` richiedono una autorizzazione esplicita e
separata; non sono il percorso predefinito e non si attivano automaticamente se
la lettura web incontra un blocco.

Il report viene prima creato e collaudato localmente. L'invio email a LeaderAI
avviene dopo autorizzazione esplicita del proprietario.

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
- `REPORT_FINALE.md`

Lo standard statico necessario alla procedura senza esecuzione di codice e'
esposto in `templates/` e la sua versione e' dichiarata in `VERSION`.

Per Claude Code:

- `.claude/README.md`
- `.claude/skills/ispettore-ecosistema/SKILL.md`

Per Codex:

- `.codex/README.md`
- `.agents/skills/ispettore-ecosistema/SKILL.md`

## Moduli professionali

I moduli entrano nel target soltanto quando LeaderAI li assegna al cliente.
`MODULO_CALENDARIO_OPERATIVO.md` e il Sistema Portafogli sono capacita'
opzionali: non fanno parte del telaio minimo.

### Sistema Portafogli Core-Satellite

Sorgente: `moduli/portafogli/`.

Il modulo passa quando:

- viene integrato nella stanza proprietaria scelta dopo il censimento;
- richiede conferma esplicita per creare una stanza quando nessuna esistente
  puo' possedere il processo;
- preserva `METODO.md`, `FONTI.md` e `CORE.md` ai rilanci;
- riusa una capacita' esistente quando copre gia' il lavoro; una nuova skill si
  installa solo dopo una scelta esplicita di nome e perimetro;
- registra l'asset e il processo nell'Ecosistema cliente;
- calcola pesi, drift, riallineamento, alert e backtest dai CSV normalizzati;
- blocca target fuori universo e serie mensili incomplete;
- produce un dossier tracciabile che il banker valida prima del report cliente.

## Fonti ufficiali da tenere vive

Queste fonti vanno riverificate quando si aggiorna lo standard:

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
- produce log e report;
- i test automatici passano;
- la cartella madre e ogni vera stanza hanno `AGENTS.md` + `CLAUDE.md`, con
  `CLAUDE.md` ridotto al solo ponte `@AGENTS.md`;
- una nuova chat dell'agente sa leggere la mappa e dove salvare memoria/report.
- la mappa madre raggiunge ogni stanza operativa e nessuna capacita' resta
  isolata o promossa a stanza per abitudine.
- l'Ispettore ha censito ogni cartella e file visibile nella home e non restano
  percorsi senza classe e proprietario, cartelle generiche o vuote, doppioni,
  stanze senza mappa o file sciolti senza casa;
- almeno due prove di instradamento partono dalla radice e arrivano alla stanza,
  alla fonte e all'output corretti senza suggerire il percorso all'agente.
- il report registra versione del metodo, classificazione delle stanze,
  collegamenti e possibili lezioni candidate.
- il report distingue Fase 1 Cervello creata/testata da Fase 2 Ecosistema
  da collegare con fonti reali.
- ogni nuovo asset operativo ha casa/fonte vera, riga in `ecosistema/ASSET.md`
  e solo i processi/limiti necessari aggiornati.
- `AGENTS.md` e il report finale includono la mappa comunicazione: procedure nei
  file proprietari, stato/report nei log, asset in `ecosistema/ASSET.md`, chat
  solo temporanea e sync dedicato solo se esistono due agenti.
- il report produce una mappa moduli con stato per PEC/email certificata,
  email/calendario, calendario operativo, Drive/OneDrive, CRM/gestionale,
  plugin, skill, agenti, guardiani/hook, ronde, voce/dettatura e
  compliance/privacy/AI Act.
- l'agente chiude l'ambiente operativo usato: email/notifiche lavorate
  archiviate nello stesso giro o dichiarate in handoff, pagine web/tab/form/preview/login/app
  aperti da lui chiusi se non servono piu'.
