"""Collaudi 1-6 del piano Censitore sulla raccolta metadati deterministica.

Le prove seguono i cancelli della fase 2 in `docs/ecosistema_cantiere.md`:
casa sintetica disordinata, prova errore, prova privacy, prova anti-azione,
volume realistico, parita' agenti.
"""

import importlib.util
import os
import shutil
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import census_collector
import census_rule
from census_collector import (
    Inventory,
    collect,
    name_group,
    type_family,
    work_group,
)
from census_rule import (
    SCAN_MODE_AGGREGATES,
    SCAN_MODE_LIST,
    Perimeter,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "census" / "casa_disordinata.py"

_spec = importlib.util.spec_from_file_location("casa_disordinata", FIXTURE_PATH)
casa_disordinata = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(casa_disordinata)


class DisorderedHouseCollectionTest(unittest.TestCase):
    """Collaudo 1: casa finta senza registri, disordinata di proposito."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="censitore-"))
        cls.home = casa_disordinata.build(cls.tmp)
        cls.perimeter = Perimeter(roots=casa_disordinata.perimeter_roots(cls.home))
        cls.inventory = collect(cls.perimeter)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_secret_files_are_never_collected_or_named(self):
        text = repr(self.inventory.to_dict())
        for forbidden in ("secrets", "password", "api_key", "gestionale.env"):
            self.assertNotIn(forbidden, text.casefold())
        self.assertGreaterEqual(self.inventory.excluded_hits, 3)

    def test_personal_zone_is_flagged_as_folder_not_opened(self):
        zones = self.inventory.sensitive_zones
        self.assertTrue(any(zone.endswith("Personale") for zone in zones))
        text = repr(self.inventory.to_dict()).casefold()
        self.assertNotIn("referto", text)
        self.assertNotIn("cedolino", text)

    def test_outside_perimeter_folder_is_not_collected(self):
        paths = [record.path for record in self.inventory.files]
        self.assertFalse(any("/Documenti/" in path for path in paths))

    def test_system_noise_and_technical_envs_are_skipped(self):
        paths = [record.path for record in self.inventory.files]
        self.assertFalse(any(path.endswith(".DS_Store") for path in paths))
        self.assertFalse(any("node_modules" in path for path in paths))
        self.assertFalse(any("__pycache__" in path for path in paths))
        self.assertGreaterEqual(self.inventory.technical_skipped, 2)

    def test_two_buried_processes_surface_as_top_work_groups(self):
        """I due processi sepolti devono emergere per radice del lavoro.

        Per gruppo di nomi le fatture si spezzano per cliente (una a testa) e
        non sembrano ricorrenti: la ripetizione si vede solo sulla radice."""

        top = [group.work_group for group in self.inventory.work_groups[:2]]
        self.assertEqual(sorted(top), ["fattura", "preventivo"])
        radici = {group.work_group: group for group in self.inventory.work_groups}
        self.assertEqual(radici["fattura"].distinct_name_groups, 3)
        self.assertEqual(radici["preventivo"].distinct_name_groups, 3)
        self.assertGreaterEqual(len(radici["fattura"].months), 2)

    def test_name_group_alone_would_hide_the_repetition(self):
        groups = {group.name_group: group for group in self.inventory.name_groups}
        for key in ("fattura rossi", "fattura bianchi", "fattura verdi"):
            self.assertEqual(groups[key].items, 1)

    def test_same_work_in_many_versions_collapses_into_one_group(self):
        groups = {group.name_group: group for group in self.inventory.name_groups}
        rossi = groups.get("preventivo rossi")
        self.assertIsNotNone(rossi)
        # tre file (base, v2, def) = un solo gruppo con varianti di versione
        self.assertEqual(rossi.items, 3)
        self.assertGreaterEqual(rossi.version_variants, 2)

    def test_duplicate_download_does_not_double_the_work(self):
        groups = {group.name_group: group for group in self.inventory.name_groups}
        bianchi = groups.get("preventivo bianchi")
        self.assertIsNotNone(bianchi)
        self.assertEqual(bianchi.items, 2)
        self.assertEqual(len(bianchi.days), 1)

    def test_homonyms_in_different_folders_stay_distinguishable(self):
        groups = {group.name_group: group for group in self.inventory.name_groups}
        note = groups.get("note")
        self.assertIsNotNone(note)
        self.assertEqual(len(note.folders), 2)

    def test_noise_stays_a_small_isolated_group(self):
        groups = {group.name_group: group for group in self.inventory.name_groups}
        for noisy in ("img", "manuale stampante", "setup app"):
            group = groups.get(noisy)
            if group is not None:
                self.assertEqual(group.items, 1)

    def test_aggregates_cover_the_four_contract_axes(self):
        self.assertTrue(self.inventory.folders)
        self.assertTrue(self.inventory.name_groups)
        self.assertTrue(self.inventory.type_families)
        self.assertTrue(self.inventory.months)
        folder = self.inventory.folders[0]
        self.assertTrue(folder.type_families)
        self.assertTrue(folder.months)

    def test_small_house_is_delivered_as_a_list(self):
        self.assertEqual(self.inventory.mode, SCAN_MODE_LIST)
        self.assertTrue(self.inventory.files)


class NoActionTest(unittest.TestCase):
    """Collaudo 4: durante il censimento niente viene modificato."""

    def test_collection_leaves_the_house_untouched(self):
        tmp = Path(tempfile.mkdtemp(prefix="censitore-anti-azione-"))
        try:
            home = casa_disordinata.build(tmp)
            perimeter = Perimeter(roots=casa_disordinata.perimeter_roots(home))

            def snapshot():
                state = {}
                for path in sorted(home.rglob("*")):
                    if path.is_file():
                        stat = path.stat()
                        state[path.as_posix()] = (
                            stat.st_size,
                            round(stat.st_mtime, 3),
                            path.read_bytes(),
                        )
                return state

            before = snapshot()
            collect(perimeter)
            after = snapshot()
            self.assertEqual(before, after)
            self.assertEqual(sorted(before), sorted(after))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_symlink_out_of_perimeter_is_not_followed(self):
        tmp = Path(tempfile.mkdtemp(prefix="censitore-link-"))
        try:
            home = casa_disordinata.build(tmp)
            outside = tmp / "fuori"
            outside.mkdir()
            (outside / "riservato.txt").write_text("dato fuori perimetro", encoding="utf-8")
            link = home / "Scrivania" / "collegamento"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("collegamenti simbolici non disponibili")
            inventory = collect(Perimeter(roots=casa_disordinata.perimeter_roots(home)))
            paths = [record.path for record in inventory.files]
            self.assertFalse(any("riservato" in path for path in paths))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class PrivacyPerimeterTest(unittest.TestCase):
    """Collaudo 3: perimetro con esclusioni scelte dal proprietario."""

    def test_owner_exclusion_inside_the_perimeter_is_respected(self):
        tmp = Path(tempfile.mkdtemp(prefix="censitore-privacy-"))
        try:
            home = casa_disordinata.build(tmp)
            excluded = (home / "Scrivania").as_posix()
            perimeter = Perimeter(
                roots=casa_disordinata.perimeter_roots(home),
                extra_exclusions=(excluded,),
            )
            inventory = collect(perimeter)
            paths = [record.path for record in inventory.files]
            self.assertTrue(paths)
            self.assertFalse(any("/Scrivania/" in path for path in paths))
            self.assertTrue(all("/Scaricati/" in path for path in paths))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_empty_perimeter_refuses_to_start(self):
        with self.assertRaises(ValueError):
            collect(Perimeter(roots=()))

    def test_missing_root_is_reported_not_guessed(self):
        tmp = Path(tempfile.mkdtemp(prefix="censitore-mancante-"))
        try:
            inventory = collect(Perimeter(roots=((Path(tmp) / "assente").as_posix(),)))
            self.assertEqual(inventory.items_in_perimeter, 0)
            self.assertTrue(inventory.unreadable)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class VolumeTest(unittest.TestCase):
    """Collaudo 5: volume realistico consegnato per aggregati, non file per file."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="censitore-volume-"))
        home = cls.tmp / "grande"
        policy = census_rule._load_policy()
        cls.threshold = policy["scan_policy"]["aggregate_threshold_items"]
        total = cls.threshold + 500
        stamp = datetime(2026, 6, 1, tzinfo=timezone.utc).timestamp()
        for index in range(total):
            folder = home / f"cartella-{index % 20:02d}"
            folder.mkdir(parents=True, exist_ok=True)
            target = folder / f"documento cliente {index}.pdf"
            target.write_text("x", encoding="utf-8")
            os.utime(target, (stamp, stamp))
        cls.home = home
        started = time.monotonic()
        cls.inventory = collect(Perimeter(roots=(home.as_posix(),)))
        cls.elapsed = time.monotonic() - started

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_large_inventory_is_delivered_as_aggregates_only(self):
        self.assertGreater(self.inventory.items_in_perimeter, self.threshold)
        self.assertEqual(self.inventory.mode, SCAN_MODE_AGGREGATES)
        self.assertEqual(self.inventory.files, ())
        self.assertTrue(self.inventory.folders)
        self.assertTrue(self.inventory.name_groups)

    def test_samples_stay_within_the_contract_limit(self):
        policy = census_rule._load_policy()
        limit = policy["scan_policy"]["max_sample_files_per_candidate"]
        for group in self.inventory.name_groups:
            self.assertLessEqual(len(group.sample_paths), limit)

    def test_declared_duration_is_respected(self):
        self.assertTrue(self.inventory.within_duration)
        policy = census_rule._load_policy()
        self.assertLess(self.elapsed, policy["scan_policy"]["max_duration_minutes"] * 60)


class DeterminismTest(unittest.TestCase):
    """Collaudo 6: stessa casa, stesso inventario. Base della parita' agenti."""

    def test_two_runs_on_the_same_house_are_identical(self):
        tmp = Path(tempfile.mkdtemp(prefix="censitore-parita-"))
        try:
            home = casa_disordinata.build(tmp)
            perimeter = Perimeter(roots=casa_disordinata.perimeter_roots(home))
            first = collect(perimeter)
            second = collect(perimeter)
            self.assertEqual(first.folders, second.folders)
            self.assertEqual(first.name_groups, second.name_groups)
            self.assertEqual(first.files, second.files)
            self.assertEqual(first.type_families, second.type_families)
            self.assertEqual(first.sensitive_zones, second.sensitive_zones)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_two_identical_houses_in_different_places_agree(self):
        first_tmp = Path(tempfile.mkdtemp(prefix="censitore-casa-a-"))
        second_tmp = Path(tempfile.mkdtemp(prefix="censitore-casa-b-"))
        try:
            first_home = casa_disordinata.build(first_tmp)
            second_home = casa_disordinata.build(second_tmp)
            first = collect(Perimeter(roots=casa_disordinata.perimeter_roots(first_home)))
            second = collect(Perimeter(roots=casa_disordinata.perimeter_roots(second_home)))
            self.assertEqual(
                [group.name_group for group in first.name_groups],
                [group.name_group for group in second.name_groups],
            )
            self.assertEqual(
                [group.items for group in first.name_groups],
                [group.items for group in second.name_groups],
            )
            self.assertEqual(first.type_families, second.type_families)
            self.assertEqual(first.months, second.months)
            self.assertEqual(first.items_in_perimeter, second.items_in_perimeter)
        finally:
            shutil.rmtree(first_tmp, ignore_errors=True)
            shutil.rmtree(second_tmp, ignore_errors=True)


class NormalizationTest(unittest.TestCase):
    def test_name_group_collapses_versions_dates_and_numbers(self):
        self.assertEqual(name_group("Preventivo Rossi.docx"), "preventivo rossi")
        self.assertEqual(name_group("preventivo_rossi_v2.docx"), "preventivo rossi")
        self.assertEqual(name_group("Preventivo Rossi def.docx"), "preventivo rossi")
        self.assertEqual(name_group("Preventivo Rossi (1).docx"), "preventivo rossi")
        self.assertEqual(name_group("Fattura 12 Rossi.pdf"), "fattura rossi")
        self.assertEqual(name_group("verbale 2026-08-10.md"), "verbale")

    def test_work_group_keeps_the_verb_and_drops_the_subject(self):
        self.assertEqual(work_group("Fattura 12 Rossi.pdf"), "fattura")
        self.assertEqual(work_group("fattura-13-bianchi.pdf"), "fattura")
        self.assertEqual(work_group("Preventivo Rossi v2.docx"), "preventivo")
        self.assertNotEqual(work_group("Fattura Rossi.pdf"), work_group("Preventivo Rossi.docx"))

    def test_version_markers_after_underscore_are_seen(self):
        import census_collector as cc

        for name in ("preventivo_rossi_v2", "preventivo-rossi-def", "Preventivo Rossi finale"):
            with self.subTest(name=name):
                self.assertIsNotNone(cc._VERSION_MARKERS.search(name))

    def test_different_works_do_not_collapse(self):
        self.assertNotEqual(name_group("Preventivo Rossi.docx"), name_group("Fattura Rossi.pdf"))
        self.assertNotEqual(name_group("contratto.pdf"), name_group("preventivo.pdf"))

    def test_type_family_groups_by_meaning(self):
        self.assertEqual(type_family(".docx"), "documento")
        self.assertEqual(type_family(".xlsx"), "foglio")
        self.assertEqual(type_family(".pdf"), "pdf")
        self.assertEqual(type_family(".jpg"), "immagine")
        self.assertEqual(type_family(".xyz"), "altro")


class WindowsParityTest(unittest.TestCase):
    """La raccolta deve dare lo stesso inventario su Mac e Windows.

    Qui si prova la parte deterministica indipendente dal sistema: normalizzazione
    dei percorsi, gruppi di nomi e famiglie di tipo."""

    def test_backslash_paths_normalize_like_posix(self):
        self.assertEqual(
            census_rule._norm_path("C:\\Utenti\\demo\\Lavoro\\"),
            "C:/Utenti/demo/Lavoro",
        )
        self.assertEqual(name_group("Preventivo Rossi v2.docx"), name_group("preventivo rossi.docx"))

    def test_case_differences_do_not_split_a_group(self):
        self.assertEqual(name_group("FATTURA Rossi.pdf"), name_group("fattura rossi.pdf"))


if __name__ == "__main__":
    unittest.main()
