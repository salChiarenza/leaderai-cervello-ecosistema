import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "templates" / "BACKUP_CASA.py"


class BackupCasaTest(unittest.TestCase):
    """La casa non e' un registro git (decisione di Sal, 16/09/2026): il backup
    e' una copia zip datata in una cartella scelta dal proprietario."""

    def make_house(self, tmp: Path) -> Path:
        casa = tmp / "EcosistemaAI-Prova"
        (casa / ".agent" / "hooks").mkdir(parents=True)
        (casa / "memory").mkdir()
        (casa / ".secrets").mkdir()
        (casa / "stanza").mkdir()
        (casa / "stanza" / "pratiche").mkdir()
        (casa / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
        (casa / "memory" / "MEMORY.md").write_text("indice\n", encoding="utf-8")
        (casa / ".secrets" / "token.json").write_text("{}", encoding="utf-8")
        (casa / "api-token-prova.txt").write_text("x", encoding="utf-8")
        (casa / "stanza" / "AGENTS.md").write_text(
            "# Stanza\n\n- `pratiche/` — ARCHIVIO PROTETTO: fascicoli\n", encoding="utf-8"
        )
        (casa / "stanza" / "pratiche" / "fascicolo.pdf").write_bytes(b"%PDF")
        (casa / "stanza" / "note.md").write_text("note\n", encoding="utf-8")
        return casa

    def run_tool(self, casa: Path, *args: str):
        return subprocess.run(
            ["python3", str(TOOL), "--casa", str(casa), *args],
            capture_output=True, text=True, check=False,
        )

    def test_without_folder_it_says_so_and_does_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            casa = self.make_house(Path(tmp))
            result = self.run_tool(casa)
            self.assertEqual(result.returncode, 0)
            self.assertIn("non ancora scelta", result.stdout)
            self.assertFalse((casa / "logs" / "backup-log.md").exists())

    def test_imposta_makes_first_copy_without_secrets_or_protected_archives(self):
        with tempfile.TemporaryDirectory() as tmp:
            casa = self.make_house(Path(tmp))
            copie = Path(tmp) / "Copie"
            result = self.run_tool(casa, "--imposta", str(copie), "--conserva", "2")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("BACKUP OK", result.stdout)
            config = json.loads((casa / ".agent" / "backup_casa.json").read_text(encoding="utf-8"))
            self.assertEqual(config["conserva"], 2)
            zips = sorted(copie.glob("Cervello-EcosistemaAI-Prova-*.zip"))
            self.assertEqual(len(zips), 1)
            names = zipfile.ZipFile(zips[0]).namelist()
            self.assertIn("AGENTS.md", names)
            self.assertIn("memory/MEMORY.md", names)
            self.assertIn("stanza/note.md", names)
            self.assertIn("stanza/AGENTS.md", names)
            self.assertNotIn(".secrets/token.json", names)
            self.assertNotIn("api-token-prova.txt", names)
            self.assertNotIn("stanza/pratiche/fascicolo.pdf", names)
            self.assertNotIn(".agent/backup_casa.json", [n for n in names if "token" in n])
            log = (casa / "logs" / "backup-log.md").read_text(encoding="utf-8")
            self.assertIn("file in", log)

    def test_keeps_only_the_last_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            casa = self.make_house(Path(tmp))
            copie = Path(tmp) / "Copie"
            self.run_tool(casa, "--imposta", str(copie), "--conserva", "2")
            for n in range(3):
                vecchia = copie / f"Cervello-EcosistemaAI-Prova-2020-01-0{n + 1}-0800.zip"
                zipfile.ZipFile(vecchia, "w").close()
            result = self.run_tool(casa)
            self.assertEqual(result.returncode, 0)
            zips = sorted(copie.glob("Cervello-EcosistemaAI-Prova-*.zip"))
            self.assertEqual(len(zips), 2)
            self.assertTrue(all("2020-01-0" not in z.name for z in zips[:0]))

    def test_stato_reports_folder_and_last_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            casa = self.make_house(Path(tmp))
            copie = Path(tmp) / "Copie"
            self.run_tool(casa, "--imposta", str(copie))
            result = self.run_tool(casa, "--stato")
            self.assertEqual(result.returncode, 0)
            self.assertIn("ultima copia: Cervello-EcosistemaAI-Prova-", result.stdout)

    def test_refuses_a_folder_that_is_not_a_house(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_tool(Path(tmp))
            self.assertEqual(result.returncode, 1)
            self.assertIn("non sembra una casa", result.stdout)


if __name__ == "__main__":
    unittest.main()
