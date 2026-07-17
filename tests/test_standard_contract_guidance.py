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

    def test_manifest_declares_safe_delivery_contract(self):
        raw = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")
        text = " ".join(raw.split())

        required = [
            "Contratto di consegna sicura",
            "fonte di sola lettura",
            "autorizzazione esplicita e separata",
            "non sono il percorso predefinito",
            "report viene prima creato e collaudato localmente",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_manifest_separates_fixed_frame_from_adaptive_rooms(self):
        text = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")

        required = [
            "Contratto architetturale adattivo",
            "Telaio universale",
            "Forma adattiva",
            "STANZA",
            "CAPACITA",
            "collegamenti a monte e a valle",
            "proposta strutturale",
            "LEZIONE CANDIDATA",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

        portfolio_contract = text.split("### Sistema Portafogli Core-Satellite", 1)[1]
        self.assertNotIn("crea `Costruzione Portafogli/`", portfolio_contract)

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
            "Oggetto: `Checkup Ecosistema`",
            "Usa `MANIFEST.md` come standard di conformita'",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
