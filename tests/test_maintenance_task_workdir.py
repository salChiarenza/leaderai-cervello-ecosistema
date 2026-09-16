import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = "01 - Cervello - installazione e aggiornamento.md"


class MaintenanceTaskWorkdirTest(unittest.TestCase):
    """Caso reale 16/09/2026: la routine nata senza cartella di lavoro partiva da
    iCloud e il controllo FUORI DAL CERVELLO la fermava a ogni giro."""

    def _norm(self, name: str) -> str:
        return " ".join((ROOT / name).read_text(encoding="utf-8").lower().split())

    def test_installer_sets_mother_folder_as_task_workdir(self):
        doc = self._norm(DOC)
        self.assertIn("la routine ha come cartella di lavoro la cartella madre", doc)
        self.assertIn("fuori dal cervello la ferma a ogni giro", doc)
        self.assertIn(
            "con cartella di lavoro uguale alla cartella madre e un giro eseguito con esito letto",
            doc,
        )

    def test_maintainer_skill_and_checkup_carry_the_rule(self):
        self.assertIn(
            "la sua cartella di lavoro e' la cartella madre",
            self._norm("templates/MANUTENTORE_SKILL.md"),
        )
        self.assertIn(
            "abbia come cartella di lavoro la cartella madre",
            self._norm("CHECKUP.md"),
        )

    def test_agent_chat_hooks_read_the_root_file(self):
        # Difetto 0.6.29 segnalato dall'assistente di una cliente: i ganci
        # cercavano docs/AGENT_CHAT.md mentre il contratto lo installa in radice.
        sh = (ROOT / "templates" / "CHAT_AGGIORNAMENTI.sh").read_text(encoding="utf-8")
        py = (ROOT / "templates" / "GUARDIANO_NOTE_AGENTI.py").read_text(encoding="utf-8")
        self.assertNotIn("docs/AGENT_CHAT.md", sh)
        self.assertNotIn("docs/AGENT_CHAT.md", py)
        self.assertIn('CHAT="$CASA/AGENT_CHAT.md"', sh)
        self.assertIn('FILE = "AGENT_CHAT.md"', py)
        import json
        contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
        self.assertIn('"destination": "AGENT_CHAT.md"', json.dumps(contract, indent=2).replace("\n", "\n"))

    def test_version_is_aligned(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        doc = (ROOT / DOC).read_text(encoding="utf-8")
        self.assertIn(f"Versione corrente: `{version}`", doc)
        self.assertIn(f"## {version} - ", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
