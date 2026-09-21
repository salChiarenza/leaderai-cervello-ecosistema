"""Lo sportello `assistenza/`: una casa sola per i guasti, e nessuna copia.

Sal, 21/09/2026: «nella casa del cliente deve esserci una cartella assistenza:
il posto dove l'assistente va quando ha un problema con la casa». Prima le tre
cose che servono li' vivevano sparse: i manuali dentro il registro delle fonti,
la tabella dei sintomi e il contatto in fondo alla carta che spiega com'e'
montata la casa. Nessuno le trovava col guasto in mano.

Il difetto tipico di questo prodotto (casi P-054 e P-055) non e' lo spostamento:
e' il puntatore rimasto indietro. Percio' qui non si controlla solo che la roba
sia arrivata, ma che nel prodotto non ne esista una seconda copia e che chi la
leggeva la legga dalla casa nuova.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

PRODOTTO = Path(__file__).resolve().parents[1]
TEMPLATES = PRODOTTO / "templates"
SPORTELLO = TEMPLATES / "assistenza"


def _modulo(nome: str, percorso: Path):
    spec = importlib.util.spec_from_file_location(nome, percorso)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


GUARDIANO_MANUALI = _modulo("_gm", TEMPLATES / "GUARDIANO_MANUALI.py")
GUARDIANO_CARTE = _modulo("_gc", TEMPLATES / "GUARDIANO_CARTE.py")

CARTE = ("SINTOMI.md", "MANUALI.md", "CONTATTO.md")


def _tutti_i_markdown() -> list[Path]:
    return [
        path
        for path in PRODOTTO.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    ]


def test_lo_sportello_porta_le_tre_carte_e_la_sua_mappa():
    assert (SPORTELLO / "AGENTS.md").is_file(), "lo sportello senza mappa non si spiega"
    assert (SPORTELLO / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"
    for carta in CARTE:
        assert (SPORTELLO / carta).is_file(), f"{carta} non c'e'"


def test_linstallazione_lo_porta_nella_casa_del_cliente():
    contratto = json.loads((PRODOTTO / "install_contract.json").read_text(encoding="utf-8"))
    comune = contratto["common"]
    destinazioni = {t["destination"] for t in comune["templates"]}
    for carta in ("AGENTS.md", "CLAUDE.md", *CARTE):
        rel = f"assistenza/{carta}"
        assert rel in destinazioni, f"{rel} non viene installato: nella casa non arriva"
        assert rel in comune["required"], f"installazione senza {rel} = valida, e non deve esserlo"


def test_i_manuali_stanno_in_un_posto_solo():
    """La tabella che il guardiano dei manuali sa leggere esiste una volta sola."""
    con_tabella = {
        path.relative_to(PRODOTTO).as_posix()
        for path in _tutti_i_markdown()
        if GUARDIANO_MANUALI._guide(path.read_text(encoding="utf-8"))
    }
    assert con_tabella == {"templates/assistenza/MANUALI.md"}


def test_la_tabella_dei_sintomi_sta_in_un_posto_solo():
    """Due tabelle sintomo -> carta = due risposte alla stessa domanda."""
    con_tabella = {
        path.relative_to(PRODOTTO).as_posix()
        for path in _tutti_i_markdown()
        if len(GUARDIANO_CARTE._carte(path.read_text(encoding="utf-8"))) >= 3
    }
    assert con_tabella == {"templates/assistenza/SINTOMI.md"}


def test_i_vecchi_posti_non_tengono_piu_la_roba_spostata():
    fonti = (TEMPLATES / "FONTI.md").read_text(encoding="utf-8")
    assert "## Manuali ufficiali degli strumenti" not in fonti
    assert "code.claude.com" not in fonti
    assert "assistenza/MANUALI.md" in fonti, "chi arriva qui deve sapere dove sono finiti"

    pagina = (TEMPLATES / "COME_E_MESSA_IN_PIEDI.md").read_text(encoding="utf-8")
    assert "## Dove si guarda, a seconda di cosa sta succedendo" not in pagina
    assert "info@salchiarenza.com" not in pagina
    assert "assistenza/SINTOMI.md" in pagina
    # cio' che resta qui e' la carta di com'e' montata la casa
    for pezzo in ("## Le quattro parti", "## Cosa vuol dire «sano»",
                  "## Come si ragiona su un guasto"):
        assert pezzo in pagina


def test_il_contatto_dellassistenza_non_e_cambiato_e_vive_li():
    contatto = (SPORTELLO / "CONTATTO.md").read_text(encoding="utf-8")
    assert "info@salchiarenza.com" in contatto


def test_i_due_guardiani_leggono_dalla_casa_nuova():
    manuali = (TEMPLATES / "GUARDIANO_MANUALI.py").read_text(encoding="utf-8")
    carte = (TEMPLATES / "GUARDIANO_CARTE.py").read_text(encoding="utf-8")
    assert 'os.path.join("assistenza", "MANUALI.md")' in manuali
    assert 'os.path.join("assistenza", "SINTOMI.md")' in carte
    assert "FONTI.md" not in manuali
    assert "COME_E_MESSA_IN_PIEDI" not in carte


def test_la_mappa_madre_manda_allo_sportello_e_resta_sotto_il_tetto():
    mappa = (TEMPLATES / "AGENTS.md").read_text(encoding="utf-8")
    assert "`assistenza/`" in mappa, "una cartella non dichiarata e' una cartella fuori mappa"
    dritto = " ".join(mappa.split())
    assert "Se qualcosa non va**, prima di fermarti o di dire «non funziona»: `assistenza/`" in dritto
    assert len(mappa.splitlines()) <= 350


def test_i_guardiani_della_struttura_accettano_lo_sportello():
    stanze = (TEMPLATES / "GUARDIANO_STANZE.sh").read_text(encoding="utf-8")
    assert "ecosistema|assistenza|memory|logs) continue" in stanze, (
        "senza questa riga lo sportello viene trattato come stanza business")
    assert "elemento non ammesso nello sportello assistenza" in stanze, (
        "lo sportello deve restare riservato come l'armadio")
    politica = (TEMPLATES / "ARCHIVE_POLICY.py").read_text(encoding="utf-8")
    assert '"ecosistema", "assistenza"' in politica, (
        "senza questo lo sportello viene accusato di non avere manutenzione")
