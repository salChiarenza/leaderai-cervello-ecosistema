import json
import os
import stat
import subprocess
import tempfile
import unittest
import zipfile
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
        # Nomi reali dei file utente, in una home finta: Codex sostituisce
        # AGENTS.md con AGENTS.override.md solo quando il nome e' quello vero.
        self.claude_user_instructions = Path(root) / "home-finta" / ".claude" / "CLAUDE.md"
        self.codex_user_instructions = Path(root) / "home-finta" / ".codex" / "AGENTS.md"
        leaderai_setup.run_setup(
            target,
            "Cliente Test",
            agent,
            claude_user_settings_path=(
                self.claude_user_settings
                if agent in {"claude", "both"}
                else None
            ),
            claude_user_instructions_path=self.claude_user_instructions,
            codex_user_instructions_path=self.codex_user_instructions,
        )
        if agent == "codex":
            self.claude_user_settings.write_text("{}\n", encoding="utf-8")
        return target

    def inspect(self, target: Path) -> ecosistema_inspector.Inspection:
        return ecosistema_inspector.inspect_ecosystem(
            target,
            claude_user_settings_path=self.claude_user_settings,
            claude_user_instructions_path=self.claude_user_instructions,
            codex_user_instructions_path=self.codex_user_instructions,
        )

    def set_phase(self, target: Path, phase: int, label: str = "Prima stanza") -> None:
        agents = target / "AGENTS.md"
        import re as _re
        updated, count = _re.subn(
            r"^- Fase del percorso: [1-4] \([^)]*\)\.",
            f"- Fase del percorso: {phase} ({label}).",
            agents.read_text(encoding="utf-8"),
            count=1,
            flags=_re.M,
        )
        self.assertEqual(count, 1)
        agents.write_text(updated, encoding="utf-8")

    def add_room_to_registry(self, target: Path, row: str = ROOM_ROW) -> None:
        # Una stanza registrata significa che il percorso e' al passo 3.
        self.set_phase(target, 3)
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

        evidence = room / "prima_prova.md"
        evidence.write_text("Esito simulato della prima prova della stanza: dato ricevuto e riscontro prodotto.\n")
        source_path = room / "STATO_ISCRIZIONI.md"
        source_path.write_text(source_path.read_text() + (
            f"\n## Prova stanza: {name}\n\n"
            "- Evento: nascita della stanza di collaudo\n"
            "- Processo: dal dato di prova nella fonte al riscontro del reparto.\n"
            f"- Ingresso: \x60{name}/STATO_ISCRIZIONI.md\x60\n"
            f"- Uscita: \x60{name}/prima_prova.md\x60\n"
            f"- Destinatario: \x60{name}/prima_prova.md\x60\n"
            "- Verifica: fixture isolata, risultato riletto e confrontato con il dato simulato.\n"
        ))

    def append_table_row(self, path: Path, marker: str, row: str) -> None:
        """Aggiunge una riga alla tabella che segue `marker`, subito dopo la riga
        separatrice: l'Ispettore legge solo righe contigue."""
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertIn(marker, lines)
        start = lines.index(marker)
        separator = next(
            index
            for index in range(start + 1, len(lines))
            if lines[index].lstrip().startswith("|---")
        )
        lines.insert(separator + 1, row.rstrip())
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def register_root_owned(
        self, target: Path, name: str, classification: str, registry: str
    ) -> None:
        self.append_table_row(
            target / "AGENTS.md",
            "### Elementi posseduti direttamente dalla cartella madre",
            f"| `{name}` | {classification} | Uso verificato | `{registry}` |",
        )

    def register_asset_detail(self, target: Path, name: str) -> None:
        self.append_table_row(
            target / "ecosistema" / "ASSET.md",
            "## Registro",
            f"| {name} | Capacita | `{name}` | Tutte | Uso verificato | ATTIVO | Test locale | Nessuno |",
        )

    def register_source_detail(self, target: Path, name: str) -> None:
        self.append_table_row(
            target / "ecosistema" / "FONTI.md",
            "## Fonti trovate",
            f"| {name} | `{name}` | Marketing | Test locale | ATTIVO |",
        )

    def codes(self, inspection: ecosistema_inspector.Inspection) -> set[str]:
        return {item.code for item in inspection.findings}

    def test_person_status_separates_technical_findings_from_real_work_block(self):
        working = ecosistema_inspector.Inspection(
            target="/tmp/ecosistema",
            rooms=[],
            findings=[],
        )
        to_review = ecosistema_inspector.Inspection(
            target="/tmp/ecosistema",
            rooms=[],
            findings=[
                ecosistema_inspector.Finding(
                    "STANDARD_VERSION_OUTDATED",
                    "BLOCKER",
                    "VERSION",
                    "La versione installata e' precedente allo standard vivo.",
                )
            ],
        )

        self.assertEqual(working.person_status(), "TUTTO FUNZIONA")
        self.assertEqual(
            to_review.person_status(),
            "FUNZIONA, CON ALCUNE COSE DA VALUTARE",
        )
        self.assertEqual(to_review.verdict, "NON PASSA")
        self.assertNotIn("NON PASSA", to_review.person_status())
        incomplete_block = ecosistema_inspector.OperationalBlock(
            function="apertura della casa operativa",
            real_use_failed=True,
        )
        self.assertEqual(
            to_review.person_status(incomplete_block),
            "FUNZIONA, CON ALCUNE COSE DA VALUTARE",
        )

        proven_block = ecosistema_inspector.OperationalBlock(
            function="apertura della casa operativa",
            real_use_failed=True,
            essential_function=True,
            repair_attempts_exhausted=True,
            no_practical_workaround=True,
        )
        self.assertEqual(
            to_review.person_status(proven_block),
            "C'E' UN PROBLEMA CHE BLOCCA: apertura della casa operativa",
        )

        report = ecosistema_inspector._markdown(to_review)
        self.assertIn(
            "- Situazione per la persona: **FUNZIONA, CON ALCUNE COSE DA VALUTARE**",
            report,
        )
        self.assertIn("- Stato tecnico interno: **NON PASSA**", report)
        self.assertNotIn("- Verdetto: **NON PASSA**", report)

        blocked_report = ecosistema_inspector._markdown(
            to_review,
            operational_block=proven_block,
        )
        self.assertIn(
            "- Situazione per la persona: **C'E' UN PROBLEMA CHE BLOCCA: "
            "apertura della casa operativa**",
            blocked_report,
        )

    def test_untracked_credentials_and_hardcoded_business_text_are_review_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room = target / "app-iscrizioni"
            room_map = room / "AGENTS.md"
            room_map.write_text(
                room_map.read_text(encoding="utf-8").replace(
                    "NON APPLICABILE: nessun generatore",
                    "`TESTI_EMAIL.md`",
                ),
                encoding="utf-8",
            )
            (room / "TESTI_EMAIL.md").write_text(
                "# Testi email\n\nConferma iscrizione approvata.\n",
                encoding="utf-8",
            )
            (room / "genera_documento.js").write_text(
                "const testo = "
                + repr(
                    "Gentile cliente, confermiamo la tua iscrizione e ti "
                    "invieremo tutte le informazioni necessarie per partecipare."
                )
                + ";\n",
                encoding="utf-8",
            )
            (room / "google-token.json").write_text("{}\n", encoding="utf-8")

            inspection = self.inspect(target)
            relevant = {
                finding.code: finding.severity
                for finding in inspection.findings
                if finding.code
                in {
                    "BUSINESS_CONTENT_HARDCODED_RISK",
                    "CREDENTIAL_FILE_OUTSIDE_SECRETS",
                }
            }

            self.assertEqual(
                relevant,
                {
                    "BUSINESS_CONTENT_HARDCODED_RISK": "ATTENZIONE",
                    "CREDENTIAL_FILE_OUTSIDE_SECRETS": "ATTENZIONE",
                },
            )
            self.assertEqual(inspection.verdict, "PASSA CON ATTENZIONE")

    def make_family_archive(self, target: Path) -> Path:
        self.create_valid_room(target)
        self.add_room_to_registry(target)
        archive = target / "app-iscrizioni" / "dati" / "pratiche"
        family = archive / "iscrizione-uno"
        family.mkdir(parents=True)
        (family / "firma.png").write_bytes(b"synthetic signature")
        (family / "iscrizione-firmata.pdf").write_bytes(b"%PDF synthetic")
        path = target / "app-iscrizioni" / "AGENTS.md"
        path.write_text(path.read_text().replace("NESSUNA SOTTOCARTELLA", "`dati/` — Dati della scuola.\n- `dati/pratiche/` — ARCHIVIO PROTETTO: fascicoli delle famiglie; FIRME SOTTOSCRITTORI", 1))
        ignore = target / ".gitignore"
        ignore.write_text(ignore.read_text() + "\n/app-iscrizioni/dati/pratiche/\n")
        return archive

    def test_new_enrolment_in_declared_archive_does_not_add_structural_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            archive = self.make_family_archive(target)
            for number in (1, 2):
                with self.subTest(enrolments=number):
                    issues = [f for f in self.inspect(target).findings if f.code.startswith("ROOM_CHILD") or f.code.startswith("SENSITIVE_ASSET") or f.code.startswith("PROTECTED_ARCHIVE")]
                    self.assertEqual(issues, [])
                    extra = archive / "iscrizione-due"
                    extra.mkdir(exist_ok=True)
                    (extra / "firma.png").write_bytes(b"synthetic")
                    (extra / "iscrizione.pdf").write_bytes(b"%PDF synthetic")

    def test_archive_does_not_hide_credentials_or_reusable_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            archive = self.make_family_archive(target)
            (archive / "token.json").write_text("{}")
            (archive / "timbro.png").write_bytes(b"synthetic")
            (archive / "firma_scuola.png").write_bytes(b"synthetic")
            findings = self.inspect(target).findings
            sensitive = {f.path for f in findings if f.code == "SENSITIVE_ASSET_OUTSIDE_PROTECTED"}
            self.assertIn("app-iscrizioni/dati/pratiche/timbro.png", sensitive)
            self.assertIn("app-iscrizioni/dati/pratiche/firma_scuola.png", sensitive)
            self.assertTrue(any(f.code.startswith("CREDENTIAL") and f.path.endswith("token.json") for f in findings))

    def test_archive_protection_requires_ignore_no_tracked_files_and_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            archive = self.make_family_archive(target)
            ignore = target / ".gitignore"
            saved = ignore.read_text()
            ignore.write_text(saved.replace("/app-iscrizioni/dati/pratiche/", ""))
            self.assertIn("PROTECTED_ARCHIVE_UNPROTECTED", self.codes(self.inspect(target)))
            ignore.write_text(saved)
            subprocess.run(["git", "add", "-f", "--", str(archive / "iscrizione-uno" / "firma.png")], cwd=target, check=True, capture_output=True)
            self.assertIn("PROTECTED_ARCHIVE_TRACKED", self.codes(self.inspect(target)))
            (archive / "collegamento").symlink_to(Path(tmp), target_is_directory=True)
            self.assertIn("PROTECTED_ARCHIVE_SYMLINK", self.codes(self.inspect(target)))

    def test_family_signature_requires_explicit_role_and_local_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            archive = self.make_family_archive(target)
            family = archive / "iscrizione-uno"
            (family / "iscrizione-firmata.pdf").unlink()
            self.assertIn("SENSITIVE_ASSET_OUTSIDE_PROTECTED", self.codes(self.inspect(target)))
            (family / "iscrizione.pdf").write_bytes(b"%PDF synthetic")
            path = target / "app-iscrizioni" / "AGENTS.md"
            path.write_text(path.read_text().replace("; FIRME SOTTOSCRITTORI", ""))
            self.assertIn("SENSITIVE_ASSET_OUTSIDE_PROTECTED", self.codes(self.inspect(target)))

    def test_invalid_archive_paths_do_not_grant_an_exemption(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.make_family_archive(target)
            path = target / "app-iscrizioni/AGENTS.md"
            original = path.read_text()
            for raw in ("../documenti/", "/tmp/", "dati/../pratiche/", "dati\\pratiche/", "C:/pratiche/"):
                with self.subTest(path=raw):
                    path.write_text(original.replace("`dati/pratiche/`", f"`{raw}`"))
                    codes = self.codes(self.inspect(target))
                    self.assertIn("PROTECTED_ARCHIVE_INVALID", codes)
                    self.assertIn("SENSITIVE_ASSET_OUTSIDE_PROTECTED", codes)

    def test_archive_helper_drift_cannot_disable_the_guard_silently(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            helper = target / ".agent/hooks/archive_policy.py"
            helper.write_text("pass\n")
            self.assertIn("GUARDIAN_SCRIPT_DRIFT", self.codes(self.inspect(target)))
            helper.unlink()
            self.assertIn("MISSING_STANDARD_FILE", self.codes(self.inspect(target)))

    def test_nested_archive_still_requires_its_direct_parent_in_the_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.make_family_archive(target)
            path = target / "app-iscrizioni/AGENTS.md"
            path.write_text(path.read_text().replace("- `dati/` — Dati della scuola.\n", ""))
            self.assertIn("ROOM_CHILD_UNDECLARED", self.codes(self.inspect(target)))

    def test_family_guide_can_be_a_word_source_elsewhere_in_the_house(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room = target / "app-iscrizioni"
            guide = target / "documenti" / "Guida famiglie.docx"
            guide.parent.mkdir()
            with zipfile.ZipFile(guide, "w") as doc:
                doc.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Guida delle famiglie approvata dalla scuola.</w:t></w:r></w:p></w:body></w:document>')
            (room / "scheda_pdf.py").write_text("import docx\n", encoding="utf-8")
            map_path = room / "AGENTS.md"
            map_path.write_text(map_path.read_text().replace("NON APPLICABILE: nessun generatore", "`@/documenti/Guida famiglie.docx`"))
            issues = [f for f in self.inspect(target).findings if "BUSINESS_SOURCE" in f.code]
            self.assertEqual(issues, [])
            guide.write_bytes(b"not a Word document")
            self.assertIn("BUSINESS_SOURCE_UNREADABLE", self.codes(self.inspect(target)))

    def test_business_source_cannot_leave_house_or_follow_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            room = target / "app-iscrizioni"
            (room / "scheda_pdf.py").write_text("import docx\n")
            external = Path(tmp) / "esterna.md"
            external.write_text("Fonte fuori dalla casa")
            (target / "collegamento.md").symlink_to(external)
            path = room / "AGENTS.md"
            original = path.read_text()
            for declaration, expected in [("@/../esterna.md", "BUSINESS_SOURCE_UNDECLARED"), ("@/collegamento.md", "BUSINESS_SOURCE_SYMLINK")]:
                with self.subTest(declaration=declaration):
                    path.write_text(original.replace("NON APPLICABILE: nessun generatore", f"`{declaration}`"))
                    self.assertIn(expected, self.codes(self.inspect(target)))

    def test_documentation_strings_are_not_business_content(self):
        explanation = "Questa funzione prepara i documenti di prova e descrive il comportamento del programma senza contenere clausole per le famiglie."
        code = repr(explanation) + "\nclass Test:\n    " + repr(explanation) + "\n    def render(self):\n        " + repr(explanation) + "\n        return 1\n"
        self.assertFalse(ecosistema_inspector._hardcoded_business_string(Path("scheda_pdf.py"), code))
        self.assertTrue(ecosistema_inspector._hardcoded_business_string(Path("scheda_pdf.py"), code + '\nCLAUSOLA = "Il genitore si impegna a consegnare la documentazione richiesta dalla scuola entro il 30 settembre."\n'))

    def test_registered_root_dotfile_is_allowed_but_still_requires_detail(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / ".gitattributes").write_text("*.sh text eol=lf\n")
            self.register_root_owned(target, ".gitattributes", "INFRASTRUTTURA", "ecosistema/ASSET.md")
            self.assertIn("ROOT_OWNED_DETAIL_MISSING", self.codes(self.inspect(target)))
            self.register_asset_detail(target, ".gitattributes")
            relevant = [f for f in self.inspect(target).findings if f.path == ".gitattributes" or f.code == "ROOT_OWNED_DETAIL_MISSING"]
            self.assertEqual(relevant, [])

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

    def test_stale_reference_to_a_merged_memory_blocks_pass(self):
        """Una fusione deve lasciare tutti i richiami sul file che resta vivo."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "memory" / "MEMORY.md").write_text(
                "# Memoria\n\nVedi [[regola-che-non-esiste]].\n",
                encoding="utf-8",
            )
            (target / "memory" / "regola-unificata.md").write_text(
                "---\nreplaces:\n  - regola-che-non-esiste\n---\n"
                "# Regola unificata\n",
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("MEMORY_MERGE_REFERENCE_STALE", self.codes(inspection))

    def test_merged_memory_without_a_replace_contract_blocks_pass(self):
        """Il controllo deve sapere quali nomi verificare prima dell'archivio."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "memory" / "regola-unificata.md").write_text(
                "# Regola unificata (fusione di due memorie)\n",
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertEqual(inspection.verdict, "NON PASSA")
            self.assertIn("MEMORY_MERGE_CONTRACT_MISSING", self.codes(inspection))

    def test_missing_or_duplicate_stop_guard_blocks_pass(self):
        for case in ("missing", "duplicate"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                target = self.make_target(tmp)
                settings_path = target / ".claude" / "settings.json"
                settings = json.loads(settings_path.read_text(encoding="utf-8"))
                stop = settings["hooks"]["Stop"]
                if case == "missing":
                    settings["hooks"]["Stop"] = []
                else:
                    stop.append(json.loads(json.dumps(stop[0])))
                settings_path.write_text(
                    json.dumps(settings),
                    encoding="utf-8",
                )

                codes = self.codes(self.inspect(target))

                self.assertIn(
                    "GUARDIAN_HOOK_MISSING"
                    if case == "missing"
                    else "GUARDIAN_HOOK_DUPLICATE",
                    codes,
                )

    def test_inert_handler_that_only_mentions_guard_name_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, agent="codex")
            hooks_path = target / ".codex" / "hooks.json"
            hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
            hooks["hooks"]["Stop"] = [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "exit 0",
                            "description": "guardiano_stanze solo nominato",
                        }
                    ]
                }
            ]
            hooks_path.write_text(json.dumps(hooks), encoding="utf-8")

            self.assertIn(
                "GUARDIAN_HOOK_MISSING",
                self.codes(self.inspect(target)),
            )

    def test_tampered_guard_script_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / ".agent" / "hooks" / "guardiano_stanze.sh").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )

            self.assertIn("GUARDIAN_SCRIPT_DRIFT", self.codes(self.inspect(target)))

    def test_codex_guard_requires_windows_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, agent="codex")
            hooks_path = target / ".codex" / "hooks.json"
            hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
            handler = hooks["hooks"]["Stop"][0]["hooks"][0]
            handler.pop("commandWindows")
            hooks_path.write_text(json.dumps(hooks), encoding="utf-8")

            self.assertIn(
                "GUARDIAN_WINDOWS_COMMAND_MISSING",
                self.codes(self.inspect(target)),
            )

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
            proof = source.read_text().split("## Prova stanza:", 1)[1]
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

            source.write_text(source.read_text() + "\n## Prova stanza:" + proof)
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
            accented.write_text(accented.read_text().replace("STATO_ISCRIZIONI.md", "STATO_ATTIVITÀ.md"))
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

    def test_hidden_flag_on_root_path_blocks_pass(self):
        if not hasattr(os, "chflags") or not hasattr(stat, "UF_HIDDEN"):
            self.skipTest("flag hidden non disponibile su questa piattaforma")
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            hidden_dir = target / "memoria-nascosta"
            hidden_dir.mkdir()
            (hidden_dir / "nota.md").write_text("contenuto\n", encoding="utf-8")
            os.chflags(hidden_dir, stat.UF_HIDDEN)

            inspection = self.inspect(target)

            self.assertIn("HIDDEN_FROM_OWNER", self.codes(inspection))

    def test_technical_environments_are_not_censused_as_owner_content(self):
        """Caso reale LeaderAI 02/09/2026: .venv e .playwright-cli producevano
        oltre 1.600 finding di business, credenziali, asset e Markdown."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            noisy_dirs = [
                target / ".venv" / "lib" / "python3.13" / "site-packages" / "libreria",
                target / ".playwright-cli" / "sessione",
                target / "strumenti" / "ambiente-python",
            ]
            for folder in noisy_dirs:
                folder.mkdir(parents=True)
                (folder / "credentials.json").write_text("{}", encoding="utf-8")
                (folder / "generatore_docx.py").write_text(
                    "import docx\nTESTO = " + repr("Gentile cliente, " * 200) + "\n",
                    encoding="utf-8",
                )
                (folder / "README.md").write_text("# nota\n" * 900, encoding="utf-8")
                (folder / "firma_timbro.png").write_bytes(b"png")
            (target / "strumenti" / "ambiente-python" / "pyvenv.cfg").write_text(
                "home = /usr/bin\n", encoding="utf-8"
            )
            self.register_root_owned(target, "strumenti", "CAPACITA", "ecosistema/ASSET.md")
            self.register_asset_detail(target, "strumenti")

            inspection = self.inspect(target)

            noisy = [
                finding
                for finding in inspection.findings
                if finding.code
                in {
                    "BUSINESS_CONTENT_HARDCODED_RISK",
                    "CREDENTIAL_FILE_OUTSIDE_SECRETS",
                    "SENSITIVE_ASSET_OUTSIDE_PROTECTED",
                    "SENSITIVE_ASSET_UNREGISTERED",
                    "MARKDOWN_DOCUMENT_REVIEW",
                }
                and (".venv" in finding.path or ".playwright-cli" in finding.path or "ambiente-python" in finding.path)
            ]
            self.assertEqual(noisy, [], [f"{f.code} {f.path}" for f in noisy])

    def test_consolidated_house_can_declare_its_own_detail_registry(self):
        """Caso reale LeaderAI 02/09/2026: anagrafe asset gia' in memory/, niente
        doppioni in ecosistema/ASSET.md."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "strumenti").mkdir()
            (target / "strumenti" / "nota.txt").write_text("uso reale\n", encoding="utf-8")
            registry = target / "memory" / "anagrafe_asset.md"
            registry.write_text(
                "# Anagrafe\n\n| Asset | Uso |\n|---|---|\n| `strumenti` | script della casa |\n",
                encoding="utf-8",
            )
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8").replace(
                    "### Elementi posseduti direttamente dalla cartella madre",
                    "- Registro di dettaglio canonico: `memory/anagrafe_asset.md`\n\n"
                    "### Elementi posseduti direttamente dalla cartella madre",
                    1,
                ),
                encoding="utf-8",
            )
            self.register_root_owned(target, "strumenti", "CAPACITA", "memory/anagrafe_asset.md")

            codes = self.codes(self.inspect(target))

            self.assertNotIn("ROOT_OWNED_REGISTRY_INVALID", codes)
            self.assertNotIn("ROOT_OWNED_DETAIL_MISSING", codes)
            self.assertNotIn("UNCLASSIFIED_DIR", codes)

    def test_editor_dot_directories_and_mcp_config_are_not_owner_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / ".obsidian").mkdir()
            (target / ".obsidian" / "app.json").write_text("{}", encoding="utf-8")
            (target / ".mcp.json").write_text("{}", encoding="utf-8")

            findings = self.inspect(target).findings

            self.assertNotIn(
                ".obsidian", [f.path for f in findings if f.code == "UNCLASSIFIED_DIR"]
            )
            self.assertNotIn(
                ".mcp.json", [f.path for f in findings if f.code == "UNOWNED_ROOT_FILE"]
            )

    def test_declared_root_owned_generic_folder_is_a_warning_not_a_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "docs").mkdir()
            (target / "docs" / "genera_report.py").write_text(
                "import docx\nTESTO = " + repr("Gentile cliente, " * 200) + "\n",
                encoding="utf-8",
            )
            self.register_root_owned(target, "docs", "FONTE", "ecosistema/FONTI.md")
            self.register_source_detail(target, "docs")

            findings = self.inspect(target).findings
            generic = [f for f in findings if f.code == "GENERIC_DIR" and f.path == "docs"]

            self.assertEqual([f.severity for f in generic], ["ATTENZIONE"])
            self.assertNotIn(
                "docs", [f.path for f in findings if f.code == "BUSINESS_SOURCE_UNDECLARED"]
            )

    def test_images_notes_and_signed_documents_are_not_credentials_or_assets(self):
        """Caso reale LeaderAI 02/09/2026: schermate 'credential-cards', una nota
        sulla password Google, contratti gia' firmati e uno script 'seam-stamp'."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            folder = target / "lavoro"
            folder.mkdir()
            (folder / "credential-cards-live.png").write_bytes(b"png")
            (folder / "cambio_password_google.md").write_text("# nota\n", encoding="utf-8")
            (folder / "contratto_firmato_sal.docx").write_bytes(b"docx")
            (folder / "seam-stamp.mjs").write_text("export {}\n", encoding="utf-8")
            self.register_root_owned(target, "lavoro", "OUTPUT", "ecosistema/ASSET.md")
            self.register_asset_detail(target, "lavoro")

            findings = self.inspect(target).findings
            noisy = [
                f"{f.code} {f.path}"
                for f in findings
                if f.path.startswith("lavoro/")
                and f.code
                in {
                    "CREDENTIAL_FILE_OUTSIDE_SECRETS",
                    "SENSITIVE_ASSET_OUTSIDE_PROTECTED",
                    "SENSITIVE_ASSET_UNREGISTERED",
                }
            ]
            self.assertEqual(noisy, [])

    def test_signature_image_in_secrets_registered_in_canonical_registry_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / ".secrets" / "firma").mkdir(parents=True)
            (target / ".secrets" / "firma" / "firma_sal.png").write_bytes(b"png")
            registry = target / "memory" / "anagrafe_asset.md"
            registry.write_text(
                "# Anagrafe\n\n| Asset | Casa |\n|---|---|\n| Firma grafica di Sal | `.secrets/firma/` |\n",
                encoding="utf-8",
            )
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8").replace(
                    "### Elementi posseduti direttamente dalla cartella madre",
                    "- Registro di dettaglio canonico: `memory/anagrafe_asset.md`\n\n"
                    "### Elementi posseduti direttamente dalla cartella madre",
                    1,
                ),
                encoding="utf-8",
            )

            codes = {f.code for f in self.inspect(target).findings if "firma" in f.path}

            self.assertEqual(codes, set())

    def test_signature_image_outside_secrets_is_still_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            (target / "lavoro").mkdir()
            (target / "lavoro" / "firma_sal.png").write_bytes(b"png")
            self.register_root_owned(target, "lavoro", "OUTPUT", "ecosistema/ASSET.md")
            self.register_asset_detail(target, "lavoro")

            codes = self.codes(self.inspect(target))

            self.assertIn("SENSITIVE_ASSET_OUTSIDE_PROTECTED", codes)

    def test_consolidated_contract_keeps_existing_room_maps(self):
        """Casa consolidata (LeaderAI 02/09/2026): statuti propri, chat in docs/,
        guardiano proprio, registro canonico. Restano ponte e riga madre."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            room = target / "commerciale"
            room.mkdir()
            (room / "AGENTS.md").write_text("# Statuto\n\nRegole del reparto.\n" + (leaderai_setup.ROOT / "templates/ecosystem-check/AGENTS.md").read_text().split("## Manutenzione", 1)[1].split("## Regole", 1)[0].join(["\n## Manutenzione", ""]).replace("`STATO.md`", "`@/ecosystem-check/STATO.md`"), encoding="utf-8")
            report = target / "ecosystem-check/STATO.md"
            report.write_text(report.read_text() + (
                "\n## Prova stanza: commerciale\n\n"
                "- Evento: adozione del controllo nella casa consolidata\n"
                "- Processo: censimento della mappa e registrazione del reparto gia presente.\n"
                "- Ingresso: `commerciale/AGENTS.md`\n"
                "- Uscita: `ecosystem-check/CONTROLLI.md`\n"
                "- Destinatario: `ecosystem-check/STATO.md`\n"
                "- Verifica: controllo strutturale della fixture isolata; nessuna prova business dichiarata.\n"
            ))

            (room / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            deep = room / "clienti" / "rossi" / "proposta"
            deep.mkdir(parents=True)
            (deep / "genera.py").write_text(
                "import docx\nTESTO = " + repr("Gentile cliente, " * 200) + "\n", encoding="utf-8"
            )
            self.add_room_to_registry(
                target,
                "| [Commerciale](commerciale) | Lead e clienti | Marketing | Amministrazione | STATUS | Proposte | Skill | `commerciale/AGENTS.md` | Amministratore di settore Commerciale | Boss dell'Ecosistema |",
            )
            (target / "docs").mkdir()
            (target / "docs" / "AGENT_CHAT.md").write_text("# Agent Chat\n", encoding="utf-8")
            (target / ".agent" / "hooks" / "mio_guardiano.py").write_text("print('ok')\n", encoding="utf-8")
            settings = target / ".claude" / "settings.json"
            config = json.loads(settings.read_text(encoding="utf-8"))
            config["hooks"]["Stop"][0]["hooks"].append(
                {"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.agent/hooks/mio_guardiano.py\""}
            )
            settings.write_text(json.dumps(config, indent=2), encoding="utf-8")
            registry = target / "memory" / "anagrafe.md"
            registry.write_text("# Anagrafe\n\n| Percorso | Classe |\n|---|---|\n| `docs` | FONTE |\n", encoding="utf-8")
            for rel in ("ecosistema/FONTI.md", "ecosistema/ASSET.md", "AGENT_CHAT.md",
                        ".agent/hooks/guardiano_stanze.sh", ".agent/hooks/guardiano_stanze_windows.ps1",
                        ".agent/hooks/archive_policy.py"):
                (target / rel).unlink()
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8").replace(
                    "### Elementi posseduti direttamente dalla cartella madre",
                    "- Contratto di stanza: consolidato\n"
                    "- Chat di gruppo: `docs/AGENT_CHAT.md`\n"
                    "- Guardiano di chiusura: `.agent/hooks/mio_guardiano.py`\n"
                    "- Registro di dettaglio canonico: `memory/anagrafe.md`\n\n"
                    "### Elementi posseduti direttamente dalla cartella madre",
                    1,
                ),
                encoding="utf-8",
            )
            self.register_root_owned(target, "docs", "FONTE", "memory/anagrafe.md")

            findings = self.inspect(target).findings
            codes = {f.code for f in findings}

            self.assertFalse({c for c in codes if c.startswith("ROOM_")}, codes)
            self.assertNotIn("MISSING_STANDARD_FILE", codes)
            self.assertNotIn("GUARDIAN_HOOK_MISSING", codes)
            self.assertNotIn("BUSINESS_SOURCE_UNDECLARED", codes)
            self.assertIn("BUSINESS_CONTENT_HARDCODED_RISK", codes)

            (room / "CLAUDE.md").write_text("copia\n", encoding="utf-8")
            self.assertIn("ROOM_CLAUDE_INVALID", self.codes(self.inspect(target)))

    def test_consolidated_contract_requires_declared_chat_and_guardian_to_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            agents = target / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8")
                + "\n- Contratto di stanza: consolidato\n- Chat di gruppo: `docs/CHAT.md`\n- Guardiano di chiusura: `.agent/hooks/assente.py`\n",
                encoding="utf-8",
            )

            codes = self.codes(self.inspect(target))

            self.assertIn("CONSOLIDATED_CHAT_MISSING", codes)
            self.assertIn("CONSOLIDATED_GUARDIAN_MISSING", codes)

    def test_dotfiles_are_not_hidden_from_owner_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)

            inspection = self.inspect(target)

            self.assertNotIn("HIDDEN_FROM_OWNER", self.codes(inspection))

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


    def test_missing_user_instructions_block_pass(self):
        """Caso Pastore 03/09/2026: casa installata, ma l'agente aperto da
        un'altra cartella non sapeva dove fosse la casa."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            self.claude_user_instructions.unlink()

            inspection = self.inspect(target)

            self.assertIn("USER_INSTRUCTIONS_MISSING", self.codes(inspection))
            self.assertEqual(inspection.verdict, "NON PASSA")

    def test_user_instructions_without_house_path_block_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            self.claude_user_instructions.write_text(
                "# Preferenze\n- Rispondi in italiano.\n", encoding="utf-8"
            )

            inspection = self.inspect(target)

            self.assertIn("USER_INSTRUCTIONS_WITHOUT_HOUSE", self.codes(inspection))
            self.assertEqual(inspection.verdict, "NON PASSA")

    def test_user_instructions_naming_the_house_without_gate_is_a_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "claude")
            self.claude_user_instructions.write_text(
                f"La casa e' `{target.resolve()}`.\n", encoding="utf-8"
            )

            inspection = self.inspect(target)

            self.assertIn("USER_INSTRUCTIONS_WITHOUT_GATE", self.codes(inspection))
            self.assertEqual(inspection.verdict, "PASSA CON ATTENZIONE")

    def test_user_instructions_accept_portable_home_form(self):
        with tempfile.TemporaryDirectory(dir=Path.home()) as tmp:
            target = self.make_target(tmp, "claude")
            relative = target.resolve().relative_to(Path.home().resolve())
            self.claude_user_instructions.write_text(
                f"Casa: `~/{relative.as_posix()}`. Fuori = FUORI DAL CERVELLO.\n",
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertNotIn("USER_INSTRUCTIONS_WITHOUT_HOUSE", self.codes(inspection))
            self.assertNotIn("USER_INSTRUCTIONS_WITHOUT_GATE", self.codes(inspection))

    def test_codex_reads_override_instructions_when_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "codex")
            override = self.codex_user_instructions.with_name("AGENTS.override.md")
            override.write_text("# Override senza casa\n", encoding="utf-8")

            inspection = self.inspect(target)

            self.assertIn("USER_INSTRUCTIONS_WITHOUT_HOUSE", self.codes(inspection))

    def test_codex_user_instructions_missing_block_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp, "codex")
            self.codex_user_instructions.unlink()

            inspection = self.inspect(target)

            self.assertIn("USER_INSTRUCTIONS_MISSING", self.codes(inspection))


    def test_room_registered_before_step_3_blocks_pass(self):
        """Caso Pastore 03/09/2026: stanze proposte il giorno dell'installazione."""
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            self.set_phase(target, 1, "Cervello")

            inspection = self.inspect(target)

            self.assertIn("ROOM_BEFORE_STEP_3", self.codes(inspection))
            self.assertEqual(inspection.verdict, "NON PASSA")

    def test_room_registered_at_step_3_is_not_flagged_for_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)

            inspection = self.inspect(target)

            self.assertNotIn("ROOM_BEFORE_STEP_3", self.codes(inspection))

    def test_house_without_phase_line_is_not_gated_by_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = self.make_target(tmp)
            self.create_valid_room(target)
            self.add_room_to_registry(target)
            agents = target / "AGENTS.md"
            agents.write_text(
                "\n".join(
                    line for line in agents.read_text(encoding="utf-8").splitlines()
                    if not line.startswith("- Fase del percorso:")
                    and not line.startswith("  missione LeaderAI che chiude il passo")
                ) + "\n",
                encoding="utf-8",
            )

            inspection = self.inspect(target)

            self.assertNotIn("ROOM_BEFORE_STEP_3", self.codes(inspection))


if __name__ == "__main__":
    unittest.main()
