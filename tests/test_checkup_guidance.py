import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckupGuidanceTest(unittest.TestCase):
    def test_checkup_is_name_agnostic_and_uses_life_signals(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Il nome non basta",
            "puo' chiamarsi in qualunque modo",
            "segnali di vita",
            "memory/MEMORY.md compilata",
            "logs/ con attivita'",
            "REPORT_FINALE.md compilato",
            "ecosistema/ASSET.md",
            "commit git",
            "file di lavoro recenti",
            "connettori provati",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
