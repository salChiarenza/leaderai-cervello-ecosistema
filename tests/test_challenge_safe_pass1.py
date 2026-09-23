import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_pass1_has_no_persistent_agent_changes():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    package = contract["client_package"]

    assert package["external_effects"] == []
    assert {rule["destination"] for rule in package["templates"]} == {
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
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


def _piatto(testo: str) -> str:
    return " ".join(testo.split()).casefold()


def test_la_casa_si_cerca_su_tutto_il_computer_prima_di_scrivere():
    # P-087, 23/09/2026: la guida diceva «monta la casa in questa cartella» e
    # decideva guardando solo la cartella aperta: un assistente aperto da iCloud o
    # da una cartella nuova non vedeva la casa vera (famiglia P-053).
    guida = (ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8")
    messaggio = _piatto(guida.split("```text", 1)[1].split("```", 1)[0])

    assert "in questa cartella" not in messaggio
    assert "cartella che deve contenere" not in _piatto(guida)
    ricerca = messaggio.index("prima di scrivere qualsiasi cosa cerca la mia casa")
    assert ricerca < messaggio.index("scarica cervello.zip")
    assert "controlla comunque tutto il computer" in messaggio
    assert "non contano le cartelle nel cestino" in messaggio
    for posto in ("icloud drive", "google drive", "onedrive"):
        assert posto in messaggio[ricerca:]
    assert "non dal nome" in messaggio
    assert "e il pacchetto scaricato (ha package_version" in messaggio
    assert "una casa sola" in messaggio
    assert "aggiorni quella dov'e', anche se mi hai aperto altrove" in messaggio
    assert "se ne trovi piu' di una, non ne tocchi nessuna" in messaggio


def test_la_casa_si_sposta_non_si_copia():
    guida = _piatto((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8"))
    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))

    assert "ci sposta la casa, non la copia" in guida
    assert "una sola casa su tutto il computer" in guida
    assert "la sposti, non la copi" in vecchia
    assert "la casa si sposta, non si copia" in vecchia


def test_ogni_chat_sa_dov_e_la_casa():
    # Sal, 23/09/2026: «da oggi in poi l'ecosistema e' la casa di tutto»: lo
    # dicono le istruzioni generali che l'assistente legge in ogni chat.
    # La richiesta sta nel messaggio che incolla la persona, non nel pacchetto
    # scaricato: il 16/09 le modifiche persistenti chieste dal documento
    # facevano bloccare l'installazione a Claude.
    guida = (ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8")
    messaggio = guida.split("```text", 1)[1].split("```", 1)[0]
    piatto = _piatto(messaggio)

    assert "<!-- LEADERAI-CASA:inizio -->" in messaggio
    assert "<!-- LEADERAI-CASA:fine -->" in messaggio
    assert "istruzioni generali, quelle che leggi all'inizio di ogni chat in qualunque cartella" in piatto
    assert "e' la casa di tutto il mio lavoro" in piatto
    assert "se questa chat e' aperta altrove, leggi e scrivi nella casa" in piatto
    assert "sostituiscilo con questo" in piatto
    assert "se per scriverlo ti serve il mio permesso, chiedimelo" in piatto
    assert "rileggi il file e controlla che il blocco ci sia" in piatto
    assert "il blocco leaderai-casa nelle istruzioni generali dell'assistente, riletto" in _piatto(guida)
    assert "fuori dal cervello" not in piatto

    contratto = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    assert contratto["client_package"]["external_effects"] == []

    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))
    assert "resta soltanto il blocco leaderai-casa" in vecchia


def test_la_casa_non_e_muta():
    # P-083, 23/09/2026: Giovanni Leto, casa aggiornata senza AGENTS.md e CLAUDE.md:
    # una chat nuova aperta nella casa non sapeva niente. Sal: «quando installiamo
    # l'ecosistema non venivano corretti i file di Claude, GPT o Codex».
    contratto = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    regole = {r["destination"]: r for r in contratto["client_package"]["templates"]}
    for nome in ("AGENTS.md", "CLAUDE.md"):
        assert regole[nome]["strategy"] == "create"
        assert regole[nome]["ownership"] == "client"

    agents = _piatto((ROOT / "templates/passo1/AGENTS.md").read_text(encoding="utf-8"))
    assert "e' la casa di tutto il lavoro" in agents
    assert "`readme.md`" in agents and "`memory/memory.md`" in agents
    assert (ROOT / "templates/passo1/CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"

    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))
    assert "`agents.md` e `claude.md` della casa non si archiviano mai" in vecchia
