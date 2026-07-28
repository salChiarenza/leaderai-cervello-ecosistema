# Claude Code

Claude Code deve partire dalla root cliente e leggere `CLAUDE.md` / `AGENTS.md`.

Per il controllo completo il proprietario puo' dire `lancia l'Ispettore` o
usare `/ispettore-ecosistema`. La skill apre la procedura unica `CHECKUP.md`
della repo `salChiarenza/leaderai-cervello-ecosistema`.

La memoria unica vive in `memory/`. `.claude/settings.local.json` deve puntare
qui con `autoMemoryDirectory` usando il percorso assoluto della cartella madre.
La configurazione diventa attiva dopo il trust del workspace; `/memory` deve
mostrare questa stessa destinazione prima del verdetto `PASSA`.
