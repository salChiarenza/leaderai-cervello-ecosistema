import tempfile
import unittest
from pathlib import Path

import leaderai_setup


ROOM_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "STATO.md",
    "REGISTRO_CONTROLLI.md",
    "STANDARD_REPARTO.md",
    "ruoli/ORCHESTRATORE.md",
    "ruoli/CONTROLLO_STRUTTURA.md",
    "ruoli/CONTROLLO_ISTRUZIONI.md",
    "ruoli/CONTROLLO_CONTINUITA.md",
    "ruoli/INTERVENTO.md",
    "ruoli/CONTROLLO_CHIUSURA.md",
)


class EcosystemCheckRoomTest(unittest.TestCase):
    def install(self, target: Path):
        return leaderai_setup.run_setup(
            target,
            "Cliente Test",
            "both",
            claude_user_settings_path=target.parent / "claude-user-settings.json",
            claude_user_instructions_path=(target.parent / "claude-user-settings.json").with_name("claude-user-CLAUDE.md"),
            codex_user_instructions_path=(target.parent / "claude-user-settings.json").with_name("codex-user-AGENTS.md"),
        )

    def test_fresh_install_creates_complete_ecosystem_check_room(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Cliente-Test"

            self.install(target)

            missing = [
                relative
                for relative in ROOM_FILES
                if not (target / "ecosystem-check" / relative).is_file()
            ]
            self.assertEqual(missing, [])
            self.assertEqual(
                (target / "ecosystem-check" / "CLAUDE.md").read_text(
                    encoding="utf-8"
                ),
                "@AGENTS.md\n",
            )
            root_map = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("[Ecosystem Check](ecosystem-check/)", root_map)
            state = (target / "ecosystem-check" / "STATO.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Cliente Test", state)
            self.assertIn("## Stato corrente", state)
            self.assertIn("## Prossimo passo", state)
            self.assertIn("## Decisioni", state)
            self.assertIn("## Scadenze", state)

    def test_reinstall_preserves_ecosystem_check_operational_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Cliente-Test"
            self.install(target)
            state = target / "ecosystem-check" / "STATO.md"
            register = target / "ecosystem-check" / "REGISTRO_CONTROLLI.md"
            self.assertTrue(state.is_file())
            self.assertTrue(register.is_file())
            state.write_text("STATO DEL CLIENTE\n", encoding="utf-8")
            register.write_text("STORIA DEL CLIENTE\n", encoding="utf-8")

            self.install(target)

            self.assertEqual(state.read_text(encoding="utf-8"), "STATO DEL CLIENTE\n")
            self.assertEqual(
                register.read_text(encoding="utf-8"), "STORIA DEL CLIENTE\n"
            )


if __name__ == "__main__":
    unittest.main()
