#!/usr/bin/env python3
"""Hook UserPromptSubmit — il manuale giusto arriva prima della spiegazione.

La casa tiene i manuali ufficiali degli strumenti nello sportello:
`assistenza/MANUALI.md`, con accanto quando si apre quale.
Averli scritti non basta: la regola «si apre la guida dello strumento di cui si
parla, non quella che si ha sottomano» va messa davanti all'agente prima che
scriva, altrimenti resta una frase da ricordare e si risponde a memoria.

Nessun indirizzo dentro questo file: si legge la tabella della casa. Un manuale
nuovo in quella tabella e' attivo senza toccare niente qui.

Fail-open e silenzioso: nessun riscontro o qualsiasi errore -> nessun output.
"""
from __future__ import annotations

import json
import os
import re
import sys

SCAFFALE = os.path.join("assistenza", "MANUALI.md")
CONTORNO = {"casa", "sviluppatori", "documentazione", "guida", "manuale", "docs", "academy"}


def _casa() -> str:
    for chiave in ("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR", "PROJECT_DIR"):
        valore = os.environ.get(chiave)
        if valore:
            return valore
    return os.getcwd()


def _guide(testo: str) -> list[tuple[str, str, str, list[str]]]:
    fuori = []
    for riga in testo.splitlines():
        riga = riga.strip()
        if not riga.startswith("|") or riga.startswith("|---") or "Quando si apre" in riga:
            continue
        pezzi = [p.strip() for p in riga.strip("|").split("|")]
        if len(pezzi) != 3 or "http" not in pezzi[1]:
            continue
        nudo = pezzi[0].replace("**", "").strip()
        nome = nudo.split("(")[0].strip()
        parole = []
        for pezzo in re.split(r"[(),/]|\be\b", nudo):
            pulito = " ".join(w for w in pezzo.split() if w.lower() not in CONTORNO).strip()
            if len(pulito) > 2:
                parole.append(pulito)
        if parole:
            fuori.append((nome, pezzi[1], pezzi[2], parole))
    return fuori


def main() -> int:
    try:
        dati = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = (dati.get("prompt") or "").lower()
    if not prompt:
        return 0
    try:
        with open(os.path.join(_casa(), SCAFFALE), encoding="utf-8") as fh:
            guide = _guide(fh.read())
    except OSError:
        return 0

    colpite = [
        "%s -> %s (si apre quando: %s)" % (nome, indirizzo, quando)
        for nome, indirizzo, quando, parole in guide
        if any(re.search(r"\b" + re.escape(p.lower()) + r"\b", prompt) for p in parole)
    ]
    if not colpite:
        return 0

    testo = ("MANUALE DA APRIRE IN QUESTA SESSIONE prima di dire come funziona un comando, "
             "una skill, un permesso o un'impostazione: " + " | ".join(colpite[:2]) +
             ". Si apre la guida dello strumento di cui si parla, non quella che si ha "
             "sottomano; la lettura vale per questa sessione, non per il ricordo.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": testo,
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
