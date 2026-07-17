# LeaderAI Cervello + Ecosistema

Repo operativa per montare un ambiente AI cliente secondo lo standard LeaderAI.

Non e' un audit a domande. E' una repo operativa: installa quando manca tutto,
fa checkup e riparazione quando l'ambiente esiste gia', scrive log e lascia un
report finale.

Regola madre: questa repo e' lo standard, la cartella viva del cliente e' il
caso reale. `CHECKUP.md` confronta il caso reale con `MANIFEST.md` e
`templates/AGENTS.md`, ripara gli scostamenti riparabili, prova e poi manda il
report finale.

La repo fornisce un telaio minimo e un metodo adattivo. Il telaio rende stabile
il Cervello; il metodo censisce il lavoro reale, riconosce le stanze gia' vive e
le collega alla mappa madre. I nomi delle stanze appartengono al cliente, non al
template.

## Uso rapido

Per installare tramite l'agente del cliente, usare:

```text
INSTALLA_CON_AI.md
```

L'agente legge questa repo ufficiale in sola lettura, trova o crea la cartella
madre nella posizione scelta col cliente e applica localmente i template dello
standard. Il percorso cliente predefinito non clona la repo e non esegue codice
scaricato.

Per il controllo periodico di un ambiente gia' installato:

```text
CHECKUP.md
```

Il proprietario dice al suo agente "esegui il checkup LeaderAI": l'agente
confronta il setup con la documentazione ufficiale viva (indice
`code.claude.com/docs/llms.txt`, pagine `.md`), ripara da solo il tecnico e
invia il resoconto a Sal. Prima di giudicare censisce le cartelle candidate:
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

- `claude` se il cliente sta usando Claude Code
- `codex` se il cliente sta usando Codex
- `both` solo se LeaderAI chiede esplicitamente di preparare entrambi

## Cosa crea

Nel target scelto crea solo i pezzi standard mancanti:

- `.gitignore` che esclude `.secrets/`, `*.env`, token, chiavi e credenziali
- inizializza la cartella madre come repository git (se non lo e' gia')
- `AGENTS.md` come mappa comune del Cervello
- `CLAUDE.md` se richiesto Claude Code
- `.codex/README.md` se richiesto Codex
- `.claude/README.md` se richiesto Claude Code
- `memory/MEMORY.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `REPORT_FINALE.md`

Questi pezzi sono infrastruttura comune. Le cartelle business vengono prima
classificate come stanza, fonte, output, capacita', infrastruttura, archivio o
elemento sospetto. Ogni vera stanza deve essere raggiungibile dalla radice e
avere una mappa corta con fonti, output e collegamenti reali.

Il report finale include anche la **mappa moduli**: PEC/email certificata,
email/calendario, calendario operativo, Drive/OneDrive, CRM/gestionale, plugin,
skill, agenti, guardiani/hook, ronde, voce/dettatura e compliance/privacy/AI
Act. Ogni modulo deve avere uno stato, cosi' il prossimo passo non dipende
dalla memoria di chi segue la consegna.

Modulo specifico gia' disponibile:

- `MODULO_CALENDARIO_OPERATIVO.md` - quando il cliente usa Calendar a colori e
  serve trasformare quella lettura visiva in struttura leggibile dall'agente.
- `moduli/portafogli/` - Sistema Portafogli Core-Satellite: fonti autorizzate,
  metodo del banker, calcoli deterministici, backtest, monitoraggio e report.
  L'agente del cliente parte da `moduli/portafogli/INSTALLA_MODULO.md`, sceglie
  la stanza proprietaria e integra il modulo senza creare una stanza concorrente.

Il Cervello include anche la **mappa comunicazione**: stato e chiusure in
`REPORT_FINALE.md`/`logs/`, procedure nei file proprietari, asset in
`ecosistema/ASSET.md`, chat solo per coordinamento temporaneo e sync dedicato
solo se il cliente usa sia Claude sia Codex.

Non sovrascrive file gia' presenti, salvo `--force`.

La versione corrente dello standard e' in `VERSION`; le modifiche consegnabili
sono registrate in `CHANGELOG.md`.

## Collaudo

```bash
python3 -m unittest discover -s tests
```

## Stato

Versione applicabile via lettura della repo ufficiale. Prima di usarla con un
cliente, leggere `AGENTS.md` e `INSTALLA_CON_AI.md`, scegliere la modalita'
Claude/Codex e verificare `VERSION` e stato GitHub.
