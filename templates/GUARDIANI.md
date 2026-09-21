# I guardiani della casa

**Quando si apre:** quando l'assistente si e' fermato e non sai chi l'ha fermato, o quando una cosa che doveva essere impedita e' passata lo stesso.

> Un guardiano e' una regola che scatta da sola nel momento in cui stai per
> sbagliare. Non e' un promemoria: una regola scritta e basta viene ignorata.
>
> Questo elenco e' la fonte unica. Vale per ogni assistente che lavora in questa
> casa, anche per quelli che non possono eseguire programmi.

## Come si installano

- **Claude Code e Codex**: si installano da soli quando monti la casa (Fase 4,
  «Gestione dell'ecosistema»). L'assistente copia i programmi in `.agent/hooks/`
  e aggiunge i richiami nelle proprie impostazioni, senza toccare quelle che
  trova gia'. Dopo l'installazione lo provi cosi': metti un file a caso nella
  cartella madre e chiedi all'assistente di chiudere il lavoro. Deve fermarsi.
  **Se non si ferma, il guardiano c'e' ma e' spento, e questa e' la cosa piu'
  pericolosa: sembra acceso.** Su Windows la causa e' quasi sempre una sola: le
  impostazioni chiamano i guardiani con `python3`, che su Windows non esiste.
  Si sostituisce `python3` con `py` nelle impostazioni dell'assistente e si
  rifa' la prova. La prova va rifatta ogni volta che si aggiorna la casa.
- **Assistenti che non eseguono programmi** (ChatGPT sul web e simili): i
  programmi non partono, quindi **queste righe sono la regola**. Prima di
  chiudere una risposta l'assistente controlla le righe che riguardano il lavoro
  che sta facendo e si comporta di conseguenza.

## L'elenco

| Guardiano | Cosa impedisce | Quando scatta |
|---|---|---|
| Dati verificati | dare un dato concreto - link, IBAN, prezzo, data, nome - senza averlo aperto, coprendosi con «se e' diverso dimmelo» | mentre chiude la risposta |
| Doppioni | creare un file nuovo quando quello per la stessa cosa esiste gia' (tipico: stesso nome con la data attaccata) | prima di scrivere un file |
| Email operativa | mandare un'email che racconta il lavoro invece di dire dove siamo, cosa cambia e cosa serve da chi legge | prima di inviare |
| Memoria | ripetere un errore gia' imparato, perche' la lezione giusta non e' arrivata al momento giusto | a ogni richiesta del proprietario |
| Note fra assistenti | scrivere nella chat di gruppo una nota che chi non c'era non capisce | dopo aver scritto la nota |
| Un blocco per turno | che due guardiani parlino insieme e la stessa risposta venga ripubblicata due volte | quando piu' di un guardiano vorrebbe fermarsi |
| Stanze | chiudere un lavoro lasciando file, cartelle o copie fuori dal posto che gli spetta | alla chiusura del turno |
| Copia di sicurezza | perdere la casa: ogni giorno ne resta una copia datata fuori dal computer | una volta al giorno |
| Note in arrivo | lavorare senza sapere cosa ha appena fatto l'altro assistente | a ogni richiesta, se la chat e' cambiata da poco |
| Manuali | spiegare come funziona uno strumento andando a memoria, o aprire la guida sbagliata (rispondere su Codex leggendo la documentazione di Claude) | quando la richiesta nomina uno strumento che ha il suo manuale in `assistenza/MANUALI.md` |
| Carte | lasciare chiuse le carte della casa mentre il proprietario sta raccontando proprio il sintomo che una di loro risolve, invece di aprire la riga di `assistenza/SINTOMI.md` | a ogni richiesta del proprietario che descrive un sintomo |
| Archivi protetti | toccare archivi e segreti scambiandoli per disordine da sistemare | quando si valuta o si pulisce una cartella |

## Regola di manutenzione

Un guardiano nuovo nasce con la sua riga qui, nello stesso lavoro. Un guardiano
senza riga non esiste per chi legge, e una riga senza guardiano e' una promessa:
il collaudo del prodotto tiene le due cose attaccate.

Installarlo non basta: va anche **richiamato nelle impostazioni di tutti e due
gli assistenti**, Claude Code e Codex. Un guardiano copiato nella casa ma che
nessuno chiama e' spento, e sembra acceso. Vale anche quando gli si insegna un
caso nuovo: se cambia cio' che deve riconoscere, si guarda anche il punto in cui
viene chiamato. La stessa prova controlla che ogni guardiano di questo elenco sia
richiamato in tutte e due le case.
