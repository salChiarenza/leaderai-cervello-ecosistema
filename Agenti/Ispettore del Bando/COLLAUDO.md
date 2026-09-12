# Collaudo dell'Ispettore del Bando

## Perimetro

Il collaudo usa fascicoli sintetici, senza documenti o dati cliente. Verifica
che una pratica apparentemente ordinata non riceva un falso verde e che
l'agente completi il lavoro tecnico prima di coinvolgere il titolare.

## Prova senza la skill

Cinque esecuzioni indipendenti hanno rispettato firma e invio, ma hanno usato
verdetti incompatibili e non hanno prodotto un contratto comune tra fonti,
prove, quadratura e ricevuta. Questa variabilita ha fissato il bisogno di tre
soli verdetti e di un verificatore deterministico.

## Cicli rosso-verde

Le prove hanno prima riprodotto e poi chiuso questi falsi verdi:

- conteggi dichiarati senza lettura delle righe reali;
- piu gesti umani mostrati insieme;
- duplicati nascosti da percorsi equivalenti;
- numero fattura vuoto;
- firma dichiarata valida senza file CAdES, firmatario e ricevuta;
- salto diretto a `PRESENTATA` per aggirare la validazione della firma;
- fase `PRESENTATA` senza protocollo finale;
- spesa in attesa senza un quesito esterno tracciato;
- prospetto spese non coincidente con la propria evidenza integra e hashata;
- stessa fattura copiata con un nome diverso o chiave documento ripetuta;
- firma dichiarata non richiesta senza prova ufficiale collegata;
- file interno usato impropriamente come prova della fonte ufficiale;
- invio definitivo mascherato come scelta generica del titolare;
- pulsante finale descritto con parole diverse da invio o presentazione;
- testo operativo nascosto nel campo libero dell'oggetto;
- fase firma dichiarata pronta senza firma o gesto corrente;
- intero fascicolo spese disattivato con un flag non provato;
- conteggio e CSV ridotti insieme lasciando documenti fuori dall'indice;
- radici dell'inventario ristrette dal manifesto per nascondere sottocartelle;
- file con estensione diversa dal PDF escluso dal conteggio;
- documenti nascosti dietro sottocartelle collegate simbolicamente;
- stesso contenuto usato contemporaneamente come fattura e pagamento;
- stessa fattura o pagamento mascherati con identificativi Unicode equivalenti;
- fattura sostituita all'output finale da firmare o inviare;
- invio aperto senza pagamento provato o deroga ufficiale;
- nota interna usata per dichiarare il pagamento non richiesto;
- file CAdES valido ma riferito a un output originale diverso;
- date fittizie o timestamp privi di fuso per firma e pagamento;
- presentazione datata prima della firma o del pagamento;
- ricevuta di pagamento riferita a un avviso, importo o riferimento diverso;
- avviso di pagamento riutilizzato come propria ricevuta;
- ricevuta finale appartenente a un riepilogo o a una pratica diversa;
- file firmato riutilizzato come ricevuta di validazione;
- riepilogo inviato riutilizzato come ricevuta finale;
- stessa ricevuta riutilizzata tra firma, pagamento e protocollo;
- gesto di pagamento mostrato senza avviso, importo e riferimento provati;
- importi infiniti, non numerici o con precisione non monetaria;
- ricevuta di pagamento usata come riepilogo finale;
- ricevuta di firma usata come avviso di pagamento;
- file firmato usato come ricevuta di pagamento;
- artefatti critici riutilizzati tra i sette ruoli della pratica;
- fonte dichiarata verificata con data non valida o futura;
- identita pratica o versione schema assente/non supportata;
- firma proposta su un file integro ma non provato come output da firmare;
- dichiarazione proposta senza controllo preparatorio sullo stesso file;
- scelta proposta senza domanda o senza due-cinque opzioni distinte;
- opzioni di scelta duplicate nascoste da maiuscole o forme Unicode equivalenti;
- accesso o 2FA proposti senza preparazione provata sullo stesso oggetto;
- firma, pagamento e presentazione collocati nel futuro.

## Esito

Il 12/09/2026 la suite dedicata passa **67 prove su 67** e due collaudi ostili
indipendenti sul pacchetto finale concludono `PASS`. L'installazione nel computer
del destinatario resta una prova distinta: la consegna non vale come
installazione o utilizzo riuscito.
