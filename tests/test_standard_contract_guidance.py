import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StandardContractGuidanceTest(unittest.TestCase):
    def test_manifest_declares_the_repo_standard(self):
        text = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")

        required = [
            "standard di conformita'",
            "cartella viva del cliente",
            "caso reale",
            "repo `salChiarenza/leaderai-cervello-ecosistema`",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checkup_forces_comparison_against_manifest_and_template(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "repo GitHub `salChiarenza/leaderai-cervello-ecosistema`",
            "`MANIFEST.md` e' lo standard di conformita'",
            "`templates/AGENTS.md` e' il comportamento atteso",
            "cartella viva del cliente e' il caso reale",
            "non riparare a sentimento",
            "SCOSTAMENTI DALLO STANDARD",
            "STANDARD APPLICATO",
            "Modello email missione checkup",
            "Missione Ecosistema LeaderAI #N - Checkup",
            "Usa `MANIFEST.md` come standard di conformita'",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
