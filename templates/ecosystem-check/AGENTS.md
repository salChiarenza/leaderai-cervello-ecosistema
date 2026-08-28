# Ecosystem Check

Questa e' la mappa locale della stanza `Ecosystem Check`.

## Stato corrente e prossimo passo

- Stato, prossimo passo, decisioni e scadenze vivono in `STATO.md`.
- La storia dei controlli conclusi vive in `REGISTRO_CONTROLLI.md`.
- Questa mappa instrada il reparto e non diventa un secondo diario.

## Scopo

Mantenere ordinato, verificabile e funzionante il Cervello + Ecosistema.

## Responsabilita business

Ecosystem Check possiede il controllo continuo della struttura AI dell'azienda:
standard dei reparti, posizione dei file, istruzioni, continuita' operativa,
assegnazione delle correzioni e verifica della loro chiusura. Mantiene lo stato
dei controlli e governa le decisioni su interventi e chiusure.

## Organigramma

- Ruolo: **Amministratore del settore Ecosystem Check**.
- Riporta al **Boss dell'Ecosistema** definito nell'`AGENTS.md` della cartella
  madre.
- L'Amministratore assegna controlli separati, impedisce sovrapposizioni e
  riporta al Boss soltanto risultati provati, problemi aperti e decisioni vere.
- La verifica finale resta separata dall'intervento: chi corregge non certifica
  da solo il proprio lavoro.

## Dentro

- `ruoli/`: compiti separati dell'orchestratore, dei controllori, di chi
  interviene e di chi verifica la chiusura.

## Fonti

- Mappa madre, mappe e fonti operative delle stanze, standard ufficiale.

## Output

- `STATO.md` e `REGISTRO_CONTROLLI.md`.

## Fonte operativa

- `STATO.md`

Mantiene in testa `Stato corrente`, `Prossimo passo`, `Decisioni` e
`Scadenze`; i controlli aperti vengono dopo.

## Fonte business editabile

- NON APPLICABILE: il reparto non genera documenti commerciali o materiali
  cliente; governa standard, controlli e interventi sulla casa AI.

## Capacita

- Orchestratore, controllori, intervento, verifica finale, Ispettore.

## A monte

- Boss dell'Ecosistema e standard ufficiale.

## A valle

- Tutte le stanze e gli elementi della casa.

## Dove scrivere

- Stato e incarichi aperti in `STATO.md`.
- Criteri stabili in `STANDARD_REPARTO.md`.
- Un solo riepilogo per controllo concluso in `REGISTRO_CONTROLLI.md`.
- I dettagli tecnici restano nella fonte proprietaria del problema; non si
  copiano qui interi rapporti o contenuti delle altre stanze.

## Regole

- L'orchestratore assegna; i controllori osservano; `INTERVENTO` corregge;
  `CONTROLLO_CHIUSURA` riprova senza usare il giudizio di chi ha corretto.
- I controllori sono in sola lettura. Solo `INTERVENTO` modifica file, entro il
  perimetro assegnato e senza eliminazioni, fusioni o spostamenti non approvati.
- Un problema senza percorso, fonte e prova osservabile non viene assegnato.
- Ogni problema aperto ha un responsabile, una correzione attesa e una prova di
  chiusura.
- Prima di creare una cartella, classificarla come `STANZA`, `FONTE`, `OUTPUT`,
  `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`.
- Nessuna stanza nasce dentro `ecosistema/`: vive accanto alla cartella comune.
- Ogni sottocartella diretta e' dichiarata nella mappa del reparto proprietario.
- Nessun controllo ricorrente viene attivato senza cadenza, chiusura delle
  superfici aperte e controllo dell'accumulo di sessioni.
- `CLAUDE.md` in questa stanza contiene soltanto `@AGENTS.md`.
