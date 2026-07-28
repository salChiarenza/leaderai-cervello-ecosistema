# Email di consegna — Cervello + Ecosistema

Modello unico e versionabile per la prima consegna. Questa email e
`INSTALLA_CON_AI.md` sono le due fonti proprietarie del percorso: messaggio e
procedura.

Modo corrente: `AGENTE_CON_POSTA`.

Il corpo viene letto ed eseguito direttamente dall'agente collegato alla
casella del cliente. Dalla prima riga tutti i verbi parlano allo stesso
lettore. Il proprietario interviene nei gesti umani che l'agente gli presenta.

## Stato prova destinatario

`PROVA_DESTINATARIO_OK — 28/07/2026`

Verifica completata partendo dal solo archivio pubblico della versione `0.4.4`,
commit funzionale `c4c5451db4a314b3ea70d04edb8af59b3ecebf9b`.
L'archivio misura `136703` byte e ha SHA-256
`11ff1ae9b0f11a919006d2ac06f42dacd1a9c400275144937b17e0df040f804a`.
La versione letta dall'archivio e' `0.4.4` e tutti i `97` test risultano
superati.

## Controlli prima dell'invio

1. Verifica dal livello di accesso del destinatario che repo e procedura siano
   pubbliche e leggibili.
2. Conferma che il lettore operativo sia l'agente collegato alla posta.
3. Compila tutti i placeholder da fonti reali.
4. Con una cartella madre presente, l'agente parte da quella. Per una nuova
   casa, parte dalla cartella padre autorizzata, crea il percorso concordato e
   usa l'eventuale richiesta nativa di accesso; il proprietario conferma quel
   gesto.
5. Mostra al proprietario oggetto, corpo HTML e fallback testuale completi.
6. L'autorizzazione esplicita del proprietario attiva questo invio.
7. Il report viene creato, collaudato e mostrato localmente; l'autorizzazione
   successiva del proprietario attiva l'eventuale invio del report.

## Modello corrente

Oggetto: `Installazione Cervello + Ecosistema — [AZIENDA]`

### Corpo HTML

```html
<p><strong>Questa missione operativa e' per l'agente AI che gestisce
l'ambiente di [NOME].</strong></p>

<p>Parti dalla cartella madre <strong>[PERCORSO COMPLETO]</strong>. Quando il
percorso deve essere creato, chiedi a [NOME] di autorizzare la cartella padre
concordata e di confermare l'eventuale richiesta nativa di accesso.</p>

<p>Apri in sola lettura la
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/main/INSTALLA_CON_AI.md">procedura ufficiale LeaderAI 0.4.4</a>
e usa la
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema">repo ufficiale</a>
come standard.</p>

<p>Cliente: [NOME]<br>
Azienda: [AZIENDA]<br>
Cartella madre: [PERCORSO COMPLETO]<br>
Backup: [SCELTA VERIFICATA]<br>
Seconda postazione: [SI / NO]</p>

<p>Dichiara nel report se stai operando come Claude Code o Codex. Il telaio comune comprende sempre
<code>AGENTS.md</code> e <code>CLAUDE.md</code> con
<code>@AGENTS.md</code>. Configura <code>.codex/</code> soltanto per Codex,
<code>.claude/</code> soltanto per Claude Code, entrambe soltanto se LeaderAI
lo ha richiesto esplicitamente.</p>

<p>Confronta la versione installata con <code>VERSION 0.4.4</code>, configura
la memoria unica prevista per l'agente attivo e usa
<code>ecosistema/STANZA_AGENTS.md</code> per ogni stanza reale. Lancia
l'Ispettore, ripara i punti sicuri e prova le strade fino agli output.</p>

<p>Completa il <code>REPORT_FINALE.md</code> temporaneo con data e stato e
mostralo localmente a [NOME]. Il suo comando <code>manda</code> autorizza
l'eventuale invio del report.</p>

<p>[FIRMA AGENTE: Sal &amp; Codex / Sal &amp; Claude Code]</p>
```

### Fallback text/plain

```text
Questa missione operativa e' per l'agente AI che gestisce l'ambiente di [NOME].

Parti dalla cartella madre [PERCORSO COMPLETO]. Quando il percorso deve essere
creato, chiedi a [NOME] di autorizzare la cartella padre concordata e di
confermare l'eventuale richiesta nativa di accesso.

Procedura ufficiale:
https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/main/INSTALLA_CON_AI.md

Repo ufficiale:
https://github.com/salChiarenza/leaderai-cervello-ecosistema

Cliente: [NOME]
Azienda: [AZIENDA]
Cartella madre: [PERCORSO COMPLETO]
Backup: [SCELTA VERIFICATA]
Seconda postazione: [SI / NO]

Dichiara nel report se stai operando come Claude Code o Codex. Il telaio comune comprende sempre AGENTS.md e
CLAUDE.md con @AGENTS.md. Configura .codex/ soltanto per Codex, .claude/
soltanto per Claude Code, entrambe soltanto su richiesta esplicita LeaderAI.

Confronta la versione installata con VERSION 0.4.4, configura la memoria unica
prevista per l'agente attivo e usa ecosistema/STANZA_AGENTS.md per ogni stanza
reale. Lancia l'Ispettore, ripara i punti sicuri e prova le strade fino agli
output.

Completa il REPORT_FINALE.md temporaneo con data e stato e mostralo localmente
a [NOME]. Il suo comando manda autorizza l'eventuale invio del report.

[FIRMA AGENTE: Sal & Codex / Sal & Claude Code]
```

Quando una scelta richiede il proprietario, scrivi `DA DECIDERE`, presentagli
la decisione concreta e riprendi dopo la sua risposta. Percorsi, account e
stato dei collegamenti arrivano dalle fonti verificate.
