import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "moduli" / "portafogli"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


engine = load_module("portfolio_engine", MODULE / "portfolio_engine.py")
installer = load_module("installa_portafogli", MODULE / "installa_portafogli.py")


class PortfolioEngineTest(unittest.TestCase):
    def test_analysis_calculates_weights_delta_and_satellite_alert(self):
        holdings = engine.load_portfolio(MODULE / "DATI_PORTAFOGLIO_MODELLO.csv")
        rows = engine.analyze_portfolio(holdings, 5.0)

        self.assertEqual(len(rows), 2)
        self.assertAlmostEqual(sum(float(row["peso_attuale_pct"]) for row in rows), 100.0)
        satellite = next(row for row in rows if row["componente"] == "SATELLITE")
        self.assertEqual(satellite["alert"], "SOGLIA")
        self.assertGreater(float(satellite["movimento_da_riferimento_pct"]), 5.0)

    def test_target_on_disallowed_instrument_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "portfolio.csv"
            content = (MODULE / "DATI_PORTAFOGLIO_MODELLO.csv").read_text(encoding="utf-8")
            path.write_text(content.replace(",SI\n", ",NO\n", 1), encoding="utf-8")

            with self.assertRaisesRegex(engine.ValidationError, "fuori universo ammesso"):
                engine.load_portfolio(path)

    def test_backtest_requires_every_target_in_every_month(self):
        holdings = engine.load_portfolio(MODULE / "DATI_PORTAFOGLIO_MODELLO.csv")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "returns.csv"
            path.write_text(
                "data,strumento_id,rendimento_mensile_pct,fonte,data_fonte\n"
                "2026-05,CORE_A,0.5,Report,2026-06-05\n",
                encoding="utf-8",
            )
            target_ids = {item.instrument_id for item in holdings if item.target_pct > 0}
            with self.assertRaisesRegex(engine.ValidationError, "rendimenti mancanti"):
                engine.load_monthly_returns(path, target_ids)

    def test_backtest_outputs_complete_months(self):
        holdings = engine.load_portfolio(MODULE / "DATI_PORTAFOGLIO_MODELLO.csv")
        target_ids = {item.instrument_id for item in holdings if item.target_pct > 0}
        monthly = engine.load_monthly_returns(
            MODULE / "RENDIMENTI_MENSILI_MODELLO.csv", target_ids
        )
        rows = engine.run_backtest(holdings, monthly, "monthly-rebalanced")

        self.assertEqual([row["data"] for row in rows], ["2026-05", "2026-06"])
        self.assertTrue(all("drawdown_pct" in row for row in rows))


class PortfolioInstallerTest(unittest.TestCase):
    def test_installs_and_preserves_custom_files_on_second_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Marco Investimenti"
            (target / "ecosistema").mkdir(parents=True)
            (target / "logs").mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            room = target / "Portafoglio Modello"
            room.mkdir()
            (room / "AGENTS.md").write_text(
                "# Portafoglio Modello\n\n## Collegamenti\n", encoding="utf-8"
            )
            (target / "ecosistema" / "ASSET.md").write_text(
                "# Asset\n\n| Asset | Casa | Uso | Stato | Note |\n|---|---|---|---|---|\n",
                encoding="utf-8",
            )
            (target / "ecosistema" / "PROCESSI.md").write_text(
                "# Processi\n", encoding="utf-8"
            )

            first = installer.install(target, "Portafoglio Modello")
            self.assertTrue((room / "portfolio_engine.py").exists())
            self.assertFalse((target / "Costruzione Portafogli").exists())
            self.assertFalse((target / ".claude" / "skills" / "gestisci-portafoglio").exists())
            self.assertEqual(
                (room / "CLAUDE.md").read_text(encoding="utf-8"),
                "# CLAUDE.md\n\n@AGENTS.md\n",
            )
            self.assertIn("Sistema Portafogli Core-Satellite", (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8"))
            self.assertIn("Portafoglio Modello", (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8"))
            self.assertIn("Stanza collegata: Portafoglio Modello", (target / "AGENTS.md").read_text(encoding="utf-8"))

            custom = room / "METODO.md"
            custom.write_text("DECISIONE MARCO\n", encoding="utf-8")
            second = installer.install(target, "Portafoglio Modello")

            self.assertEqual(custom.read_text(encoding="utf-8"), "DECISIONE MARCO\n")
            self.assertGreater(len(first.created), 0)
            self.assertGreater(len(second.existing), 0)

    def test_new_room_requires_explicit_structural_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "--create-room"):
                installer.install(target, "Portafogli")

            installer.install(target, "Portafogli", create_room=True)
            self.assertTrue((target / "Portafogli" / "AGENTS.md").exists())

    def test_new_skill_is_installed_only_when_named_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")

            installer.install(target, "Investimenti", skill_name="portafogli-azimut")

            skill = target / ".claude" / "skills" / "portafogli-azimut" / "SKILL.md"
            self.assertTrue(skill.exists())
            self.assertIn("name: portafogli-azimut", skill.read_text(encoding="utf-8"))
            self.assertFalse((target / ".claude" / "skills" / "gestisci-portafoglio").exists())


if __name__ == "__main__":
    unittest.main()
