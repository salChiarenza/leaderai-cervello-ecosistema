# Sistema Portafogli Core-Satellite

Modulo operativo per private banker e consulenti finanziari che usano una
cartella Cervello + Ecosistema LeaderAI.

## Risultato

Il modulo collega fonti autorizzate, metodo del banker, calcoli verificabili,
costruzione Core-Satellite, revisione, backtest, monitoraggio e report cliente.

## Installazione agente

L'agente del cliente legge `INSTALLA_MODULO.md` e lavora sulla cartella viva.

Prima identifica la stanza che possiede davvero il processo. Il modulo non
assegna il nome della stanza e non installa una nuova skill per default.

Comando diretto:

```bash
python3 moduli/portafogli/installa_portafogli.py \
  --target "/percorso/cartella-madre" \
  --room "Portafoglio Modello"
```

## Calcoli

Dentro la stanza proprietaria scelta:

```bash
python3 portfolio_engine.py analizza --input DATI_PORTAFOGLIO.csv --output ANALISI.csv --report REPORT_CALCOLI.md
python3 portfolio_engine.py backtest --portfolio DATI_PORTAFOGLIO.csv --returns RENDIMENTI_MENSILI.csv --output BACKTEST.csv --report REPORT_BACKTEST.md --mode monthly-rebalanced
```

## Perimetro professionale

Il sistema prepara analisi e bozze tracciabili. Il banker valida adeguatezza,
strumenti, pesi, messaggio al cliente e firma.
