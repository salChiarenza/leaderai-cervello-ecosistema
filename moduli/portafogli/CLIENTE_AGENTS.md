# Costruzione Portafogli — contratto della stanza

## Scopo

Questa stanza prepara portafogli Core-Satellite, revisioni, backtest,
monitoraggio e report usando il metodo del banker e fonti autorizzate.

## Mappa

- `METODO.md`: decisioni professionali e criteri del banker.
- `FONTI.md`: percorsi veri, proprietari, frequenza e data di verifica.
- `CORE.md`: modelli Core approvati e pesi.
- `PROCESSO.md`: sequenza operativa completa.
- `SCHEMA_DATI.md`: campi obbligatori e unità.
- `portfolio_engine.py`: fonte dei calcoli numerici.
- `SCHEDA_CLIENTE_MODELLO.md`: calco per ogni caso.
- `REPORT_INTERNO_MODELLO.md`: dossier decisionale del banker.
- `REPORT_CLIENTE_MODELLO.md`: struttura del documento cliente.

## Ordine di lavoro

1. Leggi `METODO.md`, `FONTI.md`, `CORE.md` e la scheda del caso.
2. Verifica fonti, date, valute, ammissibilità e campi obbligatori.
3. Normalizza i dati secondo `SCHEMA_DATI.md`.
4. Esegui il motore e conserva CSV e report prodotti.
5. Prepara alternative e motivazioni distinguendo fatti, ipotesi e decisioni.
6. Porta il dossier interno al banker.
7. Genera il report cliente sulla versione approvata.
8. Aggiorna storico e prossima revisione.

## Regole professionali

- Il catalogo collocabile registrato in `FONTI.md` definisce l'universo delle proposte.
- Ogni prezzo, cambio, rendimento e dato di mercato porta fonte e data.
- Il motore esegue i calcoli; il testo cita i suoi output.
- Dati incompleti producono una richiesta precisa o uno stato `DA COMPLETARE`.
- Marco valida adeguatezza, strumenti, pesi, raccomandazione e firma.
- I dati cliente restano nella cartella autorizzata e nei limiti privacy aziendali.
- Ogni output destinato al cliente include le avvertenze approvate dal banker.

## Struttura dei casi

Quando parte un caso reale, crea `clienti/<codice-anonimo>/` con almeno:

- `SCHEDA.md`
- `DATI_PORTAFOGLIO.csv`
- `STORICO.md`

Gli output del motore e i report restano nello stesso caso. Il codice anonimo
mantiene i nomi personali fuori da file riusabili o condivisibili.
