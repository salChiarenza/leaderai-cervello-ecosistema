# Asset operativi

Registro unico delle risorse operative del cliente.

Un asset e' qualunque cosa che l'agente deve sapere trovare, usare o rispettare:
email/PEC, banca, auto, fornitore, gestionale, Drive, WhatsApp, sito, repo,
kit, app, servizio esterno, archivio o canale ufficiale.

## Registro

| Asset | Tipo | Casa/fonte vera | Uso | Stato | Archivio/prove | Limiti |
|---|---|---|---|---|---|---|
| Cartella madre | Cervello | Questa cartella | Istruzioni, memoria, fonti e report | OK | `logs/`, git locale | Segreti fuori git |

## Regola di aggiornamento

Quando il cliente dice che esiste o va aggiunto un asset, l'agente aggiorna:

1. la casa/fonte vera dell'asset;
2. questo registro;
3. `ecosistema/PROCESSI.md`, solo se cambia un lavoro ricorrente;
4. `ecosistema/LIMITI.md`, solo se introduce rischi o conferme obbligatorie;
5. `logs/install-log.md` o `REPORT_FINALE.md`, con cosa e' stato fatto.

Se manca una fonte reale, scrivere `DA COLLEGARE`. Non inventare accessi,
percorsi, password, account o stati.
