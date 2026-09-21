# Cervello di {{client_name}}

Questa e' la cartella di lavoro principale di {{client_name}}.

- Versione LeaderAI: `{{version}}`
- Creata il: `{{date}}`
- Stato: vedi `logs/install-state.json`; soltanto `COMPLETED` chiude il Passo 1

## Contenuto

- `memory/MEMORY.md`: conoscenza stabile confermata.
- `AGENT_CHAT.md`: passaggi di consegna tra assistenti.
- `ecosistema/FONTI.md`: dove si trovano i dati reali.
- `ecosistema/ASSET.md`: strumenti e risorse disponibili.
- `ecosistema/PROCESSI.md`: lavori ricorrenti osservati.
- `ecosistema/LIMITI.md`: confini e cautele.
- `ecosistema/SOGGETTI.md`: persone e organizzazioni coinvolte.
- `logs/install-log.md`: prova dell'installazione.

I documenti iniziano vuoti: i fatti entrano soltanto quando vengono confermati
dal proprietario o verificati nella loro fonte.

## Installazione e aggiornamento

Il pacchetto scaricato e' il riferimento, non va copiato sopra questa cartella.
Il nome del proprietario e della sua attivita' l'assistente li ricava da solo
(utente del computer, documenti presenti, cose gia' dette); se non li trova usa
il nome dell'utente del computer e lo segna `DA CONFERMARE`. Il pacchetto
estratto e lo zip non restano nella casa: si cancellano alla fine.

L'assistente legge `install_contract.json`, poi lavora nella cartella viva:

1. apre `logs/install-state.json`; se un lavoro era rimasto a meta', riparte dal
   primo elemento non completato;
2. conserva ogni file gia' compilato dal proprietario;
3. crea soltanto i file mancanti dichiarati nel contratto;
4. aggiorna soltanto i blocchi delimitati `leaderai:...:inizio/fine`;
5. controlla che tutti i file richiesti esistano;
6. soltanto alla fine scrive `VERSION` con il valore di `PACKAGE_VERSION` e
   porta lo stato a `COMPLETED`.

Se la sessione viene chiusa, una sessione nuova legge lo stato e continua:
non ricomincia e non crea una seconda casa.
