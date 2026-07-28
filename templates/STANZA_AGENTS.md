# {{room_name}}

Questa e' la mappa locale della stanza `{{room_name}}`.

## Scopo

{{room_purpose}}

## Dentro

- {{room_contents}}

## Fonti

- {{room_sources}}

## Output

- {{room_outputs}}

## Capacita

- {{room_capabilities}}

## A monte

- {{room_upstream}}

## A valle

- {{room_downstream}}

## Dove scrivere

- Stato, procedure e output vivono nella fonte unica indicata in questa mappa.
- Le sottocartelle ordinarie appartengono a questa stanza e non diventano
  automaticamente nuove stanze.

## Regole

- Prima di creare una cartella, classificarla come `STANZA`, `FONTE`, `OUTPUT`,
  `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`.
- Non creare cartelle generiche, vuote o concorrenti.
- Non duplicare dati, stato, procedure o output gia' governati altrove.
- Una nuova stanza nasce solo quando nessuna stanza esistente puo' possedere
  quella funzione e il proprietario approva la proposta strutturale.
- `CLAUDE.md` in questa stanza contiene soltanto `@AGENTS.md`.
