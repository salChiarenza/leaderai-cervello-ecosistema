import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def compact(text: str) -> str:
    return " ".join(text.split())


class TemporaryCloneGuidanceTest(unittest.TestCase):
    def test_install_uses_system_temp_not_client_profile_folder(self):
        raw = (ROOT / "INSTALLA_CON_AI.md").read_text(encoding="utf-8")
        text = compact(raw)

        required = [
            "cartella temporanea di sistema",
            "%TEMP%\\ecosistema-ai-standard",
            "/tmp/ecosistema-ai-standard",
            "Non crearla in Documenti, Desktop",
            "home/profilo utente",
            "deve essere eliminata prima del report finale",
            "Sul PC del cliente deve restare come lavoro visibile solo la cartella madre cliente",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

        forbidden_defaults = [
            "<home>/_ecosistema_setup/standard",
            "_ecosistema_setup/standard",
            "<home>/_leaderai_install",
        ]

        for phrase in forbidden_defaults:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, raw)

    def test_checkup_marks_technical_clone_as_cleanup_target(self):
        text = compact((ROOT / "CHECKUP.md").read_text(encoding="utf-8"))

        required = [
            "TECNICA-REPO",
            "cartella temporanea di",
            "%TEMP%\\ecosistema-ai-standard",
            "/tmp/ecosistema-ai-standard",
            "non devono restare",
            "cartelle tecniche LeaderAI visibili",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
