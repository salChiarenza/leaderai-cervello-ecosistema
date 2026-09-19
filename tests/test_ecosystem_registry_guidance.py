import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import install_contract  # noqa: E402


# `ecosistema/...` vero: non preceduto da lettere o trattino, cosi' i nomi
# lunghi (`ispettore-ecosistema/SKILL.md`, `leaderai-ecosistema/tools/...`)
# non vengono scambiati per la cartella dell'armadio comune.
ECOSYSTEM_PATH_RE = re.compile(r"(?<![\w-])ecosistema/([A-Za-z0-9_./-]+)")
IGNORED_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "tests"}


def _allowed_paths() -> set[str]:
    contract = install_contract.load_contract()
    return {
        rule.destination.split("/", 1)[1]
        for rule in install_contract.template_rules(contract, "both")
        if rule.destination.startswith("ecosistema/")
    }


def _documents() -> list[Path]:
    return [
        path
        for path in sorted(ROOT.rglob("*.md"))
        if not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts)
    ]


class EcosystemRegistryGuidanceTest(unittest.TestCase):
    """Lezione del 16/09/2026 (Studio Mencarini, P-035).

    La guida ordinava di creare `ecosistema/REGOLE.md`, ma nella cartella
    `ecosistema` l'Ispettore ammette soltanto i registri e i calchi dichiarati
    dal contratto: il file appena creato faceva scattare un BLOCCO
    (`ECOSYSTEM_REGISTRY_CONTAMINATED`). Il prodotto non deve mai ordinare
    quello che poi boccia.
    """

    def test_no_document_asks_for_a_file_the_inspector_blocks(self):
        allowed = _allowed_paths()
        self.assertTrue(allowed, "il contratto non dichiara nessun file di ecosistema/")
        for document in _documents():
            for match in ECOSYSTEM_PATH_RE.finditer(document.read_text(encoding="utf-8")):
                citato = match.group(1)
                if citato.rstrip("/") == "":
                    continue
                with self.subTest(documento=document.name, percorso=citato):
                    self.assertIn(
                        citato,
                        allowed,
                        f"{document.name} cita `ecosistema/{citato}`, che l'Ispettore "
                        f"segnala come BLOCCO: ammessi solo {sorted(allowed)}",
                    )

    def test_install_guide_puts_owner_rules_in_the_root(self):
        text = " ".join(
            (ROOT / "01 - Cervello - installazione e aggiornamento.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertIn("Crea `REGOLE.md` nella cartella madre", text)
        self.assertNotIn("ecosistema/REGOLE.md", text)


if __name__ == "__main__":
    unittest.main()
