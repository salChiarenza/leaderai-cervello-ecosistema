"""Nella casa del cliente il manuale giusto arriva prima della spiegazione.

19/09/2026, Sal: «la parte dei manuali va integrata nell'ecosistema che mandiamo ai
clienti, cosi' i loro agenti possono attingere a queste fonti». Le guide ufficiali
c'erano gia' nella casa del cliente, ma servivano a un solo controllo e nessuno le
apriva al momento giusto. Dal 21/09/2026 vivono nello sportello `assistenza/MANUALI.md`. Ora ci attinge qualsiasi agente della casa, e il guardiano
le mette davanti quando la richiesta nomina lo strumento.

Portabile: nessun percorso della casa di Sal, nessun indirizzo scritto nel guardiano.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRODOTTO = Path(__file__).resolve().parents[1]
GUARDIANO = PRODOTTO / "templates" / "GUARDIANO_MANUALI.py"
SCAFFALE = PRODOTTO / "templates" / "assistenza" / "MANUALI.md"


def _casa_finta(tmp_path: Path) -> Path:
    (tmp_path / "assistenza").mkdir(parents=True, exist_ok=True)
    (tmp_path / "assistenza" / "MANUALI.md").write_text(
        SCAFFALE.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def _lancia(prompt: str, casa: Path) -> str:
    esito = subprocess.run(
        [sys.executable, str(GUARDIANO)], input=json.dumps({"prompt": prompt}),
        capture_output=True, text=True, timeout=60,
        env={"PATH": "/usr/bin:/bin", "CLAUDE_PROJECT_DIR": str(casa)},
    )
    assert esito.returncode == 0, esito.stderr
    if not esito.stdout.strip():
        return ""
    return json.loads(esito.stdout)["hookSpecificOutput"]["additionalContext"]


def test_chi_parla_di_codex_riceve_la_guida_di_codex(tmp_path):
    testo = _lancia("come configuro un hook in Codex?", _casa_finta(tmp_path))
    assert "learn.chatgpt.com" in testo
    assert "code.claude.com" not in testo


def test_chi_parla_di_claude_code_riceve_la_sua(tmp_path):
    assert "code.claude.com" in _lancia("Claude Code non parte", _casa_finta(tmp_path))


def test_il_lavoro_normale_del_cliente_resta_in_silenzio(tmp_path):
    assert _lancia("prepara il preventivo per il cliente", _casa_finta(tmp_path)) == ""


def test_senza_lo_scaffale_non_disturba(tmp_path):
    assert _lancia("come configuro un hook in Codex?", tmp_path) == ""


def test_niente_percorsi_di_sal_ne_indirizzi_nel_guardiano():
    codice = GUARDIANO.read_text(encoding="utf-8")
    assert "/Users/sal" not in codice, "percorso della casa di Sal in un file del prodotto"
    assert "code.claude.com" not in codice and "learn.chatgpt.com" not in codice


def test_un_manuale_nuovo_nello_scaffale_e_subito_attivo(tmp_path):
    """La prova del fratello: il manuale che il cliente aggiungera' domani."""
    casa = _casa_finta(tmp_path)
    fonti = casa / "assistenza" / "MANUALI.md"
    fonti.write_text(fonti.read_text(encoding="utf-8")
                     + "\n| **Strumento Nuovo** (Tizio) | https://esempio.test/guida | si lavora con Strumento Nuovo |\n",
                     encoding="utf-8")
    assert "esempio.test" in _lancia("apriamo Strumento Nuovo", casa)


def test_il_guardiano_e_installato_nelle_due_case_del_cliente():
    claude = json.loads((PRODOTTO / "templates" / "CLAUDE_SETTINGS.json").read_text(encoding="utf-8"))
    codex = json.loads((PRODOTTO / "templates" / "CODEX_HOOKS.json").read_text(encoding="utf-8"))
    contratto = (PRODOTTO / "install_contract.json").read_text(encoding="utf-8")
    acceso = json.dumps(claude, ensure_ascii=False) + json.dumps(codex, ensure_ascii=False)
    assert acceso.count("guardiano_manuali.py") >= 2, "non e' acceso in tutte e due le case"
    assert "GUARDIANO_MANUALI.py" in contratto, "l'installazione non lo porta nella casa"
