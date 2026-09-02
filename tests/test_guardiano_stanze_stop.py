import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

import leaderai_setup


class GuardianoStanzeStopTest(unittest.TestCase):
    def insert_before(self, path: Path, marker: str, row: str) -> None:
        content = path.read_text(encoding="utf-8")
        self.assertIn(marker, content)
        path.write_text(
            content.replace(marker, row.rstrip() + "\n\n" + marker, 1),
            encoding="utf-8",
        )

    def register_root_room(self, target: Path, name: str) -> None:
        self.insert_before(
            target / "AGENTS.md",
            "La prima cella di ogni stanza usa il formato",
            f"| [{name.title()}]({name}) | Piano | - | - | - | - | - | `{name}/AGENTS.md` | {name.title()} | Boss dell'Ecosistema |",
        )

    def register_root_owned(
        self,
        target: Path,
        name: str,
        classification: str,
        registry: str,
    ) -> None:
        self.insert_before(
            target / "AGENTS.md",
            "Questa tabella possiede capacita'",
            f"| `{name}` | {classification} | Uso verificato | `{registry}` |",
        )

    def register_asset_detail(self, target: Path, name: str) -> None:
        self.insert_before(
            target / "ecosistema" / "ASSET.md",
            "## Regola di aggiornamento",
            f"| {name} | Capacita | `{name}` | Tutte | Uso verificato | ATTIVO | Test locale | Nessuno |",
        )

    def register_source_detail(self, target: Path, name: str) -> None:
        self.insert_before(
            target / "ecosistema" / "FONTI.md",
            "## Fonti da collegare",
            f"| {name} | `{name}` | Marketing | Test locale | ATTIVO |",
        )

    def install(self, parent: str) -> Path:
        target = Path(parent) / "EcosistemaAI-Studio-Test"
        leaderai_setup.run_setup(
            target,
            "Studio Test",
            "both",
            claude_user_settings_path=Path(parent) / "claude-user-settings.json",
        )
        return target

    def run_guard(self, target: Path, *, active: bool = False) -> subprocess.CompletedProcess[str]:
        payload = {
            "hook_event_name": "Stop",
            "stop_hook_active": active,
            "cwd": str(target),
        }
        return subprocess.run(
            ["bash", str(target / ".agent" / "hooks" / "guardiano_stanze.sh")],
            cwd=target,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )

    def register_room(self, target: Path, name: str = "marketing") -> Path:
        room = target / name
        room.mkdir()
        room_map = (leaderai_setup.ROOT / "templates" / "STANZA_AGENTS.md").read_text(
            encoding="utf-8"
        )
        replacements = {
            "{{room_name}}": name,
            "{{room_purpose}}": "Governa il marketing dello studio.",
            "{{room_business_responsibility}}": "Mantiene piano e decisioni marketing.",
            "{{room_contents}}": "NESSUNA SOTTOCARTELLA",
            "{{room_sources}}": "`STATO.md`",
            "{{room_outputs}}": "Piano marketing verificato.",
            "{{room_operating_source}}": "STATO.md",
            "{{room_business_source}}": "NON APPLICABILE: usa la fonte operativa.",
            "{{room_capabilities}}": "Nessuna capacita separata.",
            "{{room_upstream}}": "Boss dell'Ecosistema.",
            "{{room_downstream}}": "Nessuna stanza a valle.",
        }
        for placeholder, value in replacements.items():
            room_map = room_map.replace(placeholder, value)
        (room / "AGENTS.md").write_text(room_map, encoding="utf-8")
        (room / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
        source = (leaderai_setup.ROOT / "templates" / "STANZA_FONTE.md").read_text(
            encoding="utf-8"
        )
        source_replacements = {
            "{{room_name}}": name,
            "{{room_current_state}}": "Operativo.",
            "{{room_next_step}}": "Verificare il piano.",
            "{{room_decisions}}": "Una fonte unica.",
            "{{room_deadlines}}": "Nessuna.",
        }
        for placeholder, value in source_replacements.items():
            source = source.replace(placeholder, value)
        (room / "STATO.md").write_text(source, encoding="utf-8")
        self.register_root_room(target, name)
        return room

    def test_clean_house_can_close(self):
        """Break caught: the installed guard must not block a conforming house."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "")

    @unittest.skipUnless(hasattr(os, "chflags") and hasattr(stat, "UF_HIDDEN"), "flag Finder solo su macOS/BSD")
    def test_hidden_path_blocks_first_stop_until_visible_again(self):
        """Caso reale LeaderAI 01/09/2026: cartelle nascoste 'per una scena' e mai
        fatte ricomparire. L'Ispettore le vedeva, il guardiano di chiusura no."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            hidden = target / "ecosystem-check"
            os.chflags(hidden, stat.UF_HIDDEN)
            try:
                result = self.run_guard(target)
                self.assertEqual(result.returncode, 2)
                self.assertIn("ecosystem-check - nascosto al proprietario", result.stderr)
            finally:
                os.chflags(hidden, 0)

            self.assertEqual(self.run_guard(target).returncode, 0)

    def test_extra_file_in_common_cabinet_blocks_first_stop(self):
        """Break caught: business output must never remain inside ecosistema/."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            extra = target / "ecosistema" / "BOZZA_MARKETING.md"
            extra.write_text("# Bozza\n", encoding="utf-8")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("ecosistema/BOZZA_MARKETING.md", result.stderr)

    def test_unregistered_top_level_folder_blocks_first_stop(self):
        """Break caught: a new folder cannot bypass room or root-owner registration."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            (target / "marketing").mkdir()
            (target / "marketing" / "PIANO.md").write_text(
                "# Piano\n",
                encoding="utf-8",
            )

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing", result.stderr)

    def test_unregistered_top_level_file_blocks_first_stop(self):
        """Break caught: a loose business file cannot bypass ownership routing."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            (target / "PIANO_MARKETING.md").write_text(
                "# Piano\n",
                encoding="utf-8",
            )

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("PIANO_MARKETING.md", result.stderr)

    def test_partial_room_without_bridge_blocks_first_stop(self):
        """Break caught: a room cannot exist with only half of its door contract."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = target / "marketing"
            room.mkdir()
            (room / "AGENTS.md").write_text(
                "# Marketing\n",
                encoding="utf-8",
            )
            self.register_root_room(target, "marketing")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/CLAUDE.md", result.stderr)

    def test_present_but_incomplete_room_map_blocks_first_stop(self):
        """Break caught: a file named AGENTS.md is not automatically a room map."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = target / "marketing"
            room.mkdir()
            (room / "AGENTS.md").write_text("# Marketing\n", encoding="utf-8")
            (room / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            self.register_root_room(target, "marketing")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/AGENTS.md", result.stderr)

    def test_room_map_with_all_headings_but_empty_sections_blocks(self):
        """Break caught: headings alone do not satisfy the room contract."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = target / "marketing"
            room.mkdir()
            headings = [
                "Stato corrente e prossimo passo",
                "Scopo",
                "Responsabilita business",
                "Organigramma",
                "Dentro",
                "Fonti",
                "Output",
                "Fonte operativa",
                "Fonte business editabile",
                "Capacita",
                "A monte",
                "A valle",
                "Dove scrivere",
                "Regole",
            ]
            content = "# Marketing\n\n" + "\n\n".join(
                f"## {heading}" for heading in headings
            )
            content = content.replace(
                "## Fonte operativa\n\n## Fonte business editabile",
                "## Fonte operativa\n\n- `STATO.md`\n\n## Fonte business editabile",
            )
            (room / "AGENTS.md").write_text(content + "\n", encoding="utf-8")
            (room / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            source = (leaderai_setup.ROOT / "templates" / "STANZA_FONTE.md").read_text(
                encoding="utf-8"
            )
            for placeholder, value in {
                "{{room_name}}": "marketing",
                "{{room_current_state}}": "Operativo.",
                "{{room_next_step}}": "Verifica.",
                "{{room_decisions}}": "Una fonte.",
                "{{room_deadlines}}": "Nessuna.",
            }.items():
                source = source.replace(placeholder, value)
            (room / "STATO.md").write_text(source, encoding="utf-8")
            self.register_root_room(target, "marketing")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("sezione senza contenuto", result.stderr)

    def test_room_boilerplate_cannot_replace_business_values(self):
        """Break caught: template instructions are not client room content."""
        cases = {
            "Responsabilita business": (
                "Mantiene piano e decisioni marketing.\n\n",
                "",
            ),
            "Dentro": (
                "- NESSUNA SOTTOCARTELLA\n",
                "- \n",
            ),
            "Fonte business editabile": (
                "- NON APPLICABILE: usa la fonte operativa.\n",
                "- materiale business\n",
            ),
        }
        for heading, (before, after) in cases.items():
            with self.subTest(heading=heading), tempfile.TemporaryDirectory() as tmp:
                target = self.install(tmp)
                room = self.register_room(target)
                room_map = room / "AGENTS.md"
                content = room_map.read_text(encoding="utf-8")
                self.assertIn(before, content)
                room_map.write_text(content.replace(before, after, 1), encoding="utf-8")

                result = self.run_guard(target)

                self.assertEqual(result.returncode, 2)
                self.assertIn(heading, result.stderr)

    def test_declared_room_child_must_exist(self):
        """Break caught: the map cannot invent a child folder."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = self.register_room(target)
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "NESSUNA SOTTOCARTELLA",
                    "`fantasma/` - cartella dichiarata ma assente",
                ),
                encoding="utf-8",
            )

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/fantasma", result.stderr)

    def test_declared_business_source_must_exist_inside_room(self):
        """Break caught: the editable business source must be a real local file."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = self.register_room(target)
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "NON APPLICABILE: usa la fonte operativa.",
                    "`FONTE_BUSINESS.md`",
                ),
                encoding="utf-8",
            )

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/FONTE_BUSINESS.md", result.stderr)

    def test_undeclared_direct_subfolder_blocks_first_stop(self):
        """Break caught: direct room contents must be owned by the local map."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = self.register_room(target)
            campaign = room / "campagne"
            campaign.mkdir()
            (campaign / "piano.md").write_text("# Piano\n", encoding="utf-8")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/campagne", result.stderr)

    def test_declared_direct_subfolder_and_complete_map_can_close(self):
        """Break caught: a legitimate room must not be blocked by the stronger gate."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = self.register_room(target)
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "NESSUNA SOTTOCARTELLA",
                    "`campagne/` - campagne marketing attive",
                ),
                encoding="utf-8",
            )
            campaign = room / "campagne"
            campaign.mkdir()
            (campaign / "piano.md").write_text("# Piano\n", encoding="utf-8")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_declared_operating_source_blocks_first_stop(self):
        """Break caught: a room map cannot point to a source that does not exist."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = self.register_room(target)
            (room / "STATO.md").unlink()

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/STATO.md", result.stderr)

    def test_existing_but_incomplete_operating_source_blocks_first_stop(self):
        """Break caught: an arbitrary file cannot masquerade as room state."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            room = self.register_room(target)
            (room / "STATO.md").write_text("# Appunti\n", encoding="utf-8")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("marketing/STATO.md", result.stderr)
            self.assertIn("Stato corrente", result.stderr)

    def test_oversized_agent_chat_blocks_first_stop(self):
        """Break caught: the coordination board cannot become another archive."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            (target / "AGENT_CHAT.md").write_text(
                "# Riga\n" * 351,
                encoding="utf-8",
            )

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("AGENT_CHAT.md", result.stderr)

    def test_registered_root_owned_capability_is_not_forced_into_a_room(self):
        """Break caught: the guard must preserve legitimate root-owned capabilities."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            capability = target / "asset-kadence"
            capability.mkdir()
            (capability / "README.md").write_text("# Kadence\n", encoding="utf-8")

            self.register_root_owned(
                target,
                "asset-kadence",
                "CAPACITA",
                "ecosistema/ASSET.md",
            )
            self.register_asset_detail(target, "asset-kadence")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_dependency_trees_are_not_scanned_as_business_structure(self):
        """Break caught: package caches cannot create false structural blockers."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            capability = target / "asset-kadence"
            package = capability / "node_modules" / "pacchetto"
            package.mkdir(parents=True)
            (package / "README_final.md").write_text("cache\n", encoding="utf-8")
            (capability / ".venv" / "cache").mkdir(parents=True)
            self.register_root_owned(
                target,
                "asset-kadence",
                "CAPACITA",
                "ecosistema/ASSET.md",
            )
            self.register_asset_detail(target, "asset-kadence")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_registration_requires_an_exact_path_not_a_substring(self):
        """Break caught: data cannot inherit ownership from the word metadata."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            (target / "data").write_text("dato sciolto\n", encoding="utf-8")
            self.register_root_owned(
                target,
                "metadata",
                "CAPACITA",
                "ecosistema/ASSET.md",
            )
            self.register_asset_detail(target, "metadata")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("data", result.stderr)

    def test_reference_in_an_example_does_not_register_a_root_file(self):
        """Break caught: documentation prose is not an ownership registry row."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            (target / "data").write_text("dato sciolto\n", encoding="utf-8")
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8")
                + "\nEsempio negativo: non usare `data` come contenitore generico.\n",
                encoding="utf-8",
            )
            assets = target / "ecosistema" / "ASSET.md"
            assets.write_text(
                assets.read_text(encoding="utf-8")
                + "\nNota: il percorso `data` non e' un asset registrato.\n",
                encoding="utf-8",
            )

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("data", result.stderr)

    def test_duplicate_suffix_blocks_first_stop(self):
        """Break caught: version-copy filenames cannot accumulate silently."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            capability = target / "fonti-sito"
            capability.mkdir()
            (capability / "PIANO_v2.md").write_text("# Copia\n", encoding="utf-8")
            self.register_root_owned(
                target,
                "fonti-sito",
                "ARCHIVIO",
                "ecosistema/FONTI.md",
            )
            self.register_source_detail(target, "fonti-sito")

            result = self.run_guard(target)

            self.assertEqual(result.returncode, 2)
            self.assertIn("fonti-sito/PIANO_v2.md", result.stderr)

    def test_second_stop_does_not_loop_and_surfaces_the_open_issue(self):
        """Break caught: one continuation is enforced without trapping the user forever."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            (target / "ecosistema" / "STRATEGIA.md").write_text(
                "# Strategia\n",
                encoding="utf-8",
            )

            result = self.run_guard(target, active=True)

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn("systemMessage", payload)
            self.assertNotEqual(payload.get("decision"), "block")

    def test_setup_merges_hooks_without_erasing_existing_settings(self):
        """Break caught: installing the guard cannot replace customer hook settings."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            codex_path = target / ".codex" / "hooks.json"
            claude_path = target / ".claude" / "settings.json"

            codex = json.loads(codex_path.read_text(encoding="utf-8"))
            claude = json.loads(claude_path.read_text(encoding="utf-8"))
            codex["customer_setting"] = {"keep": True}
            claude["customer_setting"] = {"keep": True}
            codex_path.write_text(json.dumps(codex), encoding="utf-8")
            claude_path.write_text(json.dumps(claude), encoding="utf-8")

            leaderai_setup.run_setup(
                target,
                "Studio Test",
                "both",
                claude_user_settings_path=Path(tmp) / "claude-user-settings.json",
            )

            codex = json.loads(codex_path.read_text(encoding="utf-8"))
            claude = json.loads(claude_path.read_text(encoding="utf-8"))
            self.assertEqual(codex["customer_setting"], {"keep": True})
            self.assertEqual(claude["customer_setting"], {"keep": True})
            for data in (codex, claude):
                handlers = [
                    handler
                    for group in data["hooks"]["Stop"]
                    for handler in group["hooks"]
                    if "guardiano_stanze" in handler.get("command", "")
                    or "guardiano_stanze" in handler.get("commandWindows", "")
                ]
                self.assertEqual(len(handlers), 1)

            codex_guard = next(
                handler
                for group in codex["hooks"]["Stop"]
                for handler in group["hooks"]
                if "guardiano_stanze" in handler.get("command", "")
            )
            self.assertIn("commandWindows", codex_guard)

    def test_setup_preserves_customer_stop_handler(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            codex_path = target / ".codex" / "hooks.json"
            codex = json.loads(codex_path.read_text(encoding="utf-8"))
            customer_group = {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python customer_check.py",
                    }
                ]
            }
            codex["hooks"]["Stop"].insert(0, customer_group)
            codex_path.write_text(json.dumps(codex), encoding="utf-8")

            leaderai_setup.run_setup(
                target,
                "Studio Test",
                "both",
                claude_user_settings_path=Path(tmp) / "claude-user-settings.json",
            )

            updated = json.loads(codex_path.read_text(encoding="utf-8"))
            commands = [
                handler.get("command", "")
                for group in updated["hooks"]["Stop"]
                for handler in group["hooks"]
            ]
            self.assertIn("python customer_check.py", commands)
            self.assertEqual(
                sum("guardiano_stanze" in command for command in commands),
                1,
            )

    def test_setup_preserves_customer_handler_that_only_mentions_guard_name(self):
        """Break caught: a customer hook with a similar name is never deleted."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            codex_path = target / ".codex" / "hooks.json"
            codex = json.loads(codex_path.read_text(encoding="utf-8"))
            customer_handler = {
                "type": "command",
                "command": "python customer_check.py",
                "description": "verifica diversa guardiano_stanze cliente",
            }
            codex["hooks"]["Stop"].insert(0, {"hooks": [customer_handler]})
            codex_path.write_text(json.dumps(codex), encoding="utf-8")

            leaderai_setup.run_setup(
                target,
                "Studio Test",
                "both",
                claude_user_settings_path=Path(tmp) / "claude-user-settings.json",
            )

            updated = json.loads(codex_path.read_text(encoding="utf-8"))
            handlers = [
                handler
                for group in updated["hooks"]["Stop"]
                for handler in group["hooks"]
            ]
            self.assertIn(customer_handler, handlers)

    def test_invalid_hook_config_blocks_before_any_other_write(self):
        """Break caught: preflight must be atomic when a customer JSON is invalid."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            codex_path = target / ".codex" / "hooks.json"
            original = "{ configurazione cliente non valida\n"
            codex_path.write_text(original, encoding="utf-8")
            guard_path = target / ".agent" / "hooks" / "guardiano_stanze.sh"
            original_guard = guard_path.read_text(encoding="utf-8")
            guard_path.unlink()

            result = leaderai_setup.run_setup(
                target,
                "Studio Test",
                "both",
                claude_user_settings_path=Path(tmp) / "claude-user-settings.json",
            )

            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertEqual(codex_path.read_text(encoding="utf-8"), original)
            self.assertFalse(guard_path.exists())
            self.assertNotEqual(original_guard, "")

    def test_invalid_customer_hook_json_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.install(tmp)
            codex_path = target / ".codex" / "hooks.json"
            original = "{ configurazione cliente non valida\n"
            codex_path.write_text(original, encoding="utf-8")

            result = leaderai_setup.run_setup(
                target,
                "Studio Test",
                "both",
                claude_user_settings_path=Path(tmp) / "claude-user-settings.json",
            )

            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertEqual(codex_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
