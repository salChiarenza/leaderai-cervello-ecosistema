# Ispettore del Bando

Agente installabile per preparare e controllare domande di bando, voucher e
contributi direttamente nell'ambiente dell'impresa.

Non si limita a fare un audit: legge fonti ufficiali, ricostruisce il fascicolo,
controlla ogni documento e ogni coppia di spesa, completa il lavoro reversibile
e ripete la verifica finche resta soltanto un vero gesto del titolare.

## Scheda

| Campo | Valore |
|---|---|
| Attivazione | `Lancia l'Ispettore del Bando` o controllo di una pratica reale |
| Fonte | Bando, modulistica e portale ufficiali correnti + fascicolo locale dell'impresa |
| Risultato | Verdetto unico, report leggibile e ricevuta legata alle prove |
| Controllo | Requisiti, progetto, fornitori, spese, moduli, firme, portale e rendicontazione |
| Arresto | Identita/2FA, firma, dichiarazione, pagamento, invio finale e scelte del titolare |

## Contenuto

- `INSTALLA_CON_AI.md`: installazione guidata da Claude.
- `SKILL.md`: ingresso operativo automatico.
- `PROCEDURA.md`: metodo completo e riutilizzabile.
- `assets/CONTROLLO_BANDO.template.json`: matrice iniziale.
- `assets/INDICE_SPESE.template.csv`: una riga verificabile per ogni coppia fattura-pagamento.
- `scripts/verifica_fascicolo.py`: controllo deterministico e ricevuta.
- `AGENTE_CLAUDE.md`: adattatore opzionale per case che usano subagenti.
- `COLLAUDO.md`: prove del comportamento sotto pressione.

Il pacchetto non contiene documenti o dati di un cliente. Ogni pratica resta
nel computer del titolare; LeaderAI riceve soltanto gli esiti autorizzati.
