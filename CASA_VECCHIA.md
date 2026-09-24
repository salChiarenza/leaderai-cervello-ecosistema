# Hai la casa vecchia? Come aggiornarla

Versione corrente: `0.7.19`

Questa pagina serve quando nella cartella del proprietario c'e' gia' una casa
nata prima di questo metodo. La riconosci cosi': `VERSION` e' piu' vecchia di
`0.7.12` (per esempio `0.6.29`, `0.7.6` o `0.7.9`), oppure manca
`logs/install-state.json`, anche se un tentativo di aggiornamento ha gia'
scritto lo stato. Dentro
possono esserci programmi, guardiani, attivita', impostazioni e registro git
messi dalle versioni vecchie, e i file del pacchetto di allora
(`install_contract.json`, `PACKAGE_VERSION`): fino al 21/09/2026 il pacchetto
si estraeva dentro la casa.

Quella casa non si butta e non se ne crea una seconda accanto: si aggiorna, e
il vecchio si toglie soltanto dopo aver provato il nuovo. Tutto quello che serve
sta nella cartella `4 Gestione dell'ecosistema`:
<https://drive.google.com/drive/folders/1wdSNouSCbuF7G8Ab_m8R_Kw0uGnphc2Q>.

## Il lavoro

- **Da costruire:** la stessa casa portata al Passo 1 corrente, con i
  documenti nuovi del pacchetto e il blocco LEADERAI-CASA nelle istruzioni
  generali; il nome della cartella e il marchio sulle pagine che il
  proprietario ha gia' restano come sono. La versione nuova si scrive
  soltanto alla fine.
- **Da evitare:** perdere o cambiare le cose del proprietario (documenti,
  memoria, fonti, processi, note, pratiche, i suoi programmi e le sue
  attivita'); fermare quello che oggi gira e gli serve, come la copia di
  sicurezza, la manutenzione o le app installate a parte; cancellare qualcosa
  della casa; creare una seconda casa; rinominare la cartella o mettere il
  marchio sulle pagine e sugli script che il proprietario ha gia'.
- **Finito quando:** la copia completa e' stata fatta prima di tutto; il
  confronto finale dice che le cose del proprietario ci sono tutte, uguali a
  prima; una chat nuova nella casa risponde dai documenti; quello che girava
  prima gira ancora.

Il come lo decidi tu, guardando la casa vera: le case vecchie sono tutte
diverse e questa pagina non le elenca. Nel dubbio una cosa e' del proprietario
e resta com'e'. Se qualcosa non torna, scegli la strada che non perde niente,
annotala in `logs/install-log.md` e arriva in fondo.

## In sicurezza, in quest'ordine

1. **Copia completa, prima di tutto.** Fai un archivio zip datato dell'intera
   cartella cosi' com'e', compresi i file nascosti e la cartella `.git`, e
   mettilo fuori dalla casa (in Download o in una cartella scelta dal
   proprietario). Poi scrivi in `logs/install-log.md` l'elenco dei file della
   casa con la loro impronta: serve al confronto finale. La copia serve a
   tornare indietro: si tiene finche' il proprietario non ha usato la casa
   aggiornata per una settimana. Non e' la copia di sicurezza quotidiana:
   quella arriva con il Passo 4 del percorso.
   Dopo ogni passo di questa pagina scrivi nello stesso file a che punto sei:
   una sessione nuova riparte da li'. Prima di ripartire ricontrolla sulla casa
   vera i passi gia' fatti: se nel frattempo sono stati rimessi dei file (per
   esempio `AGENTS.md` dalla copia), rifai i passi che li riguardano.
2. **Applica il Passo 1 corrente.** Segui `01 - Cervello - installazione e
   aggiornamento`, ramo casa esistente: aggiungi i documenti mancanti del
   pacchetto corrente, non sostituire quelli compilati e non cambiare
   impostazioni del computer. I file del pacchetto vecchio rimasti nella casa
   (`install_contract.json`, `PACKAGE_VERSION`) sono di LeaderAI, non del
   proprietario: non si aggiornano e non fermano il lavoro. Se un guardiano o
   un'attivita' LeaderAI vecchia ti blocca, o rischia di rimettere le cose
   com'erano, mettila in pausa e annotalo. I programmi e le attivita' del
   proprietario non si fermano.
3. **Il marchio resta nei documenti nuovi.** Il marchio LeaderAI (in testa
   alle pagine `.md` la riga nascosta `<!-- LeaderAI · salchiarenza.ai -->`,
   negli script `# LeaderAI · salchiarenza.ai`) va soltanto nei documenti che
   il pacchetto aggiunge al passo 2, non su quelli che il proprietario ha
   gia'. Le pagine e gli script suoi restano come sono: niente riga aggiunta,
   niente «Ecosistema» o «EcosistemaAI» cambiato in «LeaderAI», niente nuova
   regola nel file che l'assistente legge all'avvio (`AGENTS.md` o
   `CLAUDE.md`). Puoi consigliare il marchio al proprietario; lo aggiungi sulle
   sue pagine soltanto se lo chiede lui. Non rinominare la cartella interna
   `ecosistema/`: i programmi la cercano con quel nome. Non toccare i
   documenti del proprietario (Word, Excel, PDF, immagini, esportazioni,
   programmi suoi): restano come sono.
4. **Il nome della cartella non cambia.** Anche se non comincia con
   `LeaderAI-`, la cartella resta come si chiama: rinominarla non e' un passo
   di questo aggiornamento e non e' un gesto che chiedi al proprietario per
   proseguire. Se e' lui a volerla rinominare di sua iniziativa, puoi
   consigliarlo su come farlo con sicurezza (copia prima, poi il cambio), mai
   imporlo. Se lo fa, controlla che tutto quello che puntava al vecchio
   percorso funzioni ancora: istruzioni generali e blocco LEADERAI-CASA,
   collegamenti sulla Scrivania, attivita' programmate, programmi del
   proprietario.
5. **Prova la base documentale.** Apri una chat nuova dentro la casa, senza
   chiedere altro al proprietario, e rispondi a tre domande: chi e' il
   proprietario, cosa c'e' in memoria, cosa e' stato fatto oggi. Le risposte
   devono venire dai documenti aggiornati.
6. **Confronta e, se serve, torna indietro.** Rifai l'elenco dei file con la
   loro impronta e confrontalo con quello del passo 1. Le cose del proprietario
   devono esserci tutte, con lo stesso contenuto: cambiano soltanto i
   documenti nuovi che il passo 2 ha aggiunto e le parti delimitate da
   LeaderAI nelle istruzioni generali. Controlla anche che quello che girava
   prima giri ancora. Se la prova del passo 5 o il confronto non tornano, ripristina la
   copia del passo 1, annota il punto che non ha funzionato e riprova senza
   eliminare nulla.
7. **Solo dopo, la tecnica vecchia.** Guardiani, attivita' e impostazioni
   LeaderAI delle versioni vecchie restano come sono se funzionano e servono al
   proprietario: si rivedono al Passo 4, uno per volta, e per ciascuno il
   proprietario deve vedere cosa fa, dove vive, come si prova e come si spegne.
   Metti da parte, senza cancellarli, soltanto quelli rotti o che non usa
   nessuno, e i file del pacchetto vecchio se nessun programma della casa li
   usa: vanno accanto alla copia, fuori dalla casa. Nelle impostazioni generali
   dell'assistente non devono restare pezzi LeaderAI che bloccano chat aperte
   altrove: resta soltanto il blocco LEADERAI-CASA che dice dov'e' la casa,
   nella forma scritta dal Passo 1. `AGENTS.md` e `CLAUDE.md` della casa non si
   archiviano mai: sono le regole che l'assistente legge da solo quando apre la
   casa. Se citano guardiani o programmi tolti, togli soltanto quelle righe. Le
   app installate a parte, come Voce, non sono vecchia tecnica della casa:
   restano come sono. Poi riaccendi quello che hai messo in pausa e controlla
   che giri.
8. **Il registro git resta se il proprietario lo usa, e non tiene comunque
   aperto il lavoro.** Guarda prima se lavora davvero con Git o GitHub (per
   esempio per aprire o aggiornare la casa dal telefono): in quel caso `.git` e
   `.gitignore` restano, non li tocchi e non proponi nemmeno di toglierli. Se
   invece sono li' soltanto per un vecchio modo di installare e nessun
   programma del proprietario li usa, la copia del passo 1 li conserva:
   scrivi la versione nuova, chiudi l'aggiornamento e poi, nel messaggio
   finale, chiedi il permesso di toglierli, come consiglio, non come passo
   obbligato: con il suo si' li cancelli tu, senza fargli cercare cartelle
   nascoste; con un no restano e la casa funziona lo stesso. Niente clone,
   pull o push richiesti da questo aggiornamento.
9. **Tieni una sola casa.** Se lavora da piu' computer, la casa vive in una
   cartella condivisa (OneDrive, Google Drive o iCloud) marcata «sempre
   disponibile offline» su ogni computer, una macchina alla volta. Per portarla
   li' la sposti, non la copi. Se sul computer trovi due case, non unirle da
   solo: fermati e prepara per il proprietario un'email a
   info@salchiarenza.com, oggetto «Ho due case», senza dati personali.

La prova del passo 5 e il confronto del passo 6 sostituiscono il vecchio
collaudo tecnico. Non aprire il Passo 4 durante questa migrazione.

## Alla fine

Di' al proprietario in una frase cosa hai fatto, e aggiungi questo consiglio con
queste parole: «Ti consiglio di tenere questa cartella dentro una cartella
online (OneDrive, Google Drive o iCloud) oppure di farne una copia ogni tanto.
Decidi tu.» E' un consiglio, non un obbligo: se sceglie di non farlo, la casa
funziona lo stesso. Se sceglie la cartella online, la casa si sposta, non si
copia: ne resta una sola.
