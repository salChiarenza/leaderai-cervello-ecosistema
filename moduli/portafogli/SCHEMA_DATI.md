# Schema dati Portafogli

## `DATI_PORTAFOGLIO.csv`

Il file accetta separatore virgola o punto e virgola e numeri italiani o
internazionali. Le percentuali sono espresse come punti da 0 a 100.

| Campo | Tipo | Regola |
|---|---|---|
| `strumento_id` | testo | identificativo stabile e univoco |
| `nome` | testo | denominazione leggibile |
| `classe` | testo | classe di attivo approvata dal banker |
| `componente` | testo | `CORE` oppure `SATELLITE` |
| `valuta` | testo | codice ISO, es. `EUR`, `USD` |
| `quantita` | numero | valore pari o superiore a zero |
| `prezzo_corrente` | numero | prezzo nella valuta dello strumento |
| `cambio_eur` | numero | EUR per una unità di valuta; `1` per EUR |
| `peso_target_pct` | numero | peso obiettivo; somma del file = 100 |
| `prezzo_riferimento` | numero | obbligatorio per il monitoraggio satellite |
| `fonte` | testo | file, provider o documento autorizzato |
| `data_fonte` | data | formato ISO `AAAA-MM-GG` |
| `ammesso` | booleano | `SI/NO`, `TRUE/FALSE`, `1/0` |

Formula base:

```text
valore_eur = quantita × prezzo_corrente × cambio_eur
peso_attuale_pct = valore_eur / totale_eur × 100
drift_pct = peso_attuale_pct - peso_target_pct
delta_eur = valore_target_eur - valore_attuale_eur
movimento_pct = prezzo_corrente / prezzo_riferimento - 1
```

Un peso target positivo su uno strumento con `ammesso = NO` blocca l'analisi.

## `RENDIMENTI_MENSILI.csv`

| Campo | Tipo | Regola |
|---|---|---|
| `data` | data | mese in formato `AAAA-MM` oppure data ISO |
| `strumento_id` | testo | deve esistere nel portafoglio target |
| `rendimento_mensile_pct` | numero | rendimento mensile in punti percentuali |
| `fonte` | testo | documento o provider autorizzato |
| `data_fonte` | data | data di acquisizione/verifica |

Il motore richiede un rendimento per ogni strumento con peso target positivo
in ogni mese. Una lacuna genera errore esplicito e preserva la qualità del
confronto.
