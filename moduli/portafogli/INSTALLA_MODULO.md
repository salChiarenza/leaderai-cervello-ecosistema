# Installazione guidata — Sistema Portafogli

## Missione

Lavora sulla cartella viva del proprietario. Usa questa repo come standard e
la cartella viva come caso reale.

1. Individua la cartella viva dai segnali di attività: istruzioni, memoria,
   fonti, report, file recenti e connettori provati.
2. Verifica che il Cervello passi il `CHECKUP.md` della repo. Ripara gli
   scostamenti tecnici riparabili e registra gli interventi.
3. Esegui:

   ```bash
   python3 moduli/portafogli/installa_portafogli.py --target "PERCORSO_CARTELLA_VIVA"
   ```

4. Apri `Costruzione Portafogli/AGENTS.md`, `PROCESSO.md` e `SCHEMA_DATI.md`.
5. Compila `FONTI.md` usando percorsi realmente trovati e una prova innocua in
   lettura. Ogni fonte porta data e stato `OK`, `DA AGGIORNARE` o `DA COLLEGARE`.
6. Compila in bozza `METODO.md` e `CORE.md` con le decisioni già presenti nei
   file del proprietario. Segna `DECISIONE DEL BANKER` dove serve una scelta.
7. Crea un caso fittizio dai modelli CSV ed esegui `analizza` e `backtest`.
8. Registra esito, file creati, prove, fonti e decisioni aperte in
   `logs/install-log.md` e nel report finale della missione.
9. Commit della cartella viva se il repository Git è già configurato. Mantieni
   dati personali e segreti fuori dal commit.
10. Archivia l'email della missione dopo averla gestita e invia davvero il
    resoconto a `sal@salchiarenza.ai` con lo stesso numero missione.
11. Attendi `CONTINUA` oppure `CHIUDI`.

## Esito richiesto

Il resoconto include:

- cartella viva scelta e segnali usati;
- versione installata;
- file creati e file già presenti preservati;
- fonti trovate con prova e data;
- risultato dei due collaudi;
- decisioni richieste al banker;
- commit creato, se applicabile;
- stato `PASSA`, `PASSA CON ATTENZIONE` oppure `DA RIPARARE`.
