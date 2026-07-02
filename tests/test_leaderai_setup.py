import subprocess
import tempfile
import unittest
from pathlib import Path

import leaderai_setup


class LeaderAISetupTest(unittest.TestCase):
    def test_creates_cervello_and_ecosistema(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            result = leaderai_setup.run_setup(target, "Cliente Test", "claude")

            self.assertIn("AGENTS.md", result.created)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertTrue((target / ".claude" / "README.md").exists())
            self.assertFalse((target / ".codex" / "README.md").exists())
            self.assertTrue((target / "memory" / "MEMORY.md").exists())
            self.assertTrue((target / "ecosistema" / "FONTI.md").exists())
            self.assertTrue((target / "ecosistema" / "ASSET.md").exists())
            self.assertTrue((target / "REPORT_FINALE.md").exists())

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            asset = (target / "ecosistema" / "ASSET.md").read_text(encoding="utf-8")
            report = (target / "REPORT_FINALE.md").read_text(encoding="utf-8")
            self.assertIn("Cliente Test", agents)
            self.assertIn("Modalita' installata: `claude`.", agents)
            self.assertIn("Comunicazione e fonti di verita'", agents)
            self.assertIn("non va in chat", agents)
            self.assertIn("Asset operativi", asset)
            self.assertIn("FASE 1 - CERVELLO", report)
            self.assertIn("FASE 2 - ECOSISTEMA", report)
            self.assertIn("MAPPA COMUNICAZIONE", report)
            self.assertIn("Procedure e 'come si fa'", report)
            self.assertIn("MAPPA MODULI", report)
            self.assertIn("PEC/email certificata", report)
            self.assertIn("Skill per lavori ripetuti", report)

    def test_first_commit_photographs_install(self):
        # La cartella madre deve nascere come repository CON cronologia:
        # senza primo commit il backup della Fase 7 parte da un repo vuoto.
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            result = leaderai_setup.run_setup(target, "Cliente Test", "claude")

            log = subprocess.run(
                ["git", "log", "--oneline"],
                cwd=str(target),
                capture_output=True,
                text=True,
            )
            self.assertEqual(log.returncode, 0)
            self.assertIn("installazione iniziale", log.stdout)
            porcelain = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(target),
                capture_output=True,
                text=True,
            )
            self.assertEqual(porcelain.stdout.strip(), "")
            self.assertTrue(
                any("primo commit creato" in d for d in result.decisions)
            )

    def test_second_run_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            leaderai_setup.run_setup(target, "Cliente Test", "codex")
            marker = "MODIFICA CLIENTE\n"
            (target / "AGENTS.md").write_text(marker, encoding="utf-8")

            result = leaderai_setup.run_setup(target, "Cliente Test", "codex")

            self.assertIn("AGENTS.md", result.existing)
            self.assertEqual((target / "AGENTS.md").read_text(encoding="utf-8"), marker)
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_both_is_explicit_and_creates_both_agent_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            leaderai_setup.run_setup(target, "Cliente Test", "both")

            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertTrue((target / ".claude" / "README.md").exists())
            self.assertTrue((target / ".codex" / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
