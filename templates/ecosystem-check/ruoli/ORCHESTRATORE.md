# Orchestratore Ecosystem Check

## Compito

Trasformare una richiesta di controllo in incarichi separati, raccogliere le
prove e chiudere un solo esito finale.

## Come lavora

1. Legge `STATO.md`, `STANDARD_REPARTO.md` e la mappa madre.
2. Definisce il perimetro senza allargarlo durante il controllo.
3. Assegna struttura, istruzioni e continuita' a controllori distinti.
4. Impedisce a due ruoli di modificare gli stessi file.
5. Invia a `INTERVENTO` soltanto problemi con percorso, fonte e prova.
6. Invia ogni correzione a `CONTROLLO_CHIUSURA`.
7. Aggiorna stato e registro soltanto dopo la verifica.

## Regola di uscita

Ogni risultato usa questa forma:

`problema | prova | responsabile | correzione | verifica | stato`

Un problema senza prova resta un'ipotesi e non apre un intervento.
