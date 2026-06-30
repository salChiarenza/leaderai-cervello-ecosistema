# LeaderAI Cervello + Ecosistema

Repo operativa per montare un ambiente AI cliente secondo lo standard LeaderAI.

Non e' un audit a domande. E' un installatore: controlla, crea cio' che manca,
scrive log, lascia un report finale.

## Uso rapido

Per installare tramite l'agente del cliente, usare:

```text
INSTALLA_CON_AI.md
```

Il testo fa clonare questa repo via Git, trova o crea la cartella madre nella
posizione scelta col cliente e monta Cervello + Ecosistema senza trasformare il
cliente in tecnico.

Dove mettere la cartella madre si decide caso per caso con domande guidate
(disco locale oppure cartella sincronizzata OneDrive / Google Drive). Avviso da
dire chiaro: Claude Code, mentre scrive, puo' corrompere o troncare i file su
cartelle cloud con file on-demand (bug noti); il cliente sceglie se accettare il
rischio in cambio della comodita'. Il backup si sceglie sempre col cliente
(GitHub privato a comando oppure copia su Drive/OneDrive). I segreti restano
sempre fuori dal git (`.gitignore`). Dettaglio in `INSTALLA_CON_AI.md`
Domande 1, 2, 3 e Fase 7.

Uso manuale:

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

Non sovrascrive file gia' presenti, salvo `--force`.

## Collaudo

```bash
python3 -m unittest discover -s tests
```

## Stato

Versione installabile via Git. Prima di usarla con un cliente, leggere
`AGENTS.md` e `INSTALLA_CON_AI.md`, scegliere la modalita' giusta
Claude/Codex, poi verificare che la repo GitHub sia aggiornata.
