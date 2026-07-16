# Processo operativo Portafogli

## Gate 1 — Caso e fonti

1. Leggi la scheda cliente, profilo, obiettivi, orizzonte, liquidità e vincoli.
2. Apri le fonti registrate in `FONTI.md` e annota la data di verifica.
3. Confronta ogni strumento proposto con l'universo collocabile.
4. Registra dati mancanti e decisioni professionali richieste.

Esito: `PRONTO AI CALCOLI` oppure `DA COMPLETARE` con elenco preciso.

## Gate 2 — Normalizzazione

1. Porta il caso nel formato `DATI_PORTAFOGLIO.csv`.
2. Usa quantità, prezzo corrente e cambio espresso come EUR per unità di valuta.
3. Scrivi peso obiettivo in punti percentuali.
4. Per ogni satellite registra prezzo di riferimento e data della fonte.
5. Esegui il comando `analizza`.

Esito: quadratura al 100%, totale EUR, drift, importi e alert calcolati.

## Modalità A — Nuovo portafoglio

1. Seleziona il modello Core approvato per il profilo.
2. Applica i criteri satellite del metodo.
3. Prepara fino a tre alternative con differenze esplicite.
4. Esegui analisi e, quando disponibili le serie mensili, backtest.
5. Compila il dossier interno con fonti, ipotesi e punti da validare.
6. Registra la versione approvata dal banker.

## Modalità B — Revisione e riallineamento

1. Aggiorna prezzi, cambi e date.
2. Confronta peso attuale e peso obiettivo.
3. Valuta flussi in ingresso o uscita e vincoli del cliente.
4. Prepara gli importi di riallineamento e la motivazione di ogni intervento.
5. Porta la bozza alla validazione del banker.

## Modalità C — Backtest

1. Prepara `RENDIMENTI_MENSILI.csv` da fonti registrate.
2. Scegli la politica documentata: `monthly-rebalanced` oppure `buy-and-hold`.
3. Esegui il motore.
4. Riporta periodo, mesi coperti, rendimento cumulato, annualizzato e drawdown.
5. Dichiara ipotesi su costi, fiscalità, flussi e ribilanciamento.

## Modalità D — Report cliente

1. Usa esclusivamente la versione validata dal banker.
2. Trasferisci i numeri dagli output del motore.
3. Scrivi sintesi, andamento, allocazione, confronto, outlook e azioni.
4. Adatta il linguaggio al cliente.
5. Inserisci avvertenze e data di riferimento.
6. Esporta Word/PDF usando il modello approvato.

## Routine settimanale

1. Aggiorna prezzi, cambi e fonti dei satelliti.
2. Esegui `analizza`.
3. Evidenzia movimenti assoluti pari o superiori alla soglia registrata in `METODO.md`.
4. Prepara un elenco breve: fatto, impatto, azione da valutare.
5. Registra la revisione nello storico del caso.

## Aggiornamento annuale

1. Verifica catalogo collocabile e fonti.
2. Riesamina modelli Core, criteri satellite, benchmark, costi e soglie.
3. Aggiorna il modulo dalla repo e rilancia i test.
4. Esegui un caso campione e confrontalo con l'anno precedente.
5. Registra decisioni, versione e data di entrata in vigore.

## Chiusura del caso

Il caso è pronto per il cliente quando dati, calcoli, validazione del banker,
report e storico risultano allineati alla stessa data di riferimento.
