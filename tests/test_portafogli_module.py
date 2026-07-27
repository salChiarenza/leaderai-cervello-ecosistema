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
            (target / "AGENTS.md").write_text(
                (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
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
                "@AGENTS.md\n",
            )
            self.assertIn("Sistema Portafogli Core-Satellite", (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8"))
            self.assertIn("Portafoglio Modello", (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8"))
            root_map = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("### Registro delle stanze", root_map)
            self.assertIn("`Portafoglio Modello/AGENTS.md`", root_map)
            self.assertNotIn("## Stanza collegata:", root_map)
            self.assertNotIn("| Da censire |", root_map)

            custom = room / "METODO.md"
            custom.write_text("DECISIONE MARCO\n", encoding="utf-8")
            second = installer.install(target, "Portafoglio Modello")

            self.assertEqual(custom.read_text(encoding="utf-8"), "DECISIONE MARCO\n")
            self.assertEqual(
                (target / "AGENTS.md")
                .read_text(encoding="utf-8")
                .count("`Portafoglio Modello/AGENTS.md`"),
                1,
            )
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
            self.assertIn(
                "Sistema Portafogli Core-Satellite",
                (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Sistema Portafogli Core-Satellite",
                (target / "ecosistema" / "PROCESSI.md").read_text(encoding="utf-8"),
            )

    def test_new_skill_is_installed_only_when_named_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (target / ".claude").mkdir()
            (target / ".claude" / "README.md").write_text(
                "Claude attivo\n", encoding="utf-8"
            )

            installer.install(target, "Investimenti", skill_name="portafogli-azimut")

            skill = target / ".claude" / "skills" / "portafogli-azimut" / "SKILL.md"
            self.assertTrue(skill.exists())
            self.assertIn("name: portafogli-azimut", skill.read_text(encoding="utf-8"))
            self.assertFalse((target / ".claude" / "skills" / "gestisci-portafoglio").exists())

    def test_root_and_room_bridges_are_required_even_without_claude_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")

            installer.install(target, "Investimenti")

            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertEqual(
                (room / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertFalse((target / ".claude").exists())

    def test_repairs_wrong_root_bridge_with_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            wrong = "istruzioni indipendenti\n"
            (target / "CLAUDE.md").write_text(wrong, encoding="utf-8")

            installer.install(target, "Investimenti")

            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertEqual(
                (target / "CLAUDE.md.leaderai-backup").read_text(encoding="utf-8"),
                wrong,
            )

    def test_skill_requires_claude_readme_not_bridge_or_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"\.claude/README\.md"):
                installer.install(
                    target,
                    "Investimenti",
                    skill_name="portafogli-azimut",
                )

            (target / ".claude").mkdir()
            with self.assertRaisesRegex(ValueError, r"\.claude/README\.md"):
                installer.install(
                    target,
                    "Investimenti",
                    skill_name="portafogli-azimut",
                )

    def test_rejects_symlinked_room_parent_before_writing_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            target.mkdir()
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "Reparti").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "symlink"):
                installer.install(target, "Reparti/Investimenti", create_room=True)

            self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_existing_target_behind_symlinked_ancestor(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            outside = base / "Fuori"
            real_target = outside / "Casa"
            real_target.mkdir(parents=True)
            linked_parent = base / "Collegamento"
            linked_parent.symlink_to(outside, target_is_directory=True)
            target = linked_parent / "Casa"

            with self.assertRaisesRegex(ValueError, "antenata.*symlink"):
                installer.install(target, "Investimenti", create_room=True)

            self.assertEqual(list(real_target.iterdir()), [])

    def test_rejects_symlinked_skill_tree_before_writing_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (target / ".claude").mkdir()
            (target / ".claude" / "README.md").write_text(
                "# Claude attivo\n", encoding="utf-8"
            )
            (target / ".claude" / "skills").symlink_to(
                outside,
                target_is_directory=True,
            )

            with self.assertRaisesRegex(ValueError, "symlink"):
                installer.install(
                    target,
                    "Investimenti",
                    skill_name="portafogli-azimut",
                )

            self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_symlinked_root_agents_before_modifying_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            target.mkdir()
            outside.mkdir()
            outside_agents = outside / "AGENTS.md"
            outside_agents.write_text(
                (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (target / "AGENTS.md").symlink_to(outside_agents)

            with self.assertRaisesRegex(ValueError, "File operativo.*symlink"):
                installer.install(target, "Investimenti", create_room=True)

            self.assertNotIn(
                "Investimenti",
                outside_agents.read_text(encoding="utf-8"),
            )

    def test_rejects_symlinked_install_log_before_appending_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            (target / "ecosistema").mkdir(parents=True)
            (target / "logs").mkdir()
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            outside_log = outside / "install-log.md"
            outside_log.write_text("FUORI\n", encoding="utf-8")
            (target / "logs" / "install-log.md").symlink_to(outside_log)

            with self.assertRaisesRegex(ValueError, "File operativo.*symlink"):
                installer.install(target, "Investimenti", create_room=True)

            self.assertEqual(
                outside_log.read_text(encoding="utf-8"),
                "FUORI\n",
            )

    def test_rejects_broken_bridge_backup_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("copia vecchia\n", encoding="utf-8")
            (target / "CLAUDE.md.leaderai-backup").symlink_to(
                outside / "nuovo.md"
            )

            with self.assertRaisesRegex(ValueError, "Backup LeaderAI.*symlink"):
                installer.install(target, "Investimenti")

            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "copia vecchia\n",
            )

    def test_rejects_broken_managed_backup_symlink_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            managed = room / "PROCESSO.md"
            managed.write_text("personalizzato\n", encoding="utf-8")
            (room / "PROCESSO.md.leaderai-backup").symlink_to(
                outside / "nuovo.md"
            )

            with self.assertRaisesRegex(ValueError, "Backup LeaderAI.*symlink"):
                installer.install(
                    target,
                    "Investimenti",
                    update_managed=True,
                )

            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(
                managed.read_text(encoding="utf-8"),
                "personalizzato\n",
            )
            self.assertFalse((room / "CLAUDE.md").exists())

    def test_rejects_broken_skill_backup_symlink_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            outside = Path(tmp) / "Fuori"
            room = target / "Investimenti"
            skill_dir = target / ".claude" / "skills" / "portafogli-azimut"
            room.mkdir(parents=True)
            skill_dir.mkdir(parents=True)
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (target / ".claude" / "README.md").write_text(
                "# Claude attivo\n", encoding="utf-8"
            )
            skill = skill_dir / "SKILL.md"
            skill.write_text("name: vecchia\n", encoding="utf-8")
            (skill_dir / "SKILL.md.leaderai-backup").symlink_to(
                outside / "nuovo.md"
            )

            with self.assertRaisesRegex(ValueError, "Backup LeaderAI.*symlink"):
                installer.install(
                    target,
                    "Investimenti",
                    skill_name="portafogli-azimut",
                    update_managed=True,
                )

            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(skill.read_text(encoding="utf-8"), "name: vecchia\n")
            self.assertFalse((room / "CLAUDE.md").exists())

    def test_rejects_room_file_with_directory_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            (room / "PROCESSO.md").mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "File della stanza.*directory"):
                installer.install(target, "Investimenti")

            self.assertFalse((room / "CLAUDE.md").exists())

    def test_rejects_room_agents_directory_with_controlled_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            (room / "AGENTS.md").mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "File della stanza.*directory"):
                installer.install(target, "Investimenti")

    def test_second_bridge_repair_creates_a_distinct_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text(
                "ISTRUZIONI NUOVE CLIENTE\n",
                encoding="utf-8",
            )
            (target / "CLAUDE.md.leaderai-backup").write_text(
                "BACKUP VECCHIO\n",
                encoding="utf-8",
            )

            installer.install(target, "Investimenti")

            self.assertEqual(
                (target / "CLAUDE.md.leaderai-backup").read_text(encoding="utf-8"),
                "BACKUP VECCHIO\n",
            )
            self.assertEqual(
                (target / "CLAUDE.md.leaderai-backup.2").read_text(encoding="utf-8"),
                "ISTRUZIONI NUOVE CLIENTE\n",
            )
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )

    def test_second_managed_update_creates_a_distinct_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            room.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            managed = room / "PROCESSO.md"
            managed.write_text("VERSIONE NUOVA CLIENTE\n", encoding="utf-8")
            (room / "PROCESSO.md.leaderai-backup").write_text(
                "BACKUP VECCHIO\n",
                encoding="utf-8",
            )

            installer.install(
                target,
                "Investimenti",
                update_managed=True,
            )

            self.assertEqual(
                (room / "PROCESSO.md.leaderai-backup").read_text(encoding="utf-8"),
                "BACKUP VECCHIO\n",
            )
            self.assertEqual(
                (room / "PROCESSO.md.leaderai-backup.2").read_text(
                    encoding="utf-8"
                ),
                "VERSIONE NUOVA CLIENTE\n",
            )

    def test_second_skill_update_creates_a_distinct_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Casa"
            room = target / "Investimenti"
            skill_dir = target / ".claude" / "skills" / "portafogli-azimut"
            room.mkdir(parents=True)
            skill_dir.mkdir(parents=True)
            (target / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (target / ".claude" / "README.md").write_text(
                "# Claude attivo\n",
                encoding="utf-8",
            )
            skill = skill_dir / "SKILL.md"
            skill.write_text("name: versione-nuova\n", encoding="utf-8")
            (skill_dir / "SKILL.md.leaderai-backup").write_text(
                "name: backup-vecchio\n",
                encoding="utf-8",
            )

            installer.install(
                target,
                "Investimenti",
                skill_name="portafogli-azimut",
                update_managed=True,
            )

            self.assertEqual(
                (skill_dir / "SKILL.md.leaderai-backup").read_text(
                    encoding="utf-8"
                ),
                "name: backup-vecchio\n",
            )
            self.assertEqual(
                (skill_dir / "SKILL.md.leaderai-backup.2").read_text(
                    encoding="utf-8"
                ),
                "name: versione-nuova\n",
            )


if __name__ == "__main__":
    unittest.main()
