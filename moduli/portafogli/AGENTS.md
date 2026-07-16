# Modulo Portafogli — mappa

Questa cartella è il pacchetto versionato del Sistema Portafogli Core-Satellite
LeaderAI. Eredita le regole dalla radice della repo.

## Dentro

- `INSTALLA_MODULO.md`: missione operativa per l'agente del cliente.
- `installa_portafogli.py`: montaggio idempotente nella cartella viva.
- `portfolio_engine.py`: calcoli e backtest deterministici.
- `PROCESSO.md`: flusso completo dal dato al report.
- `SCHEMA_DATI.md`: contratto dei file CSV.
- `*.template.md` e `*_MODELLO.*`: file iniziali da personalizzare.
- `SKILL.md`: orchestratore Claude Code installato nella cartella cliente.

## Fuori

- I dati reali restano nella cartella viva del cliente.
- Le decisioni finanziarie restano al banker.
- Le missioni e i resoconti viaggiano via email con il protocollo della repo.

## Regole di modifica

1. Mantieni il modulo riavviabile e conservativo sui file personalizzati.
2. Ogni calcolo numerico passa da `portfolio_engine.py` e dai test.
3. Ogni campo concreto porta fonte e data.
4. Aggiorna `VERSION`, README, Manifest e test quando cambia il contratto.
5. Esegui `python3 -m unittest discover -s tests` dalla radice prima del rilascio.
