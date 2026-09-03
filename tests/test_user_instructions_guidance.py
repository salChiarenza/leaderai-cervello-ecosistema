import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


class UserInstructionsGuidanceTest(unittest.TestCase):
    """Lezioni del 03/09/2026 (caso Pastore) promosse a testo dello standard.

    L'agente aperto da un'altra cartella non sapeva che la casa esistesse;
    sei soggetti giuridici sono emersi dopo una proposta su tre attivita'; un
    rapporto lungo e' partito con collaudo incompleto; l'Ispettore era stato
    rimandato alla sessione successiva.
    """

    def test_install_guide_requires_global_instructions_and_proof_from_outside(self):
        text = _flat(ROOT / "INSTALLA_CON_AI.md")
        for phrase in [
            "4-bis. Istruzioni globali dell'agente attivo",
            "~/.claude/CLAUDE.md",
            "~/.codex/AGENTS.md",
            "blocco `LEADERAI-CASA`",
            "aggiungi o aggiorna soltanto il blocco tra i due marcatori",
            "apri l'agente da una cartella estranea",
            "`user_instructions_gate`",
            "`templates/CLAUDE_USER.md`",
            "`templates/CODEX_USER_AGENTS.md`",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_install_guide_closes_with_inspector_in_a_new_session(self):
        text = _flat(ROOT / "INSTALLA_CON_AI.md")
        self.assertIn("in una NUOVA sessione nata dalla cartella madre", text)
        self.assertIn("ultimo passo obbligatorio dell'installazione", text)
        self.assertIn("solo allora l'installazione e' chiusa", text)

    def test_final_confirmation_requires_full_pass_everywhere(self):
        surfaces = {
            "INSTALLA_CON_AI.md": "soltanto con verdetto `PASSA` pieno",
            "CHECKUP.md": "soltanto con verdetto `PASSA` pieno",
            "EMAIL_CONSEGNA.md": "`PASSA` pieno",
            "MANIFEST.md": "parte soltanto con verdetto `PASSA` pieno",
            "templates/AGENTS.md": "con verdetto `PASSA` pieno",
            "templates/PROCESSI.md": "soltanto con verdetto `PASSA` pieno",
            "templates/ISPETTORE_SKILL.md": "soltanto con verdetto `PASSA` pieno",
        }
        for name, phrase in surfaces.items():
            text = _flat(ROOT / name)
            with self.subTest(surface=name):
                self.assertIn(phrase, text)
                self.assertIn("PASSA CON ATTENZIONE", text)
                self.assertIn("SERVE UN TUO PASSAGGIO", text)

    def test_subjects_registry_is_part_of_the_common_frame(self):
        template = _flat(ROOT / "templates" / "SOGGETTI.md")
        self.assertIn("piu' soggetti, una casa", template.lower())
        self.assertIn("Le stanze seguono le funzioni del lavoro", template)
        self.assertIn("| {{client_name}} |", template)
        for name in [
            "MANIFEST.md",
            "README.md",
            "AGENTS.md",
            "CHECKUP.md",
            "INSTALLA_CON_AI.md",
            "templates/AGENTS.md",
            "templates/MEMORY.md",
            "templates/ISPETTORE_SKILL.md",
        ]:
            with self.subTest(surface=name):
                self.assertIn("SOGGETTI.md", _flat(ROOT / name))
        guardian = (ROOT / "templates" / "GUARDIANO_STANZE.sh").read_text(encoding="utf-8")
        self.assertIn("SOGGETTI.md", guardian)

    def test_guided_path_keeps_structural_decisions_in_session(self):
        for name in ["templates/AGENTS.md", "templates/LIMITI.md", "INSTALLA_CON_AI.md", "CHECKUP.md"]:
            text = _flat(ROOT / name)
            with self.subTest(surface=name):
                self.assertIn("DA DECIDERE IN CALL", text)
        self.assertIn("PERCORSO GUIDATO CHIUSO", _flat(ROOT / "templates" / "AGENTS.md"))
        self.assertIn("PERCORSO GUIDATO CHIUSO", _flat(ROOT / "INSTALLA_CON_AI.md"))

    def test_checkup_and_skill_verify_global_instructions(self):
        checkup = _flat(ROOT / "CHECKUP.md")
        skill = _flat(ROOT / "templates" / "ISPETTORE_SKILL.md")
        for text, label in ((checkup, "CHECKUP.md"), (skill, "ISPETTORE_SKILL.md")):
            with self.subTest(surface=label):
                self.assertIn("LEADERAI-CASA", text)
                self.assertIn("~/.claude/CLAUDE.md", text)
                self.assertIn("~/.codex/AGENTS.md", text)
                self.assertIn("FUORI DAL CERVELLO", text)
        self.assertIn("USER_INSTRUCTIONS_MISSING", checkup)
        self.assertIn("USER_INSTRUCTIONS_WITHOUT_HOUSE", checkup)
        self.assertIn("USER_INSTRUCTIONS_WITHOUT_GATE", checkup)

    def test_readmes_explain_why_the_gate_works_from_outside(self):
        for name in ["templates/CLAUDE_README.md", "templates/CODEX_README.md"]:
            text = _flat(ROOT / name)
            with self.subTest(surface=name):
                self.assertIn("LEADERAI-CASA", text)
                self.assertIn("parte cieco", text)

    def test_checkup_updates_managed_files_before_new_registries(self):
        checkup = _flat(ROOT / "CHECKUP.md")
        skill = _flat(ROOT / "templates" / "ISPETTORE_SKILL.md")
        self.assertIn("prima i file gestiti dallo standard", checkup)
        self.assertIn("poi registri e calchi nuovi", checkup)
        self.assertIn("un guardiano vecchio blocca i file nuovi", skill)

    def test_guided_path_phase_is_declared_and_enforced(self):
        template = _flat(ROOT / "templates" / "AGENTS.md")
        self.assertIn("Fase del percorso: 1 (Cervello)", template)
        self.assertIn("sotto il 3 nessuna stanza di lavoro", template)
        for name, phrase in {
            "CHECKUP.md": "ROOM_BEFORE_STEP_3",
            "templates/ISPETTORE_SKILL.md": "ROOM_BEFORE_STEP_3",
            "INSTALLA_CON_AI.md": "Fase del percorso: 1 (Cervello)",
            "EMAIL_CONSEGNA.md": "Fase del percorso: [N di 4]",
            "MANIFEST.md": "fase del percorso guidato dichiarata nella mappa madre",
        }.items():
            with self.subTest(surface=name):
                self.assertIn(phrase, _flat(ROOT / name))
        guardian = (ROOT / "templates" / "GUARDIANO_STANZE.sh").read_text(encoding="utf-8")
        self.assertIn("stanza creata prima del passo 3", guardian)

    def test_windows_backslash_lesson_is_in_the_install_guide(self):
        text = _flat(ROOT / "INSTALLA_CON_AI.md")
        self.assertIn("backslash siano intatti", text)
        self.assertIn("sed, awk", text)


if __name__ == "__main__":
    unittest.main()
