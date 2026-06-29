# LeaderAI Cervello + Ecosistema

Repo operativa per montare un ambiente AI cliente secondo lo standard LeaderAI.

Non e' un audit a domande. E' un installatore: controlla, crea cio' che manca,
scrive log, lascia un report finale.

## Uso rapido

Per installare tramite l'agente del cliente, usare:

```text
INSTALLA_CON_AI.md
```

Il testo fa clonare questa repo via Git, trova la cartella OneDrive giusta e
monta Cervello + Ecosistema senza trasformare il cliente in tecnico.

Uso manuale:

```bash
python3 leaderai_setup.py --target /percorso/EcosistemaAI-Cliente --client "Nome Cliente" --agent both
```

Valori per `--agent`:

- `codex`
- `claude`
- `both`

## Cosa crea

Nel target scelto crea solo i pezzi standard mancanti:

- `AGENTS.md`
- `CLAUDE.md` se richiesto Claude Code
- `.codex/README.md` se richiesto Codex
- `.claude/README.md` se richiesto Claude Code
- `memory/MEMORY.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `REPORT_FINALE.md`

Non sovrascrive file gia' presenti, salvo `--force`.

## Collaudo

```bash
python3 -m unittest discover -s tests
```

## Stato

Versione iniziale installabile via Git. Prima di usarla con un cliente, leggere
`AGENTS.md` e `INSTALLA_CON_AI.md`, poi verificare che la repo GitHub sia
aggiornata.
