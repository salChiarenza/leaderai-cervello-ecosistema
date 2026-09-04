---
name: ispettore-ecosistema
description: Usa quando l'utente dice lancia l'Ispettore, controlla la casa, verifica l'Ecosistema, cerca cartelle inutili o doppioni, controlla le strade, controlla istruzioni, capacita' o passaggi manuali, oppure dopo la creazione, rinomina, fusione o spostamento di cartelle nell'Ecosistema.
---

# Ispettore Ecosistema

La fonte unica della procedura e' `CHECKUP.md` nell'Ecosistema Base su Google
Drive, collegato dal corso `LeaderAI Ecosystem` su Systeme.io. GitHub conserva
soltanto il backup e non entra nel checkup.

## Avvio senza doppio consenso

Se l'utente ha gia' detto `lancia l'Ispettore`, `controlla l'Ecosistema`,
`verifica le strade`, `cerca doppioni` o una formula equivalente, inizia il
checkup. Non chiedere di nuovo se vuole avviarlo. Chiedi soltanto davanti a un
gesto umano vero previsto dal `CHECKUP.md`.

## Scelta del controllo

Se la richiesta riguarda una casa cliente installata o il controllo completo,
esegui tutto il `CHECKUP.md`. Se riguarda soltanto istruzioni, capacita' o
passaggi manuali, dichiara `CONTROLLO FOCALIZZATO - ISTRUZIONI` ed esegui il
Passo 2-ter. Il controllo focalizzato non emette il verdetto complessivo
PASSA / PASSA CON ATTENZIONE / NON PASSA, non crea, rinomina o rimodella
stanze e non trasforma una casa diversa dal telaio cliente in un errore.

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
6-ter. Leggi `- Fase del percorso: N` nella mappa madre. Sotto il 3 nessuna
   stanza di lavoro: una stanza registrata con fase 1 o 2 e' `ROOM_BEFORE_STEP_3`
   e blocca il verdetto. La riga la alza solo la missione che chiude il passo.
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
   spostare, fondere o eliminare contenuti preesistenti chiedi conferma.
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
fonte proprietaria. Nel messaggio visibile alla persona indica soltanto:

- `Cosa funziona`;
- `Cosa completiamo`;
- `Cosa serve da te`;
- `Quando si chiude`.

Se serve un gesto umano, usa `SERVE UN TUO PASSAGGIO` e chiedi una sola cosa.
