import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTRACT_FILES = [
    "AGENTS.md",
    "README.md",
    "MANIFEST.md",
    "01 - Cervello - installazione e aggiornamento.md",
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

    def test_delivery_email_is_a_short_pointer_to_the_single_operational_file(self):
        email = self.read("EMAIL_CONSEGNA.md")
        install = self.read("01 - Cervello - installazione e aggiornamento.md")

        self.assertLess(len(email.splitlines()), 80)
        self.assertIn("Ciao [NOME]", email)
        self.assertIn("01 - Cervello - installazione e aggiornamento.md", email)
        self.assertIn(
            "https://drive.google.com/file/d/19l_f_VViewXaVVhq3in9KBnnqkoRyh7E/view",
            email,
        )
        self.assertIn("mostra a sal", email.lower())
        self.assertIn("autorizzazione esplicita", email)
        self.assertIn("controlla gmail inviati", email.lower())
        self.assertNotIn("github.com/salChiarenza/leaderai-cervello-ecosistema/blob/", email)
        for operational_only in [
            "SITUAZIONE IN BREVE",
            "AI_ACT_CHECK_OK",
            "ID missione",
            "%USERPROFILE%",
            "SERVE UN TUO PASSAGGIO",
        ]:
            with self.subTest(operational_only=operational_only):
                self.assertNotIn(operational_only, email)
                self.assertIn(operational_only, install)
        version = self.read("VERSION").strip()
        self.assertIn(f"Versione corrente: `{version}`", install)
        self.assertIn("installazione e aggiornamento", install.lower())
        self.assertNotIn("Modello email di consegna", install)
        for relative_path in [
            "AGENTS.md",
            "README.md",
            "MANIFEST.md",
            "01 - Cervello - installazione e aggiornamento.md",
        ]:
            with self.subTest(pointer=relative_path):
                self.assertIn("EMAIL_CONSEGNA.md", self.read(relative_path))

    def test_ai_act_gate_is_installed_and_blocks_unclear_delivery(self):
        email = self.read("EMAIL_CONSEGNA.md")
        install = self.read("01 - Cervello - installazione e aggiornamento.md")
        processes = self.read("templates/PROCESSI.md")
        limits = self.read("templates/LIMITI.md")

        for surface in (install, processes):
            self.assertIn("AI_ACT_CHECK_OK", surface)
            self.assertIn("sistema", surface.lower())
            self.assertIn("ruolo", surface.lower())
            self.assertIn("rischio", surface.lower())

        self.assertIn("NON PASSA", install)
        self.assertIn("NON PASSA", processes)
        self.assertIn("NON PASSA", limits)

    def test_checkup_and_inspector_skill_read_machine_contract(self):
        self.assertIn("install_contract.json", self.read("CHECKUP.md"))
        self.assertIn(
            "install_contract.json",
            self.read("templates/ISPETTORE_SKILL.md"),
        )

    def test_manutentore_skill_repairs_only_reversible_things(self):
        skill = self.read("templates/MANUTENTORE_SKILL.md")
        self.assertIn("name: manutentore-ecosistema", skill)
        self.assertIn("guardiano_stanze.sh --misura", skill)
        # Il nome di un archivio non prova manutenzione: la prova nativa
        # controlla accorpamento nella fonte, conservazione e assenza di copie.
        self.assertIn("48 ore", skill)
        self.assertIn("Vietato, sempre: eliminare", skill)
        self.assertIn("ecosystem-check/CONTROLLI.md", skill)
        self.assertIn("manutenzione-ecosistema", skill)
        registry = self.read("templates/ecosystem-check/CONTROLLI.md")
        for column in ("Chi controlla", "Quando", "Cosa misura", "Dove scrive", "Stato"):
            self.assertIn(column, registry)
        contract = json.loads(self.read("install_contract.json"))
        for agent, path in (
            ("claude", ".claude/skills/manutentore-ecosistema/SKILL.md"),
            ("codex", ".agents/skills/manutentore-ecosistema/SKILL.md"),
        ):
            self.assertIn(path, contract["agents"][agent]["required"])
        self.assertIn("ecosystem-check/CONTROLLI.md", contract["common"]["required"])

    def test_remote_push_requires_explicit_command(self):
        install = self.read("01 - Cervello - installazione e aggiornamento.md")
        self.assertIn(
            "esegui `git push` soltanto dopo il mio comando",
            install,
        )
        self.assertNotIn(
            "il push lo fa l'agente da solo a fine sessione",
            install,
        )

    def test_delivery_email_has_one_human_reader_and_no_embedded_mission(self):
        email = self.read("EMAIL_CONSEGNA.md")

        self.assertIn("Ciao [NOME]", email)
        for embedded_mission_phrase in [
            "Modo corrente: `AGENTE_CON_POSTA`",
            "Questa missione operativa e' per l'agente AI che gestisce",
            "ISTRUZIONI PER L'AGENTE",
            "CHIUSURA LOCALE",
        ]:
            with self.subTest(phrase=embedded_mission_phrase):
                self.assertNotIn(embedded_mission_phrase, email)

    def test_agent_emails_have_human_readable_progress_first(self):
        checkup = self.read("CHECKUP.md")
        processes = self.read("templates/PROCESSI.md")

        for relative, text in [
            ("CHECKUP.md", checkup),
            ("templates/PROCESSI.md", processes),
        ]:
            with self.subTest(relative=relative):
                self.assertIn("SITUAZIONE IN BREVE", text)
                self.assertIn("Cosa funziona:", text)
                self.assertIn("Cosa completiamo:", text)
                self.assertIn("Cosa serve da te:", text)
                self.assertIn("Quando si chiude:", text)

    def test_mission_closes_locally_without_return_email(self):
        checkup = self.read("CHECKUP.md")

        self.assertNotIn("fai un nuovo autocontrollo e mandi un nuovo", checkup)
        self.assertNotIn("nuova autorizzazione prima dell'invio finale", checkup)
        self.assertIn("zero aggiornamenti intermedi", checkup)
        self.assertIn("SALVATAGGIO NELLA CASA", checkup)
        self.assertIn("manca `AGENT_CHAT.md`", checkup)

    def test_mission_email_cycle_closes_in_the_client_house(self):
        for relative in (
            "AGENTS.md",
            "CHECKUP.md",
            "01 - Cervello - installazione e aggiornamento.md",
            "MANIFEST.md",
            "README.md",
            "templates/PROCESSI.md",
        ):
            text = " ".join(self.read(relative).split())
            with self.subTest(relative=relative):
                self.assertIn("una volta sola", text)
                self.assertTrue(
                    "chiusura locale" in text.lower()
                    or "chiude localmente" in text.lower()
                )
                self.assertIn("DA DECIDERE IN CALL", text)
                self.assertNotIn("CONTINUA TERMINALE", text)

    def test_entrypoint_gate_is_in_installation_and_agent_boot_files(self):
        install = self.read("01 - Cervello - installazione e aggiornamento.md")
        checkup = self.read("CHECKUP.md")
        codex = self.read("templates/CODEX_README.md")
        claude = self.read("templates/CLAUDE_README.md")
        agents = self.read("templates/AGENTS.md")

        for text in (install, checkup, codex, agents):
            normalized = " ".join(text.split())
            self.assertIn("FUORI DAL CERVELLO", normalized)
            self.assertIn("nuova task", normalized)
            self.assertIn("tre regole", normalized)
        self.assertIn("progetto locale primario", codex)
        self.assertIn('codex app "<CARTELLA_MADRE>"', codex)
        self.assertIn('codex -C "<CARTELLA_MADRE>"', codex)
        self.assertIn("nuova sessione", claude)
        self.assertIn("/context", claude)
        self.assertIn("/memory", claude)

    def test_brand_identity_and_cross_agent_handoff_are_blocking_checks(self):
        checkup = self.read("CHECKUP.md")
        chat = self.read("templates/AGENT_CHAT.md")
        manifest = self.read("MANIFEST.md")

        self.assertIn("Crea la Brand Identity", checkup)
        self.assertIn("senza indizi", checkup)
        self.assertIn("Codex -> Claude Code -> Codex", checkup)
        for field in (
            "ID missione",
            "agente proprietario",
            "base Git",
            "Prove",
            "PRESO IN CARICO",
        ):
            self.assertIn(field, chat)
        self.assertIn("Crea la Brand Identity", manifest)

    def test_delivery_email_keeps_only_sender_checks(self):
        email = self.read("EMAIL_CONSEGNA.md")

        self.assertIn("sal@salchiarenza.com", email)
        self.assertIn("destinatario", email)
        self.assertIn("versione corrente", " ".join(email.split()))
        self.assertIn("link si apra", " ".join(email.split()))
        self.assertNotIn("ID missione", email)
        self.assertNotIn("%USERPROFILE%", email)


if __name__ == "__main__":
    unittest.main()
