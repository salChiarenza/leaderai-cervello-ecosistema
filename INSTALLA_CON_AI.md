# Autoconfigurazione Git - Cervello + Ecosistema

Questo e' il testo da incollare nel Claude Code o Codex del cliente.

## Testo da copiare

```text
Voglio configurare il mio Cervello + Ecosistema LeaderAI da GitHub.

Repo da usare:
https://github.com/salChiarenza/leaderai-cervello-ecosistema

Obiettivo finale:
creare o aggiornare UNA cartella madre su OneDrive, cosi' PC ufficio e portatile
leggono le stesse istruzioni, la stessa memoria e le stesse fonti.

Cliente:
Marco De Nicolo - Private Banker / Partner Azimut

Agisci tu, senza chiedermi istruzioni tecniche. Chiedimi solo scelte umane vere
o permessi che non puoi concedere al posto mio.

Fase 1 - autodiagnosi
1. Dimmi sistema operativo, utente corrente, cartelle OneDrive trovate, presenza di Git, Python e agente attivo.
2. Cerca una cartella di lavoro gia' viva su OneDrive, soprattutto:
   - Mark investimenti
   - EcosistemaAI-Marco-De-Nicolo
   - Studio-AI
3. Se trovi "Mark investimenti" su OneDrive e sembra la cartella gia' usata per il lavoro, proponila come cartella madre. Non creare doppioni. Chiedimi conferma solo su questa scelta.
4. Se non trovi una cartella viva, crea su OneDrive:
   EcosistemaAI-Marco-De-Nicolo

Fase 2 - prepara Git e Python
1. Se Git manca ed e' installabile, installalo o guidami solo nel click/permesso necessario.
2. Se Python manca ed e' installabile, installalo o guidami solo nel click/permesso necessario.
3. Crea una cartella tecnica per il clone, NON la cartella madre finale. Per esempio:
   <OneDrive>/_leaderai_install/leaderai-cervello-ecosistema
   oppure, se OneDrive non e' ancora disponibile:
   <home>/_leaderai_install/leaderai-cervello-ecosistema

Fase 3 - clona o aggiorna la repo
1. Se la cartella tecnica contiene gia' la repo, fai aggiornamento:
   git pull
2. Se non esiste, clona:
   git clone https://github.com/salChiarenza/leaderai-cervello-ecosistema <cartella-tecnica>
3. Entra nella repo e leggi:
   - AGENTS.md
   - README.md
   - MANIFEST.md

Fase 4 - monta Cervello + Ecosistema nella cartella madre
Esegui dalla repo:

python3 leaderai_setup.py --target "<cartella-madre-OneDrive>" --client "Marco De Nicolo - Azimut" --agent both

Se il comando `python3` non esiste ma `python` o `py` si', usa quello corretto
per questo computer.

Fase 5 - personalizza il contenuto per Marco
Dopo l'installazione, apri i file creati nella cartella madre e aggiorna solo i
punti necessari, senza cancellare il resto.

In `AGENTS.md` aggiungi una sezione "Regole Marco De Nicolo":
- Marco De Nicolo, Private Banker / Partner Azimut.
- Rispondi in italiano, chiaro e operativo.
- Supporti ricerca, analisi, outlook, organizzazione fonti, bozze report e bozze portafoglio.
- Vincolo MiFID: non generi raccomandazioni finali. Ogni output e' bozza da rivedere.
- La scelta degli strumenti, la raccomandazione al cliente e la firma restano sempre a Marco/Azimut.
- Ogni numero destinato a un cliente deve essere verificato da Marco prima dell'uso.
- Non inviare email, non cancellare file, non spostare cartelle vive e non usare dati sensibili senza conferma esplicita.

In `memory/MEMORY.md` aggiungi i puntatori:
- `AGENTS.md` - regole operative e vincolo MiFID.
- `ecosistema/FONTI.md` - fonti autorizzate e cartelle reali.
- `ecosistema/PROCESSI.md` - lavori ricorrenti: report cliente, outlook, scheda portafoglio.
- `ecosistema/LIMITI.md` - azioni vietate o da confermare.

In `ecosistema/FONTI.md` registra quello che esiste davvero:
- cartella madre OneDrive usata;
- cartella/report clienti disponibili;
- catalogo fondi Azimut o fondi collocabili, solo se Marco indica il file reale;
- eventuali output gia' prodotti in Claude/Codex.
Non inventare percorsi: se una fonte non e' presente, scrivi "da collegare".

In `ecosistema/PROCESSI.md` aggiungi questi processi candidati:
- Scheda cliente per proposta di riallocazione: input profilo/rischio/vincoli, output bozza da rivedere.
- Report cliente: input rendicontazione o report nativo, output commento cliente.
- Outlook o approfondimento quotata/fondo: input fonti autorizzate, output bozza narrativa.

In `ecosistema/LIMITI.md` aggiungi:
- Nessuna raccomandazione finale automatica.
- Nessun invio al cliente senza Marco.
- Nessun uso di file cliente non autorizzati.
- Nessuna modifica/cancellazione di dati originali.

Fase 6 - collaudo
1. Verifica che nella cartella madre esistano:
   AGENTS.md, CLAUDE.md, memory/MEMORY.md, ecosistema/FONTI.md,
   ecosistema/PROCESSI.md, ecosistema/LIMITI.md, logs/install-log.md,
   REPORT_FINALE.md.
2. Leggi `AGENTS.md` e dimmi in 5 righe:
   - chi sono;
   - dove sta la cartella madre;
   - quali fonti vedi;
   - cosa puoi fare;
   - cosa NON puoi fare.
3. Prepara una prova piccola, senza dati sensibili:
   "crea una scheda cliente vuota per proposta di riallocazione, con campi da compilare e disclaimer bozza da rivedere".
4. Se qualcosa non passa, correggi e riprova.

Report finale obbligatorio:
- cartella madre scelta;
- repo clonata/aggiornata si/no;
- file creati;
- OneDrive verificato si/no;
- prova scheda cliente completata si/no;
- cosa resta da collegare;
- verdetto: PASSA / PASSA CON ATTENZIONE / NON PASSA.
```
