# {{room_name}}

Questa e' la mappa locale della stanza `{{room_name}}`.

## Stato corrente e prossimo passo

- Stato, prossimo passo, decisioni e scadenze si leggono e si aggiornano nella
  Fonte operativa dichiarata sotto.
- Questa mappa instrada e non diventa un secondo diario.

## Scopo

{{room_purpose}}

## Responsabilita business

{{room_business_responsibility}}

Descrivere la funzione aziendale riconosciuta dal proprietario, lo stato che
mantiene e le decisioni che governa. Elencare script, skill, modelli o output
non dimostra una stanza.

## Organigramma

- Ruolo: **Amministratore del settore `{{room_name}}`**.
- Riporta al **Boss dell'Ecosistema** definito nell'`AGENTS.md` della cartella
  madre.
- L'Amministratore governa stato, decisioni, fonti, capacita' e output del
  settore; coordina i suoi elementi subordinati e riporta al Boss risultati,
  blocchi e passaggi verso altri settori.
- Riporta al Boss senza duplicare nella mappa madre i dettagli operativi del
  settore.

## Dentro

- {{room_contents}}
- Ogni sottocartella diretta usa il formato: percorso tra apici inversi,
  seguito dalla sua funzione.
- Se non esistono sottocartelle, scrivere NESSUNA SOTTOCARTELLA.

## Fonti

- {{room_sources}}

## Output

- {{room_outputs}}

## Fonte operativa

- `{{room_operating_source}}`
- Deve esistere dentro questa stanza e mantenere, in testa, `Stato corrente`,
  `Prossimo passo`, `Decisioni` e `Scadenze`. Se non esiste gia', nasce dal
  calco `ecosistema/STANZA_FONTE.md` e riceve un nome che descrive la domanda
  business della stanza.

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
- Non lasciare campi del calco non compilati: una stanza incompleta non viene
  salvata.
- Ogni sottocartella diretta e' dichiarata in `Dentro`; una cartella non
  dichiarata non ha proprietario e blocca il collaudo.
- Il contenuto business che il proprietario deve poter correggere vive in un
  file fonte esterno al codice e dichiarato in questa mappa. Codice e app lo
  leggono e generano PDF, Word o altri derivati; se la fonte manca, falliscono
  in modo visibile e non usano una copia hardcoded silenziosa.
- Nei file progetto lo stato corrente, il prossimo passo e le scadenze stanno
  in testa; il diario viene dopo ed e' ordinato dal piu' recente.
- Una nuova stanza nasce solo quando nessuna stanza esistente puo' possedere
  quella responsabilita' business e il proprietario approva la proposta
  strutturale.
- Una cartella con una pipeline completa di fonti, script, modelli e output
  resta `CAPACITA` se non mantiene stato e decisioni di una funzione business.
- `CLAUDE.md` in questa stanza contiene soltanto `@AGENTS.md`.
