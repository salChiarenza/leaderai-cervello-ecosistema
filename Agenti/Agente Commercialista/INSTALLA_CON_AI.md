# Installa l'Agente Commercialista con la tua AI

Apri questo file dalla tua cartella madre e chiedi al tuo agente:

> Installa l'Agente Commercialista nella mia casa seguendo questo file. Prima
> trova la stanza che possiede amministrazione e fiscalita'; integra i file
> esistenti, non creare doppioni. Fermati soltanto quando serve un mio accesso,
> una scelta fiscale o un'azione irreversibile.

## 1. Trova la casa vera

Leggi la mappa della cartella madre e censisci dove vivono oggi dati fiscali,
fatture, banca, documenti e stato operativo. Classifica il ruolo come
`CAPACITA`; non creare una nuova stanza se una responsabilita' amministrativa
esiste gia'. Se nessuna stanza la possiede, proponi al titolare la collocazione
prima di scrivere.

## 2. Crea una sola fonte

Nella stanza proprietaria crea `SCADENZARIO_FISCALE.md` dal calco
`SCADENZARIO_FISCALE_TEMPLATE.md`. Se esiste gia' un file fiscale vivo,
integralo e mantieni una sola fonte: non affiancare un registro parallelo.

Compila prima con prove gia' presenti nella casa. Ogni punto personale che non
ha documento, portale autenticato o ricevuta resta `DA VERIFICARE`.

## 3. Installa procedura e adattatore

Copia `PROCEDURA.md` nella cartella procedure della stanza e adatta soltanto i
puntatori ai percorsi reali.

- Codex skill: copia `SKILL.md` in
  `.agents/skills/agente-commercialista/SKILL.md`.
- Claude Code: copia `AGENTE_CLAUDE.md` in
  `.claude/agents/agente-commercialista.md`.
- Codex subagent: copia `AGENTE_CODEX.toml` in
  `.codex/agents/agente-commercialista.toml` e registralo nella configurazione
  di progetto se la versione di Codex in uso lo richiede.

Sostituisci `<STANZA_AMMINISTRATIVA>` e `<PROCEDURA_COMMERCIALISTA>` con i
percorsi reali. Non copiare dati o norme dentro gli adattatori.

## 4. Censisci la posizione reale

Controlla prima i file e le fonti gia' collegate. Poi arriva ai portali
ufficiali pertinenti; il titolare completa identita' digitale e OTP. Registra
per ogni riga fonte, data, stato e prossima azione. Non avviare iscrizioni,
pagamenti o invii durante il censimento.

## 5. Aggancia il controllo esistente

Se la casa ha gia' un Manutentore o una routine giornaliera, aggiungi li' il
controllo leggero dello scadenzario. La routine segnala soltanto una novita' o
un'azione concreta e resta silenziosa sullo stato invariato. Non creare una
seconda automazione per rappresentare lo stesso agente.

Registra il controllo con proprietario, frequenza, misura, destinazione e
arresto. Frequenza minima consigliata: giornaliera soltanto se esiste gia' una
routine; accesso ai portali protetti solo quando scade una riverifica.

## 6. Prova

Il collaudo passa quando:

1. `Lancia l'Agente Commercialista` apre fonte e procedura corrette;
2. la domanda sulle prossime scadenze distingue candidati e obblighi provati;
3. un documento viene cercato nelle fonti prima di essere chiesto al titolare;
4. una pratica chiusa contiene ricevuta, quietanza o protocollo;
5. il controllo segnala una riga urgente e tace su una riga regolare.

Annota versione, file installati e prove nel log tecnico della casa.
