import json
import tempfile
import unittest
from pathlib import Path

import ecosistema_inspector
import install_contract
from census_rule import (
    CERTAINTY_DEDUCIBLE,
    CERTAINTY_OBSERVED,
    CERTAINTY_TO_CONFIRM,
    PATH_ALLOWED,
    PATH_EXCLUDED,
    PATH_OUTSIDE,
    PATH_SENSITIVE,
    SCAN_MODE_AGGREGATES,
    SCAN_MODE_LIST,
    Candidate,
    CertaintyAmbiguity,
    ContractError,
    Evidence,
    Perimeter,
    PerimeterViolation,
    Trace,
    classify_certainty,
    classify_path,
    dedupe_candidates,
    dedupe_traces,
    plan_scan,
    prioritize,
    priority_key,
    render_row,
    report_is_clean,
    run_census,
    sensitive_zone,
    validate_evidence,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "census"
CONTRACT_PATH = ROOT / "install_contract.json"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class ContractIsTheSingleSourceTest(unittest.TestCase):
    """Il contratto macchina e' l'unica fonte; l'accessor e la regola falliscono
    in modo visibile se manca o e' incoerente."""

    def setUp(self):
        self.contract = install_contract.load_contract()
        self.policy = install_contract.process_census_policy(self.contract)
        self.raw = self.contract["inspection_policies"]["process_census"]

    def test_policy_declares_phase_two_read_only_and_three_levels(self):
        self.assertEqual(self.policy.agent_name, "Agente Censitore")
        self.assertEqual(self.policy.skill_name, "censitore-processi")
        self.assertEqual(self.policy.phase_served, 2)
        self.assertEqual(self.policy.next_phase, 3)
        self.assertTrue(self.policy.read_only)
        self.assertEqual(
            self.policy.certainty_levels,
            (CERTAINTY_OBSERVED, CERTAINTY_DEDUCIBLE, CERTAINTY_TO_CONFIRM),
        )
        self.assertEqual(self.policy.trigger_commands, ("censisci i miei processi",))
        self.assertEqual(
            set(self.policy.path_classes),
            {PATH_ALLOWED, PATH_OUTSIDE, PATH_EXCLUDED, PATH_SENSITIVE},
        )

    def test_no_ambiguity_between_observed_and_deduced_in_the_rules(self):
        rules = self.raw["certainty_rules"]
        self.assertIn("nessun anello dedotto", rules[CERTAINTY_OBSERVED])
        self.assertIn("dedotto", rules[CERTAINTY_DEDUCIBLE])
        self.assertIn("nessuna prova diretta", rules[CERTAINTY_TO_CONFIRM])

    def test_table_has_the_ten_columns_of_the_plan(self):
        self.assertEqual(
            self.policy.table_columns,
            (
                "processo candidato",
                "innesco",
                "sequenza",
                "fonti/strumenti",
                "output",
                "frequenza osservata",
                "attrito",
                "prova",
                "certezza",
                "stato",
            ),
        )
        self.assertEqual(len(self.policy.card_fields), 7)

    def test_sources_and_registries_reuse_what_exists(self):
        self.assertEqual(
            self.policy.allowed_sources,
            ("albero", "metadati", "documenti", "email", "calendario", "cronologie", "registri"),
        )
        self.assertEqual(
            self.policy.consent_required_sources, ("email", "calendario", "cronologie")
        )
        for registry in self.policy.output_registries:
            self.assertIn(registry, self.contract["common"]["required"])
        self.assertEqual(self.policy.room_status_after_census, "DA DECIDERE IN CALL")
        self.assertIn("nuova stanza", self.policy.forbidden_actions)
        self.assertIn("automazione", self.policy.forbidden_actions)

    def test_priority_uses_only_the_four_criteria_and_no_economics(self):
        self.assertEqual(
            self.policy.priority_criteria,
            ("ripetizione", "attrito", "chiarezza dell'output", "rischio"),
        )
        self.assertEqual(
            set(self.raw["priority_forbidden_estimates"]),
            {"ore", "costi", "ritorni economici"},
        )
        key = priority_key(Candidate(name="x"))
        self.assertEqual(len(key), 5)

    def test_exclusions_cover_the_inspector_credential_terms(self):
        excluded = {term.casefold() for term in self.policy.always_excluded_terms}
        for term in ecosistema_inspector.CREDENTIAL_NAME_TERMS:
            self.assertIn(term.casefold(), excluded)
        self.assertIn(".secrets", self.policy.always_excluded_dirs)

    def test_volume_thresholds_are_ordered(self):
        self.assertLess(
            self.policy.aggregate_threshold_items, self.policy.volume_reference_items
        )
        self.assertEqual(
            self.policy.aggregation_axes, ("cartella", "tipo", "periodo", "gruppo di nomi")
        )

    def test_episode_identity_matches_adoption_rule(self):
        adoption = self.contract["inspection_policies"]["adoption_observation"]
        self.assertIn("episode esplicito", adoption["episode_identity"])
        self.assertIn("episode esplicito", self.raw["episode_identity"])

    def _broken_contract(self, mutate) -> Path:
        data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        mutate(data)
        tmp = Path(tempfile.mkdtemp()) / "install_contract.json"
        tmp.write_text(json.dumps(data), encoding="utf-8")
        return tmp

    def test_missing_policy_fails_visibly_in_rule_and_loader(self):
        def drop(data):
            del data["inspection_policies"]["process_census"]

        broken = self._broken_contract(drop)
        with self.assertRaises(ContractError):
            plan_scan(10, contract_path=broken)
        with self.assertRaises(ValueError):
            install_contract.load_contract(broken)

    def test_missing_level_fails_visibly(self):
        def drop_level(data):
            data["inspection_policies"]["process_census"]["certainty_levels"] = [
                CERTAINTY_OBSERVED,
                CERTAINTY_TO_CONFIRM,
            ]

        broken = self._broken_contract(drop_level)
        with self.assertRaises(ContractError):
            classify_path("/x", Perimeter(roots=("/x",)), contract_path=broken)

    def test_read_only_false_fails_visibly(self):
        def flip(data):
            data["inspection_policies"]["process_census"]["read_only"] = False

        broken = self._broken_contract(flip)
        with self.assertRaises(ContractError):
            report_is_clean("ok", contract_path=broken)
        with self.assertRaises(ValueError):
            install_contract.load_contract(broken)


class PathClassificationTest(unittest.TestCase):
    def setUp(self):
        self.data = _fixture("perimetro_esclusioni.json")
        self.perimeter = Perimeter.from_dict(self.data["perimeter"])

    def test_windows_and_posix_paths_classify_the_same(self):
        for path, expected in self.data["paths"].items():
            with self.subTest(path=path):
                self.assertEqual(classify_path(path, self.perimeter), expected)
                posix = path.replace("\\", "/")
                self.assertEqual(classify_path(posix, self.perimeter), expected)

    def test_exclusions_win_even_inside_the_perimeter(self):
        self.assertEqual(
            classify_path(
                "C:/Utenti/demo/Lavoro/Clienti/.ssh/id_rsa", self.perimeter
            ),
            PATH_EXCLUDED,
        )
        self.assertEqual(
            classify_path("/Users/demo/Desktop/.secrets/x.env", Perimeter(roots=("/",))),
            PATH_EXCLUDED,
        )

    def test_sensitive_zone_reports_the_folder_never_the_file(self):
        for path, zone in self.data["sensitive_zone_of"].items():
            with self.subTest(path=path):
                self.assertEqual(sensitive_zone(path), zone)
                self.assertNotIn("cedolino", sensitive_zone(path).casefold())
                self.assertNotIn("causa.pdf", sensitive_zone(path))
        self.assertEqual(sensitive_zone("/Users/demo/Lavoro/ordine.xlsx"), "")

    def test_evidence_on_excluded_or_outside_path_is_refused(self):
        for path in (
            "C:/Utenti/demo/Lavoro/Contabilita riservata/bilancio.xlsx",
            "C:/Utenti/demo/Lavoro/Clienti/token_api.json",
            "C:/Utenti/demo/Lavoro/Legale/causa.pdf",
            "C:/Utenti/demo/Desktop/nota.txt",
        ):
            with self.subTest(path=path), self.assertRaises(PerimeterViolation):
                validate_evidence(Evidence(path=path, source="albero"), self.perimeter)
        validate_evidence(
            Evidence(path="C:/Utenti/demo/Lavoro/Clienti/ordine.xlsx", source="albero"),
            self.perimeter,
        )

    def test_consent_sources_need_owner_inclusion(self):
        email = Evidence(path="", source="email", date="2026-08-01", note="oggetto: ordine")
        with self.assertRaises(PerimeterViolation):
            validate_evidence(email, self.perimeter)
        validate_evidence(email, Perimeter.from_dict(self.data["perimeter_with_email"]))
        with self.assertRaises(PerimeterViolation):
            validate_evidence(Evidence(path="/x", source="whatsapp"), self.perimeter)


class CertaintyTest(unittest.TestCase):
    perimeter = Perimeter(roots=("/casa",))

    def test_direct_evidence_on_every_step_is_observed(self):
        candidate = Candidate(
            name="Fattura",
            sequence=("chiusura", "emissione"),
            evidence=(
                Evidence(path="/casa/a.pdf", source="albero", step="chiusura"),
                Evidence(path="/casa/b.pdf", source="albero", step="emissione"),
            ),
        )
        outcome = classify_certainty(candidate, self.perimeter)
        self.assertEqual(outcome.level, CERTAINTY_OBSERVED)
        self.assertEqual(outcome.uncovered_steps, ())

    def test_inferred_link_downgrades_to_deducible(self):
        candidate = Candidate(
            name="Preventivo",
            sequence=("richiesta", "bozza"),
            evidence=(Evidence(path="/casa/p.docx", source="albero", step="bozza"),),
            inferred_links=("la richiesta arriva via email",),
        )
        outcome = classify_certainty(candidate, self.perimeter)
        self.assertEqual(outcome.level, CERTAINTY_DEDUCIBLE)
        self.assertEqual(outcome.uncovered_steps, ("richiesta",))

    def test_uncovered_step_alone_is_deducible_not_observed(self):
        candidate = Candidate(
            name="Preventivo",
            sequence=("richiesta", "bozza"),
            evidence=(Evidence(path="/casa/p.docx", source="albero", step="bozza"),),
        )
        self.assertEqual(
            classify_certainty(candidate, self.perimeter).level, CERTAINTY_DEDUCIBLE
        )

    def test_only_indirect_evidence_is_to_confirm(self):
        candidate = Candidate(
            name="Rumore",
            evidence=(Evidence(path="/casa/x.jpg", source="albero", direct=False),),
        )
        self.assertEqual(
            classify_certainty(candidate, self.perimeter).level, CERTAINTY_TO_CONFIRM
        )
        self.assertEqual(
            classify_certainty(Candidate(name="Vuoto"), self.perimeter).level,
            CERTAINTY_TO_CONFIRM,
        )

    def test_declared_certainty_must_match_computed(self):
        plausible = Candidate(
            name="Plausibile",
            sequence=("a", "b"),
            evidence=(Evidence(path="/casa/a.md", source="albero", step="a"),),
            inferred_links=("b segue a",),
            declared_certainty=CERTAINTY_OBSERVED,
        )
        with self.assertRaises(CertaintyAmbiguity):
            classify_certainty(plausible, self.perimeter)
        downgraded = Candidate(
            name="Provato",
            evidence=(Evidence(path="/casa/a.md", source="albero"),),
            declared_certainty=CERTAINTY_DEDUCIBLE,
        )
        with self.assertRaises(CertaintyAmbiguity):
            classify_certainty(downgraded, self.perimeter)
        agreed = Candidate(
            name="Provato",
            evidence=(Evidence(path="/casa/a.md", source="albero"),),
            declared_certainty=CERTAINTY_OBSERVED,
        )
        self.assertEqual(classify_certainty(agreed, self.perimeter).level, CERTAINTY_OBSERVED)

    def test_evidence_outside_perimeter_never_counts(self):
        candidate = Candidate(
            name="Fuori",
            evidence=(Evidence(path="/altrove/a.md", source="albero"),),
        )
        with self.assertRaises(PerimeterViolation):
            classify_certainty(candidate, self.perimeter)


class EpisodeDedupTest(unittest.TestCase):
    def test_same_episode_two_traces_counts_one(self):
        keys, collapsed = dedupe_traces(
            [
                Trace(subject="Rossi", date="2026-07-10", source="albero"),
                Trace(subject="rossi ", date="2026-07-10", source="metadati"),
                Trace(subject="Bianchi", date="2026-08-02", source="albero"),
            ]
        )
        self.assertEqual(len(keys), 2)
        self.assertEqual(collapsed, 1)

    def test_same_subject_two_episodes_counts_two(self):
        keys, collapsed = dedupe_traces(
            [
                Trace(episode="prev-rossi-1", subject="Rossi", date="2026-07-10"),
                Trace(episode="prev-rossi-2", subject="Rossi", date="2026-07-10"),
            ]
        )
        self.assertEqual(len(keys), 2)
        self.assertEqual(collapsed, 0)

    def test_two_candidates_on_the_same_episodes_are_one_process(self):
        traces = (Trace(subject="Rossi", date="2026-07-10"), Trace(subject="Bianchi", date="2026-08-02"))
        kept, merged = dedupe_candidates(
            [
                Candidate(name="Preventivo al cliente", traces=traces),
                Candidate(name="Preventivo cliente", traces=traces),
                Candidate(name="Fattura", traces=(Trace(subject="Rossi", date="2026-07-20"),)),
            ]
        )
        self.assertEqual([item.name for item in kept], ["Preventivo al cliente", "Fattura"])
        self.assertEqual(merged, [("Preventivo al cliente", "Preventivo cliente")])

    def test_shared_subject_with_different_episodes_stays_two_processes(self):
        kept, merged = dedupe_candidates(
            [
                Candidate(name="Preventivo", traces=(Trace(subject="Rossi", date="2026-07-10"),)),
                Candidate(name="Fattura", traces=(Trace(subject="Rossi", date="2026-07-20"),)),
            ]
        )
        self.assertEqual(len(kept), 2)
        self.assertEqual(merged, [])


class VolumeAndReportTest(unittest.TestCase):
    def test_small_inventory_is_listed_large_inventory_is_aggregated(self):
        small = plan_scan(500)
        self.assertEqual(small.mode, SCAN_MODE_LIST)
        large = plan_scan(50_000)
        self.assertEqual(large.mode, SCAN_MODE_AGGREGATES)
        self.assertEqual(large.aggregation_axes, ("cartella", "tipo", "periodo", "gruppo di nomi"))
        self.assertGreaterEqual(large.volume_reference_items, 50_000)
        self.assertLessEqual(large.max_sample_files_per_candidate, 10)

    def test_duration_limit_is_declared_and_checked(self):
        inside = plan_scan(10, elapsed_minutes=5)
        self.assertTrue(inside.within_duration)
        outside = plan_scan(10, elapsed_minutes=inside.max_duration_minutes + 1)
        self.assertFalse(outside.within_duration)
        with self.assertRaises(ValueError):
            plan_scan(-1)

    def test_report_with_secrets_is_not_clean(self):
        dirty = "prova: /casa/.secrets/x.env password=abc IBAN IT60X0542811101000000123456"
        clean, findings = report_is_clean(dirty)
        self.assertFalse(clean)
        self.assertIn("pattern IBAN", findings)
        self.assertTrue(any("termine escluso" in item for item in findings))
        self.assertFalse(report_is_clean("chiave sk-live_abcdefghijklmnopqrstuvwxyz0123")[0])
        self.assertTrue(report_is_clean("| Preventivo | richiesta | bozza -> invio |")[0])

    def test_row_follows_contract_columns_and_points_without_content(self):
        candidate = Candidate(
            name="Fattura",
            trigger="lavoro concluso",
            sequence=("chiusura", "emissione"),
            sources=("Desktop",),
            output="fattura PDF",
            frequency="2 episodi",
            evidence=(Evidence(path="/casa/Fattura 12.pdf", source="albero", date="2026-07-20"),),
        )
        outcome = classify_certainty(candidate, Perimeter(roots=("/casa",)))
        row = render_row(candidate, outcome)
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        self.assertEqual(len(cells), 10)
        self.assertEqual(cells[0], "Fattura")
        self.assertEqual(cells[7], "/casa/Fattura 12.pdf (2026-07-20)")
        self.assertEqual(cells[8], CERTAINTY_OBSERVED)
        self.assertEqual(cells[9], "in attesa")


class DisorderedHouseTest(unittest.TestCase):
    """Collaudo 1 del piano su dati gia' raccolti: due processi, deduplica,
    rumore scartato, segreto mai aperto, zona sensibile solo segnalata."""

    def setUp(self):
        self.data = _fixture("casa_disordinata.json")
        self.perimeter = Perimeter.from_dict(self.data["perimeter"])

    def run_fixture(self):
        return run_census(
            self.data["candidates"],
            self.perimeter,
            observed_paths=self.data["observed_paths"],
        )

    def test_paths_are_classified_as_expected(self):
        for path, expected in self.data["expected"]["path_classes"].items():
            with self.subTest(path=path):
                self.assertEqual(classify_path(path, self.perimeter), expected)

    def test_two_processes_dedup_noise_and_levels(self):
        outcome = self.run_fixture()
        names = [item.name for item in outcome.candidates]
        self.assertEqual(sorted(names), sorted(self.data["expected"]["kept"]))
        self.assertEqual(
            [list(pair) for pair in outcome.merged], self.data["expected"]["merged"]
        )
        levels = dict(zip(names, outcome.levels))
        self.assertEqual(levels, self.data["expected"]["levels"])
        self.assertEqual(outcome.certain_count, 1)
        self.assertEqual(names[0], self.data["expected"]["priority_first"])

    def test_secret_never_cited_and_sensitive_zone_only_flagged(self):
        outcome = self.run_fixture()
        report = "\n".join(outcome.rows)
        self.assertNotIn(".secrets", report)
        self.assertNotIn("password", report.casefold())
        self.assertNotIn("referto", report.casefold())
        self.assertTrue(report_is_clean(report)[0])
        self.assertEqual(
            list(outcome.sensitive_zones), self.data["expected"]["sensitive_zones"]
        )

    def test_same_input_gives_same_output_for_both_agents(self):
        first = self.run_fixture()
        second = self.run_fixture()
        self.assertEqual(first, second)
        self.assertEqual(
            [item.name for item in prioritize(first.candidates)],
            [item.name for item in first.candidates],
        )


class InsufficientTracesTest(unittest.TestCase):
    def test_nothing_is_declared_certain(self):
        data = _fixture("tracce_insufficienti.json")
        outcome = run_census(data["candidates"], data["perimeter"])
        self.assertEqual(list(outcome.levels), data["expected"]["levels"])
        self.assertEqual(outcome.certain_count, data["expected"]["certain_count"])

    def test_unread_traces_keep_everything_to_confirm(self):
        data = _fixture("casa_disordinata.json")
        outcome = run_census(
            data["candidates"], data["perimeter"], traces_read=False
        )
        self.assertTrue(all(level == CERTAINTY_TO_CONFIRM for level in outcome.levels))
        self.assertEqual(outcome.certain_count, 0)
        self.assertIn("DA CONFERMARE", outcome.note)

    def test_empty_census_has_no_candidates(self):
        outcome = run_census([], {"roots": ["/casa"]})
        self.assertEqual(outcome.candidates, ())
        self.assertIn("nessun candidato", outcome.note)


if __name__ == "__main__":
    unittest.main()
