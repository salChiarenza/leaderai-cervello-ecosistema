import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT_FILES = [
    "AGENTS.md",
    "README.md",
    "MANIFEST.md",
    "INSTALLA_CON_AI.md",
    "CHECKUP.md",
    "templates/AGENTS.md",
]

OLD_FORMULAS = [
    "`CLAUDE.md` se il cliente usa Claude Code",
    "`CLAUDE.md` se richiesto Claude Code",
    "`CLAUDE.md` come ponte verso `AGENTS.md` quando si usa Claude Code",
    "`CLAUDE.md` e `.claude/README.md` devono esistere solo in modalita'",
    "In modalita' Claude, il `CLAUDE.md` locale",
    "`AGENTS.md` e, per Claude, ponte `CLAUDE.md`",
]


class CrossAgentContractTest(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_canonical_bridge_template_is_single_source_of_truth(self):
        template = self.read("templates/CLAUDE.md")

        self.assertEqual(template, "@AGENTS.md\n")
        self.assertEqual(template.count("@AGENTS.md"), 1)

    def test_every_versioned_agents_file_has_a_local_bridge(self):
        agents_files = [
            path for path in ROOT.rglob("AGENTS.md") if ".git" not in path.parts
        ]

        self.assertGreaterEqual(len(agents_files), 2)
        for agents_path in agents_files:
            bridge = agents_path.with_name("CLAUDE.md")
            with self.subTest(room=agents_path.parent.relative_to(ROOT)):
                self.assertTrue(bridge.is_file(), f"ponte mancante: {bridge}")
                self.assertFalse(
                    bridge.is_symlink(),
                    f"ponte non Windows-safe: {bridge}",
                )
                self.assertEqual(
                    bridge.read_text(encoding="utf-8"),
                    "@AGENTS.md\n",
                )

    def test_all_contract_docs_declare_the_universal_bridge(self):
        for relative_path in CONTRACT_FILES:
            text = self.read(relative_path)
            with self.subTest(file=relative_path):
                self.assertIn("AGENTS.md", text)
                self.assertIn("CLAUDE.md", text)
                self.assertIn(
                    "@AGENTS.md",
                    text,
                    f"{relative_path} deve mostrare il ponte canonico",
                )
                normalized = " ".join(text.split()).lower()
                self.assertRegex(
                    normalized,
                    r"(claude\.md.{0,180}(sempre|universale)|"
                    r"(sempre|universale).{0,180}claude\.md)",
                    f"{relative_path} deve dichiarare CLAUDE.md nel telaio comune",
                )

    def test_active_agent_branches_remain_conditional(self):
        for relative_path in CONTRACT_FILES:
            text = self.read(relative_path)
            with self.subTest(file=relative_path):
                self.assertIn(".codex", text)
                self.assertIn(".claude", text)

        checkup = self.read("CHECKUP.md")
        self.assertIn("Ramo Codex — solo se Codex e' attivo", checkup)
        self.assertIn("Ramo Claude Code — solo se Claude Code e' attivo", checkup)
        self.assertIn("`.codex/config.toml`", checkup)
        self.assertIn("`.claude/settings.json`", checkup)
        self.assertIn("entrambi i rami", checkup)

    def test_checkup_cannot_pass_without_bridge_and_active_branch(self):
        checkup = self.read("CHECKUP.md")
        gate = checkup.split("## Gate di conformita' — verdetto bloccante", 1)[1]

        self.assertIn("manca `AGENTS.md`", gate)
        self.assertIn("manca `CLAUDE.md`", gate)
        self.assertIn("manca `.codex/README.md` quando Codex e' attivo", gate)
        self.assertIn(
            "manca `.claude/README.md` quando Claude Code e' attivo",
            gate,
        )
        self.assertIn(
            "manca `.agents/skills/ispettore-ecosistema/SKILL.md` "
            "quando Codex e' attivo",
            gate,
        )
        self.assertIn(
            "manca `.claude/skills/ispettore-ecosistema/SKILL.md` "
            "quando Claude Code e'",
            gate,
        )
        self.assertIn("obbligatoriamente `NON PASSA`", gate)
        self.assertIn("PASSA CON ATTENZIONE", gate)

    def test_old_conditional_bridge_formulas_do_not_return(self):
        for relative_path in CONTRACT_FILES:
            text = self.read(relative_path)
            for formula in OLD_FORMULAS:
                with self.subTest(file=relative_path, formula=formula):
                    self.assertNotIn(formula, text)

    def test_delivery_email_is_versioned_and_never_sends_automatically(self):
        email = self.read("EMAIL_CONSEGNA.md")
        install = self.read("INSTALLA_CON_AI.md")

        self.assertIn("Modello unico e versionabile", email)
        self.assertIn(
            "https://github.com/salChiarenza/leaderai-cervello-ecosistema",
            email,
        )
        self.assertIn(
            "https://github.com/salChiarenza/leaderai-cervello-ecosistema/"
            "blob/main/INSTALLA_CON_AI.md",
            email,
        )
        self.assertIn("autorizzazione esplicita", email)
        self.assertIn(
            "l'autorizzazione successiva del proprietario attiva "
            "l'eventuale invio del report",
            " ".join(email.split()),
        )
        self.assertIn("PROVA_DESTINATARIO", email)
        self.assertIn(
            "[FIRMA AGENTE: Sal & Codex / Sal & Claude Code]",
            email,
        )
        self.assertNotIn("Modello email di consegna", install)
        for relative_path in [
            "AGENTS.md",
            "README.md",
            "MANIFEST.md",
            "INSTALLA_CON_AI.md",
        ]:
            with self.subTest(pointer=relative_path):
                self.assertIn("EMAIL_CONSEGNA.md", self.read(relative_path))

    def test_delivery_email_has_one_direct_operational_reader(self):
        email = self.read("EMAIL_CONSEGNA.md")

        self.assertIn("Modo corrente: `AGENTE_CON_POSTA`", email)
        self.assertIn(
            "Questa missione operativa e' per l'agente AI che gestisce",
            email,
        )
        for mixed_reader_phrase in [
            "Ciao [NOME]",
            "apri [AGENTE ATTIVO",
            "Affidagli questa missione",
            "leggi l'ultima email",
            "digli di leggere",
        ]:
            with self.subTest(phrase=mixed_reader_phrase):
                self.assertNotIn(mixed_reader_phrase, email)

    def test_every_continue_requires_a_new_send_authorization(self):
        checkup = self.read("CHECKUP.md")

        self.assertNotIn("fai un nuovo autocontrollo e mandi un nuovo", checkup)
        self.assertIn("nuova autorizzazione prima di ogni nuovo invio", checkup)
        self.assertIn("manca `AGENT_CHAT.md`", checkup)


if __name__ == "__main__":
    unittest.main()
