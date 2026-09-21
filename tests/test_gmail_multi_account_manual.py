"""La richiesta su piu' Gmail apre la guida ufficiale prima della spiegazione."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PRODOTTO = Path(__file__).resolve().parents[1]
GUARDIANO = PRODOTTO / "templates" / "GUARDIANO_MANUALI.py"
MANUALI = PRODOTTO / "templates" / "assistenza" / "MANUALI.md"


def test_aggiungere_un_altro_account_gmail_apre_la_guida_google(tmp_path: Path):
    assistenza = tmp_path / "assistenza"
    assistenza.mkdir()
    (assistenza / "MANUALI.md").write_text(
        MANUALI.read_text(encoding="utf-8"), encoding="utf-8"
    )

    esito = subprocess.run(
        [sys.executable, str(GUARDIANO)],
        input=json.dumps({"prompt": "come aggiungo un altro account Gmail nel browser?"}),
        capture_output=True,
        text=True,
        timeout=60,
        env={"PATH": "/usr/bin:/bin", "CODEX_PROJECT_DIR": str(tmp_path)},
    )

    assert esito.returncode == 0, esito.stderr
    contesto = json.loads(esito.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "support.google.com/accounts/answer/1721977" in contesto
