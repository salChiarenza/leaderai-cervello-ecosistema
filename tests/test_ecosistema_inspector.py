import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import ecosistema_inspector
import leaderai_setup


ROOM_ROW = (
    "| [Iscrizioni](app-iscrizioni) | Gestire iscrizioni | Radice | "
    "Documenti | Gestionale | Pratiche | App | `app-iscrizioni/AGENTS.md` |"
)


class EcosistemaInspectorTest(unittest.TestCase):
    def make_target(self, root: str, agent: str = "claude") -> Path:
        target = Path(root) / "EcosistemaAI-Test"
        leaderai_setup.run_setup(target, "Cliente Test", agent)
        return target

    def add_room_to_registry(self, target: Path, row: str = ROOM_ROW) -> None:
        agents = target / "AGENTS.md"
        text = agents.read_text(encoding="utf-8")
        placeholder = (
            "| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - |"
        )
        agents.write_text(text.replace(placeholder, row), encoding="utf-8")

    def create_valid_room(self, target: Path, name: str = "app-iscrizioni") -> None:
        room = target / name
        room.mkdir()
        template = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "STANZA_AGENTS.md"
        ).read_text(encoding="utf-8")
        replacements = {
            "{{room_name}}": "Iscrizioni",
            "{{room_purpose}}": "Gestire iscrizioni",
            "{{room_contents}}": "Pratiche",
            "{{room_sources}}": "Gestionale",
            "{{room_outputs}}": "Documenti",
            "{{room_business_source}}": "NON APPLICABILE: nessun generatore",
            "{{room_capabilities}}": "App",
            "{{room_upstream}}": "Radice",
            "{{room_downstream}}": "Documenti",
        }
        for key, value in replacements.items():
            template = template.replace(key, value)
        (room / "AGENTS.md").write_text(template, encoding="utf-8")
        (room / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")

    def codes(self, inspection: ecosistema_inspector.Inspection) -> set[str]:
        return {item.code for item in inspection.findings}

    def test_fresh_install_passes_mechanical_inspection(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertEqual(inspection.verdict, "PASSA")
            self.assertEqual(inspection.findings, [])
            settings = json.loads(
                (target / ".claude" / "settings.local.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                settings["autoMemoryDirectory"],
                str((target / "memory").absolute()),
            )
            tracked = subprocess.run(
                ["git", "ls-files"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertNotIn(".claude/settings.local.json", tracked)
            self.assertNotIn("REPORT_FINALE.md", tracked)

    def test_unclassified_generic_and_empty_folders_block_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "documenti").mkdir()
            app = target / "app-iscrizioni"
            app.mkdir()
            (app / "app.txt").write_text("viva\n", encoding="utf-8")

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("UNCLASSIFIED_DIR", self.codes(inspection))
            self.assertIn("GENERIC_DIR", self.codes(inspection))
            self.assertIn("EMPTY_DIR", self.codes(inspection))

    def test_declared_room_requires_complete_local_maps(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "app-iscrizioni").mkdir()
            self.add_room_to_registry(target)

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertIn("ROOM_AGENTS_MISSING", self.codes(inspection))
            self.assertIn("ROOM_CLAUDE_MISSING", self.codes(inspection))

    def test_valid_declared_room_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertEqual(inspection.verdict, "PASSA")

    def test_duplicate_room_purpose_and_loose_root_file_block_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target, "app-iscrizioni")
            self.create_valid_room(target, "segreteria")
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            placeholder = (
                "| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - |"
            )
            rows = (
                ROOM_ROW
                + "\n"
                + "| [Segreteria](segreteria) | Gestire iscrizioni | Radice | "
                "Documenti | Gestionale | Pratiche | App | `segreteria/AGENTS.md` |"
            )
            agents.write_text(text.replace(placeholder, rows), encoding="utf-8")
            (target / "VERSION").write_text("0.3.8\n", encoding="utf-8")

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertIn("DUPLICATE_ROOM_PURPOSE", self.codes(inspection))
            self.assertIn("UNOWNED_ROOT_FILE", self.codes(inspection))

    def test_missing_active_agent_skill_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            skill = target / ".claude" / "skills" / "ispettore-ecosistema"
            (skill / "SKILL.md").unlink()

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertIn("INSPECTOR_SKILL_MISSING", self.codes(inspection))

    def test_santa_brigida_regression_is_non_passa(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8").replace(
                    f"Versione standard applicata: `{leaderai_setup.STANDARD_VERSION}`.",
                    "Versione standard applicata: `0.3.0`.",
                ),
                encoding="utf-8",
            )
            (target / ".claude" / "settings.local.json").write_text(
                json.dumps(
                    {
                        "autoMemoryDirectory": str(
                            Path(tmp) / "memoria-claude-esterna"
                        )
                    }
                ),
                encoding="utf-8",
            )
            (target / "REPORT_FINALE.md").write_text(
                "# Report finale del 22/07\n\nGestionale: DA SCOPRIRE\n",
                encoding="utf-8",
            )
            documenti = target / "documenti"
            documenti.mkdir()
            (documenti / "guida.docx").write_text("derivato\n", encoding="utf-8")
            app = target / "app-iscrizioni"
            (app / "dati").mkdir(parents=True)
            (app / "PROGETTO.md").write_text(
                "# Progetto\n\n## Diario\n\n### 23/07/2026\n"
                "Lavoro.\n\n## PROSSIMO\nScadenza 30/09.\n",
                encoding="utf-8",
            )
            (app / "dati" / "config_posta.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            (app / "scheda_pdf.py").write_text(
                'GUIDA = "La famiglia deve seguire questa procedura completa '
                'per iscrivere ogni partecipante e consegnare tutti i documenti '
                'richiesti dalla scuola."\n',
                encoding="utf-8",
            )
            (app / "firma-scuola.png").write_bytes(b"test")
            self.add_room_to_registry(target)

            inspection = ecosistema_inspector.inspect_ecosystem(target)
            codes = self.codes(inspection)

            self.assertEqual(inspection.verdict, "NON PASSA")
            expected = {
                "STANDARD_VERSION_OUTDATED",
                "ROOM_AGENTS_MISSING",
                "ROOM_CLAUDE_MISSING",
                "UNCLASSIFIED_DIR",
                "GENERIC_DIR",
                "CLAUDE_MEMORY_DIVERGED",
                "STALE_REPORT",
                "CREDENTIAL_FILE_OUTSIDE_SECRETS",
                "BUSINESS_SOURCE_UNDECLARED",
                "BUSINESS_CONTENT_HARDCODED_RISK",
                "SENSITIVE_ASSET_OUTSIDE_PROTECTED",
                "SENSITIVE_ASSET_UNREGISTERED",
                "PROJECT_CONTROL_OUT_OF_ORDER",
            }
            self.assertTrue(expected.issubset(codes), expected - codes)

    def test_credential_path_in_git_history_requires_rotation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            config = target / "app-iscrizioni" / "dati" / "config_posta.json"
            config.parent.mkdir(parents=True)
            config.write_text("{}\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "-f", config.relative_to(target).as_posix()],
                cwd=str(target),
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-m",
                    "test config path",
                ],
                cwd=str(target),
                check=True,
                capture_output=True,
            )
            config.unlink()

            inspection = ecosistema_inspector.inspect_ecosystem(target)

            self.assertIn(
                "CREDENTIAL_EXPOSURE_NOT_EXCLUDED",
                self.codes(inspection),
            )


if __name__ == "__main__":
    unittest.main()
