import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "templates" / "SALVATAGGIO_AUTOMATICO.py"


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


class SalvataggioAutomaticoTest(unittest.TestCase):
    """Caso reale 16/09/2026: la barra «Conferma modifiche» a ogni turno.
    A fine turno la casa si salva da sola, segreti esclusi, senza mai bloccare."""

    def run_hook(self, casa: Path):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(casa))
        return subprocess.run(
            ["python3", str(HOOK)], input="{}", cwd=str(casa), env=env,
            capture_output=True, text=True, check=False,
        )

    def test_registered_for_claude_codex_and_contract(self):
        claude = json.loads((ROOT / "templates" / "CLAUDE_SETTINGS.json").read_text(encoding="utf-8"))
        self.assertTrue(any(
            "salvataggio_automatico.py" in h["command"]
            for group in claude["hooks"]["Stop"] for h in group["hooks"]
        ))
        codex = json.loads((ROOT / "templates" / "CODEX_HOOKS.json").read_text(encoding="utf-8"))
        entries = [h for group in codex["hooks"]["Stop"] for h in group["hooks"] if "salvataggio_automatico.py" in h["command"]]
        self.assertEqual(len(entries), 1)
        self.assertIn("salvataggio_automatico.py", entries[0]["commandWindows"])
        contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
        text = json.dumps(contract)
        self.assertIn('"template": "SALVATAGGIO_AUTOMATICO.py"', text)
        self.assertIn(".agent/hooks/salvataggio_automatico.py", text)
        doc = (ROOT / "01 - Cervello - installazione e aggiornamento.md").read_text(encoding="utf-8")
        self.assertIn("salvataggio_automatico.py", doc)

    def test_saves_changes_and_leaves_secrets_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            casa = Path(tmp)
            git("init", "-q", "-b", "main", cwd=casa)
            git("config", "user.name", "Prova", cwd=casa)
            git("config", "user.email", "prova@example.com", cwd=casa)
            (casa / "AGENTS.md").write_text("# Casa\n", encoding="utf-8")
            git("add", "-A", cwd=casa); git("commit", "-q", "-m", "primo", cwd=casa)
            (casa / "memory").mkdir()
            (casa / "memory" / "nota.md").write_text("una nota\n", encoding="utf-8")
            (casa / "token_drive.json").write_text("{}", encoding="utf-8")
            (casa / ".env").write_text("SEGRETO=1\n", encoding="utf-8")
            result = self.run_hook(casa)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            log = git("log", "--oneline", cwd=casa).stdout
            self.assertIn("Salvataggio automatico", log)
            salvati = git("show", "--name-only", "--format=", "HEAD", cwd=casa).stdout
            self.assertIn("memory/nota.md", salvati)
            self.assertNotIn("token_drive.json", salvati)
            self.assertNotIn(".env", salvati)
            # niente da salvare: nessun secondo commit
            prima = git("rev-parse", "HEAD", cwd=casa).stdout
            self.run_hook(casa)
            self.assertEqual(prima, git("rev-parse", "HEAD", cwd=casa).stdout)

    def test_commits_even_without_git_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            casa = Path(tmp)
            git("init", "-q", "-b", "main", cwd=casa)
            (casa / "REGOLE.md").write_text("regole\n", encoding="utf-8")
            env = dict(os.environ, CLAUDE_PROJECT_DIR=str(casa), HOME=tmp,
                       GIT_CONFIG_GLOBAL=str(casa / "nessuna-config"),
                       GIT_CONFIG_NOSYSTEM="1")
            result = subprocess.run(["python3", str(HOOK)], input="{}", cwd=str(casa),
                                    env=env, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Salvataggio automatico", git("log", "--oneline", cwd=casa).stdout)

    def test_silent_outside_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "file.md").write_text("x", encoding="utf-8")
            result = self.run_hook(Path(tmp))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
