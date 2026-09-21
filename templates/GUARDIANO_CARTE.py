#!/usr/bin/env python3
"""Hook UserPromptSubmit — la carta giusta della casa arriva col sintomo.

La casa tiene le sue carte, e nello sportello `assistenza/SINTOMI.md` c'e'
scritto quale si apre a seconda di cosa sta succedendo. Averle scritte non
basta: quando il proprietario racconta il sintomo, quella riga va messa davanti
all'agente prima che risponda, altrimenti si tira a indovinare e la carta resta
chiusa.

Nessun indirizzo e nessun nome di carta dentro questo file: si legge la tabella
della casa. Una riga nuova in quella tabella e' attiva senza toccare niente qui.

Fail-open e silenzioso: nessun riscontro o qualsiasi errore -> nessun output.
"""
from __future__ import annotations

import json
import os
import re
import sys

PAGINA = os.path.join("assistenza", "SINTOMI.md")
# parole che stanno in ogni frase italiana: da sole non descrivono un sintomo
CONTORNO = {
    "anche", "ancora", "altra", "altro", "come", "cosa", "cose", "dalla",
    "degli", "della", "delle", "dello", "dopo", "dove", "essere", "fare",
    "fatta", "fatto", "mentre", "molto", "nella", "niente", "nulla", "oppure",
    "perche", "prima", "qualcosa", "qualcuno", "quando", "quella", "quelle",
    "quello", "questa", "queste", "questi", "questo", "sempre", "senza",
    "solo", "soltanto", "sono", "sopra", "sotto", "stato", "tutta", "tutto",
    "verso",
}
# una riga si accende quando il prompt ne tocca almeno due parole: una sola
# parola in comune e' un'assonanza, non un sintomo
SOGLIA = 2


def _casa() -> str:
    for chiave in ("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR", "PROJECT_DIR"):
        valore = os.environ.get(chiave)
        if valore:
            return valore
    return os.getcwd()


def _carte(testo: str) -> list[tuple[str, str, list[str]]]:
    fuori = []
    for riga in testo.splitlines():
        riga = riga.strip()
        if not riga.startswith("|") or riga.startswith("|---"):
            continue
        pezzi = [p.strip().replace("**", "") for p in riga.strip("|").split("|")]
        # due colonne, e la seconda deve indicare davvero una carta: cosi' la
        # riga di intestazione resta fuori da sola, senza sapere come si chiama
        if len(pezzi) != 2 or ".md" not in pezzi[1]:
            continue
        parole = sorted({
            parola
            for parola in re.split(r"[^a-zà-ÿ]+", pezzi[0].lower())
            if len(parola) > 3 and parola not in CONTORNO
        })
        if parole:
            fuori.append((pezzi[0], pezzi[1], parole))
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
        with open(os.path.join(_casa(), PAGINA), encoding="utf-8") as fh:
            carte = _carte(fh.read())
    except OSError:
        return 0

    pesate = []
    for sintomo, carta, parole in carte:
        toccate = sum(
            1 for parola in parole
            if re.search(r"\b" + re.escape(parola) + r"\b", prompt)
        )
        if toccate >= min(SOGLIA, len(parole)):
            pesate.append((toccate, "%s -> %s" % (sintomo, carta)))
    if not pesate:
        return 0
    pesate.sort(key=lambda voce: -voce[0])
    colpite = [voce for _, voce in pesate[:2]]

    testo = ("CARTA DELLA CASA DA APRIRE IN QUESTA SESSIONE prima di dire cos'e' "
             "rotto e prima di ripararlo: " + " | ".join(colpite) +
             ". Si apre la carta del sintomo che si ha davanti, non quella che si "
             "ha sottomano; la lettura vale per questa sessione, non per il ricordo.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": testo,
    }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
