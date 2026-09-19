import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARDIANO = ROOT / "templates" / "GUARDIANO_NOTE_AGENTI.py"
CALCO = ROOT / "templates" / "AGENT_CHAT.md"


def _parti_richieste() -> tuple[str, ...]:
    """Le parti che il guardiano pretende, lette dal guardiano stesso."""
    testo = GUARDIANO.read_text(encoding="utf-8")
    match = re.search(r"^RICHIESTI = \((.*?)\)$", testo, flags=re.MULTILINE | re.DOTALL)
    assert match, "RICHIESTI non trovato nel guardiano"
    return tuple(re.findall(r'"([^"]+)"', match.group(1)))


def _blocco_calco() -> str:
    """Il calco della nota pubblicato nel modello di AGENT_CHAT.md."""
    testo = CALCO.read_text(encoding="utf-8")
    match = re.search(r"## Calco nota\s*```text\s*(.*?)```", testo, flags=re.DOTALL)
    assert match, "calco nota non trovato nel modello"
    return match.group(1)


def _esegui(chat: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        casa = Path(tmp)
        (casa / "AGENT_CHAT.md").write_text(chat, encoding="utf-8")
        evento = {"cwd": str(casa), "tool_input": {"file_path": "AGENT_CHAT.md"}}
        return subprocess.run(
            [sys.executable, str(GUARDIANO)],
            input=json.dumps(evento),
            capture_output=True,
            text=True,
        )


def _chat_con_nota(nota: str) -> str:
    testo = CALCO.read_text(encoding="utf-8")
    return testo.replace("## Log\n", f"## Log\n\n{nota.strip()}\n", 1)


class GuardianoNoteCalcoTest(unittest.TestCase):
    """Lezione del 16/09/2026 (Studio Mencarini, P-038).

    Il guardiano separava le note su `## data` mentre il calco pubblicato nello
    stesso modello le apriva con `### [DATA/ORA]` e chiedeva parti diverse:
    scritta secondo il modello, la nota non veniva mai riconosciuta, il
    guardiano leggeva tutto il log come una nota sola e bloccava ogni modifica
    alla chat. Modello e guardiano si provano insieme, non a parole.
    """

    def test_the_template_carries_every_part_the_guardian_requires(self):
        calco = _blocco_calco()
        for parte in _parti_richieste():
            with self.subTest(parte=parte):
                self.assertIn(parte, calco)

    def test_a_note_written_as_the_template_prescribes_passes(self):
        nota = _blocco_calco()
        nota = nota.replace("[DATA/ORA]", "17/09/2026 (09:30)")
        nota = re.sub(r"\[[^\]]+\]", "una riga vera", nota)
        esito = _esegui(_chat_con_nota(nota))
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_a_note_missing_a_required_part_is_blocked(self):
        richieste = _parti_richieste()
        nota = _blocco_calco()
        nota = nota.replace("[DATA/ORA]", "17/09/2026 (09:30)")
        nota = re.sub(r"\[[^\]]+\]", "una riga vera", nota)
        nota = "\n".join(r for r in nota.splitlines() if richieste[-1] not in r)
        esito = _esegui(_chat_con_nota(nota))
        self.assertEqual(esito.returncode, 2)
        self.assertIn(richieste[-1], esito.stderr)


if __name__ == "__main__":
    unittest.main()
