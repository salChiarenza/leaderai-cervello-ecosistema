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
        "logs/install-state.json",
    }
    assert all(
        Path(rule["destination"]).suffix in {".md", ".json"}
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


def test_every_public_pass1_source_is_plain_text():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    for rule in contract["client_package"]["templates"]:
        source = ROOT / "templates" / rule["source"]
        assert source.is_file()
        assert source.suffix in {".md", ".json"}
        assert not source.is_symlink()


def test_public_contract_can_resume_and_merge_gmail_without_overwriting_client_files():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    package = contract["client_package"]
    rules = {rule["destination"]: rule for rule in package["templates"]}

    assert package["state_file"] == "logs/install-state.json"
    assert rules["logs/install-state.json"]["strategy"] == "state"
    assert rules["memory/MEMORY.md"]["ownership"] == "client"
    assert rules["ecosistema/FONTI.md"]["ownership"] == "client"
    assert rules["ecosistema/FONTI.md"]["managed_blocks"] == [
        {
            "id": "gmail-multiple-accounts",
            "start": "<!-- leaderai:gmail-multiple-accounts:inizio -->",
            "end": "<!-- leaderai:gmail-multiple-accounts:fine -->",
        }
    ]

    state = json.loads(
        (ROOT / "templates" / "passo1" / "INSTALL_STATE.json").read_text(
            encoding="utf-8"
        )
    )
    assert state["status"] == "NOT_STARTED"
    assert state["next_step"] == "inspect_target"


def test_package_does_not_claim_completion_before_the_final_state():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    combined = "\n".join(
        (ROOT / "templates" / rule["source"]).read_text(encoding="utf-8")
        for rule in contract["client_package"]["templates"]
    ).casefold()

    assert "passo 1 completato" not in combined
