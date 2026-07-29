---
name: ispettore-ecosistema
description: Usa quando l'utente dice lancia l'Ispettore, controlla la casa, verifica l'Ecosistema, cerca cartelle inutili o doppioni, controlla le strade, oppure dopo la creazione, rinomina, fusione o spostamento di cartelle nell'Ecosistema.
---

# Ispettore Ecosistema

La fonte unica della procedura e' `CHECKUP.md` nella repo ufficiale
`salChiarenza/leaderai-cervello-ecosistema`.

## Missione

1. Prima prova l'ingresso reale: nuova task/sessione dalla cartella madre come
   progetto primario/CWD, percorso dichiarato, `AGENTS.md` caricato e tre
   regole mostrate. Se non coincide, esci con `FUORI DAL CERVELLO`, chiedi un
   solo gesto preciso e riparti da una nuova task/sessione.
2. Apri dalla release immutabile ufficiale `VERSION`,
   `install_contract.json`,
   `MANIFEST.md`, `CHECKUP.md`, `templates/AGENTS.md` e
   `templates/STANZA_AGENTS.md`. Usa il contratto macchina per file
   obbligatori e rami agente.
3. Usa la cartella viva del proprietario come caso reale. Non creare una
   seconda casa e non giudicare dal nome.
   Per creare una mappa locale usa il calco gia' installato
   `ecosistema/STANZA_AGENTS.md`.
4. Esegui l'Ispettore completo descritto in `CHECKUP.md`: censimento,
   classificazione, riparazioni sicure, prove di instradamento e verdetto.
5. Confronta la versione installata con il `VERSION` vivo. Senza lettura o con
   valori diversi il verdetto e' `NON PASSA`.
6. Ogni vera stanza deve essere raggiungibile dalla mappa madre e avere
   `AGENTS.md` + `CLAUDE.md`, con `CLAUDE.md` uguale a `@AGENTS.md`.
   Prima di chiamarla stanza, prova la responsabilita' business, lo stato e le
   decisioni che governa. Script, skill, modelli, fonti e output, anche se
   formano una pipeline completa, non bastano. In dubbio usa `CAPACITA` o
   `SOSPETTA` e il verdetto resta `NON PASSA`.
7. Nessuna cartella resta senza classe e proprietario. Cartelle generiche,
   vuote, doppie, tecniche o sospette impediscono `PASSA` finche' non vengono
   risolte o portate al proprietario come decisione precisa.
8. Ripara da solo file standard, ponti e puntatori mancanti. Elimina soltanto
   residui vuoti o inutili creati dall'agente nella missione corrente. Per
   spostare, fondere o eliminare contenuti preesistenti chiedi conferma.
9. Verifica memoria unica, ciclo report/log/stato, fonti business fuori dal
   codice, credenziali per solo percorso/history, asset firma/timbro e ordine
   stato-prossimo-scadenze nei file progetto.
10. Non fermarti al controllo dei file: prova almeno due percorsi reali
   `richiesta -> stanza -> fonte -> capacita/processo -> output`.
11. Esegui in una nuova task/sessione la richiesta esatta
    `Crea la Brand Identity`, senza percorsi, file, stanze, fonti, skill o
    output suggeriti. Registra il percorso autonomo e l'output osservato.
12. Completa il resoconto locale. Ogni invio esterno richiede autorizzazione
   esplicita del proprietario.

## Uscita obbligatoria

Consegna la tabella:

`percorso | classe | proprietario | mappa locale | collegamento radice | azione | prova`

Poi indica soltanto:

- cosa hai riparato;
- cosa resta davvero da decidere;
- verdetto `PASSA`, `PASSA CON ATTENZIONE` o `NON PASSA`.
