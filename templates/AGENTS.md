# AGENTS.md - {{client_name}}

Questa e' la porta del Cervello AI del cliente.

## Obiettivo

Aiutare il cliente a lavorare meglio usando AI, senza inventare fonti e senza
spargere memoria in posti casuali.

## Regole base

- Prima leggere questa mappa.
- La memoria condivisa vive in `memory/MEMORY.md`.
- I log operativi vivono in `logs/`.
- La mappa dell'azienda vive in `ecosistema/`.
- Non cancellare o spostare file del cliente senza conferma esplicita.
- Non salvare segreti, password, token o dati bancari in memoria.
- Se manca un pezzo standard, crearlo.
- Se serve una decisione umana vera, scriverla nel report finale come `DECISIONE`.

## Fase 1 - Cervello

Il Cervello e' pronto quando:

- questa mappa esiste;
- la memoria a file esiste;
- i log esistono;
- Codex/Claude Code hanno il loro punto di aggancio;
- una nuova chat sa dove leggere e dove scrivere.

## Fase 2 - Ecosistema

L'Ecosistema non e' una copia dell'azienda.

E' la mappa delle fonti reali:

- cartelle operative;
- documenti ricorrenti;
- email e calendario se collegati;
- gestionali/CRM/fatture se esistono;
- processi ricorrenti;
- limiti e azioni che richiedono conferma.

## Report

Ogni intervento importante chiude con `REPORT_FINALE.md` o con una voce in
`logs/install-log.md`.

Creato da LeaderAI Cervello + Ecosistema il {{date}}.
