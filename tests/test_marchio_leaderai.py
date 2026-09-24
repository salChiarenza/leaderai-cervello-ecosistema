"""La casa si presenta come LeaderAI: nome della cartella e marchio nei file (Sal, 23/09/2026)."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARCHIO = "<!-- LeaderAI · salchiarenza.ai -->"


def _pagine_del_passo1():
    contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
    for rule in contract["client_package"]["templates"]:
        source = ROOT / "templates" / rule["source"]
        if source.suffix == ".md" and source.name != "CLAUDE.md":
            yield source


def test_ogni_pagina_della_casa_nuova_porta_il_marchio_in_testa():
    pagine = list(_pagine_del_passo1())
    assert len(pagine) == 10
    for pagina in pagine:
        prima_riga = pagina.read_text(encoding="utf-8").splitlines()[0]
        assert prima_riga == MARCHIO, pagina.name


def test_il_ponte_claude_resta_una_riga_sola():
    ponte = (ROOT / "templates" / "passo1" / "CLAUDE.md").read_text(encoding="utf-8")
    assert ponte == "@AGENTS.md\n"


def test_la_casa_nuova_spiega_il_marchio_e_rispetta_i_documenti_del_proprietario():
    readme = (ROOT / "templates" / "passo1" / "README.md").read_text(encoding="utf-8")
    assert "## Il marchio LeaderAI" in readme
    assert "proprieta' del file" in readme
    assert "I documenti del proprietario restano come sono." in readme
    # P-100, 24/09/2026: un programma della casa che legge le pagine dalla prima
    # riga non deve rompersi sulla riga nascosta del marchio.
    assert "Un programma che legge le pagine della casa salta la riga nascosta del marchio in testa." in " ".join(readme.split())


def test_la_guida_propone_una_cartella_leaderai():
    guida = (ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8")
    assert "con il nome LeaderAI-" in guida
    assert "EcosistemaAI-" not in guida


def test_la_casa_vecchia_non_cambia_nome_e_il_marchio_resta_nei_documenti_nuovi():
    # Sal, 24/09/2026, caso Monica Cordaro (Santa Brigida): l'aggiornamento aveva
    # rinominato la cartella e marchiato 172 pagine e 44 script della sua casa,
    # rompendole (le sue schede Instagram leggevano dalla prima riga). Sulla casa
    # del cliente si consiglia, non si impone (P-099, P-100).
    pagina = (ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8")
    copia = pagina.index("**Copia completa, prima di tutto.**")
    passo1 = pagina.index("**Applica il Passo 1 corrente.**")
    marchio = pagina.index("**Il marchio resta nei documenti nuovi.**")
    nome = pagina.index("**Il nome della cartella non cambia.**")
    prova = pagina.index("**Prova la base documentale.**")
    assert copia < passo1 < marchio < nome < prova
    piatta = " ".join(pagina.split())
    assert "rinominarla non e' un passo di questo aggiornamento" in piatta
    assert "mai imporlo" in piatta
    assert "senza chiedere altro al proprietario" in piatta
    # Il registro git resta se il proprietario lo usa davvero (per esempio dal
    # telefono): non e' piu' un si' finale scontato.
    assert "il registro git resta se il proprietario lo usa" in piatta.casefold()
    assert "non li tocchi e non proponi nemmeno di toglierli" in piatta
    assert "con un no restano e la casa funziona lo stesso" in piatta
    assert "SERVE UN TUO PASSAGGIO" not in pagina
    assert "una sessione nuova riparte da li'" in pagina


def test_la_casa_vecchia_non_tocca_nomi_dei_programmi_ne_documenti_del_proprietario():
    pagina = " ".join((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8").split())
    assert MARCHIO in pagina
    assert "# LeaderAI · salchiarenza.ai" in pagina
    assert "Non rinominare la cartella interna `ecosistema/`" in pagina
    assert "Non toccare i documenti del proprietario" in pagina
    assert "Le app installate a parte, come Voce, non sono vecchia tecnica della casa" in pagina
    assert "riaccendi quello che hai messo in pausa" in pagina


def test_la_casa_esistente_non_tocca_la_riga_del_marchio_sulle_mie_pagine():
    # P-099/P-100, 24/09/2026: sulle pagine gia' del proprietario si tocca
    # soltanto un blocco delimitato leaderai:...:inizio/fine gia' esistente,
    # mai la riga del marchio in testa.
    guida = " ".join((ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8").split())
    assert "leaderai:...:inizio e fine che ci sono gia'." in guida
    assert "e la riga del marchio in testa" not in guida


def test_le_pagine_pubbliche_non_usano_casi_veri_come_esempio():
    for nome in ("CASA_VECCHIA.md", "PASSO1_CLIENTE.md"):
        testo = (ROOT / nome).read_text(encoding="utf-8").casefold()
        for vero in ("santabrigida", "santa brigida", "mindujo", "studio-sansone"):
            assert vero not in testo, (nome, vero)
