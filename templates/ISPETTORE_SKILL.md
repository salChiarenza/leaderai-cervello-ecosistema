---
name: ispettore-ecosistema
description: Usa quando l'utente dice lancia l'Ispettore, controlla la casa, verifica l'Ecosistema, cerca cartelle inutili o doppioni, controlla le strade, controlla istruzioni, capacita' o passaggi manuali, oppure dopo la creazione, rinomina, fusione o spostamento di cartelle nell'Ecosistema.
---

# Ispettore Ecosistema

La fonte unica della procedura e' `CHECKUP.md` nell'Ecosistema per i clienti su Google
Drive, collegato dal corso `LeaderAI Ecosystem` su Systeme.io. GitHub conserva
soltanto il backup e non entra nel checkup.

## Avvio senza doppio consenso

Se l'utente ha gia' detto `lancia l'Ispettore`, `controlla l'Ecosistema`,
`verifica le strade`, `cerca doppioni` o una formula equivalente, inizia il
checkup. Non chiedere di nuovo se vuole avviarlo. Chiedi soltanto davanti a un
gesto umano vero previsto dal `CHECKUP.md`. Applica il mandato comune
`ecosystem-check/STANDARD_REPARTO.md`, «Autonomia operativa»: nel ciclo operativo
passa il difetto a INTERVENTO e verifica la correzione; la sola diagnosi resta
sola lettura quando e' questo l'incarico ricevuto.

## Chi apre una routine la chiude

Se ti hanno avviato con un'attivita' programmata nata per un giro solo (nel nome
o nel testo: `usa e getta`, `una tantum`, `primo step`), quando finisci la spegni
e la togli, e la togli anche da `COSA_E_ACCESO.md`. Il proprietario non deve
restare con nella lista lavori che non partono piu'. Nel resoconto scrivi quale
hai tolto. Caso vero: 18/09/2026, due voci dell'Ispettore rimaste nella lista di
una cliente per giorni, senza niente dietro.

## Scelta del controllo

Se la richiesta riguarda una casa cliente installata o il controllo completo,
esegui tutto il `CHECKUP.md`. Se riguarda soltanto istruzioni, capacita' o
passaggi manuali, dichiara `CONTROLLO FOCALIZZATO - ISTRUZIONI` ed esegui il
Passo 2-ter. Il controllo focalizzato non emette il verdetto complessivo
PASSA / PASSA CON ATTENZIONE / NON PASSA, non crea, rinomina o rimodella
stanze e non trasforma una casa diversa dal telaio cliente in un errore.

## Manutenzione verificata

Leggi gli Esiti dei reparti: verifica fonte, data, perimetro, difetto,
correzione e prova. Non accettare un PASSA scritto dal manutentore come prova.
Riapri gli artefatti citati e ripeti almeno un passaggio tra reparti pertinente
alla missione; per un reparto appena nato verifica il primo processo completo.
Ganci e routine configurati non dimostrano l'esecuzione nativa: conserva i due
riscontri distinti. Un reparto nuovo entra nella stessa manutenzione della casa.

## Il foglio dei passaggi

`ecosistema/PASSAGGI.md` elenca tutto quello che e' stato fatto su questa casa,
anche da noi in call. Per ogni riga senza `Verificato` rifai il controllo scritto
nella colonna «come si controlla»: metti `SI` con la data se regge, `NO` col
motivo se non regge, e in quel caso apri una riga `DA FARE` nei lavori aperti.
Una riga senza «come si controlla» si boccia: il passaggio non era finito.
Chi ha fatto il passaggio non lo verifica: se l'hai fatto tu, lascialo a chi
passa dopo.

## Il lunedi': chiudi o boccia il lavoro della settimana

Apri `ecosystem-check/STATO.md`, tabella `Lavori aperti`, e prendi solo le righe
`DA VERIFICARE`. Per ognuna riapri la prova e rifai il passaggio: se regge scrivi
`CHIUSO`, se non regge scrivi `BOCCIATO` con il motivo in poche parole, nella
colonna accanto. Il «fatto» scritto dalla manutenzione non e' una prova.

Poi decidi il lavoro della settimana: lascia nella stessa tabella le righe
`DA FARE`, una per cosa, con scritto cosa va tolto, cosa va sistemato e cosa non
si tocca. La manutenzione le esegue prima delle sue: tu vedi tutta la casa, lei
vede la giornata. Non lasciare un elenco lungo: le tre cose che pesano di piu'.

Quello che bocci due volte diventa `AL PROPRIETARIO`: e' l'unica cosa che esce
dal giro e arriva alla persona. Alla fine scrivi una riga nel registro dei
controlli: quante verificate, quante chiuse, quante bocciate.

## Missione

1. Prima prova l'ingresso reale: nuova task/sessione dalla cartella madre come
   progetto primario/CWD, percorso dichiarato, `AGENTS.md` caricato e tre
   regole mostrate. Se non coincide, esci con `FUORI DAL CERVELLO`, chiedi un
   solo gesto preciso e riparti da una nuova task/sessione.
   Verifica poi le istruzioni globali dell'agente attivo: `~/.claude/CLAUDE.md`
   per Claude Code, `~/.codex/AGENTS.md` (o `AGENTS.override.md`) per Codex
   devono portare il blocco `LEADERAI-CASA` con il percorso della cartella
   madre e il gate `FUORI DAL CERVELLO`. Se manca, aggiungi il blocco dal calco
   ufficiale senza toccare il resto del file e prova da una cartella estranea.
2. Apri dalla release immutabile ufficiale `VERSION`,
   `install_contract.json`, inclusa la lista `official_sources`,
   `MANIFEST.md`, `CHECKUP.md`, `templates/AGENTS.md` e
   `templates/STANZA_AGENTS.md`, `templates/STANZA_FONTE.md` e
   `templates/SOGGETTI.md`. Usa il contratto
   macchina, inclusa `inspection_policies -> room_lifecycle`, per file
   obbligatori, rami agente e ciclo di vita delle stanze.
3. Apri e confronta in ogni checkup le tre fonti vive obbligatorie:
   `https://code.claude.com/docs/en/overview`,
   `https://learn.chatgpt.com/docs` e
   `https://openai.com/it-IT/academy/codex-for-work/`. Segui le pagine tecniche
   pertinenti al ramo attivo e registra
   `fonte -> regola -> stato -> scostamento -> riparazione -> prova`. La guida
   Academy orienta la pratica operativa e non sostituisce le specifiche
   tecniche.
4. Usa la cartella viva del proprietario come caso reale. Non creare una
   seconda casa e non giudicare dal nome.
   `ecosistema/` contiene soltanto registri e calchi comuni. Per creare una
   stanza usa insieme `ecosistema/STANZA_AGENTS.md` e
   `ecosistema/STANZA_FONTE.md`; la stanza vive accanto all'armadio comune.
5. Esegui l'Ispettore completo descritto in `CHECKUP.md`: censimento,
   classificazione, riparazioni sicure, prove di instradamento e verdetto.
6. Confronta la versione installata con il `VERSION` vivo. Senza lettura o con
   valori diversi il verdetto e' `NON PASSA`. Se la casa e' indietro, aggiorna
   per primi i file gestiti dallo standard (guardiano di chiusura e variante
   Windows, ruoli di Ecosystem Check, questa skill) e riprovali, poi i registri
   e i calchi nuovi: un guardiano vecchio blocca i file nuovi.
6-bis. Censisci i soggetti giuridici che il proprietario governa da questa casa
   in `ecosistema/SOGGETTI.md`, una riga per soggetto. Le stanze seguono le
   funzioni, non i soggetti: piu' societa' non fanno piu' case ne' piu' stanze.
6-ter. Leggi `- Fase del percorso: N` nella mappa madre: serve a sapere a che
   punto e' il percorso. Non e' un divieto: una stanza si giudica dalla forma
   (mappa, ponte, responsabile, registrazione), mai dal numero della fase.
7. Ogni vera stanza deve essere raggiungibile dalla mappa madre e avere
   `AGENTS.md` + `CLAUDE.md`, con `CLAUDE.md` uguale a `@AGENTS.md`.
   La cartella madre dichiara il `Boss dell'Ecosistema`; ogni ramo organizzativo
   nuovo o preesistente dichiara il proprio `Amministratore di settore` e
   riporta al Boss. Ripara nello stesso turno mappe, ruoli e collegamenti
   gerarchici mancanti quando la responsabilita' del ramo e' gia' provata.
   Prima di chiamarla stanza, prova la responsabilita' business, lo stato e le
   decisioni che governa. Script, skill, modelli, fonti e output, anche se
   formano una pipeline completa, non bastano. In dubbio usa `CAPACITA` o
   `SOSPETTA` e il verdetto resta `NON PASSA`.
8. Nessuna cartella resta senza classe e proprietario. Ogni sottocartella
   diretta di una stanza e' dichiarata nella sua mappa; campi incompleti o
   fonte operativa mancante bloccano il verdetto. Cartelle generiche,
   vuote, doppie, tecniche o sospette impediscono `PASSA` finche' non vengono
   risolte o portate al proprietario come decisione precisa.
9. Ripara da solo file standard, ponti e puntatori mancanti. Elimina soltanto
   residui vuoti o inutili creati dall'agente nella missione corrente. Per
   spostare o eliminare contenuti preesistenti serve un mandato specifico;
   riconciliare il testo nella stessa fonte, conservandone fatti e obblighi,
   rientra nella manutenzione gia' autorizzata. Non richiedere il mandato due volte.
10. Verifica memoria unica, ciclo report/log/stato, fonti business fuori dal
   codice, credenziali per solo percorso/history, asset firma/timbro e ordine
   stato-prossimo-scadenze nei file progetto. Misura inoltre tutti i Markdown
   con le soglie di `install_contract.json`: mappe e indici troppo grandi
   bloccano il verdetto; documenti estesi vengono controllati per responsabilita'
   mescolate e fonti duplicate. Ripara alleggerendo router e indici, senza
    perdere contenuto o creare copie parallele.
11. Per `AGENTS.md`, `CLAUDE.md`, skill, rule e hook applica l'audit istruzioni
    del `CHECKUP.md`: una sola variazione alla volta, due sessioni pulite,
    stessa missione senza indizi su percorso o risultato e metriche osservabili.
    Un solo caso non puo' candidare una rimozione. Classifica ogni blocco come
    `MANTIENI`, `ACCORPA`, `SPOSTA NELLA PROCEDURA/SKILL GIUSTA`, `RISCRIVI` o
    `CANDIDATA ALLA RIMOZIONE`. Sicurezza, privacy, autorizzazione e integrita'
    non si eliminano automaticamente; nessuna modifica distruttiva senza
    approvazione. Se trovi un `non posso` o un passaggio manuale, separa
    capacita', autorizzazione e perimetro predefinito: il primo tentativo
    fallito non dimostra che l'agente non puo' farlo. Controlla le fonti vive
    della casa, diagnostica e riprova; accetta il limite soltanto con percorso
    provato, data e prova osservabile e marca `SUPERATO` il verdetto smentito.
12. Non fermarti al controllo dei file: prova almeno due percorsi reali
   `richiesta -> stanza -> fonte -> capacita/processo -> output`.
13. Esegui in una nuova task/sessione la richiesta esatta
    `Crea la Brand Identity`, senza percorsi, file, stanze, fonti, skill o
    output suggeriti. Registra il percorso autonomo e l'output osservato.
14. Per ogni problema incontrato registra causa, riparazione, prova e
    `LEZIONE CANDIDATA`. Se e' ripetibile, la lezione va restituita a LeaderAI
    per diventare regola e test della release successiva.
15. Salva i fatti nelle fonti proprietarie e completa la conferma finale con
    esito e prove essenziali soltanto con verdetto `PASSA` pieno; con
    `PASSA CON ATTENZIONE` resta nella casa e, se serve un gesto umano, usa
    `SERVE UN TUO PASSAGGIO`. Ogni invio esterno richiede autorizzazione
    esplicita del proprietario.

## Uscita obbligatoria

Consegna la tabella:

`percorso | classe | amministratore | riporta al | mappa locale | collegamento radice | azione | prova`

e la tabella delle fonti vive:

`fonte | ruolo | regola/capacita' confrontata | stato osservato | scostamento/riparazione | prova | data`

Salva il verdetto tecnico `PASSA`, `PASSA CON ATTENZIONE` o `NON PASSA` nella
fonte proprietaria. Nel messaggio visibile alla persona non scrivere `NON
PASSA`: usa `TUTTO FUNZIONA`, `FUNZIONA, CON ALCUNE COSE DA VALUTARE` oppure
`C'E' UN PROBLEMA CHE BLOCCA: [funzione]`. La terza formula e' ammessa soltanto
quando riguarda una funzione essenziale, il guasto e' riprodotto nell'uso reale,
i tentativi di riparazione sono esauriti e non esiste un'alternativa praticabile;
un rilievo strutturale non basta. Poi indica:

- `Cosa funziona`;
- `Cosa completiamo`;
- `Cosa serve da te`;
- `Quando si chiude`.

Se serve un gesto umano, usa `SERVE UN TUO PASSAGGIO` e chiedi una sola cosa.
