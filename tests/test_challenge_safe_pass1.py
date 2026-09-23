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


def test_la_ripresa_guarda_la_casa_vera_non_lo_stato_vecchio():
    # 23/09/2026, Giovanni Leto: dopo aver rimesso AGENTS.md e CLAUDE.md dalla copia,
    # lo stato diceva ancora di ripartire dal passo successivo: «se riparte da li'
    # senza guardare, si ritrova nello stesso pasticcio».
    guida = _piatto((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8"))
    messaggio = _piatto((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8").split("```text", 1)[1].split("```", 1)[0])
    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))

    assert "prima di ripartire ricontrolla sulla casa vera i passi segnati come fatti" in messaggio
    assert "dopo aver ricontrollato sulla casa vera i passi gia' segnati come fatti" in guida
    assert "prima di ripartire ricontrolla sulla casa vera i passi gia' fatti" in vecchia


def test_una_routine_gira_su_una_sola_ai():
    # Sal, 23/09/2026: «le routine vengono installate su tutte le AI... non va bene
    # doppia routine»: visto da lui e da Caterina Mencarini, capita a chi usa piu' AI.
    installatore = _piatto((ROOT / "01 - Cervello - installazione e aggiornamento.md").read_text(encoding="utf-8"))
    manutentore = _piatto((ROOT / "templates/MANUTENTORE_SKILL.md").read_text(encoding="utf-8"))
    acceso = _piatto((ROOT / "templates/COSA_E_ACCESO.md").read_text(encoding="utf-8"))

    assert "invoca la skill `manutentore-ecosistema`, su una sola ai" in installatore
    assert "mai tutte e due" in installatore
    assert "gli chiedi una volta su quale la vuole" in installatore
    assert "mai due routine per lo stesso lavoro, nemmeno su due ai diverse" in installatore
    assert "per motore o reparto" not in installatore

    assert "niente seconda automazione, nemmeno su un'altra ai" in manutentore
    assert "metti in pausa quella che non e' in tabella (non cancellarla)" in manutentore

    assert "| su quale ai |" in acceso
    assert "ogni cosa che parte da sola gira su una sola ai" in acceso
    assert "{{routine_ai}}" not in acceso


def _messaggio() -> str:
    guida = (ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8")
    return _piatto(guida.split("```text", 1)[1].split("```", 1)[0])


def test_l_aggiornamento_e_un_lavoro_con_un_risultato():
    # Sal, 23/09/2026: chi riceve le istruzioni deve interpretare il lavoro; «sappiamo
    # cosa deve costruire, sappiamo cosa deve evitare, sappiamo cosa deve portare a
    # termine». Lo stesso giorno due aggiornamenti veri erano andati storti per due
    # regole seguite alla lettera (uno fermo a meta', uno che aveva archiviato troppo).
    messaggio = _messaggio()
    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))

    for parte in ("da costruire:", "da evitare:", "finito quando:"):
        assert parte in messaggio
        assert f"**{parte}**" in vecchia
    assert "il come lo decidi tu" in messaggio
    assert "il come lo decidi tu" in vecchia
    assert "nel dubbio un file e' mio e resta com'e'" in messaggio
    assert "nel dubbio una cosa e' del proprietario e resta com'e'" in vecchia
    assert "scegli la strada che non perde niente di mio" in messaggio
    assert "scegli la strada che non perde niente" in vecchia
    assert "arriva in fondo" in messaggio


def test_prima_la_copia_alla_fine_il_confronto():
    # La rete la tiene il confronto dei fatti, non una regola: copia completa prima,
    # elenco dei file prima e dopo, copia rimessa se una cosa del proprietario cambia.
    messaggio = _messaggio()
    # Prova dal vivo del 23/09: una copia fatta come cartella sembrava una seconda casa.
    assert "fanne una copia completa in un archivio zip datato, fuori dalla casa" in messaggio
    assert "una cartella copiata sembrerebbe una seconda casa" in messaggio
    assert "l'elenco dei suoi file" in messaggio
    assert "rifai l'elenco e confrontalo" in messaggio
    assert "rimetti la copia e dimmelo" in messaggio

    pagina = (ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8")
    copia = pagina.index("**Copia completa, prima di tutto.**")
    prova = pagina.index("**Prova la base documentale.**")
    confronto = pagina.index("**Confronta e, se serve, torna indietro.**")
    tecnica = pagina.index("**Solo dopo, la tecnica vecchia.**")
    assert copia < prova < confronto < tecnica
    vecchia = _piatto(pagina)
    assert "l'elenco dei file della casa con la loro impronta" in vecchia
    assert "ripristina la copia del passo 1" in vecchia

    risultato = _piatto((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8").split("## Risultato corretto", 1)[1])
    assert "confrontando l'elenco dei file fatto all'inizio con quello finale" in risultato


def test_i_file_del_pacchetto_vecchio_non_fermano_l_aggiornamento():
    # P-067, 23/09/2026: fino al 21/09 il pacchetto si estraeva dentro la casa; il
    # contratto di allora e' rimasto in quelle case. La guida diceva «file senza blocco:
    # non lo sostituisce; conflitto: non inventa una fusione» e l'assistente si e'
    # fermato a meta' aggiornamento su un file nostro, chiedendo a Sal cosa fare.
    guida = _piatto((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8"))
    messaggio = _messaggio()
    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))

    for regola in ("senza blocco leaderai: non lo sostituisce", "non inventa una fusione"):
        assert regola not in guida
        assert regola not in vecchia
    assert (
        "i file di un pacchetto vecchio rimasti nella casa (install_contract.json, "
        "package_version) sono di leaderai, non miei" in messaggio
    )
    assert "non si aggiornano e non fermano il lavoro" in messaggio
    assert "non fermano l'aggiornamento" in guida
    assert "(`install_contract.json`, `package_version`) sono di leaderai" in vecchia


def test_la_casa_vecchia_si_riconosce_anche_senza_il_numero():
    # Una casa nata 0.6 e portata a una 0.7 di quei giorni non ha VERSION 0.6: e'
    # vecchia lo stesso, e resta vecchia anche dopo un tentativo fermo che ha gia'
    # scritto lo stato dell'installazione (23/09/2026, la prima casa vera).
    messaggio = _messaggio()
    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))
    assert "se trovi una casa con version piu' vecchia di 0.7.12 (per esempio 0.6.29, 0.7.6 o 0.7.9), oppure senza logs/install-state.json" in messaggio
    assert "anche se un tentativo di aggiornamento ha gia' scritto lo stato" in messaggio
    assert "`version` e' piu' vecchia di `0.7.12`" in vecchia
    assert "anche se un tentativo di aggiornamento ha gia' scritto lo stato" in vecchia


def test_quello_che_gira_non_si_ferma():
    # 23/09/2026: la pagina diceva di fermare «attivita' programmate, manutenzione e
    # guardiani» senza dire quali: in uno studio avrebbe fermato anche il giro della posta
    # del proprietario. La tecnica che funziona e serve resta fino al Passo 4.
    vecchia = _piatto((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8"))
    assert "ferma attivita' programmate" not in vecchia
    assert "i programmi e le attivita' del proprietario non si fermano" in vecchia
    assert "restano come sono se funzionano e servono al proprietario" in vecchia
    assert "quello che girava prima gira ancora" in vecchia
    assert "metti da parte, senza cancellarli, soltanto quelli rotti o che non usa nessuno" in vecchia


def test_il_consiglio_sulla_copia_arriva_con_le_sue_parole():
    # P-089, 23/09/2026: con il solo messaggio l'assistente consigliava un disco esterno
    # in 3 prove su 3, cioe' il posto tolto con P-063.
    messaggio = _piatto((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8").split("```text", 1)[1].split("```", 1)[0])
    assert "dentro una cartella online (onedrive, google drive o icloud) oppure di farne una copia ogni tanto. decidi tu." in messaggio
    assert "dammi il tuo consiglio" not in messaggio
    assert "sposta la casa, non copiarla, e aggiorna il percorso nel blocco leaderai-casa" in messaggio
