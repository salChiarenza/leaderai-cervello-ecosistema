# Installa l'Ispettore del Bando con Claude

Apri questa cartella dal catalogo LeaderAI e chiedi a Claude Code:

> Installa l'Ispettore del Bando nella mia casa AI seguendo questo file. Trova
> prima la cartella viva che possiede bandi e pratiche. Integra la capacita li,
> senza creare stanze o registri doppi. Poi prova il richiamo su una pratica
> reale senza firmare, pagare o inviare nulla.

## 1. Trova casa e processo reali

Leggi la mappa della cartella madre e individua dove vivono oggi stato,
documenti e procedure dei bandi. Classifica l'Ispettore come `CAPACITA`. Se
esiste gia una gestione bandi, integralo li; se non esiste una responsabilita
proprietaria, chiedi al titolare dove collocarla prima di creare una stanza.

## 2. Installa la skill completa

Copia questa cartella in:

`.claude/skills/ispettore-del-bando/`

Mantieni insieme `SKILL.md`, `PROCEDURA.md`, `assets/` e `scripts/`. Copia
`AGENTE_CLAUDE.md` in `.claude/agents/ispettore-del-bando.md` solo se la casa
usa gia agenti specializzati richiamabili; altrimenti la skill e sufficiente.

Non sostituire percorsi esistenti con quelli del computer di LeaderAI. Non
copiarti credenziali, token o documenti della pratica dentro la skill.

## 3. Collega la capacita

Nella mappa o nell'anagrafe asset della casa registra:

- attivazione: `Lancia l'Ispettore del Bando`;
- fonte: cartella viva della singola pratica e fonti ufficiali correnti;
- risultato: `REPORT_ISPETTORE_BANDO.md` e `RICEVUTA_ISPETTORE_BANDO.json`;
- controllo: completezza, coerenza, integrita e quadratura;
- arresto: accesso/2FA, firma, dichiarazione, pagamento e invio finale.

Non creare una routine ricorrente: l'Ispettore parte a chiamata o quando cambia
una pratica reale.

## 4. Prova senza azioni esterne

Il collaudo passa quando:

1. `Lancia l'Ispettore del Bando` apre la pratica viva e le fonti ufficiali;
2. un documento solo dichiarato presente non diventa `PROVATO`;
3. una quadratura incompleta produce `BLOCCATO`;
4. una risposta scritta esterna mancante produce `IN ATTESA`;
5. firma e invio restano al titolare;
6. il report usa soltanto `PRONTO`, `BLOCCATO` o `IN ATTESA`;
7. nessuna pagina operativa o processo aperto per la prova resta in esecuzione.

Annota nella fonte tecnica della casa versione, posizione installata e prove.

