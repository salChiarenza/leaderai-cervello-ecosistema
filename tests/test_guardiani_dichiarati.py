"""Ogni guardiano ha la sua riga in chiaro, e l'elenco si installa in ogni casa.

Caso vero del 17/09/2026. Sal: «sei il mio grande guardiano, che vale sia per
Claude, sia per Codex, sia per certi GPT, sia per qualsiasi AI che usa il mio
sistema» e «la tua cosa di scrivere fogli su fogli verranno ignorati».

Percio': i guardiani non si spiegano a voce e non vivono in un foglio a parte.
Sono programmi che si installano da soli dove il motore li sa eseguire, piu' un
elenco unico - `templates/GUARDIANI.md` - che il contratto mette in ogni casa e
che vale come regola per gli assistenti che non eseguono programmi.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PRODOTTO = Path(__file__).resolve().parents[1]
ELENCO = PRODOTTO / "templates" / "GUARDIANI.md"
CONTRATTO = PRODOTTO / "install_contract.json"

# il programma che fa rispettare la regola -> la riga che la dice a chi legge
GUARDIANI = {
    "GUARDIANO_DATI_VERIFICATI.py": "Dati verificati",
    "GUARDIANO_DOPPIONI.py": "Doppioni",
    "GUARDIANO_EMAIL_OPERATIVA.py": "Email operativa",
    "GUARDIANO_MEMORIA.py": "Memoria",
    "GUARDIANO_MANUALI.py": "Manuali",
    "GUARDIANO_NOTE_AGENTI.py": "Note fra assistenti",
    "GUARDIANO_TURNO.py": "Un blocco per turno",
    "GUARDIANO_STANZE.sh": "Stanze",
    "BACKUP_CASA.py": "Copia di sicurezza",
    "CHAT_AGGIORNAMENTI.sh": "Note in arrivo",
    "ARCHIVE_POLICY.py": "Archivi protetti",
}


def _righe() -> dict[str, tuple[str, str]]:
    righe = {}
    for riga in ELENCO.read_text(encoding="utf-8").splitlines():
        riga = riga.strip()
        if not riga.startswith("|") or riga.startswith("|---") or "Cosa impedisce" in riga:
            continue
        pezzi = [p.strip() for p in riga.strip("|").split("|")]
        if len(pezzi) == 3:
            righe[pezzi[0]] = (pezzi[1], pezzi[2])
    return righe


def test_ogni_guardiano_del_prodotto_ha_la_sua_riga():
    righe = _righe()
    for programma, nome in GUARDIANI.items():
        assert (PRODOTTO / "templates" / programma).is_file(), f"{programma} non c'e' piu'"
        assert nome in righe, f"{programma} gira senza riga nell'elenco: chi legge non lo sa"


def test_nessuna_riga_promette_un_guardiano_che_non_esiste():
    nomi = set(GUARDIANI.values())
    for nome in _righe():
        assert nome in nomi, f"la riga «{nome}» non ha un programma dietro"


def test_ogni_riga_dice_cosa_impedisce_e_quando_scatta():
    for nome, (impedisce, quando) in _righe().items():
        assert len(impedisce) > 20, f"«{nome}» non dice cosa impedisce"
        assert len(quando) > 8, f"«{nome}» non dice quando scatta"


def test_il_contratto_installa_lelenco_in_ogni_casa():
    contratto = json.loads(CONTRATTO.read_text(encoding="utf-8"))
    comune = contratto["common"]
    voci = [t for t in comune["templates"] if t["template"] == "GUARDIANI.md"]
    assert voci, "l'elenco non e' dichiarato fra i file comuni: nelle case non arriva"
    assert voci[0]["destination"] == "ecosistema/GUARDIANI.md"
    assert "ecosistema/GUARDIANI.md" in comune["required"], "installazione senza elenco = valida, e non deve esserlo"


def test_lelenco_parla_anche_agli_assistenti_senza_programmi():
    testo = ELENCO.read_text(encoding="utf-8")
    assert "non eseguono programmi" in testo
    assert "queste righe sono la regola" in testo


# --- 19/09/2026, caso Paolo Buro nella casa di Sal: sapere non basta, serve
# che qualcuno ti chiami. Nella casa di Sal un guardiano aggiornato era rimasto
# senza richiamo e non partiva; qui la stessa famiglia riguarda i due motori.

# Il guardiano che scatta su un evento dell'assistente -> come si chiama il suo
# programma dentro le impostazioni. Restano fuori i tre che nessun evento chiama:
# la copia di sicurezza (routine giornaliera) e le due librerie usate dagli altri
# guardiani, «Un blocco per turno» e «Archivi protetti».
GUARDIANI_CON_EVENTO = {
    "Dati verificati": "guardiano_dati_verificati.py",
    "Doppioni": "guardiano_doppioni.py",
    "Email operativa": "guardiano_email_operativa.py",
    "Memoria": "guardiano_memoria.py",
    "Note fra assistenti": "guardiano_note_agenti.py",
    "Note in arrivo": "chat_aggiornamenti.sh",
    "Stanze": "guardiano_stanze.sh",
    "Manuali": "guardiano_manuali.py",
}

IMPOSTAZIONI = {
    "Claude Code": "CLAUDE_SETTINGS.json",
    "Codex": "CODEX_HOOKS.json",
}


def _programmi_richiamati(nome_template: str) -> str:
    """Tutti i comandi che quelle impostazioni eseguono, in un testo solo."""
    configurazione = json.loads(
        (PRODOTTO / "templates" / nome_template).read_text(encoding="utf-8")
    )
    comandi = []
    for gruppi in configurazione.get("hooks", {}).values():
        for gruppo in gruppi:
            comandi += [h.get("command", "") for h in gruppo.get("hooks", [])]
    return " ".join(comandi)


def test_ogni_guardiano_e_chiamato_in_tutte_e_due_le_case():
    """L'elenco promette che i guardiani valgono per Claude Code e per Codex.

    Se le impostazioni di un motore non li richiamano, in quella casa il
    guardiano e' installato ma spento - e l'elenco stesso dice che questa e' la
    cosa piu' pericolosa, perche' sembra acceso.
    """
    for motore, nome_template in IMPOSTAZIONI.items():
        richiamati = _programmi_richiamati(nome_template)
        for guardiano, programma in GUARDIANI_CON_EVENTO.items():
            assert programma in richiamati, (
                f"{motore}: «{guardiano}» si installa ma niente lo chiama "
                f"({programma} non compare nelle impostazioni)"
            )


def test_lelenco_dice_come_si_prova_dopo_linstallazione():
    testo = ELENCO.read_text(encoding="utf-8")
    assert re.search(r"metti un file .*e chiedi all'assistente di chiudere il lavoro", testo, re.S)
    assert "Deve fermarsi." in testo
