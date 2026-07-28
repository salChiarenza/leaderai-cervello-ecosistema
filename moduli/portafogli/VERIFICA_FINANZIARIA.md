# Gate di verifica finanziaria

Questo gate si applica prima di usare o mostrare numeri finanziari e prima di
citare, confrontare o proporre uno strumento.

## Trigger

Attiva il gate quando il lavoro contiene almeno uno di questi elementi:

- prezzi, NAV, cambi, importi, percentuali, rendimenti, costi, date o benchmark;
- fondi, ETF, titoli, obbligazioni, certificati, ISIN o classi di quote;
- ricerca, confronto, selezione, portafoglio, backtest, outlook o report.

## Identità e stato dello strumento

Per ogni strumento registra nel dossier interno:

1. denominazione esatta;
2. ISIN o altro identificativo ufficiale;
3. classe, valuta e società di gestione/emittente;
4. stato del prodotto: `ATTIVO`, `CHIUSO A NUOVE SOTTOSCRIZIONI`, `SOSPESO`,
   `INCORPORATO`, `RINOMINATO`, `LIQUIDATO` oppure `NON VERIFICATO`;
5. collocabilità nel catalogo autorizzato corrente;
6. fonte primaria, data del documento e data/ora della verifica.

Tratta come due fatti distinti:

- esistenza e stato giuridico/commerciale dello strumento;
- disponibilità effettiva nell'universo collocabile del banker.

Un risultato di ricerca, una vecchia scheda o la memoria del modello servono
soltanto per individuare il prodotto. La prova arriva dalla pagina o dal
documento ufficiale corrente e dal catalogo autorizzato quando la collocabilità
è rilevante.

## Ordine delle fonti

1. Catalogo collocabile e fonti interne autorizzate dal banker/società.
2. Pagina ufficiale dell'emittente o società di gestione, KID/KIID,
   prospetto e avvisi di fusione, rinomina, sospensione o liquidazione.
3. Registro, mercato o comunicazione regolamentata pertinente al tipo e al
   domicilio dello strumento.
4. Provider autorizzato registrato in `FONTI.md` per prezzo, NAV, cambio,
   benchmark e serie storiche.

Usa aggregatori, motori di ricerca e risposte di altri modelli come piste.
Chiudi la verifica con una fonte primaria.

## Verifica dei numeri

Per ogni numero materiale registra:

- valore, unità e valuta;
- periodo e data/ora di riferimento;
- fonte e data della fonte;
- formula, dati di ingresso e criterio di arrotondamento;
- natura lorda/netta e costi, fiscalità o cambio inclusi;
- ricalcolo indipendente tramite `portfolio_engine.py` quando il dato è
  calcolato dal Sistema Portafogli.

## Secondo controllo

1. Scomponi la prima risposta in affermazioni verificabili.
2. Cerca attivamente evidenze contrarie che possano smentirla o renderla
   superata.
3. Riapri le fonti primarie e rifai i calcoli dagli input.
4. Usa un secondo modello soltanto come revisore aggiuntivo: il consenso tra
   modelli non sostituisce la prova.
5. Elenca le correzioni rispetto alla prima risposta.

## Evidenza nel dossier

Usa una tabella unica nel dossier del caso:

| Elemento | Identificativo | Affermazione/numero | Fonte primaria | Data fonte | Verifica | Calcolo | Esito |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Esito

- `PASSA`: ogni numero materiale e ogni strumento usato nel risultato ha prova
  corrente, calcolo coerente e stato/collocabilità compatibili con l'uso.
- `ESITO SOSPESO`: manca almeno una prova critica, lo strumento risulta
  `NON VERIFICATO` oppure le fonti divergono.

Con `ESITO SOSPESO`, prepara l'elenco preciso delle prove mancanti e la fonte
da consultare. Il report cliente nasce dalla versione `PASSA` validata dal
banker.
