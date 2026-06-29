# LeaderAI Cervello + Ecosistema

Repo installabile per creare la cartella madre AI di un cliente.

Questa repo e' letta sia da Claude Code sia da Codex. `CLAUDE.md`, se
presente, deve essere un symlink o una copia di questo file.

## Cosa fa

Monta in una cartella cliente lo standard minimo LeaderAI:

- `AGENTS.md`
- `CLAUDE.md` se serve Claude Code
- `.codex/README.md` se serve Codex
- `.claude/README.md` se serve Claude Code
- `memory/MEMORY.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `REPORT_FINALE.md`

## Regola madre

Il cliente non deve fare debug tecnico. L'agente del cliente fa autodiagnosi,
installa o ripara cio' che manca, crea la cartella madre nel posto giusto e
chiude solo dopo un collaudo reale.

Per clienti con piu' computer, la cartella madre deve stare in una posizione
sincronizzata, per esempio OneDrive. Non usare `Downloads`, `Desktop` locale o
cartelle temporanee come destinazione finale.

## Uso cliente

Il file da consegnare e':

- `INSTALLA_CON_AI.md`

Il cliente incolla quel testo in Claude Code o Codex. Prima del clone non ha
questa repo, quindi la missione deve stare tutta nel testo.

## Divieti

- Non salvare segreti, password, token o dati bancari.
- Non cancellare o spostare file del cliente senza conferma esplicita.
- Non creare doppioni di cartelle se ne esiste gia' una viva.
- Non sovrascrivere file esistenti senza `--force` e senza motivo chiaro.
- Non promettere output professionali regolamentati: l'agente prepara bozze,
  il professionista verifica, decide e firma.

## Comandi

Collaudo repo:

```bash
python3 -m unittest discover -s tests
```

Installazione manuale:

```bash
python3 leaderai_setup.py --target /percorso/EcosistemaAI-Cliente --client "Nome Cliente" --agent both
```

## Quando finisci una modifica

1. Aggiorna `README.md`, `MANIFEST.md` o `INSTALLA_CON_AI.md` se cambia un fatto
   critico.
2. Esegui i test.
3. Commit e push su GitHub: la base cliente e' la repo, non il clone locale.
4. Aggiorna l'anagrafe LeaderAI in `leaderai/memory/reference_mcp_attivi.md`.
