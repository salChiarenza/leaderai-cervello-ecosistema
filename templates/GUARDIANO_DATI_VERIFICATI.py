#!/usr/bin/env python3
"""
Hook Stop — guardiano della RISERVA (Claude Code; gemello Codex via sync).

Problema (27/06): l'errore non e' "non sapevo il dato", e' aver consegnato
un dato concreto (link, IBAN, prezzo, data, nome) NON verificato, vestito da
risposta con una frase di riserva ("ho usato il link... *se e' diverso dimmi*").
La riserva non e' una protezione: e' la prova che sapevo di non aver verificato.

Regola che fa rispettare (Definizione di Finito, a livello di ELEMENTO):
un dato concreto o l'ho aperto alla fonte (verificato), o lo dichiaro mancante
in modo netto. La terza via — "sembra giusto, lo metto con la riserva" — e'
vietata. La riserva su un fatto = STOP, non lasciapassare.

Come: a fine turno legge l'ultimo messaggio di testo dell'agente. Se contiene
INSIEME (a) una frase di riserva e (b) il segnale di un dato concreto, blocca la
chiusura UNA volta e ricorda di verificare o dichiarare il buco.

Universale: vale per ogni reparto e ogni tipo di dato, non solo i link.
Fail-open e silenzioso: qualsiasi errore o nessun match -> nessun output.
`stop_hook_active` = loop guard: scatta una volta sola.
"""
from __future__ import annotations

import json
import os
import re
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from guardiano_turno import prendi_lucchetto

# (a) Frasi di riserva: il "tell" che so di non aver verificato.
RISERVA = [
    r"\bse\b.{0,45}\b(?:diverso|diversa|sbagliato|sbagliata|un altro|un'altra|errato|errata)\b",
    r"se non (?:è|e'|e) (?:giusto|giusta|quello|quella|corretto|corretta)",
    r"se sbaglio",
    r"\bcorreggi(?:mi|lo|la)?\b",
    r"\bdimmi se\b",
    r"\bfammi sapere se\b",
    r"confermi che (?:è|e'|e)",
    r"\bse confermi\b",
    r"\b(?:dammi|mandami|passami) (?:l'|il |la )?(?:url|link|indirizzo|form|iban|dato)\b",
    r"\b(?:lo|la|li) sostituisco\b",
    r"\b(?:te lo|te la) (?:cambio|sostituisco)\b",
    r"\bcredo (?:che |sia |di )",
    r"\bdovrebbe essere\b",
    r"\bpresumo\b",
    r"\bsalvo errori\b",
    r"non sono sicuro",
    r"\bmi pare\b",
    r"\bpenso sia\b",
    r"\bverifica tu\b",
    r"se ho capito bene",
    r"\bse (?:è|e'|e) corretto\b",
]

# (b) Segnale di un dato concreto nello stesso messaggio.
DATO = [
    r"https?://\S+",                 # link/URL
    r"\bIBAN\b",
    r"€\s?\d|\bEUR\b|\d+\s?euro",    # prezzo
    r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",  # data gg/mm(/aaaa)
    r"\bil link\b|\bil form\b|\bla mail\b",
]


def _ultimo_testo(transcript_path: str) -> str:
    """Ultimo messaggio assistant che contiene un blocco di testo."""
    try:
        righe = open(transcript_path, encoding="utf-8").read().splitlines()
    except OSError:
        return ""
    testo = ""
    for line in righe:
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") != "assistant":
            continue
        cont = (o.get("message") or {}).get("content")
        if isinstance(cont, list):
            parti = [b.get("text", "") for b in cont if b.get("type") == "text"]
            if any(p.strip() for p in parti):
                testo = "\n".join(parti)
        elif isinstance(cont, str) and cont.strip():
            testo = cont
    return testo


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0  # loop guard: una volta sola
    tp = data.get("transcript_path") or ""
    if not tp:
        return 0
    testo = _ultimo_testo(tp)
    if not testo:
        return 0
    # Una frase di riserva CITATA (tra virgolette «» "" '' o in blocco code)
    # non e' una riserva reale: e' spiegazione della regola. La rimuovo prima di
    # cercare il "tell", cosi' parlare della regola non fa scattare il guardiano.
    senza_citazioni = re.sub(r"«[^»]*»|\"[^\"]*\"|'[^']*'|`[^`]*`", " ", testo)
    low = senza_citazioni.lower()

    hit_riserva = next((m.group(0) for r in RISERVA
                        for m in [re.search(r, low)] if m), None)
    if not hit_riserva:
        return 0
    if not any(re.search(r, testo, re.IGNORECASE) for r in DATO):
        return 0

    msg = (
        "RISERVA SU UN DATO CONSEGNATO — fermati prima di chiudere.\n"
        "Nel tuo ultimo messaggio hai messo un dato concreto (link/IBAN/prezzo/"
        "data) accompagnato da una frase di riserva: «%s».\n"
        "Una riserva su un fatto non e' un lasciapassare: e' la prova che non l'hai "
        "verificato. Regola (Definizione di Finito, per elemento): o apri la fonte "
        "in questa sessione e confermi il dato, o lo dichiari MANCANTE in modo netto "
        "e togli il valore inventato. Niente terza via «sembra giusto, lo metto con "
        "la riserva». Correggi l'output, poi chiudi." % hit_riserva
    )
    # un solo blocco per turno fra tutti i guardiani (vedi turno_guard.py)
    if not prendi_lucchetto(data, "riserva"):
        return 0

    print(json.dumps({"decision": "block", "reason": msg}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
