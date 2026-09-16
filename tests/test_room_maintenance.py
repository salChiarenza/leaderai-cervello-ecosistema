"""Prove dell'espansione: responsabilita' ereditata e controlli eseguibili."""
import json
import tempfile
import unittest
import subprocess
from types import SimpleNamespace
from unittest.mock import patch
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

    def test_native_maintenance_oracle_rejects_moving_duplicates_to_a_new_archive(self):
        from tests.room_growth_live import notes_reconciled
        notes = self.room / "appunti.md"
        original = "# Appunti\n\n## 29/08/2026\n\n" + "Appunto operativo datato da conservare.\n" * 801
        notes.write_text(original)
        before = {p.relative_to(self.room).as_posix() for p in self.room.rglob("*.md")}
        self.assertFalse(all(notes_reconciled(self.room, before, "2026-08-29").values()))
        notes.write_text("# Appunti\nVedi appunti_archivio.md.\n")
        archive = self.room / "appunti_archivio.md"
        archive.write_text(original)
        self.assertFalse(all(notes_reconciled(self.room, before, "2026-08-29").values()))
        archive.unlink()
        notes.write_text("# Appunti\n\n## 29/08/2026\n\nAppunto operativo datato da conservare.\n\nAccorpate 801 occorrenze identiche.\n")
        self.assertTrue(all(notes_reconciled(self.room, before, "2026-08-29").values()))
        notes.write_text("# Appunti\n\nNessun appunto.\n")
        self.assertFalse(all(notes_reconciled(self.room, before, "2026-08-29").values()))

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

    def test_installed_maintenance_has_no_unresolved_template_marker(self):
        for folder in (".agents/skills", ".claude/skills"):
            for path in (self.root / folder).rglob("SKILL.md"):
                self.assertNotIn("{{", path.read_text(), str(path))

    def test_autonomy_uses_routine_mandate_without_suggesting_the_repairs(self):
        from tests.room_growth_live import maintenance_prompt
        prompt = maintenance_prompt()
        self.assertIn("verificatore distinto", prompt)
        self.assertIn("limiti del titolare", prompt)
        for hint in ("AUTO-01", "prima_prova", "verde", "duplicat", "puntator"):
            self.assertNotIn(hint, prompt)

    def test_growth_runtime_scopes_every_prompt_and_enables_native_review(self):
        from tests.room_growth_live import run_growth
        for agent in ("codex", "claude"):
            calls = []
            def simulated_agent(command, root, prompt, timeout):
                calls.append((command, prompt))
                (root / "amministrazione").mkdir(exist_ok=True)
                return SimpleNamespace(state="COMPLETED", return_code=0, stdout="", stderr="")
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as evidence, patch(
                    "installation_harness.execute_agent", simulated_agent):
                run_growth(agent, Path(evidence) / "result")
                self.assertEqual(len(calls), 4)
                for command, prompt in calls:
                    self.assertIn("non usare rete, altre cartelle, account o configurazioni globali", prompt)
                    if agent == "codex":
                        self.assertNotIn("--ephemeral", command)
                        self.assertIn("multi_agent", command)
                    else:
                        self.assertIn('{"autoMemoryEnabled":false}', command)
                        self.assertIn("Agent", command[command.index("--tools") + 1].split(","))

    def test_native_review_requires_own_child_reads_and_completion(self):
        from tests.room_growth_live import codex_native_review
        with tempfile.TemporaryDirectory() as logs:
            path = Path(logs) / "child.jsonl"
            meta = {"payload": {"id": "child", "cwd": str(self.root),
                "source": {"subagent": {"thread_spawn": {"parent_thread_id": "parent"}}}}}
            def command(thread, output):
                return {"type": "event_msg", "payload": {"thread_id": thread,
                    "item": {"type": "CommandExecution", "exit_code": 0,
                        "command": "cat app-iscrizioni/prima_prova.md memory/MEMORY.md app-iscrizioni/STATO_ISCRIZIONI.md", "aggregated_output": output}}}
            done = {"type": "event_msg", "payload": {"type": "task_complete", "last_agent_message": "Verificato"}}
            output = "dato ricevuto e riscontro prodotto\nColore aziendale: verde. Fonte: 01/09/2026.\n[Prova della stanza](prima_prova.md)"
            path.write_text("\n".join(map(json.dumps, [meta, command("parent", output), done])))
            found = codex_native_review("parent", self.root, logs)
            self.assertFalse(found[0]["proof_read"])
            self.assertFalse(found[0]["memory_read"])
            self.assertEqual(codex_native_review("unrelated", self.root, logs), [])
            self.assertEqual(codex_native_review("parent", self.room, logs), [])
            path.write_text("\n".join(map(json.dumps, [meta, command("child", output)])))
            self.assertIsNone(codex_native_review("parent", self.root, logs)[0]["completed"])
            path.write_text("\n".join(map(json.dumps, [meta, command("child", output), done])))
            found = codex_native_review("parent", self.root, logs)[0]
            self.assertTrue(found["completed"] and found["proof_read"] and found["memory_read"])
            self.assertTrue(found.get("verified"), "Manca la prova delle tre letture prima della conclusione")
            argv = command("child", output)
            argv["payload"]["item"]["command"] = ["/bin/zsh", "-c", argv["payload"]["item"]["command"]]
            message = {"type": "event_msg", "payload": {"thread_id": "child", "item": {
                "type": "SubAgentActivity", "kind": "interacted", "agent_thread_id": "parent"}}}
            path.write_text("\n".join(map(json.dumps, [meta, argv, message, done])))
            self.assertTrue(codex_native_review("parent", self.root, logs)[0]["verified"])
            path.write_text("\n".join(map(json.dumps, [meta, done, command("child", output)])))
            self.assertFalse(codex_native_review("parent", self.root, logs)[0]["verified"])

            mutation = command("child", "")
            mutation["payload"]["item"]["command"] = "sed -i '' 's/rosso/verde/' memory/MEMORY.md"
            path.write_text("\n".join(map(json.dumps, [meta, mutation, command("child", output), done])))
            self.assertFalse(codex_native_review("parent", self.root, logs)[0]["verified"],
                "Il revisore che modifica via shell non e' indipendente")
            fake = command("child", output)
            fake["payload"]["item"]["command"] = "echo 'dato ricevuto e riscontro prodotto'"
            path.write_text("\n".join(map(json.dumps, [meta, fake, done])))
            self.assertFalse(codex_native_review("parent", self.root, logs)[0]["verified"])

    def test_review_shell_fails_closed_on_writes_and_unknown_execution(self):
        from tests.room_growth_live import review_command_readonly
        for command in ("cat memory/MEMORY.md", "sed -n '1,100p' memory/MEMORY.md",
                        "/bin/zsh -lc 'git diff -- memory/MEMORY.md'", "cat a.md | head -40",
                        ["/bin/zsh", "-lc", "cat memory/MEMORY.md"],
                        "GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git diff HEAD",
                        'TMPDIR="$PWD/.agent" PYTHONDONTWRITEBYTECODE=1 bash .agent/hooks/guardiano_stanze.sh --misura',
                        'bash .agent/hooks/guardiano_stanze.sh --misura; echo "EXIT_CODE=$?"',
                        "git log --oneline -10; echo '---'; git diff --stat",
                        "find . -path './.git' -prune -o -type f -print | sort", "ls .agent 2>&1",
                        'grep -rn "prima-prova-vecchia" . 2>/dev/null'):
            self.assertTrue(review_command_readonly(command), command)
        for command in ("sed -i '' 's/a/b/' a.md", "sed -n '1w backup' a.md",
                        "cat a.md > a.md", "cat $(touch a.md)",
                        "grep -rn parola . 2>/dev/null-copy", "grep -rn parola . 2>errori.txt",
                        "python3 check.py", "rg --pre ./rewrite a.md", "./cat a.md",
                        "git diff --output=a.md", "cat a.md &", "cat a.md; bash script.sh",
                        "bash .agent/hooks/guardiano_stanze.sh", "GIT_CONFIG_GLOBAL=other git diff",
                        "find . -exec touch a.md ';'", "sort a.md -o a.md", "find . -delete",
                        "printf -v PATH /tmp/programmi; cat a.md",
                        'TMPDIR="$(touch a.md)" bash .agent/hooks/guardiano_stanze.sh --misura'):
            self.assertFalse(review_command_readonly(command), command)
        from tests.room_growth_live import review_reads
        forged = "cat memory/MEMORY.md; echo 'dato ricevuto e riscontro prodotto' app-iscrizioni/prima_prova.md"
        self.assertFalse(review_reads(forged, "dato ricevuto e riscontro prodotto", self.root)["proof_read"])

    def autonomy_case(self, variant="valid"):
        from tests.room_growth_live import run_autonomy
        baseline = []
        def simulated_agent(command, root, prompt, timeout):
            # Il caso pronto porta gia' il difetto da riparare: se manca, il
            # revisore starebbe confrontando con il template dell'installatore.
            baseline.append("prima-prova-vecchia.md" in (root / "app-iscrizioni/STATO_ISCRIZIONI.md").read_text())
            source = root / "app-iscrizioni/STATO_ISCRIZIONI.md"
            source.write_text(source.read_text().replace("prima-prova-vecchia.md", "prima_prova.md"))
            memory = root / "memory/MEMORY.md"
            memory.write_text("# Memoria\n- Colore aziendale: verde. Fonte: 01/09/2026.\n")
            work = root / "ecosystem-check/STATO.md"
            work.write_text(work.read_text().replace("- Stato: ASSEGNATA", "- Stato: CHIUSA"))
            if variant == "empty_directory":
                (root / "cartella-inutile").mkdir()
            def event(block, parent=None):
                return {"parent_tool_use_id": parent, "message": {"content": [block]}}
            completed = event({"type": "tool_result", "tool_use_id": "review", "content": "Verificato"})
            background = variant.startswith("background_")
            events = [event({"type": "tool_use", "id": "review", "name": "Agent", "input": {"run_in_background": background}})]
            if background:
                events.append(event({"type": "tool_result", "tool_use_id": "review", "content": "Async agent launched successfully."}))
            if variant == "completion_before_reads":
                events.append(completed)
            for i, name in enumerate(("app-iscrizioni/STATO_ISCRIZIONI.md", "app-iscrizioni/prima_prova.md", "memory/MEMORY.md")):
                parent = "unrelated" if variant == "unrelated_child" else "review"
                content = (root / name).read_text()
                if variant == "stale_source" and i == 0:
                    content = content.replace("prima_prova.md", "prima-prova-vecchia.md")
                if variant == "no_reads":
                    continue
                events += [event({"type": "tool_use", "name": "Read", "id": f"read-{i}",
                    "input": {"file_path": str(root / name)}}, parent),
                    event({"type": "tool_result", "tool_use_id": f"read-{i}", "content": content}, parent)]
            if variant == "reviewer_writes":
                events.append(event({"type": "tool_use", "name": "Edit", "id": "write", "input": {}}, "review"))
            if variant == "reviewer_shell_writes":
                events.insert(1, event({"type": "tool_use", "name": "Bash", "id": "write",
                    "input": {"command": "sed -i '' 's/rosso/verde/' memory/MEMORY.md"}}, "review"))
            if background and variant != "background_ack_only":
                events.append({"type": "system", "subtype": "task_notification", "tool_use_id": "review",
                    "status": "failed" if variant == "background_failed" else "completed", "summary": "Verificato"})
            elif not background and variant != "completion_before_reads":
                events.append(completed)
            return SimpleNamespace(state="COMPLETED", return_code=0, stderr="",
                stdout="\n".join(map(json.dumps, events)))
        with tempfile.TemporaryDirectory() as evidence, patch("behavior_harness.execute_agent", simulated_agent):
            report = run_autonomy("claude", Path(evidence) / "result")
        return report, baseline

    def test_autonomy_baseline_is_the_ready_case_not_the_installer(self):
        report, baseline = self.autonomy_case()
        self.assertEqual(baseline, [True], "Il revisore deve confrontare con il caso pronto, non con il template iniziale")
        self.assertTrue(report["passed"], report)

    def test_claude_background_review_waits_for_runtime_completion(self):
        report, _ = self.autonomy_case("background_valid")
        self.assertTrue(report["checks"]["revisore_distinto_eseguito"], report)
        for variant in ("background_ack_only", "background_failed"):
            report, _ = self.autonomy_case(variant)
            self.assertFalse(report["checks"]["revisore_distinto_eseguito"], report)

    def test_autonomy_rejects_a_new_empty_directory(self):
        report, _ = self.autonomy_case("empty_directory")
        self.assertFalse(report["passed"], report)

    def test_claude_review_requires_own_current_reads_before_completion(self):
        for variant in ("no_reads", "unrelated_child", "stale_source", "completion_before_reads", "reviewer_writes", "reviewer_shell_writes"):
            with self.subTest(variant=variant):
                report, _ = self.autonomy_case(variant)
                self.assertFalse(report["checks"]["revisore_distinto_eseguito"], report)
