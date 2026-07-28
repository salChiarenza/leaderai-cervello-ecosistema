# Sistema Portafogli Core-Satellite

Modulo operativo per private banker e consulenti finanziari che usano una
cartella Cervello + Ecosistema LeaderAI.

## Risultato

Il modulo collega fonti autorizzate, metodo del banker, calcoli verificabili,
controllo corrente di identita', stato e collocabilita' degli strumenti,
costruzione Core-Satellite, revisione, backtest, monitoraggio e report cliente.

## Installazione agente

L'agente del cliente legge `INSTALLA_MODULO.md` e lavora sulla cartella viva.

Prima identifica la stanza che possiede davvero la responsabilita' business,
lo stato e le decisioni del processo. Una cartella chiamata `Portafoglio
Modello` non diventa stanza perche' contiene motori, fonti e report: resta una
capacita' finche' il banker non riconosce una funzione business autonoma. Il
modulo non assegna il nome della stanza e non installa una nuova skill per
default.

La skill esistente viene integrata con `VERIFICA_FINANZIARIA.md`; su una nuova
installazione il nome viene scelto esplicitamente. La descrizione della skill
attiva il controllo quando compaiono numeri finanziari, fondi, titoli, ISIN o
richieste sullo stato di uno strumento.

Comando diretto:

```bash
python3 moduli/portafogli/installa_portafogli.py \
  --target "/percorso/cartella-madre" \
  --room "PERCORSO_RELATIVO_STANZA_REALE"
```

## Calcoli

Dentro la stanza proprietaria scelta:

```bash
python3 portfolio_engine.py analizza --input DATI_PORTAFOGLIO.csv --output ANALISI.csv --report REPORT_CALCOLI.md
python3 portfolio_engine.py backtest --portfolio DATI_PORTAFOGLIO.csv --returns RENDIMENTI_MENSILI.csv --output BACKTEST.csv --report REPORT_BACKTEST.md --mode monthly-rebalanced
```

## Perimetro professionale

Il sistema prepara analisi e bozze tracciabili. Ogni report cliente richiede
gate finanziario `PASSA`; il banker valida adeguatezza, strumenti, pesi,
messaggio al cliente e firma.
