# Procedura dell'Ispettore del Bando

## Risultato

Una pratica completa, coerente e provata, pronta al successivo gesto del
titolare oppure fermata da blocchi nominati con precisione. L'Ispettore lavora
sui file reali nel computer dell'impresa e non centralizza fascicoli, documenti
riservati o credenziali presso LeaderAI.

## 1. Fissa la fonte ufficiale corrente

Per ogni pratica apri e registra:

- pagina ufficiale dell'ente;
- testo integrale del bando e relativi aggiornamenti;
- modulistica ufficiale corrente;
- guida e campi reali del portale;
- calendario di precompilazione, apertura e chiusura;
- contatti ufficiali per i conflitti interpretativi.

Registra indirizzo e data di verifica. Se pagina, PDF, modulo e portale non
coincidono, non scegliere il dato piu comodo: apri un `BLOCCO` o una
`IN_ATTESA_ESTERNA` e conserva la risposta scritta.

## 2. Costruisci la matrice completa

La matrice comprende almeno:

| Area | Cosa provare |
|---|---|
| Impresa | identita, sede, dimensione, iscrizione, attivita, PEC, poteri di firma |
| Regolarita | diritto annuale, DURC, sicurezza, antimafia, polizze e altri requisiti richiesti |
| Aiuti | regime, de minimis, cumulo, premialita e dichiarazioni applicabili |
| Progetto | problema iniziale, tecnologia ammessa, attivita, persone, risultato misurabile e cronoprogramma |
| Fornitori | categoria ammessa, indipendenza, incarichi o certificazioni richiesti, preventivo e autodichiarazione |
| Spese | periodo, intestazione, valuta, imponibile/IVA, pagamento, unicita, pertinenza, CUP e rendicontabilita |
| Moduli | ogni campo, firma richiesta, allegato richiamato e coerenza incrociata |
| Portale | anagrafica, PEC, sezione corretta, campi, caricamenti, riepilogo e formato firme |
| Chiusura | bollo/pagamento, invio, ricevute, protocollo e fascicolo di rendicontazione |

Una voce passa a `PROVATO` soltanto se l'evidenza e leggibile, corrente,
intestata al soggetto giusto e riferita allo stesso output che sara usato.

## 3. Controlla fascicoli numerosi senza campionare

Quando esistono molte fatture e ricevute, indicizzale tutte. Per ogni coppia
ricostruisci almeno numero e data documento, fornitore, cliente, importo,
valuta, IVA, identificativo e data del pagamento. Segnala duplicati, note di
credito, rimborsi, abbonamenti che attraversano il periodo, valute estere,
documenti esteri, date di confine e riferimenti obbligatori mancanti.

La quadratura richiede:

- inventario completo delle cartelle canoniche `spese/fatture` e
  `spese/pagamenti`, senza filtro di estensione, uguale ai percorsi registrati
  nell'indice;
- numero atteso = fatture trovate = pagamenti trovati = coppie verificate;
- zero coppie irrisolte;
- totale ammesso e totale escluso separati;
- evidenza integra del prospetto usato.

La riconciliazione non decide da sola l'ammissibilita fiscale o amministrativa.
Quando serve giudizio professionale o dell'ente, prepara il quesito completo e
mantieni la voce `IN_ATTESA_ESTERNA` fino alla risposta scritta.

Non disattivare il controllo spese cancellando il fascicolo o impostando un
flag. `richieste: false` passa soltanto con il controllo canonico
`spese-non-richieste` e con la stessa evidenza integra censita tra le fonti
ufficiali.

## 4. Riapri gli output finali

Controlla i file esatti che entreranno nel portale, non le bozze da cui
derivano. Verifica nomi, intestazioni, codici fiscali/partite IVA, PEC, importi,
date, firma richiesta, numero pagine, allegati e coerenza tra moduli,
preventivi, progetto e portale.

Registra in `output_finale` le evidenze esatte dell'output da firmare e del
riepilogo finale da inviare. Il gesto umano deve puntare proprio a quelle
evidenze: non e valido sostituirle con una fattura, una bozza o un file diverso
anche se integro. Prima dell'invio, `riepilogo-finale` deve provarne la lettura;
il riepilogo deve avere identita e hash distinti da avvisi e ricevute.

Per le firme:

- identifica dalla fonte ufficiale il formato accettato;
- se la firma non e richiesta, prova questa eccezione con il controllo
  `firma-non-richiesta` e collega l'evidenza ufficiale esatta in
  `validazione_firma.fonte_non_richiesta_evidenza`;
- se e richiesto CAdES, il file finale deve essere `.p7m` e la firma va
  validata sul documento esatto;
- l'agente prepara e verifica; il titolare o delegato autorizzato applica la
  firma e conferma le dichiarazioni.

Dopo la firma conserva il file firmato e la ricevuta del verificatore come
evidenze distinte, registra formato, firmatario atteso e verificato, strumento,
data ISO con fuso ed esito. Registra inoltre l'evidenza originale e l'hash del
contenuto estratto dal `.p7m`: devono coincidere con l'output finale indicato
prima della firma. Solo allora aggiungi `validazione-firma-digitale` come
`PROVATO`. Finche questo controllo non passa, pagamento e invio finale restano
nascosti.

## 5. Lavora nel portale fino all'ultimo gesto

Il titolare gestisce identita digitale, 2FA e gesti irreversibili. Ricevuto
l'accesso, l'agente completa i campi e i caricamenti autorizzati, confronta il
riepilogo generato dal portale e aggiorna le impronte dei file finali.

La sequenza del manifesto e rigida: `preparazione` → `firma` → `pagamento` →
`invio` → `presentata`. Il pagamento e richiesto per impostazione predefinita:
prima dell'invio servono `pagamento-completato`, ricevuta integra, importo,
riferimento e timestamp ISO con fuso. Saltalo soltanto con
`pagamento-non-richiesto` collegato
alla fonte ufficiale esatta. In
ogni fase registra un solo gesto umano strutturato; i gesti futuri non restano
precompilati come `PASSAGGIO_UMANO`. Il verificatore scrive il testo da
`categoria_umana` e da `oggetto_evidenza`, che deve puntare a un file integro
richiamato dal controllo. Per una decisione prepara e censisce una scheda delle
opzioni: `scelta-da-compiere` prova lo stesso file e `scelta_titolare` registra
la domanda e da due a cinque opzioni distinte. Una dichiarazione usa allo stesso
modo `dichiarazione-da-confermare`. Il report rimanda al file provato, mai a un
comando libero verso il portale.

Prima dell'invio finale devono essere provati:

- sezione e pratica corrette;
- tutti i campi obbligatori;
- allegati caricati e leggibili;
- firme valide nel formato richiesto;
- importi e PEC coerenti;
- riepilogo finale riletto;
- pagamento completato e provato, oppure ufficialmente non richiesto.

Dopo l'invio scarica e verifica ricevuta, protocollo ed eventuale ricevuta di
pagamento. Il controllo `ricevuta-protocollo` deve richiamare l'evidenza esatta;
deve richiamare anche il riepilogo inviato. In `presentazione` registra hash del
riepilogo, identificativo della domanda atteso e letto nella ricevuta, numero di
protocollo, data con fuso orario e portale. I due identificativi devono
coincidere. Solo allora, e senza gesti umani ancora
pendenti, la fase puo diventare `PRESENTATA`. L'avviso e la ricevuta di
pagamento devono avere la stessa impronta di origine, importo e riferimento.
Le date devono rispettare la sequenza reale: firma validata, pagamento
eseguito, presentazione protocollata; nessuna puo essere nel futuro.

## 6. Prepara subito la rendicontazione

Dal primo giorno conserva regole e prove future: CUP, fatture e pagamenti,
quietanze, registri formazione e frequenza, relazioni dei fornitori, relazione
finale, nuovi assessment, continuita delle polizze e termini di conservazione.
Una spesa difficile da rendicontare non va nascosta dietro l'urgenza della
domanda.

## Errori che invalidano il verde

- fidarsi del nome del file senza aprirlo;
- campionare un fascicolo che deve essere completo;
- contare una dichiarazione orale come risposta dell'ente;
- usare una firma PAdES quando la procedura richiede CAdES o viceversa;
- dire `PRONTO` con coppie spesa non quadrate;
- contare due volte lo stesso documento cambiandone nome o percorso;
- ridurre insieme il CSV e il conteggio dichiarato lasciando documenti fuori;
- dichiarare che la firma non serve senza la fonte ufficiale integra;
- lasciare al titolare controlli che l'agente puo eseguire;
- mascherare firma, pagamento o invio come scelta generica del titolare;
- confondere caricamento con presentazione;
- modificare i file dopo la ricevuta senza rigenerarla.
