---
name: manutentore-ecosistema
description: Usa quando l'utente dice fai manutenzione, lancia il Manutentore, pulisci la casa, i file sono troppo grandi, archivia il vecchio, oppure quando l'automazione giornaliera di manutenzione parte. Misura tutta la casa con il guardiano, ripara da solo le cose meccaniche e reversibili, riporta al proprietario il resto.
---

# Manutentore Ecosistema

Il Manutentore e' il manager della manutenzione continua della casa. Ogni
giorno misura tutto, ripara da solo cio' che e' meccanico e reversibile,
rimisura e lascia tre righe. Non giudica: chi giudica e' l'Ispettore
(`ispettore-ecosistema`) a comando e il proprietario.

## Avvio senza doppio consenso

Se l'utente ha detto `fai manutenzione`, `lancia il Manutentore`, `pulisci la
casa`, `archivia il vecchio` o l'automazione giornaliera e' partita, comincia
subito. Non chiedere conferma per le riparazioni ammesse qui sotto: sono
reversibili e restano nella casa.

## 1. Misura

1. Posizionati nella cartella madre (quella con `AGENTS.md` e `.agent/hooks/`).
2. Esegui `bash .agent/hooks/guardiano_stanze.sh --misura` (su Windows:
   `powershell .agent/hooks/guardiano_stanze_windows.ps1 --misura`). Ogni riga
   stampata e' un problema con il suo percorso. Nessuna riga: casa entro le
   soglie, passa al punto 4.
3. Raggruppa le righe per stanza (prima cartella del percorso). Ogni stanza si
   ripara da sola, una alla volta, senza toccare le altre.

## 2. Ripara (solo queste cose, per ogni stanza)

Ammesso, senza chiedere:

- **Documento oltre 800 righe o 80 KiB** (file diverso da mappe e chat): sposta
  le sezioni datate (`## gg/mm/aaaa ...` o `## aaaa-mm-gg ...`) piu' vecchie di
  7 giorni in `<nome>_archivio_<aaaa-mm-gg>.md` nella stessa cartella, in cima
  al file di archivio, con una riga di intestazione che dice da dove vengono e
  quando. Nel file vivo lascia una riga `> Archivio: <nome file>`. Se il file
  non ha sezioni datate, non toccarlo: segnalalo al proprietario.
- **Mappa oltre 350 righe** (`AGENTS.md`, `MEMORY.md`): non tagliare. Segnala
  al proprietario con il numero di righe: una mappa si accorpa con giudizio.
- **`AGENT_CHAT.md` oltre 350 righe o con note piu' vecchie di 48 ore**: sposta
  le note vecchie in `AGENT_CHAT_archivio_<aaaa-mm-gg>.md` accanto, lasciando
  in chat le note delle ultime 48 ore e la riga `> Note piu' vecchie: <file>`.
- **Percorso nascosto al proprietario**: rendilo visibile (`chflags nohidden`
  su Mac, `attrib -h` su Windows).
- **Skill gemelle diverse** (`.claude/skills/X/SKILL.md` e
  `.agents/skills/X/SKILL.md`): copia la piu' recente sull'altra, tranne le
  righe che nominano l'agente (firma `Sal & Claude` / `Sal & Codex`).

Vietato, sempre: eliminare file o cartelle, riscrivere contenuti, spostare
file fuori dalla loro stanza, toccare `.secrets/`, `.git/`, `logs/`, inviare
email o messaggi, creare copie `_v2`/`_finale`, creare nuove stanze. Cartelle
vuote, copie parallele, stanze senza mappa e classi mancanti vanno al
proprietario come decisione, con percorso preciso.

## 3. Rimisura

Rilancia `guardiano_stanze.sh --misura`. Le righe sparite sono riparazioni
riuscite; quelle rimaste sono per il proprietario.

## 4. Scrivi

- In `ecosystem-check/STATO.md`, sezione `## Manutenzione giornaliera`, in cima:
  data, quante cose trovate, quante riparate (cosa e dove), quante restano e a
  chi. Massimo 5 righe, massimo 7 giornate conservate: le piu' vecchie si
  tolgono.
- Se hai riparato almeno una cosa, una riga in
  `ecosystem-check/REGISTRO_CONTROLLI.md` con data, perimetro, trovati,
  chiusi, aperti, esito `MANUTENZIONE`, prova (il file di archivio creato).
- Rileggi `ecosystem-check/CONTROLLI.md`: ogni riga `MANCA` va ripetuta al
  proprietario finche' non diventa `ATTIVO`.

## 5. Riporta

Al proprietario al massimo 5 righe in parole normali: quante cose, cosa hai
sistemato, cosa resta a lui e dove sta il resoconto. Niente percorsi lunghi,
niente sigle. Poi chiudi ogni superficie aperta e termina la sessione.

## Automazione

L'installazione crea l'automazione giornaliera `manutenzione-ecosistema`
(ore 07:45 locali, modello leggero) che invoca questa skill. Chi la apre la
chiude: una sola sessione, nessun accumulo. Se l'automazione manca, il checkup
la segnala e la fa creare.

Creato da LeaderAI Cervello + Ecosistema il {{today}} per {{client_name}}
(standard {{version}}).
