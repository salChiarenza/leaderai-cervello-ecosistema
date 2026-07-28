# Memory - {{client_name}}

Indice della memoria condivisa del Cervello.

## Regole

- Una riga per ogni memoria stabile.
- Ogni riga deve puntare a un file reale o a una sezione reale.
- Non usare questa memoria per segreti, password, token o dati bancari.
- Non duplicare lo stato operativo: lo stato business vive nel file
  proprietario della stanza; il log e' solo tecnico e il report e' temporaneo.
- Per Claude Code questa stessa cartella deve essere anche la destinazione di
  auto memory tramite `autoMemoryDirectory`; due directory di memoria attive
  sono un blocco da riconciliare.

## Indice

- `AGENTS.md` - mappa iniziale del Cervello e dell'Ecosistema.
- `logs/install-log.md` - versione applicata e soli cambi
  tecnici/strutturali.
- `ecosistema/FONTI.md` - dove vivono le fonti vere del cliente.
- `ecosistema/ASSET.md` - capacita' e asset collegati alle stanze che servono.
- `ecosistema/PROCESSI.md` - processi osservati o candidati.
- `ecosistema/LIMITI.md` - azioni che richiedono conferma umana.
