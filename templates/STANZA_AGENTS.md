# {{room_name}}

Questa e' la mappa locale della stanza `{{room_name}}`.

## Stato corrente e prossimo passo

- Stato, prossimo passo, decisioni e scadenze si leggono e si aggiornano nella
  Fonte operativa dichiarata sotto.
- Questa mappa instrada e non diventa un secondo diario.

## Scopo

{{room_purpose}}

## Responsabilita business

{{room_business_responsibility}}

Descrivere la funzione aziendale riconosciuta dal proprietario, lo stato che
mantiene e le decisioni che governa. Elencare script, skill, modelli o output
non dimostra una stanza.

## Organigramma

- Ruolo: **Amministratore del settore `{{room_name}}`**.
- Riporta al **Boss dell'Ecosistema** definito nell'`AGENTS.md` della cartella
  madre.
- L'Amministratore governa stato, decisioni, fonti, capacita' e output del
  settore; coordina i suoi elementi subordinati e riporta al Boss risultati,
  blocchi e passaggi verso altri settori.
- Riporta al Boss senza duplicare nella mappa madre i dettagli operativi del
  settore.

## Dentro

- {{room_contents}}
- Ogni sottocartella diretta usa il formato: percorso tra apici inversi,
  seguito dalla sua funzione.
- Se non esistono sottocartelle, scrivere NESSUNA SOTTOCARTELLA.
- Un archivio di fascicoli puo' essere annidato: dichiarare il percorso locale
  seguito da ARCHIVIO PROTETTO: e dalla funzione; dichiarare anche la sua
  sottocartella diretta antenata. Tutti gli elementi devono
  essere esclusi da Git, assenti da indice e storia e senza collegamenti simbolici.
  Aggiungere FIRME SOTTOSCRITTORI solo per firme raccolte nei fascicoli, mai
  per firma, timbro o sigillo riutilizzabili dell'organizzazione.

## Fonti

- {{room_sources}}

## Output

- {{room_outputs}}

## Fonte operativa

- `{{room_operating_source}}`
- Deve esistere dentro questa stanza e mantenere, in testa, `Stato corrente`,
  `Prossimo passo`, `Decisioni` e `Scadenze`. Se non esiste gia', nasce dal
  calco `ecosistema/STANZA_FONTE.md` e riceve un nome che descrive la domanda
  business della stanza.

## Fonte business editabile

- {{room_business_source}}
- Se la stanza non genera documenti da contenuti business, scrivere
  `NON APPLICABILE` e motivare in una riga.
- La fonte puo' essere testo UTF-8 o Word .docx. Il percorso parte dalla stanza;
  il prefisso @/ parte dalla cartella madre. Deve restare nella stessa casa,
  senza collegamenti simbolici. Un generatore deve dichiarare la fonte reale.

## Capacita

- {{room_capabilities}}

## A monte

- {{room_upstream}}

## A valle

- {{room_downstream}}

## Dove scrivere

- Stato, procedure e output vivono nella fonte unica indicata in questa mappa.
- Le sottocartelle ordinarie appartengono a questa stanza e non diventano
  automaticamente nuove stanze.

## Manutenzione

- Responsabile: Amministratore del settore {{room_name}}; eredita il mandato operativo della stanza.
- Quando: alla nascita e prima di chiudere una modifica a struttura, istruzioni, fonti, capacita o collegamenti; nella misura giornaliera gia presente.
- Controlli: mappa, fonte unica, smistamento, dimensioni MD, duplicazioni e contraddizioni; ganci, skill, configurazioni e passaggi a monte/a valle. Eseguire il guardiano della casa e verificare nel contenuto i punti che la macchina non puo giudicare.
- Esiti: `{{room_operating_source}}`; data, evento, perimetro, difetti, correzioni, prova riletta e residui con responsabile. Conservare un solo stato corrente, storia utile nel diario.
- Infrastruttura: sottocartelle e strumenti del reparto ereditano questo responsabile; componenti comuni in Ecosystem Check e nei registri della casa. Nessun agente o timer per ogni cartella.

Alla nascita completare anche la prima prova richiesta -> fonte -> lavoro ->
output -> destinatario interno. Negli Esiti aggiungi `## Prova stanza: <nome-cartella>` con sei righe:
`Evento`, `Processo`, `Ingresso`, `Uscita`, `Destinatario`, `Verifica`.
Ingresso/Uscita/Destinatario citano ciascuno un file reale tra apici inversi,
con percorso dalla radice; ingresso e risultato sono distinti. Processo e
Verifica descrivono il lavoro fatto e il riscontro riletto (almeno 30 caratteri).
Mai precompilare un PASSA: una fonte vuota, una ricevuta mancante o file assenti
fermano la chiusura. Un reparto gia vivo registra l'adozione del controllo,
che non certifica retroattivamente i suoi processi business. Gli accessi
esterni non provati restano DA COLLEGARE. Una mappa compilata da sola non
certifica il funzionamento. L'Ispettore rilegge la prova e ripete un passaggio.

## Regole

- Prima di creare una cartella, classificarla come `STANZA`, `FONTE`, `OUTPUT`,
  `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO` o `SOSPETTA`.
- Non creare cartelle generiche, vuote o concorrenti.
- Non duplicare dati, stato, procedure o output gia' governati altrove.
- Non lasciare campi del calco non compilati: una stanza incompleta non viene
  salvata.
- Ogni sottocartella diretta e' dichiarata in `Dentro`; una cartella non
  dichiarata non ha proprietario e blocca il collaudo.
- Il contenuto business che il proprietario deve poter correggere vive in un
  file fonte esterno al codice e dichiarato in questa mappa. Codice e app lo
  leggono e generano PDF, Word o altri derivati; se la fonte manca, falliscono
  in modo visibile e non usano una copia hardcoded silenziosa.
- Nei file progetto lo stato corrente, il prossimo passo e le scadenze stanno
  in testa; il diario viene dopo ed e' ordinato dal piu' recente.
- Una nuova stanza nasce solo quando nessuna stanza esistente puo' possedere
  quella responsabilita' business e il proprietario approva la proposta
  strutturale.
- Una cartella con una pipeline completa di fonti, script, modelli e output
  resta `CAPACITA` se non mantiene stato e decisioni di una funzione business.
- `CLAUDE.md` in questa stanza contiene soltanto `@AGENTS.md`.

Il guardiano scrive una sola ricevuta `.agent/guardiano-ultimo-evento.json`
quando riceve Stop con sessione e casa: data, esito e impronte del codice.
`--misura` non la produce; un lancio manuale con payload puo produrla e non
prova l'origine automatica. L'Ispettore incrocia sessione e cronologia nativa,
controlla l'assenza di simulazioni manuali e confronta la ricevuta con
configurazione e codice attuali e distingue assenza, esito BLOCCO e prova
eseguita prima dell'ultima modifica; non dichiara un avvio da un file presente.

La ricevuta del guardiano documenta l'esecuzione, non certifica da sola chi
l'ha avviata. Per attestare un evento automatico, confronta sessione e ora
con la cronologia nativa e verifica che l'agente non abbia lanciato o scritto
manualmente la prova. Senza questa correlazione registra soltanto
«script eseguito, attivazione nativa da verificare».
