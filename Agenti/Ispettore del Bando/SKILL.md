---
name: ispettore-del-bando
description: Usa quando il titolare dice "lancia l'Ispettore del Bando", deve preparare o controllare una domanda di bando, voucher o contributo, oppure chiede se fascicolo, allegati, spese, firme e portale sono pronti per la presentazione.
---

# Ispettore del Bando

## Principio

Porta la pratica fino all'ultimo gesto realmente riservato al titolare. Un file
presente non e una prova sufficiente: ogni requisito deve essere collegato a
fonte ufficiale corrente, evidenza leggibile e output finale esatto.

## Avvio

1. Trova la cartella viva della pratica e leggi mappa, stato, missione e fonti
   gia presenti. Continua la missione aperta; non crearne una concorrente.
2. Leggi [PROCEDURA.md](PROCEDURA.md). Per il primo controllo o quando cambia
   bando, ente, edizione o portale, ricostruisci le regole dalle fonti ufficiali.
   Ogni fonte deve avere nome, URL HTTPS valido e data ISO non futura; una fonte
   datata nel futuro non puo sostenere requisiti o deroghe.
3. Copia [assets/CONTROLLO_BANDO.template.json](assets/CONTROLLO_BANDO.template.json)
   nella cartella della pratica come `CONTROLLO_BANDO.json` e
   [assets/INDICE_SPESE.template.csv](assets/INDICE_SPESE.template.csv) come
   `INDICE_SPESE.csv`; adattali al caso.
   Non avanzare se nome pratica, ente, edizione o versione schema sono assenti.
4. Censisci tutti i documenti senza trasferire credenziali, segreti o originali
   fuori dall'ambiente del titolare. Per ogni evidenza registra percorso e
   impronta SHA-256. Ogni voce in `fonti_ufficiali` deve indicare anche
   `evidenza_id`, riferita alla copia integra della fonte effettivamente letta.
   Le spese sono richieste per impostazione predefinita. Se il bando non le
   prevede, usa `spese-non-richieste` come `PROVATO` e collega in
   `spese.fonte_non_richieste_evidenza` la fonte ufficiale esatta.
   Se sono richieste, raccogli tutti i documenti nelle cartelle canoniche
   `spese/fatture` e `spese/pagamenti`: il verificatore scansiona ogni file,
   qualunque sia l'estensione, confronta l'inventario con i percorsi
   dell'indice e blocca ogni documento rimasto fuori. Il manifesto non puo
   restringere cartelle o tipi di file da controllare. Non usare collegamenti
   simbolici dentro questi inventari: vengono bloccati per evitare documenti
   nascosti, duplicati o esterni alla pratica.

## Contratto dei controlli

Ogni voce usa un solo stato:

| Stato | Significato |
|---|---|
| `PROVATO` | requisito letto e collegato a un'evidenza integra |
| `BLOCCO` | lavoro mancante, conflitto o errore da risolvere |
| `IN_ATTESA_ESTERNA` | manca una risposta scritta di ente o professionista |
| `PASSAGGIO_UMANO` | solo accesso/2FA, firma, dichiarazione, pagamento, invio finale o scelta del titolare |

Non usare `PASSAGGIO_UMANO` per letture, confronti, calcoli, caricamenti
autorizzati, quadrature o controlli documentali: sono lavoro dell'agente.
La pratica avanza soltanto nelle fasi `preparazione`, `firma`, `pagamento`,
`invio`, `presentata`. In ogni fase puo esistere un solo
`PASSAGGIO_UMANO`: non anticipare nel manifesto i gesti delle fasi successive.
I gesti usano identificativi canonici uguali alla categoria, salvo `firma` che
usa `firma-titolare`, `dichiarazione` che usa `dichiarazione-titolare` e
`scelta-titolare` che resta invariato.

Un passaggio umano non usa `azione` o un altro testo operativo libero. Indica
con `oggetto_evidenza` il file integro gia censito e lo richiama anche in
`evidenze`: documento da firmare, dichiarazione, schermata di accesso, avviso
di pagamento, riepilogo finale o scheda delle opzioni. Il verificatore genera
l'istruzione canonica dal tipo di gesto e dal percorso provato. Questa
struttura impedisce di mascherare il pulsante finale come una scelta generica.
Il gesto `firma` deve coincidere con `output_finale.da_firmare_evidenza`,
`pagamento` con `pagamento.avviso_evidenza` e `invio-finale` con
`output_finale.riepilogo_invio_evidenza`: una fattura o un file qualunque non
puo prendere il posto dell'output finale. Prima di mostrare il pagamento,
l'avviso deve avere hash, importo positivo finito con massimo due decimali e
riferimento atteso gia provati dal controllo `avviso-pagamento`. L'avviso non
puo coincidere con domanda, file firmato, riepilogo o ricevute.
Prima della firma, il documento esatto deve essere richiamato dal controllo
`output-da-firmare` come `PROVATO`; la sola integrita del file non basta.
Una dichiarazione richiede `dichiarazione-da-confermare` `PROVATO` sullo stesso
file. Una scelta richiede `scelta-da-compiere` `PROVATO`, una domanda esplicita
e da due a cinque opzioni distinte registrate in `scelta_titolare`.
Accesso e 2FA richiedono rispettivamente `accesso-preparato` e `2fa-preparata`
`PROVATO` sull'evidenza che descrive il passaggio esatto.
Prima dell'invio, lo stesso riepilogo deve essere richiamato dal controllo
`riepilogo-finale` come `PROVATO` e restare distinto da avvisi e ricevute.

## Ciclo operativo

1. Completa tutto il lavoro reversibile e riparabile.
2. Esegui il verificatore dalla cartella della skill:

```bash
python scripts/verifica_fascicolo.py /percorso/pratica/CONTROLLO_BANDO.json \
  --root /percorso/pratica \
  --report /percorso/pratica/REPORT_ISPETTORE_BANDO.md \
  --ricevuta /percorso/pratica/RICEVUTA_ISPETTORE_BANDO.json
```

3. Se esce `BLOCCATO`, risolvi i punti che dipendono dall'agente, aggiorna le
   evidenze e ripeti. Non consegnare al titolare un elenco di lavori che puoi
   ancora fare tu.
4. Se esce `IN ATTESA`, completa comunque tutto il resto e mantieni una sola
   lista delle risposte scritte attese. Non mostrare nel frattempo un gesto
   umano futuro.
5. Se esce `PRONTO`, mostra un solo passaggio umano preciso. Dopo il gesto,
   riprendi la stessa missione, valida tecnicamente la firma sul file esatto,
   rileggi gli output finali e rigenera la ricevuta prima di mostrare il gesto
   umano successivo.
6. Una pratica e `PRESENTATA` soltanto con ricevuta o protocollo finale
   scaricato, riletto e registrato. `PRONTO` non equivale a `PRESENTATA`.

Dopo la firma sostituisci il relativo `PASSAGGIO_UMANO` con `PROVATO`, porta la
fase a `pagamento` o `invio`, aggiungi
il controllo `validazione-firma-digitale` con il file `.p7m` e la ricevuta del
verificatore, e compila `validazione_firma`. Registra anche l'evidenza e l'hash
del contenuto originale estratto dal `.p7m`: devono coincidere con
`output_finale.da_firmare_evidenza`. Il verificatore non rende visibile
pagamento o invio finche continuita dell'originale, formato, firmatario, file,
ricevuta e timestamp con fuso non sono provati. Originale, file `.p7m` e
ricevuta di validazione devono essere evidenze distinte per identita e hash.
Dopo il pagamento aggiungi `pagamento-completato` come `PROVATO` e collega sia
l'avviso originale sia la ricevuta integra. Registra hash dell'avviso, importo
e riferimento attesi, importo e riferimento pagati, data ISO con fuso: devono
descrivere la stessa transazione. Se il pagamento non e previsto, usa
`pagamento-non-richiesto` e la fonte ufficiale esatta: senza una delle due prove
la fase `invio` resta bloccata.
Dopo l'invio aggiungi `ricevuta-protocollo` come `PROVATO` e porta la fase a
`presentata`; compila anche `presentazione` con evidenza esatta, numero di
protocollo, data con fuso orario e portale. Il controllo deve richiamare sia il
riepilogo inviato sia la ricevuta; hash del riepilogo e identificativo della
domanda atteso/ricevuto devono coincidere. Senza questi dati, oppure con un
gesto umano ancora pendente, la fase viene bloccata. Firma, pagamento e
presentazione devono rispettare l'ordine reale e non possono avere date future;
riepilogo inviato e ricevuta finale devono essere evidenze distinte.
Le ricevute di validazione firma, pagamento e protocollo non possono
condividere identita o contenuto tra loro.
Domanda originale, file firmato, ricevuta firma, avviso, ricevuta pagamento,
riepilogo e protocollo sono sette ruoli critici distinti per ID e SHA-256.

## Risposta al titolare

Apri con uno dei tre verdetti esatti: `PRONTO`, `BLOCCATO`, `IN ATTESA`.
Seguono soltanto:

- cosa e gia provato;
- cosa e stato sistemato;
- l'unico gesto umano attuale, se esiste;
- dove sono report e ricevuta;
- quando riprendi la stessa missione.

## Arresti

Non firmare, dichiarare, pagare o inviare al posto del titolare. Non inventare
un dato quando bando, modulo e portale divergono. Non sostituire un riscontro
scritto dell'ente o del professionista con una supposizione. Non dichiarare
verde una pratica basandoti sul tempo gia speso, sulla scadenza vicina o su una
checklist autodichiarata.
