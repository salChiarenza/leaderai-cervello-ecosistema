# Sistema Portafogli — contratto della stanza proprietaria

## Stato corrente e prossimo passo

- Stato: dichiarato nel file del caso attivo.
- Prossimo passo: dichiarato nel file del caso attivo.
- Scadenze: prossima revisione e responsabile restano in testa al caso.

## Scopo

Questa stanza possiede il processo Portafogli e prepara portafogli
Core-Satellite, revisioni, backtest, monitoraggio e report usando il metodo del
banker e fonti autorizzate. Il suo nome deriva dall'ecosistema reale del
proprietario.

## Dentro

- `METODO.md`: decisioni professionali e criteri del banker.
- `FONTI.md`: percorsi veri, proprietari, frequenza e data di verifica.
- `CORE.md`: modelli Core approvati e pesi.
- `VERIFICA_FINANZIARIA.md`: gate obbligatorio per numeri, strumenti, stato e
  collocabilità.
- `PROCESSO.md`: sequenza operativa completa.
- `SCHEMA_DATI.md`: campi obbligatori e unità.
- `portfolio_engine.py`: fonte dei calcoli numerici.
- `SCHEDA_CLIENTE_MODELLO.md`: calco per ogni caso.
- `REPORT_INTERNO_MODELLO.md`: dossier decisionale del banker.
- `REPORT_CLIENTE_MODELLO.md`: struttura del documento cliente.

## Fonti

- `FONTI.md`, mandato e dati del caso autorizzato.
- Dati di mercato con fonte e data.

## Output

- Calcoli, dossier interno, report cliente e storico delle revisioni.

## Fonte business editabile

- `METODO.md`, `CORE.md`, `REPORT_INTERNO_MODELLO.md` e
  `REPORT_CLIENTE_MODELLO.md`; il motore produce derivati e non mantiene una
  seconda copia dei contenuti nel codice.

## Capacita

- Motore numerico, skill gia' presenti e procedure registrate in questa stanza.
  Sono capacita' della stanza, non stanze separate.

## A monte

- Compilare con le stanze e le fonti che forniscono mandato, universo, dati
  cliente e dati di mercato.

## A valle

- Compilare con le stanze o gli output che ricevono dossier, report, storico e
  prossime revisioni.

## Dove scrivere

- Stato, prossimo passo e scadenze nel file del caso attivo.
- Fonti in `FONTI.md`; calcoli e report nella convenzione casi approvata.
- Questa stanza deve essere raggiungibile dall'`AGENTS.md` della cartella madre.

## Ordine di lavoro

1. Leggi `VERIFICA_FINANZIARIA.md`, `METODO.md`, `FONTI.md`, `CORE.md` e la
   scheda del caso.
2. Verifica fonti, date, valute, identità, stato, collocabilità e campi
   obbligatori.
3. Normalizza i dati secondo `SCHEMA_DATI.md`.
4. Esegui il motore e conserva CSV e report prodotti.
5. Prepara alternative e motivazioni distinguendo fatti, ipotesi e decisioni.
6. Porta il dossier interno al banker.
7. Genera il report cliente sulla versione approvata.
8. Aggiorna storico e prossima revisione.

## Regole professionali

- Il catalogo collocabile registrato in `FONTI.md` definisce l'universo delle proposte.
- Ogni numero materiale e ogni strumento attivano il gate di
  `VERIFICA_FINANZIARIA.md`.
- Ogni prezzo, cambio, rendimento e dato di mercato porta fonte, data e
  ricalcolo quando applicabile.
- Esistenza dello strumento e collocabilità sono prove distinte.
- Il motore esegue i calcoli; il testo cita i suoi output.
- Dati o stati critici incompleti producono `ESITO SOSPESO` con la prova da
  recuperare.
- Il banker valida adeguatezza, strumenti, pesi, raccomandazione e firma.
- I dati cliente restano nella cartella autorizzata e nei limiti privacy aziendali.
- Ogni output destinato al cliente include le avvertenze approvate dal banker.

## Struttura dei casi

Prima censisci come la stanza organizza gia' i casi reali. Riusa nomi, percorsi
e registri esistenti quando consentono di distinguere almeno:

- scheda e mandato del caso;
- dati di portafoglio usati dal motore;
- storico delle decisioni e delle revisioni;
- output numerici e report approvati.

Se la stanza non ha ancora una convenzione, proponi al banker una struttura
minima, per esempio `clienti/<codice-anonimo>/` con `SCHEDA.md`,
`DATI_PORTAFOGLIO.csv` e `STORICO.md`. Creala solo dopo approvazione. Il codice
anonimo mantiene i nomi personali fuori da file riusabili o condivisibili.
