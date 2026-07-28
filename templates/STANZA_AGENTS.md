# {{room_name}}

Questa e' la mappa locale della stanza `{{room_name}}`.

## Stato corrente e prossimo passo

- Stato: da compilare nel file proprietario della stanza.
- Prossimo passo: da compilare nel file proprietario della stanza.
- Scadenze: nessuna oppure data, responsabile e azione in evidenza.

## Scopo

{{room_purpose}}

## Dentro

- {{room_contents}}

## Fonti

- {{room_sources}}

## Output

- {{room_outputs}}

## Fonte business editabile

- {{room_business_source}}
- Se la stanza non genera documenti da contenuti business, scrivere
  `NON APPLICABILE` e motivare in una riga.

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
- Il contenuto business che il proprietario deve poter correggere vive in un
  file fonte esterno al codice e dichiarato in questa mappa. Codice e app lo
  leggono e generano PDF, Word o altri derivati; se la fonte manca, falliscono
  in modo visibile e non usano una copia hardcoded silenziosa.
- Nei file progetto lo stato corrente, il prossimo passo e le scadenze stanno
  in testa; il diario viene dopo ed e' ordinato dal piu' recente.
- Una nuova stanza nasce solo quando nessuna stanza esistente puo' possedere
  quella funzione e il proprietario approva la proposta strutturale.
- `CLAUDE.md` in questa stanza contiene soltanto `@AGENTS.md`.
