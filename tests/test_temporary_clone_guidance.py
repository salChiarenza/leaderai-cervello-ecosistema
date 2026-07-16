import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def compact(text: str) -> str:
    return " ".join(text.split())


class SafeDeliveryGuidanceTest(unittest.TestCase):
    def test_new_install_reads_standard_without_cloning_by_default(self):
        raw = (ROOT / "INSTALLA_CON_AI.md").read_text(encoding="utf-8")
        text = compact(raw)

        required = [
            "repo ufficiale resta lo standard LeaderAI verificabile",
            "legge in sola lettura",
            "Il percorso standard non richiede clone della repo",
            "Python non serve nel percorso standard",
            "niente clone e niente esecuzione di codice scaricato",
            "leaderai_setup.py` resta un attrezzo LeaderAI",
            "solo dopo la sua autorizzazione esplicita",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

        forbidden_defaults = [
            "git clone https://github.com/salChiarenza/leaderai-cervello-ecosistema",
            "%TEMP%\\ecosistema-ai-standard",
            "/tmp/ecosistema-ai-standard",
        ]

        for phrase in forbidden_defaults:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, raw)

    def test_new_install_exposes_readable_static_templates(self):
        install = (ROOT / "INSTALLA_CON_AI.md").read_text(encoding="utf-8")
        required_templates = [
            "GITIGNORE.txt",
            "CODEX_README.md",
            "CLAUDE_README.md",
            "CLAUDE.md",
            "FONTI.md",
            "PROCESSI.md",
            "LIMITI.md",
            "INSTALL_LOG.md",
        ]

        for name in required_templates:
            with self.subTest(name=name):
                self.assertTrue((ROOT / "templates" / name).is_file())
                self.assertIn(f"templates/{name}", install)

    def test_report_is_local_before_external_send(self):
        text = compact((ROOT / "INSTALLA_CON_AI.md").read_text(encoding="utf-8"))
        required = [
            "Completa e collauda `REPORT_FINALE.md` nella cartella madre",
            "Autorizzi l'invio del report a sal@salchiarenza.ai?",
            "Solo dopo un si' esplicito, invia davvero il report",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

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

    def test_checkup_does_not_clone_by_default(self):
        raw = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        text = compact(raw)

        required = [
            "Se la repo e' gia' presente sul computer",
            "aggiornala",
            "usa GitHub come riferimento di lettura",
            "Crea un clone tecnico temporaneo solo dopo conferma esplicita",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

        forbidden = [
            "Aggiorna o clona la repo",
            "Se il clone non esiste ancora, clonalo",
        ]

        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, raw)


if __name__ == "__main__":
    unittest.main()
