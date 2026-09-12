"""Prove dell'espansione: responsabilita' ereditata e controlli eseguibili."""
import json
import tempfile
import unittest
from pathlib import Path

from templates import ARCHIVE_POLICY as policy
from tests import test_guardiano_stanze_stop as fixture_module


class RoomMaintenanceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.fixture = fixture_module.GuardianoStanzeStopTest()
        self.root = self.fixture.install(self.tmp.name)
        self.room = self.fixture.register_room(self.root, "amministrazione")

    def findings(self):
        return policy.maintenance_findings(self.root)

    def test_birth_requires_maintenance_even_in_consolidated_house(self):
        path = self.room / "AGENTS.md"
        text = path.read_text()
        import re
        path.write_text(re.sub(r"(?ms)^## Manutenzione\n.*?(?=^## |\Z)", "", text))
        self.assertIn("ROOM_MAINTENANCE_MISSING", [x[0] for x in self.findings()])
        result = self.fixture.run_guard(self.root)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("manutenzione", result.stderr.lower())
        root_map = self.root / "AGENTS.md"
        root_map.write_text(root_map.read_text() + "\n- Contratto di stanza: consolidato\n")
        self.assertIn("ROOM_MAINTENANCE_MISSING", [x[0] for x in self.findings()])

    def test_subfolder_inherits_without_adding_agent_or_schedule(self):
        before = sorted(p.relative_to(self.root).as_posix() for d in (".agents", ".claude", ".codex") for p in (self.root / d).rglob("*") if p.is_file())
        child = self.room / "banca"
        child.mkdir()
        (child / "estratto.csv").write_text("id,importo\nsimulato-1,100\n")
        self.assertEqual(policy.maintenance_owner(self.root, "amministrazione/banca/estratto.csv"), "amministrazione")
        self.assertEqual(policy.maintenance_owner(self.root, ".codex/hooks.json"), "ecosystem-check")
        after = sorted(p.relative_to(self.root).as_posix() for d in (".agents", ".claude", ".codex") for p in (self.root / d).rglob("*") if p.is_file())
        self.assertEqual(before, after)

    def test_existing_but_empty_receipt_cannot_pass(self):
        (self.room / "STATO.md").write_text("")
        self.assertIn("ROOM_BIRTH_PROOF_MISSING", [x[0] for x in self.findings()])
        self.assertEqual(self.fixture.run_guard(self.root).returncode, 2)

    def test_removed_result_breaks_the_birth_proof(self):
        (self.room / "prima_prova.md").unlink()
        self.assertIn("ROOM_BIRTH_PROOF_FILE", [x[0] for x in self.findings()])

    def test_missing_receipt_destination_blocks(self):
        p = self.room / "AGENTS.md"
        p.write_text(p.read_text().replace("- Esiti: `STATO.md`", "- Esiti: `mancante.md`"))
        self.assertIn("ROOM_MAINTENANCE_EVIDENCE", [x[0] for x in self.findings()])

    def test_disabled_or_fake_hook_cannot_count_as_active(self):
        p = self.root / ".codex/hooks.json"
        data = json.loads(p.read_text())
        data["hooks"]["Stop"] = [{"hooks": [{"type": "command", "command": "echo guardiano_stanze.sh"}]}]
        p.write_text(json.dumps(data))
        self.assertIn("MAINTENANCE_HOOK_UNWIRED", [x[0] for x in self.findings()])

    def test_wrong_house_hook_or_absent_engine_config_is_reported(self):
        p = self.root / ".codex/hooks.json"
        data = json.loads(p.read_text())
        data["hooks"]["Stop"] = [{"hooks": [{"type": "command", "command": "bash /altra-casa/.agent/hooks/guardiano_stanze.sh"}]}]
        p.write_text(json.dumps(data))
        self.assertIn("MAINTENANCE_HOOK_UNWIRED", [x[0] for x in self.findings()])
        p.unlink()
        self.assertIn("MAINTENANCE_HOOK_UNWIRED", [x[0] for x in self.findings()])

    def test_oversized_md_and_broken_hook_are_both_visible(self):
        (self.room / "lavoro.md").write_text("contenuto\n" * 801)
        (self.root / ".agent/hooks/guardiano_stanze.sh").write_text("")
        self.assertTrue(any("lavoro.md" in x for x in policy.scan(self.root)))
        self.assertIn("MAINTENANCE_HOOK_MISSING", [x[0] for x in self.findings()])

    def test_guardian_itself_records_only_a_complete_hook_event(self):
        import subprocess
        path = self.root / ".agent/guardiano-ultimo-evento.json"
        self.fixture.run_guard(self.root)
        self.assertFalse(path.exists())
        payload = {"hook_event_name": "Stop", "session_id": "sessione-prova", "cwd": str(self.root)}
        result = subprocess.run(["bash", str(self.root / ".agent/hooks/guardiano_stanze.sh")], input=json.dumps(payload), text=True, capture_output=True, cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(path.read_text())["esito"], "PASSA")
        (self.room / "prima_prova.md").unlink()
        subprocess.run(["bash", str(self.root / ".agent/hooks/guardiano_stanze.sh")], input=json.dumps(payload), text=True, capture_output=True, cwd=self.root)
        self.assertEqual(json.loads(path.read_text())["esito"], "BLOCCO")

    def test_native_oracle_accepts_extra_columns_but_rejects_wrong_amounts(self):
        from tests.room_growth_live import quotes_reconciled
        text = "| PRATICA-A | 100 | 100 | 0 | pagata | BANCA-001 |\n| PRATICA-B | 200 | 0 | 200 | non pagata |"
        self.assertTrue(quotes_reconciled(text))
        self.assertFalse(quotes_reconciled(text.replace("100 | 0 | pagata", "90 | 10 | pagata")))
        self.assertFalse(quotes_reconciled(text + "\n| PRATICA-A | 100 | 0 | 100 |"))

    def test_receipt_requires_independent_native_session_and_no_manual_writer(self):
        from tests.room_growth_live import native_session_matches
        receipt = {"sessione": "native-1"}
        start = json.dumps({"type": "thread.started", "thread_id": "native-1"})
        self.assertTrue(native_session_matches("codex", start, receipt))
        self.assertFalse(native_session_matches("codex", start, {"sessione": "inventata"}))
        for command in ["python3 -c 'fake_receipt()'", "cat input > .agent/guardiano-ultimo-evento.json", "cat input; bash guard.sh", "cat $(touch receipt)"]:
            transcript = start + "\n" + json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": command}})
            self.assertFalse(native_session_matches("codex", transcript, receipt))
        self.assertFalse(native_session_matches("codex", start + "\n" + json.dumps({"item": {"type": "file_change"}}), receipt))
        claude = json.dumps({"type": "result", "session_id": "native-1"})
        self.assertTrue(native_session_matches("claude", claude, receipt))
        manual = json.dumps({"message": {"content": [{"type": "tool_use", "name": "Write", "input": {}}]}})
        self.assertFalse(native_session_matches("claude", claude + "\n" + manual, receipt))

    def test_maintenance_does_not_execute_declared_commands(self):
        p = self.room / "AGENTS.md"
        p.write_text(p.read_text() + "\n<!-- rm -rf / -->\n")
        self.assertEqual(self.findings(), [])
