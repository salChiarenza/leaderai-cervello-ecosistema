import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import ecosistema_inspector
import leaderai_setup


ROOM_ROW = (
    "| [Iscrizioni](app-iscrizioni) | Gestire iscrizioni | Radice | "
    "Documenti | Gestionale | Pratiche | App | `app-iscrizioni/AGENTS.md` | "
    "Amministratore di settore Iscrizioni | Boss dell'Ecosistema |"
)


class EcosistemaInspectorTest(unittest.TestCase):
    def make_target(self, root: str, agent: str = "claude") -> Path:
        target = Path(root) / "EcosistemaAI-Test"
        self.claude_user_settings = Path(root) / "claude-user-settings.json"
        leaderai_setup.run_setup(
            target,
            "Cliente Test",
            agent,
            claude_user_settings_path=(
                self.claude_user_settings
                if agent in {"claude", "both"}
                else None
            ),
        )
        if agent == "codex":
            self.claude_user_settings.write_text("{}\n", encoding="utf-8")
        return target

    def inspect(self, target: Path) -> ecosistema_inspector.Inspection:
        return ecosistema_inspector.inspect_ecosystem(
            target,
            claude_user_settings_path=self.claude_user_settings,
        )

    def add_room_to_registry(self, target: Path, row: str = ROOM_ROW) -> None:
        agents = target / "AGENTS.md"
        text = agents.read_text(encoding="utf-8")
        placeholder = (
            "| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - | "
            "Da assegnare | Boss dell'Ecosistema |"
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
            "{{room_business_responsibility}}": (
                "Mantiene lo stato delle pratiche e le decisioni sulle iscrizioni"
            ),
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

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "PASSA")
            self.assertEqual(inspection.findings, [])
            settings = json.loads(self.claude_user_settings.read_text(encoding="utf-8"))
            self.assertEqual(
                settings["autoMemoryDirectory"],
                leaderai_setup._portable_machine_path(target / "memory"),
            )
            tracked = subprocess.run(
                ["git", "ls-files"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertFalse((target / ".claude" / "settings.local.json").exists())
            self.assertNotIn("REPORT_FINALE.md", tracked)

    def test_oversized_markdown_router_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            agents = target / "AGENTS.md"
            policy = ecosistema_inspector.MARKDOWN_HYGIENE
            agents.write_text(
                agents.read_text(encoding="utf-8")
                + ("dettaglio da promuovere\n" * (policy.router_max_lines + 1)),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("MARKDOWN_ROUTER_TOO_LARGE", self.codes(inspection))

    def test_extended_markdown_document_requires_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            policy = ecosistema_inspector.MARKDOWN_HYGIENE
            manual = target / "ecosistema" / "manuale-esteso.md"
            manual.write_text(
                "# Manuale\n" + ("contenuto coerente\n" * policy.document_review_lines),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "PASSA CON ATTENZIONE")
            self.assertIn("MARKDOWN_DOCUMENT_REVIEW", self.codes(inspection))

    def test_unclassified_generic_and_empty_folders_block_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "documenti").mkdir()
            app = target / "app-iscrizioni"
            app.mkdir()
            (app / "app.txt").write_text("viva\n", encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("UNCLASSIFIED_DIR", self.codes(inspection))
            self.assertIn("GENERIC_DIR", self.codes(inspection))
            self.assertIn("EMPTY_DIR", self.codes(inspection))

    def test_declared_room_requires_complete_local_maps(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "app-iscrizioni").mkdir()
            self.add_room_to_registry(target)

            inspection = self.inspect(target)

            self.assertIn("ROOM_AGENTS_MISSING", self.codes(inspection))
            self.assertIn("ROOM_CLAUDE_MISSING", self.codes(inspection))

    def test_valid_declared_room_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "PASSA")

    def test_root_without_ecosystem_boss_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8").replace(
                    "Boss dell'Ecosistema",
                    "Coordinatore centrale",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ECOSYSTEM_BOSS_MISSING", self.codes(inspection))

    def test_existing_room_without_sector_administrator_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            old_row = (
                "| [Iscrizioni](app-iscrizioni) | Gestire iscrizioni | Radice | "
                "Documenti | Gestionale | Pratiche | App | "
                "`app-iscrizioni/AGENTS.md` |"
            )
            self.add_room_to_registry(target, old_row)

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_ADMINISTRATOR_MISSING", self.codes(inspection))
            self.assertIn("ROOM_BOSS_ROUTE_MISSING", self.codes(inspection))

    def test_declared_room_symlink_outside_house_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            external = Path(tmp) / "stanza-esterna"
            external.mkdir()
            (external / "AGENTS.md").write_text(
                "# Stanza\n\n## Responsabilita business\nMantiene stato e decisioni.\n",
                encoding="utf-8",
            )
            (external / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (target / "app-iscrizioni").symlink_to(external, target_is_directory=True)
            self.add_room_to_registry(target)

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_PATH_SYMLINK", self.codes(inspection))

    def test_required_agents_symlink_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            external = Path(tmp) / "AGENTS-esterno.md"
            external.write_text(
                (target / "AGENTS.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (target / "AGENTS.md").unlink()
            (target / "AGENTS.md").symlink_to(external)

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("STANDARD_PATH_SYMLINK", self.codes(inspection))

    def test_empty_gitignore_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / ".gitignore").write_text("", encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("GITIGNORE_RULES_MISSING", self.codes(inspection))
            self.assertIn("GITIGNORE_INEFFECTIVE", self.codes(inspection))

    def test_missing_git_repository_is_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / ".git").rename(Path(tmp) / "git-backup")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("GIT_REPOSITORY_MISSING", self.codes(inspection))

    def test_technical_portfolio_pipeline_is_not_proven_as_a_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target, "Portafoglio Modello")
            room_map = target / "Portafoglio Modello" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "Mantiene lo stato delle pratiche e le decisioni sulle iscrizioni",
                    "DA DEFINIRE: contiene skill, motori, modelli e report",
                ),
                encoding="utf-8",
            )
            self.add_room_to_registry(
                target,
                "| [Portafoglio Modello](Portafoglio Modello) | Costruire modelli | "
                "Fonti | Report | Dati | Documenti | Script | "
                "`Portafoglio Modello/AGENTS.md` |",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn(
                "ROOM_BUSINESS_RESPONSIBILITY_UNPROVEN",
                self.codes(inspection),
            )

    def test_root_can_own_portfolio_capability_without_creating_a_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            portfolio = target / "Portafoglio Modello"
            portfolio.mkdir()
            (portfolio / "motore.py").write_text("print('ok')\n", encoding="utf-8")
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            placeholder = (
                "| Da censire | Da definire | Da definire dal lavoro reale | "
                "`ecosistema/ASSET.md` o `ecosistema/FONTI.md` |"
            )
            row = (
                "| `Portafoglio Modello` | CAPACITA | Costruzione portafogli | "
                "`ecosistema/ASSET.md` |"
            )
            agents.write_text(text.replace(placeholder, row), encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "PASSA")
            self.assertFalse((portfolio / "AGENTS.md").exists())
            self.assertFalse((portfolio / "CLAUDE.md").exists())

    def test_existing_canonical_memory_can_keep_its_consolidated_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            canonical = target / "_claude-memory"
            canonical.mkdir()
            (canonical / "MEMORY.md").write_text("# Memoria viva\n", encoding="utf-8")
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            text = text.replace(
                "Memoria canonica: `memory/`.",
                "Memoria canonica: `_claude-memory/`.",
            )
            placeholder = (
                "| Da censire | Da definire | Da definire dal lavoro reale | "
                "`ecosistema/ASSET.md` o `ecosistema/FONTI.md` |"
            )
            row = (
                "| `_claude-memory` | INFRASTRUTTURA | Memoria condivisa | "
                "`_claude-memory/MEMORY.md` |"
            )
            agents.write_text(text.replace(placeholder, row), encoding="utf-8")
            self.claude_user_settings.write_text(
                json.dumps(
                    {
                        "autoMemoryDirectory": (
                            leaderai_setup._portable_machine_path(canonical)
                        )
                    }
                ),
                encoding="utf-8",
            )
            memory = target / "memory"
            (memory / "MEMORY.md").unlink()
            memory.rmdir()

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "PASSA")

    def test_duplicate_room_purpose_and_loose_root_file_block_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target, "app-iscrizioni")
            self.create_valid_room(target, "segreteria")
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            placeholder = (
                "| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - | "
                "Da assegnare | Boss dell'Ecosistema |"
            )
            rows = (
                ROOM_ROW
                + "\n"
                + "| [Segreteria](segreteria) | Gestire iscrizioni | Radice | "
                "Documenti | Gestionale | Pratiche | App | `segreteria/AGENTS.md` | "
                "Amministratore di settore Segreteria | Boss dell'Ecosistema |"
            )
            agents.write_text(text.replace(placeholder, rows), encoding="utf-8")
            (target / "VERSION").write_text("0.3.8\n", encoding="utf-8")

            inspection = self.inspect(target)

            self.assertIn("DUPLICATE_ROOM_PURPOSE", self.codes(inspection))
            self.assertIn("UNOWNED_ROOT_FILE", self.codes(inspection))

    def test_missing_active_agent_skill_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            skill = target / ".claude" / "skills" / "ispettore-ecosistema"
            (skill / "SKILL.md").unlink()

            inspection = self.inspect(target)

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
            self.claude_user_settings.write_text(
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

            inspection = self.inspect(target)
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

    def test_absolute_home_memory_path_is_flagged_as_not_portable(self):
        """Caso Marco De Nicolo' 28/07/2026: percorso corretto sul PC fisso,
        rotto in silenzio sul portatile perche' inchioda il nome utente."""
        with tempfile.TemporaryDirectory(dir=Path.home()) as tmp:
            target = self.make_target(tmp)
            self.claude_user_settings.write_text(
                json.dumps(
                    {"autoMemoryDirectory": str((target / "memory").resolve())}
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)
            codes = self.codes(inspection)

            self.assertIn("CLAUDE_MEMORY_NOT_PORTABLE", codes)
            # E' un avviso, non un blocco: il percorso funziona su questa macchina,
            # ma va reso portabile prima di replicarlo sulla seconda postazione.
            self.assertEqual(inspection.verdict, "PASSA CON ATTENZIONE")

    def test_portable_memory_path_passes_clean(self):
        with tempfile.TemporaryDirectory(dir=Path.home()) as tmp:
            target = self.make_target(tmp)
            relative = (target / "memory").resolve().relative_to(Path.home().resolve())
            self.claude_user_settings.write_text(
                json.dumps({"autoMemoryDirectory": f"~/{relative.as_posix()}"}),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertNotIn("CLAUDE_MEMORY_NOT_PORTABLE", self.codes(inspection))
            self.assertEqual(inspection.verdict, "PASSA")

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

            inspection = self.inspect(target)

            self.assertIn(
                "CREDENTIAL_EXPOSURE_NOT_EXCLUDED",
                self.codes(inspection),
            )


if __name__ == "__main__":
    unittest.main()
