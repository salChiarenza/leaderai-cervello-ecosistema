# Chat di gruppo — {{client_name}}

Chat condivisa tra TUTTI gli agenti che lavorano in questa casa (Codex, Claude
Code e quelli che arriveranno). Gli agenti leggono e scrivono file: questa e'
la loro bacheca comune, il posto dove si coordinano quando lavorano sulla
stessa cosa.

## Regole d'uso

1. **Nuove note sempre in CIMA**, sotto `## Log`. La piu' recente per prima.
2. **Ogni nota dichiara**: data/ora, ID missione, agente proprietario, stato,
   base Git, obiettivo, file coinvolti, prove, prossimo agente e prossimo passo.
3. **Massimo 20 righe per nota.** Se serve di piu', file dedicato e link qui.
4. **Una nota vive 48 ore.** Poi si promuove nel file giusto (stato, procedura,
   `ecosistema/ASSET.md`) e si toglie da qui. La chat e' coordinamento; la
   memoria vive in `memory/`, lo stato nel file proprietario della stanza.
5. **Leggere tutto il log prima di scrivere o di dichiarare "nessuna risposta".**
6. Prima di modificare file importanti, annunciare qui cosa si tocca, per
   evitare che due agenti lavorino sullo stesso file insieme.
7. L'agente che riceve un handoff rilegge tutto il log e aggiunge
   `PRESO IN CARICO` nella stessa missione prima di continuare.
8. A ogni nuova sessione si legge questo file prima dei file operativi.

## Calco nota

```text
### [DATA/ORA] [ID MISSIONE] — [AGENTE]
Stato: CLAIM / PRESO IN CARICO / BLOCCO / FATTO
Base Git: [SHA o NON PRESENTE]
Obiettivo: [...]
File: [...]
Prove: [...]
Prossimo agente: [...]
Prossimo passo: [...]
```

## Collaudo continuita'

In una casa `both`, la continuita' passa soltanto con questa prova reale:
Codex apre una nuova task dalla cartella madre e lascia un handoff; Claude Code
apre una nuova sessione dalla stessa cartella, scrive `PRESO IN CARICO` e
continua senza suggerimenti esterni; una nuova task Codex rilegge il risultato
e chiude la missione. Tre sessioni distinte, una sola casa, un solo ID.

## Log

(vuoto — prima nota degli agenti qui sopra)
