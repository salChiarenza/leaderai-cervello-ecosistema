import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import install_contract  # noqa: E402
from census_rule import (  # noqa: E402
    PATH_ALLOWED,
    PATH_EXCLUDED,
    PATH_SENSITIVE,
    Perimeter,
    classify_path,
)


STUDIO = "Studio Legale"
MESTIERE = ("legale", "avvocat", "tribunale")


class CensusTradeTermsTest(unittest.TestCase):
    """Lezione del 16/09/2026 (Studio Mencarini, P-037).

    I tratti sensibili erano scritti una volta per tutti i mestieri e
    contenevano «legale», «avvocat», «tribunale»: in uno studio legale
    l'intero perimetro diventava zona sensibile e il censimento non partiva.
    Il tratto che descrive il mestiere del proprietario non distingue piu'
    niente: si dichiara prima di leggere e smette di marcare, dentro il
    perimetro che il proprietario ha gia' approvato. Tutto il resto resta.
    """

    def test_a_law_firm_can_be_censused_after_declaring_its_trade(self):
        perimetro = Perimeter(roots=(STUDIO,), trade_terms=MESTIERE)
        self.assertEqual(
            classify_path(f"{STUDIO}/Pratiche/Rossi/comparsa.pdf", perimetro),
            PATH_ALLOWED,
        )

    def test_without_the_declaration_nothing_changes(self):
        perimetro = Perimeter(roots=(STUDIO,))
        self.assertEqual(
            classify_path(f"{STUDIO}/Pratiche/Rossi/comparsa.pdf", perimetro),
            PATH_SENSITIVE,
        )

    def test_the_declaration_does_not_open_the_zones_outside_the_trade(self):
        perimetro = Perimeter(roots=(STUDIO,), trade_terms=MESTIERE)
        for percorso in (
            f"{STUDIO}/Personale/salute/referto.pdf",
            f"{STUDIO}/Pratiche/Rossi/separazione/accordo.pdf",
        ):
            with self.subTest(percorso=percorso):
                self.assertEqual(classify_path(percorso, perimetro), PATH_SENSITIVE)

    def test_absolute_exclusions_still_win(self):
        perimetro = Perimeter(roots=(STUDIO,), trade_terms=MESTIERE)
        self.assertEqual(
            classify_path(f"{STUDIO}/Pratiche/Rossi/iban.txt", perimetro),
            PATH_EXCLUDED,
        )

    def test_the_policy_tells_the_agent_to_ask_for_the_trade_first(self):
        policy = install_contract.load_contract()["inspection_policies"]["process_census"]
        self.assertIn("sensitive_zone_terms_del_mestiere", policy)
        testo = policy["sensitive_zone_terms_del_mestiere"]
        self.assertIn("prima di leggere", testo)
        self.assertIn("rapporto", testo)


if __name__ == "__main__":
    unittest.main()
