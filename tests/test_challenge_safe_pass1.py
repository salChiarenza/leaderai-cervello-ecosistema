import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_pass1_has_no_persistent_agent_changes():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    package = contract["client_package"]

    assert package["external_effects"] == []
    assert {rule["destination"] for rule in package["templates"]} == {
        "README.md",
        "memory/MEMORY.md",
        "AGENT_CHAT.md",
        "ecosistema/FONTI.md",
        "ecosistema/ASSET.md",
        "ecosistema/PROCESSI.md",
        "ecosistema/LIMITI.md",
        "ecosistema/SOGGETTI.md",
        "logs/install-log.md",
    }
    assert all(
        Path(rule["destination"]).suffix == ".md"
        for rule in package["templates"]
    )

    guide = (ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8").casefold()
    for forbidden in (
        "automemorydirectory",
        "~/.claude",
        "~/.codex",
        "non chiedere",
        "senza altre domande",
        "07:45",
    ):
        assert forbidden not in guide


def test_every_public_pass1_source_is_plain_markdown():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    for rule in contract["client_package"]["templates"]:
        source = ROOT / "templates" / rule["source"]
        assert source.is_file()
        assert source.suffix == ".md"
        assert not source.is_symlink()
