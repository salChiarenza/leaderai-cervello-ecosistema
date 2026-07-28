---
name: gestisci-portafoglio
description: Usa automaticamente il Sistema Portafogli quando un lavoro finanziario contiene numeri, prezzi, percentuali, rendimenti, costi, date, valute, benchmark, fondi, ETF, titoli, ISIN o ricerche sullo stato di uno strumento; usalo anche per costruzione Core-Satellite, analisi, riallineamento, backtest, monitoraggio, outlook e report cliente. Verifica fonti, calcoli, identità, stato corrente e collocabilità prima del risultato.
---

# Gestisci Portafoglio

1. Apri `ecosistema/ASSET.md` e individua la stanza proprietaria registrata per
   `Sistema Portafogli Core-Satellite`. Verifica che possieda una
   responsabilita' business, stato e decisioni: un nome di prodotto o modello
   con script e output non basta a dimostrare una stanza.
2. Apri l'`AGENTS.md` di quella stanza. Se il collegamento manca o e' rotto,
   censisci le stanze esistenti: quando una sola stanza possiede gia' processo,
   fonti e motore Portafogli, ripara il puntatore nei registri e provalo. Se la
   proprieta' e' ambigua o nessuna stanza e' adatta, fermati con stato
   `DA RIPARARE` e presenta la decisione al banker. Non creare una stanza per
   supposizione.
3. Leggi `VERIFICA_FINANZIARIA.md`, `METODO.md`, `FONTI.md`, `CORE.md` e la
   scheda del caso.
4. Scegli in `PROCESSO.md` la modalita' richiesta.
5. Applica il gate a ogni numero materiale e a ogni strumento citato,
   confrontato, cercato o proposto. Verifica identita', classe, valuta, stato
   corrente e collocabilita' separatamente.
6. Registra fonte primaria, data del dato, data/ora della verifica e ricalcolo
   nel dossier interno.
7. Esegui `portfolio_engine.py` per ogni numero calcolato destinato all'analisi
   o al report.
8. Esegui il secondo controllo cercando anche evidenze contrarie alla prima
   risposta. Un secondo modello e' un revisore aggiuntivo, non una fonte.
9. Con gate `ESITO SOSPESO`, elenca le prove mancanti e fermati prima del
   report cliente.
10. Con gate `PASSA`, prepara il dossier interno con fatti, ipotesi e decisioni
    del banker.
11. Genera il report cliente dalla versione validata dal banker.
12. Aggiorna lo storico del caso.

Ogni output indica data di riferimento, fonti, limiti e passaggio di validazione
professionale.
