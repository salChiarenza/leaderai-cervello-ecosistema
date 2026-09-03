import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "moduli" / "portafogli"


def load_installer():
    path = MODULE / "installa_portafogli.py"
    spec = importlib.util.spec_from_file_location("financial_gate_installer", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


installer = load_installer()


class FinancialVerificationContractTest(unittest.TestCase):
    def test_skill_triggers_on_numbers_and_instrument_status(self):
        skill = (MODULE / "SKILL.md").read_text(encoding="utf-8")

        for marker in (
            "numeri",
            "rendimenti",
            "fondi",
            "ISIN",
            "stato corrente",
            "collocabilita",
            "VERIFICA_FINANZIARIA.md",
            "ESITO SOSPESO",
        ):
            self.assertIn(marker, skill)

    def test_gate_requires_primary_evidence_and_distinct_availability(self):
        gate = (MODULE / "VERIFICA_FINANZIARIA.md").read_text(encoding="utf-8")

        for marker in (
            "fonte primaria",
            "data/ora della verifica",
            "ATTIVO",
            "CHIUSO A NUOVE SOTTOSCRIZIONI",
            "INCORPORATO",
            "LIQUIDATO",
            "NON VERIFICATO",
            "disponibilità effettiva nell'universo collocabile",
            "portfolio_engine.py",
            "evidenze contrarie",
            "PASSA",
            "ESITO SOSPESO",
        ):
            self.assertIn(marker, gate)

    def test_process_blocks_client_report_until_gate_passes(self):
        process = (MODULE / "PROCESSO.md").read_text(encoding="utf-8")
        report = (MODULE / "REPORT_INTERNO_MODELLO.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("PASSA - PRONTO AI CALCOLI", process)
        self.assertIn("ESITO SOSPESO", process)
        self.assertIn("il gate finanziario è `PASSA`", process)
        self.assertIn("Gate verifica finanziaria", report)
        self.assertIn("Identità, stato e collocabilità", report)

    def test_installer_delivers_gate_and_auto_triggering_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (target / ".claude").mkdir()
            (target / ".claude" / "README.md").write_text(
                "# Claude attivo\n", encoding="utf-8"
            )

            installer.install(
                target,
                "Investimenti",
                skill_name="portafoglio-cliente",
            )

            installed_gate = room / "VERIFICA_FINANZIARIA.md"
            installed_skill = (
                target
                / ".claude"
                / "skills"
                / "portafoglio-cliente"
                / "SKILL.md"
            )
            self.assertTrue(installed_gate.is_file())
            self.assertIn("ESITO SOSPESO", installed_gate.read_text(encoding="utf-8"))
            self.assertIn(
                "name: portafoglio-cliente",
                installed_skill.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "numeri, prezzi, percentuali",
                installed_skill.read_text(encoding="utf-8"),
            )

    def test_versions_and_public_contract_are_updated(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "0.6.9")
        self.assertEqual((MODULE / "VERSION").read_text().strip(), "0.3.0")
        self.assertIn(
            "VERIFICA_FINANZIARIA.md",
            (ROOT / "MANIFEST.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "verifica automatica di numeri",
            (ROOT / "README.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
