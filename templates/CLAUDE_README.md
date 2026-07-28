# Claude Code

Claude Code deve partire dalla root cliente e leggere `CLAUDE.md` / `AGENTS.md`.

Per il controllo completo il proprietario puo' dire `lancia l'Ispettore` o
usare `/ispettore-ecosistema`. La skill apre la procedura unica `CHECKUP.md`
della repo `salChiarenza/leaderai-cervello-ecosistema`.

La memoria canonica e' dichiarata nell'`AGENTS.md` radice. Su ogni computer,
`~/.claude/settings.json` deve impostare `autoMemoryDirectory` sul suo percorso
assoluto. La chiave non e' accettata nelle settings project/local. Dopo il trust
del workspace, `/memory` deve mostrare la stessa destinazione prima del verdetto
`PASSA`.
