# LeaderAI Cervello + Ecosistema

Repo installabile per creare la cartella madre AI di un cliente.

Questa repo e' letta sia da Claude Code sia da Codex. `CLAUDE.md`, se
presente, deve essere un symlink o una copia di questo file.

## Cosa fa

Monta in una cartella cliente lo standard minimo LeaderAI:

- `.gitignore` che esclude `.secrets/`, `*.env`, token, chiavi e credenziali
- inizializza la cartella madre come repository git (se non lo e' gia')
- `AGENTS.md` come mappa comune del Cervello
- `CLAUDE.md` se il cliente usa Claude Code
- `.codex/README.md` se serve Codex
- `.claude/README.md` se serve Claude Code
- `memory/MEMORY.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `REPORT_FINALE.md`

## Regola madre

Il cliente non deve fare debug tecnico. L'agente del cliente fa autodiagnosi,
installa o ripara cio' che manca, crea la cartella madre nel posto giusto e
chiude solo dopo un collaudo reale.

## Scelta agente

La repo e' una sola, ma l'installazione non deve creare tutto a caso.

- Se il cliente sta usando Claude Code, usare `--agent claude`.
- Se il cliente sta usando Codex, usare `--agent codex`.
- Usare `--agent both` solo se LeaderAI lo chiede esplicitamente per preparare
  la stessa cartella a entrambi gli agenti.

L'agente cliente deve configurare solo la modalita' con cui sta lavorando. Non
crea la configurazione dell'altro agente per prudenza o per abitudine.

Dove mettere la cartella madre si decide caso per caso, con domande guidate, non
con una regola fissa. Le opzioni sono disco locale oppure cartella sincronizzata
(OneDrive / Google Drive). Avviso da dire chiaro: Claude Code, mentre scrive,
puo' corrompere o troncare i file su cartelle cloud con file on-demand (bug
noti); il cliente sceglie se accettare il rischio in cambio della comodita' di
usarla da piu' PC. Evitare comunque `Downloads`, `Desktop` o cartelle temporanee
come destinazione finale.

Per clienti con piu' computer, backup e seconda postazione si scelgono col
cliente: GitHub privato (cartella madre = repository git, `push` a comando,
secondo PC via `clone` + `pull`/`push`) oppure copia/sincronizzazione su
Drive/OneDrive, secondo cosa il cliente gia' usa. I documenti di business restano
su Drive/OneDrive/server e si leggono via connettore; non entrano nella repo.

## Uso cliente

Il file da consegnare e':

- `INSTALLA_CON_AI.md`

Il cliente incolla quel testo in Claude Code o Codex. Prima del clone non ha
questa repo, quindi la missione deve stare tutta nel testo.

## Divieti

- Non salvare segreti, password, token o dati bancari.
- Mai far entrare i segreti nella cronologia git: `.secrets/`, `*.env`, token,
  chiavi e credenziali stanno nel `.gitignore`. Questo vale sempre, qualunque
  posizione abbia scelto il cliente. I connettori si ri-autorizzano con login su
  ogni PC, le chiavi non viaggiano nel backup.
- Non imporre una posizione: la cartella madre puo' stare in locale o su cloud
  secondo la scelta del cliente. Sul cloud va dato l'avviso sul rischio
  corruzione/troncamento; locale e' la via piu' sicura ma non e' l'unica.
- Non cancellare o spostare file del cliente senza conferma esplicita.
- Non creare doppioni di cartelle se ne esiste gia' una viva.
- Non sovrascrivere file esistenti senza `--force` e senza motivo chiaro.
- Non promettere output professionali regolamentati: l'agente prepara bozze,
  il professionista verifica, decide e firma.

## Riflesso asset operativo

Ogni volta che nasce una risorsa da usare o rispettare (PEC, email, banca, auto,
gestionale, Drive, WhatsApp, fornitore, sito, repo, kit, app, archivio), il
cliente deve ritrovarla in `ecosistema/ASSET.md`.

La regola e' una: casa/fonte vera + riga asset + eventuale processo/limite
aggiornato + log. Se manca la fonte reale, resta `DA COLLEGARE`; non si inventa.

## Comandi

Collaudo repo:

```bash
python3 -m unittest discover -s tests
```

Installazione manuale:

```bash
python3 leaderai_setup.py --target /percorso/EcosistemaAI-Cliente --client "Nome Cliente" --agent claude
```

## Quando finisci una modifica

1. Aggiorna `README.md`, `MANIFEST.md` o `INSTALLA_CON_AI.md` se cambia un fatto
   critico.
2. Esegui i test.
3. Commit e push su GitHub: la base cliente e' la repo, non il clone locale.
4. Aggiorna l'anagrafe LeaderAI in `leaderai/memory/reference_mcp_attivi.md`.
