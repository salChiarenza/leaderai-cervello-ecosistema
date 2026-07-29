import json
import tempfile
import textwrap
import unittest
from pathlib import Path

import installation_harness


FAKE_INSTALLER = r"""
import json
import pathlib
import re
import subprocess
import sys

prompt = sys.stdin.read()
workspace = pathlib.Path.cwd()
snapshot = workspace / "standard-snapshot"
target_match = re.search(
    r"cartella locale vuota\s+`([^`]+)`",
    prompt,
)
mode_match = re.search(r"- modalita': (codex|claude|both);", prompt)
if not target_match or not mode_match:
    raise SystemExit(11)
target = workspace / target_match.group(1)
mode = mode_match.group(1)
version = (snapshot / "VERSION").read_text(encoding="utf-8").strip()

context = {
    "client_name": "Cliente Collaudo",
    "date": "29/07/2026",
    "agent": mode,
    "version": version,
}

def render(name):
    text = (snapshot / "templates" / name).read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text.rstrip() + "\n"

def write(relative, content):
    path = target / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

write("AGENTS.md", render("AGENTS.md"))
write("CLAUDE.md", render("CLAUDE.md"))
write("AGENT_CHAT.md", render("AGENT_CHAT.md"))
write("memory/MEMORY.md", render("MEMORY.md"))
write("ecosistema/ASSET.md", render("ASSET.md"))
write("ecosistema/FONTI.md", render("FONTI.md"))
write("ecosistema/PROCESSI.md", render("PROCESSI.md"))
write("ecosistema/LIMITI.md", render("LIMITI.md"))
write("ecosistema/STANZA_AGENTS.md", render("STANZA_AGENTS.md"))
write(".gitignore", render("GITIGNORE.txt"))
write(
    "logs/install-log.md",
    "# Install log\n\n"
    "Installazione manuale dello standard " + version + " in modalita' "
    + mode + ".\n",
)

if mode in ("codex", "both"):
    write(".codex/README.md", render("CODEX_README.md"))
    write(
        ".agents/skills/ispettore-ecosistema/SKILL.md",
        render("ISPETTORE_SKILL.md"),
    )
if mode in ("claude", "both"):
    write(".claude/README.md", render("CLAUDE_README.md"))
    write(
        ".claude/skills/ispettore-ecosistema/SKILL.md",
        render("ISPETTORE_SKILL.md"),
    )

write(
    "REPORT_FINALE.md",
    "# Report missione LeaderAI\n\n"
    "VALIDO AL: 29/07/2026 12:00 UTC\n"
    "STATO MISSIONE: APERTA\n\n"
    "## Standard\n\n"
    "- Repo ufficiale letta dalla fotografia immutabile.\n"
    "- Versione: " + version + "\n"
    "- Modalita: " + mode + "\n"
    "- Codice esterno eseguito: no\n"
    "- Fonti reali: DA COLLEGARE\n"
    "- Browser e impostazioni utente: DA COLLAUDARE\n\n"
    "- default_browser: DA COLLAUDARE\n"
    "- desktop_launcher: DA COLLAUDARE\n"
    "- remote_backup: DA COLLEGARE\n\n"
    "## Verdetto\n\n"
    "PASSA CON ATTENZIONE\n",
)

subprocess.run(["git", "init"], cwd=target, check=True, capture_output=True)
subprocess.run(["git", "add", "-A"], cwd=target, check=True, capture_output=True)
subprocess.run(
    [
        "git",
        "-c",
        "user.name=LeaderAI Test",
        "-c",
        "user.email=test@leaderai.local",
        "commit",
        "-m",
        "installazione iniziale",
    ],
    cwd=target,
    check=True,
    capture_output=True,
)
print(json.dumps({"type": "result", "result": "installazione completata"}))
"""


class InstallationHarnessTest(unittest.TestCase):
    def test_manual_harness_uses_bounded_official_installation_core(self):
        install = (
            installation_harness.REPO_ROOT / "INSTALLA_CON_AI.md"
        ).read_text(encoding="utf-8")
        prompt = installation_harness.MISSION_TEMPLATE

        self.assertEqual(install.count("START_NUCLEO_INSTALLAZIONE"), 1)
        self.assertEqual(install.count("END_NUCLEO_INSTALLAZIONE"), 1)
        self.assertIn("START_NUCLEO_INSTALLAZIONE", prompt)
        self.assertIn("END_NUCLEO_INSTALLAZIONE", prompt)
        self.assertIn("esattamente `installazione iniziale`", prompt)
        self.assertIn(
            "`## Verdetto` uguale a `PASSA CON ATTENZIONE`",
            prompt,
        )
        self.assertNotIn("Leggi integralmente", prompt)

    def make_fake(self, root: Path, source: str = FAKE_INSTALLER) -> Path:
        path = root / "fake agent.py"
        path.write_text(textwrap.dedent(source), encoding="utf-8")
        return path

    def run_fake(
        self,
        root: Path,
        *,
        mode: str,
        target_name: str = "Casa prova con spazi - città d'Artù",
        source: str = FAKE_INSTALLER,
    ) -> installation_harness.InstallationResult:
        fake = self.make_fake(root, source)
        return installation_harness.run_installation(
            agent="codex",
            mode=mode,
            executable=str(fake),
            source_root=installation_harness.REPO_ROOT,
            evidence_dir=root / ("evidence-" + mode),
            timeout_seconds=10.0,
            transcript_format="jsonl",
            workspace_dir=root / ("workspace-" + mode),
            target_name=target_name,
        )

    def test_claude_stream_json_requires_verbose_but_single_json_does_not(self):
        workspace = Path("/tmp/workspace-manuale")
        jsonl = installation_harness.build_command(
            "claude", "claude", workspace, "jsonl"
        )
        single_json = installation_harness.build_command(
            "claude", "claude", workspace, "json"
        )
        self.assertEqual(
            jsonl[jsonl.index("--output-format") + 1],
            "stream-json",
        )
        self.assertIn("--verbose", jsonl)
        self.assertEqual(
            single_json[single_json.index("--output-format") + 1],
            "json",
        )
        self.assertNotIn("--verbose", single_json)
        self.assertEqual(
            jsonl[jsonl.index("--permission-mode") + 1],
            "bypassPermissions",
        )

    def test_report_mode_accepts_exact_value_before_explanatory_text(self):
        self.assertEqual(
            installation_harness._report_mode(
                "- Modalita': `claude` (governa il ramo Claude)\n"
            ),
            "claude",
        )
        self.assertEqual(
            installation_harness._report_mode("- Modalità scelta: codex.\n"),
            "codex",
        )
        self.assertIsNone(
            installation_harness._report_mode(
                "- Nota: la modalita' consigliata potrebbe essere both.\n"
            )
        )

    def test_manual_mission_keeps_source_read_only_but_target_copies_writable(self):
        mission = installation_harness.MISSION_TEMPLATE
        guide = (
            installation_harness.REPO_ROOT / "INSTALLA_CON_AI.md"
        ).read_text(encoding="utf-8")

        for text in (mission, guide):
            normalized = " ".join(text.split())
            self.assertIn("fonte resta intoccabile", normalized)
            self.assertIn("rendi scrivibili soltanto i file", normalized)

    def test_fake_agent_passes_all_installation_modes_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for mode in ("codex", "claude", "both"):
                with self.subTest(mode=mode):
                    result = self.run_fake(root, mode=mode)
                    self.assertEqual(result.status, "PASS")
                    self.assertTrue(result.oracle_passed)
                    evidence = Path(result.evidence_dir)
                    oracle = json.loads(
                        (evidence / "oracle.json").read_text(encoding="utf-8")
                    )
                    self.assertTrue(oracle["passed"])
                    self.assertTrue((evidence / "standard-manifest-pre.json").is_file())
                    self.assertTrue((evidence / "standard-manifest-post.json").is_file())
                    self.assertTrue((evidence / "target-manifest-pre.json").is_file())
                    self.assertTrue((evidence / "target-manifest-post.json").is_file())
                    self.assertTrue((evidence / "git.json").is_file())
                    self.assertTrue((evidence / "observed-report.md").is_file())
                    self.assertNotIn(
                        str(root / ("workspace-" + mode)),
                        (evidence / "command.json").read_text(encoding="utf-8"),
                    )

    def test_oracle_rejects_non_passa_even_if_future_goal_mentions_passa(self):
        source = FAKE_INSTALLER.replace(
            '"PASSA CON ATTENZIONE\\n",',
            '"NON PASSA. Obiettivo futuro: PASSA CON ATTENZIONE\\n",',
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_fake(Path(tmp), mode="codex", source=source)

            self.assertEqual(result.status, "ORACLE_FAIL")
            oracle = json.loads(
                (Path(result.evidence_dir) / "oracle.json").read_text(
                    encoding="utf-8"
                )
            )
            report_check = next(
                check
                for check in oracle["checks"]
                if check["name"] == "versione_e_report_coerenti"
            )
            self.assertIn("verdetto=NON PASSA", report_check["detail"])

    def test_oracle_rejects_wrong_mode_declared_in_agents(self):
        source = FAKE_INSTALLER.replace(
            'write("CLAUDE.md", render("CLAUDE.md"))',
            'write("AGENTS.md", render("AGENTS.md").replace("`claude`", "`codex`"))\n'
            'write("CLAUDE.md", render("CLAUDE.md"))',
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_fake(Path(tmp), mode="claude", source=source)

            self.assertEqual(result.status, "ORACLE_FAIL")
            oracle = json.loads(
                (Path(result.evidence_dir) / "oracle.json").read_text(
                    encoding="utf-8"
                )
            )
            report_check = next(
                check
                for check in oracle["checks"]
                if check["name"] == "versione_e_report_coerenti"
            )
            self.assertIn("modalita_mappa=codex", report_check["detail"])

    def test_paths_with_spaces_accents_and_apostrophe_are_supported(self):
        with tempfile.TemporaryDirectory(prefix="percorso città d'Artù - ") as tmp:
            root = Path(tmp)
            result = self.run_fake(
                root,
                mode="codex",
                target_name="Casa città d'Artù con spazi",
            )
            self.assertEqual(result.status, "PASS")
            self.assertIn("Casa città d'Artù", result.target_dir)

    def test_default_temporary_workspace_is_removed_after_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = self.make_fake(root)
            result = installation_harness.run_installation(
                agent="codex",
                mode="codex",
                executable=str(fake),
                source_root=installation_harness.REPO_ROOT,
                evidence_dir=root / "evidence",
                timeout_seconds=10.0,
                transcript_format="jsonl",
            )
            self.assertEqual(result.status, "PASS")
            self.assertEqual(result.workspace_dir, "$TEMPORARY_WORKSPACE")

    def test_standard_snapshot_has_no_python_setup_or_git_clone_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_fake(root, mode="codex")
            manifest = json.loads(
                (
                    Path(result.evidence_dir) / "standard-manifest-pre.json"
                ).read_text(encoding="utf-8")
            )
            files = set(manifest["files"])
            self.assertNotIn("leaderai_setup.py", files)
            self.assertFalse(any(path.endswith(".py") for path in files))
            self.assertFalse(any(path.startswith(".git/") for path in files))

    def test_missing_cli_is_a_failure_with_complete_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = installation_harness.run_installation(
                agent="codex",
                mode="codex",
                executable=str(root / "cli-inesistente"),
                source_root=installation_harness.REPO_ROOT,
                evidence_dir=root / "evidence",
                timeout_seconds=1.0,
                transcript_format="jsonl",
                workspace_dir=root / "workspace",
            )
            self.assertEqual(result.status, "EXECUTABLE_MISSING")
            self.assertFalse(result.executable_found)
            self.assertTrue((Path(result.evidence_dir) / "result.json").is_file())
            self.assertTrue((Path(result.evidence_dir) / "oracle.json").is_file())

    def test_authentication_error_is_not_a_skip(self):
        auth_failure = """
        import sys
        sys.stdin.read()
        print("Authentication required", file=sys.stderr)
        raise SystemExit(3)
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = self.make_fake(root, auth_failure)
            result = installation_harness.run_installation(
                agent="codex",
                mode="codex",
                executable=str(fake),
                source_root=installation_harness.REPO_ROOT,
                evidence_dir=root / "evidence",
                timeout_seconds=2.0,
                transcript_format="jsonl",
                workspace_dir=root / "workspace",
            )
            self.assertEqual(result.status, "AUTH_FAILURE")
            self.assertFalse(result.oracle_passed)

    def test_timeout_is_a_failure_with_partial_transcript(self):
        timeout_agent = """
        import json
        import sys
        import time
        sys.stdin.read()
        print(json.dumps({"type": "session.started"}), flush=True)
        time.sleep(5)
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = self.make_fake(root, timeout_agent)
            result = installation_harness.run_installation(
                agent="codex",
                mode="codex",
                executable=str(fake),
                source_root=installation_harness.REPO_ROOT,
                evidence_dir=root / "evidence",
                timeout_seconds=0.1,
                transcript_format="jsonl",
                workspace_dir=root / "workspace",
            )
            self.assertEqual(result.status, "TIMEOUT")
            self.assertTrue(result.timed_out)
            self.assertTrue((Path(result.evidence_dir) / "transcript.jsonl").is_file())

    def test_evidence_inside_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                installation_harness._ensure_separate_paths(
                    root / "target",
                    root / "target" / "evidence",
                )


if __name__ == "__main__":
    unittest.main()
