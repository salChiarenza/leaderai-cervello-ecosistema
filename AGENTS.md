# LeaderAI Cervello + Ecosistema

Repo installabile per creare la cartella madre AI di un cliente.

Questa repo e' letta sia da Claude Code sia da Codex. `AGENTS.md` e'
la fonte unica comune; `CLAUDE.md` e' sempre presente e contiene soltanto
`@AGENTS.md`. Una copia indipendente crea drift.

Regola madre: questa repo e' lo standard LeaderAI, la cartella viva del cliente
e' il caso reale. Ogni checkup confronta il caso reale con `MANIFEST.md`,
`templates/AGENTS.md`, `templates/STANZA_AGENTS.md` e le istruzioni operative
della repo; poi ripara, prova e riporta gli scostamenti.

`install_contract.json` e' la fonte macchina unica per installazione manuale,
setup tecnico, Ispettore e harness di rilascio. Vietato mantenere una seconda
lista di file obbligatori o rami agente.

Lo standard ha due strati: il telaio universale del Cervello e il metodo
adattivo con cui si scoprono le stanze del cliente. La repo non assegna nomi di
reparti o cartelle business: censisce l'ambiente reale, classifica stanze,
fonti, output, capacita', infrastruttura e archivi, poi verifica che ogni stanza
sia raggiungibile dalla mappa madre. Un modulo si integra nella cartella madre
o nella stanza proprietaria; una nuova stanza richiede una responsabilita'
business autonoma e l'approvazione del proprietario.

## Cosa fa

Monta in una cartella cliente lo standard minimo LeaderAI:

- `.gitignore` che esclude `.secrets/`, `*.env`, token, chiavi, credenziali e
  `REPORT_FINALE.md`
- inizializza la cartella madre come repository git (se non lo e' gia')
- `AGENTS.md` come mappa comune del Cervello
- `CLAUDE.md` come ponte permanente di una riga (`@AGENTS.md`)
- `.codex/README.md` se serve Codex
- `.claude/README.md` se serve Claude Code
- user settings Claude Code (`~/.claude/settings.json`) con
  `autoMemoryDirectory` sulla memoria canonica della casa, verificate su ogni PC
- skill `ispettore-ecosistema` nel percorso dell'agente attivo
- `memory/MEMORY.md`
- `AGENT_CHAT.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `ecosistema/STANZA_AGENTS.md`
- `REPORT_FINALE.md` solo come output temporaneo e datato della missione aperta

Questi sono il telaio e i registri comuni. Le stanze operative del cliente non
sono elencate qui: emergono dai suoi processi reali e rispettano il contratto
adattivo di `MANIFEST.md`.

Moduli professionali versionati:

- `moduli/portafogli/` - costruzione Core-Satellite, analisi, backtest,
  monitoraggio e report cliente con motore deterministico e validazione del
  banker. L'agente sceglie prima la cartella madre o la stanza proprietaria e poi segue
  `moduli/portafogli/INSTALLA_MODULO.md`.

Il report temporaneo della missione deve includere la mappa moduli con stato per PEC/email
certificata, email/calendario, Drive/cartelle, CRM/gestionale, plugin, skill,
agenti/ruoli, guardiani/hook, ronde, voce/dettatura e compliance/privacy/AI Act.

## Regola madre

Il cliente non deve fare debug tecnico. L'agente del cliente fa autodiagnosi,
installa o ripara cio' che manca, crea la cartella madre nel posto giusto e
chiude solo dopo un collaudo reale.

## Telaio comune e scelta agente

La repo e' una sola. Il contratto comune esiste sempre nella cartella madre e
in ogni vera stanza: `AGENTS.md` come fonte unica e `CLAUDE.md` come ponte
`@AGENTS.md`.

- Se il cliente sta usando Claude Code, usare `--agent claude`.
- Se il cliente sta usando Codex, usare `--agent codex`.
- Usare `--agent both` solo se LeaderAI lo chiede esplicitamente per preparare
  la stessa cartella a entrambi gli agenti.

`--agent` governa soltanto la configurazione specifica: `.claude/` per Claude
Code, `.codex/` per Codex o entrambe con `both`. Non governa la presenza del
telaio comune `AGENTS.md` + `CLAUDE.md`.

## Comunicazione e fonti di verita'

Gli agenti non si parlano direttamente. Si coordinano leggendo e scrivendo file
condivisi.

| Caso | Dove si scrive nel Cervello/Ecosistema cliente | Durata |
|---|---|---|
| Stato business corrente, prossimo passo, scadenze | file proprietario della stanza | finche' cambia |
| Storia tecnica/strutturale | `logs/install-log.md` | stabile |
| Output della missione aperta | `REPORT_FINALE.md`, datato e fuori Git | fino a `CHIUDI` |
| Procedura / come si fa una cosa | file del reparto o dell'area che la usa, es. `ecosistema/PROCESSI.md` o una procedura dedicata | stabile |
| Problema di allineamento tra Claude e Codex | un sync dedicato solo se il cliente usa entrambi gli agenti | finche' il sync si chiude |
| Coordinamento immediato sullo stesso file | una chat temporanea solo se serve evitare collisioni | massimo 48 ore |
| Asset/capacita' nuova | `ecosistema/ASSET.md` | stabile |

Regola pratica: se una nota spiega "come si fa", non va in chat. Va nella
procedura o nel file proprietario. La chat e' solo coordinamento temporaneo.

## Protocollo missioni LeaderAI

Il ciclo e' chiuso e semplice:

`MISSIONE` -> `ESECUZIONE` -> `AUTOCONTROLLO` -> `REPORT` -> `SAL_VERIFICA` -> `CONTINUA` oppure `CHIUDI`.

- `MISSIONE`: l'agente del cliente legge l'email con oggetto concreto, apre link/file e
  segue lo schema indicato.
- `ESECUZIONE`: fa le azioni, ripara cio' che puo', prova cio' che dichiara.
- `AUTOCONTROLLO`: prima di scrivere a Sal rilegge missione, azioni, prove,
  file toccati, blocchi umani veri e superfici aperte da lui.
- `REPORT`: completa e collauda il report locale, lo mostra al proprietario e
  lo lascia `PRONTO DA INVIARE`; l'invio a `sal@salchiarenza.ai` avviene solo
  dopo autorizzazione esplicita del proprietario per quello specifico invio.
- `SAL_VERIFICA`: aspetta risposta LeaderAI; lo stato resta nel report
  temporaneo.
- `CONTINUA`: lavora ancora sulla stessa missione, aggiorna il report e chiede
  una nuova autorizzazione prima dell'eventuale nuovo invio.
- `CHIUDI`: promuove i fatti nelle fonti proprietarie, usa il log solo per
  cambi strutturali, elimina il report e chiude pagine/app aperte da lui.

Regola posta: dopo aver letto e gestito una email o notifica, archiviala nello
stesso giro. La Inbox contiene solo blocchi o decisioni immediate ancora attivi;
`SAL_VERIFICA` resta tracciato nei log/report, non nella Inbox.

Non creare automatismi permanenti tra agenti: ogni giro nasce da missione umana
o risposta esplicita LeaderAI.

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

L'agente apre quel file dalla repo ufficiale in sola lettura, legge `VERSION`,
`MANIFEST.md` e i template indicati, poi applica lo standard localmente. La
procedura predefinita non richiede clone della repo ne' esecuzione di codice
scaricato. `leaderai_setup.py` resta un attrezzo tecnico opzionale, utilizzabile
solo dopo autorizzazione esplicita.

Per un ambiente gia' installato c'e' `CHECKUP.md`: il proprietario dice al suo
agente `lancia l'Ispettore` oppure `esegui il checkup LeaderAI`; la skill
`ispettore-ecosistema` apre la fonte unica e l'agente confronta il setup con la doc
ufficiale viva (indice `code.claude.com/docs/llms.txt`, pagine `.md`), ripara
da solo il tecnico e prepara il resoconto per Sal. Lo invia solo dopo
autorizzazione esplicita del proprietario. Prima di giudicare censisce le
cartelle candidate: la cartella viva puo' chiamarsi in qualunque modo, quindi
si riconosce dai segnali di vita (memoria compilata, log, asset,
commit, file di lavoro recenti, connettori provati), non dal nome. La ricerca
non si limita a `EcosistemaAI-*` o `leaderai-cervello-ecosistema`: include
anche nomi brandizzati o sbagliati (`LeaderAI`, `Leader AI`, `leader ai`,
`leder ai`, `cervello`, `_leaderai`, `install`, `setup`, `repo`, `clone`) e
classifica ogni risultato sospetto. La fonte unica del metodo e' il
`CHECKUP.md` versionato in questa repo; nel workspace LeaderAI resta soltanto
un puntatore alla versione pubblicata.

Nel checkup di un ambiente gia' installato, l'agente usa la repo locale se gia'
presente e la aggiorna; se manca, legge GitHub come riferimento di sola lettura
per `CHECKUP.md`, `MANIFEST.md`, `templates/AGENTS.md`,
`templates/STANZA_AGENTS.md` e `templates/ISPETTORE_SKILL.md`. Crea un clone
tecnico temporaneo solo con conferma esplicita.

Nella nuova installazione, invece, parte sempre dalla lettura web della repo e
dal montaggio locale dei template. Il clone non e' un ripiego automatico.

Il modello unico dell'email di prima consegna vive in `EMAIL_CONSEGNA.md`.
`INSTALLA_CON_AI.md` contiene soltanto la procedura esecutiva: niente copie
parallele dell'email.

## Divieti

- Non salvare segreti, password, token o dati bancari.
- Mai far entrare i segreti nella cronologia git: `.secrets/`, `*.env`, token,
  chiavi e credenziali stanno nel `.gitignore`. Questo vale sempre, qualunque
  posizione abbia scelto il cliente. I connettori si ri-autorizzano con login su
  ogni PC, le chiavi non viaggiano nel backup.
- Non aprire file sospetti di contenere credenziali durante il censimento:
  controllare percorso, indice e history Git; se l'esposizione non e' esclusa,
  bloccare l'uso e proporre rotazione.
- Non hardcodare nel codice testi o regole business editabili: la fonte resta
  esterna, app e script generano derivati e falliscono visibilmente se manca.
- Firma, timbro e sigillo stanno protetti fuori Git, sono registrati per soli
  metadati in `ASSET.md` e richiedono conferma per ogni singolo uso.
- Non imporre una posizione: la cartella madre puo' stare in locale o su cloud
  secondo la scelta del cliente. Sul cloud va dato l'avviso sul rischio
  corruzione/troncamento; locale e' la via piu' sicura ma non e' l'unica.
- Non cancellare o spostare file del cliente senza conferma esplicita.
- Non creare doppioni di cartelle se ne esiste gia' una viva.
- Non sovrascrivere i file vivi del cliente. `--force` puo' riparare soltanto
  il ponte canonico `CLAUDE.md`; ogni altra modifica richiede integrazione
  esplicita e tracciata.
- Non promettere output professionali regolamentati: l'agente prepara bozze,
  il professionista verifica, decide e firma.

## Riflesso asset operativo

Ogni volta che nasce una risorsa da usare o rispettare (PEC, email, banca, auto,
gestionale, Drive, WhatsApp, fornitore, sito, repo, kit, app, archivio), il
cliente deve ritrovarla in `ecosistema/ASSET.md`.

La regola e' una: casa/fonte vera + riga asset + eventuale processo/limite
aggiornato; il log si aggiorna soltanto se cambia installazione o struttura. Se
manca la fonte reale, resta `DA COLLEGARE`; non si inventa.

## Comandi

Collaudo repo:

```bash
python3 -m tests.gate --quick
```

Collaudo completo di rilascio, su macchina con Codex e Claude autenticati:

```bash
python3 -m tests.gate --release --agents codex,claude
```

Preflight strutturale opzionale e in sola lettura:

```bash
python3 ecosistema_inspector.py --target /percorso/EcosistemaAI-Cliente
```

Collaudo diretto del modulo Portafogli:

```bash
python3 moduli/portafogli/portfolio_engine.py analizza \
  --input moduli/portafogli/DATI_PORTAFOGLIO_MODELLO.csv \
  --output /tmp/analisi-portafoglio.csv \
  --report /tmp/report-calcoli.md
```

Installazione manuale:

```bash
python3 leaderai_setup.py --target /percorso/EcosistemaAI-Cliente --client "Nome Cliente" --agent claude
```

Questo comando e' per uso tecnico verificato o per una installazione autorizzata
esplicitamente; non e' il percorso cliente predefinito.

## Quando finisci una modifica

1. Aggiorna `README.md`, `MANIFEST.md` o `INSTALLA_CON_AI.md` se cambia un fatto
   critico.
2. Esegui i test.
3. Per un rilascio esegui il gate completo: autenticazione mancante, timeout,
   test saltati o prova live fallita bloccano commit e push.
4. Commit e push su GitHub: la base cliente e' la repo ufficiale, non copie o
   fork paralleli.
5. Aggiorna l'anagrafe LeaderAI in `leaderai/memory/reference_mcp_attivi.md`.
Ogni collaudo parte da una nuova task/sessione con la cartella madre come
progetto primario/CWD. Una task aperta fuori root non vede il Cervello:
percorso corrente, `AGENTS.md` caricato e tre regole mostrate sono prove
obbligatorie. Il gate comportamentale include `Crea la Brand Identity` senza
indizi tecnici.
