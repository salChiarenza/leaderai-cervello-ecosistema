import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import ecosistema_inspector
import install_contract
import leaderai_setup


class InstallContractTest(unittest.TestCase):
    def settings_path(self, root: Path, name: str = "claude-settings.json") -> Path:
        return root / name

    def test_contract_is_the_machine_source_for_templates_and_agent_rules(self):
        contract = install_contract.load_contract()

        self.assertEqual(
            set(contract["supported_agents"]),
            {"codex", "claude", "both"},
        )
        sources = install_contract.official_sources(contract)
        self.assertEqual(
            [source.url for source in sources],
            [
                "https://code.claude.com/docs/en/overview",
                "https://learn.chatgpt.com/docs",
                "https://openai.com/it-IT/academy/codex-for-work/",
                "https://code.claude.com/docs/en/hooks",
                "https://learn.chatgpt.com/docs/hooks",
            ],
        )
        self.assertEqual(
            [source.role for source in sources],
            [
                "technical_entrypoint",
                "technical_entrypoint",
                "operational_training",
                "technical_specification",
                "technical_specification",
            ],
        )
        markdown_policy = install_contract.markdown_hygiene_policy(contract)
        self.assertEqual(
            set(markdown_policy.router_names),
            {"agents.md", "memory.md", "agent_chat.md"},
        )
        self.assertLess(
            markdown_policy.router_max_lines,
            markdown_policy.document_review_lines,
        )
        self.assertLess(
            markdown_policy.router_max_bytes,
            markdown_policy.document_review_bytes,
        )
        organization = install_contract.organization_policy(contract)
        self.assertEqual(organization.root_role, "Boss dell'Ecosistema")
        self.assertEqual(organization.sector_role, "Amministratore di settore")
        self.assertEqual(organization.default_reports_to, organization.root_role)
        room_policy = install_contract.room_lifecycle_policy(contract)
        self.assertEqual(
            room_policy.classifications,
            (
                "STANZA",
                "FONTE",
                "OUTPUT",
                "CAPACITA",
                "INFRASTRUTTURA",
                "ARCHIVIO",
                "SOSPETTA",
            ),
        )
        self.assertEqual(room_policy.bridge_content, "@AGENTS.md\n")
        self.assertEqual(room_policy.map_template, "ecosistema/STANZA_AGENTS.md")
        self.assertEqual(room_policy.source_template, "ecosistema/STANZA_FONTE.md")
        self.assertEqual(
            room_policy.root_owned_classifications,
            ("FONTE", "OUTPUT", "CAPACITA", "INFRASTRUTTURA", "ARCHIVIO"),
        )
        self.assertEqual(
            room_policy.root_owned_registry_paths,
            ("ecosistema/ASSET.md", "ecosistema/FONTI.md"),
        )
        self.assertIn("fonte operativa", room_policy.required_sections)
        self.assertEqual(
            room_policy.required_terms,
            (
                "amministratore del settore",
                "boss dell'ecosistema",
                "riporta al boss",
            ),
        )
        self.assertEqual(room_policy.required_terms_section, "organigramma")
        self.assertEqual(
            room_policy.business_source_section,
            "fonte business editabile",
        )
        self.assertEqual(
            room_policy.owner_source_headings,
            ("stato corrente", "prossimo passo", "decisioni", "scadenze"),
        )
        both_destinations = {
            rule.destination
            for rule in install_contract.template_rules(contract, "both")
        }
        self.assertIn(".codex/README.md", both_destinations)
        self.assertIn(".claude/README.md", both_destinations)
        self.assertIn("ecosistema/STANZA_FONTE.md", both_destinations)
        self.assertEqual(install_contract.forbidden_paths(contract, "both"), [])
        self.assertIn(
            ".claude/README.md",
            install_contract.forbidden_paths(contract, "codex"),
        )
        self.assertIn(
            ".codex/README.md",
            install_contract.forbidden_paths(contract, "claude"),
        )
        self.assertEqual(
            install_contract.external_effects(contract, "codex"),
            {"git_baseline"},
        )
        self.assertEqual(
            install_contract.external_effects(contract, "claude"),
            {"git_baseline", "claude_user_settings"},
        )
        self.assertEqual(
            install_contract.environment_checks(contract),
            {"default_browser", "desktop_launcher", "remote_backup"},
        )
        common_destinations = {
            str(rule["destination"])
            for rule in contract["common"]["templates"]
        }
        dynamic_defaults = {
            str(
                contract["semantic_requirements"][requirement][
                    "default_path"
                ]
            )
            for requirement in install_contract.semantic_requirements(contract)
        }
        self.assertTrue(
            common_destinations - dynamic_defaults
            <= set(install_contract.required_paths(contract, "codex"))
        )
        self.assertEqual(
            install_contract.semantic_requirements(contract),
            {"canonical_memory_index"},
        )
        self.assertEqual(dynamic_defaults, {"memory/MEMORY.md"})

    def test_room_lifecycle_rejects_ambiguous_or_weakened_policy(self):
        mutations = {
            "boolean_depth": lambda raw: raw.update(scan_depth=True),
            "reduced_depth": lambda raw: raw.update(scan_depth=1),
            "same_templates": lambda raw: raw.update(
                source_template=raw["map_template"]
            ),
            "asset_reused_as_map_template": lambda raw: raw.update(
                map_template="ecosistema/ASSET.md"
            ),
            "windows_drive_relative_template": lambda raw: raw.update(
                map_template="C:stanza.md"
            ),
            "invented_class": lambda raw: (
                raw["classifications"].append("CARAMELLA"),
                raw["root_owned_classifications"].append("CARAMELLA"),
            ),
            "reduced_sections": lambda raw: raw["required_sections"].pop(),
            "invented_term": lambda raw: raw["required_terms"].append(
                "formula inventata"
            ),
            "reduced_source_headings": lambda raw: raw[
                "owner_source_headings"
            ].pop(),
            "root_map_reused_as_registry": lambda raw: raw[
                "root_owned_registry_paths"
            ].__setitem__(0, "AGENTS.md"),
            "overlapping_sections": lambda raw: raw.update(
                contents_section=raw["owner_source_section"]
            ),
            "routed_section_not_required": lambda raw: raw.update(
                required_terms_section="sezione inventata"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                contract = copy.deepcopy(install_contract.CONTRACT)
                raw = contract["inspection_policies"]["room_lifecycle"]
                mutate(raw)
                with self.assertRaises(ValueError):
                    install_contract.room_lifecycle_policy(contract)

    def test_contract_rejects_duplicate_template_destinations(self):
        for case, destination in (
            ("exact", None),
            ("windows_case_collision", "ecosistema/asset.md"),
        ):
            with self.subTest(case=case):
                contract = copy.deepcopy(install_contract.CONTRACT)
                duplicate = copy.deepcopy(contract["common"]["templates"][0])
                duplicate["template"] = contract["common"]["templates"][1][
                    "template"
                ]
                if destination is not None:
                    duplicate["destination"] = destination
                contract["common"]["templates"].append(duplicate)

                with self.assertRaisesRegex(
                    ValueError,
                    "Destinazione template duplicata",
                ):
                    install_contract.template_rules(contract, "both")

    def test_every_contract_destination_is_installed_for_both(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            settings = self.settings_path(root)

            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "both",
                claude_user_settings_path=settings,
            )

            self.assertEqual(result.target_verdict, "PASSA")
            for rule in install_contract.template_rules(
                install_contract.CONTRACT,
                "both",
            ):
                self.assertTrue(
                    (target / rule.destination).is_file(),
                    rule.destination,
                )
            for rel in install_contract.required_paths(
                install_contract.CONTRACT,
                "both",
            ):
                self.assertTrue((target / rel).is_file(), rel)

    def test_rerun_rejects_tampered_room_templates(self):
        for relative in (
            "ecosistema/STANZA_AGENTS.md",
            "ecosistema/STANZA_FONTE.md",
        ):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                target = root / "Casa"
                settings = self.settings_path(root)
                leaderai_setup.run_setup(
                    target,
                    "Cliente",
                    "both",
                    claude_user_settings_path=settings,
                )
                (target / relative).write_text("", encoding="utf-8")

                result = leaderai_setup.run_setup(
                    target,
                    "Cliente",
                    "both",
                    claude_user_settings_path=settings,
                )

                self.assertEqual(result.target_verdict, "NON PASSA")
                self.assertTrue(
                    any("calco stanza" in blocker.lower() for blocker in result.blockers)
                )

    def test_claude_settings_preserve_other_keys_and_use_machine_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            settings = self.settings_path(root)
            settings.write_text(
                json.dumps(
                    {
                        "theme": "dark",
                        "permissions": {"allow": ["Read"]},
                    }
                ),
                encoding="utf-8",
            )

            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=settings,
            )

            payload = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(payload["theme"], "dark")
            self.assertEqual(payload["permissions"], {"allow": ["Read"]})
            self.assertEqual(
                payload["autoMemoryDirectory"],
                leaderai_setup._portable_machine_path(target / "memory"),
            )
            self.assertEqual(result.target_verdict, "PASSA")

    def test_claude_settings_under_home_use_portable_tilde_form(self):
        with tempfile.TemporaryDirectory(dir=Path.home()) as tmp:
            root = Path(tmp)
            target = root / "Casa"
            settings = self.settings_path(root)

            leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=settings,
            )

            payload = json.loads(settings.read_text(encoding="utf-8"))
            relative = (target / "memory").resolve().relative_to(
                Path.home().resolve()
            )
            self.assertEqual(
                payload["autoMemoryDirectory"],
                f"~/{relative.as_posix()}",
            )

    def test_one_global_settings_file_cannot_be_silently_reused_for_two_houses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "Casa-Uno"
            second = root / "Casa-Due"
            settings = self.settings_path(root)
            leaderai_setup.run_setup(
                first,
                "Cliente Uno",
                "claude",
                claude_user_settings_path=settings,
            )
            original = settings.read_text(encoding="utf-8")

            result = leaderai_setup.run_setup(
                second,
                "Cliente Due",
                "claude",
                claude_user_settings_path=settings,
            )

            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertTrue(
                any("memoria diversa" in item for item in result.blockers)
            )
            self.assertEqual(settings.read_text(encoding="utf-8"), original)
            self.assertFalse(second.exists())

    def test_agent_switch_blocks_before_creating_opposite_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            leaderai_setup.run_setup(target, "Cliente", "codex")

            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=self.settings_path(root),
            )

            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertFalse((target / ".claude" / "README.md").exists())
            self.assertTrue((target / ".codex" / "README.md").exists())
            self.assertIn(
                "Cambio agente bloccato",
                " | ".join(result.blockers),
            )

    def test_explicit_agent_migration_removes_only_generated_old_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            leaderai_setup.run_setup(target, "Cliente", "codex")

            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=self.settings_path(root),
                migrate_agent=True,
            )

            self.assertEqual(result.target_verdict, "PASSA")
            self.assertFalse((target / ".codex").exists())
            self.assertFalse((target / ".agents").exists())
            self.assertTrue((target / ".claude" / "README.md").is_file())
            self.assertIn(".codex/README.md", result.removed)
            self.assertIn(
                "Modalita' installata: `claude`.",
                (target / "AGENTS.md").read_text(encoding="utf-8"),
            )

    def test_agent_migration_preserves_unknown_customer_content_by_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            leaderai_setup.run_setup(target, "Cliente", "codex")
            customer_file = target / ".codex" / "cliente.txt"
            customer_file.write_text("preservare\n", encoding="utf-8")

            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=self.settings_path(root),
                migrate_agent=True,
            )

            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertEqual(customer_file.read_text(encoding="utf-8"), "preservare\n")
            self.assertFalse((target / ".claude" / "README.md").exists())

    def test_old_installed_version_never_passes_or_partially_upgrades(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            leaderai_setup.run_setup(target, "Cliente", "codex")
            agents = target / "AGENTS.md"
            old = agents.read_text(encoding="utf-8").replace(
                f"Versione standard applicata: `{leaderai_setup.STANDARD_VERSION}`.",
                "Versione standard applicata: `0.1.0`.",
            )
            agents.write_text(old, encoding="utf-8")
            before = agents.read_text(encoding="utf-8")

            result = leaderai_setup.run_setup(target, "Cliente", "codex")

            self.assertEqual(result.target_verdict, "NON PASSA")
            self.assertEqual(agents.read_text(encoding="utf-8"), before)
            self.assertIn(
                "STANDARD_VERSION_OUTDATED",
                result.inspection_codes,
            )

    def test_setup_and_inspector_share_the_same_target_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            settings = self.settings_path(root)
            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=settings,
            )
            inspection = ecosistema_inspector.inspect_ecosystem(
                target,
                agent="claude",
                claude_user_settings_path=settings,
            )
            self.assertEqual(result.target_verdict, inspection.verdict)
            self.assertFalse((target / "REPORT_FINALE.md").exists())
            self.assertIn(
                leaderai_setup.STANDARD_VERSION,
                (target / "logs" / "install-log.md").read_text(encoding="utf-8"),
            )

    def test_identical_rerun_is_idempotent_and_leaves_clean_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "Casa"
            settings = self.settings_path(root)
            leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=settings,
            )
            log_before = (target / "logs" / "install-log.md").read_text(
                encoding="utf-8"
            )

            result = leaderai_setup.run_setup(
                target,
                "Cliente",
                "claude",
                claude_user_settings_path=settings,
            )
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(target),
                check=True,
                capture_output=True,
                text=True,
            ).stdout

            self.assertEqual(result.created, [])
            self.assertEqual(result.updated, [])
            self.assertEqual(result.removed, [])
            self.assertEqual(status, "")
            self.assertFalse((target / "REPORT_FINALE.md").exists())
            self.assertEqual(
                (target / "logs" / "install-log.md").read_text(encoding="utf-8"),
                log_before,
            )


if __name__ == "__main__":
    unittest.main()
