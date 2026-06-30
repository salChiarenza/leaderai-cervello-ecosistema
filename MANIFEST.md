# Manifest LeaderAI Cervello + Ecosistema

## Obiettivo

Portare una cartella cliente a uno standard minimo operativo:

1. Fase 1 - Cervello: istruzioni, memoria, log, agenti, report.
2. Fase 2 - Ecosistema: fonti reali, processi, limiti, decisioni.

## Regola

L'agente non deve fare un esame al cliente.

Deve:

1. leggere questa repo;
2. montare i pezzi standard mancanti;
3. non sovrascrivere cio' che esiste;
4. collaudare;
5. scrivere un report finale.

## Modalita' agente

La repo resta unica. La modalita' cambia in base all'agente reale del cliente:

- Claude Code -> `--agent claude`
- Codex -> `--agent codex`
- Entrambi -> `--agent both`, solo su richiesta esplicita LeaderAI

Il Cervello passa quando e' pronto per l'agente usato oggi. Non e' necessario
creare l'altro lato se il cliente non lo usa.

## Standard minimo

Il target passa solo se esistono:

- `.gitignore` che esclude i segreti (`.secrets/`, `*.env`, token, chiavi, credenziali)
- la cartella madre e' un repository git (nella posizione scelta col cliente, locale o cloud; sul cloud vale l'avviso sul rischio corruzione)
- `AGENTS.md`
- `memory/MEMORY.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `REPORT_FINALE.md`

Per Claude Code:

- `CLAUDE.md`
- `.claude/README.md`

Per Codex:

- `.codex/README.md`

## Fonti ufficiali da tenere vive

Queste fonti vanno riverificate quando si aggiorna lo standard:

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
- una nuova chat dell'agente sa leggere `AGENTS.md` e dove salvare memoria/report.
- il report distingue Fase 1 Cervello creata/testata da Fase 2 Ecosistema
  da collegare con fonti reali.
- ogni nuovo asset operativo ha casa/fonte vera, riga in `ecosistema/ASSET.md`
  e solo i processi/limiti necessari aggiornati.
