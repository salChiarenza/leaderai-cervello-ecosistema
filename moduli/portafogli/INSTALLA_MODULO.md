# Installazione guidata — Sistema Portafogli

## Missione

Lavora sulla cartella viva del proprietario. Usa questa repo come standard e
la cartella viva come caso reale.

1. Individua la cartella viva dai segnali di attività: istruzioni, memoria,
   fonti, report, file recenti e connettori provati.
2. Verifica che il Cervello passi il `CHECKUP.md` della repo. Ripara gli
   scostamenti tecnici riparabili e registra gli interventi.
3. Censisci le cartelle e le capacita' Portafogli gia' presenti. Classifica
   stanze, fonti, output, skill, script e archivi. Individua la stanza che
   possiede davvero la responsabilita' business, lo stato e le decisioni del
   processo: usa il suo nome e il suo percorso reali. Non promuovere
   `Portafoglio Modello` o un'altra cartella tecnica a stanza soltanto perche'
   contiene una pipeline completa.
4. Se esiste una skill equivalente, riusala e integra il gate
   `VERIFICA_FINANZIARIA.md`: la descrizione deve attivarla automaticamente
   quando compaiono numeri finanziari, fondi, titoli, ISIN o verifiche sullo
   stato di uno strumento. Se nessuna stanza puo' possedere la responsabilita'
   business, presenta al proprietario una proposta con stato, decisioni, scopo,
   fonti, output, monte/valle e collaudo. Crea la stanza solo dopo il suo ok.
5. Esegui sulla stanza scelta:

   ```bash
   python3 moduli/portafogli/installa_portafogli.py \
     --target "PERCORSO_CARTELLA_VIVA" \
     --room "PERCORSO_RELATIVO_STANZA"
   ```

   Usa `--create-room` soltanto se la nuova stanza e' stata approvata. Usa
   `--skill-name nome-scelto` soltanto se e' stata approvata una nuova skill.
6. Apri nella stanza scelta `AGENTS.md`, `VERIFICA_FINANZIARIA.md`,
   `PROCESSO.md` e `SCHEMA_DATI.md`.
   Prima di creare casi, riusa la convenzione della stanza; se non esiste,
   proponi al banker la struttura minima descritta in `AGENTS.md` e attendi il
   suo ok.
7. Compila `FONTI.md` usando percorsi realmente trovati e una prova innocua in
   lettura. Ogni fonte porta data e stato `OK`, `DA AGGIORNARE` o `DA COLLEGARE`.
8. Compila in bozza `METODO.md` e `CORE.md` con le decisioni già presenti nei
   file del proprietario. Segna `DECISIONE DEL BANKER` dove serve una scelta.
9. Crea un caso fittizio dai modelli CSV ed esegui `analizza` e `backtest`.
10. Prova il gate con almeno tre richieste:
    - un calcolo con percentuali o rendimento;
    - la ricerca di un fondo attivo e collocabile;
    - un fondo non verificabile, chiuso, incorporato o fuori catalogo.
    Il terzo caso deve produrre `ESITO SOSPESO`, con prova mancante o stato
    corrente esplicito.
11. Dalla radice prova una richiesta per ciascuna variante reale: l'agente deve
    trovare stanza, fonte, capacita' e output senza che gli venga suggerito il
    percorso.
12. Registra esito, file creati, prove, fonti e decisioni aperte in
   `logs/install-log.md` e nel report finale della missione.
13. Commit della cartella viva se il repository Git è già configurato. Mantieni
   dati personali e segreti fuori dal commit.
14. Completa il resoconto locale, mostralo al proprietario e chiedi
    autorizzazione esplicita all'invio. Fino al suo si' lo stato e'
    `PRONTO DA INVIARE`.
15. Solo dopo il si', invia davvero il resoconto a `sal@salchiarenza.ai`,
    archivia l'email della missione nello stesso giro e passa a `SAL_VERIFICA`.
16. Attendi `CONTINUA` oppure `CHIUDI`.

## Esito richiesto

Il resoconto include:

- cartella viva scelta e segnali usati;
- stanza proprietaria scelta, classificazione e collegamenti monte/valle;
- capacita' esistenti riusate e doppioni evitati;
- versione installata;
- file creati e file già presenti preservati;
- fonti trovate con prova e data;
- esito del gate su numeri e strumenti, con identita', stato e collocabilita'
  distinti;
- risultato dei due collaudi;
- risultato delle prove di instradamento dalla radice;
- decisioni richieste al banker;
- commit creato, se applicabile;
- stato `PASSA`, `PASSA CON ATTENZIONE` oppure `DA RIPARARE`.
