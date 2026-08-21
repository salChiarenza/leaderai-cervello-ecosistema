import json
import unittest
from pathlib import Path

from adoption_rule import (
    REQUIRED_VERDICTS,
    VERDICT_OBSERVED,
    VERDICT_PARTIAL_ONE_STATION,
    VERDICT_TRACES_ABSENT,
    AdoptionOutcome,
    ContractError,
    classify_adoption,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "adoption"
CONTRACT_PATH = ROOT / "install_contract.json"


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
    def test_stesso_episodio_in_piu_sorgenti_conta_uno(self):
        data, outcome = _run_fixture("doppione.json")
        self.assertEqual(outcome.verdict, VERDICT_OBSERVED)
        self.assertEqual(outcome.verdict, data["expected"]["verdict"])
        self.assertEqual(outcome.unique_count, data["expected"]["unique_count"])
        self.assertEqual(
            outcome.duplicates_collapsed, data["expected"]["duplicates_collapsed"]
        )
        self.assertEqual(outcome.unique_gestures, ("Emissione fattura elettronica",))

    def test_stesso_gesto_in_due_episodi_distinti_conta_due(self):
        data, outcome = _run_fixture("stesso_gesto_due_episodi.json")
        self.assertEqual(outcome.verdict, VERDICT_OBSERVED)
        self.assertEqual(outcome.unique_count, 2)
        self.assertEqual(outcome.duplicates_collapsed, 0)

    def test_stesso_gesto_in_due_giorni_conta_due(self):
        data, outcome = _run_fixture("stesso_gesto_due_giorni.json")
        self.assertEqual(outcome.verdict, VERDICT_OBSERVED)
        self.assertEqual(outcome.unique_count, 2)
        self.assertEqual(outcome.duplicates_collapsed, 0)

    def test_sorgenti_sessioni_log_file_ammesse(self):
        data, outcome = _run_fixture("sorgenti_ammesse.json")
        self.assertEqual(outcome.verdict, VERDICT_OBSERVED)
        self.assertEqual(outcome.unique_count, 4)

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

    def test_verdetti_e_sorgenti_vivono_nel_contratto_macchina(self):
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        policy = contract["inspection_policies"]["adoption_observation"]
        self.assertEqual(set(policy["verdicts"]), set(REQUIRED_VERDICTS))
        # Il contratto copre tutte le tracce del Passo 1-quinquies.
        self.assertLessEqual(
            {"git", "chat", "diario", "sessioni", "file", "log", "memory"},
            set(policy["dedup_sources"]),
        )


class ContractSourceTest(unittest.TestCase):
    """Il contratto macchina e' la fonte obbligatoria: manca, malformato o
    incompleto -> errore visibile, mai default locali."""

    def test_contratto_mancante_fallisce(self):
        missing = ROOT / "tests" / "fixtures" / "adoption" / "non_esiste.json"
        with self.assertRaises(ContractError):
            classify_adoption(
                [{"gesture": "x", "source": "git"}],
                traces_read=True,
                contract_path=missing,
            )

    def test_contratto_json_malformato_fallisce(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "install_contract.json"
            bad.write_text("{ questo non e' json valido ", encoding="utf-8")
            with self.assertRaises(ContractError):
                classify_adoption(
                    [{"gesture": "x", "source": "git"}],
                    traces_read=True,
                    contract_path=bad,
                )

    def test_policy_incompleta_verdetti_mancanti_fallisce(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            partial = Path(tmp) / "install_contract.json"
            partial.write_text(
                json.dumps(
                    {
                        "inspection_policies": {
                            "adoption_observation": {
                                "verdicts": ["ADOZIONE OSSERVATA"],
                                "dedup_sources": ["git"],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ContractError):
                classify_adoption(
                    [{"gesture": "x", "source": "git"}],
                    traces_read=True,
                    contract_path=partial,
                )

    def test_policy_incompleta_sorgenti_mancanti_fallisce(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            partial = Path(tmp) / "install_contract.json"
            partial.write_text(
                json.dumps(
                    {
                        "inspection_policies": {
                            "adoption_observation": {
                                "verdicts": sorted(REQUIRED_VERDICTS),
                                "dedup_sources": [],
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ContractError):
                classify_adoption(
                    [{"gesture": "x", "source": "git"}],
                    traces_read=True,
                    contract_path=partial,
                )


if __name__ == "__main__":
    unittest.main()
