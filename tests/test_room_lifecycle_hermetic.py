import json
import shutil
import tempfile
import unittest
from pathlib import Path

import leaderai_setup
from tests import test_ecosistema_inspector as existing_inspector_tests


ROOM_PLACEHOLDER = (
    "| Da censire | Da definire dal lavoro reale | - | - | - | - | - | - | "
    "Da assegnare | Boss dell'Ecosistema |"
)
ROOT_OWNED_PLACEHOLDER = (
    "| Da censire | Da definire | Da definire dal lavoro reale | "
    "`ecosistema/ASSET.md` o `ecosistema/FONTI.md` |"
)


class RoomLifecycleHermeticTest(unittest.TestCase):
    """Regressioni di tenuta per stanze e registro della cartella madre.

    L'installazione completa viene eseguita una sola volta. Ogni test lavora su
    una copia indipendente, inclusa la baseline Git, e usa impostazioni Claude
    coerenti con il percorso della copia.
    """

    inspect = existing_inspector_tests.EcosistemaInspectorTest.inspect
    create_valid_room = (
        existing_inspector_tests.EcosistemaInspectorTest.create_valid_room
    )
    codes = existing_inspector_tests.EcosistemaInspectorTest.codes

    @classmethod
    def setUpClass(cls) -> None:
        cls._seed_context = tempfile.TemporaryDirectory()
        fixture = existing_inspector_tests.EcosistemaInspectorTest()
        cls._seed_target = fixture.make_target(cls._seed_context.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._seed_context.cleanup()

    def fresh_target(self) -> Path:
        context = tempfile.TemporaryDirectory()
        self.addCleanup(context.cleanup)
        root = Path(context.name)
        target = root / "EcosistemaAI-Test"
        shutil.copytree(self._seed_target, target, symlinks=True)
        # Le prove ermetiche registrano stanze: il percorso e' al passo 3.
        existing_inspector_tests.EcosistemaInspectorTest.set_phase(self, target, 3)
        # Home finta della copia: istruzioni globali che portano nella casa copiata.
        context_values = {
            "client_name": "Cliente Test",
            "version": leaderai_setup.STANDARD_VERSION,
            "house_path": leaderai_setup._portable_machine_path(target),
        }
        self.claude_user_instructions = root / "home-finta" / ".claude" / "CLAUDE.md"
        self.codex_user_instructions = root / "home-finta" / ".codex" / "AGENTS.md"
        for path, template in (
            (self.claude_user_instructions, "CLAUDE_USER.md"),
            (self.codex_user_instructions, "CODEX_USER_AGENTS.md"),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                leaderai_setup.read_template(template, context_values),
                encoding="utf-8",
            )
        self.claude_user_settings = root / "claude-user-settings.json"
        self.claude_user_settings.write_text(
            json.dumps(
                {
                    "autoMemoryDirectory": leaderai_setup._portable_machine_path(
                        target / "memory"
                    )
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return target

    def set_room_rows(self, target: Path, *rows: str) -> None:
        agents = target / "AGENTS.md"
        text = agents.read_text(encoding="utf-8")
        self.assertIn(ROOM_PLACEHOLDER, text)
        agents.write_text(
            text.replace(ROOM_PLACEHOLDER, "\n".join(rows)),
            encoding="utf-8",
        )

    def add_room_to_registry(self, target: Path) -> None:
        self.set_room_rows(target, self.room_row())

    def set_root_owned_rows(self, target: Path, *rows: str) -> None:
        agents = target / "AGENTS.md"
        text = agents.read_text(encoding="utf-8")
        self.assertIn(ROOT_OWNED_PLACEHOLDER, text)
        agents.write_text(
            text.replace(ROOT_OWNED_PLACEHOLDER, "\n".join(rows)),
            encoding="utf-8",
        )

    @staticmethod
    def room_row(
        name: str = "Iscrizioni",
        path: str = "app-iscrizioni",
        purpose: str = "Gestire iscrizioni",
        upstream: str = "Radice",
        downstream: str = "Documenti",
        sources: str = "Gestionale",
        outputs: str = "Documenti",
        capabilities: str = "App",
        map_path: str | None = None,
        administrator: str | None = None,
        reports_to: str = "Boss dell'Ecosistema",
    ) -> str:
        map_path = map_path or f"{path}/AGENTS.md"
        administrator = administrator or f"Amministratore di settore {name}"
        return (
            f"| [{name}]({path}) | {purpose} | {upstream} | {downstream} | "
            f"{sources} | {outputs} | {capabilities} | `{map_path}` | "
            f"{administrator} | {reports_to} |"
        )

    @staticmethod
    def root_owned_row(
        path: str,
        classification: str = "CAPACITA",
        usage: str = "Supporta il lavoro del cliente",
        registry: str = "ecosistema/ASSET.md",
    ) -> str:
        return (
            f"| `{path}` | {classification} | {usage} | `{registry}` |"
        )

    def customize_room(
        self,
        target: Path,
        path: str,
        name: str,
        purpose: str,
    ) -> None:
        room_map = target / path / "AGENTS.md"
        text = room_map.read_text(encoding="utf-8")
        text = text.replace("Gestire iscrizioni", purpose)
        text = text.replace("Iscrizioni", name)
        room_map.write_text(text, encoding="utf-8")

    def add_business_generator(
        self,
        target: Path,
        source_name: str = "CONTENUTI_DOCUMENTO.md",
    ) -> Path:
        room = target / "app-iscrizioni"
        room_map = room / "AGENTS.md"
        room_map.write_text(
            room_map.read_text(encoding="utf-8").replace(
                "NON APPLICABILE: nessun generatore",
                f"`{source_name}`",
            ),
            encoding="utf-8",
        )
        (room / "genera_pdf.py").write_text(
            "from pathlib import Path\n\n"
            f"FONTE = Path(__file__).with_name({source_name!r})\n\n"
            "def genera_pdf():\n"
            "    return FONTE.read_text(encoding='utf-8')\n",
            encoding="utf-8",
        )
        return room / source_name

    def assert_blocker(self, target: Path, code: str) -> None:
        inspection = self.inspect(target)
        self.assertEqual(inspection.verdict, "NON PASSA")
        self.assertIn(code, self.codes(inspection))

    def test_root_owned_case_and_alias_duplicates_are_blocked(self):
        target = self.fresh_target()
        (target / "Catalogo").mkdir()
        (target / "Catalogo" / "voce.txt").write_text("viva\n", encoding="utf-8")
        self.set_root_owned_rows(
            target,
            self.root_owned_row("Catalogo"),
            self.root_owned_row("catalogo/."),
        )

        self.assert_blocker(target, "DUPLICATE_ROOT_OWNED_PATH")

    def test_room_case_and_path_alias_duplicates_are_blocked(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.set_room_rows(
            target,
            self.room_row(),
            self.room_row(
                name="Alias iscrizioni",
                path="APP-ISCRIZIONI/.",
                purpose="Gestire alias iscrizioni",
                map_path="APP-ISCRIZIONI/AGENTS.md",
            ),
        )

        self.assert_blocker(target, "DUPLICATE_ROOM_PATH")

    def test_duplicate_contract_sections_are_blocked(self):
        cases = (
            ("room-map", "ROOM_MAP_SECTION_DUPLICATE"),
            ("owner-source", "ROOM_OWNER_SOURCE_SECTION_DUPLICATE"),
            ("root-registry", "ROOT_ROOM_REGISTRY_DUPLICATE"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                if case == "root-registry":
                    agents = target / "AGENTS.md"
                    agents.write_text(
                        agents.read_text(encoding="utf-8")
                        + "\n### Registro delle stanze\n",
                        encoding="utf-8",
                    )
                else:
                    self.create_valid_room(target)
                    self.add_room_to_registry(target)
                    if case == "room-map":
                        path = target / "app-iscrizioni" / "AGENTS.md"
                        path.write_text(
                            path.read_text(encoding="utf-8")
                            + "\n## Scopo\n\nSecondo scopo.\n",
                            encoding="utf-8",
                        )
                    else:
                        path = target / "app-iscrizioni" / "STATO_ISCRIZIONI.md"
                        path.write_text(
                            path.read_text(encoding="utf-8")
                            + "\n## Decisioni\n\nSeconda sezione.\n",
                            encoding="utf-8",
                        )
                self.assert_blocker(target, expected)

    def test_dentro_requires_a_real_direct_relative_value(self):
        cases = (
            ("senza-valore", "- ", "ROOM_CONTENTS_UNDECLARED"),
            (
                "assoluto-unix",
                "- `/archivio/` - percorso esterno",
                "ROOM_CHILD_DECLARATION_INVALID",
            ),
            (
                "assoluto-windows",
                "- `C:\\archivio\\` - percorso esterno",
                "ROOM_CHILD_DECLARATION_INVALID",
            ),
        )
        for case, replacement, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.add_room_to_registry(target)
                room_map = target / "app-iscrizioni" / "AGENTS.md"
                room_map.write_text(
                    room_map.read_text(encoding="utf-8").replace(
                        "- NESSUNA SOTTOCARTELLA",
                        replacement,
                    ),
                    encoding="utf-8",
                )
                self.assert_blocker(target, expected)

    def test_business_generator_accepts_one_local_editable_source(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.add_room_to_registry(target)
        source = self.add_business_generator(target)
        source.write_text("# Contenuti\n\nTesto approvato dal cliente.\n", encoding="utf-8")

        inspection = self.inspect(target)

        self.assertEqual(inspection.verdict, "PASSA")

    def test_business_generator_source_failures_are_explicit(self):
        cases = (
            ("missing", "ROOM_BUSINESS_SOURCE_MISSING"),
            ("symlink", "ROOM_BUSINESS_SOURCE_SYMLINK"),
            ("empty", "ROOM_BUSINESS_SOURCE_EMPTY"),
            ("placeholder", "ROOM_BUSINESS_SOURCE_PLACEHOLDER"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.add_room_to_registry(target)
                source = self.add_business_generator(target)
                if case == "symlink":
                    external = target.parent / "contenuti-esterni.md"
                    external.write_text("# Contenuti\n\nTesto vivo.\n", encoding="utf-8")
                    source.symlink_to(external)
                elif case == "empty":
                    source.write_text("", encoding="utf-8")
                elif case == "placeholder":
                    source.write_text("# Contenuti\n\nDA DEFINIRE\n", encoding="utf-8")
                self.assert_blocker(target, expected)

    def test_unreadable_maps_and_bridges_return_findings_instead_of_crashing(self):
        cases = (
            ("root-map", "ROOT_MAP_UNREADABLE"),
            ("root-bridge", "ROOT_BRIDGE_UNREADABLE"),
            ("room-map", "ROOM_MAP_UNREADABLE"),
            ("room-bridge", "ROOM_BRIDGE_UNREADABLE"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                if case.startswith("room-"):
                    self.create_valid_room(target)
                    self.add_room_to_registry(target)
                path = {
                    "root-map": target / "AGENTS.md",
                    "root-bridge": target / "CLAUDE.md",
                    "room-map": target / "app-iscrizioni" / "AGENTS.md",
                    "room-bridge": target / "app-iscrizioni" / "CLAUDE.md",
                }[case]
                path.write_bytes(b"\xff\xfe\x00")
                self.assert_blocker(target, expected)

    def test_room_row_placeholders_do_not_count_as_identity_or_ownership(self):
        cases = (
            (
                "name",
                self.room_row(name="{{room_name}}"),
                "ROOM_NAME_UNPROVEN",
            ),
            (
                "purpose",
                self.room_row(purpose="{{room_purpose}}"),
                "ROOM_PURPOSE_UNPROVEN",
            ),
            (
                "administrator",
                self.room_row(administrator="{{room_administrator}}"),
                "ROOM_ADMINISTRATOR_MISSING",
            ),
        )
        for case, row, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.set_room_rows(target, row)
                self.assert_blocker(target, expected)

    def test_operating_source_rejects_copied_template_name_and_placeholder_values(self):
        cases = (
            ("copied-name", "ROOM_OWNER_SOURCE_GENERIC_NAME"),
            ("placeholder-values", "ROOM_OWNER_SOURCE_INCOMPLETE"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.add_room_to_registry(target)
                room = target / "app-iscrizioni"
                source = room / "STATO_ISCRIZIONI.md"
                if case == "copied-name":
                    copied = room / "STANZA_FONTE copia.md"
                    source.rename(copied)
                    room_map = room / "AGENTS.md"
                    room_map.write_text(
                        room_map.read_text(encoding="utf-8").replace(
                            "STATO_ISCRIZIONI.md",
                            copied.name,
                        ),
                        encoding="utf-8",
                    )
                else:
                    source.write_text(
                        "# Iscrizioni - fonte operativa\n\n"
                        "## Stato corrente\n\nDA DEFINIRE\n\n"
                        "## Prossimo passo\n\nTODO\n\n"
                        "## Decisioni\n\nTBD\n\n"
                        "## Scadenze\n\nDA COMPILARE\n",
                        encoding="utf-8",
                    )
                self.assert_blocker(target, expected)

    def test_room_map_route_and_source_roles_cannot_disagree(self):
        cases = (
            ("wrong-map-row", "ROOM_MAP_ROUTE_INVALID"),
            ("operating-source-conflict", "ROOM_OWNER_SOURCE_CONFLICT"),
            ("source-role-conflict", "ROOM_SOURCE_ROLE_CONFLICT"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                if case == "wrong-map-row":
                    self.set_room_rows(
                        target,
                        self.room_row(map_path="app-iscrizioni/MAPPA.md"),
                    )
                else:
                    self.add_room_to_registry(target)
                    room_map = target / "app-iscrizioni" / "AGENTS.md"
                    if case == "operating-source-conflict":
                        room_map.write_text(
                            room_map.read_text(encoding="utf-8").replace(
                                "## Stato corrente e prossimo passo\n",
                                "## Stato corrente e prossimo passo\n\n"
                                "- Fonte operativa: `ALTRA_FONTE.md`\n",
                            ),
                            encoding="utf-8",
                        )
                    else:
                        room_map.write_text(
                            room_map.read_text(encoding="utf-8").replace(
                                "NON APPLICABILE: nessun generatore",
                                "`STATO_ISCRIZIONI.md`",
                            ),
                            encoding="utf-8",
                        )
                self.assert_blocker(target, expected)

    def test_root_owned_rows_require_use_registry_direct_path_and_unique_owner(self):
        cases = (
            ("usage", "ROOT_OWNED_USAGE_UNPROVEN"),
            ("registry", "ROOT_OWNED_REGISTRY_INVALID"),
            ("direct", "ROOT_OWNED_PATH_NOT_DIRECT"),
            ("standard-collision", "ROOT_OWNED_STANDARD_COLLISION"),
            ("double-ownership", "ROOM_OWNERSHIP_CONFLICT"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                if case == "direct":
                    owned = target / "contenitore" / "catalogo.txt"
                    owned.parent.mkdir()
                    owned.write_text("vivo\n", encoding="utf-8")
                    row = self.root_owned_row("contenitore/catalogo.txt")
                elif case == "standard-collision":
                    row = self.root_owned_row("memory", classification="INFRASTRUTTURA")
                elif case == "double-ownership":
                    self.create_valid_room(target)
                    self.add_room_to_registry(target)
                    row = self.root_owned_row("app-iscrizioni")
                else:
                    (target / "catalogo.txt").write_text("vivo\n", encoding="utf-8")
                    if case == "usage":
                        row = self.root_owned_row("catalogo.txt", usage="DA DEFINIRE")
                    else:
                        row = self.root_owned_row(
                            "catalogo.txt",
                            registry="ecosistema/PROCESSI.md",
                        )
                self.set_root_owned_rows(target, row)
                self.assert_blocker(target, expected)

    def test_rooms_must_be_visible_top_level_business_branches(self):
        cases = (
            ("nested", "settori/iscrizioni", "ROOM_PATH_NOT_TOP_LEVEL"),
            ("hidden", ".iscrizioni", "ROOM_PATH_NOT_TOP_LEVEL"),
            ("standard", "memory", "ROOM_STANDARD_COLLISION"),
        )
        for case, path, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.set_room_rows(target, self.room_row(path=path))
                self.assert_blocker(target, expected)

    def test_hidden_root_and_room_content_cannot_escape_classification(self):
        cases = (
            ("root", "UNCLASSIFIED_DIR"),
            ("room", "ROOM_CHILD_UNDECLARED"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                if case == "root":
                    hidden = target / ".materiale"
                else:
                    self.create_valid_room(target)
                    self.add_room_to_registry(target)
                    hidden = target / "app-iscrizioni" / ".materiale"
                hidden.mkdir()
                (hidden / "nota.md").write_text("# Nota\n", encoding="utf-8")
                self.assert_blocker(target, expected)

    def test_room_tree_cannot_reach_a_third_subdirectory_level(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.add_room_to_registry(target)
        deepest = target / "app-iscrizioni" / "pratiche" / "2026" / "agosto"
        deepest.mkdir(parents=True)
        (deepest / "pratica.md").write_text("# Pratica\n", encoding="utf-8")
        room_map = target / "app-iscrizioni" / "AGENTS.md"
        room_map.write_text(
            room_map.read_text(encoding="utf-8").replace(
                "- NESSUNA SOTTOCARTELLA",
                "- `pratiche/` - pratiche vive",
            ),
            encoding="utf-8",
        )

        self.assert_blocker(target, "ROOM_CHILD_TOO_DEEP")

    def test_fenced_and_commented_registry_markers_are_inert(self):
        target = self.fresh_target()
        agents = target / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8")
            + "\n<!--\n### Registro delle stanze\n-->\n"
            + "```markdown\n### Registro delle stanze\n```\n",
            encoding="utf-8",
        )

        inspection = self.inspect(target)

        self.assertEqual(inspection.verdict, "PASSA")

    def test_registry_table_must_not_be_detached_from_its_marker(self):
        target = self.fresh_target()
        agents = target / "AGENTS.md"
        text = agents.read_text(encoding="utf-8")
        text = text.replace(
            "### Registro delle stanze\n\n| Stanza",
            "### Registro delle stanze\n\n"
            "Questa spiegazione separa il marker dal registro.\n\n| Stanza",
        )
        agents.write_text(text, encoding="utf-8")

        self.assert_blocker(target, "ROOT_ROOM_REGISTRY_SCHEMA_INVALID")

    def test_missing_or_altered_root_markers_are_blocked(self):
        cases = (
            (
                "missing-room-registry",
                "### Registro delle stanze",
                "### Registro rimosso",
                "ROOT_ROOM_REGISTRY_MISSING",
            ),
            (
                "altered-owned-registry",
                "### Elementi posseduti direttamente dalla cartella madre",
                "#### Elementi posseduti direttamente dalla cartella madre",
                "ROOT_OWNED_REGISTRY_MISSING",
            ),
        )
        for case, old, new, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                agents = target / "AGENTS.md"
                agents.write_text(
                    agents.read_text(encoding="utf-8").replace(old, new, 1),
                    encoding="utf-8",
                )
                self.assert_blocker(target, expected)

    def test_root_and_local_room_maps_cannot_drift(self):
        cases = (
            ("name", "ROOM_NAME_DRIFT"),
            ("purpose", "ROOM_PURPOSE_DRIFT"),
            ("organization", "ROOM_ORGANIZATION_NAME_DRIFT"),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.add_room_to_registry(target)
                room_map = target / "app-iscrizioni" / "AGENTS.md"
                text = room_map.read_text(encoding="utf-8")
                if case == "name":
                    text = text.replace("# Iscrizioni", "# Segreteria", 1)
                elif case == "purpose":
                    text = text.replace("Gestire iscrizioni", "Gestire segreteria", 1)
                else:
                    text = text.replace(
                        "Amministratore del settore `Iscrizioni`",
                        "Amministratore del settore `Segreteria`",
                    )
                room_map.write_text(text, encoding="utf-8")
                self.assert_blocker(target, expected)

    def test_duplicate_room_names_are_case_insensitive(self):
        target = self.fresh_target()
        self.create_valid_room(target, "app-iscrizioni")
        self.create_valid_room(target, "segreteria")
        self.customize_room(target, "segreteria", "ISCRIZIONI", "Gestire segreteria")
        self.set_room_rows(
            target,
            self.room_row(),
            self.room_row(
                name="ISCRIZIONI",
                path="segreteria",
                purpose="Gestire segreteria",
            ),
        )

        self.assert_blocker(target, "DUPLICATE_ROOM_NAME")

    def test_five_room_registry_routes_cannot_remain_placeholders(self):
        for placeholder in ("DA DEFINIRE", "-", "NON APPLICABILE"):
            with self.subTest(placeholder=placeholder):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.set_room_rows(
                    target,
                    self.room_row(
                        upstream=placeholder,
                        downstream=placeholder,
                        sources=placeholder,
                        outputs=placeholder,
                        capabilities=placeholder,
                    ),
                )

                inspection = self.inspect(target)

                self.assertEqual(inspection.verdict, "NON PASSA")
                self.assertIn(
                    "ROOM_REGISTRY_FIELDS_UNPROVEN",
                    self.codes(inspection),
                )
                detail = next(
                    finding.detail
                    for finding in inspection.findings
                    if finding.code == "ROOM_REGISTRY_FIELDS_UNPROVEN"
                )
                for label in (
                    "A monte",
                    "A valle",
                    "Fonti",
                    "Output",
                    "Capacita'",
                ):
                    self.assertIn(label, detail)

    def test_five_room_registry_routes_must_match_the_local_map(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.set_room_rows(
            target,
            self.room_row(
                upstream="Email",
                downstream="Archivio",
                sources="Foglio esterno",
                outputs="Report finale",
                capabilities="Script locale",
            ),
        )

        inspection = self.inspect(target)

        self.assertEqual(inspection.verdict, "NON PASSA")
        self.assertIn("ROOM_REGISTRY_FIELD_DRIFT", self.codes(inspection))
        detail = next(
            finding.detail
            for finding in inspection.findings
            if finding.code == "ROOM_REGISTRY_FIELD_DRIFT"
        )
        for label in ("A monte", "A valle", "Fonti", "Output", "Capacita'"):
            self.assertIn(label, detail)

    def test_two_pure_operating_sources_are_ambiguous(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.add_room_to_registry(target)
        room = target / "app-iscrizioni"
        shutil.copy2(
            room / "STATO_ISCRIZIONI.md",
            room / "STATO_PRATICHE.md",
        )

        self.assert_blocker(target, "ROOM_OWNER_SOURCE_MULTIPLE")

    def test_operating_source_h1_must_identify_its_room(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.add_room_to_registry(target)
        source = target / "app-iscrizioni" / "STATO_ISCRIZIONI.md"
        source.write_text(
            source.read_text(encoding="utf-8").replace(
                "# Iscrizioni - fonte operativa",
                "# Segreteria - fonte operativa",
                1,
            ),
            encoding="utf-8",
        )

        self.assert_blocker(target, "ROOM_OWNER_SOURCE_TITLE_DRIFT")

    def test_business_and_operating_source_conflict_is_case_insensitive(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.add_room_to_registry(target)
        room_map = target / "app-iscrizioni" / "AGENTS.md"
        room_map.write_text(
            room_map.read_text(encoding="utf-8").replace(
                "NON APPLICABILE: nessun generatore",
                "`stato_iscrizioni.MD`",
            ),
            encoding="utf-8",
        )

        self.assert_blocker(target, "ROOM_SOURCE_ROLE_CONFLICT")

    def test_root_owned_element_must_appear_in_its_detail_registry(self):
        target = self.fresh_target()
        (target / "catalogo.txt").write_text("Catalogo vivo.\n", encoding="utf-8")
        self.set_root_owned_rows(
            target,
            self.root_owned_row(
                "catalogo.txt",
                classification="FONTE",
                registry="ecosistema/ASSET.md",
            ),
        )

        self.assert_blocker(target, "ROOT_OWNED_DETAIL_MISSING")

    def test_corrupt_utf8_operational_files_return_findings_not_exceptions(self):
        cases = (
            (
                "inspector-skill",
                ".claude/skills/ispettore-ecosistema/SKILL.md",
                "INSPECTOR_SKILL_UNREADABLE",
            ),
            (
                "asset-registry",
                "ecosistema/ASSET.md",
                "ASSET_REGISTRY_UNREADABLE",
            ),
            (
                "project-control",
                "app-iscrizioni/PROGETTO.md",
                "PROJECT_CONTROL_UNREADABLE",
            ),
            (
                "sources-registry",
                "ecosistema/FONTI.md",
                "REQUIRED_TEXT_UNREADABLE",
            ),
            (
                "process-registry",
                "ecosistema/PROCESSI.md",
                "REQUIRED_TEXT_UNREADABLE",
            ),
            (
                "agent-chat",
                "AGENT_CHAT.md",
                "REQUIRED_TEXT_UNREADABLE",
            ),
            (
                "memory-index",
                "memory/MEMORY.md",
                "REQUIRED_TEXT_UNREADABLE",
            ),
        )
        for case, relative, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                if case == "project-control":
                    self.create_valid_room(target)
                    self.add_room_to_registry(target)
                path = target / relative
                path.write_bytes(b"\xff\xfe\x00")
                self.assert_blocker(target, expected)

    def test_negated_business_responsibility_is_not_proof(self):
        negated_values = (
            "Non mantiene lo stato delle pratiche e non governa le decisioni "
            "sulle iscrizioni",
            "Lo stato non viene mantenuto in alcun modo operativo da questa "
            "stanza. Le decisioni non vengono governate.",
        )
        for negated in negated_values:
            with self.subTest(negated=negated):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.add_room_to_registry(target)
                room_map = target / "app-iscrizioni" / "AGENTS.md"
                room_map.write_text(
                    room_map.read_text(encoding="utf-8").replace(
                        "Mantiene lo stato delle pratiche e le decisioni "
                        "sulle iscrizioni",
                        negated,
                    ),
                    encoding="utf-8",
                )

                self.assert_blocker(
                    target,
                    "ROOM_BUSINESS_RESPONSIBILITY_UNPROVEN",
                )

    def test_negated_organization_terms_do_not_satisfy_the_contract(self):
        for case in ("prepositive", "postpositive"):
            with self.subTest(case=case):
                target = self.fresh_target()
                self.create_valid_room(target)
                self.add_room_to_registry(target)
                room_map = target / "app-iscrizioni" / "AGENTS.md"
                text = room_map.read_text(encoding="utf-8")
                if case == "prepositive":
                    text = text.replace(
                        "Ruolo: **Amministratore del settore",
                        "Ruolo: **non Amministratore del settore",
                    )
                    text = text.replace("Riporta al **Boss", "Non riporta al **Boss")
                    text = text.replace("Riporta al Boss", "Non riporta al Boss")
                    text = text.replace("riporta al Boss", "non riporta al Boss")
                else:
                    text = text.replace(
                        "Amministratore del settore `Iscrizioni`**.",
                        "Amministratore del settore `Iscrizioni`**, che non esiste.",
                    )
                    text = text.replace(
                        "Boss dell'Ecosistema** definito",
                        "Boss dell'Ecosistema**, che non esiste, definito",
                    )
                    text = text.replace(
                        "Riporta al Boss senza duplicare",
                        "Riporta al Boss, ma il riporto non avviene, senza duplicare",
                    )
                room_map.write_text(text, encoding="utf-8")

                self.assert_blocker(target, "ROOM_MAP_INCOMPLETE")

    def test_windows_absolute_and_reserved_paths_are_rejected(self):
        cases = (
            (
                "room-drive",
                self.room_row(path=r"C:\\Clienti\\Iscrizioni"),
                None,
                "INVALID_ROOM_PATH",
            ),
            (
                "room-reserved",
                self.room_row(path="CON"),
                None,
                "INVALID_ROOM_PATH",
            ),
            (
                "root-unc",
                None,
                self.root_owned_row(r"\\\\server\\condivisa"),
                "ROOT_OWNED_PATH_INVALID",
            ),
        )
        for case, room_row, owned_row, expected in cases:
            with self.subTest(case=case):
                target = self.fresh_target()
                if room_row:
                    self.set_room_rows(target, room_row)
                else:
                    self.set_root_owned_rows(target, owned_row)
                self.assert_blocker(target, expected)

    def test_windows_relative_map_separator_is_portable(self):
        target = self.fresh_target()
        self.create_valid_room(target)
        self.set_room_rows(
            target,
            self.room_row(map_path=r"app-iscrizioni\AGENTS.md"),
        )

        inspection = self.inspect(target)

        self.assertEqual(inspection.verdict, "PASSA")


if __name__ == "__main__":
    unittest.main()
