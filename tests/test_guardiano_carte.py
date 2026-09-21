"""Nella casa del cliente la carta giusta arriva insieme al sintomo.

`assistenza/SINTOMI.md` dice gia' dove si guarda a seconda di cosa
sta succedendo. Scritto non basta: il proprietario racconta il sintomo con le sue
parole («non e' partito», «e' pieno di doppioni») e l'assistente tira a indovinare
mentre la carta sta li' chiusa. Il guardiano gliela mette davanti nel momento in
cui il sintomo viene nominato.

Stessa forma del guardiano dei manuali: la tabella della casa e' la fonte, il
programma non conosce nessuna carta. Una riga nuova nella tabella si accende da
sola, senza toccare il codice.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRODOTTO = Path(__file__).resolve().parents[1]
GUARDIANO = PRODOTTO / "templates" / "GUARDIANO_CARTE.py"
PAGINA = PRODOTTO / "templates" / "assistenza" / "SINTOMI.md"


def _casa_finta(tmp_path: Path) -> Path:
    (tmp_path / "assistenza").mkdir(parents=True, exist_ok=True)
    (tmp_path / "assistenza" / "SINTOMI.md").write_text(
        PAGINA.read_text(encoding="utf-8"), encoding="utf-8")
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


def test_chi_racconta_una_cosa_che_non_e_partita_riceve_la_carta_di_cio_che_gira(tmp_path):
    testo = _lancia("la manutenzione doveva partire stanotte e non e' partita",
                    _casa_finta(tmp_path))
    assert "COSA_E_ACCESO.md" in testo
    assert "LIMITI.md" not in testo


def test_chi_racconta_la_casa_disordinata_riceve_la_carta_del_controllo(tmp_path):
    testo = _lancia("la casa e' piena di doppioni e di stanze senza contratto",
                    _casa_finta(tmp_path))
    assert "CHECKUP.md" in testo


def test_chi_non_sa_se_e_un_guasto_riceve_la_carta_dei_limiti(tmp_path):
    testo = _lancia("l'agente non riesce a farlo, e' un guasto?", _casa_finta(tmp_path))
    assert "LIMITI.md" in testo


def test_il_lavoro_normale_del_cliente_resta_in_silenzio(tmp_path):
    casa = _casa_finta(tmp_path)
    assert _lancia("prepara il preventivo per il cliente", casa) == ""
    assert _lancia("scrivi due righe di risposta a Marco", casa) == ""


def test_una_parola_sola_in_comune_non_basta(tmp_path):
    """Assonanza, non sintomo: «casa» da sola non apre nessuna carta."""
    assert _lancia("fai il backup della casa", _casa_finta(tmp_path)) == ""


def test_senza_la_pagina_non_disturba(tmp_path):
    assert _lancia("la manutenzione doveva partire e non e' partita", tmp_path) == ""


def test_mai_piu_di_due_carte_per_volta(tmp_path):
    testo = _lancia(
        "la fonte e' vuota e risponde cose diverse dal vero, la casa e' disordinata "
        "con doppioni e strade rotte, l'agente non riesce e non sai se e' un guasto "
        "o un confine, e qualcosa doveva partire e non e' partito",
        _casa_finta(tmp_path))
    assert testo
    assert testo.count(" -> ") <= 2


def test_niente_percorsi_di_sal_ne_carte_scritte_nel_guardiano():
    codice = GUARDIANO.read_text(encoding="utf-8")
    assert "/Users/sal" not in codice, "percorso della casa di Sal in un file del prodotto"
    for carta in ("FONTI.md", "LIMITI.md", "COSA_E_ACCESO.md", "GUARDIANI.md",
                  "PASSAGGI.md", "CHECKUP.md", "MANUALI.md", "CONTATTO.md"):
        assert carta not in codice, f"{carta} cablata nel guardiano: la tabella non comanda piu'"


def test_una_riga_nuova_nella_tabella_e_subito_attiva(tmp_path):
    """La prova del fratello: la riga che il cliente aggiungera' domani."""
    casa = _casa_finta(tmp_path)
    pagina = casa / "assistenza" / "SINTOMI.md"
    pagina.write_text(
        pagina.read_text(encoding="utf-8")
        + "\n| Le notifiche non arrivano piu' sul telefono del proprietario "
          "| `ecosistema/NOTIFICHE.md`: chi avvisa, su quale telefono, con quale prova |\n",
        encoding="utf-8")
    assert "NOTIFICHE.md" in _lancia(
        "le notifiche non arrivano piu' sul telefono", casa)


def test_il_guardiano_e_installato_nelle_due_case_del_cliente():
    claude = json.loads((PRODOTTO / "templates" / "CLAUDE_SETTINGS.json").read_text(encoding="utf-8"))
    codex = json.loads((PRODOTTO / "templates" / "CODEX_HOOKS.json").read_text(encoding="utf-8"))
    acceso = json.dumps(claude, ensure_ascii=False) + json.dumps(codex, ensure_ascii=False)
    assert acceso.count("guardiano_carte.py") >= 2, "non e' acceso in tutte e due le case"
    for configurazione in (claude, codex):
        chiamate = [
            handler.get("command", "")
            for gruppo in configurazione["hooks"]["UserPromptSubmit"]
            for handler in gruppo["hooks"]
        ]
        assert any("guardiano_carte.py" in c for c in chiamate), (
            "acceso su un evento sbagliato: la carta serve quando arriva la richiesta")


def test_linstallazione_lo_porta_davvero_nella_casa():
    contratto = json.loads((PRODOTTO / "install_contract.json").read_text(encoding="utf-8"))
    comune = contratto["common"]
    voci = [t for t in comune["templates"] if t["template"] == "GUARDIANO_CARTE.py"]
    assert voci, "il guardiano non e' dichiarato fra i file comuni: nelle case non arriva"
    assert voci[0]["destination"] == ".agent/hooks/guardiano_carte.py"
    assert ".agent/hooks/guardiano_carte.py" in comune["required"], (
        "installazione senza guardiano = valida, e non deve esserlo")
