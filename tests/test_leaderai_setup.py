import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import leaderai_setup


class LeaderAISetupTest(unittest.TestCase):
    def run_setup(self, target: Path, agent: str, **kwargs):
        if agent in {"claude", "both"}:
            kwargs.setdefault(
                "claude_user_settings_path",
                target.parent / f"{target.name}-claude-user-settings.json",
            )
            kwargs.setdefault(
                "claude_user_instructions_path",
                target.parent / f"{target.name}-claude-user-CLAUDE.md",
            )
        if agent in {"codex", "both"}:
            kwargs.setdefault(
                "codex_user_instructions_path",
                target.parent / f"{target.name}-codex-user-AGENTS.md",
            )
        return leaderai_setup.run_setup(
            target,
            "Cliente Test",
            agent,
            **kwargs,
        )

    def test_fresh_install_agent_matrix(self):
        cases = {
            "codex": (True, False, "`.codex/README.md`"),
            "claude": (False, True, "`.claude/README.md`"),
            "both": (
                True,
                True,
                "`.claude/README.md`, `.codex/README.md`",
            ),
        }
        for agent, (has_codex, has_claude, active_config) in cases.items():
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "EcosistemaAI-Test"
                self.run_setup(target, agent)

                self.assertTrue((target / "AGENTS.md").is_file())
                self.assertTrue((target / "CLAUDE.md").is_file())
                self.assertFalse((target / "CLAUDE.md").is_symlink())
                self.assertEqual(
                    (target / "CLAUDE.md").read_text(encoding="utf-8"),
                    "@AGENTS.md\n",
                )
                self.assertEqual((target / ".codex" / "README.md").exists(), has_codex)
                self.assertEqual((target / ".claude" / "README.md").exists(), has_claude)
                self.assertEqual(
                    (target / ".claude" / "settings.local.json").exists(),
                    False,
                )
                self.assertEqual(
                    (
                        target
                        / ".agents"
                        / "skills"
                        / "ispettore-ecosistema"
                        / "SKILL.md"
                    ).exists(),
                    has_codex,
                )
                self.assertEqual(
                    (
                        target
                        / ".claude"
                        / "skills"
                        / "ispettore-ecosistema"
                        / "SKILL.md"
                    ).exists(),
                    has_claude,
                )

                self.assertFalse((target / "REPORT_FINALE.md").exists())
                log = (target / "logs" / "install-log.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn(f"- Agent: {agent}", log)
                for config in active_config.split(", "):
                    self.assertTrue((target / config.strip("`")).exists())

    def test_creates_cervello_and_ecosistema(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            result = self.run_setup(target, "claude")

            self.assertIn("AGENTS.md", result.created)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertIn("@AGENTS.md", (target / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertTrue((target / ".claude" / "README.md").exists())
            self.assertFalse((target / ".codex" / "README.md").exists())
            self.assertTrue(
                (
                    target
                    / ".claude"
                    / "skills"
                    / "ispettore-ecosistema"
                    / "SKILL.md"
                ).exists()
            )
            self.assertFalse(
                (
                    target
                    / ".agents"
                    / "skills"
                    / "ispettore-ecosistema"
                    / "SKILL.md"
                ).exists()
            )
            self.assertTrue((target / "memory" / "MEMORY.md").exists())
            self.assertTrue((target / "ecosistema" / "FONTI.md").exists())
            self.assertTrue((target / "ecosistema" / "ASSET.md").exists())
            self.assertFalse((target / "REPORT_FINALE.md").exists())

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            asset = (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8")
            log = (target / "logs" / "install-log.md").read_text(encoding="utf-8")
            self.assertIn("Cliente Test", agents)
            self.assertIn("Modalita' installata: `claude`.", agents)
            self.assertIn("Comunicazione e fonti di verita'", agents)
            self.assertIn("AGENT_CHAT.md", agents)
            self.assertTrue((target / "AGENT_CHAT.md").exists())
            self.assertIn("Asset operativi", asset)
            self.assertIn(
                f"- Standard version: {leaderai_setup.STANDARD_VERSION}", log
            )
            self.assertIn("- Agent: claude", log)
            self.assertIn("Architettura adattiva", agents)
            self.assertFalse((target / "resoconti").exists())

    def test_first_commit_photographs_install(self):
        # La cartella madre deve nascere come repository CON cronologia:
        # senza primo commit il backup della Fase 7 parte da un repo vuoto.
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            result = self.run_setup(target, "claude")

            log = subprocess.run(
                ["git", "log", "--oneline"],
                cwd=str(target),
                capture_output=True,
                text=True,
            )
            self.assertEqual(log.returncode, 0)
            self.assertIn("installazione iniziale", log.stdout)
            porcelain = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(target),
                capture_output=True,
                text=True,
            )
            self.assertEqual(porcelain.stdout.strip(), "")
            self.assertIn("primo commit creato", result.git_outcome)

    def test_second_run_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )
            marker = "MODIFICA CLIENTE\n"
            (target / "AGENTS.md").write_text(marker, encoding="utf-8")

            result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertIn("AGENTS.md", result.existing)
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), marker)
            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertIn("@AGENTS.md", (target / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertFalse((target / ".claude").exists())

    def test_both_is_explicit_and_creates_both_agent_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            self.run_setup(target, "both")

            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertTrue((target / ".claude" / "README.md").exists())
            self.assertTrue((target / ".codex" / "README.md").exists())
            self.assertTrue(
                (
                    target
                    / ".claude"
                    / "skills"
                    / "ispettore-ecosistema"
                    / "SKILL.md"
                ).exists()
            )
            self.assertTrue(
                (
                    target
                    / ".agents"
                    / "skills"
                    / "ispettore-ecosistema"
                    / "SKILL.md"
                ).exists()
            )

    def test_migrates_pre_036_codex_install_by_adding_common_bridge(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Pre036"
            target.mkdir()
            original_agents = "# Istruzioni cliente storiche\n"
            (target / "AGENTS.md").write_text(original_agents, encoding="utf-8")
            (target / ".codex").mkdir()
            (target / ".codex" / "README.md").write_text(
                "configurazione precedente\n",
                encoding="utf-8",
            )

            result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertIn("CLAUDE.md", result.created)
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertEqual(
                (target / "AGENTS.md").read_text(encoding="utf-8"),
                original_agents,
            )
            self.assertFalse((target / ".claude").exists())

    def test_force_replaces_valid_claude_symlink_without_touching_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Symlink"
            target.mkdir()
            original_agents = "# Fonte cliente da preservare\n"
            (target / "AGENTS.md").write_text(original_agents, encoding="utf-8")
            (target / "CLAUDE.md").symlink_to("AGENTS.md")

            result = leaderai_setup.run_setup(
                target,
                "Cliente Test",
                "codex",
                force=True,
                codex_user_instructions_path=target.parent / "codex-user-AGENTS.md",
            )

            self.assertIn("CLAUDE.md", result.updated)
            self.assertFalse((target / "CLAUDE.md").is_symlink())
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertEqual(
                (target / "AGENTS.md").read_text(encoding="utf-8"),
                original_agents,
            )

    def test_repeated_force_repairs_keep_every_distinct_claude_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-BackupMultipli"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Fonte cliente\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text(
                "ISTRUZIONI CLIENTE UNO\n",
                encoding="utf-8",
            )

            leaderai_setup.run_setup(
                target,
                "Cliente Test",
                "codex",
                force=True,
                codex_user_instructions_path=target.parent / "codex-user-AGENTS.md",
            )
            (target / "CLAUDE.md").write_text(
                "ISTRUZIONI CLIENTE DUE\n",
                encoding="utf-8",
            )
            leaderai_setup.run_setup(
                target,
                "Cliente Test",
                "codex",
                force=True,
                codex_user_instructions_path=target.parent / "codex-user-AGENTS.md",
            )

            self.assertEqual(
                (target / "CLAUDE.md.leaderai-backup").read_text(encoding="utf-8"),
                "ISTRUZIONI CLIENTE UNO\n",
            )
            self.assertEqual(
                (target / "CLAUDE.md.leaderai-backup.2").read_text(encoding="utf-8"),
                "ISTRUZIONI CLIENTE DUE\n",
            )
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )

    def test_broken_claude_symlink_blocks_without_force_and_repairs_with_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-BrokenSymlink"
            target.mkdir()
            original_agents = "# Fonte cliente\n"
            (target / "AGENTS.md").write_text(original_agents, encoding="utf-8")
            (target / "CLAUDE.md").symlink_to("file-che-non-esiste.md")

            blocked = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertTrue(blocked.blockers)
            self.assertEqual(blocked.target_verdict, "NON PASSA")
            self.assertTrue((target / "CLAUDE.md").is_symlink())
            self.assertFalse((target / "REPORT_FINALE.md").exists())

            result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", force=True, codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertIn("CLAUDE.md", result.updated)
            self.assertFalse((target / "CLAUDE.md").is_symlink())
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertEqual(
                (target / "AGENTS.md").read_text(encoding="utf-8"),
                original_agents,
            )

    def test_wrong_bridge_is_preserved_without_force_and_repaired_with_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-WrongBridge"
            target.mkdir()
            original_agents = "# Regole reali del cliente\n"
            wrong_bridge = "# CLAUDE.md\n\nIstruzioni separate e superate\n"
            (target / "AGENTS.md").write_text(original_agents, encoding="utf-8")
            (target / "CLAUDE.md").write_text(wrong_bridge, encoding="utf-8")

            preserved = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                wrong_bridge,
            )
            self.assertTrue(preserved.blockers)
            self.assertEqual(preserved.target_verdict, "NON PASSA")
            self.assertFalse((target / "REPORT_FINALE.md").exists())

            repaired = leaderai_setup.run_setup(
                target,
                "Cliente Test",
                "codex",
                force=True,
                codex_user_instructions_path=target.parent / "codex-user-AGENTS.md",
            )

            self.assertIn("CLAUDE.md", repaired.updated)
            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            self.assertEqual(
                (target / "AGENTS.md").read_text(encoding="utf-8"),
                original_agents,
            )

    def test_dry_run_reports_changes_without_creating_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-DryRun"

            result = leaderai_setup.run_setup(
                target,
                "Cliente Test",
                "codex",
                dry_run=True,
            )

            self.assertFalse(target.exists())
            self.assertIn("AGENTS.md", result.created)
            self.assertIn("CLAUDE.md", result.created)
            self.assertIn(".codex/README.md", result.created)
            self.assertNotIn(".claude/README.md", result.created)
            self.assertIn("dry-run", result.git_outcome)

    def test_force_only_repairs_bridge_and_preserves_every_customer_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Cliente"
            for dirname in ("memory", "logs", "ecosistema", ".codex", ".claude"):
                (target / dirname).mkdir(parents=True, exist_ok=True)
            protected = {
                "AGENTS.md": "AGENTS CLIENTE\n",
                "memory/MEMORY.md": "MEMORIA CLIENTE\n",
                "AGENT_CHAT.md": "CHAT CLIENTE\n",
                ".codex/README.md": "CONFIG CODEX CLIENTE\n",
                ".claude/README.md": "CONFIG CLAUDE CLIENTE\n",
                "ecosistema/FONTI.md": "FONTI CLIENTE\n",
                "ecosistema/ASSET.md": "ASSET CLIENTE\n",
                "ecosistema/PROCESSI.md": "PROCESSI CLIENTE\n",
                "ecosistema/LIMITI.md": "LIMITI CLIENTE\n",
            }
            for rel, content in protected.items():
                (target / rel).write_text(content, encoding="utf-8")
            (target / ".gitignore").write_text(
                leaderai_setup.GITIGNORE_CONTENT + "regola-cliente\n",
                encoding="utf-8",
            )
            old_report = "REPORT STORICO\nVERDETTO\n- PASSA\n"
            (target / "REPORT_FINALE.md").write_text(old_report, encoding="utf-8")
            (target / "CLAUDE.md").write_text("ponte errato\n", encoding="utf-8")

            result = self.run_setup(target, "both", force=True)

            self.assertEqual(
                (target / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )
            for rel, content in protected.items():
                self.assertEqual((target / rel).read_text(encoding="utf-8"), content)
            report = (target / "REPORT_FINALE.md").read_text(encoding="utf-8")
            self.assertEqual(report, old_report)
            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertIn("CLAUDE.md", result.updated)

    def test_gitignore_adds_every_missing_required_rule_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Gitignore"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            (target / ".gitignore").write_text(
                ".secrets/\nregola-cliente\n",
                encoding="utf-8",
            )

            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )
            first = (target / ".gitignore").read_text(encoding="utf-8")
            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )
            second = (target / ".gitignore").read_text(encoding="utf-8")

            for rule in leaderai_setup._required_gitignore_rules():
                self.assertEqual(first.splitlines().count(rule), 1)
            self.assertIn("regola-cliente", first)
            self.assertEqual(second, first)

    def test_gitignore_safety_block_overrides_secret_negations(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-GitignoreNegazione"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            (target / ".gitignore").write_text(
                "*.env\n!segreto.env\nregola-cliente\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "init"],
                cwd=str(target),
                check=True,
                capture_output=True,
            )

            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )
            secret = target / "segreto.env"
            secret.write_text("NON-COMMITTERE\n", encoding="utf-8")

            ignored = subprocess.run(
                ["git", "check-ignore", "-q", "segreto.env"],
                cwd=str(target),
            )
            status = subprocess.run(
                ["git", "status", "--porcelain", "--", "segreto.env"],
                cwd=str(target),
                capture_output=True,
                text=True,
            )
            gitignore = (target / ".gitignore").read_text(encoding="utf-8")
            self.assertEqual(ignored.returncode, 0)
            self.assertEqual(status.stdout, "")
            self.assertLess(
                gitignore.index("!segreto.env"),
                gitignore.rindex("*.env"),
            )

    def test_rejects_symlinked_standard_parent_before_writing_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-SymlinkParent"
            outside = Path(tmp) / "Fuori"
            target.mkdir()
            outside.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            (target / "ecosistema").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "Directory standard.*symlink"):
                leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_rejects_symlinked_target_ancestor_before_writing_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            outside = base / "Fuori"
            outside.mkdir()
            linked_parent = base / "Collegamento"
            linked_parent.symlink_to(outside, target_is_directory=True)
            target = linked_parent / "EcosistemaAI-Test"

            with self.assertRaisesRegex(ValueError, "(padre|antenata).*symlink"):
                leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_existing_target_behind_symlinked_ancestor(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            outside = base / "Fuori"
            real_target = outside / "EcosistemaAI-Test"
            real_target.mkdir(parents=True)
            linked_parent = base / "Collegamento"
            linked_parent.symlink_to(outside, target_is_directory=True)
            target = linked_parent / "EcosistemaAI-Test"

            with self.assertRaisesRegex(ValueError, "antenata.*symlink"):
                leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertEqual(list(real_target.iterdir()), [])

    def test_rejects_standard_file_occupied_by_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-TipoErrato"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            (target / ".codex" / "README.md").mkdir(parents=True)

            with self.assertRaisesRegex(ValueError, "File standard.*directory"):
                leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertFalse((target / "CLAUDE.md").exists())

    def test_failed_first_commit_is_reported_truthfully(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-CommitFallito"
            real_run = subprocess.run

            def fail_first_commit(command, *args, **kwargs):
                if command[0] == "git" and "commit" in command and "--amend" not in command:
                    raise subprocess.CalledProcessError(1, command)
                return real_run(command, *args, **kwargs)

            with mock.patch.object(
                leaderai_setup.subprocess,
                "run",
                side_effect=fail_first_commit,
            ):
                result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            log = (target / "logs" / "install-log.md").read_text(encoding="utf-8")
            self.assertIn("primo commit fallito", result.git_outcome)
            self.assertIn("primo commit fallito", log)
            self.assertFalse((target / "REPORT_FINALE.md").exists())
            head = real_run(
                ["git", "rev-parse", "--verify", "HEAD"],
                cwd=str(target),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(head.returncode, 0)

    def test_cli_returns_nonzero_when_gate_has_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-CLI-Bloccato"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            (target / "CLAUDE.md").write_text("copia indipendente\n", encoding="utf-8")

            completed = subprocess.run(
                [
                    "python3",
                    str(Path(leaderai_setup.__file__)),
                    "--target",
                    str(target),
                    "--client",
                    "Cliente Test",
                    "--agent",
                    "codex",
                    "--quiet",
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("created=", completed.stdout)
            self.assertIn("verdict=NON PASSA", completed.stdout)
            self.assertFalse((target / "REPORT_FINALE.md").exists())

    def test_identical_rerun_does_not_append_log_or_create_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Idempotente"
            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )
            log_before = (target / "logs" / "install-log.md").read_text(
                encoding="utf-8"
            )
            count_before = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            self.assertEqual(
                (target / "logs" / "install-log.md").read_text(encoding="utf-8"),
                log_before,
            )
            count_after = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.assertEqual(count_after, count_before)
            self.assertEqual(result.created, [])
            self.assertEqual(result.updated, [])

    def test_live_repository_is_never_auto_staged_or_committed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Live"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            subprocess.run(["git", "init"], cwd=str(target), check=True, capture_output=True)
            subprocess.run(
                ["git", "add", "AGENTS.md"],
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
                    "baseline",
                ],
                cwd=str(target),
                check=True,
                capture_output=True,
            )
            (target / "cliente-non-toccare.txt").write_text(
                "dato cliente\n", encoding="utf-8"
            )

            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            count = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            staged = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            untracked = subprocess.run(
                ["git", "status", "--porcelain", "cliente-non-toccare.txt"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            self.assertEqual(count, "1")
            self.assertEqual(staged, "")
            self.assertIn("cliente-non-toccare.txt", untracked)

    def test_legacy_report_is_preserved_and_blocks_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Migrazione"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Cliente\n", encoding="utf-8")
            old = "# Report vecchio\n\nVERDETTO\n- PASSA\n"
            (target / "REPORT_FINALE.md").write_text(old, encoding="utf-8")

            result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            report = (target / "REPORT_FINALE.md").read_text(encoding="utf-8")
            self.assertEqual(report, old)
            self.assertEqual(result.target_verdict, "NON PASSA")

    def test_legacy_report_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Migrazione"
            leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )
            report_path = target / "REPORT_FINALE.md"
            old = "# Residuo storico\n\nFatto del cliente\n"
            report_path.write_text(old, encoding="utf-8")
            (target / ".codex" / "README.md").unlink()

            result = leaderai_setup.run_setup(
                target, "Cliente Test", "codex", codex_user_instructions_path=target.parent / "codex-user-AGENTS.md"
            )

            report = report_path.read_text(encoding="utf-8")
            self.assertEqual(report, old)
            self.assertEqual(result.target_verdict, "NON PASSA")

    def test_run_setup_rejects_invalid_agent_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Invalid"

            with self.assertRaisesRegex(ValueError, "Agente non valido"):
                leaderai_setup.run_setup(target, "Cliente Test", "gemini")

            self.assertFalse(target.exists())

    def test_technical_setup_refuses_unclassified_live_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Azienda"
            target.mkdir()
            (target / "lavoro-reale.xlsx").write_text("dato", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "CHECKUP.md"):
                self.run_setup(target, "claude")


    def test_user_instructions_block_is_added_without_touching_existing_content(self):
        """Il blocco LEADERAI-CASA entra nel file utente e lo lascia intatto."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            instructions = Path(tmp) / "claude-user-CLAUDE.md"
            instructions.write_text(
                "# Preferenze personali\n\n- Rispondi in italiano.\n",
                encoding="utf-8",
            )

            result = self.run_setup(
                target, "claude", claude_user_instructions_path=instructions
            )

            text = instructions.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# Preferenze personali\n"))
            self.assertIn("- Rispondi in italiano.", text)
            self.assertIn("<!-- LEADERAI-CASA:inizio -->", text)
            self.assertIn("<!-- LEADERAI-CASA:fine -->", text)
            self.assertIn("FUORI DAL CERVELLO", text)
            self.assertIn(leaderai_setup._portable_machine_path(target), text)
            self.assertNotIn("{{", text)
            self.assertTrue(
                any(
                    "Istruzioni globali Claude Code aggiornate" in item
                    for item in result.external_effects
                )
            )
            self.assertEqual(result.target_verdict, "PASSA")

            again = self.run_setup(
                target, "claude", claude_user_instructions_path=instructions
            )
            self.assertEqual(instructions.read_text(encoding="utf-8"), text)
            self.assertEqual(text.count("<!-- LEADERAI-CASA:inizio -->"), 1)
            self.assertTrue(
                any("gia' corrette" in item for item in again.external_effects)
            )

    def test_user_instructions_block_is_refreshed_in_place(self):
        """Un blocco vecchio viene sostituito dove sta, non duplicato in coda."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            instructions = Path(tmp) / "claude-user-CLAUDE.md"
            instructions.write_text(
                "<!-- LEADERAI-CASA:inizio -->\nvecchio blocco\n"
                "<!-- LEADERAI-CASA:fine -->\n\n# Dopo\n",
                encoding="utf-8",
            )

            self.run_setup(target, "claude", claude_user_instructions_path=instructions)

            text = instructions.read_text(encoding="utf-8")
            self.assertNotIn("vecchio blocco", text)
            self.assertEqual(text.count("<!-- LEADERAI-CASA:inizio -->"), 1)
            self.assertTrue(text.rstrip().endswith("# Dopo"))

    def test_user_instructions_are_not_written_without_a_path_read_on_this_machine(self):
        """Senza percorso letto sulla macchina il setup non tocca la home."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"

            result = leaderai_setup.run_setup(target, "Cliente Test", "codex")

            self.assertEqual(
                sorted(item.name for item in Path(tmp).iterdir()),
                ["EcosistemaAI-Test"],
            )
            self.assertTrue(
                any(
                    "Istruzioni globali Codex: DA COLLAUDARE" in item
                    for item in result.external_effects
                )
            )

    def test_codex_override_file_receives_the_block_when_present(self):
        """Codex legge AGENTS.override.md al posto di AGENTS.md: il blocco va li'."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            home_codex = Path(tmp) / "codex-home"
            home_codex.mkdir()
            override = home_codex / "AGENTS.override.md"
            override.write_text("# Override attivo\n", encoding="utf-8")
            requested = home_codex / "AGENTS.md"

            self.run_setup(target, "codex", codex_user_instructions_path=requested)

            self.assertFalse(requested.exists())
            self.assertIn(
                "<!-- LEADERAI-CASA:inizio -->",
                override.read_text(encoding="utf-8"),
            )

    def test_user_instructions_inside_the_house_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"

            result = self.run_setup(
                target,
                "claude",
                claude_user_instructions_path=target / "CLAUDE_UTENTE.md",
            )

            self.assertTrue(
                any(
                    "non possono vivere dentro la cartella cliente" in item
                    for item in result.blockers
                )
            )
            self.assertEqual(result.target_verdict, "NON PASSA")


if __name__ == "__main__":
    unittest.main()
