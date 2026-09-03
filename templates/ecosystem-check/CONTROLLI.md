# Registro dei controlli - un controllo per ogni cosa che nasce

Legge della casa: ogni stanza, procedura, automazione o capacita' nasce con il
suo controllo. Una riga qui risponde a quattro domande: chi controlla, quando,
cosa misura, dove scrive. Stato `ATTIVO` oppure `MANCA` con la data: un `MANCA`
e' un debito visibile che il Manutentore ripete finche' non si chiude.

| Area / fase | Cosa deve essere vero | Chi controlla | Quando | Cosa misura | Dove scrive | Stato |
|---|---|---|---|---|---|---|
| Casa intera | Mappe entro 350 righe, documenti entro 800, chat di gruppo entro 48 ore, niente copie parallele, niente cartelle vuote o nascoste | guardiano di chiusura + Manutentore (`manutentore-ecosistema`) | ogni chiusura di turno + ogni giorno | soglie di `install_contract.json` | blocco in chat; `STATO.md` (Manutenzione) | ATTIVO |
| Struttura delle stanze | Ogni stanza con mappa completa, ponte `@AGENTS.md`, fonte operativa, registrazione nella mappa madre | guardiano di chiusura + Ispettore (`ispettore-ecosistema`) | chiusura turno + a comando | contratto di stanza | blocco in chat; `REGISTRO_CONTROLLI.md` | ATTIVO |
| Istruzioni degli agenti | `AGENTS.md`, `CLAUDE.md`, skill e hook coerenti con lo standard installato | Ispettore (`CHECKUP.md`, audit istruzioni) | a ogni checkup | versione installata vs standard vivo | `REGISTRO_CONTROLLI.md` | ATTIVO |
| Continuita' operativa | Stato, prossimo passo e scadenze in testa a ogni fonte operativa | controllore `ruoli/CONTROLLO_CONTINUITA.md` | a ogni ciclo | ordine stato-prossimo-scadenze | `STATO.md` | ATTIVO |
| Nuova stanza o capacita' | Nasce con classe, mappa, fonte e riga in questo registro | guardiano di chiusura | chiusura turno | presenza della riga | blocco in chat | ATTIVO |

## Come si usa

- Cosa nuova, riga nuova, prima di dire finito. Il proprietario della stanza
  scrive la riga; se il controllo ancora non esiste, scrive `MANCA` con la data.
- Il controllo non e' la procedura: qui stanno le quattro risposte, il come
  vive nel file proprietario.
- Il Manutentore rilegge ogni giorno le righe `MANCA` e le riporta al
  proprietario finche' non diventano `ATTIVO`.
