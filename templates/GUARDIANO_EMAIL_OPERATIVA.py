#!/usr/bin/env python3
"""
Hook PreToolUse — un'email operativa dice sempre le quattro cose.

Il problema che risolve: quando l'agente scrive per conto del proprietario a un
cliente, a un fornitore o all'agente di qualcun altro, e' facile che il testo
racconti il lavoro invece di farlo capire. Chi legge resta senza sapere a che
punto siamo, cosa deve fare e quando la cosa e' chiusa.

La regola: un'email operativa apre con quattro risposte, con queste parole.

    Cosa funziona:      quello che e' gia' in piedi e provato
    Cosa completiamo:   quello che chiude questo giro
    Cosa serve da te:   il solo gesto umano necessario, oppure "niente"
    Quando si chiude:   il fatto osservabile che dice che e' finita

Non blocca le email personali: scatta solo quando il testo ha il tono di un
lavoro (una richiesta, una consegna, un aggiornamento) ed e' abbastanza lungo
da essere una missione, non un saluto.

Blocca prima dell'invio (exit 2), cosi' l'agente riscrive e nessuno riceve un
testo che non si capisce. Fail-open: qualsiasi errore, nessun blocco.

Installazione: `<casa>/.agent/hooks/guardiano_email_operativa.py`, hook
PreToolUse sugli strumenti che mandano posta.
"""
from __future__ import annotations

import json
import re
import sys

MINIMO_PAROLE = 40  # sotto questa soglia e' un messaggio breve, non una missione

SEZIONI = (
    ("Cosa funziona", r"cosa\s+funziona"),
    ("Cosa completiamo", r"cosa\s+(?:completiamo|chiudiamo|facciamo)"),
    ("Cosa serve da te", r"cosa\s+serve\s+(?:da\s+te|da\s+voi|da\s+lei)"),
    ("Quando si chiude", r"quando\s+si\s+chiude"),
)

# Segnali che il testo e' una comunicazione di lavoro e non un saluto.
LAVORO = re.compile(
    r"\b(?:install\w+|aggiorn\w+|configur\w+|consegn\w+|missione|procedura|"
    r"esegui|verifica|collaud\w+|scadenz\w+|prossim\w+ pass\w+|allegat\w+)\b",
    re.IGNORECASE,
)


def _testo(dati: dict) -> str:
    campi = dati.get("tool_input") or {}
    if not isinstance(campi, dict):
        return ""
    pezzi = [
        campi.get(chiave) or ""
        for chiave in ("subject", "body", "text", "message", "htmlBody")
    ]
    return "\n".join(p for p in pezzi if isinstance(p, str))


def main() -> int:
    try:
        dati = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    nome = str(dati.get("tool_name") or "")
    if "send" not in nome.lower() and "mail" not in nome.lower():
        return 0

    testo = _testo(dati)
    if not testo.strip():
        return 0
    if len(testo.split()) < MINIMO_PAROLE:
        return 0
    if not LAVORO.search(testo):
        return 0

    mancanti = [
        etichetta
        for etichetta, schema in SEZIONI
        if not re.search(schema, testo, re.IGNORECASE)
    ]
    if not mancanti:
        return 0

    print(
        "EMAIL OPERATIVA INCOMPLETA\n"
        "Chi la riceve deve capire subito a che punto siamo e cosa fare.\n"
        "Mancano queste risposte in apertura: " + ", ".join(mancanti) + ".\n"
        "Riscrivi il testo con le quattro righe e rimanda.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
