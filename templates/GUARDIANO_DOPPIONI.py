#!/usr/bin/env python3
"""
Guardiano anti-proliferazione (hook PreToolUse su Write).

Malattia (13/06): ognuno crea un FILE NUOVO invece di modificare quello che
c'e'. Firma: file con una DATA nel nome (es. `home-224-20260524-editoriale.html`),
copie-fotografia di una cosa che esiste gia'. 282 file su 1258 sono cosi'.

Regola che fa rispettare (CLAUDE.md "Keep it simple"): UN file per cosa. Si
MODIFICA, non si copia. La data sta in git, non nel nome.

Blocca SOLO il caso inequivocabile, e in tutto il resto LASCIA PASSARE
(fail-open: meglio non bloccare che bloccare per errore):

  DENY se, TUTTI insieme:
    1. il file NON esiste ancora (lo stai creando, non modificando);
    2. NON e' dentro backups/ o logs/ (li' le copie datate sono legittime);
    3. il nome ha una DATA + un NOME vero davanti (NAME+data = snapshot di NAME),
       non solo una data (una data sola = log datato legittimo, es. audit/2026-06-13.md);
    4. esiste GIA' un file "fratello" con lo stesso nome-prima-della-data
       (cioe' stai aggiungendo l'ennesima copia a una famiglia che gia' c'e').

  In tutti gli altri casi: allow (nessun output, exit 0).
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

# token data: 20260524 | 2026-05-24 | 2026_05_24 | 240526-ish no (troppo ambiguo)
DATA = re.compile(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})")
ESENTI_DIR = ("/backups/", "/backup/", "/logs/", "/log/", "/.git/", "/_archivio/", "/_storico/")


def nome_prima_della_data(stem):
    """Ritorna il nome che precede la prima data nel filename (senza estensione),
    ripulito da separatori finali. '' se la data e' all'inizio (= log datato)."""
    m = DATA.search(stem)
    if not m:
        return None  # nessuna data: non e' uno snapshot, non ci riguarda
    prefisso = stem[:m.start()].strip(" -_.")
    return prefisso


def deve_bloccare(file_path):
    p = file_path.replace("\\", "/")
    # 1) sta CREANDO (non modificando)?
    if os.path.exists(file_path):
        return None
    # 2) cartelle dove le copie datate sono legittime
    low = p.lower()
    if any(frag in low + "/" for frag in ESENTI_DIR):
        return None
    stem = os.path.splitext(os.path.basename(p))[0]
    # 3) NOME + data (non solo data)
    prefisso = nome_prima_della_data(stem)
    if prefisso is None or len(prefisso) < 3:
        return None  # niente data, o data sola (log legittimo)
    # 4) esiste gia' una "famiglia" con quello stesso prefisso nella stessa cartella?
    dirp = os.path.dirname(file_path) or "."
    fratelli = [f for f in glob.glob(os.path.join(dirp, prefisso + "*"))
                if os.path.abspath(f) != os.path.abspath(file_path)]
    if not fratelli:
        return None  # primo della famiglia: lascia passare (non e' "l'ennesima copia")
    esempi = ", ".join(sorted(os.path.basename(f) for f in fratelli)[:3])
    return (prefisso, esempi)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # input illeggibile -> non blocco mai
    if data.get("tool_name") != "Write":
        return 0
    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    try:
        esito = deve_bloccare(file_path)
    except Exception:
        return 0  # qualunque errore -> fail-open
    if not esito:
        return 0
    prefisso, esempi = esito
    reason = (
        "STOP — regola un-file-per-cosa. Stai creando una COPIA datata di '%s', "
        "ma esiste gia' (%s). Non aggiungere l'ennesimo file: MODIFICA quello giusto, "
        "la copia di sicurezza quotidiana tiene la storia. La data non va nel nome del file. "
        "Se ti serve davvero uno snapshot storico, mettilo in una cartella backups/ o logs/."
        % (prefisso, esempi)
    )
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
