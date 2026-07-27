# Changelog

## 0.3.4 - 27/07/2026

- Chat di gruppo nella casa cliente: `AGENT_CHAT.md` entra nel telaio
  (template, installazione, setup tecnico e checkup). Tutti gli agenti della
  casa si coordinano li', con regole di disciplina dentro al file.

## 0.3.3 - 27/07/2026

- L'ecosistema vive a se' nel PC: percorso standard `EcosistemaAI-[AZIENDA]`
  nel profilo utente, fuori dalle cartelle di agenti e programmi.
- Permesso di scrittura limitato alla cartella dell'agente = gesto umano:
  l'agente si fa concedere l'accesso al percorso scelto invece di ripiegare
  dentro la propria cartella (caso reale: casa creata in Documenti\Codex
  perche' la sessione scriveva solo li').

## 0.3.2 - 27/07/2026

- La cartella madre porta il nome dell'azienda e vive fuori da cartelle
  intitolate a un agente o a un programma: la casa resta valida quando cambia
  l'agente.
- L'email di consegna indica il percorso completo della cartella madre invece
  della sola scelta locale/cloud.
- L'agente rileva sulla macchina quale assistente gira davvero e lo dichiara nel
  report, invece di riceverlo scritto a distanza.

## 0.3.1 - 17/07/2026

- Il modulo Portafogli riusa anche la convenzione esistente dei casi; una
  struttura minima nuova resta una proposta da approvare.
- L'installer ripara i registri standard mancanti, registra la stanza nella
  tabella canonica della mappa madre e non crea una seconda mappa parallela.
- Puntatori Portafogli univoci vengono auto-riparati; i casi ambigui restano una
  decisione del banker.
- Installazione, checkup e modulo usano ora gli stessi stati email: report
  locale `PRONTO DA INVIARE`, invio solo dopo autorizzazione, poi
  `SAL_VERIFICA` con email archiviata.
- Il checkup accetta `CLAUDE.md` solo come ponte/import o symlink verso
  `AGENTS.md`, non come copia indipendente soggetta a drift.

## 0.3.0 - 17/07/2026

- Lo standard distingue il telaio universale dalla forma aziendale adattiva:
  prima censisce e classifica l'ambiente reale, poi collega le stanze gia' vive.
- Ogni stanza operativa deve essere raggiungibile dalla mappa madre e dichiarare
  fonti, output, capacita', collegamenti a monte e collegamenti a valle.
- Skill, script e moduli sono capacita' di una stanza; diventano una nuova stanza
  solo dopo una proposta motivata e l'approvazione del proprietario.
- Il checkup verifica ora grafo, collegamenti e prove di instradamento, oltre ai
  file tecnici e alle fonti.
- Il modulo Portafogli richiede la stanza proprietaria scelta dopo il censimento;
  non crea piu' `Costruzione Portafogli/` o una skill Claude per default.
- Ogni report registra la versione del metodo e le lezioni candidate emerse sul
  caso reale, cosi' LeaderAI puo' trasformarle in regole e test della repo.

## 0.2.0 - 16/07/2026

- Nuova installazione cliente tramite lettura della repo ufficiale e applicazione
  locale dello standard.
- Clone della repo ed esecuzione di `leaderai_setup.py` spostati nel percorso
  tecnico opzionale, attivabile solo con autorizzazione esplicita.
- Report creato e collaudato localmente prima dell'eventuale invio email.
- File statici dello standard esposti in `templates/`, cosi' l'agente del cliente
  puo' montarli senza eseguire codice scaricato.
