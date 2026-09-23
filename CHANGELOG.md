# Changelog

## 0.7.17 - 23/09/2026

- **Una casa sola, in qualunque cartella si apra l'AI (P-087).** La persona non
  sceglie piu' cartelle: prima di scrivere, l'assistente cerca la casa su tutto
  il computer, cartelle online comprese, dal contenuto e non dal nome; Cestino e
  pacchetto scaricato non contano. Una casa: la aggiorna dov'e'. Piu' case: non
  le tocca e prepara l'email «Ho due case». Nessuna: la crea nella cartella
  utente. Nato dalle due voci della casa nell'app di Caterina Mencarini (23/09), poi risultate la
  stessa cartella: il buco della guida era reale comunque (stessa famiglia di P-053).
- **Torna il biglietto della casa.** Il blocco `LEADERAI-CASA` nelle istruzioni
  generali dell'assistente (Claude Code e Codex/ChatGPT Work) dice in ogni chat
  che la casa e' la casa di tutto il lavoro. Lo chiede la persona nel messaggio
  che incolla, non il pacchetto: il 16/09 la stessa modifica chiesta dal
  documento scaricato faceva bloccare l'installazione a Claude. Non ferma le chat
  aperte altrove: le fa lavorare nella casa. Solo istruzioni, nessun gancio.
- **La casa si sposta, non si copia**, anche quando va in una cartella online.
- **La casa non e' piu' muta (P-083).** Il Passo 1 crea `AGENTS.md` (letto da
  Codex e ChatGPT Work) e `CLAUDE.md` (che per Claude richiama `AGENTS.md`): chi
  apre la casa trova subito cosa leggere. Le case nate con la 0.7 li ricevono con
  l'aggiornamento; nella pagina delle case vecchie non si archiviano mai. Caso
  vero: Giovanni Leto, casa aggiornata e poi muta.

## 0.7.16 - 21/09/2026

- **Una fase, una promessa.** Il Passo 1 consegna soltanto la base documentale;
  stanze e primo processo arrivano nel Passo 3, mentre backup, guardiani, skill,
  automazioni e impostazioni entrano soltanto nel Passo 4, separatamente e con
  scelta visibile della persona.
- **La casa vecchia non installa piu' la tecnica prima della base.** Prima mette
  al sicuro i dati, applica e prova il Passo 1; soltanto dopo separa i vecchi
  componenti. La nuova tecnica si valuta piu' avanti nel Passo 4.
- **La cartella del cliente non contiene piu' il motore LeaderAI.** La sorgente
  tecnica viene pubblicata in una cartella sorella privata; il link pubblico
  mostra soltanto percorso, pacchetto e prodotti destinati al cliente.

## 0.7.15 - 21/09/2026

- **Il pacchetto ha un'impronta.** A ogni pubblicazione il costruttore scrive
  nella guida l'impronta SHA-256 di `Cervello.zip`, anche dentro il messaggio da
  incollare: l'assistente la confronta con il file scaricato e un pacchetto
  alterato, incompleto o vecchio non passa (parere esterno del 21/09).
- **Il nome si chiede solo se l'utente del computer non e' un nome vero**
  (Utente, User, admin, o il nome di un altro): una domanda sola, alla fine.
  Casi veri: «Utente» e «cecilia».
- **Provenienza nel registro di installazione:** il pacchetto viene dalla
  cartella `1 Cervello` del Drive LeaderAI.

## 0.7.14 - 21/09/2026

- **Case vecchie: il vecchio si toglie solo dopo aver provato il nuovo.** Dal
  parere esterno del 21/09: prima inventario e copia completa della cartella
  cosi' com'e' (file nascosti e registro git compresi), attivita' giornaliera in
  pausa, poi copia di sicurezza quotidiana, guardiani, documenti nuovi e guida;
  il registro git si toglie soltanto dopo una prova dalla casa aggiornata, e la
  copia completa resta per tornare indietro.
- **Il nome non si cerca nei documenti del computer.** L'assistente lo prende da
  cio' che il proprietario ha scritto nella chat o dall'utente del computer;
  l'attivita' si scrive quando il proprietario la dice.

## 0.7.13 - 21/09/2026

- **La guida dice di nuovo chi l'ha scritta.** In testa alla guida pubblicata
  torna il blocco di provenienza: autore, cosa contiene il pacchetto, cosa
  l'assistente non fa, ispezionare e poi andare avanti. Era nella guida tecnica
  0.6.29 ed era rimasto fuori dalla guida breve pubblicata dalla 0.7.1: due
  assistenti puliti provati il 21/09 si sarebbero fermati a chiedere «chi te
  l'ha mandato?».
- **Il messaggio da incollare porta l'autorizzazione della persona** e il
  collegamento diretto al pacchetto: l'assistente che vede solo il blocco sa
  chi lo autorizza e dove scaricare. Su ChatGPT Work la persona dice si' alla
  richiesta di usare internet.
- **Il nome del proprietario lo trova l'assistente**, dall'utente del computer o
  dai documenti presenti; domandarlo non e' il primo passo (decisione di Sal).
- **Il pacchetto si estrae in Download e si cancella alla fine**: non resta
  nella casa (caso Zedda, 21/09).
- **Pagina «Hai la casa vecchia? Come aggiornarla»** in `1 Cervello`: copia di
  sicurezza, via il registro git, guardiani provati (su Windows `py`), guardiani
  solo nella casa, documenti nuovi di gestione, poi la guida normale. Prima
  viaggiava in email scritte a mano (Corroppoli, 18/09).
- **Consiglio, non obbligo.** Alla fine l'assistente consiglia cartella online o
  copia ogni tanto; la scelta resta al proprietario (Sal, 21/09).
- **Cosa vede la persona alla fine**: nove documenti con tabelle ancora vuote,
  ed e' giusto cosi'. La guida glielo fa dire.

## 0.7.12 - 21/09/2026

- **Stesso pacchetto per installare, aggiornare o riprendere.** L'assistente
  scarica sempre il pacchetto corrente come riferimento, riconosce la casa
  reale e non lo copia sopra ai documenti del cliente.
- **Windows non crea piu' `Cervello/Cervello`.** I file dello ZIP sono alla
  radice: `Estrai tutto` crea un solo involucro. I vecchi pacchetti con il
  livello interno restano riconoscibili.
- **La versione viene dichiarata soltanto alla fine.** Il pacchetto porta
  `PACKAGE_VERSION`; `VERSION` nasce o cambia dopo il controllo dei file
  richiesti e dei contenuti conservati. Una casa vecchia non puo' sembrare
  aggiornata solo perche' le e' stato scritto il numero nuovo.
- **Una sessione interrotta riparte.** `logs/install-state.json` viene scritto
  prima delle modifiche e aggiornato dopo ogni file. Fino a `COMPLETED`, il
  giro successivo continua dal lavoro rimasto e non apre una seconda casa.
- **I documenti del cliente restano suoi.** I file esistenti non vengono
  sostituiti; il contratto permette di aggiornare soltanto blocchi LeaderAI
  delimitati. Il primo blocco gestito porta nel censimento il passaggio per
  aggiungere e provare separatamente piu' Gmail.
- Prova deterministica del pacchetto su installazione nuova, casa 0.7.10,
  interruzione/ripresa, vecchio ZIP annidato e contenuti cliente preservati.

## 0.7.11 - 21/09/2026

- **Le carte dell'armadio non aspettano piu' che qualcuno si ricordi di
  aprirle.** Nella casa del cliente stavano nove carte. Solo tre avevano
  qualcuno che le metteva davanti all'assistente al momento giusto: manuali,
  memoria, note fra assistenti. Le altre sei - limiti, cosa e' acceso,
  guardiani, come e' messa in piedi, passaggi, soggetti - esistevano, il
  controllo verificava che ci fossero, e nessuno ci mandava mai nessuno.
  Esserci non e' funzionare.
- **Guardiano Carte** (`guardiano_carte.py`, UserPromptSubmit, acceso in tutte
  e due le case): il proprietario descrive un sintomo, l'assistente si vede
  arrivare davanti la carta che lo risolve. Legge la tabella dei sintomi in
  `ecosistema/COME_E_MESSA_IN_PIEDI.md`: una riga nuova li' si accende da sola,
  senza toccare il programma. Massimo due carte per volta; serve piu' di una
  parola in comune, altrimenti un'assonanza aprirebbe la carta sbagliata.
- **Ogni carta dice da sola quando si apre:** riga `Quando si apre:` sotto il
  titolo delle sei carte, in parole del proprietario.
- **Se qualcosa non va, la porta manda da qualche parte.** La mappa madre
  rimanda a «Come e' messa in piedi questa casa», che porta la tabella
  sintomo -> carta e, se l'assistente resta fermo lo stesso, l'assistenza
  LeaderAI con l'indirizzo: prima non c'era scritto da nessuna parte a chi
  scrivere.
- **Checkup, punto 8:** il controllo non misura piu' solo che le carte
  esistano, ma che ognuna porti il suo «Quando si apre» e sia raggiungibile
  dalla tabella dei sintomi.
- 583 prove verdi (da 572), piu' l'installazione provata su una casa vera con
  tutti e due gli assistenti.
- **Il controllo smette di fidarsi della prosa.** L'Ispettore adesso misura da
  solo cio' che il checkup chiedeva a parole: ogni carta porta la sua riga
  «Quando si apre» in testa e la tabella dei sintomi la nomina; una riga sepolta
  in fondo o un segnaposto non passano.
- **Guardiano installato e mai chiamato = guasto.** Nuovo controllo che confronta
  i programmi presenti nella casa con quelli davvero richiamati dalle
  impostazioni dei due assistenti. E' il caso P-054 del 19/09, dove sei guardiani
  su otto erano spenti e la prova era verde lo stesso. Una casa installata per un
  solo assistente non viene accusata.
- **Il divieto di git arriva anche dove era rimasto scritto il contrario.** La
  decisione del 16/09 (la casa del cliente non e' un registro di modifiche) era
  nella guida ma non nelle istruzioni interne del prodotto, che ordinavano ancora
  di inizializzare la cartella come repository e di fare il primo commit; il
  collaudo dell'installazione pretendeva quel commit. Tolti tutti e tre, e la
  prova ora verifica il divieto invece del commit.
- 594 prove verdi.

- **Nasce lo sportello `assistenza/` nella casa del cliente.** L'assistente che
  si blocca entra da li': i manuali ufficiali con il loro «quando si apre», la
  tabella che lega ogni sintomo alla carta giusta, e a chi scrivere se resta
  fermo. Il materiale e' stato spostato, non copiato: le vecchie sezioni sono
  sparite dalle carte dove stavano, e i due guardiani, l'Ispettore, la mappa
  madre, il contratto di installazione e le prove sono stati ripuntati. Una
  prova nuova legge tutti i documenti del prodotto e boccia la stessa tabella
  scritta in due posti.
- **Niente disco esterno per la copia di sicurezza.** La cartella deve essere
  sincronizzata (iCloud, Drive, OneDrive): un disco esterno non si condivide e
  non si raggiunge da un secondo computer.
- 603 prove verdi, piu' l'installazione reale su una casa di prova con i due
  assistenti e i guardiani lanciati a mano dal suo interno.

- Registrato come P-061 nel foglio dei problemi.

## 0.7.10 - 19/09/2026

- **I guardiani stanno solo nella casa.** Un partecipante della Challenge
  (Lorenzo Montagner) ha fatto la verifica da una chat dell'app aperta senza
  cartella: un guardiano registrato nelle impostazioni globali del suo Mac e'
  partito, non ha trovato il suo file e ha bloccato il prompt. L'installatore
  non li scrive li'; ce li aveva copiati il suo assistente nella
  "configurazione globale", e ne' la guida ne' il checkup lo vietavano.
- **Guida, passo 4:** nelle user settings va solo `autoMemoryDirectory`, mai
  `hooks` con `${CLAUDE_PROJECT_DIR}`.
- **Checkup 5-bis e Ispettore:** nuovo controllo `CLAUDE_USER_HOOKS_IN_HOUSE`,
  BLOCKER, con prova `test_house_hooks_in_user_settings_block`. Chi ha gia' la
  casa lo scopre al prossimo checkup e sposta i guardiani nella cartella.
- **La regola arriva alla persona, non solo all'agente.** Passo 1 ha la
  sezione «Da adesso: apri sempre la tua AI dentro la cartella»; la guida la
  fa dire dall'agente nella conferma finale ed e' il quinto guasto noto. Cosi'
  ogni testo futuro (corso, membership, email) la eredita dal prodotto.
- Registrato come P-056 nel foglio dei problemi.

## 0.7.9 - 19/09/2026

- **Un guardiano che nessuno chiama e' spento.** Nella casa di Sal una email
  gia' lavorata era rimasta in Posta in arrivo: il guardiano sapeva gestirla dal
  17/09, ma il punto in cui viene chiamato nominava ancora solo gli invii nuovi.
  Guardando la stessa famiglia nel prodotto: delle otto regole che scattano da
  sole, lato Codex ne partivano due. Sei guardiani - dati verificati, doppioni,
  email operativa, memoria, note fra assistenti, note in arrivo - erano
  installati in ogni casa e non li chiamava nessuno, mentre l'elenco prometteva
  che valessero per tutti e due gli assistenti.
- **Ora la prova guarda la chiamata, non solo il programma.**
  `test_guardiani_dichiarati.py` verifica che ogni guardiano dell'elenco sia
  richiamato nelle impostazioni di Claude Code **e** di Codex: la prova di prima
  controllava che il guardiano esistesse, ed era verde mentre l'errore passava.
- **`GUARDIANI.md` dice la regola a chi legge:** installarlo non basta, va
  richiamato in tutte e due le case, e se gli si insegna un caso nuovo si
  guarda anche il punto che lo chiama.

## 0.7.8 - 18/09/2026

- **Niente da lanciare a mano.** Regola di Sal, vista nella casa di una cliente:
  «il cliente non deve sognarsi di spingere qualcosa». Ogni capacita' installata
  ha la sua ricorrenza; il proprietario riceve il risultato.
- **Il Manutentore accorpa, non segnala.** Quando la mappa madre o quella di un
  reparto arriva al tetto, la stringe lui: unisce le ripetizioni, porta il
  dettaglio nel file del reparto, conserva obblighi ed eccezioni parola per
  parola e scrive nel resoconto quanto era grande prima e dopo. Al proprietario
  resta una sola domanda, sul contenuto che non esiste da nessun'altra parte.
  Prima diceva «va accorpata, non la posso tagliare io» e si fermava li'.
- **Chi apre una routine la chiude.** Un'attivita' nata per un giro solo, gia'
  eseguita, viene spenta e tolta: dall'Ispettore che l'ha creata e comunque dal
  Manutentore al giro dopo. Caso vero: due voci morte rimaste per giorni nella
  lista di una cliente, che sembravano lavori attivi.
- **Nuovo `templates/COSA_E_ACCESO.md`.** Una pagina sola, in parole del
  proprietario: cosa fa, quando parte, dove scrive, come si spegne. La tiene
  aggiornata il Manutentore; una capacita' installata e non elencata e' un
  difetto. Il dettaglio dei guardiani resta in `GUARDIANI.md`, senza due elenchi.
- **Il ponte fra chi ripara e chi controlla.** Idea di Sal, 18/09/2026: la
  manutenzione lavora ogni mattina, il controllo della casa passa il lunedi' e
  dice se quel lavoro regge. Ora scrivono nella stessa tabella `Lavori aperti`
  con quattro stati soli: `DA VERIFICARE` (riparato, non ancora ricontrollato),
  `CHIUSO` (il controllo ha riaperto la prova), `BOCCIATO` (col motivo, e la
  mattina dopo la manutenzione riparte da li'), `AL PROPRIETARIO` (bocciato due
  volte: l'unica cosa che arriva alla persona). Nessuno si scrive `CHIUSO` da
  solo e una riga senza prova non si chiude.
- **Comanda il controllo, esegue la manutenzione.** Sal, stesso giorno: chi vede
  tutta la casa deve anche dire cosa togliere e cosa sistemare. Il lunedi' il
  controllo lascia al massimo tre righe `DA FARE`; la mattina dopo la
  manutenzione le esegue prima delle proprie, e se una richiede un gesto fuori
  dal suo mandato la lascia scrivendo perche'. Chi ha eseguito non giudica il
  proprio lavoro: e' la risposta a «chi controlla il manutentore».
- **La tabella resta corta:** le righe chiuse spariscono dopo sette giorni e nel
  registro resta il numero, non la riga. Una riga ferma da quattordici giorni
  sale al proprietario da sola.
- **La mappa della casa dice chi ci lavora.** Prima non nominava nessuno dei
  manuali: l'assistente poteva vivere nella casa senza aprirli mai. Ora la mappa
  porta al Manutentore, all'Ispettore, a come e' messa in piedi la casa e a cosa
  e' acceso. I due documenti nuovi entrano nel contratto di installazione, nei
  due guardiani e nell'armadio comune: prima erano scritti e nessuno li
  installava.
- **La mappa e' rientrata sotto il tetto** senza perdere una parola: paragrafi
  riavvolti, 18 righe libere. Era a un soffio dal limite, come nella casa della
  cliente da cui e' partita questa giornata.
- **Il foglio dei passaggi.** Idea di Sal: «un foglio dove mettiamo tutti i
  passaggi che facciamo, cosi' l'Ispettore puo' verificare». Nuovo
  `templates/PASSAGGI.md`: ogni cosa fatta sulla casa — da noi in call, dal
  proprietario o da un agente — lascia una riga con quando, chi, cosa e **come si
  controlla**. Chi l'ha fatta non la verifica: l'Ispettore riapre il controllo e
  scrive `SI` o `NO`; un `NO` diventa un ordine nei lavori aperti. Una riga senza
  «come si controlla» si boccia a scatola chiusa: il passaggio non era finito.
- Prova nuova `tests/test_capacita_automatiche.py` sui tre comportamenti, sul
  ponte e sulla mappa che nomina i manuali (560 prove verdi).

## 0.7.7 - 17/09/2026

- **I guardiani si presentano.** Nuovo `templates/GUARDIANI.md`, installato in
  ogni casa come `ecosistema/GUARDIANI.md` e obbligatorio nel contratto: una
  riga per guardiano - cosa impedisce, quando scatta - piu' come si installa e
  come si prova dopo l'installazione. Prima i dieci programmi arrivavano muti:
  nessuno sapeva quali regole facessero rispettare.
- **Vale anche per chi non esegue programmi.** L'elenco dice esplicitamente che
  per gli assistenti senza ganci (ChatGPT sul web e simili) quelle righe sono la
  regola da rispettere leggendo. Fino a ieri il prodotto proteggeva soltanto
  Claude Code e Codex.
- `templates/GUARDIANO_STANZE.sh` ammette il nuovo file nell'armadio comune:
  senza questa riga il guardiano bocciava il file appena installato (trovato
  provando l'installazione, non a tavolino).
- Prova nuova `tests/test_guardiani_dichiarati.py`: un guardiano senza riga e
  una riga senza guardiano fanno diventare rossa la suite. 549 prove verdi.

## 0.7.6 - 17/09/2026

- Tolta una duplicazione reale in `templates/AGENTS.md` (P-041): le due regole
  di chiusura ("chi apre chiude", "email lavorata = archiviata") ripetevano
  parola per parola cio' che sta gia' in `templates/PROCESSI.md`, sezione
  Chiusura ambiente. Ora e' un rimando di una riga. Margine sotto il tetto di
  350 righe: da 8 a 15 righe.
- Non toccato il blocco piu' grande, `## Missioni da LeaderAI`: e' doppione
  voluto di `templates/PROCESSI.md` per un motivo preciso
  (`tests/test_mission_loop_guidance.py`,
  `test_client_template_contains_closed_mission_loop`) — la mappa del
  cliente deve restare autosufficiente anche se `ecosistema/PROCESSI.md` non
  viene aperto. Restringere il tetto resta una decisione di Sal, non tecnica.
- 468 prove verdi.

## 0.7.5 - 17/09/2026

- **Ingresso proporzionato alla richiesta.** La mappa della casa ordinava di
  leggere a ogni avvio mappa, memoria e **tutta** la chat degli assistenti:
  anche per «qual e' la mia partita IVA?». Ora una domanda puntuale su un dato
  gia' mappato apre soltanto la fonte che possiede quel dato; stato, note
  recenti della chat e mappa della stanza si aprono per lavoro operativo,
  modifica o coordinamento; una fonte gia' letta e non cambiata non si rilegge.
- Il checkup verifica la regola sulle case gia' installate e la aggiunge dal
  modello corrente se manca; la voce della chat non chiede piu' di leggere
  tutto il log a ogni sessione.
- Nessun guardiano nuovo: sono cambiate le istruzioni. Prova
  `tests/test_ingresso_proporzionato.py`, sei casi, compreso il controllo che
  la regola resti generica (nessun percorso della casa di Sal nel prodotto).
- Motivo: Sal, 17/09/2026, miglioramento gia' provato nella sua casa.

## 0.7.4 - 17/09/2026

Quattro difetti trovati dall'assistente dello Studio Legale Mencarini mentre
installava e censiva davvero (rapporto del 16/09/2026). Il prodotto ordinava
cose che poi bloccava.

- La guida non manda piu' le regole del proprietario in `ecosistema/`, dove
  l'Ispettore ammette soltanto i sette registri comuni e le avrebbe bocciate:
  `REGOLE.md` nasce nella cartella madre, accanto ad `AGENTS.md` (P-035).
- Il censimento dei processi e l'adozione osservata non promettono piu' un
  programma che il cliente non riceve: dalla 0.7.1 il pacchetto e' solo
  documentale, quindi la politica scritta nel contratto **e'** la regola e si
  applica leggendola. `census_rule.py` e `adoption_rule.py` restano dichiarati
  come attuazione di riferimento LeaderAI (P-036).
- I tratti sensibili del censimento si tarano sul mestiere del proprietario:
  chi lavora in uno studio legale dichiara «legale», «avvocat» e «tribunale»
  prima di leggere e quelle parole smettono di marcare zona sensibile dentro il
  perimetro gia' approvato. Prima marcavano l'intero studio e il censimento non
  partiva. Vale per ogni mestiere che coincide con un tratto: sanitario,
  paghe e contributi, consulenza alla persona. Gli altri tratti restano e le
  esclusioni assolute (segreti, credenziali, IBAN, documenti di identita')
  vincono sempre (P-037).
- Il guardiano delle note e il modello che fa rispettare parlano la stessa
  lingua: titolo `## data`, le tre parti `Di cosa si parla:`, `Cosa cambia:` e
  `Cosa serve:`, via `Base Git` che la 0.7.0 aveva gia' tolto. Prima il modello
  insegnava una forma che il guardiano non riconosceva e ogni modifica alla
  chat veniva bloccata. Provandoli insieme e' emerso un quinto difetto: il
  guardiano apriva il registro alla prima parola `## Log`, che compare gia'
  nelle regole in testa al file (P-038).

Quattro prove nuove, una per difetto, tutte rosse sul caso vero prima della
correzione: `test_ecosystem_registry_guidance.py`,
`test_census_rule_availability.py`, `test_census_trade_terms.py`,
`test_guardiano_note_calco.py`. 462 prove verdi.

## 0.7.3 - 16/09/2026

- La guida apre con il controllo che fa l'assistente da solo: cerca `VERSION` e
  i documenti del contratto e decide se installare o aggiornare. Il proprietario
  non deve sapere ne' dire in che stato e' la sua casa.
- Nell'aggiornamento resta una sola scelta umana, la cartella delle copie di
  sicurezza.
- Motivo: Sal, 16/09/2026, «non deve essere il cliente a capire se ha
  l'ecosistema».

## 0.7.2 - 16/09/2026

- La guida cliente contiene il ramo per chi ha gia' la casa: cosa cambia, gli
  otto passaggi dell'aggiornamento, la cartella `4 Gestione dell'ecosistema` come
  fonte e la verifica finale. Prima viveva soltanto nelle email scritte a mano.
- Motivo: Sal, 16/09/2026, «mettiamolo nelle istruzioni, cosi' se non ce lo
  ricordiamo e' scritto».

## 0.7.1 - 16/09/2026

- Il pacchetto pubblico del Passo 1 diventa solo documentale: nove file
  Markdown, `VERSION` e un contratto JSON senza effetti esterni.
- Rimossi dal primo ingresso script, hook, skill, impostazioni globali e
  attivita' programmate. Le capacita' di controllo restano al Passo 4 e
  richiedono una scelta separata.
- Nuova guida cliente breve e verificabile: decompressione, apertura della
  cartella, personalizzazione dei soli segnaposto e controllo finale.
- Motivo: il classificatore di sicurezza di Claude riconosceva correttamente
  il vecchio pacchetto come modifica persistente del comportamento dell'agente
  e bloccava l'installazione con `Instruction Poisoning`.

## 0.7.0 - 16/09/2026

- La casa del cliente non e' piu' un registro git: niente `git init`, commit,
  `.gitignore`, GitHub o barra «Conferma modifiche». Il backup e' la copia di
  sicurezza datata (`templates/BACKUP_CASA.py` -> `.agent/hooks/backup_casa.py`):
  la routine delle 07:45 fa ogni giorno una copia zip nella cartella scelta dal
  proprietario (Domanda 2), tiene le ultime sette e lascia fuori `.secrets/`,
  file che sembrano segreti e gli archivi dichiarati `ARCHIVIO PROTETTO`.
- L'Ispettore blocca una casa con `.git` (`GIT_REPOSITORY_PRESENT`: prima la
  copia, poi un solo gesto del proprietario per rimuoverla), segnala la cartella
  delle copie non scelta come nota (`BACKUP_NOT_CONFIGURED`) e una copia piu'
  vecchia di 48 ore come attenzione (`BACKUP_STALE`). Le note non abbassano il
  verdetto.
- Gli archivi protetti sono protetti dalla dichiarazione nella mappa: fuori
  dalla copia e dalle misure. Le credenziali fuori `.secrets/` restano
  segnalate per percorso. Le tracce di adozione non includono piu' la storia
  git. I ganci Codex partono dalla cartella della sessione (`$PWD`).
- Tolto il gancio `salvataggio_automatico.py` della 0.6.31: senza registro git
  non serve.
- Motivo: Sal, in call con una cliente, «git dalla casa va tolto». Il programma
  Git resta necessario solo su Windows come terminale (Git Bash) dei controlli.

## 0.6.31 - 16/09/2026

- Nuovo gancio di fine turno `salvataggio_automatico.py` (Claude Code e
  Codex, Mac e Windows): se la casa ha modifiche non salvate le mette nel
  registro git locale con data e ora, lasciando fuori segreti e impostazioni
  locali. Non blocca mai la chiusura.
- Motivo: a una cliente l'app mostrava a ogni turno la barra «Conferma
  modifiche» e le chiedeva di cliccare. Il proprietario non deve mai salvare a
  mano: la casa lo fa da sola.

## 0.6.30 - 16/09/2026

- La routine giornaliera `manutenzione-ecosistema` nasce con la cartella madre
  come cartella di lavoro; il checkup lo verifica e ripara la definizione.
- Motivo: sul Mac di una cliente la routine era stata creata senza cartella di
  lavoro, partiva dalla cartella predefinita (iCloud) e il controllo FUORI DAL
  CERVELLO la fermava a ogni giro. Il suo assistente si e' fermato e ha chiesto
  alla proprietaria di impostare la cartella a mano.
- I due ganci sulla chat degli agenti (`CHAT_AGGIORNAMENTI.sh` e
  `GUARDIANO_NOTE_AGENTI.py`) cercavano `docs/AGENT_CHAT.md`, mentre il
  contratto installa `AGENT_CHAT.md` nella radice: non scattavano mai. Ora
  leggono il file nella radice. Segnalato dall'assistente della stessa cliente.

## 0.6.29 - 15/09/2026

- La guida si apre dichiarando la propria provenienza: chi l'ha scritta, cosa
  contiene `Cervello.zip` (testo e Markdown, niente codice eseguibile), cosa
  scrive l'agente e cosa fa l'automazione delle 07:45. L'ispezione del
  pacchetto e' il percorso previsto, non un'alternativa al procedere.
- Motivo: l'assistente di un partecipante alla Challenge si e' fermato prima
  di installare, chiedendo al proprietario chi gli avesse mandato il link e se
  poteva fidarsi. Le informazioni c'erano gia', ma 200 righe piu' in basso.

## 0.6.28 - 14/09/2026

- Aperta la cartella `Prodotti/Skill` nel catalogo: una cartella per skill,
  pronta da copiare in `.claude/skills/` o `.agents/skills/` della casa.
  Sorgente nella copia di lavoro: `Skill/`, inclusa nella release.
- Prima skill: `mente-da-principiante` (esperto con mente da principiante,
  Jeff Bezos): prima la competenza sul campo, poi lo sguardo nuovo; una
  costruzione si promuove solo con prova del risultato, di non regressione e
  del percorso reale. Versione autonoma, senza rimandi alla casa LeaderAI.
- `00 Inizia qui` e `Prodotti/Leggimi.md` dicono dove stanno le skill e come
  si installano.

## 0.6.27 - 13/09/2026

- Il percorso ha un solo significato ovunque: cinque passi, con
  `5 Collaudo e consegna` come chiusura; i prodotti opzionali stanno nella
  cartella separata `Prodotti` e si aggiungono soltanto dopo la consegna.
- La guida del Cervello chiama `Operazioni` i propri passaggi interni, cosi'
  non crea una seconda numerazione di fasi dentro il Passo 1.
- Il Passo 1 mantiene un solo foglio da eseguire: anche la preparazione per chi
  usa ancora l'AI nel browser vive nella guida. Il pacchetto tecnico
  `Cervello.zip` sostituisce l'apertura manuale dei singoli modelli.
- Allineati Manifest, Checkup, mappa installata e Censitore ai nomi visibili
  sul Drive.
- Rimossa anche la vecchia tassonomia interna `Fase 1 / Fase 2` dalle fonti
  correnti: Cervello ed Ecosistema operativo restano componenti, non una
  seconda sequenza di fasi.

## 0.6.26 - 13/09/2026

- Il Passo 1 espone un solo documento operativo:
  `01 - Cervello - installazione e aggiornamento.md`, aggiornato in luogo a
  ogni release e con versione corrente visibile nel testo.
- `EMAIL_CONSEGNA.md` resta il modello breve per il primo invio: controlli del
  mittente e un solo collegamento alla procedura; nessuna missione operativa
  duplicata nel corpo dell'email.
- Ritirata la scheda generata `01 - Cervello.md`, che ripeteva il nome del
  passo senza aggiungere istruzioni.

## 0.6.25 - 13/09/2026

- Mandato comune per tutti i ruoli: l'incarico include intervento, verifica e
  ripresa; niente secondo consenso per il lavoro gia' autorizzato. Al titolare
  restano decisioni fuori mandato, accessi e gesti umani reali.
- Il Manutentore riprende gli incarichi senza esecutore e riconcilia anche la
  memoria sotto soglia. Assegnato non significa eseguito; un revisore dichiarato
  indisponibile richiede riscontro, non un'ipotesi.
- Il gate di rilascio prova anche la ripresa nativa con titolare assente,
  verifica distinta, conservazione degli originali e vera eccezione economica.
  Configurazione del timer e funzionamento sulla macchina cliente restano
  prove separate. Nessuna nuova routine, stanza o gerarchia di agenti.

## 0.6.24 - 12/09/2026

- Il Manutentore riconcilia istruzioni, memoria e stato anche sotto soglia:
  aggiorna e accorpa nella fonte esistente, conservando obblighi e prove.
- Tolto il divieto generale di riscrivere contenuti; dubbi, eliminazione di
  file e azioni esterne mantengono i loro limiti. Nessun nuovo guardiano o timer.
- Stato corrente distinto dai cicli conclusi; verifica del prima/dopo e del
  secondo giro senza duplicati nello standard unico del reparto.
- La prova di manutenzione respinge anche la falsa riduzione ottenuta
  spostando i duplicati in un nuovo archivio; conserva testo, data e occorrenze.

## 0.6.23 - 12/09/2026

- Ogni reparto nasce con responsabile, inneschi e controlli di manutenzione,
  fonte degli esiti e prova del primo passaggio tra reparti. Le sottocartelle
  ereditano, senza moltiplicare agenti o routine.
- Guardiano e Ispettore condividono la verifica del profilo e del gancio
  presente/collegato. Il Manutentore rilegge le mappe correnti, controlla
  contenuti e infrastruttura; l'Ispettore rilegge prove e processi.
- Collaudo di espansione nativa con incasso simulato, sottocartella ereditata
  e difetti intenzionali nei MD e nella configurazione del gancio.

## 0.6.22 - 12/09/2026

- Nasce `Ispettore del Bando`, prodotto-agente installabile per Claude: legge
  fonti ufficiali e fascicolo locale, completa il lavoro reversibile e usa i
  soli verdetti `PRONTO`, `BLOCCATO` e `IN ATTESA`.
- Il verificatore legge ogni riga dell'indice spese, controlla unicita,
  percorsi, impronte, date, importi e totali; una quadratura dichiarata o una
  prova modificata non apre firma o invio.
- Firma CAdES, pagamento e invio sono sequenziali: dopo la firma servono file
  `.p7m`, firmatario e ricevuta di validazione provati; `PRESENTATA` richiede
  ricevuta o protocollo finale integro.
- Il caso Villa ha guidato il perimetro, ma il pacchetto non contiene dati o
  documenti del cliente. Sessantasette prove automatiche e collaudo indipendente
  sotto pressione coprono i confini principali, compresi i tentativi di
  restringere cartelle o tipi di file dell'inventario, nascondere file dietro
  collegamenti simbolici, usare lo stesso contenuto come fattura e pagamento,
  firmare il file sbagliato, perdere la continuita con l'originale, usare date
  fittizie o future, invertire l'ordine temporale, mostrare un pagamento senza
  avviso completo o con importi non monetari, riusare file firmati, avvisi,
  riepiloghi o ricevute tra i sette ruoli critici, collegare il protocollo a
  una pratica diversa, usare fonti datate nel futuro o saltare il pagamento
  prima dell'invio.

## 0.6.21 - 09/09/2026

- La formula visibile `C'E' UN PROBLEMA CHE BLOCCA` richiede ora quattro prove
  insieme: funzione essenziale, guasto riprodotto nell'uso reale, tentativi di
  riparazione esauriti e nessuna alternativa praticabile. Il solo nome di una
  funzione non puo' piu' produrre l'allarme grave.
- Testo business dentro un'app funzionante e file di accesso locali mai entrati
  nella storia Git restano elementi da valutare e collaudare, non blocchi. Una
  credenziale presente o passata da Git resta invece un blocco di sicurezza.
- Origine: rilettura del checkup Vedere Meglio del 09/09/2026. Le 26 voci sui
  testi delle app, i due file Google gia' esclusi da Git e gli otto documenti
  lunghi non dimostravano alcuna funzione ferma.

## 0.6.20 - 09/09/2026

- Separato lo stato visibile alla persona dal verdetto tecnico di conformita':
  il riepilogo ora usa `TUTTO FUNZIONA`, `FUNZIONA, CON ALCUNE COSE DA
  VALUTARE` oppure nomina la sola funzione realmente bloccata e provata.
- `NON PASSA` resta disponibile come codice tecnico interno per gate, log ed
  exit status, ma non compare piu' come giudizio nelle chat, nelle email o nel
  riepilogo dell'Ispettore.
- Aggiornati `CHECKUP.md`, il modello email, le istruzioni installate e la skill
  dell'Ispettore; aggiunte prove automatiche sulla traduzione e sul testo
  distribuito ai clienti.
- Origine: risposta del checkup cliente del 09/09/2026, in cui un rilievo di
  conformita' e' stato comunicato come se l'intero lavoro non funzionasse.

## 0.6.19 - 08/09/2026

- Python 3 (dal 3.8) dichiarato requisito del guardiano di chiusura e
  dell'Ispettore in `01 - Cervello - installazione e aggiornamento.md` (Fase 2 e verifica finale), in
  `MANIFEST.md` e in `CHECKUP.md`: la 0.6.18 lo richiedeva senza dirlo.
- Guardiano: Python provato davvero prima dell'uso (`python3`, `python`, `py`),
  cosi' un alias Windows che non risponde non passa per motore presente;
  due rilievi distinti e leggibili per motore assente e Python mancante.
- Collaudo comportamentale: il controllo «doppione storico non usato» ignora
  le sole frasi che citano l'archivio; una sessione che spiega di non aver
  usato la bozza non viene piu' bocciata (falso positivo del rilascio 0.6.19).
- Origine: revisione critica del 08/09 sulla 0.6.18, registrata in LeaderAI
  (`docs/ecosistema_cantiere.md`). Nessuna modifica alle esenzioni degli
  archivi, alle firme, alle fonti Word o ai file di radice.

## 0.6.18 - 08/09/2026

- Corretto il controllo degli archivi di fascicoli: dichiarazione esplicita,
  percorsi locali e protezione Git verificata prima dell'esclusione dalle
  sole misure strutturali. Credenziali e asset riutilizzabili restano controllati.
- Firme dei sottoscrittori riconoscibili nei fascicoli con PDF locale, ruolo
  dichiarato e archivio protetto; timbri e firme dell'organizzazione restano separati.
- Fonti Word .docx ammesse nella stessa casa, anche dalla cartella madre con
  prefisso @/. Restano i controlli di esistenza, contenuto e collegamenti.
- File di radice con punto iniziale registrabili; docstring Python escluse
  dall'allarme sui testi business, clausole nel programma ancora rilevate.
- Guardiano: una camminata strutturale in Python al posto delle sei ricerche
  shell e dei processi per singolo file. Nuovo componente canonico
  `.agent/hooks/archive_policy.py`, incluso nel contratto e nelle prove di integrita'.
- Origine: rapporto cliente dell'08/09 e verifica indipendente registrata in
  LeaderAI. Nessun dato cliente incluso nei test. Tempo Windows e collaudo
  della casa originaria restano da misurare, distinti dal collaudo del prodotto.
- Specifiche degli ingressi rilette l'08/09: [Claude Code](https://code.claude.com/docs/en/hooks)
  e [Codex](https://learn.chatgpt.com/docs/hooks); soglie timeout preservate.

## 0.6.17 - 07/09/2026

- Nasce `Percorso Ecosistema/`, vista leggibile in cinque file generata dalla
  definizione unica: i primi quattro passi chiudono la consegna iniziale; il
  quinto, `Evoluzione quando serve`, si apre soltanto davanti a un nuovo
  processo reale.
- Il Passo 1 dichiara la stessa infrastruttura funzionale per la casa di Sal e
  per le case cliente: stessi compiti, controlli e prova finale, con contenuti,
  reparti e dati sempre su misura.
- App, skill e prodotti-agente restano opzionali: si installa soltanto la
  capacita' richiesta dal lavoro. La radice Drive resta invariata e il catalogo
  `LeaderAI Ecosystem/Agenti` continua a vivere separato dal prodotto.
- Collaudo completo: 403 test e 506 sottoprove verdi; copia Drive riletta con
  135 elementi attesi, 139 presenti e zero differenze o extra non consentiti.
- Correzione anti-doppione: `Percorso Ecosistema` esiste nella copia pubblicata
  su Drive e viene generato durante il caricamento; il checkout tecnico non ne
  conserva una seconda copia persistente.

## 0.6.16 - 07/09/2026

- I prodotti-agente escono dalla release dell'Ecosistema: la casa corrente e'
  il catalogo separato `LeaderAI Ecosystem/Agenti`, collegato dalla lezione `Agenti` del
  corso senza duplicare i pacchetti.
- `Agente Commercialista` resta installabile nella stanza amministrativa, ma
  si consegna dalla propria cartella nel catalogo; la directory tecnica locale
  e' esclusa meccanicamente dal caricamento di `Ecosistema per i clienti`.
- Una skill semplice resta una capacita' interna e non diventa da sola un
  prodotto-agente.

## 0.6.15 - 04/09/2026

- Il catalogo `Agenti` contiene ora **Agente Commercialista**, pacchetto
  opzionale installabile nella stanza amministrativa gia' esistente. Include
  fonte unica, procedura e adattatori sottili per Claude Code e Codex, senza
  dati fiscali personali o norme hardcoded.
- Il ruolo parte con `Lancia l'Agente Commercialista`, cerca i documenti prima
  di chiederli, distingue regole generali e posizione provata, arriva
  all'ultimo clic e si ferma per accesso, firma, pagamento, invio o giudizio
  professionale. La routine fiscale riusa il Manutentore della casa.
- Tre prove del pacchetto e gate completo: 401 test verdi.

### Agente Censitore - fase 2

- Nasce `census_collector.py`: raccolta metadati deterministica in sola lettura
  del perimetro autorizzato. Non apre contenuti, non segue collegamenti
  simbolici, salta ambienti tecnici e rumore di sistema, e sopra la soglia del
  contratto consegna al modello soltanto aggregati per cartella, tipo, periodo,
  gruppi di nomi e radici di lavoro, con campioni mirati.
- La **radice del lavoro** affianca il gruppo di nomi: `Fattura 12 Rossi`,
  `fattura-13-bianchi` e `Fattura 14 Verdi` sono tre episodi di un processo, non
  tre lavori. Senza questo la ripetizione si spezzava per cliente e i processi
  ricorrenti restavano invisibili.
- Skill gemella `censitore-processi` (`templates/CENSITORE_PROCESSI_SKILL.md`)
  installata per Claude e Codex dal contratto; `templates/PROCESSI.md` porta la
  panoramica del censimento, le schede dei candidati e cio' che non e' stato
  guardato.
- Collaudi 1-6 del piano verdi su una casa finta volutamente disordinata
  (Desktop e Download mescolati, omonimi, versioni, episodio duplicato,
  cartella segreta, cartella personale): 40 test nuovi, gate 398 verdi.
- Correzioni trovate dal collaudo: la zona sensibile di una cartella e' la
  cartella stessa, e i marcatori di versione dopo underscore (`_v2`) ora si
  vedono.

### Agente Censitore - fase 1

- Nasce il contratto testabile dell'**Agente Censitore dei processi** (Passo 2):
  policy `process_census` in `install_contract.json`, accessor validante in
  `install_contract.py`, regola deterministica `census_rule.py` e test con
  fixture (casa disordinata, tracce insufficienti, perimetro con esclusioni).
- Certezza calcolata e mai ambigua: `OSSERVATO`, `DEDUCIBILE`, `DA CONFERMARE`;
  esclusioni che vincono anche dentro il perimetro; zona sensibile segnalata
  senza aprire il file; deduplica per episodio; aggregati oltre soglia con
  durata massima dichiarata; rapporto controllato contro segreti.
- Nessuna skill, raccolta metadati o calco registri: sono la fase 2 del piano
  in `docs/ecosistema_cantiere.md` della casa LeaderAI.

## 0.6.14 - 04/09/2026

- Il nome visibile `Ecosistema Base` diventa **Ecosistema per i clienti**: dice
  subito che contiene il prodotto pulito, distinto dal lavoro privato di Sal.
- La cartella madre Drive ora contiene anche `Ecosistema di Sal`, con tutte le
  aree operative, App e Agenti, e `Backup automatico`. Il corso continua a
  collegare gli stessi file del prodotto e resta inattivo fino alla fine della
  Challenge.

## 0.6.13 - 04/09/2026

- Chiarito l'ordine di autorita': Systeme.io e' ingresso e programma,
  l'Ecosistema per i clienti su Google Drive contiene la versione corrente, la cartella
  locale serve per modifiche e test, GitHub conserva soltanto il backup.
- Installazione e checkup non leggono piu' GitHub e non creano cloni tecnici:
  aprono i file correnti dal prodotto. Un rilascio aggiorna e rilegge Drive prima
  del commit e del push di sicurezza.

## 0.6.12 - 04/09/2026

- L'email di consegna non manda piu' il cliente su GitHub: i fogli dello
  standard si aprono dall'**Ecosistema per i clienti su Google Drive** (cartella
  leggibile con il solo link: VERSION, MANIFEST, INSTALLA_CON_AI, CHECKUP e i
  calchi) e il proprietario segue lo stesso passo nel corso privato **LeaderAI
  Ecosystem** su Systeme.io. Questa formulazione e' stata superata dalla 0.6.13:
  GitHub conserva soltanto il backup successivo alla prova Drive.
- Controllo prima dell'invio: si verifica dal livello di accesso del
  destinatario, senza login Google, che cartella e fogli si aprano dai link.
- Decisione di Sal del 04/09/2026: "spostiamo tutto su Google e Systeme.io,
  senza doppie copie".

## 0.6.11 - 03/09/2026

- Nasce il **Manutentore** (`manutentore-ecosistema`, skill installata accanto
  all'Ispettore per Claude e Codex): il manager della manutenzione continua.
  Ogni giorno misura la casa con `guardiano_stanze.sh --misura`, ripara da solo
  solo il meccanico e reversibile (sezioni datate vecchie negli archivi
  `<nome>_archivio_<data>.md`, chat di gruppo oltre 48 ore, percorsi nascosti,
  skill gemelle), rimisura e lascia cinque righe in `ecosystem-check/STATO.md`.
  Mai eliminazioni, mai riscritture, mai invii: cartelle vuote, copie parallele
  e mappe gonfie restano decisioni del proprietario.
- Il guardiano di chiusura ha la modalita' `--misura`: elenca i problemi senza
  bloccare; la variante Windows inoltra gli argomenti.
- Nuovo registro `ecosystem-check/CONTROLLI.md`: una riga per ogni cosa che
  nasce (chi controlla, quando, cosa misura, dove scrive, stato `ATTIVO` o
  `MANCA` con data). Legge di Sal 03/09/2026: niente nasce senza il suo
  controllo, con parametri suoi; il Manutentore ripete i `MANCA` ogni giorno.
- L'installazione crea l'automazione giornaliera `manutenzione-ecosistema`
  (07:45, modello leggero); il checkup verifica skill e automazione.

## 0.6.10 - 03/09/2026

- Il guardiano di chiusura misura anche i documenti vivi: un Markdown oltre 800
  righe o 80 KiB (fuori dalle mappe, gia' limitate a 350) blocca la chiusura e
  chiede di spostare la parte vecchia in `<nome>_archivio_<data>.md` nella
  stessa stanza o di spezzare per responsabilita'. Gli archivi datati e le
  cartelle `_archivio`/`_storico` non si misurano. Soglie da
  `install_contract.json` (`document_review_lines`/`document_review_bytes`),
  finora applicate solo dall'Ispettore a comando.
- La chat di gruppo vive 48 ore anche per il guardiano: le note datate
  (`## gg/mm/aaaa` o `## aaaa-mm-gg`) piu' vecchie di due giorni bloccano la
  chiusura finche' non vengono promosse nel file proprietario o archiviate.
- Caso reale 03/09/2026 nella casa LeaderAI: stato operativo a 1.770 righe e
  chat a 567 senza che nessun controllo automatico se ne accorgesse; regola 10
  dell'Ispettore esisteva ma partiva solo a comando.

## 0.6.9 - 03/09/2026

- Fase del percorso guidato dichiarata nella mappa madre: `- Fase del percorso:
  N (nome)` con 1 Cervello, 2 Censimento, 3 Prima stanza, 4 Ispettore e
  consegna. Il calco nasce a 1; la riga la alza soltanto la missione LeaderAI
  che chiude il passo, di uno alla volta. Il guardiano di chiusura blocca ogni
  stanza di lavoro registrata con fase 1 o 2; l'Ispettore emette
  `ROOM_BEFORE_STEP_3`. Caso reale 03/09/2026: il Claude della cliente ha
  proposto sei stanze il giorno dell'installazione e nessuno, ne' la missione
  ne' il consulente, sapeva a che passo fosse la casa.
- Il modello dell'email di consegna porta la riga `Fase del percorso: N di 4`,
  e nella casa LeaderAI il guardiano email blocca le missioni senza fase o con
  fase piu' avanti di un passo rispetto alla scheda del cliente.
- Definizione dei quattro passi con test di uscita in `FASI.md` della casa
  LeaderAI; il checkup li applica al Passo 1-bis (punto 1-ter).


## 0.6.8 - 03/09/2026

- Ordine dell'aggiornamento nel checkup: prima i file gestiti dallo standard
  (guardiano di chiusura e variante Windows, ruoli di Ecosystem Check, skill
  dell'Ispettore), sostituiti con le copie della release e riprovati; poi i
  registri e i calchi nuovi. Un guardiano della versione precedente non conosce
  i file resi obbligatori dalla versione nuova e li blocca (caso reale
  03/09/2026: anagrafe dei soggetti con il guardiano 0.6.6). Regola in
  `CHECKUP.md` Passo 0 e nella skill dell'Ispettore, con test.


## 0.6.7 - 03/09/2026

- Istruzioni globali dell'agente attivo (caso reale Pastore, 03/09/2026: casa
  installata, ma Claude Code aperto da un'altra cartella non sapeva che la casa
  esistesse). Lo standard ora scrive il blocco marcato `LEADERAI-CASA` nelle
  istruzioni lette in ogni sessione: `~/.claude/CLAUDE.md` per Claude Code
  (calco `templates/CLAUDE_USER.md`), `~/.codex/AGENTS.md` o
  `AGENTS.override.md` per Codex (calco `templates/CODEX_USER_AGENTS.md`).
  Il blocco si aggiunge o si aggiorna senza toccare il resto del file. Nuovi
  effetti esterni `claude_user_instructions` e `codex_user_instructions`, nuovo
  controllo ambiente `user_instructions_gate` (prova da cartella estranea ->
  `FUORI DAL CERVELLO`). `leaderai_setup.py` li applica solo con un percorso
  letto sulla macchina (`--claude-user-instructions`,
  `--codex-user-instructions`); senza, non tocca la home. L'Ispettore emette
  `USER_INSTRUCTIONS_MISSING` e `USER_INSTRUCTIONS_WITHOUT_HOUSE` (bloccanti) e
  `USER_INSTRUCTIONS_WITHOUT_GATE` (attenzione); accetta il percorso della casa
  in forma assoluta, `~/`, `$HOME/` o `%USERPROFILE%\`.
- Fonti ufficiali obbligatorie in ogni checkup: la pagina memory di Claude Code
  (scope dei `CLAUDE.md`) e la pagina `AGENTS.md` di Codex (caricamento
  gerarchico, override, tetto di byte).
- Anagrafe dei soggetti giuridici: nuovo calco `templates/SOGGETTI.md` ->
  `ecosistema/SOGGETTI.md`, obbligatorio nell'armadio comune (contratto,
  guardiano, harness). Regola "piu' soggetti, una casa": stanze per funzione,
  sottocartelle per soggetto solo dove la legge o il lavoro lo impongono,
  stanza per soggetto solo con processi propri. Caso reale: sei enti dichiarati
  dopo una proposta costruita su tre attivita'.
- Percorso guidato LeaderAI: finche' `logs/install-log.md` non registra
  `PERCORSO GUIDATO CHIUSO`, creare, fondere, spostare o eliminare stanze si
  decide nella sessione con il consulente (`DA DECIDERE IN CALL`), anche se il
  proprietario approva a voce. Riga aggiunta in `ecosistema/LIMITI.md`.
- Ispettore come ultimo passo obbligatorio dell'installazione, in una nuova
  sessione nata dalla cartella madre: la sessione che monta la casa non chiude
  l'installazione.
- Criterio della conferma finale reso esplicito ovunque: parte soltanto con
  verdetto `PASSA` pieno; con `PASSA CON ATTENZIONE` resta nella casa e, se
  serve un gesto umano, il solo messaggio ammesso e' `SERVE UN TUO PASSAGGIO`.
  Caso reale: rapporto di nove sezioni partito con collaudo incompleto.
- Lezione candidata promossa: su Windows i comandi di testo POSIX (sed, awk)
  perdono i backslash dei percorsi `%USERPROFILE%\...`; dopo ogni scrittura
  automatica dei registri si verifica con una ricerca e si registra la prova.
- Risolto un avviso di sintassi nell'Ispettore (sequenza di escape in una
  stringa) che sarebbe diventato errore nelle prossime versioni di Python.


## 0.6.6 - 02/09/2026

- Contratto di stanza "consolidato": una casa nata prima dello standard, con
  statuti di reparto propri e provati (caso reale: la casa madre LeaderAI, tre
  prove di instradamento su tre), dichiara `- Contratto di stanza: consolidato`
  nella mappa madre e, sotto, `Chat di gruppo`, `Guardiano di chiusura` e
  `Registro di dettaglio canonico`. Restano obbligatori ponte, mappa leggibile e
  riga completa nella mappa madre; il calco a 14 sezioni, la sezione Dentro, la
  profondita' massima e la fonte business per stanza valgono per il contratto
  completo delle case nuove. Il guardiano di chiusura applica lo stesso
  contratto e accetta i registri canonici.
- Nuovi finding `CONSOLIDATED_CHAT_MISSING`, `CONSOLIDATED_GUARDIAN_MISSING`,
  `CONSOLIDATED_GUARDIAN_NOT_HOOKED`; test dedicati per Ispettore e guardiano.
- Casa del prodotto: Ecosistema per i clienti su Google Drive (cartella madre "LeaderAI
  Ecosystem", accanto a "Ecosistema di Sal"); la repo resta backup tecnico e
  numerazione delle versioni. La release viene ricostruita dal Drive file per
  file (`leaderai-ecosistema/tools/ecosistema_base_drive.py` nella casa LeaderAI).


## 0.6.5 - 02/09/2026

- Precisione dei rilevatori sul banco LeaderAI: immagini, note Markdown,
  documenti e media non sono piu' candidati "configurazione credenziali"
  (una schermata `credential-cards` o una nota sul cambio password non
  contengono segreti). Gli asset di firma, timbro e sigillo sono soltanto le
  immagini o i certificati sorgente: un contratto gia' firmato e' un output, uno
  script o una nota che parlano di firma non sono l'asset.
- Gli asset ad alto rischio possono essere registrati anche nel registro di
  dettaglio canonico dichiarato dalla mappa madre (casa consolidata), non solo
  in `ecosistema/ASSET.md`.


## 0.6.4 - 02/09/2026

- Il guardiano di chiusura (`guardiano_stanze.sh`) ripete a ogni `Stop` il
  controllo dei percorsi invisibili al proprietario (macOS `chflags hidden`,
  Windows attributo Hidden): caso reale LeaderAI 01/09/2026, tre cartelle
  nascoste "per una scena video" e mai fatte ricomparire. L'Ispettore le vedeva
  (0.6.2), il guardiano no. Test dedicato su macOS.
- `ecosistema_inspector.py` esclude dal censimento dei file gli ambienti tecnici
  (`.venv`, `node_modules`, `site-packages`, cache, cartelle con `pyvenv.cfg`,
  `.playwright-cli`): sul banco LeaderAI producevano oltre 1.600 finding di
  business, credenziali, asset e Markdown che non erano contenuto del
  proprietario. Le dotdir di editor e strumenti (`.obsidian`, `.vscode`, ...)
  non richiedono una classe; ogni altra dotdir alla radice resta da classificare.
- Casa consolidata: la mappa madre puo' dichiarare
  `- Registro di dettaglio canonico: \`percorso.md\`` e usare un registro proprio al
  posto di `ecosistema/ASSET.md` e `ecosistema/FONTI.md`, senza creare doppioni.
  Una cartella dal nome generico dichiarata e registrata dalla madre resta una
  segnalazione, non un blocco, e non deve avere la mappa di una stanza.
- `.mcp.json` (configurazione MCP di progetto di Claude Code) e' un file di
  radice ammesso.


## 0.6.3 - 01/09/2026

- L'Ispettore ora protegge le fusioni della memoria: il file consolidato
  dichiara nel frontmatter `replaces:` gli stem superati e il controllo blocca
  ogni wikilink interno ancora rivolto a una di quelle voci. Una memoria fusa
  senza contratto `replaces:` non passa il collaudo.
- Il Passo 2-ter richiede anche la prova diretta degli inneschi ereditati dal
  richiamo attivo della casa: avere un `trigger:` sintatticamente valido non
  dimostra che le parole operative rimangano raggiungibili.

## 0.6.2 - 01/09/2026

- Nuovo controllo del censimento: nessun percorso della casa, dotfile esclusi,
  puo' portare un flag di invisibilita' (macOS `chflags hidden`, Windows
  attributo `Hidden`). Il caso reale sul banco LeaderAI: `memory/`, `docs/` e
  `console/` invisibili nel Finder — per il proprietario "mai esistite" mentre
  l'agente le usava ogni giorno. Il censimento ora confronta cio' che vede
  l'agente con cio' che vede il proprietario; il flag si toglie nello stesso
  turno.
- `ecosistema_inspector.py`: finding bloccante `HIDDEN_FROM_OWNER` con test
  dedicati (flag su cartella di radice; i dotfile restano esclusi).

## 0.6.1 - 29/08/2026

- Corretta una regola tecnica superata sul ramo Claude Code: `autoMemoryDirectory`
  e' letta da ogni scope di settings (user, project, local, policy, `--settings`),
  non solo dalle user settings. Nelle settings di progetto o locali il valore vale
  dopo il trust del workspace. Lo standard LeaderAI resta le user settings, ma ora
  per la ragione giusta: la memoria segue la macchina, non la copia della repo.
- Nuovo controllo C.7 del ramo Claude Code: la chiave di permesso nel posto
  sbagliato. Una chiave inventata o annidata sotto il blocco sbagliato viene
  scartata in silenzio e lascia il proprietario convinto di aver autorizzato
  qualcosa. Il controllo nomina il caso trovato sul banco di collaudo LeaderAI:
  `autoMode` sta al primo livello del file, non dentro `permissions`, e il
  classificatore lo legge solo da `~/.claude/settings.json`, dalle managed
  settings e da `--settings`.
- Aggiunte alle fonti Claude Code del Passo 1 la pagina di riferimento delle
  chiavi settings e quella di configurazione di auto mode.

## 0.6.0 - 28/08/2026

- Nasce `Ecosystem Check`, prima stanza standard installata in ogni casa
  accanto a `ecosistema/`: mappa, stato, standard di reparto, registro dei
  controlli e sei ruoli separati per assegnazione, controllo, intervento e
  verifica finale.
- Il prefabbricato ora distingue la stanza comune di controllo dalle stanze
  business adattive del cliente. Una casa puo' avere zero stanze business, ma
  non resta senza il reparto che verifica struttura, istruzioni e continuita'.
- Il registro conserva un riepilogo per ciclo; il controllo iniziale precede
  l'eventuale attivazione della cadenza settimanale.
- L'Ispettore distingue capacita', autorizzazione e perimetro predefinito:
  un primo tentativo fallito non diventa piu' automaticamente un limite o un
  lavoro manuale scaricato sulla persona.
- Ogni `non posso` deve indicare percorso provato, data e prova osservabile;
  prima l'agente controlla le capacita' vive, diagnostica e riprova. I verdetti
  smentiti da una prova successiva vengono marcati `SUPERATO` e corretti nella
  fonte proprietaria.
- LeaderAI diventa il banco di collaudo reale dell'Ispettore: la fonte resta
  questa repo, i test automatici girano qui e la prova d'uso avviene nella casa
  `/Users/sal/leaderai`; le lezioni tornano nel prodotto prima del rilascio.
- Aggiunto il controllo focalizzato sulle istruzioni: puo' essere usato anche
  in una casa che non adotta il telaio cliente, senza imporre stanze, registri
  o verdetto di conformita' complessivo.

## 0.5.8 - 27/08/2026

- Il contratto delle stanze non dipende piu' soltanto dall'Ispettore avviato a
  richiesta: un project hook `Stop` controlla automaticamente ogni chiusura di
  Codex e Claude Code.
- Il guardiano blocca materiali business dentro `ecosistema/`, elementi
  sciolti senza proprietario, stanze senza mappa o ponte, copie `_v2`/`_finale`,
  cartelle vuote e router oltre 350 righe o 24 KiB. Il secondo passaggio non
  crea un ciclo infinito.
- Una mappa presente soltanto di nome non basta: registri, celle obbligatorie,
  sezioni compilate, fonte operativa, fonte business e sottocartelle dichiarate
  devono coincidere con percorsi reali. Testo di esempio, prefissi simili e
  istruzioni del calco non possono produrre un verde falso.
- Il ramo Codex include anche il comando Windows; Claude usa Git Bash su
  Windows come previsto dalla documentazione ufficiale. Le configurazioni JSON
  vengono unite senza cancellare chiavi o hook del cliente e senza duplicare
  il guardiano.
- Setup, Ispettore e collaudo manuale verificano contenuto degli script, una
  sola registrazione `Stop`, variante Windows e prove reali pulita/bloccante.
  Un JSON cliente non valido viene preservato e produce un blocco esplicito
  prima di qualsiasi altra scrittura; un hook cliente dal nome simile resta
  intatto.
- Le specifiche ufficiali degli hook Codex e Claude Code sono entrate nelle
  fonti vive del contratto. Il template della mappa madre e' stato alleggerito
  da 350 a 325 righe per lasciare spazio al lavoro reale senza superare da solo
  il proprio limite.

## 0.5.7 - 27/08/2026

- `ecosistema/` diventa un armadio comune riservato: contiene soltanto i
  registri e i calchi dichiarati dal contratto. Piani, bozze, asset e cartelle
  operative al suo interno bloccano il collaudo.
- Ogni vera stanza nasce come prefabbricato atomico: mappa `AGENTS.md`, ponte
  `CLAUDE.md`, fonte operativa nominata e compilata, riga nella mappa madre e
  prova. Il nuovo `STANZA_FONTE.md` porta in testa stato, prossimo passo,
  decisioni e scadenze.
- La policy macchina `inspection_policies -> room_lifecycle` governa classi,
  file, sezioni, organigramma e profondita' del controllo. L'Ispettore blocca
  campi incompleti, fonti assenti/vuote/illeggibili, sottocartelle fantasma,
  generiche, vuote, non dichiarate o collegate fuori casa e classi inventate.
- Il metro di controllo non puo' essere indebolito dal contratto: classi,
  registri, calchi, sezioni, termini, profondita' e nomi sono canonici. Anche
  due destinazioni che differiscono soltanto per maiuscole vengono fermate,
  per evitare collisioni silenziose su Windows.
- La riga madre e la mappa locale devono coincidere in tutti i dieci campi;
  una seconda fonte operativa, un elemento madre assente dal registro di
  dettaglio, una frase che nega il ruolo dichiarato o un file portante non
  leggibile producono un blocco esplicito, mai un verde falso o un crash.
- Il caso anonimo di uno studio cliente, con materiale marketing collocato
  dentro `ecosistema/`, e' diventato una regressione deterministica. La stessa
  legge e' scritta in Manifest, installazione, checkup, skill e mappe dei due
  agenti.

## 0.5.6 - 21/08/2026

- Il checkup guadagna il Passo 1-quinquies "Come si lavora davvero qui dentro":
  dalle tracce gia' presenti sulla macchina (registro sessioni, cronologia dei
  file toccati, `logs/`, diario dei file progetto, `AGENT_CHAT.md`, `MEMORY.md`
  e storia Git) l'agente ricostruisce quali strumenti entrano davvero nelle
  giornate di lavoro, con quale frequenza e su quali lavori. La sezione dichiara
  quali tracce ha letto, da quale macchina arrivano e quale periodo coprono.
- L'etichetta e' legata al periodo: uno strumento provato e funzionante che
  resta assente dalle tracce del periodo osservato si riporta come `NON USATO
  NEL PERIODO OSSERVATO`, non come un mancato uso definitivo. Entra nel rapporto
  con la sua prova, vive accanto all'elenco bloccante del gate e lascia il
  verdetto deciso dalle sole condizioni tecniche.
- Un episodio conta uno: le tracce dello stesso episodio (Git, chat, diario)
  vengono deduplicate per identita' di episodio, non per solo testo del gesto.
  Due episodi distinti contano due anche con lo stesso gesto e nello stesso
  giorno; lo stesso gesto ripetuto in giorni diversi conta una volta per giorno.
  Regola deterministica `adoption_rule.py -> classify_adoption`, con verdetti e
  tracce ammesse in `install_contract.json -> inspection_policies ->
  adoption_observation`, fonte macchina obbligatoria: contratto mancante, JSON
  non valido o policy incompleta fanno fallire la regola in modo visibile, senza
  default locali. Le tracce ammesse coprono tutte quelle del Passo 1-quinquies
  (sessioni, cronologia file, `logs/`, diario, chat, `MEMORY.md`, Git) con
  vocabolario canonico nel contratto. La validazione richiede ora l'intero set
  canonico: una policy che dichiara solo una parte delle tracce (es. il solo
  Git) viene fermata con l'elenco delle mancanti, misurando la completezza sul
  glossario del contratto stesso, senza una seconda lista divergente. Fixture di
  prova per: stesso episodio in piu' sorgenti (uno), stesso gesto in due episodi
  distinti (due), stesso gesto in due giorni (due), sorgenti sessioni/log/file
  ammesse, tracce assenti, copertura parziale, contratto
  mancante/malformato/incompleto, sorgenti parziali non canoniche.
- Osservazione parziale: le tracce vivono sulla macchina dell'agente mentre la
  casa puo' stare su Drive/OneDrive condivisa fra piu' PC. Se la casa e'
  condivisa e le tracce arrivano da una sola postazione, l'esito e'
  `OSSERVAZIONE PARZIALE - UNA POSTAZIONE`; `TRACCE ASSENTI` resta al caso in cui
  il registro manchi davvero. Con tracce insufficienti non si giudica l'uso.
- Il gesto manuale chiede una prova esplicita: la sola presenza di un file e' un
  indizio, la prova e' il gesto (messaggio scritto a mano, file creato a mano,
  riga di diario) con data.
- L'Output separa `VERDETTO CONFORMITA'` (com'e' fatta la casa) da `ADOZIONE
  OSSERVATA` (come si lavora davvero): uno non decide l'altro. Il rapporto porta
  le righe `Uso reale quotidiano`, `Non usato nel periodo` e `Lavori ancora a
  mano`, piu' il blocco `COME SI LAVORA QUI DENTRO` con tracce, macchina e
  periodo coperto.
- Confine di prodotto scritto dentro il passo: il checkup dice cosa si usa; la
  misura della spesa e del consumo appartiene al prodotto `Il Consigliere`
  (repo `salChiarenza/il-consigliere`).

## 0.5.5 - 06/08/2026

- Le comunicazioni visibili a Sal e al cliente usano ora un riepilogo in
  parole comuni: `Cosa funziona`, `Cosa completiamo`, `Cosa serve da te` e
  `Quando si chiude`.
- Le classificazioni tecniche restano nelle fonti della casa e non compaiono
  nelle email. Quando serve davvero un gesto umano, il messaggio apre con
  `SERVE UN TUO PASSAGGIO`, indica il solo gesto richiesto e promette la
  ripresa immediata della stessa missione.
- Il contratto di consegna rifiuta email che espongono a Sal o al cliente le
  etichette tecniche `NON PASSA` e `BLOCCO REALE`.

## 0.5.4 - 06/08/2026

- Le missioni cliente continuano nella stessa casa fino a completamento e
  prova di tutti i criteri, compreso il processo reale e la continuita' dopo la
  riapertura.
- Gli stati intermedi restano locali. Quando Sal richiede una conferma finale,
  parte una volta sola, soltanto con esito `PASSA`, e apre con `Perfetto, l'ho
  fatto. Tutto completato e funzionante.`.
- Scritta la legge dell'unico `BLOCCO REALE`: una domanda unica soltanto dopo
  tentativi sicuri falliti; ricevuta la risposta, l'agente riprende la stessa
  missione. Vietati avanzamenti e istruzioni a puntate.
- Rimossi dal contratto operativo i cicli di rapporti intermedi,
  `SAL_VERIFICA`, `CONTINUA` e `CHIUDI`.
- Il setup e il collaudo non creano piu' `REPORT_FINALE.md`: stato e prove
  vengono salvati direttamente nelle fonti proprietarie. L'Ispettore riconosce
  il vecchio file come residuo da migrare e spostare nel Cestino.
- Il ciclo produce zero aggiornamenti intermedi; quando la missione richiede
  una conferma finale, ne parte una sola dopo il collaudo completo.

## Non pubblicato - 05/08/2026

- Il Passo 2-ter guadagna una lettura veloce prima della prova comportamentale:
  sei segnali letti sul file (ordine stretto al posto del criterio, ovvieta',
  procedura lunga dentro il file sempre letto, doppione tra livelli, memoria
  scritta a mano, peso misurato) filtrano i blocchi prima di spendere due
  sessioni ciascuno. La lettura produce segnalazioni; le rimozioni restano
  legate alla prova e all'approvazione del proprietario.
- Il metro ufficiale del Passo 2-ter entra tra le fonti comuni: articolo
  Anthropic "The new rules of context engineering for Claude 5 generation
  models" (24/07/2026) per il ramo Claude Code, pagina `agents-md` di OpenAI
  per il ramo Codex, con il tetto `project_doc_max_bytes` a 32 KiB citato come
  misura.
- Aggiornati i quattro indirizzi della documentazione Codex citati nel
  checkup: `developers.openai.com/codex/...` rimanda oggi a
  `learn.chatgpt.com`. Verificato il 05/08/2026 su tutti e quattro; il
  redirect risponde, quindi il checkup non falliva, e ora i link puntano
  diretti alla casa attuale.

## Non pubblicato - 02/08/2026

- "Chi apre chiude" ed "email lavorata = email archiviata" salgono nelle Regole
  base delle istruzioni installate al cliente: prima vivevano solo nel capitolo
  delle missioni LeaderAI, quindi l'agente del cliente le applicava alle
  missioni e le ignorava nel lavoro quotidiano (caso reale rilevato il
  04/08/2026 sull'installazione di Massimiliano Caporali). La chiusura
  ambiente in `PROCESSI.md` vale ora per ogni lavoro e precisa che si chiude
  solo cio' che ha aperto l'agente.

- Il ciclo ordinario di una missione ora si chiude nella casa del cliente:
  esecuzione, prova, salvataggio nelle fonti proprietarie e chiusura ambiente.
- L'email della missione e' l'unico messaggio: zero report di ritorno;
  decisioni e gesti umani restano come `DA DECIDERE IN CALL`.

- Ogni consegna richiede ora `AI_ACT_CHECK_OK` per il sistema e l'uso concreti:
  ruolo, persone coinvolte, rischio, trasparenza, data, esito e presidio.
- Pratiche vietate, alto rischio e dubbi sostanziali bloccano la consegna; il
  controllo di un sistema non viene riusato automaticamente per un altro.

- L'Ispettore confronta un blocco di istruzioni alla volta tra contesto attuale
  e alleggerito, in due sessioni pulite e su copie temporanee.
- Le prove ricevono soltanto il compito aziendale: nessun indizio su cartella,
  fonte, procedura o risultato atteso puo' mascherare l'effetto del contesto.
- Il rapporto misura esito, fonti, instradamento, completamento, richieste
  umane, tempo, consumo quando disponibile e sicurezza; errori tecnici restano
  `DA COLLAUDARE`.
- Un solo caso non puo' candidare una rimozione. Sicurezza, privacy,
  autorizzazione e integrita' non vengono eliminate automaticamente.
- I casi di prova e i riferimenti storici pubblici sono anonimizzati.

## 0.5.3 - 31/07/2026

- La pagina iniziale della repo espone i riferimenti ufficiali per Claude Code,
  ChatGPT e Codex per il lavoro.
- Le stesse guide entrano in `ecosistema/FONTI.md`, quindi restano disponibili
  anche nella casa installata del cliente.
- `install_contract.json` le rende parte del metro macchina: l'Ispettore deve
  aprirle, confrontare regola e stato reale, riparare e mostrare la prova.
- Il comando `lancia l'Ispettore` avvia il checkup senza una seconda domanda.
- Il Cervello e' ora verificato come organigramma: Boss dell'Ecosistema alla
  radice e un Amministratore di settore per ogni ramo organizzativo, nuovo o
  preesistente. L'Ispettore blocca mappe prive della catena verso il Boss.
- L'Ispettore misura tutti i Markdown: mappe e indici oltre le soglie macchina
  bloccano il verdetto; i documenti estesi vengono controllati per fonti
  duplicate o responsabilita' mescolate e poi alleggeriti senza perdere dati.
- Ogni problema ripetibile porta nel report causa, riparazione, prova e lezione
  candidata, cosi' puo' diventare regola e test dei checkup successivi.
- I test impediscono a una versione futura di consegnare il pacchetto senza i
  collegamenti o senza il contratto di confronto.

## 0.5.2 - 30/07/2026

- Ogni email operativa agente-agente apre con `STATO PER LE PERSONE`: fatto,
  manca, prossimo passo e intervento umano, in parole semplici.
- Il formato vale in entrambe le direzioni: missione LeaderAI al cliente e
  rapporto dell'agente del cliente verso LeaderAI.
- `REPORT_FINALE.md`, modello di consegna, checkup e processi installati portano
  lo stesso riepilogo prima dei dettagli tecnici.

## 0.5.1 - 29/07/2026

- Corretto il gate Windows: i finti agenti Python vengono avviati tramite il
  runtime Python invece di essere trattati come eseguibili Win32.
- I test della memoria Claude ora rispettano la stessa regola del prodotto:
  quando la memoria vive sotto la home, `autoMemoryDirectory` usa la forma
  portabile `~/...` anche su Windows.
- La regressione sul repository Git mancante non tenta piu' di cancellare
  oggetti Git protetti in sola lettura su Windows; sposta la cartella `.git`
  fuori dal target e verifica lo stesso blocco dell'Ispettore.

## 0.5.0 - 29/07/2026

- L'ingresso nel Cervello e' ora un gate: ogni nuova task/sessione nasce dalla
  cartella madre come progetto primario/CWD, dichiara il percorso e mostra tre
  regole lette da `AGENTS.md`. Una task aperta altrove resta
  `FUORI DAL CERVELLO`.
- Aggiunta la prova esatta `Crea la Brand Identity` senza percorsi, file,
  stanze, fonti o output suggeriti. Il gate osserva instradamento autonomo,
  fonte brand reale e output nella responsabilita' proprietaria.
- La chat di gruppo porta ID missione, agente proprietario, base Git, prove e
  prossimo agente; in modalita' `both` il collaudo richiede il passaggio
  Codex -> Claude Code -> Codex su tre sessioni distinte.
- L'email operativa distingue `INSTALLA` e `CONTINUA`, usa link di release
  immutabili e verifica mittente, thread e autorizzazione del proprietario.
- `01 - Cervello - installazione e aggiornamento.md` espone un nucleo deterministico delimitato: il gate
  manuale prova il telaio senza consumare l'intera procedura di
  personalizzazione, che resta nello stesso file ufficiale.
- Aggiunto `install_contract.json`, fonte macchina unica per installazione
  manuale, setup tecnico, Ispettore e collaudo.
- Il setup Claude configura davvero `autoMemoryDirectory` nelle user settings,
  preserva le altre chiavi e blocca una seconda casa gia' configurata invece di
  sovrascriverla.
- Il verdetto del setup deriva dall'Ispettore: versione vecchia, memoria non
  collegata, ramo agente incoerente o baseline Git assente non possono piu'
  produrre `PASSA`.
- I cambi Codex/Claude sono espliciti: `both` mantiene i due rami;
  `--migrate-agent` rimuove soltanto file standard riconosciuti e si ferma
  davanti a contenuti del cliente.
- Aggiunto il gate deterministico `python3 -m tests.gate --quick`: zero test,
  test saltati, errori o fallimenti bloccano il rilascio.
- Aggiunti due harness con prove conservate. Il primo avvia agenti reali su una
  casa anonima e verifica instradamento, fonte corretta, output e isolamento tra
  stanze. Il secondo ripete l'installazione manuale dalla sola procedura, senza
  clone, Python o setup tecnico.
- Il gate completo `python3 -m tests.gate --release --agents codex,claude`
  richiede entrambi gli agenti reali e tratta CLI assente, login mancante,
  timeout o oracolo fallito come blocchi.
- Aggiunta CI deterministica su macOS e Windows con percorsi contenenti spazi,
  accenti e apostrofi; il live resta su runner autenticato dedicato.

## 0.4.5 - 29/07/2026

- **MUST percorsi d'ambiente in forma portabile.** `autoMemoryDirectory` si
  scrive nella forma `~/`, non piu' come percorso assoluto: una sola stringa
  vale su tutte le postazioni del cliente e si risolve sull'utente del computer
  corrente. La 0.4.3 prescriveva il percorso assoluto locale.
- Nuova sezione del Manifest: percorsi, nomi utente, lettere di disco e valori
  d'ambiente destinati a un'altra macchina si scrivono in forma portabile
  oppure si leggono dalla fonte di quella macchina. Vietato riproporre altrove
  un percorso letto su un computer diverso.
- L'Ispettore segnala `CLAUDE_MEMORY_NOT_PORTABLE` quando `autoMemoryDirectory`
  usa un percorso assoluto dentro la home dell'utente corrente. E' un avviso,
  non un blocco: il verdetto diventa `PASSA CON ATTENZIONE`.
- Due regressioni coprono il caso: percorso assoluto sotto la home segnalato,
  forma `~/` pulita.
- Origine anonimizzata: ambiente con due postazioni e nomi utente diversi. Il
  percorso assoluto replicato sul portatile avrebbe rotto la memoria senza
  alcun errore visibile.

## 0.4.4 - 28/07/2026

- L'email operativa dichiara un solo lettore reale. Il modello corrente usa
  `AGENTE_CON_POSTA`: l'agente collegato alla casella del cliente riceve la
  missione direttamente dalla prima riga.
- Il proprietario compare nei soli gesti umani che l'agente gli presenta al
  momento corretto; il report viene mostrato localmente e parte dopo il suo
  comando `manda`.
- Aggiunta una regressione che blocca il passaggio circolare `apri Claude e
  digli di leggere questa email`.

## 0.4.3 - 28/07/2026

- Una casa semplice puo' avere zero stanze: capacita', fonti e output possono
  essere posseduti direttamente dalla cartella madre e registrati nella mappa
  radice, senza creare `AGENTS.md` e `CLAUDE.md` locali inutili.
- Aggiunto il registro degli elementi posseduti dalla madre e il relativo
  controllo deterministico. La regressione prova che `Portafoglio Modello`
  passa come `CAPACITA` della madre senza essere promosso a stanza.
- Corretto lo scope Claude Code: `autoMemoryDirectory` vive nelle user settings
  di ogni computer (`~/.claude/settings.json`), con percorso assoluto locale e
  prova `/memory`; le settings project/local vengono segnalate come invalide.
- La memoria canonica e' dichiarata nella mappa madre. Un ambiente esistente
  puo' conservare il proprio nome e percorso consolidato, anche su OneDrive,
  dopo riconciliazione e prova su tutte le postazioni.

## 0.4.2 - 28/07/2026

- Aggiunto il gate anti-falsa-stanza: una cartella e' `STANZA` solo quando
  possiede una responsabilita' business riconosciuta, mantiene stato e
  decisioni e governa lavoro corrente.
- Script, skill, modelli, fonti e output possono formare una pipeline completa
  senza creare una stanza; in caso ambiguo la classe resta `CAPACITA` o
  `SOSPETTA` e il verdetto e' `NON PASSA`.
- Aggiunta la regressione `Portafoglio Modello`: il nome di un prodotto o di
  una lavorazione non dimostra una funzione aziendale autonoma.
- Il contratto locale e l'Ispettore richiedono ora una sezione esplicita
  `Responsabilita business`; il preflight blocca placeholder e dichiarazioni
  non risolte.
- Gli esempi del modulo Portafogli usano una stanza business neutra e non
  insegnano piu' a trattare `Portafoglio Modello` come stanza.

## 0.4.1 - 28/07/2026

- Il modulo Portafogli include il gate unico `VERIFICA_FINANZIARIA.md`, attivo
  su numeri finanziari, fondi, ETF, titoli, ISIN e richieste sullo stato di uno
  strumento.
- La skill distingue identita' e stato corrente del prodotto dalla sua
  collocabilita' nel catalogo autorizzato.
- Ogni numero materiale porta fonte, data/ora, valuta, periodo, formula e
  ricalcolo; ogni strumento porta identificativo, classe, valuta e stato tra
  attivo, chiuso, sospeso, incorporato, rinominato, liquidato o non verificato.
- Il secondo controllo cerca anche evidenze contrarie alla prima risposta; il
  consenso tra modelli resta una revisione aggiuntiva e non sostituisce la
  fonte primaria.
- Un elemento critico privo di prova produce `ESITO SOSPESO`; il report cliente
  nasce soltanto dal gate `PASSA` validato dal banker.

## 0.4.0 - 28/07/2026

- Il gate legge obbligatoriamente il `VERSION` vivo e lo confronta con la
  versione installata registrata in `AGENTS.md`: assenza o differenza =
  `NON PASSA`.
- Il `CHECKUP.md` e' ora l'Ispettore Ecosistema richiamabile con frasi naturali
  come `lancia l'Ispettore`, senza creare una seconda procedura concorrente.
- Ogni nuova cartella passa un ciclo obbligatorio: classificazione, stanza
  proprietaria, eventuale mappa locale, collegamento alla radice e prova.
- Aggiunto `templates/STANZA_AGENTS.md`, installato anche come calco locale
  `ecosistema/STANZA_AGENTS.md`: ogni vera stanza dichiara scopo, contenuto,
  fonti, output, capacita', monte, valle e dove scrivere; il ponte locale resta
  `CLAUDE.md` con il solo `@AGENTS.md`.
- L'installazione monta la skill `ispettore-ecosistema` nel percorso
  dell'agente attivo: `.claude/skills/` per Claude Code, `.agents/skills/` per
  Codex, entrambe soltanto in modalita' `both`.
- Il gate blocca cartelle visibili senza classe o proprietario, stanze senza
  mappa, cartelle generiche, vuote, doppie o tecniche, file sciolti nella home e
  instradamenti che non arrivano all'output.
- Aggiunto `ecosistema_inspector.py`, preflight deterministico e in sola
  lettura; il giudizio sui processi e le riparazioni restano all'agente guidato
  dal `CHECKUP.md`.
- Claude Code usa la stessa `memory/` della casa tramite
  `.claude/settings.local.json:autoMemoryDirectory`, fuori Git e attiva dopo
  trust; due memorie divergenti bloccano il verdetto finche' non vengono unite.
- Stato business, storia tecnica e report non sono piu' intercambiabili: stato
  e scadenze nel file proprietario, `install-log` solo per struttura,
  `REPORT_FINALE.md` temporaneo, datato, ignorato da Git ed eliminato a
  `CHIUDI`.
- I contenuti business modificabili vivono fuori dal codice; app e script
  producono derivati e falliscono visibilmente quando la fonte manca.
- L'Ispettore rileva configurazioni credenziali fuori `.secrets/` senza
  leggerle, controlla indice/history Git e richiede rotazione solo se
  l'esposizione non e' esclusa.
- Firma, timbro e sigillo sono asset ad alto rischio: file protetto fuori Git,
  soli metadati in `ASSET.md`, conferma umana per ogni uso.
- I file progetto portano in testa stato corrente, prossimo passo e scadenze;
  il diario resta sotto e ordinato dal piu' recente.
- Aggiunti test reali su una casa simulata: cartella `documenti` generica,
  stanza senza mappe, stanza conforme, funzioni duplicate, file sciolto e skill
  dell'agente mancante; aggiunta anche la regressione integrale della revisione
  operativa a sei giorni.

## 0.3.8 - 27/07/2026

- Aggiunto il gate anti-collaudo circolare: una prova operativa deve esistere
  prima del checkup ed essere indipendente dalla missione che lo avvia.
- L'email di installazione, checkup o report non puo' dimostrare il collegamento
  della casella usata nel lavoro quotidiano; una richiesta inventata durante il
  checkup non puo' dimostrare un processo reale.
- Il report registra ora la provenienza di ogni prova. Se manca una richiesta o
  una fonte preesistente, il processo resta `DA COLLAUDARE` e il gate e'
  obbligatoriamente `NON PASSA`.
- Aggiunto un test di regressione nato dal caso Sansone, nel quale una checklist
  inventata e l'email del checkup erano state accettate come prove reali.

## 0.3.7 - 27/07/2026

- Contratto universale chiuso e provato: ogni `AGENTS.md` versionato ha accanto
  un `CLAUDE.md` Windows-safe con il solo import `@AGENTS.md`, anche quando il
  cliente usa soltanto Codex. Le cartelle `.codex/` e `.claude/` restano invece
  legate agli agenti realmente attivi.
- Installatore reso conservativo sulle case gia' vive: `--force` ripara
  esclusivamente il ponte canonico, non sovrascrive i file del cliente, blocca
  target e registri attraversati da symlink, rifiuta file/directory del tipo
  sbagliato e chiude le regole `.gitignore` sensibili in fondo al file, cosi'
  una negazione precedente non puo' riaprire segreti.
- Git locale reso prevedibile: primo commit solo sulle nuove installazioni,
  nessuno staging/commit automatico nelle repo esistenti e rilanci identici
  senza nuovi log o commit. Report e log dichiarano l'esito reale anche quando
  il commit fallisce.
- Checkup riscritto con rami Codex/Claude separati, gate bloccante verificabile,
  uscita CLI non-zero sui blocchi, report aggiornabile senza verdetti obsoleti
  e autorizzazione esplicita prima di qualunque invio.
- Modulo Portafogli allineato allo stesso contratto, inclusi ponte locale,
  rilevamento reale della configurazione Claude, preflight dei tipi e
  protezione di percorsi, registri e backup da symlink. Ogni contenuto diverso
  sostituito conserva un backup univoco, anche nelle riparazioni successive.
- `EMAIL_CONSEGNA.md` e' la fonte unica dell'email operativa; la prova del
  destinatario viene registrata solo dopo la verifica della versione pubblica.

## 0.3.6 - 27/07/2026

- Il ponte `CLAUDE.md` (`@AGENTS.md`, una riga) c'e' SEMPRE nella cartella
  madre, qualunque agente sia in uso: Claude Code legge `CLAUDE.md`, Codex
  legge `AGENTS.md`. Fonti ufficiali verificate 27/07/2026:
  code.claude.com/docs/en/memory#agents-md (import consigliato, su Windows
  preferito al symlink) e learn.chatgpt.com/docs/agent-configuration/agents-md.
- `.claude/` e `.codex/` restano legate all'agente realmente in uso.
- Telaio, installatore, setup tecnico e contratto della casa allineati.

## 0.3.5 - 27/07/2026

- Il contratto degli agenti della casa (`templates/AGENTS.md`) ora nomina
  `AGENT_CHAT.md` come chat di gruppo: gli agenti sanno dove coordinarsi
  leggendo le regole della casa, senza doverlo scoprire.

## 0.3.4 - 27/07/2026

- Chat di gruppo nella casa cliente: `AGENT_CHAT.md` entra nel telaio
  (template, installazione, setup tecnico e checkup). Tutti gli agenti della
  casa si coordinano li', con regole di disciplina dentro al file.

## 0.3.3 - 27/07/2026

- L'ecosistema vive a se' nel PC: percorso standard `EcosistemaAI-[AZIENDA]`
  nel profilo utente, fuori dalle cartelle di agenti e programmi.
- Permesso di scrittura limitato alla cartella dell'agente = gesto umano:
  l'agente si fa concedere l'accesso al percorso scelto invece di ripiegare
  dentro la propria cartella (caso reale: casa creata in Documenti\Codex
  perche' la sessione scriveva solo li').

## 0.3.2 - 27/07/2026

- La cartella madre porta il nome dell'azienda e vive fuori da cartelle
  intitolate a un agente o a un programma: la casa resta valida quando cambia
  l'agente.
- L'email di consegna indica il percorso completo della cartella madre invece
  della sola scelta locale/cloud.
- L'agente rileva sulla macchina quale assistente gira davvero e lo dichiara nel
  report, invece di riceverlo scritto a distanza.

## 0.3.1 - 17/07/2026

- Il modulo Portafogli riusa anche la convenzione esistente dei casi; una
  struttura minima nuova resta una proposta da approvare.
- L'installer ripara i registri standard mancanti, registra la stanza nella
  tabella canonica della mappa madre e non crea una seconda mappa parallela.
- Puntatori Portafogli univoci vengono auto-riparati; i casi ambigui restano una
  decisione del banker.
- Installazione, checkup e modulo usano ora gli stessi stati email: report
  locale `PRONTO DA INVIARE`, invio solo dopo autorizzazione, poi
  `SAL_VERIFICA` con email archiviata.
- Il checkup accetta `CLAUDE.md` solo come ponte/import o symlink verso
  `AGENTS.md`, non come copia indipendente soggetta a drift.

## 0.3.0 - 17/07/2026

- Lo standard distingue il telaio universale dalla forma aziendale adattiva:
  prima censisce e classifica l'ambiente reale, poi collega le stanze gia' vive.
- Ogni stanza operativa deve essere raggiungibile dalla mappa madre e dichiarare
  fonti, output, capacita', collegamenti a monte e collegamenti a valle.
- Skill, script e moduli sono capacita' di una stanza; diventano una nuova stanza
  solo dopo una proposta motivata e l'approvazione del proprietario.
- Il checkup verifica ora grafo, collegamenti e prove di instradamento, oltre ai
  file tecnici e alle fonti.
- Il modulo Portafogli richiede la stanza proprietaria scelta dopo il censimento;
  non crea piu' `Costruzione Portafogli/` o una skill Claude per default.
- Ogni report registra la versione del metodo e le lezioni candidate emerse sul
  caso reale, cosi' LeaderAI puo' trasformarle in regole e test della repo.

## 0.2.0 - 16/07/2026

- Nuova installazione cliente tramite lettura della repo ufficiale e applicazione
  locale dello standard.
- Clone della repo ed esecuzione di `leaderai_setup.py` spostati nel percorso
  tecnico opzionale, attivabile solo con autorizzazione esplicita.
- Report creato e collaudato localmente prima dell'eventuale invio email.
- File statici dello standard esposti in `templates/`, cosi' l'agente del cliente
  puo' montarli senza eseguire codice scaricato.
