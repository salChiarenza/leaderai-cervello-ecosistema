# LeaderAI Cervello + Ecosistema

Repo operativa per montare un ambiente AI cliente secondo lo standard LeaderAI.

Non e' un audit a domande. E' una repo operativa: installa quando manca tutto,
fa checkup e riparazione quando l'ambiente esiste gia', scrive log e lascia un
report finale.

Regola madre: questa repo e' lo standard, la cartella viva del cliente e' il
caso reale. `CHECKUP.md` confronta il caso reale con `MANIFEST.md`,
`templates/AGENTS.md` e `templates/STANZA_AGENTS.md`, ripara gli scostamenti
riparabili, prova e prepara il report finale. L'invio avviene solo dopo
autorizzazione esplicita del proprietario.

`install_contract.json` e' il contratto macchina unico del nucleo
d'installazione: procedura manuale, setup tecnico, Ispettore e collaudo leggono
la stessa lista di file obbligatori e rami agente. Browser, launcher e backup
remoto sono controlli della macchina cliente dichiarati nello stesso contratto
e restano `DA COLLAUDARE` nel gate anonimo.

La repo fornisce un telaio minimo e un metodo adattivo. Il telaio rende stabile
il Cervello; il metodo censisce il lavoro reale, riconosce le stanze gia' vive e
le collega alla mappa madre. La cartella madre e ogni vera stanza hanno sempre
`AGENTS.md` come fonte unica e `CLAUDE.md` come ponte `@AGENTS.md`. I nomi
delle stanze appartengono al cliente, non al template.

## Uso rapido

Per installare tramite l'agente del cliente, usare:

```text
INSTALLA_CON_AI.md
```

Il testo della prima email di consegna vive soltanto in `EMAIL_CONSEGNA.md`.
La procedura non ne mantiene una seconda copia.

L'agente legge questa repo ufficiale in sola lettura, trova o crea la cartella
madre nella posizione scelta col cliente e applica localmente i template dello
standard. Il percorso cliente predefinito non clona la repo e non esegue codice
scaricato.

Per il controllo periodico di un ambiente gia' installato:

```text
CHECKUP.md
```

Il proprietario dice al suo agente `lancia l'Ispettore` oppure
`esegui il checkup LeaderAI`: la skill `ispettore-ecosistema` apre la fonte
unica `CHECKUP.md` e l'agente confronta il setup con la documentazione
ufficiale viva (indice
`code.claude.com/docs/llms.txt`, pagine `.md`), ripara da solo il tecnico e
prepara il resoconto per Sal. Lo invia soltanto dopo autorizzazione esplicita
del proprietario. Prima di giudicare censisce le cartelle candidate:
la cartella viva puo' chiamarsi in qualunque modo, quindi si riconosce dai
segnali di vita (memoria compilata, log, report, asset, commit, file di lavoro
recenti, connettori provati), non dal nome. La ricerca include anche nomi
brandizzati o sbagliati come `LeaderAI`, `Leader AI`, `leader ai`, `leder ai`,
`cervello`, `ecosistema`, `_leaderai`, `install`, `setup`, `repo` e `clone`.

Ogni missione segue un ciclo chiuso: `MISSIONE` -> `ESECUZIONE` ->
`AUTOCONTROLLO` -> `REPORT` -> `SAL_VERIFICA` -> `CONTINUA` oppure `CHIUDI`.
L'agente del cliente non decide da solo che e' finita dopo il primo report:
aspetta la verifica LeaderAI.

Dove mettere la cartella madre si decide caso per caso con domande guidate
(disco locale oppure cartella sincronizzata OneDrive / Google Drive). Avviso da
dire chiaro: Claude Code, mentre scrive, puo' corrompere o troncare i file su
cartelle cloud con file on-demand (bug noti); il cliente sceglie se accettare il
rischio in cambio della comodita'. Il backup si sceglie sempre col cliente
(GitHub privato a comando oppure copia su Drive/OneDrive). I segreti restano
sempre fuori dal git (`.gitignore`). Dettaglio in `INSTALLA_CON_AI.md`
Domande 1, 2, 3 e Fase 7.

Uso tecnico opzionale, dopo autorizzazione esplicita:

```bash
python3 leaderai_setup.py --target /percorso/EcosistemaAI-Cliente --client "Nome Cliente" --agent claude
```

Valori per `--agent`:

- `claude` crea soltanto la configurazione `.claude/`
- `codex` crea soltanto la configurazione `.codex/`
- `both` crea entrambe le configurazioni, solo su richiesta esplicita LeaderAI

In tutti e tre i casi il telaio comune resta identico: `AGENTS.md` +
`CLAUDE.md`. La modalita' seleziona le configurazioni dell'agente, non i file
del contratto comune. Un cambio tra Codex e Claude viene fermato: si usa
`--agent both` per mantenere entrambi oppure `--migrate-agent` per una
migrazione esplicita e conservativa. Per Claude, il setup preserva le altre
user settings e blocca il lavoro se `autoMemoryDirectory` punta gia' a una
seconda casa.

## Cosa crea

Nel target scelto crea solo i pezzi standard mancanti:

- `.gitignore` che esclude `.secrets/`, `*.env`, token, chiavi, credenziali e
  `REPORT_FINALE.md`
- inizializza la cartella madre come repository git (se non lo e' gia')
- `AGENTS.md` come mappa comune del Cervello
- `CLAUDE.md` come ponte permanente di una riga (`@AGENTS.md`)
- `.codex/README.md` se richiesto Codex
- `.claude/README.md` se richiesto Claude Code
- user settings Claude Code (`~/.claude/settings.json`) con
  `autoMemoryDirectory` sulla memoria canonica della casa, verificate su ogni PC
- `.agents/skills/ispettore-ecosistema/SKILL.md` se richiesto Codex
- `.claude/skills/ispettore-ecosistema/SKILL.md` se richiesto Claude Code
- `memory/MEMORY.md`
- `AGENT_CHAT.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `ecosistema/STANZA_AGENTS.md` come calco locale per le nuove stanze
- `REPORT_FINALE.md` come output temporaneo e datato della missione aperta

Questi pezzi sono infrastruttura comune. Le cartelle business vengono prima
classificate come stanza, fonte, output, capacita', infrastruttura, archivio o
elemento sospetto. Ogni vera stanza deve essere raggiungibile dalla radice e
avere `AGENTS.md` + `CLAUDE.md`, con mappa corta, fonti, output e collegamenti
reali.

Ogni nuova stanza usa il calco installato `ecosistema/STANZA_AGENTS.md`,
generato dalla fonte repo `templates/STANZA_AGENTS.md`. Prima del salvataggio
l'Ispettore controlla che ogni percorso visibile nella home abbia classe e
proprietario, che le stanze siano collegate alla radice e che non restino
cartelle generiche, vuote, doppie, tecniche o file sciolti senza casa.

Il report temporaneo include anche la **mappa moduli**: PEC/email certificata,
email/calendario, calendario operativo, Drive/OneDrive, CRM/gestionale, plugin,
skill, agenti, guardiani/hook, ronde, voce/dettatura e compliance/privacy/AI
Act. Ogni modulo deve avere uno stato, cosi' il prossimo passo non dipende
dalla memoria di chi segue la consegna.

Modulo specifico gia' disponibile:

- `MODULO_CALENDARIO_OPERATIVO.md` - quando il cliente usa Calendar a colori e
  serve trasformare quella lettura visiva in struttura leggibile dall'agente.
- `moduli/portafogli/` - Sistema Portafogli Core-Satellite: fonti autorizzate,
  verifica automatica di numeri, identita', stato e collocabilita' degli
  strumenti, metodo del banker, calcoli deterministici, backtest, monitoraggio
  e report.
  L'agente del cliente parte da `moduli/portafogli/INSTALLA_MODULO.md`, sceglie
  la cartella madre o la stanza proprietaria e integra il modulo senza creare
  una stanza concorrente.

Il Cervello include anche la **mappa comunicazione**: stato business nel file
proprietario della stanza, storia tecnica nel solo `logs/install-log.md`,
report datato solo durante la missione, asset in `ecosistema/ASSET.md`, chat
solo per coordinamento temporaneo e sync dedicato solo se il cliente usa sia
Claude sia Codex.

L'Ispettore confronta sempre la versione installata con il `VERSION` vivo,
verifica che Claude usi una sola memoria, individua configurazioni credenziali
fuori `.secrets/` senza aprirle, controlla firma/timbro e impedisce copie
hardcoded di contenuti business modificabili.

I file vivi del cliente restano intatti. `--force` serve soltanto a riparare il
ponte canonico `CLAUDE.md` quando e' mancante o errato.

La versione corrente dello standard e' in `VERSION`; le modifiche consegnabili
sono registrate in `CHANGELOG.md`.

## Collaudo

Gate deterministico obbligatorio:

```bash
python3 -m tests.gate --quick
```

Gate completo di rilascio, su macchina con entrambi gli agenti autenticati:

```bash
python3 -m tests.gate --release --agents codex,claude
```

Il gate completo avvia sessioni nuove reali. Prova due richieste business senza
percorsi suggeriti e ripete l'installazione manuale partendo dalla sola
procedura. Conserva prompt, trascrizioni, manifest prima/dopo, diff e verdetti.
Zero test, test saltati, CLI assente, autenticazione mancante, timeout o
oracolo fallito bloccano il rilascio.

Preflight strutturale opzionale e in sola lettura, quando la repo e' locale e
l'esecuzione e' stata autorizzata:

```bash
python3 ecosistema_inspector.py --target /percorso/EcosistemaAI-Cliente
```

## Stato

Versione applicabile via lettura della repo ufficiale. Prima di usarla con un
cliente, leggere `AGENTS.md` e `INSTALLA_CON_AI.md`, scegliere la modalita'
Claude/Codex e verificare `VERSION` e stato GitHub.
La cartella madre deve essere anche il punto di ingresso reale dell'agente:
progetto locale primario in Codex Desktop, `-C`/directory corrente in Codex
CLI, directory corrente in Claude Code. Dopo un cambio di cartella si apre una
nuova task/sessione e si prova `AGENTS.md` prima del lavoro.
