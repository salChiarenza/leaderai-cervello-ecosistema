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

    def test_checkup_forces_extended_search_for_suspicious_leaderai_folders(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "ricerca estesa obbligatoria",
            "LeaderAI",
            "Leader AI",
            "leader ai",
            "leder ai",
            "_leaderai",
            "leaderai-cervello-ecosistema",
            "Downloads",
            "OneDrive",
            "PowerShell",
            "SOSPETTA",
            "nessuna cartella sospetta",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checkup_audits_room_graph_and_routes(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Censimento e rete delle stanze",
            "STANZA",
            "CAPACITA",
            "collegamenti a monte e collegamenti a valle",
            "ogni stanza sia raggiungibile",
            "PROPOSTA STRUTTURALE",
            "richiesta -> stanza -> fonte -> capacita'/processo -> output",
            "LEZIONE CANDIDATA",
            "VERSIONE METODO",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())


if __name__ == "__main__":
    unittest.main()
