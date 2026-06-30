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
            self.assertIn("Asset operativi", asset)
            self.assertIn("FASE 1 - CERVELLO", report)
            self.assertIn("FASE 2 - ECOSISTEMA", report)

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
