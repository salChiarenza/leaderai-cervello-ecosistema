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
    pagina = " ".join((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8").split())
    assert "`CLAUDE.md` resta la sola riga `@AGENTS.md`" in pagina


def test_la_casa_nuova_spiega_il_marchio_e_rispetta_i_documenti_del_proprietario():
    readme = (ROOT / "templates" / "passo1" / "README.md").read_text(encoding="utf-8")
    assert "## Il marchio LeaderAI" in readme
    assert "proprieta' del file" in readme
    assert "I documenti del proprietario restano come sono." in readme


def test_la_guida_propone_una_cartella_leaderai():
    guida = (ROOT / "PASSO1_CLIENTE.md").read_text(encoding="utf-8")
    assert "con il nome LeaderAI-" in guida
    assert "EcosistemaAI-" not in guida


def test_la_casa_vecchia_cambia_nome_con_un_solo_gesto_dopo_la_copia():
    pagina = (ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8")
    copia = pagina.index("**Copia completa, prima di tutto.**")
    nome = pagina.index("**Dai alla casa il nome LeaderAI.**")
    passo1 = pagina.index("**Applica il Passo 1 corrente.**")
    marchio = pagina.index("**Metti il marchio LeaderAI.**")
    prova = pagina.index("**Prova la base documentale.**")
    # 23/09/2026, prove dal vivo: con il nome cambiato prima del Passo 1 servivano due
    # gesti (rinomina e poi una chat nuova per la prova). Ora la chat riaperta dopo
    # la rinomina e' la chat della prova: un gesto solo.
    assert copia < passo1 < marchio < nome < prova
    assert "l'unico che gli chiedi" in " ".join(pagina.split())
    assert "la prova si fa li', senza chiedere altro al proprietario" in " ".join(pagina.split())
    # Stessa prova dal vivo: il registro git chiesto come secondo gesto teneva
    # l'aggiornamento aperto. Ora e' un si' finale e lo cancella l'assistente.
    assert "il registro git si toglie alla fine, e non tiene aperto il lavoro" in " ".join(pagina.split()).casefold()
    assert "con il suo si' li cancelli tu" in " ".join(pagina.split())
    assert "SERVE UN TUO PASSAGGIO" in pagina
    assert "scrivimi: continua" in pagina
    assert "una sessione nuova riparte da li'" in pagina
    assert "come si chiama la casa" in pagina


def test_la_casa_vecchia_non_tocca_nomi_dei_programmi_ne_documenti_del_proprietario():
    pagina = " ".join((ROOT / "CASA_VECCHIA.md").read_text(encoding="utf-8").split())
    assert MARCHIO in pagina
    assert "# LeaderAI · salchiarenza.ai" in pagina
    assert "Non rinominare la cartella interna `ecosistema/`" in pagina
    assert "Non toccare i documenti del proprietario" in pagina
    assert "Le app installate a parte, come Voce, non sono vecchia tecnica della casa" in pagina
    assert "riaccendi quello che hai messo in pausa" in pagina


def test_le_pagine_pubbliche_non_usano_casi_veri_come_esempio():
    for nome in ("CASA_VECCHIA.md", "PASSO1_CLIENTE.md"):
        testo = (ROOT / nome).read_text(encoding="utf-8").casefold()
        for vero in ("santabrigida", "santa brigida", "mindujo", "studio-sansone"):
            assert vero not in testo, (nome, vero)
