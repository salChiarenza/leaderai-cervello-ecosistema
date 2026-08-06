import json
import stat
import tempfile
import textwrap
import unittest
from pathlib import Path

import behavior_harness


FAKE_SUCCESS = """\
#!/usr/bin/env python3
import json
import pathlib
import sys

prompt = sys.stdin.read()
root = pathlib.Path.cwd()
if "Cliente Aurora" in prompt:
    output = root / "relazioni" / "output" / "scheda-operativa.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "# Scheda operativa Cliente Aurora\\n\\n"
        "- Relazione: REL-2026-017\\n"
        "- Bisogno: Laboratorio operativo di 45 minuti\\n"
        "- Data: 03/08/2026\\n",
        encoding="utf-8",
    )
elif "ORD-042" in prompt:
    output = root / "operazioni" / "output" / "piano-consegna.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "# Piano ORD-042\\n\\n"
        "- Responsabile: Giulia R.\\n"
        "- Scadenza: 07/08/2026\\n"
        "- Blocco: approvazione legale della clausola privacy\\n",
        encoding="utf-8",
    )
elif prompt.strip() == "Crea la Brand Identity":
    output = root / "identita" / "output" / "brand-identity.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "# Brand Identity\\n\\n"
        "- Codice: AVORIO-37\\n"
        "- Promessa: Accoglienza sartoriale senza pressione\\n"
        "- Materia: Noce caldo e champagne opaco\\n",
        encoding="utf-8",
    )
else:
    raise SystemExit(9)

if "--output-format" in sys.argv and "json" in sys.argv:
    print(json.dumps({"type": "result", "result": "completato"}))
else:
    print(json.dumps({"type": "session.started", "session_id": "fake-new"}))
    print(json.dumps({"type": "result", "result": "completato"}))
"""

FAKE_FAILURE = """\
#!/usr/bin/env python3
import sys
sys.stdin.read()
print('{"type":"error","message":"errore controllato"}')
raise SystemExit(7)
"""

FAKE_AUTH_FAILURE = """\
#!/usr/bin/env python3
import sys
sys.stdin.read()
print('{"error":"authentication_failed","message":"Not logged in"}')
raise SystemExit(1)
"""

FAKE_TIMEOUT = """\
#!/usr/bin/env python3
import sys
import time
sys.stdin.read()
print('{"type":"session.started"}', flush=True)
time.sleep(5)
"""

FAKE_BAD_ORACLE = """\
#!/usr/bin/env python3
import json
import pathlib
import sys

sys.stdin.read()
root = pathlib.Path.cwd()
(root / "scheda-operativa.md").write_text(
    "Corso registrato introduttivo\\n", encoding="utf-8"
)
source = root / "relazioni" / "fonti" / "cliente-aurora.md"
source.write_text("fonte alterata\\n", encoding="utf-8")
print(json.dumps({"type": "result", "result": "fatto"}))
"""


class BehaviorHarnessTest(unittest.TestCase):
    def make_executable(self, root: Path, name: str, source: str) -> Path:
        executable = root / f"{name}.py"
        executable.write_text(textwrap.dedent(source), encoding="utf-8")
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
        return executable

    def run_fake(
        self,
        root: Path,
        scenario: behavior_harness.Scenario,
        executable: Path,
        *,
        agent: str = "codex",
        transcript_format: str = "jsonl",
        timeout_seconds: float = 2.0,
    ) -> behavior_harness.ScenarioResult:
        return behavior_harness.run_scenario(
            scenario=scenario,
            agent=agent,
            executable=str(executable),
            fixture=behavior_harness.DEFAULT_FIXTURE,
            evidence_dir=root / "evidence" / scenario.name,
            timeout_seconds=timeout_seconds,
            transcript_format=transcript_format,
            target_dir=root / "targets" / scenario.name,
        )

    def test_fixture_has_mother_map_three_real_rooms_and_historical_duplicates(self):
        fixture = behavior_harness.DEFAULT_FIXTURE

        self.assertTrue((fixture / "AGENTS.md").is_file())
        for room, source, historical in (
            (
                "relazioni",
                "fonti/cliente-aurora.md",
                "archivio/cliente-aurora-2024.md",
            ),
            (
                "operazioni",
                "fonti/ordine-042.md",
                "archivio/ordine-042-bozza.md",
            ),
            (
                "identita",
                "fonti/brand-verificato.md",
                "archivio/brand-superato.md",
            ),
        ):
            room_root = fixture / room
            room_map = (room_root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("vera stanza", room_map)
            self.assertTrue((room_root / source).is_file())
            self.assertTrue((room_root / historical).is_file())
            self.assertEqual(
                (room_root / "CLAUDE.md").read_text(encoding="utf-8"),
                "@AGENTS.md\n",
            )

        blocks = fixture.parent / "context_blocks"
        current = (blocks / "routing-source-current.md").read_text(
            encoding="utf-8"
        )
        lighter = (blocks / "routing-source-lighter.md").read_text(
            encoding="utf-8"
        )
        root_map = (fixture / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(root_map.count(current), 1)
        self.assertNotEqual(current, lighter)

    def test_business_prompts_contain_no_filesystem_paths(self):
        for scenario in behavior_harness.SCENARIOS.values():
            with self.subTest(scenario=scenario.name):
                self.assertNotIn("/", scenario.business_prompt)
                self.assertNotIn("\\", scenario.business_prompt)
                self.assertNotIn(".md", scenario.business_prompt)

    def test_brand_identity_prompt_is_exact_and_contains_no_harness_hints(self):
        scenario = behavior_harness.SCENARIOS["brand_identity"]

        self.assertEqual(scenario.prompt, "Crea la Brand Identity\n")
        folded = scenario.prompt.casefold()
        for forbidden in (
            "agents",
            "mappa",
            "stanza",
            "fonte",
            "output",
            "file",
            "/",
            "\\",
            ".md",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, folded)

    def test_commands_create_fresh_sessions_scoped_to_the_fixture(self):
        target = Path("/tmp/anonymous-house")
        codex = behavior_harness.build_command(
            "codex", "codex", target, "jsonl"
        )
        claude = behavior_harness.build_command(
            "claude", "claude", target, "jsonl"
        )
        claude_json = behavior_harness.build_command(
            "claude", "claude", target, "json"
        )

        self.assertIn("--ephemeral", codex)
        self.assertIn("workspace-write", codex)
        self.assertEqual(codex[codex.index("--cd") + 1], str(target))
        self.assertNotIn("resume", codex)
        self.assertNotIn("--add-dir", codex)

        self.assertIn("--no-session-persistence", claude)
        self.assertEqual(
            claude[claude.index("--tools") + 1],
            "Read,Write,Edit,Glob,Grep",
        )
        self.assertNotIn("--continue", claude)
        self.assertNotIn("--resume", claude)
        self.assertNotIn("--add-dir", claude)
        self.assertIn("--verbose", claude)
        self.assertNotIn("--verbose", claude_json)

    def test_three_independent_scenarios_pass_with_fake_jsonl_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(root, "fake-agent", FAKE_SUCCESS)

            results = [
                self.run_fake(root, scenario, executable)
                for scenario in behavior_harness.SCENARIOS.values()
            ]

            self.assertEqual(
                [result.status for result in results],
                ["PASS", "PASS", "PASS"],
            )
            for result in results:
                evidence = Path(result.evidence_dir)
                self.assertTrue((evidence / "prompt.txt").is_file())
                self.assertTrue((evidence / "transcript.jsonl").is_file())
                self.assertTrue((evidence / "manifest-pre.json").is_file())
                self.assertTrue((evidence / "manifest-post.json").is_file())
                self.assertTrue((evidence / "diff.json").is_file())
                self.assertTrue((evidence / "oracle.json").is_file())
                self.assertTrue((evidence / "observed-output.md").is_file())
                oracle = json.loads(
                    (evidence / "oracle.json").read_text(encoding="utf-8")
                )
                self.assertTrue(oracle["passed"])

    def test_json_transcript_and_redacted_command_are_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(root, "fake-claude", FAKE_SUCCESS)
            scenario = behavior_harness.SCENARIOS["relazioni_scheda"]

            result = self.run_fake(
                root,
                scenario,
                executable,
                agent="claude",
                transcript_format="json",
            )

            self.assertEqual(result.status, "PASS")
            evidence = Path(result.evidence_dir)
            transcript = json.loads(
                (evidence / "transcript.json").read_text(encoding="utf-8")
            )
            self.assertEqual(transcript["type"], "result")
            command = json.loads(
                (evidence / "command.json").read_text(encoding="utf-8")
            )
            self.assertEqual(command["cwd"], "$TARGET")
            self.assertIn("<PROMPT via stdin>", command["argv"])
            self.assertNotIn(str(root / "targets"), json.dumps(command))
            self.assertFalse(command["environment_recorded"])

    def test_multiline_json_transcript_is_preserved_as_one_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp)
            stdout = json.dumps(
                {"type": "result", "details": {"status": "ok"}},
                ensure_ascii=False,
                indent=2,
            )

            path = behavior_harness.write_transcript(evidence, stdout, "json")

            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                {"type": "result", "details": {"status": "ok"}},
            )

    def test_missing_executable_is_reported_without_model_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scenario = behavior_harness.SCENARIOS["relazioni_scheda"]

            result = self.run_fake(
                root,
                scenario,
                root / "eseguibile-che-non-esiste",
            )

            self.assertEqual(result.status, "EXECUTABLE_MISSING")
            self.assertFalse(result.executable_found)
            self.assertIsNone(result.return_code)
            self.assertTrue((Path(result.evidence_dir) / "result.json").is_file())

    def test_nonzero_return_code_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(root, "fake-failure", FAKE_FAILURE)
            scenario = behavior_harness.SCENARIOS["operazioni_consegna"]

            result = self.run_fake(root, scenario, executable)

            self.assertEqual(result.status, "RETURN_CODE_ERROR")
            self.assertEqual(result.return_code, 7)
            self.assertFalse(result.oracle_passed)

    def test_authentication_failure_is_reported_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(
                root,
                "fake-auth-failure",
                FAKE_AUTH_FAILURE,
            )
            scenario = behavior_harness.SCENARIOS["relazioni_scheda"]

            result = self.run_fake(root, scenario, executable, agent="claude")

            self.assertEqual(result.status, "AUTH_FAILURE")
            self.assertEqual(result.return_code, 1)
            self.assertFalse(result.oracle_passed)

    def test_timeout_is_reported_and_partial_transcript_is_saved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(root, "fake-timeout", FAKE_TIMEOUT)
            scenario = behavior_harness.SCENARIOS["operazioni_consegna"]

            result = self.run_fake(
                root,
                scenario,
                executable,
                timeout_seconds=0.1,
            )

            self.assertEqual(result.status, "TIMEOUT")
            self.assertTrue(result.timed_out)
            transcript = Path(result.evidence_dir) / "transcript.jsonl"
            self.assertTrue(transcript.is_file())
            records = [
                json.loads(line)
                for line in transcript.read_text(encoding="utf-8").splitlines()
            ]
            self.assertTrue(records)

    def test_oracle_rejects_root_output_and_modified_canonical_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(
                root, "fake-bad-oracle", FAKE_BAD_ORACLE
            )
            scenario = behavior_harness.SCENARIOS["relazioni_scheda"]

            result = self.run_fake(root, scenario, executable)

            self.assertEqual(result.status, "ORACLE_FAIL")
            oracle = json.loads(
                (Path(result.evidence_dir) / "oracle.json").read_text(
                    encoding="utf-8"
                )
            )
            checks = {item["name"]: item["passed"] for item in oracle["checks"]}
            self.assertFalse(checks["output_nel_percorso_proprietario"])
            self.assertFalse(checks["nessun_output_in_root_o_cartelle_generiche"])
            self.assertFalse(checks["fonti_standard_inalterate"])

    def test_context_comparison_uses_two_clean_sessions_and_classifies_one_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = self.make_executable(root, "fake-agent", FAKE_SUCCESS)
            current = (
                "- Prima di lavorare, apri la mappa della stanza proprietaria.\n"
                "- Leggi i fatti dalla fonte canonica indicata nella mappa locale.\n"
            )
            lighter = (
                "- Instrada dalla tabella, poi apri mappa locale e fonte canonica.\n"
            )
            variant = behavior_harness.InstructionVariant(
                block_id="routing-and-source",
                instruction_path="AGENTS.md",
                current_text=current,
                lighter_text=lighter,
                candidate_action="compact",
            )

            result = behavior_harness.run_context_comparison(
                scenario=behavior_harness.SCENARIOS["relazioni_scheda"],
                variant=variant,
                agent="codex",
                executable=str(executable),
                fixture=behavior_harness.DEFAULT_FIXTURE,
                evidence_dir=root / "comparison",
                timeout_seconds=2.0,
                transcript_format="jsonl",
            )

            self.assertEqual(result.classification, "ACCORPA")
            self.assertTrue(result.full.outcome_observed)
            self.assertTrue(result.lighter.outcome_observed)
            self.assertTrue(result.full.correct_sources)
            self.assertTrue(result.lighter.correct_routing)
            self.assertTrue(result.lighter.safety_preserved)
            self.assertEqual(result.full.run_status, "PASS")
            self.assertEqual(result.lighter.run_status, "PASS")
            self.assertTrue((root / "comparison" / "full" / "result.json").is_file())
            self.assertTrue((root / "comparison" / "lighter" / "result.json").is_file())
            self.assertTrue((root / "comparison" / "comparison.json").is_file())
            for variant_name in ("full", "lighter"):
                prompt = (
                    root / "comparison" / variant_name / "prompt.txt"
                ).read_text(encoding="utf-8")
                self.assertEqual(
                    prompt,
                    behavior_harness.SCENARIOS["relazioni_scheda"].business_prompt
                    + "\n",
                )
                self.assertNotIn("Orientati leggendo la mappa madre", prompt)

    def test_protected_instruction_is_never_removal_candidate_automatically(self):
        metrics = behavior_harness.ContextMetrics(
            run_status="PASS",
            outcome_observed=True,
            correct_sources=True,
            correct_routing=True,
            completed=True,
            human_correction_requests=0,
            duration_seconds=1.0,
            input_tokens=None,
            output_tokens=None,
            safety_preserved=True,
        )
        variant = behavior_harness.InstructionVariant(
            block_id="privacy",
            instruction_path="AGENTS.md",
            current_text="privacy",
            lighter_text="",
            candidate_action="remove",
            protected=True,
        )

        classification, reason = behavior_harness.classify_instruction_variant(
            variant,
            metrics,
            metrics,
        )

        self.assertEqual(classification, "MANTIENI")
        self.assertIn("non si eliminano automaticamente", reason)

    def test_single_case_cannot_candidate_an_instruction_for_removal(self):
        metrics = behavior_harness.ContextMetrics(
            run_status="PASS",
            outcome_observed=True,
            correct_sources=True,
            correct_routing=True,
            completed=True,
            human_correction_requests=0,
            duration_seconds=1.0,
            input_tokens=None,
            output_tokens=None,
            safety_preserved=True,
        )
        variant = behavior_harness.InstructionVariant(
            block_id="legacy-rule",
            instruction_path="AGENTS.md",
            current_text="regola storica",
            lighter_text="",
            candidate_action="remove",
        )

        classification, reason = behavior_harness.classify_instruction_variant(
            variant,
            metrics,
            metrics,
        )

        self.assertEqual(classification, "MANTIENI")
        self.assertIn("Un solo caso non basta", reason)

    def test_technical_failure_does_not_become_an_instruction_verdict(self):
        baseline = behavior_harness.ContextMetrics(
            run_status="PASS",
            outcome_observed=True,
            correct_sources=True,
            correct_routing=True,
            completed=True,
            human_correction_requests=0,
            duration_seconds=1.0,
            input_tokens=None,
            output_tokens=None,
            safety_preserved=True,
        )
        failed = behavior_harness.ContextMetrics(
            run_status="AUTH_FAILURE",
            outcome_observed=False,
            correct_sources=False,
            correct_routing=False,
            completed=False,
            human_correction_requests=0,
            duration_seconds=1.0,
            input_tokens=None,
            output_tokens=None,
            safety_preserved=True,
        )
        variant = behavior_harness.InstructionVariant(
            block_id="routing",
            instruction_path="AGENTS.md",
            current_text="regola",
            lighter_text="",
            candidate_action="compact",
        )

        classification, reason = behavior_harness.classify_instruction_variant(
            variant,
            baseline,
            failed,
        )

        self.assertEqual(classification, "DA COLLAUDARE")
        self.assertIn("errore tecnico", reason)

    def test_usage_is_reported_only_when_available(self):
        self.assertEqual(
            behavior_harness._usage_from_transcript(
                '{"type":"result","usage":{"input_tokens":41,"output_tokens":7}}\n'
            ),
            (41, 7),
        )
        self.assertEqual(
            behavior_harness._usage_from_transcript('{"type":"result"}\n'),
            (None, None),
        )


if __name__ == "__main__":
    unittest.main()
