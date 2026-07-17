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
            "autorizzazione esplicita",
            "PRONTO DA INVIARE",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_client_template_contains_closed_mission_loop(self):
        text = (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")
        processes = (ROOT / "templates" / "PROCESSI.md").read_text(encoding="utf-8")

        required = [
            "Missioni da LeaderAI",
            "Il protocollo completo vive in `ecosistema/PROCESSI.md`",
            "AUTOCONTROLLO",
            "SAL_VERIFICA",
            "CONTINUA",
            "CHIUDI",
            "l'agente non decide da solo",
            "Archivia nello stesso giro",
            "autorizzazione esplicita",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

        self.assertIn("Protocollo missioni LeaderAI", processes)
        self.assertIn("MISSIONE -> ESECUZIONE -> AUTOCONTROLLO", processes)


if __name__ == "__main__":
    unittest.main()
