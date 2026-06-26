import tempfile
import unittest
from pathlib import Path

import leaderai_setup


class LeaderAISetupTest(unittest.TestCase):
    def test_creates_cervello_and_ecosistema(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "EcosistemaAI-Test"
            result = leaderai_setup.run_setup(target, "Cliente Test", "both")

            self.assertIn("AGENTS.md", result.created)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertTrue((target / ".codex" / "README.md").exists())
            self.assertTrue((target / ".claude" / "README.md").exists())
            self.assertTrue((target / "memory" / "MEMORY.md").exists())
            self.assertTrue((target / "ecosistema" / "FONTI.md").exists())
            self.assertTrue((target / "REPORT_FINALE.md").exists())

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Cliente Test", agents)

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


if __name__ == "__main__":
    unittest.main()
