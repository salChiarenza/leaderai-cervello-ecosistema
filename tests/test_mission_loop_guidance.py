import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MissionLoopGuidanceTest(unittest.TestCase):
    def test_checkup_contains_closed_mission_loop(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Protocollo missione chiusa",
            "MISSIONE",
            "ESECUZIONE",
            "AUTOCONTROLLO",
            "REPORT",
            "SAL_VERIFICA",
            "CONTINUA",
            "CHIUDI",
            "attiva un autocontrollo",
            "Non chiudere la missione dopo il primo report",
            "email lavorata è già archiviata",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_client_template_contains_closed_mission_loop(self):
        text = (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")

        required = [
            "Protocollo missioni LeaderAI",
            "AUTOCONTROLLO",
            "SAL_VERIFICA",
            "CONTINUA",
            "CHIUDI",
            "non decidere tu che e' finita",
            "Archivia** l'email-missione nello stesso giro",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
