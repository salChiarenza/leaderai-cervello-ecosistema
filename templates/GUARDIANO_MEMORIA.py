#!/usr/bin/env python3
"""
Hook UserPromptSubmit — richiamo ATTIVO delle memorie a contesto.

Il problema che risolve: le memorie in `memory/` sono PASSIVE. L'agente legge
l'indice `MEMORY.md` all'avvio, ma la singola memoria non scatta nel momento in
cui servirebbe — cosi' si ripete ogni volta lo stesso errore che quella memoria
avrebbe evitato.

Le poche regole SEMPRE valide le inietta il guardiano delle regole di casa a
ogni turno. Tutte le altre memorie sono A CONTESTO: iniettarle sempre sarebbe
rumore. Questo guardiano le attiva PER INNESCO.

Come: ogni memoria puo' dichiarare nel proprio frontmatter una riga
`trigger: [parola1, parola2, ...]`. Quando una di quelle parole compare nel
messaggio, la memoria viene richiamata in coda al messaggio (una riga sola,
descrizione + percorso), cosi' l'agente la apre PRIMA di lavorare, non dopo.

Niente secondo sistema di memoria: l'innesco e' un campo dentro il frontmatter
della memoria stessa. Per rendere attiva una memoria si aggiunge la riga
`trigger:`; nient'altro.

Fail-open e silenzioso: qualsiasi errore, o nessuna corrispondenza, non produce
nessun output e non blocca niente.

Installazione: `<casa>/.agent/hooks/GUARDIANO_MEMORIA.py`, richiamato come hook
UserPromptSubmit nelle impostazioni dell'agente.
"""
from __future__ import annotations

import glob
import difflib
import json
import os
import re
import sys
from pathlib import Path

MAX_RICHIAMI = 5


def _clean(tok: str) -> str:
    return tok.strip().strip('"').strip("'").lower()


def _casa() -> str:
    """La cartella madre: dalla variabile dell'agente, o risalendo dal file.

    Il guardiano vive in `<casa>/.agent/hooks/`, quindi due livelli sopra la
    sua cartella c'e' sempre la casa, ovunque il cliente l'abbia messa.
    """
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return env
    return str(Path(__file__).resolve().parents[2])


def _frontmatter(path: str) -> tuple[str | None, list[str]]:
    """Legge SOLO il frontmatter e ritorna (description, [trigger...]).

    `trigger` accettato in due stili YAML:
      inline  -> trigger: [a, b, c]
      block   -> trigger:\\n  - a\\n  - b
    """
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(2000)
    except OSError:
        return None, []
    lines = head.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, []
    desc: str | None = None
    trig: list[str] = []
    i, n = 1, len(lines)
    while i < n:
        s = lines[i].strip()
        if s == "---":
            break
        if s.startswith("description:"):
            desc = _clean(s.split(":", 1)[1])
        elif s.startswith("trigger:"):
            val = s.split(":", 1)[1].strip()
            if val and val != "[]":  # stile inline
                trig = [_clean(t) for t in val.strip("[]").split(",") if t.strip()]
            else:  # stile block: righe "- item" che seguono
                j = i + 1
                while j < n:
                    bs = lines[j].strip()
                    if bs.startswith("- "):
                        trig.append(_clean(bs[2:]))
                        j += 1
                    elif bs == "":
                        j += 1
                    else:
                        break
                i = j - 1
        i += 1
    return desc, [t for t in trig if t]


def _word_matches(trigger: str, words: set[str]) -> bool:
    """Parola esatta, oppure refuso breve e riconoscibile.

    Chi lavora da dettatura o da telefono scrive spesso storto: `rispodni` deve
    attivare `rispondi`. La somiglianza resta prudente: solo parole lunghe,
    stessa iniziale, lunghezza quasi uguale e somiglianza alta.
    """
    if trigger in words:
        return True
    if len(trigger) < 6 or " " in trigger:
        return False
    return any(
        len(word) >= 6
        and word[:1] == trigger[:1]
        and abs(len(word) - len(trigger)) <= 2
        and difflib.SequenceMatcher(None, word, trigger).ratio() >= 0.82
        for word in words
    )


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = (data.get("prompt") or "").lower()
    if not prompt:
        return 0
    root = _casa()
    memdir = os.path.join(root, "memory")
    if not os.path.isdir(memdir):
        return 0

    # Parole intere del messaggio: un innesco di una parola sola combacia su
    # parola intera (niente pezzi dentro altre parole, tipo 'iva' in 'attiva').
    parole = set(re.findall(r"[a-zàèéìòùA-Z0-9]+", prompt))

    richiami: list[tuple[int, str, str]] = []
    for path in sorted(glob.glob(os.path.join(memdir, "*.md"))):
        if os.path.basename(path) == "MEMORY.md":
            continue
        try:
            desc, trig = _frontmatter(path)
        except Exception:
            continue
        if not trig:
            continue
        hit = [
            t
            for t in trig
            if (" " in t and t in prompt) or (" " not in t and _word_matches(t, parole))
        ]
        if hit:
            rel = os.path.relpath(path, root)
            richiami.append((len(hit), rel, desc or rel))

    if not richiami:
        return 0
    richiami.sort(key=lambda x: -x[0])  # piu' inneschi combaciati = piu' pertinente
    righe = "\n".join("• %s" % rel for _, rel, _ in richiami[:MAX_RICHIAMI])
    ctx = "MEMORIE PERTINENTI: apri solo quelle utili e applicale.\n" + righe
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ctx,
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
