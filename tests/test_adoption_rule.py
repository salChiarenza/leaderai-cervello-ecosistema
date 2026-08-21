import json
import unittest
from pathlib import Path

from adoption_rule import (
    VERDICT_OBSERVED,
    VERDICT_PARTIAL_ONE_STATION,
    VERDICT_TRACES_ABSENT,
    AdoptionOutcome,
    classify_adoption,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "adoption"


def _run_fixture(name: str) -> tuple[dict, AdoptionOutcome]:
    data = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    outcome = classify_adoption(
        data["episodes"],
        traces_read=data["traces_read"],
        house_shared=data["house_shared"],
        machines_in_house=data["machines_in_house"],
    )
    return data, outcome


class AdoptionRuleTest(unittest.TestCase):
    def test_doppione_collassa_su_un_solo_gesto(self):
        data, outcome = _run_fixture("doppione.json")
        self.assertEqual(outcome.verdict, VERDICT_OBSERVED)
        self.assertEqual(outcome.verdict, data["expected"]["verdict"])
        self.assertEqual(outcome.unique_count, 1)
        self.assertEqual(outcome.duplicates_collapsed, 2)
        self.assertEqual(outcome.unique_gestures, ("Emissione fattura elettronica",))

    def test_tracce_assenti_non_giudica_l_uso(self):
        data, outcome = _run_fixture("tracce_assenti.json")
        self.assertEqual(outcome.verdict, VERDICT_TRACES_ABSENT)
        self.assertEqual(outcome.verdict, data["expected"]["verdict"])
        self.assertEqual(outcome.unique_count, 0)
        self.assertFalse(outcome.traces_read)

    def test_tracce_lette_ma_episodi_vuoti_restano_tracce_assenti(self):
        outcome = classify_adoption([], traces_read=True)
        self.assertEqual(outcome.verdict, VERDICT_TRACES_ABSENT)

    def test_copertura_parziale_una_sola_postazione(self):
        data, outcome = _run_fixture("copertura_parziale.json")
        self.assertEqual(outcome.verdict, VERDICT_PARTIAL_ONE_STATION)
        self.assertEqual(outcome.verdict, data["expected"]["verdict"])
        self.assertEqual(outcome.unique_count, 2)
        self.assertEqual(outcome.machines_observed, ("pc-ufficio",))

    def test_casa_condivisa_ma_tracce_da_due_postazioni_non_e_parziale(self):
        episodes = [
            {"gesture": "invio email", "source": "git", "machine": "pc-ufficio"},
            {"gesture": "analisi", "source": "diario", "machine": "portatile-casa"},
        ]
        outcome = classify_adoption(
            episodes,
            traces_read=True,
            house_shared=True,
            machines_in_house=["pc-ufficio", "portatile-casa"],
        )
        self.assertEqual(outcome.verdict, VERDICT_OBSERVED)

    def test_traccia_non_ammessa_e_un_errore(self):
        with self.assertRaises(ValueError):
            classify_adoption(
                [{"gesture": "x", "source": "email"}],
                traces_read=True,
            )

    def test_verdetti_vivono_nel_contratto_macchina(self):
        contract = json.loads(
            (ROOT / "install_contract.json").read_text(encoding="utf-8")
        )
        policy = contract["inspection_policies"]["adoption_observation"]
        self.assertEqual(
            set(policy["verdicts"]),
            {
                VERDICT_TRACES_ABSENT,
                VERDICT_PARTIAL_ONE_STATION,
                VERDICT_OBSERVED,
            },
        )
        self.assertEqual(set(policy["dedup_sources"]), {"git", "chat", "diario"})


if __name__ == "__main__":
    unittest.main()
