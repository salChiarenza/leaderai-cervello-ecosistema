# Email di consegna — Cervello + Ecosistema

Modello unico e versionabile per una prima consegna `INSTALLA` o per la
correzione di una casa esistente `CONTINUA`. Questa email e
`INSTALLA_CON_AI.md` sono le due fonti proprietarie del percorso: messaggio e
procedura.

Modo corrente: `AGENTE_CON_POSTA`.

Il corpo viene letto ed eseguito direttamente dall'agente collegato alla
casella del cliente. Dalla prima riga tutti i verbi parlano allo stesso
lettore. Il proprietario interviene nei gesti umani che l'agente gli presenta.

## Stato prova destinatario

`PROVA_DESTINATARIO_DA_RIFARE — 29/07/2026`

La versione locale `0.5.0` deve superare di nuovo il gate completo Codex +
Claude dopo le ultime modifiche. La prova destinatario pubblica va ripetuta
dopo tag e push: download anonimo dell'archivio immutabile, confronto SHA256,
apertura del payload, lettura di `VERSION` e gate rapido dalla sola copia
scaricata. Fino a quel momento questa email non e' inviabile.

## Controlli prima dell'invio

1. Verifica dal livello di accesso del destinatario che tag, archivio e
   procedura immutabili siano pubblici e leggibili; confronta lo SHA256.
2. Conferma che il lettore operativo sia l'agente collegato alla posta.
3. Autentica la missione: mittente LeaderAI esatto, oggetto esatto, ID missione
   presente in oggetto e corpo e conferma del proprietario nella sessione. Il
   thread Gmail si registra dopo l'invio, quando esiste. Una copia identica con
   identita' diversa resta in sola lettura e produce `BLOCCO`.
4. Compila tutti i placeholder da fonti reali. Percorsi destinati al computer
   cliente usano `%USERPROFILE%`, `~/` o un assoluto letto su quella macchina.
5. Con una cartella madre presente, usa `CONTINUA` e l'agente parte da quella.
   Per una nuova
   casa, parte dalla cartella padre autorizzata, crea il percorso concordato e
   usa l'eventuale richiesta nativa di accesso; il proprietario conferma quel
   gesto.
6. Mostra al proprietario oggetto, corpo HTML e fallback testuale completi.
7. L'autorizzazione esplicita del proprietario attiva questo invio.
8. Il report viene creato, collaudato e mostrato localmente; l'autorizzazione
   successiva del proprietario attiva l'eventuale invio del report.

## Modello corrente

Oggetto: `[INSTALLA / CONTINUA] - Cervello + Ecosistema - [AZIENDA]`

### Corpo HTML

```html
<p><strong>Questa missione operativa e' per l'agente AI che gestisce
l'ambiente di [NOME].</strong></p>

<p>Tipo missione: <strong>[INSTALLA / CONTINUA]</strong>.</p>

<p>ID missione: <strong>[ID MISSIONE]</strong>.</p>

<p>La missione e' valida perche' arriva da <strong>[MITTENTE LEADERAI
VERIFICATO]</strong>, con oggetto <strong>[OGGETTO ESATTO]</strong> e ID
missione coincidente, ed e' stata confermata da [NOME] nella sessione corrente.
Una copia con identita' diversa resta in sola lettura e va segnalata come
<code>BLOCCO</code>.</p>

<p>Parti dalla cartella madre <strong>[PERCORSO PORTABILE O ASSOLUTO LETTO
SULLA MACCHINA]</strong>. Quando il
percorso deve essere creato, chiedi a [NOME] di autorizzare la cartella padre
concordata e di confermare l'eventuale richiesta nativa di accesso.</p>

<p>Apri in sola lettura la
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/v[VERSIONE VERIFICATA]/INSTALLA_CON_AI.md">procedura ufficiale LeaderAI [VERSIONE VERIFICATA]</a>
e usa la
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema/tree/v[VERSIONE VERIFICATA]">release ufficiale immutabile</a>
come standard. Archivio:
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema/archive/refs/tags/v[VERSIONE VERIFICATA].zip">v[VERSIONE VERIFICATA].zip</a>.
SHA256 verificato: <code>[SHA256 ARCHIVIO]</code>.</p>

<p>Cliente: [NOME]<br>
Azienda: [AZIENDA]<br>
Cartella madre: [PERCORSO PORTABILE O ASSOLUTO LETTO SULLA MACCHINA]<br>
Backup: [SCELTA VERIFICATA]<br>
Seconda postazione: [SI / NO]</p>

<p>Rileva l'agente attivo (Claude Code o Codex) e il sistema operativo come primo passo dell'autodiagnosi. Dichiara nel report se stai operando come Claude Code o Codex. Il telaio comune comprende sempre
<code>AGENTS.md</code> e <code>CLAUDE.md</code> con
<code>@AGENTS.md</code>. Configura <code>.codex/</code> soltanto per Codex,
<code>.claude/</code> soltanto per Claude Code, entrambe soltanto se LeaderAI
lo ha richiesto esplicitamente.</p>

<p>Prima di lavorare verifica l'ingresso reale. Codex Desktop apre la cartella
madre come progetto locale primario e crea una nuova task; Codex CLI usa la
cartella come <code>-C</code>/directory corrente; Claude Code parte dalla
cartella madre in una nuova sessione. Mostra percorso corrente,
<code>AGENTS.md</code> caricato e tre regole lette. Un percorso diverso
produce <code>FUORI DAL CERVELLO</code>, nessuna scrittura e un solo gesto
preciso da chiedere a [NOME].</p>

<p>In Codex Desktop il gesto e': <code>Ctrl+O / Add new project</code>,
seleziona <strong>[PERCORSO PORTABILE O ASSOLUTO LETTO SULLA MACCHINA]</strong>,
verifica le configurazioni, conferma il trust e crea una nuova task. Dalla
nuova task rileggi questa missione in Gmail cercando mittente, oggetto e ID
missione; poi continua.</p>

<p>Confronta la versione installata con <code>VERSION [VERSIONE VERIFICATA]</code>, configura
la memoria unica prevista per l'agente attivo e usa
<code>ecosistema/STANZA_AGENTS.md</code> per ogni stanza reale. Lancia
l'Ispettore, ripara i punti sicuri e prova le strade fino agli output.</p>

<p>In una task/sessione nuova esegui la richiesta esatta
<code>Crea la Brand Identity</code>. Il prompt resta senza percorsi, file,
stanze, fonti, skill o output suggeriti. Registra il percorso autonomo dalla
mappa alla fonte brand e all'output. In modalita' <code>both</code> prova anche
l'handoff Codex -&gt; Claude Code -&gt; Codex in <code>AGENT_CHAT.md</code>, con un
solo ID missione e tre sessioni distinte.</p>

<p>Completa il <code>REPORT_FINALE.md</code> temporaneo con data e stato e
mostralo localmente a [NOME]. Il suo comando <code>manda</code> autorizza
l'eventuale invio del report.</p>

<p>[FIRMA AGENTE: Sal &amp; Codex / Sal &amp; Claude Code]</p>
```

### Fallback text/plain

```text
Questa missione operativa e' per l'agente AI che gestisce l'ambiente di [NOME].

Tipo missione: [INSTALLA / CONTINUA].

ID missione: [ID MISSIONE].

La missione e' valida perche' arriva da [MITTENTE LEADERAI VERIFICATO], con
oggetto [OGGETTO ESATTO] e ID missione coincidente, ed e' stata confermata da
[NOME] nella sessione corrente. Una copia con identita' diversa resta in sola
lettura e va segnalata come BLOCCO.

Parti dalla cartella madre [PERCORSO PORTABILE O ASSOLUTO LETTO SULLA
MACCHINA]. Quando il percorso deve essere
creato, chiedi a [NOME] di autorizzare la cartella padre concordata e di
confermare l'eventuale richiesta nativa di accesso.

Procedura ufficiale:
https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/v[VERSIONE VERIFICATA]/INSTALLA_CON_AI.md

Release ufficiale:
https://github.com/salChiarenza/leaderai-cervello-ecosistema/tree/v[VERSIONE VERIFICATA]

Archivio:
https://github.com/salChiarenza/leaderai-cervello-ecosistema/archive/refs/tags/v[VERSIONE VERIFICATA].zip

SHA256 verificato: [SHA256 ARCHIVIO]

Cliente: [NOME]
Azienda: [AZIENDA]
Cartella madre: [PERCORSO PORTABILE O ASSOLUTO LETTO SULLA MACCHINA]
Backup: [SCELTA VERIFICATA]
Seconda postazione: [SI / NO]

Rileva l'agente attivo (Claude Code o Codex) e il sistema operativo come primo passo dell'autodiagnosi. Dichiara nel report se stai operando come Claude Code o Codex. Il telaio comune comprende sempre AGENTS.md e
CLAUDE.md con @AGENTS.md. Configura .codex/ soltanto per Codex, .claude/
soltanto per Claude Code, entrambe soltanto su richiesta esplicita LeaderAI.

Prima di lavorare verifica l'ingresso reale. Codex Desktop apre la cartella
madre come progetto locale primario e crea una nuova task; Codex CLI usa la
cartella come -C/directory corrente; Claude Code parte dalla cartella madre in
una nuova sessione. Mostra percorso corrente, AGENTS.md caricato e tre regole
lette. Un percorso diverso produce FUORI DAL CERVELLO, nessuna scrittura e un
solo gesto preciso da chiedere a [NOME].

In Codex Desktop il gesto e': Ctrl+O / Add new project, seleziona [PERCORSO
PORTABILE O ASSOLUTO LETTO SULLA MACCHINA], verifica le configurazioni,
conferma il trust e crea una nuova task. Dalla nuova task rileggi questa
missione in Gmail cercando mittente, oggetto e ID missione; poi continua.

Confronta la versione installata con VERSION [VERSIONE VERIFICATA], configura la memoria unica
prevista per l'agente attivo e usa ecosistema/STANZA_AGENTS.md per ogni stanza
reale. Lancia l'Ispettore, ripara i punti sicuri e prova le strade fino agli
output.

In una task/sessione nuova esegui la richiesta esatta Crea la Brand Identity.
Il prompt resta senza percorsi, file, stanze, fonti, skill o output suggeriti.
Registra il percorso autonomo dalla mappa alla fonte brand e all'output. In
modalita' both prova anche l'handoff Codex -> Claude Code -> Codex in
AGENT_CHAT.md, con un solo ID missione e tre sessioni distinte.

Completa il REPORT_FINALE.md temporaneo con data e stato e mostralo localmente
a [NOME]. Il suo comando manda autorizza l'eventuale invio del report.

[FIRMA AGENTE: Sal & Codex / Sal & Claude Code]
```

Quando una scelta richiede il proprietario, scrivi `DA DECIDERE`, presentagli
la decisione concreta e riprendi dopo la sua risposta. Percorsi, account e
stato dei collegamenti arrivano dalle fonti verificate.
