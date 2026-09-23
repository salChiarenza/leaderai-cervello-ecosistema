<!-- vista: inizio (generata, non correggere a mano) -->

# LeaderAI Cervello + Ecosistema 0.7.17

Costruisce un ambiente AI di lavoro in cinque passi. Il Passo 1 consegna soltanto la base documentale; stanze, controlli e capacita' nascono dopo dal lavoro vero. Funziona con Claude Code e con ChatGPT Work.

Dentro ci sono 3 stanze, 3 agenti, 2 skill, 13 guardiani, 4 memorie, 50 modelli, 39 prove nella sorgente completa. Alla persona arrivano in 5 passi, uno per volta; non sono tutti nel Passo 1.

| Nella sorgente | Quanti | Quando serve |
|---|---|---|
| Stanze | 3 | dove vive ogni cosa (le altre nascono dal lavoro del cliente) |
| Agenti | 3 | prodotti opzionali successivi |
| Skill | 2 | capacita' opzionali successive |
| Guardiani | 13 | controlli valutati nel Passo 4 |
| Memorie | 4 | la conoscenza che resta (modelli vuoti da riempire) |
| Modelli | 50 | il calco di ogni pezzo |
| Prove | 39 | si controlla da solo |

## Come si installa

| Fase | Cosa monta | Finito quando |
|---|---|---|
| 1. Cervello | nasce una sola cartella madre con il telaio documentale minimo: memoria, chat, fonti, asset, processi,… | Cervello.zip non contiene file eseguibili ne' cartelle di configurazione dell'agente; install_contract.json… |
| 2. Mappa del lavoro | l'agente intervista e registra, non crea: soggetti giuridici in ecosistema/SOGGETTI.md, fonti vere in… | ogni riga dei registri porta un dato vero (nome del soggetto, percorso o accesso della fonte, esempio del… |
| 3. Prima stanza col primo processo | la casa del cliente si costruisce come la casa di Sal, che e' l'unico modello vivo: le stanze seguono chi… | una richiesta reale fatta all'agente senza suggerimenti, che nomina il soggetto e il lavoro, fa partire la… |
| 4. Gestione dell'ecosistema | su una casa gia' usata e compresa si valutano Controllo della casa, Manutenzione e guardiani. | il Manutentore ha girato una volta da solo e ha scritto la sua misura; l'Ispettore parte da solo alla sua… |
| 5. Collaudo e consegna | controllo completo della casa contro lo standard (versione, telaio, stanze, strade, istruzioni), riparazioni… | verdetto PASSA pieno, approvazione di Sal e conferma finale al modo previsto; da qui in poi il cliente decide… |

## Libreria sorgente completa

```text
Cervello + Ecosistema/
|-- Agenti/                                            # 3 prodotti opzionali per i passi successivi
|-- Skill/                                             # 2 capacita' opzionali per i passi successivi
|-- moduli/                                            # pezzi che si montano solo quando servono
|-- templates/                                         # 50 modelli: il calco di mappa, stanza, fonte, controlli
|-- tests/                                             # 39 prove che il prodotto gira prima di uscire
|-- 01 - Cervello - installazione e aggiornamento.md   # l'unico file da cui parte il cliente
|-- CHECKUP.md                                         # diagnosi e riparazione di una casa già viva
|-- MANIFEST.md                                        # lo standard con cui si confronta il caso reale
|-- install_contract.json                              # la lista che leggono installazione, Ispettore e collaudo
```

> Blocco generato il 21/09/2026 dalle cartelle del prodotto con
> `leaderai-ecosistema/tools/mappa_sistema.py`. Si rigenera, non si corregge a mano.

<!-- vista: fine -->

Copia di lavoro del prodotto che monta un ambiente AI cliente secondo lo
standard LeaderAI. La versione corrente vive nell'Ecosistema per i clienti su Google
Drive; GitHub conserva soltanto il backup successivo alla prova Drive.

E' una repo operativa: installa quando manca tutto, fa checkup e riparazione
quando l'ambiente esiste gia', aggiorna le fonti della casa e chiude con una
conferma unica.

Le fasi successive restano visibili nel percorso. La prima usa un solo file,
`01 - Cervello - installazione e aggiornamento.md`, che monta o aggiorna
soltanto la base documentale dichiarata da `install_contract.json`. Stanze,
controlli e capacita' arrivano nei passi successivi, dal lavoro reale e con una
scelta separata: ogni casa conserva contenuto su misura. Il percorso guidato
termina con `5 Collaudo e consegna`; eventuali nuovi prodotti o processi si
aggiungono dopo, soltanto quando servono.

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

Regola madre: l'Ecosistema per i clienti su Drive e' lo standard corrente, la cartella
viva del cliente e' il caso reale. `CHECKUP.md` confronta il caso reale con `MANIFEST.md`,
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

Per installare o aggiornare tramite l'agente del cliente, il file visibile e':

```text
01 - Cervello - installazione e aggiornamento.md
```

La fonte tecnica del documento e' `01 - Cervello - installazione e aggiornamento.md`. Il testo della prima
email vive in `EMAIL_CONSEGNA.md` ed e' soltanto un invito breve con il link;
non contiene una seconda copia della procedura.

L'agente legge l'Ecosistema per i clienti in sola lettura, trova o crea la cartella
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
segnali di vita (memoria compilata, log, asset, copie di sicurezza, file di lavoro
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
rischio in cambio della comodita'. La casa non e' un registro git: il backup e'
la copia di sicurezza datata in una cartella scelta col cliente
(`.agent/hooks/backup_casa.py`, routine delle 07:45). I segreti restano in
`.secrets/`, fuori dalla copia. Dettaglio in `01 - Cervello - installazione e aggiornamento.md`
Domande 1, 2, 3 e Operazione 7.

Uso tecnico opzionale, dopo autorizzazione esplicita:

```bash
python3 leaderai_setup.py --target /percorso/LeaderAI-Cliente --client "Nome Cliente" --agent claude
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

- `.agent/hooks/backup_casa.py`, la copia di sicurezza datata (nessun registro git)
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
- `.agents/skills/censitore-processi/SKILL.md` se richiesto Codex
- `.claude/skills/ispettore-ecosistema/SKILL.md` se richiesto Claude Code
- `.claude/skills/manutentore-ecosistema/SKILL.md` se richiesto Claude Code
- `.claude/skills/censitore-processi/SKILL.md` se richiesto Claude Code
- `.agent/hooks/guardiano_stanze.sh` e adattatore Windows: prima della chiusura
  intercettano file fuori posto, cartelle incomplete, copie e mappe gonfie
- `.agent/hooks/archive_policy.py`: parser condiviso degli archivi protetti e
  misura strutturale in una camminata; dettagli in `MANIFEST.md`, sezione
  «Archivi di fascicoli e fonti Word»
- `memory/MEMORY.md`
- `AGENT_CHAT.md`
- `logs/install-log.md`
- `ecosistema/FONTI.md`
- `ecosistema/ASSET.md`
- `ecosistema/PROCESSI.md`
- `ecosistema/LIMITI.md`
- `ecosistema/SOGGETTI.md` anagrafe dei soggetti giuridici: piu' soggetti, una casa
- riga `Fase del percorso: N` nella mappa madre: dice a che punto sei del
  percorso e non impedisce di creare stanze, che si giudicano dalla loro forma
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

Skill opzionali nel catalogo `LeaderAI Ecosystem/Ecosistema per i clienti/Prodotti/Skill`
(sorgente `Skill/`, una cartella per skill con il suo `SKILL.md`): l'agente copia la
cartella scelta in `.claude/skills/` o `.agents/skills/` della casa. Prima skill:
`mente-da-principiante`.

Prodotti-agente opzionali gia' disponibili nel catalogo
`LeaderAI Ecosystem/Ecosistema per i clienti/Prodotti`:

- `Agente Commercialista` - installazione guidata, fonte fiscale
  unica, procedura e adattatori per Claude Code e Codex. Si integra nella
  stanza amministrativa emersa dal lavoro reale; non contiene dati personali
  e non sostituisce il professionista abilitato. Non fa parte della release
  dell'Ecosistema; la cartella tecnica locale resta soltanto l'officina.
- `Ispettore del Bando` - installazione Claude guidata, matrice unica della
  pratica, indice analitico delle coppie fattura-pagamento, verifica di prove e
  firme, report e ricevuta. Il titolare conserva accessi e azioni irreversibili;
  il pacchetto non contiene fascicoli o dati cliente.

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
python3 ecosistema_inspector.py --target /percorso/LeaderAI-Cliente
```

## Stato

Versione applicabile via lettura dell'Ecosistema per i clienti. Prima di usarla con un
cliente, leggere `AGENTS.md` e `01 - Cervello - installazione e aggiornamento.md`, scegliere la modalita'
Claude/Codex e verificare `VERSION` direttamente su Drive.
La cartella madre deve essere anche il punto di ingresso reale dell'agente:
progetto locale primario in Codex Desktop, `-C`/directory corrente in Codex
CLI, directory corrente in Claude Code. Dopo un cambio di cartella si apre una
nuova task/sessione e si prova `AGENTS.md` prima del lavoro.

## Layout (0.7.1, 16/09/2026)

Una riga per pezzo: cosa e' e a cosa serve. Si aggiorna a ogni versione.

### 1. La casa del cliente al Passo 1

```
LeaderAI-<Cliente>/               Passo 1 (0.7.1): solo documenti, nessuno script, nessun gancio, niente git
├─ README.md                     come e' fatta la casa e da dove viene (letto per primo)
├─ AGENTS.md                     la mappa madre: chi c'e', dove stanno le cose, come si lavora
├─ CLAUDE.md                     il ponte di una riga (@AGENTS.md): l'assistente legge la mappa
├─ AGENT_CHAT.md                 la chat di gruppo degli agenti (note al massimo 48 ore)
├─ memory/MEMORY.md              la memoria unica, con indice
├─ ecosistema/                   l'armadio comune: le anagrafi, non una stanza
│  ├─ SOGGETTI.md                i soggetti (aziende, studi, enti)
│  ├─ FONTI.md                   dove stanno i dati veri (cartelle, email, gestionali)
│  ├─ ASSET.md                   strumenti e risorse, con stato e limiti
│  ├─ PROCESSI.md                i lavori ricorrenti (dal censimento, Passo 2)
│  ├─ LIMITI.md                  cosa l'assistente non deve fare
│  └─ STANZA_AGENTS.md, STANZA_FONTE.md   i calchi per far nascere una stanza completa
├─ <una stanza per processo>/    dal Passo 3: AGENTS.md + CLAUDE.md + la sua fonte, agganciata alla mappa madre
├─ .secrets/                     credenziali: fuori da tutto, anche dalla copia di sicurezza
└─ logs/install-log.md           cosa e' stato installato, quando, con quale versione
```

### 2. Passo 4, con scelta della persona

```
Passo 4, con una scelta visibile della persona: i controlli che scattano da soli
├─ assistenza/                   lo sportello: si entra col guasto in mano
│  ├─ SINTOMI.md                 dal sintomo alla carta giusta (la legge il guardiano delle carte)
│  ├─ MANUALI.md                 le guide ufficiali degli strumenti (la legge il guardiano dei manuali)
│  └─ CONTATTO.md                l'assistenza LeaderAI, quando hai provato e sei ancora fermo
├─ ecosystem-check/              la stanza che controlla la casa
│  ├─ AGENTS.md, STATO.md        mappa e stato dei controlli
│  ├─ CONTROLLI.md               registro: ogni cosa nasce col suo controllo
│  ├─ REGISTRO_CONTROLLI.md      esiti dei giri di controllo
│  ├─ STANDARD_REPARTO.md        lo standard di una stanza
│  └─ ruoli/                     orchestratore, struttura, istruzioni, continuita', chiusura, intervento
├─ .agent/hooks/                 i guardiani che arrivano col Passo 4
│  ├─ guardiano_stanze.sh (+ .ps1)   a fine turno: casa in ordine, niente file fuori posto
│  ├─ archive_policy.py          archivi protetti: dichiarati, fuori da copie e misure
│  └─ backup_casa.py             la copia di sicurezza datata (routine 07:45, ultime sette)
├─ .claude/                      settings.json (ganci) + skills/: Ispettore, Manutentore, Censitore, Impara dagli errori
├─ .codex/ e .agents/skills/     lo stesso per chi usa ChatGPT Work / Codex
└─ routine manutenzione-ecosistema   ogni giorno alle 07:45, dalla cartella madre: riordino + copia di sicurezza
```

### 3. Il prodotto

```
leaderai-cervello-ecosistema/     il prodotto (Drive = copia per i clienti, GitHub = solo backup)
├─ PASSO1_CLIENTE.md             la guida breve del Passo 1: scarica, apri, personalizza, verifica (0.7.1)
├─ 01 - Cervello - installazione e aggiornamento.md   la guida completa: installazione e aggiornamento (in riallineamento)
├─ CHECKUP.md                    l'Ispettore: censisce, ripara e prova una casa gia' esistente
├─ MANIFEST.md                   lo standard: cosa deve esserci e come si misura
├─ EMAIL_CONSEGNA.md             la prima email al cliente: un link e basta
├─ MODULO_CALENDARIO_OPERATIVO.md   modulo: il calendario operativo
├─ README.md · CHANGELOG.md · VERSION   presentazione, storia delle versioni, versione corrente
├─ install_contract.json         il contratto macchina: file, ganci, controlli, soglie (una fonte sola)
├─ templates/                    i calchi che diventano la casa (passo1/ = i nove documenti del Passo 1)
├─ Skill/ · Agenti/ · moduli/    catalogo: mente-da-principiante; Agente Commercialista, Ispettore del Bando; portafogli
├─ leaderai_setup.py             installatore tecnico: solo per il collaudo LeaderAI, mai per il cliente
├─ ecosistema_inspector.py       il motore dell'Ispettore
├─ installation_harness.py · behavior_harness.py   collaudi vivi con i motori veri (Claude Code e Codex)
├─ census_collector.py · census_rule.py · adoption_rule.py   regole macchina: censimento processi, adozione osservata
└─ tests/                        31 file: ogni regola ha la sua prova
```
