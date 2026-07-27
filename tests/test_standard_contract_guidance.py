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

    def test_portfolio_cases_reuse_the_live_room_convention(self):
        text = (ROOT / "moduli" / "portafogli" / "CLIENTE_AGENTS.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Prima censisci come la stanza organizza gia' i casi reali", text)
        self.assertIn("Creala solo dopo approvazione", text)
        self.assertNotIn("Quando parte un caso reale, crea", text)

    def test_portfolio_mission_requires_owner_consent_before_email(self):
        text = (ROOT / "moduli" / "portafogli" / "INSTALLA_MODULO.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("autorizzazione esplicita all'invio", text)
        self.assertIn("PRONTO DA INVIARE", text)
        self.assertIn("Solo dopo il si'", text)

    def test_checkup_requires_a_bridge_instead_of_an_independent_copy(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        self.assertIn("ponte/import", text)
        self.assertIn("Una copia indipendente non e' conforme", text)
        self.assertNotIn("symlink o copia coerente", text)

    def test_portfolio_skill_repairs_unambiguous_broken_pointers(self):
        text = (ROOT / "moduli" / "portafogli" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("ripara il puntatore nei registri e provalo", text)
        self.assertIn("proprieta' e' ambigua", text)

    def test_installation_email_states_match_the_checkup(self):
        text = (ROOT / "INSTALLA_CON_AI.md").read_text(encoding="utf-8")

        self.assertIn("PRONTO DA INVIARE", text)
        self.assertIn("archivia l'email della missione nello stesso giro", text)
        self.assertNotIn("Dopo il report vai in `SAL_VERIFICA`", text)

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
