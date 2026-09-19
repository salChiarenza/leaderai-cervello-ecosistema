#!/usr/bin/env python3
"""
Hook PostToolUse — la nota in chat di gruppo deve essere capibile da chi non c'era.

Problema che risolve (29/08/2026, sessione di lavoro): le note di `AGENT_CHAT.md` (radice della casa)
partivano dalla decisione senza dire di quale lavoro si trattava. Chi le legge dopo
(l'altro agente, una sessione nuova, il proprietario, un altro strumento) non capisce e deve riaprire tutto.
La regola scritta in testa al file non bastava: qui la fa rispettare la macchina.

Controlla la nota piu' recente del Log dopo ogni scrittura sul file:
- deve contenere `Di cosa si parla:`, `Cosa cambia:` e `Cosa serve:`;
- non deve superare le 20 righe.
Se manca qualcosa, blocca e chiede la riscrittura di quella sola nota.
"""
from __future__ import annotations

import json
import os
import re
import sys

FILE = "AGENT_CHAT.md"
RICHIESTI = ("Di cosa si parla:", "Cosa cambia:", "Cosa serve:")
MAX_RIGHE = 20
# Titolo di una nota, come lo scrive il calco in testa al file: due o tre
# cancelletti e una data, italiana (17/09/2026) oppure ISO (2026-09-17).
# L'inizio del registro: il titolo `## Log` a capo riga, non la parola citata
# dentro le regole d'uso in testa al file.
SEZIONE_LOG = re.compile(r"(?m)^## Log[ \t]*$")
TITOLO_NOTA = re.compile(r"(?m)^(?=#{2,3} \[?(?:\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}))")


def _event() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def _root(event: dict) -> str:
    return event.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def _prima_nota(testo: str) -> str | None:
    apertura = SEZIONE_LOG.search(testo)
    if not apertura:
        return None
    log = testo[apertura.end():]
    note = [n for n in re.split(TITOLO_NOTA, log) if n.strip()]
    return note[0] if note else None


def main() -> int:
    event = _event()
    root = _root(event)
    path = os.path.join(root, FILE)
    if not os.path.exists(path):
        return 0

    # gira solo se lo strumento ha davvero toccato la chat di gruppo
    blob = json.dumps(event.get("tool_input", {}), ensure_ascii=False)
    if "AGENT_CHAT.md" not in blob:
        return 0

    try:
        nota = _prima_nota(open(path, encoding="utf-8").read())
    except Exception:
        return 0
    if not nota:
        return 0

    mancano = [r for r in RICHIESTI if r not in nota]
    righe = len([r for r in nota.strip().splitlines() if r.strip()])
    problemi = []
    if mancano:
        problemi.append("mancano le parti: " + ", ".join(f"`{m}`" for m in mancano))
    if righe > MAX_RIGHE:
        problemi.append(f"e' lunga {righe} righe, il tetto e' {MAX_RIGHE}")
    if not problemi:
        return 0

    titolo = nota.strip().splitlines()[0]
    print(
        "Nota in chat di gruppo non leggibile da chi non c'era (" + "; ".join(problemi) + "). "
        f"Riscrivi solo quella nota ({titolo.strip('# ')}) nella forma prevista in testa a {FILE}: "
        "`Di cosa si parla:` una o due righe in parole normali che dicono di quale lavoro si "
        "tratta; `Cosa cambia:` il fatto nuovo o la decisione; `Cosa serve:` una cosa sola, chi "
        "fa cosa. Codici e percorsi solo nella riga `File:` in fondo.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
