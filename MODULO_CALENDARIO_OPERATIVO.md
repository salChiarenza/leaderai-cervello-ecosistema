# Modulo Calendario Operativo

Questo modulo organizza Google Calendar quando il cliente lavora guardando i
colori e l'agente deve leggere categorie affidabili.

## Missione

Creare o verificare un calendario operativo leggibile da persone e agente AI:

- persone: continuano a riconoscere i colori;
- agente: usa i colori solo se legge/scrive il valore tecnico e ha una legenda;
- fallback: se i colori non sono collaudabili, legge nome calendario, prefisso
  titolo, descrizione o etichetta;
- report: mostra prove reali, non auto-dichiarazioni.

Nota tecnica: Google Calendar API espone campi colore/label sugli eventi
(`colorId` e, per i colori/label piu' recenti, `eventLabelId`), ma non tutte le
superfici agente li mostrano o li scrivono nello stesso modo. Per questo decide
il collaudo, non l'ipotesi.

## Quando usarlo

Usalo se il cliente:

- ha un unico calendario con colori diversi;
- usa l'agenda per appuntamenti, produzione, scadenze o team;
- vuole che l'agente capisca che tipo di impegno sta leggendo;
- rischia di confondere "calendar collegato" con "calendar organizzato".

## Procedura

1. Verifica accesso reale a Google Calendar leggendo un evento vero, senza
   modificarlo.
2. Chiedi al cliente cosa significano i colori attuali.
3. Scrivi la legenda colori in forma macchina: colore/label tecnico -> nome
   umano -> significato operativo -> esempi.
4. Testa la legenda su eventi veri o test:
   - leggi colore/label di un evento esistente;
   - crea evento test con colore/label scelto;
   - rileggi l'evento test;
   - confronta il risultato con la legenda.
5. Se il test passa, mantieni il modello a colori e registra la legenda.
6. Se il test non passa, proponi massimo 6-8 calendari operativi, usando nomi
   chiari.
7. Se usi calendari separati, abbina a ogni calendario il colore che il team
   gia' riconosce.
8. Crea solo eventi test o nuovi eventi approvati.
9. Rileggi gli eventi creati e produci una tabella con prova.

Schema consigliato per atelier/negozi:

- Clienti / appuntamenti
- Prove abito
- Atelier / produzione
- Marketing / contenuti
- Amministrazione / fornitori
- Personale / blocchi

## Regole

- Non migrare eventi vecchi senza conferma esplicita.
- Non cancellare o spostare eventi esistenti nel primo blocco.
- Non usare il colore come fonte di verita' se non e' stato collaudato con
  legenda, lettura e scrittura.
- Non creare calendari per ogni micro-caso.
- Non dichiarare `ATTIVO` senza prova letta.

## Stati

- `NON SERVE`: il calendario non e' parte del lavoro operativo.
- `DA SCOPRIRE`: uso/colori non sono ancora chiari.
- `DA COLLAUDARE`: accesso o struttura presenti, ma senza prova.
- `INSTALLABILE`: il cliente autorizza creazione/riordino.
- `ATTIVO`: legenda colori collaudata oppure calendari/etichette creati o
  confermati; eventi test riletti e registrati.

## Dove registrare

- `ecosistema/FONTI.md`: Google Calendar collegato o da collegare.
- `ecosistema/ASSET.md`: calendari operativi, colori, proprietario, stato.
- `ecosistema/PROCESSI.md`: regole di naming e creazione eventi.
- `ecosistema/LIMITI.md`: cosa richiede conferma umana.
- `REPORT_FINALE.md`: tabella di prova e verdetto.

## Tabella di collaudo

| Modello | Colore/label | Calendario | Evento test | Prova letta | Stato |
|---|---|---|---|---|---|
| Legenda colori o calendari separati | da compilare | da compilare | da compilare | da compilare | DA COLLAUDARE |
