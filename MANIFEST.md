# Manifest LeaderAI Cervello + Ecosistema

## Obiettivo

Portare una cartella cliente a uno standard minimo operativo:

1. Fase 1 - Cervello: istruzioni, memoria unica, log tecnico e agenti.
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
5. produrre un report di missione datato e temporaneo.

## Contratto architetturale adattivo

La repo insegna **come leggere e governare** un Ecosistema. Il nome e il numero
delle stanze nascono dal lavoro reale del proprietario.

### Telaio universale

Restano stabili in ogni installazione:

- una sola cartella madre viva;
- `AGENTS.md` alla radice come mappa e router comune;
- `CLAUDE.md` sempre presente come ponte di una riga (`@AGENTS.md`);
- memoria indicizzata, log e registri di fonti, asset, processi e limiti;
- calco locale `ecosistema/STANZA_AGENTS.md` per creare mappe senza dipendere
  da un percorso esterno;
- Ispettore Ecosistema richiamabile dall'agente attivo;
- versione del metodo applicato e prove di collaudo.

La versione installata vive nell'`AGENTS.md` della cartella madre. Ogni
Ispettore legge anche il `VERSION` della repo ufficiale aggiornata e blocca il
verdetto se non puo' confrontare i due valori o se non coincidono.

Per Claude Code esiste una sola memoria. `autoMemoryDirectory` viene impostato
nelle **user settings** di ciascun computer (`~/.claude/settings.json`), oppure
da policy o `--settings`: la documentazione ufficiale non accetta questa chiave
nelle settings project/local. Il valore e' assoluto o inizia con `~/`, quindi
su due PC puo' essere diverso pur puntando alla stessa cartella OneDrive.
`/memory` deve confermare la destinazione su ogni postazione. Se esiste una
memoria auto esterna, le voci si confrontano e si uniscono prima di cambiare il
percorso.

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

Una vera stanza passa il contratto quando:

1. dichiara quale responsabilita' business possiede, quali decisioni mantiene
   e quale stato operativo governa;
2. e' raggiungibile dalla mappa madre;
3. ha una mappa corta alla porta: `AGENTS.md` come fonte unica e `CLAUDE.md`
   come ponte `@AGENTS.md`, con scopo, fonti, output e modo di muoversi;
4. dichiara collegamenti a monte e a valle solo per processi reali;
5. usa una sola fonte di verita' per ogni dato o stato;
6. registra le capacita' che la servono e la prova che funzionano.

Script, skill, modelli, fonti e output possono formare una pipeline completa
senza costituire una stanza. Descrivono **come** si esegue un lavoro; la stanza
descrive **chi possiede la responsabilita' business**. Un nome di prodotto o
di lavorazione, per esempio `Portafoglio Modello`, resta `CAPACITA` o
`SOSPETTA` finche' il proprietario non dimostra che e' anche una funzione
business autonoma con stato e decisioni propri. In dubbio il gate e'
`NON PASSA`: l'agente non crea la mappa locale e non inventa una stanza.

Una casa semplice puo' avere **zero stanze**. Quando una capacita', fonte o
output non appartiene a una responsabilita' business autonoma, la cartella
madre puo' possederlo direttamente: lo registra nell'`AGENTS.md` radice e in
`ecosistema/ASSET.md` o `ecosistema/FONTI.md`. In questo caso non nasce una
mappa locale. La crescita futura puo' promuoverlo a stanza solo quando emerge
una responsabilita' business reale approvata dal proprietario.

Il contratto locale nasce dalla fonte repo `templates/STANZA_AGENTS.md` e viene
installato come `ecosistema/STANZA_AGENTS.md`. Ogni cartella nuova
viene classificata e assegnata alla cartella madre o a una stanza proprietaria
prima del salvataggio.
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
- `REPORT_FINALE.md` esiste soltanto durante una missione, con data/ora e stato.
  E' ignorato da Git, non e' una fonte di stato e viene eliminato dopo `CHIUDI`
  quando i fatti stabili sono stati promossi nelle fonti proprietarie.
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

Il report di missione viene prima creato e collaudato localmente, con data/ora e
stato. L'invio email a LeaderAI avviene dopo autorizzazione esplicita del
proprietario; dopo `CHIUDI` il report temporaneo viene eliminato.

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
- `ecosistema/STANZA_AGENTS.md`

Lo standard statico necessario alla procedura senza esecuzione di codice e'
esposto in `templates/` e la sua versione e' dichiarata in `VERSION`.

Per Claude Code:

- `.claude/README.md`
- `.claude/skills/ispettore-ecosistema/SKILL.md`
- `autoMemoryDirectory` nelle user settings di ogni computer
  (`~/.claude/settings.json`), con percorso assoluto verso la memoria canonica
  dichiarata nella mappa madre e prova `/memory`

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
- la versione installata coincide con il `VERSION` vivo, Claude usa una sola
  memoria, nessun report temporaneo e' trattato come stato stabile;
- contenuti business modificabili, credenziali, firma/timbro e file progetto
  rispettano il contratto di unicita', protezione e ordine;
- almeno due prove di instradamento partono dalla radice e arrivano alla
  madre/stanza, alla fonte e all'output corretti senza suggerire il percorso
  all'agente.
- il report registra versione del metodo, classificazione delle stanze,
  collegamenti e possibili lezioni candidate.
- il report distingue Fase 1 Cervello creata/testata da Fase 2 Ecosistema
  da collegare con fonti reali.
- ogni nuovo asset operativo ha casa/fonte vera, riga in `ecosistema/ASSET.md`
  e solo i processi/limiti necessari aggiornati.
- `AGENTS.md` e il report temporaneo includono la mappa comunicazione:
  procedure e stato business nei file proprietari, storia tecnica nel log,
  asset in `ecosistema/ASSET.md`, chat solo temporanea e sync dedicato solo se
  esistono due agenti.
- il report produce una mappa moduli con stato per PEC/email certificata,
  email/calendario, calendario operativo, Drive/OneDrive, CRM/gestionale,
  plugin, skill, agenti, guardiani/hook, ronde, voce/dettatura e
  compliance/privacy/AI Act.
- l'agente chiude l'ambiente operativo usato: email/notifiche lavorate
  archiviate nello stesso giro o dichiarate in handoff, pagine web/tab/form/preview/login/app
  aperti da lui chiusi se non servono piu'.
