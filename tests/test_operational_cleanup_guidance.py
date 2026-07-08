import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OperationalCleanupGuidanceTest(unittest.TestCase):
    def test_client_template_requires_environment_cleanup(self):
        text = (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")

        required = [
            "Chiusura ambiente",
            "Email: archivia",
            "Browser: chiudi",
            "App: chiudi",
            "Handoff",
            "Non chiudere pagine personali",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checkup_and_installation_report_cleanup_state(self):
        checkup = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        install = (ROOT / "INSTALLA_CON_AI.md").read_text(encoding="utf-8")

        for phrase in [
            "stato di chiusura ambiente",
            "pagine web",
            "tab browser",
            "handoff nel report",
        ]:
            with self.subTest(file="CHECKUP.md", phrase=phrase):
                self.assertIn(phrase, checkup)

        for phrase in [
            "chiusura ambiente",
            "email/browser/tab/app",
            "superfici aperte da te",
            "chiudi le pagine/app aperte da te",
        ]:
            with self.subTest(file="INSTALLA_CON_AI.md", phrase=phrase):
                self.assertIn(phrase, install)

    def test_manifest_includes_operational_cleanup_as_standard(self):
        text = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")

        required = [
            "chiude l'ambiente operativo",
            "email/notifiche lavorate",
            "pagine web/tab/form/preview/login/app",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
