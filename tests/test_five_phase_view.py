"""Contratto leggibile del percorso in cinque fasi."""
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_product_explains_common_infrastructure_and_optional_growth():
    required = {
        "MANIFEST.md": "stessa infrastruttura comune",
        "README.md": "contenuto su misura",
        "01 - Cervello - installazione e aggiornamento.md": "non installare tutto il catalogo",
        "CHECKUP.md": "5 Collaudo e consegna",
        "EMAIL_CONSEGNA.md": "01 - Cervello - installazione e aggiornamento.md",
        "templates/AGENTS.md": "Dopo il Passo 5 - Prodotti quando servono",
    }
    for name, phrase in required.items():
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert phrase in text


def test_installation_does_not_create_a_second_set_of_phase_numbers():
    text = (ROOT / "01 - Cervello - installazione e aggiornamento.md").read_text(encoding="utf-8")
    assert "Operazione 1 - autodiagnosi" in text
    assert not re.search(r"\bFase \d", text)


def test_current_sources_do_not_keep_the_old_two_phase_taxonomy():
    for name in ("README.md", "MANIFEST.md", "templates/AGENTS.md", "templates/PROCESSI.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert not re.search(r"\bFase [12]\b", text), name
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "prime quattro" not in readme
    assert "la quinta aggiunge" not in readme


def test_census_skill_uses_the_visible_step_name():
    text = (ROOT / "templates/CENSITORE_PROCESSI_SKILL.md").read_text(encoding="utf-8")
    assert "Passo 2 Mappa del lavoro" in text
    assert "Passo 2 Censimento" not in text


def test_the_only_visible_instruction_also_handles_browser_users():
    text = (ROOT / "01 - Cervello - installazione e aggiornamento.md").read_text(encoding="utf-8")
    assert "Se usi l'AI solo nel browser" in text
    assert not (ROOT / "PRIMA_DI_INIZIARE.md").exists()


def test_visible_path_exists_only_in_the_published_copy():
    view = ROOT / "Percorso Ecosistema"
    if (ROOT / ".git").exists():
        assert not view.exists()
        return
    assert sorted(path.name for path in view.glob("*.md")) == [
        "02 - Mappa del lavoro.md",
        "03 - Primo processo.md",
        "04 - Gestione dell'ecosistema.md",
        "05 - Collaudo e consegna.md",
    ]
