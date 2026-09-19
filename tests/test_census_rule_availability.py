import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import install_contract  # noqa: E402


PY_RE = re.compile(r"[A-Za-z0-9_./-]+\.py")
# L'unica chiave che puo' nominare un attrezzo che il cliente non riceve:
# dice per iscritto che e' roba di LeaderAI, non un programma da cercare.
LEADERAI_TOOL_KEY = "leaderai_reference_implementation"


def _installed_files(contract: dict) -> set[str]:
    nomi: set[str] = set()
    for rule in install_contract.template_rules(contract, "both"):
        for percorso in (rule.destination, rule.template):
            if percorso:
                nomi.add(percorso)
                nomi.add(Path(percorso).name)
    return nomi


def _walk(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _walk(value, f"{path}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


class CensusRuleAvailabilityTest(unittest.TestCase):
    """Lezione del 16/09/2026 (Studio Mencarini, P-036).

    Il contratto diceva che il censimento dei processi «e' applicato da
    `census_rule.py`», ma dalla 0.7.1 il pacchetto del cliente e' solo
    documentale (`.md` e `.json`): quel programma non arriva e non arrivera'
    mai. L'assistente dello Studio l'ha cercato, non l'ha trovato e ha dovuto
    applicare la politica a mano. La politica scritta nel contratto **e'** la
    regola: i documenti del cliente non devono mandarlo a caccia di un file.
    """

    def setUp(self):
        self.contract = install_contract.load_contract()
        self.installati = _installed_files(self.contract)

    def test_policies_never_send_the_client_looking_for_a_program(self):
        for path, value in _walk(self.contract.get("inspection_policies", {}), "inspection_policies"):
            for citato in PY_RE.findall(value):
                if path.rsplit("/", 1)[-1] == LEADERAI_TOOL_KEY:
                    continue
                if citato in self.installati or Path(citato).name in self.installati:
                    continue
                self.fail(
                    f"{path} nomina `{citato}`, che il pacchetto del cliente non "
                    f"contiene: spostalo sotto `{LEADERAI_TOOL_KEY}` o installalo"
                )

    def test_policies_say_the_agent_applies_them_by_reading_the_contract(self):
        for nome in ("process_census", "adoption_observation"):
            policy = self.contract["inspection_policies"][nome]
            with self.subTest(policy=nome):
                self.assertIn("applicazione", policy)
                self.assertIn("leggendo questa politica", policy["applicazione"])

    def test_client_documents_do_not_present_the_tool_as_the_rule(self):
        for nome in ("MANIFEST.md", "CHECKUP.md"):
            testo = " ".join((ROOT / nome).read_text(encoding="utf-8").split())
            with self.subTest(documento=nome):
                self.assertNotIn("applicato da `census_rule.py`", testo)
                self.assertNotIn("La regola deterministica e' `adoption_rule.py", testo)


if __name__ == "__main__":
    unittest.main()
