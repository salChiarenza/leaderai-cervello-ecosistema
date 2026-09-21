# Email di consegna — Cervello LeaderAI

Questo file serve all'agente LeaderAI che prepara la prima email. Non contiene
la procedura di installazione o aggiornamento: quella vive in un solo documento
versionato su Drive, `01 - Cervello - installazione e aggiornamento.md`.

## Controlli prima dell'invio

1. Leggi la scheda del cliente e verifica nome e destinatario.
2. Usa il mittente `sal@salchiarenza.com`.
3. Il link e' sempre quello della **cartella** `1 Cervello`, mai quello del
   singolo documento: un link a un file non mostra la cartella che lo contiene,
   e la guida rimanda al pacchetto che sta li' accanto. Caso 20/09/2026,
   Simona Vari: dal link al solo documento non trovava `Cervello.zip` e ha
   creduto che mancasse un allegato. Controlla che la cartella si apra come
   destinatario, che dentro ci siano il documento e il pacchetto, e che il
   documento mostri la versione corrente indicata in `VERSION`.
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
<p><a href="https://drive.google.com/drive/folders/1SzRA4SCSyXw_PnHWP7ouGeNzUv6Wcl1L">Apri la cartella 1 Cervello</a></p>
<p>Dentro trovi due cose, una accanto all'altra: il documento
<strong>01 - Cervello - installazione e aggiornamento</strong> e il pacchetto
<strong>Cervello.zip</strong>. Non c'e' niente in allegato a questa email: si
scarica tutto da li', cosi' prendi sempre la versione piu' recente.</p>
<p>L'agente ti chiedera' soltanto eventuali accessi, permessi o decisioni che
richiedono il tuo intervento.</p>
<p>Sal</p>
```

### Corpo testuale

Ciao [NOME],

per installare o aggiornare il tuo Cervello LeaderAI, apri questo documento
con ChatGPT Work, Codex o Claude Code e segui le istruzioni fino al controllo
finale:

Cartella 1 Cervello
https://drive.google.com/drive/folders/1SzRA4SCSyXw_PnHWP7ouGeNzUv6Wcl1L

Dentro trovi due cose, una accanto all'altra: il documento
"01 - Cervello - installazione e aggiornamento" e il pacchetto Cervello.zip.
Non c'e' niente in allegato a questa email: si scarica tutto da li', cosi'
prendi sempre la versione piu' recente.

L'agente ti chiedera' soltanto eventuali accessi, permessi o decisioni che
richiedono il tuo intervento.

Sal
