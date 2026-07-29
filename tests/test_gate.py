import io
import tempfile
import unittest
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
            ["TIMEOUT", "AUTH_FAILURE"],
        )
        self.assertFalse(any(entry["passed"] for entry in entries))


if __name__ == "__main__":
    unittest.main()
