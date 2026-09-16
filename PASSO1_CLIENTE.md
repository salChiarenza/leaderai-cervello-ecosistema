# Cervello LeaderAI - Passo 1

Versione corrente: `0.7.1`

## Il risultato

Alla fine hai una sola cartella di lavoro con nove documenti ordinari: memoria,
fonti, strumenti, processi, limiti, soggetti, chat e registro di installazione.
Il pacchetto non contiene programmi e non cambia le impostazioni di Claude o
Codex. Skill, controlli automatici e attivita' programmate appartengono al
Passo 4 e richiedono una scelta separata.

## Cosa scaricare

Nella stessa cartella Drive di questa guida trovi `Cervello.zip`. Dentro devono
esserci soltanto:

- `VERSION` e `install_contract.json`;
- file Markdown nei percorsi indicati dal contratto;
- nessun file eseguibile e nessuna cartella di configurazione dell'assistente.

Se il contenuto e' diverso, fermati e segnalalo a LeaderAI.

## Installazione semplice

1. Scarica `Cervello.zip` e decomprimilo.
2. Rinomina la cartella `Cervello` con il nome della tua attivita'.
3. Spostala nella posizione in cui vuoi lavorare.
4. Apri quella cartella come progetto locale in Claude Code o Codex.
5. Invia all'assistente il messaggio qui sotto.

```text
Questa e' la mia cartella di lavoro LeaderAI. Leggi README.md,
install_contract.json e i documenti presenti. Verifica che il pacchetto
contenga soltanto file Markdown e JSON nei percorsi dichiarati.

Poi sostituisci nei documenti solo questi dati:
- {{client_name}} = [scrivi qui il tuo nome o quello dell'attivita']
- {{date}} = [data di oggi]
- {{version}} = il valore del file VERSION

Non aggiungere skill, programmi, collegamenti ad account, configurazioni
dell'assistente o attivita' programmate. Non sovrascrivere eventuali documenti
gia' compilati: se ne trovi, mostrami il conflitto.

Alla fine mostrami: percorso della cartella, versione e lista dei nove
documenti. Il risultato e' corretto solo se tutti esistono e i segnaposto sono
stati sostituiti.
```

## Verifica visibile

La cartella e' pronta quando:

- `VERSION` mostra `0.7.1`;
- esistono tutti i nove documenti elencati in `install_contract.json`;
- nei documenti non restano `{{client_name}}`, `{{date}}` o `{{version}}`;
- non sono comparse cartelle nascoste di configurazione o file eseguibili.

Questo chiude il Passo 1. Il Passo 2 serve a compilare la mappa del lavoro con
fonti e processi reali.
