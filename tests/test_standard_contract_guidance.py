import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StandardContractGuidanceTest(unittest.TestCase):
    def test_client_package_exposes_official_learning_links(self):
        expected = [
            "https://code.claude.com/docs/en/overview",
            "https://learn.chatgpt.com/docs",
            "https://openai.com/it-IT/academy/codex-for-work/",
        ]
        surfaces = [
            ROOT / "README.md",
            ROOT / "MANIFEST.md",
            ROOT / "CHECKUP.md",
            ROOT / "templates" / "FONTI.md",
            ROOT / "templates" / "ISPETTORE_SKILL.md",
        ]

        for surface in surfaces:
            text = surface.read_text(encoding="utf-8")
            for url in expected:
                with self.subTest(surface=surface.name, url=url):
                    self.assertIn(url, text)

    def test_manifest_declares_the_current_standard(self):
        text = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")

        required = [
            "standard di conformita'",
            "cartella viva del cliente",
            "caso reale",
            "Ecosistema Base",
            "GitHub non entra",
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
            "GitHub non entra nel percorso cliente",
            "non vengono creati cloni tecnici",
            "La conferma finale vive nel messaggio conclusivo",
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
            "responsabilita' business",
            "`Portafoglio Modello`",
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
        self.assertIn("Dopo il si'", text)
        self.assertIn("chiudi localmente", text)

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

        self.assertIn("zero aggiornamenti intermedi", text)
        self.assertIn("archivia l'email della missione", text.lower())
        self.assertIn("DA DECIDERE IN CALL", text)
        self.assertNotIn("PRONTO DA INVIARE", text)

    def test_checkup_forces_comparison_against_manifest_and_template(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Ecosistema Base su Google Drive e' lo standard LeaderAI corrente",
            "`MANIFEST.md` e' lo standard di conformita'",
            "`templates/AGENTS.md` e' il comportamento atteso",
            "cartella viva del cliente e' il caso reale",
            "non riparare a sentimento",
            "SCOSTAMENTI DALLO STANDARD",
            "STANDARD APPLICATO",
            "Modello email missione checkup",
            "Oggetto: `Checkup Ecosistema`",
            "Usa `MANIFEST.md` come standard di conformita'",
            "GitHub conserva soltanto il backup",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
