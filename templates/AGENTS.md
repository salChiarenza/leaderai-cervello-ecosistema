# AGENTS.md - {{client_name}}

Questa e' la porta del Cervello AI del cliente.

## Obiettivo

Aiutare il cliente a lavorare meglio usando AI, senza inventare fonti e senza
spargere memoria in posti casuali.

Modalita' installata: `{{agent}}`.

## Regole base

- Prima leggere questa mappa.
- La memoria condivisa vive in `memory/MEMORY.md`.
- I log operativi vivono in `logs/`.
- La mappa dell'azienda vive in `ecosistema/`.
- Il registro asset operativi vive in `ecosistema/ASSET.md`.
- Non cancellare o spostare file del cliente senza conferma esplicita.
- Non salvare segreti, password, token o dati bancari in memoria.
- La posizione di questa cartella (locale o cloud) e il backup (GitHub privato a
  comando oppure copia su Drive/OneDrive) sono stati scelti col cliente caso per
  caso. Sul cloud vale l'avviso: Claude Code puo' corrompere/troncare i file
  durante la scrittura. I segreti restano sempre nel `.gitignore`.
- Se manca un pezzo standard, crearlo.
- Se questa cartella e' stata installata per `claude`, non creare `.codex`
  senza richiesta esplicita LeaderAI.
- Se questa cartella e' stata installata per `codex`, non creare `.claude` o
  `CLAUDE.md` senza richiesta esplicita LeaderAI.
- Se serve una decisione umana vera, scriverla nel report finale come `DECISIONE`.

## Comunicazione e fonti di verita'

Gli agenti non si parlano direttamente. Si coordinano leggendo e scrivendo file
condivisi.

| Caso | Dove si scrive | Durata |
|---|---|---|
| Stato operativo o chiusura lavoro | `REPORT_FINALE.md` oppure `logs/install-log.md` | finche' serve come prova |
| Procedura / come si fa una cosa | file dell'area che la usa, es. `ecosistema/PROCESSI.md` o procedura dedicata | stabile |
| Problema di allineamento tra Claude e Codex | sync dedicato solo se si usano entrambi gli agenti | finche' si chiude |
| Coordinamento immediato sullo stesso file | chat temporanea solo se serve evitare collisioni | massimo 48 ore |
| Asset/capacita' nuova | `ecosistema/ASSET.md` | stabile |

Regola pratica: se una nota spiega "come si fa", non va in chat. Va nella
procedura o nel file proprietario. La chat e' solo coordinamento temporaneo.

## Riflesso asset operativo

Quando il cliente dice "aggiungi", "abbiamo", "ho comprato", "attiva",
"collega" o indica una nuova risorsa operativa, non basta nominarla in chat.

Ogni asset deve lasciare quattro tracce:

- casa/fonte vera;
- riga in `ecosistema/ASSET.md`;
- processo o limite aggiornato, solo se cambia davvero;
- log finale in `logs/install-log.md` o `REPORT_FINALE.md`.

Esempi di asset: PEC, email, banca, auto, gestionale, Drive, WhatsApp,
fornitore, sito, repo, kit, app o archivio.

## Fase 1 - Cervello

Il Cervello e' pronto quando:

- questa mappa esiste;
- la memoria a file esiste;
- i log esistono;
- l'agente scelto ha il suo punto di aggancio;
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

Se una fonte non esiste ancora, scrivere `da collegare` e indicare dove
andrebbe collegata. Non inventare percorsi, CRM o cartelle clienti.

## Mappa moduli

Alla fine del setup o di un audit, il report deve dire quali moduli servono
davvero e quali no. Non partire dal modulo preferito del momento.

Stati ammessi: `NON SERVE`, `DA SCOPRIRE`, `DA COLLAUDARE`, `INSTALLABILE`,
`ATTIVO`.

Moduli minimi da valutare: PEC/email certificata, email/calendario,
calendario operativo, Drive/OneDrive/cartelle, CRM/gestionale/export,
plugin/connettori, skill, agenti/ruoli, guardiani/hook, ronde/monitoraggi,
voce/dettatura, compliance/privacy/AI Act.

Se l'agenda vive di colori, applicare il modulo calendario operativo: colori per
il team, categorie leggibili per l'agente, prova letta prima di `ATTIVO`.

## Report

Ogni intervento importante chiude con `REPORT_FINALE.md` o con una voce in
`logs/install-log.md`.

Creato da LeaderAI Cervello + Ecosistema il {{date}}.
