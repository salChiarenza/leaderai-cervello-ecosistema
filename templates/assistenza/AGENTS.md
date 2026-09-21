# assistenza

Questa e' la mappa locale di `assistenza/`: lo sportello della casa, non una stanza
di lavoro. Non tiene stato, non tiene decisioni, non produce output per il
proprietario: tiene le tre carte che servono quando qualcosa si e' fermato.

## Scopo

Dare all'assistente un posto solo dove andare quando ha un problema con la casa:
da quale sintomo si parte, quale guida si apre, a chi si scrive se resta fermo.
Prima queste tre cose vivevano sparse fra i registri e nessuno le trovava al
momento giusto.

## Dentro

- `SINTOMI.md` - la tabella sintomo -> carta. E' l'ingresso: si entra da cosa sta
  succedendo, non dal nome di un file. La legge anche il guardiano delle carte.
- `MANUALI.md` - le guide ufficiali degli strumenti, con accanto quando si apre
  quale. La legge anche il guardiano dei manuali.
- `CONTATTO.md` - l'assistenza LeaderAI: cosa scrivere e a chi, quando hai
  provato e sei ancora fermo.
- NESSUNA SOTTOCARTELLA.

## Quando ci si entra

- Una cosa della casa non funziona e non sai quale carta apre quel guasto:
  `SINTOMI.md`, e la riga ti manda dove devi andare.
- Stai per dire come funziona un comando, una skill, un permesso o
  un'impostazione: `MANUALI.md`, prima di rispondere.
- Hai provato e sei ancora fermo: `CONTATTO.md`, invece di tacere.

Non ci si entra per capire com'e' montata la casa: quella e'
`ecosistema/COME_E_MESSA_IN_PIEDI.md`. Qui si entra col guasto in mano.

## Regole

- Ogni carta porta, subito sotto il titolo, la riga `**Quando si apre:**` con il
  momento reale in cui un assistente deve venire qui.
- La tabella di `SINTOMI.md` e' l'unica fonte del legame sintomo -> carta: una
  riga nuova li' e' attiva subito, senza toccare nessun programma.
- Le carte non si copiano altrove: chi le nomina mette il percorso, non il testo.
- Qui non vivono registri del cliente, materiali business, stato o diari: quelli
  stanno in `ecosistema/` e nelle stanze.
