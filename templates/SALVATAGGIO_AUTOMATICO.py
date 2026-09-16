#!/usr/bin/env python3
"""
Hook Stop — salvataggio automatico della casa nel registro git locale.

Problema (16/09/2026, studio legale): ogni turno lascia modifiche non salvate
e l'app dell'agente mostra di continuo la barra «Conferma modifiche». Il
proprietario non deve cliccare niente: a fine turno la casa si salva da sola.

Cosa fa: se la cartella madre e' un registro git e ci sono modifiche, le
aggiunge e crea un salvataggio con data e ora. Rispetta .gitignore e in piu'
lascia fuori qualunque file che sembri un segreto (token, chiavi, password,
credenziali, .env, impostazioni locali), anche se non ignorato.

Fail-open e silenzioso: nessun git, nessuna modifica o qualsiasi errore ->
nessun output, exit 0. Non blocca mai la chiusura del turno.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime

SEGRETI = re.compile(
    r"(?:^|/)(?:\.secrets/|\.env$|[^/]*\.env$|[^/]*\.key$|[^/]*\.pem$|"
    r"[^/]*token[^/]*|[^/]*secret[^/]*|[^/]*password[^/]*|[^/]*credential[^/]*|"
    r"settings\.local\.json$)",
    re.IGNORECASE,
)
IDENTITA = ["-c", "user.name=Cervello LeaderAI", "-c", "user.email=cervello@leaderai.local"]


def _git(*args: str, cwd: str, extra: list[str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *(extra or []), *args], cwd=cwd, capture_output=True, text=True
    )


def casa() -> str:
    for chiave in ("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR"):
        valore = os.environ.get(chiave)
        if valore:
            return valore
    esito = _git("rev-parse", "--show-toplevel", cwd=os.getcwd())
    return esito.stdout.strip() or os.getcwd()


def salva(cwd: str) -> bool:
    """Un salvataggio se c'e' qualcosa da salvare. True = commit creato."""
    if _git("rev-parse", "--is-inside-work-tree", cwd=cwd).stdout.strip() != "true":
        return False
    if not _git("status", "--porcelain", "--untracked-files=all", cwd=cwd).stdout.strip():
        return False
    _git("add", "-A", cwd=cwd)
    in_attesa = _git("diff", "--cached", "--name-only", cwd=cwd).stdout.splitlines()
    esclusi = [p for p in in_attesa if SEGRETI.search(p)]
    if esclusi:
        _git("reset", "-q", "--", *esclusi, cwd=cwd)
    if not _git("diff", "--cached", "--name-only", cwd=cwd).stdout.strip():
        return False
    messaggio = "Salvataggio automatico " + datetime.now().strftime("%d/%m/%Y %H:%M")
    esito = _git("commit", "-q", "-m", messaggio, cwd=cwd)
    if esito.returncode != 0:
        esito = _git("commit", "-q", "-m", messaggio, cwd=cwd, extra=IDENTITA)
    return esito.returncode == 0


def main() -> int:
    try:
        sys.stdin.read()  # il payload dell'hook non serve: si guarda il disco
    except Exception:
        pass
    try:
        salva(casa())
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
