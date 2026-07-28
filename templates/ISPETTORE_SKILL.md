---
name: ispettore-ecosistema
description: Usa quando l'utente dice lancia l'Ispettore, controlla la casa, verifica l'Ecosistema, cerca cartelle inutili o doppioni, controlla le strade, oppure dopo la creazione, rinomina, fusione o spostamento di cartelle nell'Ecosistema.
---

# Ispettore Ecosistema

La fonte unica della procedura e' `CHECKUP.md` nella repo ufficiale
`salChiarenza/leaderai-cervello-ecosistema`.

## Missione

1. Apri dalla repo ufficiale `VERSION`, `MANIFEST.md`, `CHECKUP.md`,
   `templates/AGENTS.md` e `templates/STANZA_AGENTS.md`.
2. Usa la cartella viva del proprietario come caso reale. Non creare una
   seconda casa e non giudicare dal nome.
3. Esegui l'Ispettore completo descritto in `CHECKUP.md`: censimento,
   classificazione, riparazioni sicure, prove di instradamento e verdetto.
4. Ogni vera stanza deve essere raggiungibile dalla mappa madre e avere
   `AGENTS.md` + `CLAUDE.md`, con `CLAUDE.md` uguale a `@AGENTS.md`.
5. Nessuna cartella resta senza classe e proprietario. Cartelle generiche,
   vuote, doppie, tecniche o sospette impediscono `PASSA` finche' non vengono
   risolte o portate al proprietario come decisione precisa.
6. Ripara da solo file standard, ponti e puntatori mancanti. Elimina soltanto
   residui vuoti o inutili creati dall'agente nella missione corrente. Per
   spostare, fondere o eliminare contenuti preesistenti chiedi conferma.
7. Non fermarti al controllo dei file: prova almeno due percorsi reali
   `richiesta -> stanza -> fonte -> capacita/processo -> output`.
8. Completa il resoconto locale. Ogni invio esterno richiede autorizzazione
   esplicita del proprietario.

## Uscita obbligatoria

Consegna la tabella:

`percorso | classe | proprietario | mappa locale | collegamento radice | azione | prova`

Poi indica soltanto:

- cosa hai riparato;
- cosa resta davvero da decidere;
- verdetto `PASSA`, `PASSA CON ATTENZIONE` o `NON PASSA`.
