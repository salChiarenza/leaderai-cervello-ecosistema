import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import installation_harness
from tests import gate


class GateTest(unittest.TestCase):
    def test_quick_fails_if_discovery_returns_zero_tests(self):
        result = gate.run_quick(
            stream=io.StringIO(),
            suite=unittest.TestSuite(),
        )
        self.assertEqual(result.status, "ZERO_TESTS")
        self.assertEqual(result.tests_run, 0)
        self.assertFalse(result.successful)

    def test_quick_passes_a_nonempty_green_suite(self):
        class PassingTest(unittest.TestCase):
            def runTest(self):
                self.assertTrue(True)

        result = gate.run_quick(
            stream=io.StringIO(),
            suite=unittest.TestSuite([PassingTest()]),
        )
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.tests_run, 1)
        self.assertTrue(result.successful)

    def test_quick_treats_skip_as_failure(self):
        class SkippedTest(unittest.TestCase):
            @unittest.skip("skip controllato")
            def runTest(self):
                self.fail("non deve partire")

        result = gate.run_quick(
            stream=io.StringIO(),
            suite=unittest.TestSuite([SkippedTest()]),
        )
        self.assertEqual(result.status, "SKIPPED_TESTS")
        self.assertEqual(result.skipped, 1)
        self.assertFalse(result.successful)

    def test_release_requires_both_agents_and_rejects_unknown(self):
        self.assertEqual(
            gate.parse_agents("codex,claude"),
            ("codex", "claude"),
        )
        with self.assertRaises(ValueError):
            gate.parse_agents("codex")
        with self.assertRaises(ValueError):
            gate.parse_agents("codex,claude,gemini")

    def test_live_gate_propagates_cli_auth_timeout_and_oracle_failures(self):
        behavior_results = [
            SimpleNamespace(status="PASS"),
            SimpleNamespace(status="TIMEOUT"),
        ]
        install_result = installation_harness.InstallationResult(
            agent="codex",
            mode="codex",
            status="AUTH_FAILURE",
            return_code=3,
            timed_out=False,
            executable_found=True,
            oracle_passed=False,
            evidence_dir="/tmp/install-evidence",
            workspace_dir="$TEMPORARY_WORKSPACE",
            target_dir="$TEMPORARY_TARGET",
            duration_seconds=0.1,
            error="auth",
        )
        with tempfile.TemporaryDirectory() as tmp, mock.patch(
            "behavior_harness.run_harness",
            return_value=(Path(tmp) / "behavior-evidence", behavior_results),
        ), mock.patch(
            "installation_harness.run_installation",
            return_value=install_result,
        ):
            entries = gate.run_release_live(
                agents=("codex",),
                evidence_root=Path(tmp) / "release",
                timeout_seconds=1.0,
            )

        self.assertEqual(
            [entry["status"] for entry in entries],
            ["TIMEOUT", "AUTH_FAILURE", "PRECONDITION_FAILED"],
        )
        self.assertFalse(any(entry["passed"] for entry in entries))

    def test_release_cannot_pass_with_installation_but_failed_autonomy(self):
        result = installation_harness.InstallationResult(
            agent="claude", mode="claude", status="PASS", return_code=0,
            timed_out=False, executable_found=True, oracle_passed=True,
            evidence_dir="/tmp/simulated", workspace_dir="$TEMPORARY_WORKSPACE",
            target_dir="$TEMPORARY_TARGET", duration_seconds=0.1, error=None)
        with tempfile.TemporaryDirectory() as tmp, mock.patch(
            "behavior_harness.run_harness", return_value=(Path(tmp), [SimpleNamespace(status="PASS")])
        ), mock.patch("installation_harness.run_installation", return_value=result), mock.patch(
            "tests.room_growth_live.run_autonomy", return_value={"passed": False,
                "checks": {"revisore_distinto_eseguito": False}}
        ) as autonomy:
            entries = gate.run_release_live(agents=("claude",), evidence_root=Path(tmp),
                timeout_seconds=1, executables={"claude": "fake-claude"})
        self.assertEqual(entries[-1]["kind"], "autonomy")
        self.assertEqual(entries[-1]["status"], "AUTONOMY_FAILURE")
        self.assertFalse(entries[-1]["passed"])
        self.assertEqual(autonomy.call_args.kwargs["executable"], "fake-claude")

    def test_main_accepts_the_complete_six_pass_release_matrix(self):
        entries = [
            {
                "kind": kind,
                "agent": agent,
                "status": "PASS",
                "passed": True,
            }
            for agent in ("codex", "claude")
            for kind in ("behavior", "manual_installation", "autonomy")
        ]
        quick = gate.QuickResult(
            status="PASS", tests_run=1, failures=0, errors=0,
            skipped=0, successful=True,
        )
        with tempfile.TemporaryDirectory() as tmp, mock.patch(
            "tests.gate.run_quick", return_value=quick
        ), mock.patch(
            "tests.gate.run_release_live", return_value=entries
        ):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(
                    gate.main([
                        "--release", "--agents", "codex,claude",
                        "--evidence-dir", tmp,
                    ]),
                    0,
                )

    def test_release_matrix_rejects_missing_duplicate_and_invalid_entries(self):
        entries = [
            {"kind": kind, "agent": agent, "status": "PASS", "passed": True}
            for agent in ("codex", "claude")
            for kind in ("behavior", "manual_installation", "autonomy")
        ]
        self.assertTrue(gate.release_matrix_passes(entries))

        cases = {
            "missing": entries[:-1],
            "duplicate": entries[:-1] + [entries[0]],
            "status": [
                *entries[:-1],
                {**entries[-1], "status": "TIMEOUT", "passed": False},
            ],
            "passed": [{**entry, "passed": False} if index == 0 else entry
                       for index, entry in enumerate(entries)],
            "unknown_kind": [
                *entries[:-1], {**entries[-1], "kind": "unexpected"},
            ],
            "unknown_agent": [
                *entries[:-1], {**entries[-1], "agent": "gemini"},
            ],
        }
        for label, invalid_entries in cases.items():
            with self.subTest(label=label):
                self.assertFalse(gate.release_matrix_passes(invalid_entries))


if __name__ == "__main__":
    unittest.main()
