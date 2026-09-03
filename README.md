# LeaderAI Cervello + Ecosistema

Repo operativa per montare un ambiente AI cliente secondo lo standard LeaderAI.

E' una repo operativa: installa quando manca tutto, fa checkup e riparazione
quando l'ambiente esiste gia', aggiorna le fonti della casa e chiude con una
conferma unica.

## Fonti ufficiali vive del checkup

- [Claude Code - panoramica ufficiale](https://code.claude.com/docs/en/overview)
- [Claude Code - hook ufficiali](https://code.claude.com/docs/en/hooks)
- [ChatGPT - documentazione ufficiale](https://learn.chatgpt.com/docs)
- [Codex - hook ufficiali](https://learn.chatgpt.com/docs/hooks)
- [OpenAI Academy - Codex per il lavoro](https://openai.com/it-IT/academy/codex-for-work/)

L'Ispettore apre queste fonti a ogni checkup e collega le regole pertinenti
allo stato osservato, alle riparazioni e alle prove. Le pagine tecniche
stabiliscono la conformita'; `Codex per il lavoro` orienta la pratica operativa
e non sostituisce le specifiche tecniche.

Regola madre: questa repo e' lo standard, la cartella viva del cliente e' il
caso reale. `CHECKUP.md` confronta il caso reale con `MANIFEST.md`,
`templates/AGENTS.md`, `templates/STANZA_AGENTS.md` e
`templates/STANZA_FONTE.md` e `templates/ecosystem-check/`, ripara gli scostamenti
riparabili, prova, salva i fatti nelle fonti proprietarie e chiude localmente.
Il ciclo ordinario produce zero aggiornamenti intermedi. Quando la missione
richiede una conferma finale, ne parte una sola dopo il collaudo completo.

`install_contract.json` e' il contratto macchina unico del nucleo
d'installazione: procedura manuale, setup tecnico, Ispettore e collaudo leggono
la stessa lista di file obbligatori e rami agente. Browser, launcher e backup
remoto sono controlli della macchina cliente dichiarati nello stesso contratto
e restano `DA COLLAUDARE` nel gate anonimo.

La repo fornisce un telaio minimo, la stanza standard `Ecosystem Check` e un
metodo adattivo. Il telaio rende stabile il Cervello; Ecosystem Check governa
controlli, interventi e storico; il metodo censisce il lavoro reale, riconosce
le stanze business gia' vive e le collega alla mappa madre. La cartella madre e ogni vera stanza hanno sempre
`AGENTS.md` come fonte unica e `CLAUDE.md` come ponte `@AGENTS.md`. I nomi
delle stanze appartengono al cliente, non al template.

## Uso rapido

Per installare tramite l'agente del cliente, usare:

```text
INSTALLA_CON_AI.md
```

Il testo della prima email di consegna vive soltanto in `EMAIL_CONSEGNA.md`.
La procedura non ne mantiene una seconda copia.

L'agente legge questa repo ufficiale in sola lettura, trova o crea la cartella
madre nella posizione scelta col cliente e applica localmente i template dello
standard. Il percorso cliente predefinito non clona la repo e non esegue codice
scaricato.

Per il controllo periodico di un ambiente gia' installato:

```text
CHECKUP.md
```

Il proprietario dice al suo agente `lancia l'Ispettore` oppure
`esegui il checkup LeaderAI`: la skill `ispettore-ecosistema` apre la fonte
unica `CHECKUP.md` e l'agente confronta il setup con la documentazione
ufficiale viva (indice
`code.claude.com/docs/llms.txt`, pagine `.md`), ripara da solo il tecnico e
prepara la conferma finale per Sal quando la missione la richiede. La invia
soltanto dopo autorizzazione esplicita del proprietario. Prima di giudicare
censisce le cartelle candidate:
la cartella viva puo' chiamarsi in qualunque modo, quindi si riconosce dai
segnali di vita (memoria compilata, log, asset, commit, file di lavoro
recenti, connettori provati), non dal nome. La ricerca include anche nomi
brandizzati o sbagliati come `LeaderAI`, `Leader AI`, `leader ai`, `leder ai`,
`cervello`, `ecosistema`, `_leaderai`, `install`, `setup`, `repo` e `clone`.

Ogni missione segue un ciclo locale: `MISSIONE` -> `ESECUZIONE` ->
`AUTOCONTROLLO` -> `SALVATAGGIO NELLA CASA` -> `CHIUSURA LOCALE`.
L'email della missione e' l'unico messaggio del ciclo ordinario. L'agente crea
e prova tutto nella casa del cliente, promuove stato e prove nelle fonti
proprietarie, archivia l'email e chiude le
superfici aperte. Il ciclo produce zero aggiornamenti intermedi; decisioni e
gesti umani veri restano come `DA DECIDERE IN CALL`.
L'unica interruzione ammessa arriva quando serve un gesto che puo' compiere il
proprietario. Il messaggio visibile apre con `SERVE UN TUO PASSAGGIO`, indica
cosa l'agente ha gia' sistemato e chiede un solo gesto. Dopo la risposta
riprende la stessa missione; le classificazioni tecniche restano nella casa.
Quando Sal richiede espressamente una conferma finale, parte una volta sola
quando tutti i criteri sono completati e provati: apre con `Perfetto, l'ho
fatto. Tutto completato e
funzionante.` e riporta le prove essenziali di tutti i criteri della missione.
Le email operative tra agenti aprono sempre con `SITUAZIONE IN BREVE`: cosa
funziona, cosa completiamo, cosa serve da te e quando si chiude. I dettagli
tecnici restano nelle fonti della casa.

Dove mettere la cartella madre si decide caso per caso con domande guidate
(disco locale oppure cartella sincronizzata OneDrive / Google Drive). Avviso da
dire chiaro: Claude Code, mentre scrive, puo' corrompere o troncare i file su
cartelle cloud con file on-demand (bug noti); il cliente sceglie se accettare il
rischio in cambio della comodita'. Il backup si sceglie sempre col cliente
(GitHub privato a comando oppure copia su Drive/OneDrive). I segreti restano
sempre fuori dal git (`.gitignore`). Dettaglio in `INSTALLA_CON_AI.md`
Domande 1, 2, 3 e Fase 7.

Uso tecnico opzionale, dopo autorizzazione esplicita:

```bash
python3 leaderai_setup.py --target /percorso/EcosistemaAI-Cliente --client "Nome Cliente" --agent claude
```

Valori per `--agent`:

- `claude` crea soltanto la configurazione `.claude/`
- `codex` crea soltanto la configurazione `.codex/`
- `both` crea entrambe le configurazioni, solo su richiesta esplicita LeaderAI

In tutti e tre i casi il telaio comune resta identico: `AGENTS.md` +
`CLAUDE.md`. La modalita' seleziona le configurazioni dell'agente, non i file
del contratto comune. Un cambio tra Codex e Claude viene fermato: si usa
`--agent both` per mantenere entrambi oppure `--migrate-agent` per una
migrazione esplicita e conservativa. Per Claude, il setup preserva le altre
user settings e blocca il lavoro se `autoMemoryDirectory` punta gia' a una
seconda casa.

## Cosa crea

Nel target scelto crea solo i pezzi standard mancanti:

- `.gitignore` che esclude `.secrets/`, `*.env`, token, chiavi e credenziali
- inizializza la cartella madre come repository git (se non lo e' gia')
- `AGENTS.md` come mappa comune del Cervello
- `CLAUDE.md` come ponte permanente di una riga (`@AGENTS.md`)
- `.codex/README.md` se richiesto Codex
- `.codex/hooks.json` con il controllo finale, unito alle impostazioni esistenti
- `.claude/README.md` se richiesto Claude Code
- `.claude/settings.json` con lo stesso controllo finale, senza sovrascritture
- user settings Claude Code (`~/.claude/settings.json`) con
  `autoMemoryDirectory` sulla memoria canonica della casa, verificate su ogni PC
- istruzioni globali dell'agente attivo su ogni PC (`~/.claude/CLAUDE.md` o
  `~/.codex/AGENTS.md`) con il blocco `LEADERAI-CASA`: nominano la cartella
  madre e fanno rispondere `FUORI DAL CERVELLO` a una sessione nata altrove
- `.agents/skills/ispettore-ecosistema/SKILL.md` se richiesto Codex
- `.agents/skills/manutentore-ecosistema/SKILL.md` se richiesto Codex
- `.claude/skills/ispettore-ecosistema/SKILL.md` se richiesto Claude Code
- `.claude/skills/manutentore-ecosistema/SKILL.md` se richiesto Claude Code
- `.agent/hooks/guardiano_stanze.sh` e adattatore Windows: prima della chiusura
  intercettano file fuori posto, cartelle incomplete, copie e mappe gonfie
- `memory/MEMORY.md`
- `AGENT_CHAT.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `ecosistema/SOGGETTI.md` anagrafe dei soggetti giuridici: piu' soggetti, una casa
- riga `Fase del percorso: N` nella mappa madre: sotto il passo 3 il guardiano
  blocca ogni stanza di lavoro, la fase sale solo con la missione che chiude il passo
- `ecosistema/STANZA_AGENTS.md` come calco locale per le nuove stanze
- `ecosistema/STANZA_FONTE.md` come calco della loro fonte operativa

Questi pezzi sono l'armadio comune: `ecosistema/` non ospita cartelle o
materiali business diversi dai registri e calchi dichiarati. Le cartelle
business vivono accanto a esso e vengono prima
classificate come stanza, fonte, output, capacita', infrastruttura, archivio o
elemento sospetto. Ogni vera stanza deve essere raggiungibile dalla radice e
avere `AGENTS.md` + `CLAUDE.md`, con mappa corta, fonti, output e collegamenti
reali.

La struttura e' un organigramma: l'agente nella cartella madre e' il **Boss
dell'Ecosistema**; ogni ramo organizzativo, nuovo o gia' esistente, e' affidato
a un **Amministratore di settore** che governa quella stanza e riporta al Boss.
Le normali sottocartelle restano strumenti del settore e non diventano falsi
rami.

Ogni nuova stanza nasce nello stesso salvataggio con mappa, ponte, fonte
operativa, riga alla radice e prova, usando i due calchi installati. Prima del
salvataggio l'Ispettore controlla anche campi incompleti e sottocartelle dirette
non dichiarate, oltre a percorsi senza classe o proprietario.

Controlla anche la salute dei Markdown: misura tutti i file, blocca mappe e
indici cresciuti oltre le soglie del contratto macchina e revisiona i documenti
estesi per scoprire responsabilita' mescolate o fonti duplicate. Alleggerisce i
router portando i dettagli nelle fonti proprietarie e lasciando collegamenti,
senza tagliare contenuti alla cieca. Ogni nuovo problema ripetibile entra in
`ecosistema/PROCESSI.md` come lezione candidata e, dopo la validazione
LeaderAI, diventa regola e test dei checkup successivi.

`ecosistema/ASSET.md` include anche la **mappa moduli**: PEC/email certificata,
email/calendario, calendario operativo, Drive/OneDrive, CRM/gestionale, plugin,
skill, agenti, guardiani/hook, ronde, voce/dettatura e compliance/privacy/AI
Act. Ogni modulo deve avere uno stato, cosi' il prossimo passo non dipende
dalla memoria di chi segue la consegna.

Modulo specifico gia' disponibile:

- `MODULO_CALENDARIO_OPERATIVO.md` - quando il cliente usa Calendar a colori e
  serve trasformare quella lettura visiva in struttura leggibile dall'agente.
- `moduli/portafogli/` - Sistema Portafogli Core-Satellite: fonti autorizzate,
  verifica automatica di numeri, identita', stato e collocabilita' degli
  strumenti, metodo del banker, calcoli deterministici, backtest, monitoraggio
  e report.
  L'agente del cliente parte da `moduli/portafogli/INSTALLA_MODULO.md`, sceglie
  la cartella madre o la stanza proprietaria e integra il modulo senza creare
  una stanza concorrente.

Il Cervello include anche la **mappa comunicazione**: stato business nel file
proprietario della stanza, storia tecnica nel solo `logs/install-log.md`, asset
in `ecosistema/ASSET.md`, chat solo per coordinamento temporaneo e sync dedicato
solo se il cliente usa sia Claude sia Codex.

L'Ispettore confronta sempre la versione installata con il `VERSION` vivo,
verifica che Claude usi una sola memoria, individua configurazioni credenziali
fuori `.secrets/` senza aprirle, controlla firma/timbro e impedisce copie
hardcoded di contenuti business modificabili. Quando una memoria viene fusa,
controlla anche che nessun wikilink resti puntato a una voce sostituita.

Controlla anche se istruzioni, skill, rule o hook stanno stringendo troppo
l'agente. Il confronto cambia un solo blocco per volta e usa due sessioni
nuove sulla stessa missione: contesto completo contro alleggerito. Il rapporto
misura risultato, fonti, percorso, completamento, intervento umano, tempo,
consumo quando disponibile e sicurezza; propone soltanto una classificazione,
senza modifiche distruttive automatiche. La missione non contiene indizi su
cartella, fonte o risultato atteso; un solo caso non puo' candidare la rimozione
di una istruzione.

Quando la richiesta riguarda soltanto istruzioni, capacita' o passaggi
manuali, l'Ispettore usa il controllo focalizzato: verifica questi punti senza
imporre il telaio cliente, creare stanze o emettere il verdetto complessivo
della casa. Un primo tentativo fallito non prova un limite tecnico.

I file vivi del cliente restano intatti. `--force` serve soltanto a riparare il
ponte canonico `CLAUDE.md` quando e' mancante o errato.

La versione corrente dello standard e' in `VERSION`; le modifiche consegnabili
sono registrate in `CHANGELOG.md`.

## Collaudo

Gate deterministico obbligatorio:

```bash
python3 -m tests.gate --quick
```

Gate completo di rilascio, su macchina con entrambi gli agenti autenticati:

```bash
python3 -m tests.gate --release --agents codex,claude
```

Il gate completo avvia sessioni nuove reali. Prova due richieste business senza
percorsi suggeriti e ripete l'installazione manuale partendo dalla sola
procedura. Conserva prompt, trascrizioni, manifest prima/dopo, diff e verdetti.
Zero test, test saltati, CLI assente, autenticazione mancante, timeout o
oracolo fallito bloccano il rilascio.

Confronto mirato di un blocco di istruzioni, su fixture anonima e due sessioni
pulite:

```bash
python3 behavior_harness.py compare-context --help
```

Preflight strutturale opzionale e in sola lettura, quando la repo e' locale e
l'esecuzione e' stata autorizzata:

```bash
python3 ecosistema_inspector.py --target /percorso/EcosistemaAI-Cliente
```

## Stato

Versione applicabile via lettura della repo ufficiale. Prima di usarla con un
cliente, leggere `AGENTS.md` e `INSTALLA_CON_AI.md`, scegliere la modalita'
Claude/Codex e verificare `VERSION` e stato GitHub.
La cartella madre deve essere anche il punto di ingresso reale dell'agente:
progetto locale primario in Codex Desktop, `-C`/directory corrente in Codex
CLI, directory corrente in Claude Code. Dopo un cambio di cartella si apre una
nuova task/sessione e si prova `AGENTS.md` prima del lavoro.
