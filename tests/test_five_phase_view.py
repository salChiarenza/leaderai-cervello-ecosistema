"""Contratto leggibile del percorso in cinque fasi."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_product_explains_common_infrastructure_and_optional_growth():
    required = {
        "MANIFEST.md": "stessa infrastruttura comune",
        "README.md": "contenuto su misura",
        "INSTALLA_CON_AI.md": "non installare tutto il catalogo",
        "CHECKUP.md": "Evoluzione quando serve",
        "EMAIL_CONSEGNA.md": "Percorso Ecosistema",
        "templates/AGENTS.md": "Passo 5 - Evoluzione quando serve",
    }
    for name, phrase in required.items():
        text = " ".join((ROOT / name).read_text(encoding="utf-8").split())
        assert phrase in text


def test_visible_path_exists_only_in_the_published_copy():
    view = ROOT / "Percorso Ecosistema"
    if (ROOT / ".git").exists():
        assert not view.exists()
        return
    assert sorted(path.name for path in view.glob("*.md")) == [
        "01 - Cervello.md",
        "02 - Censimento.md",
        "03 - Primo processo.md",
        "04 - Controllo e consegna.md",
        "05 - Evoluzione quando serve.md",
    ]
