# Email di consegna — Cervello + Ecosistema

Modello unico e versionabile per la prima consegna. La procedura operativa vive
in `INSTALLA_CON_AI.md`; nessun altro file duplica questa email.

## Stato prova destinatario

`PROVA_DESTINATARIO_OK — 27/07/2026`

Verifica anonima completata sulla versione pubblica `0.3.7`, commit `670dced`:
repo, `VERSION`, `EMAIL_CONSEGNA.md`, `INSTALLA_CON_AI.md`, `CHECKUP.md`,
`templates/CLAUDE.md` e ponte Portafogli sono leggibili senza account. Il
percorso descritto dalla sola email raggiunge tutti i file necessari.

## Controlli prima dell'invio

1. Verifica dal livello di accesso del destinatario che repo e procedura siano
   pubbliche e leggibili.
2. Compila tutti i placeholder da fonti reali.
3. Se la cartella madre esiste, l'agente parte da quella. Se manca, parte dalla
   cartella padre autorizzata, crea il percorso concordato e usa l'eventuale
   richiesta nativa di accesso; il proprietario conferma soltanto quel gesto.
4. Mostra al proprietario oggetto, corpo HTML e fallback testuale completi.
5. Invia solo dopo un'autorizzazione esplicita riferita a questo testo.
6. Nessun report o follow-up parte automaticamente: il report viene prima
   creato, collaudato e mostrato localmente.

## Modello corrente

Oggetto: `Installazione Cervello + Ecosistema — [AZIENDA]`

### Corpo HTML

```html
<p>Ciao [NOME],</p>

<p>apri [AGENTE ATTIVO: Codex / Claude Code] nella cartella madre
<strong>[PERCORSO COMPLETO]</strong>. Se la cartella non esiste ancora, apri
la cartella padre concordata e lascia che l'agente crei il percorso; quando
compare la richiesta nativa di accesso, conferma quel singolo gesto.</p>

<p>Affidagli questa missione:</p>

<p>Apri in sola lettura la
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/main/INSTALLA_CON_AI.md">procedura ufficiale LeaderAI</a>
e usa la
<a href="https://github.com/salChiarenza/leaderai-cervello-ecosistema">repo ufficiale</a>
come standard.</p>

<p>Cliente: [NOME]<br>
Azienda: [AZIENDA]<br>
Cartella madre: [PERCORSO COMPLETO]<br>
Backup: [SCELTA VERIFICATA]<br>
Seconda postazione: [SI / NO]</p>

<p>Rileva l'agente che sta lavorando davvero. Il telaio comune comprende sempre
<code>AGENTS.md</code> e <code>CLAUDE.md</code> con
<code>@AGENTS.md</code>. Configura <code>.codex/</code> soltanto per Codex,
<code>.claude/</code> soltanto per Claude Code, entrambe soltanto se LeaderAI
lo ha richiesto esplicitamente.</p>

<p>Diagnostica, integra, prova e completa <code>REPORT_FINALE.md</code>.
Mostrami il report locale. Ogni invio email successivo richiede una mia nuova
autorizzazione esplicita.</p>

<p>[FIRMA AGENTE: Sal &amp; Codex / Sal &amp; Claude Code]</p>
```

### Fallback text/plain

```text
Ciao [NOME],

apri [AGENTE ATTIVO: Codex / Claude Code] nella cartella madre
[PERCORSO COMPLETO]. Se non esiste, apri la cartella padre concordata e lascia
che l'agente crei il percorso; conferma soltanto l'eventuale richiesta nativa
di accesso.

Procedura ufficiale:
https://github.com/salChiarenza/leaderai-cervello-ecosistema/blob/main/INSTALLA_CON_AI.md

Repo ufficiale:
https://github.com/salChiarenza/leaderai-cervello-ecosistema

Cliente: [NOME]
Azienda: [AZIENDA]
Cartella madre: [PERCORSO COMPLETO]
Backup: [SCELTA VERIFICATA]
Seconda postazione: [SI / NO]

Rileva l'agente attivo. Il telaio comune comprende sempre AGENTS.md e
CLAUDE.md con @AGENTS.md. Configura .codex/ soltanto per Codex, .claude/
soltanto per Claude Code, entrambe soltanto su richiesta esplicita LeaderAI.

Diagnostica, integra, prova e completa REPORT_FINALE.md. Mostrami il report
locale. Ogni invio email successivo richiede una mia nuova autorizzazione
esplicita.

[FIRMA AGENTE: Sal & Codex / Sal & Claude Code]
```

Se una scelta manca, scrivi `DA DECIDERE` e risolvila con il proprietario prima
dell'invio. Non inventare percorsi, account o stato dei collegamenti.
