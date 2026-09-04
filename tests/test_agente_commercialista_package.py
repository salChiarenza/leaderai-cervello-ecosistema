import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "Agenti" / "Agente Commercialista"
FILES = (
    "LEGGIMI.md",
    "INSTALLA_CON_AI.md",
    "SCADENZARIO_FISCALE_TEMPLATE.md",
    "PROCEDURA.md",
    "SKILL.md",
    "AGENTE_CLAUDE.md",
    "AGENTE_CODEX.toml",
)


class AgenteCommercialistaPackageTest(unittest.TestCase):
    def test_package_is_complete_and_has_one_operational_source(self):
        for name in FILES:
            self.assertTrue((PACKAGE / name).is_file(), name)
        install = (PACKAGE / "INSTALLA_CON_AI.md").read_text(encoding="utf-8")
        self.assertIn("SCADENZARIO_FISCALE.md", install)
        self.assertIn(".agents/skills/agente-commercialista/SKILL.md", install)
        self.assertIn(".claude/agents/agente-commercialista.md", install)
        self.assertIn(".codex/agents/agente-commercialista.toml", install)

    def test_package_declares_activation_control_and_stop(self):
        text = (PACKAGE / "LEGGIMI.md").read_text(encoding="utf-8")
        for token in (
            "Attivazione",
            "Fonte",
            "Risultato",
            "Controllo",
            "Arresto",
            "Lancia l'Agente Commercialista",
        ):
            self.assertIn(token, text)

    def test_package_contains_no_sal_specific_data(self):
        combined = "\n".join(
            (PACKAGE / name).read_text(encoding="utf-8") for name in FILES
        )
        for forbidden in (
            "Sal Chiarenza",
            "Isabella Gattuso",
            "03366400806",
            "/Users/sal",
            "AGV",
        ):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
