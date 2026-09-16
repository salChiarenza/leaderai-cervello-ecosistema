#!/usr/bin/env python3
"""Lucchetto condiviso: UN SOLO blocco per turno, fra tutti i guardiani.

Il 30/08/2026 il proprietario ha visto tre copie della stessa bozza email in chat. Causa:
ogni guardiano Stop che blocca costringe l'agente a RIPUBBLICARE il messaggio
intero, bozze comprese. Con un guardiano solo era un fastidio; da quando sono
due (assenso 14/06, sintesi 27/08) il blocco del primo finiva nel transcript e
faceva scattare il secondo. Uno chiamava l'altro.

Regola: il primo guardiano che blocca in un turno prende il lucchetto. Gli altri
quel turno lasciano passare e si limitano al turno dopo. Cosi' l'agente riscrive
al massimo una volta e il proprietario non vede mai la stessa cosa tre volte.
"""
from pathlib import Path

def casa():
    """La cartella madre: la dice l'agente, o si risale da questo file."""
    import os
    from pathlib import Path
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and Path(env).is_dir():
        return Path(env)
    return Path(__file__).resolve().parents[2]


STATO = casa() / ".agent" / "state" / "turno_guardiani.txt"


def prendi_lucchetto(dati: dict, nome: str) -> bool:
    """True se questo guardiano puo' bloccare adesso: nessun altro l'ha gia' fatto."""
    turno = str(dati.get("prompt_id") or dati.get("session_id") or "")
    if not turno:
        return True
    try:
        occupato, da_chi = STATO.read_text(encoding="utf-8").strip().split("|", 1)
    except (OSError, ValueError):
        occupato, da_chi = "", ""
    if occupato == turno:
        return False                      # qualcuno ha gia' bloccato questo turno
    try:
        STATO.parent.mkdir(parents=True, exist_ok=True)
        STATO.write_text("%s|%s" % (turno, nome), encoding="utf-8")
    except OSError:
        pass
    return True
