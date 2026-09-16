# Email di consegna — Cervello LeaderAI

Questo file serve all'agente LeaderAI che prepara la prima email. Non contiene
la procedura di installazione o aggiornamento: quella vive in un solo documento
versionato su Drive, `01 - Cervello - installazione e aggiornamento.md`.

## Controlli prima dell'invio

1. Leggi la scheda del cliente e verifica nome e destinatario.
2. Usa il mittente `sal@salchiarenza.com`.
3. Controlla che il link si apra come destinatario, che il file si chiami
   `01 - Cervello - installazione e aggiornamento.md` e mostri la versione
   corrente indicata in `VERSION`.
4. Controlla Gmail Inviati per evitare un doppione nelle ultime 24 ore.
5. Mostra a Sal oggetto e corpo completi; invia soltanto dopo la sua
   autorizzazione esplicita.
6. Dopo l'invio verifica Inviati e aggiorna lo stato del cliente.

## Modello corrente

Oggetto: `Cervello LeaderAI — installazione o aggiornamento`

### Corpo HTML

```html
<p>Ciao [NOME],</p>
<p>per installare o aggiornare il tuo Cervello LeaderAI, apri questo documento
con ChatGPT Work, Codex o Claude Code e segui le istruzioni fino al controllo
finale:</p>
<p><a href="https://drive.google.com/file/d/19l_f_VViewXaVVhq3in9KBnnqkoRyh7E/view">Apri 01 - Cervello - installazione e aggiornamento.md</a></p>
<p>L'agente ti chiedera' soltanto eventuali accessi, permessi o decisioni che
richiedono il tuo intervento.</p>
<p>Sal</p>
```

### Corpo testuale

Ciao [NOME],

per installare o aggiornare il tuo Cervello LeaderAI, apri questo documento
con ChatGPT Work, Codex o Claude Code e segui le istruzioni fino al controllo
finale:

01 - Cervello - installazione e aggiornamento.md
https://drive.google.com/file/d/19l_f_VViewXaVVhq3in9KBnnqkoRyh7E/view

L'agente ti chiedera' soltanto eventuali accessi, permessi o decisioni che
richiedono il tuo intervento.

Sal
