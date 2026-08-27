import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import ecosistema_inspector
import leaderai_setup


ROOM_ROW = (
    "| [Iscrizioni](app-iscrizioni) | Gestire iscrizioni | Radice | "
    "Documenti | Gestionale | Documenti | App | `app-iscrizioni/AGENTS.md` | "
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
            "{{room_contents}}": "NESSUNA SOTTOCARTELLA",
            "{{room_sources}}": "Gestionale",
            "{{room_outputs}}": "Documenti",
            "{{room_operating_source}}": "STATO_ISCRIZIONI.md",
            "{{room_business_source}}": "NON APPLICABILE: nessun generatore",
            "{{room_capabilities}}": "App",
            "{{room_upstream}}": "Radice",
            "{{room_downstream}}": "Documenti",
        }
        for key, value in replacements.items():
            template = template.replace(key, value)
        (room / "AGENTS.md").write_text(template, encoding="utf-8")
        (room / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
        (room / "STATO_ISCRIZIONI.md").write_text(
            "# Iscrizioni - fonte operativa\n\n"
            "## Stato corrente\n\nAttivo.\n\n"
            "## Prossimo passo\n\nVerificare le nuove pratiche.\n\n"
            "## Decisioni\n\nFonte unica confermata.\n\n"
            "## Scadenze\n\nNessuna.\n\n"
            "## Diario\n\nNessuna nota.\n",
            encoding="utf-8",
        )

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
            source = target / "ecosistema" / "FONTI.md"
            source.write_text(
                source.read_text(encoding="utf-8")
                + ("contenuto coerente\n" * policy.document_review_lines),
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

    def test_business_material_inside_ecosistema_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "ecosistema" / "BOZZA_MARKETING.md").write_text(
                "# Bozza\n",
                encoding="utf-8",
            )
            assets = target / "ecosistema" / "asset-visivi"
            assets.mkdir()
            (assets / "logo.txt").write_text("logo\n", encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            contaminated = {
                item.path
                for item in inspection.findings
                if item.code == "ECOSYSTEM_REGISTRY_CONTAMINATED"
            }
            self.assertIn("ecosistema/BOZZA_MARKETING.md", contaminated)
            self.assertIn("ecosistema/asset-visivi", contaminated)

    def test_room_child_must_be_declared_in_room_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            child = target / "app-iscrizioni" / "bozze"
            child.mkdir()
            (child / "nota.md").write_text("# Nota\n", encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_CHILD_UNDECLARED", self.codes(inspection))

            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "- NESSUNA SOTTOCARTELLA",
                    "- `bozze/` - bozze temporanee della stanza",
                ),
                encoding="utf-8",
            )

            repaired = self.inspect(target)

            self.assertEqual(repaired.verdict, "PASSA")

    def test_room_map_and_owner_source_must_be_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            source = target / "app-iscrizioni" / "STATO_ISCRIZIONI.md"
            source.unlink()
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "Gestire iscrizioni",
                    "{{room_purpose}}",
                    1,
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_MAP_PLACEHOLDER", self.codes(inspection))
            self.assertIn("ROOM_OWNER_SOURCE_MISSING", self.codes(inspection))

            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "{{room_purpose}}",
                    "Gestire iscrizioni",
                ),
                encoding="utf-8",
            )
            source.write_text(
                "# Iscrizioni - fonte operativa\n\n"
                "## Stato corrente\n\nAttivo.\n\n"
                "## Prossimo passo\n\nVerificare.\n\n"
                "## Decisioni\n\nNessuna.\n\n"
                "## Scadenze\n\nNessuna.\n",
                encoding="utf-8",
            )

            repaired = self.inspect(target)

            self.assertEqual(repaired.verdict, "PASSA")

    def test_room_map_requires_exact_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "## Output",
                    "## Risultati",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_MAP_INCOMPLETE", self.codes(inspection))

    def test_room_map_requires_sector_administrator_and_boss_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            text = room_map.read_text(encoding="utf-8")
            text = text.replace("Amministratore del settore", "Referente locale")
            text = text.replace("Boss dell'Ecosistema", "Coordinatore centrale")
            text = text.replace("Riporta al Boss", "Collabora con il coordinatore")
            room_map.write_text(text, encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_MAP_INCOMPLETE", self.codes(inspection))

    def test_room_owner_source_cannot_keep_template_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            source = target / "app-iscrizioni" / "STATO_ISCRIZIONI.md"
            source.write_text(
                "# Iscrizioni\n\n"
                "## Stato corrente\n\n{{room_current_state}}\n\n"
                "## Prossimo passo\n\n{{room_next_step}}\n\n"
                "## Decisioni\n\n{{room_decisions}}\n\n"
                "## Scadenze\n\n{{room_deadlines}}\n",
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_OWNER_SOURCE_PLACEHOLDER", self.codes(inspection))

    def test_unreadable_room_owner_source_is_a_blocker_not_a_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            source = target / "app-iscrizioni" / "STATO_ISCRIZIONI.md"
            source.write_bytes(b"\xff\xfe\x00")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_OWNER_SOURCE_UNREADABLE", self.codes(inspection))

    def test_declared_room_child_symlink_is_still_a_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            external = Path(tmp) / "bozze-esterne"
            external.mkdir()
            (external / "nota.md").write_text("# Nota\n", encoding="utf-8")
            child = target / "app-iscrizioni" / "bozze"
            child.symlink_to(external, target_is_directory=True)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "- NESSUNA SOTTOCARTELLA",
                    "- `bozze/` - bozze temporanee della stanza",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_CHILD_SYMLINK", self.codes(inspection))

    def test_ecosystem_registry_symlink_is_not_traversed(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            external = Path(tmp) / "ecosistema-esterno"
            (target / "ecosistema").rename(external)
            (target / "ecosistema").symlink_to(external, target_is_directory=True)

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ECOSYSTEM_REGISTRY_SYMLINK", self.codes(inspection))

    def test_root_owned_element_requires_a_contract_classification(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "catalogo.txt").write_text("catalogo\n", encoding="utf-8")
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            placeholder = (
                "| Da censire | Da definire | Da definire dal lavoro reale | "
                "`ecosistema/ASSET.md` o `ecosistema/FONTI.md` |"
            )
            row = (
                "| `catalogo.txt` | CARAMELLA | Catalogo prodotti | "
                "`ecosistema/ASSET.md` |"
            )
            agents.write_text(text.replace(placeholder, row), encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOT_OWNED_CLASS_INVALID", self.codes(inspection))

    def test_declared_room_child_must_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "- NESSUNA SOTTOCARTELLA",
                    "- `fantasma/` - cartella dichiarata",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_CHILD_DECLARED_MISSING", self.codes(inspection))

    def test_declared_room_child_cannot_be_empty_or_generic(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            (target / "app-iscrizioni" / "documenti").mkdir()
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "- NESSUNA SOTTOCARTELLA",
                    "- `documenti/` - documenti della stanza",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_CHILD_GENERIC", self.codes(inspection))
            self.assertIn("ROOM_CHILD_EMPTY", self.codes(inspection))

    def test_owner_source_core_sections_must_lead_and_have_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            source = target / "app-iscrizioni" / "STATO_ISCRIZIONI.md"
            source.write_text(
                "# Iscrizioni\n\n"
                "## Diario\n\nNota storica.\n\n"
                "## Stato corrente\n\nAttivo.\n\n"
                "## Prossimo passo\n\nVerificare.\n\n"
                "## Decisioni\n\nNessuna.\n\n"
                "## Scadenze\n\n",
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_OWNER_SOURCE_INCOMPLETE", self.codes(inspection))

    def test_file_listed_in_dentro_is_not_treated_as_a_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room = target / "app-iscrizioni"
            (room / "NOTA.md").write_text("# Nota\n", encoding="utf-8")
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "- NESSUNA SOTTOCARTELLA",
                    "- NESSUNA SOTTOCARTELLA\n"
                    "- `NOTA.md` - nota locale della stanza",
                ),
                encoding="utf-8",
            )

            self.assertEqual(self.inspect(target).verdict, "PASSA")

    def test_source_path_preserves_case_and_accents(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room = target / "app-iscrizioni"
            source = room / "STATO_ISCRIZIONI.md"
            accented = room / "STATO_ATTIVITÀ.md"
            source.rename(accented)
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "STATO_ISCRIZIONI.md",
                    "STATO_ATTIVITÀ.md",
                ),
                encoding="utf-8",
            )

            self.assertEqual(self.inspect(target).verdict, "PASSA")

    def test_root_owned_suspect_and_room_classes_stay_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "mistero.txt").write_text("mistero\n", encoding="utf-8")
            (target / "ramo.txt").write_text("ramo\n", encoding="utf-8")
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            placeholder = (
                "| Da censire | Da definire | Da definire dal lavoro reale | "
                "`ecosistema/ASSET.md` o `ecosistema/FONTI.md` |"
            )
            rows = (
                "| `mistero.txt` | SOSPETTA | Da chiarire | "
                "`ecosistema/ASSET.md` |\n"
                "| `ramo.txt` | STANZA | Ramo dichiarato nel registro sbagliato | "
                "`ecosistema/ASSET.md` |"
            )
            agents.write_text(text.replace(placeholder, rows), encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOT_OWNED_CLASS_UNRESOLVED", self.codes(inspection))
            self.assertIn("ROOT_OWNED_CLASS_INVALID", self.codes(inspection))

    def test_root_owned_path_must_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            agents = target / "AGENTS.md"
            text = agents.read_text(encoding="utf-8")
            placeholder = (
                "| Da censire | Da definire | Da definire dal lavoro reale | "
                "`ecosistema/ASSET.md` o `ecosistema/FONTI.md` |"
            )
            row = (
                "| `fantasma/` | CAPACITA | Cartella inesistente | "
                "`ecosistema/ASSET.md` |"
            )
            agents.write_text(text.replace(placeholder, row), encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOT_OWNED_PATH_MISSING", self.codes(inspection))

    def test_required_room_sections_must_have_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "## Scopo\n\nGestire iscrizioni",
                    "## Scopo\n\n",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_MAP_INCOMPLETE", self.codes(inspection))

    def test_responsibility_guidance_alone_is_not_business_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "Mantiene lo stato delle pratiche e le decisioni sulle iscrizioni\n\n",
                    "",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn(
                "ROOM_BUSINESS_RESPONSIBILITY_UNPROVEN",
                self.codes(inspection),
            )

    def test_organization_terms_must_live_in_organization_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            text = room_map.read_text(encoding="utf-8")
            text = text.replace("Amministratore del settore", "Referente locale")
            text = text.replace("Boss dell'Ecosistema", "Coordinatore centrale")
            text = text.replace("Riporta al Boss", "Collabora con il coordinatore")
            text = text.replace(
                "Gestire iscrizioni",
                "Gestire iscrizioni. Amministratore del settore, Boss "
                "dell'Ecosistema, riporta al Boss.",
                1,
            )
            room_map.write_text(text, encoding="utf-8")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_MAP_INCOMPLETE", self.codes(inspection))

    @unittest.skipIf(os.name == "nt", "chmod non e' affidabile su Windows")
    def test_unreadable_room_child_is_a_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            child = target / "app-iscrizioni" / "pratiche"
            child.mkdir()
            (child / "nota.md").write_text("# Nota\n", encoding="utf-8")
            room_map = target / "app-iscrizioni" / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "- NESSUNA SOTTOCARTELLA",
                    "- `pratiche/` - pratiche vive",
                ),
                encoding="utf-8",
            )
            child.chmod(0)
            try:
                inspection = self.inspect(target)
            finally:
                child.chmod(0o700)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_CHILD_UNREADABLE", self.codes(inspection))

    def test_unreadable_room_bridge_is_a_blocker_not_a_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            bridge = target / "app-iscrizioni" / "CLAUDE.md"
            bridge.write_bytes(b"\xff\xfe\x00")

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_BRIDGE_UNREADABLE", self.codes(inspection))

    def test_owner_source_must_receive_a_business_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room = target / "app-iscrizioni"
            source = room / "STATO_ISCRIZIONI.md"
            generic = room / "STANZA_FONTE.md"
            source.rename(generic)
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "STATO_ISCRIZIONI.md",
                    "STANZA_FONTE.md",
                ),
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("ROOM_OWNER_SOURCE_GENERIC_NAME", self.codes(inspection))

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
            room_text = room_map.read_text(encoding="utf-8")
            room_text = room_text.replace("Iscrizioni", "Portafoglio Modello")
            room_text = room_text.replace(
                "Gestire iscrizioni",
                "Costruire modelli",
            )
            room_text = room_text.replace(
                "Mantiene lo stato delle pratiche e le decisioni sulle iscrizioni",
                "Contiene skill, motori, modelli e report",
            )
            room_map.write_text(room_text, encoding="utf-8")
            self.add_room_to_registry(
                target,
                "| [Portafoglio Modello](Portafoglio Modello) | Costruire modelli | "
                "Fonti | Report | Dati | Documenti | Script | "
                "`Portafoglio Modello/AGENTS.md` | "
                "Amministratore di settore Portafoglio | Boss dell'Ecosistema |",
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
            asset_registry = target / "ecosistema" / "ASSET.md"
            asset_text = asset_registry.read_text(encoding="utf-8")
            asset_row = (
                "| `Portafoglio Modello` | Capacita | Cartella madre | Tutte | "
                "Costruzione portafogli | ATTIVO | `Portafoglio Modello/` | "
                "Nessuno |\n"
            )
            asset_registry.write_text(
                asset_text.replace(
                    "\n\n## Regola di aggiornamento",
                    f"\n{asset_row}\n## Regola di aggiornamento",
                ),
                encoding="utf-8",
            )

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
                "`ecosistema/ASSET.md` |"
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
            asset_registry = target / "ecosistema" / "ASSET.md"
            asset_text = asset_registry.read_text(encoding="utf-8")
            asset_row = (
                "| `_claude-memory` | Infrastruttura | Cartella madre | Tutte | "
                "Memoria condivisa | ATTIVO | `_claude-memory/MEMORY.md` | "
                "Nessuno |\n"
            )
            asset_registry.write_text(
                asset_text.replace(
                    "\n\n## Regola di aggiornamento",
                    f"\n{asset_row}\n## Regola di aggiornamento",
                ),
                encoding="utf-8",
            )

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

    def test_anonymous_school_regression_is_non_passa(self):
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
                "LEGACY_MISSION_FILE",
                "CREDENTIAL_FILE_OUTSIDE_SECRETS",
                "BUSINESS_SOURCE_UNDECLARED",
                "BUSINESS_CONTENT_HARDCODED_RISK",
                "SENSITIVE_ASSET_OUTSIDE_PROTECTED",
                "SENSITIVE_ASSET_UNREGISTERED",
                "PROJECT_CONTROL_OUT_OF_ORDER",
            }
            self.assertTrue(expected.issubset(codes), expected - codes)

    def test_absolute_home_memory_path_is_flagged_as_not_portable(self):
        """Caso anonimo multipostazione: il percorso del PC fisso si rompe
        in silenzio sul portatile quando inchioda il nome utente."""
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
