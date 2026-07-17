# Asset operativi

Registro unico delle risorse operative del cliente.

Un asset e' qualunque cosa che l'agente deve sapere trovare, usare o rispettare:
email/PEC, banca, auto, fornitore, gestionale, Drive, WhatsApp, sito, repo,
kit, app, servizio esterno, archivio o canale ufficiale.

## Registro

| Asset | Tipo | Casa/fonte vera | Stanza/e servite | Uso | Stato | Archivio/prove | Limiti |
|---|---|---|---|---|---|---|---|
| Cartella madre | Cervello | Questa cartella | Tutte | Istruzioni, memoria, fonti e report | OK | `logs/`, git locale | Segreti fuori git |

## Regola di aggiornamento

Quando il cliente dice che esiste o va aggiunto un asset, l'agente aggiorna:

1. la casa/fonte vera dell'asset;
2. la stanza o le stanze realmente servite e questo registro;
3. `ecosistema/PROCESSI.md`, solo se cambia un lavoro ricorrente;
4. `ecosistema/LIMITI.md`, solo se introduce rischi o conferme obbligatorie;
5. `logs/install-log.md` o `REPORT_FINALE.md`, con cosa e' stato fatto.

Se manca una fonte reale, scrivere `DA COLLEGARE`. Non inventare accessi,
percorsi, password, account o stati.

## Caso PEC/email certificata

Per ogni cliente chiedere o scoprire se esiste una PEC/email certificata e cosa
deve farci l'agente:

- solo registrarla come recapito/asset;
- leggerla e archiviare messaggi/ricevute;
- preparare o inviare comunicazioni certificate.

Stato consentito:

- `NON SERVE` se il cliente non la usa;
- `DA SCOPRIRE` se non e' stato chiarito;
- `DA COLLAUDARE` se esiste ma manca una prova;
- `INSTALLABILE` se il provider consente collegamento ma manca consenso o
  configurazione;
- `ATTIVO` solo dopo prova reale.

Credenziali, app password e token stanno solo in `.secrets/`. Ogni invio a
terzi richiede conferma umana esplicita.
