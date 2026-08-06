---
name: ispettore-ecosistema
description: Usa quando l'utente dice lancia l'Ispettore, controlla la casa, verifica l'Ecosistema, cerca cartelle inutili o doppioni, controlla le strade, oppure dopo la creazione, rinomina, fusione o spostamento di cartelle nell'Ecosistema.
---

# Ispettore Ecosistema

La fonte unica della procedura e' `CHECKUP.md` nella repo ufficiale
`salChiarenza/leaderai-cervello-ecosistema`.

## Avvio senza doppio consenso

Se l'utente ha gia' detto `lancia l'Ispettore`, `controlla l'Ecosistema`,
`verifica le strade`, `cerca doppioni` o una formula equivalente, inizia il
checkup. Non chiedere di nuovo se vuole avviarlo. Chiedi soltanto davanti a un
gesto umano vero previsto dal `CHECKUP.md`.

## Missione

1. Prima prova l'ingresso reale: nuova task/sessione dalla cartella madre come
   progetto primario/CWD, percorso dichiarato, `AGENTS.md` caricato e tre
   regole mostrate. Se non coincide, esci con `FUORI DAL CERVELLO`, chiedi un
   solo gesto preciso e riparti da una nuova task/sessione.
2. Apri dalla release immutabile ufficiale `VERSION`,
   `install_contract.json`, inclusa la lista `official_sources`,
   `MANIFEST.md`, `CHECKUP.md`, `templates/AGENTS.md` e
   `templates/STANZA_AGENTS.md`. Usa il contratto macchina per file
   obbligatori e rami agente.
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
   Per creare una mappa locale usa il calco gia' installato
   `ecosistema/STANZA_AGENTS.md`.
5. Esegui l'Ispettore completo descritto in `CHECKUP.md`: censimento,
   classificazione, riparazioni sicure, prove di instradamento e verdetto.
6. Confronta la versione installata con il `VERSION` vivo. Senza lettura o con
   valori diversi il verdetto e' `NON PASSA`.
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
8. Nessuna cartella resta senza classe e proprietario. Cartelle generiche,
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
    approvazione.
12. Non fermarti al controllo dei file: prova almeno due percorsi reali
   `richiesta -> stanza -> fonte -> capacita/processo -> output`.
13. Esegui in una nuova task/sessione la richiesta esatta
    `Crea la Brand Identity`, senza percorsi, file, stanze, fonti, skill o
    output suggeriti. Registra il percorso autonomo e l'output osservato.
14. Per ogni problema incontrato registra causa, riparazione, prova e
    `LEZIONE CANDIDATA`. Se e' ripetibile, la lezione va restituita a LeaderAI
    per diventare regola e test della release successiva.
15. Completa il resoconto locale. Aprilo con `STATO PER LE PERSONE`: `Fatto`,
    `Manca`, `Prossimo passo`, `Intervento umano`; poi inserisci dettagli e
    prove tecniche. Ogni invio esterno richiede autorizzazione esplicita del
    proprietario.

## Uscita obbligatoria

Consegna la tabella:

`percorso | classe | amministratore | riporta al | mappa locale | collegamento radice | azione | prova`

e la tabella delle fonti vive:

`fonte | ruolo | regola/capacita' confrontata | stato osservato | scostamento/riparazione | prova | data`

Poi indica soltanto:

- cosa hai riparato;
- cosa resta davvero da decidere;
- verdetto `PASSA`, `PASSA CON ATTENZIONE` o `NON PASSA`.
