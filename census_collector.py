#!/usr/bin/env python3
"""Raccolta metadati deterministica per l'Agente Censitore (Passo 2).

Legge un perimetro approvato **in sola lettura** e produce un inventario
ripetibile: nessuna apertura di contenuti, nessuna scrittura, nessun invio.
Il modello non riceve mai questo modulo l'elenco file per file su perimetri
grandi: sopra la soglia del contratto la consegna passa ad aggregati per
cartella, tipo, periodo e gruppi di nomi, con campioni mirati.

Confine di prodotto: qui si raccolgono soltanto struttura e metadati. Chi
decide che cosa e' un processo, con quale certezza e con quali prove e'
`census_rule.py`. La skill `censitore-processi` guida l'agente e non duplica
nessuna delle due regole.

Solo standard library. Funziona uguale su Mac e Windows: i percorsi si
normalizzano in forma POSIX e l'ordine dell'uscita e' deterministico.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import census_rule
from census_rule import (
    PATH_ALLOWED,
    PATH_EXCLUDED,
    PATH_OUTSIDE,
    PATH_SENSITIVE,
    SCAN_MODE_AGGREGATES,
    ContractError,
    Perimeter,
    classify_path,
    plan_scan,
    sensitive_zone,
)


ROOT = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "install_contract.json"

# Ambienti tecnici: librerie, cache e strumenti installati. Non sono lavoro del
# proprietario e gonfierebbero l'inventario senza aggiungere un processo.
# Stessa famiglia gia' esclusa dall'Ispettore.
TECHNICAL_DIRS = frozenset(
    {
        ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
        ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".nox",
        "site-packages", "dist-packages", ".cache", "vendor", ".idea",
        ".vscode", ".gradle", "build", "dist", ".next", ".nuxt", "target",
    }
)

# Rumore di sistema: non e' un documento di lavoro.
NOISE_NAMES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini", ".localized"})

# Famiglie di tipo: il modello ragiona su queste, non sull'estensione grezza.
TYPE_FAMILIES: dict[str, frozenset[str]] = {
    "documento": frozenset({".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".pages"}),
    "foglio": frozenset({".xls", ".xlsx", ".ods", ".csv", ".numbers"}),
    "presentazione": frozenset({".ppt", ".pptx", ".odp", ".key"}),
    "pdf": frozenset({".pdf"}),
    "immagine": frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".tif", ".tiff", ".svg"}),
    "audio": frozenset({".mp3", ".wav", ".m4a", ".aac", ".flac"}),
    "video": frozenset({".mp4", ".mov", ".avi", ".mkv", ".webm"}),
    "archivio": frozenset({".zip", ".rar", ".7z", ".tar", ".gz"}),
    "email": frozenset({".eml", ".msg"}),
    "codice": frozenset({".py", ".js", ".ts", ".sh", ".html", ".css", ".json", ".yaml", ".yml"}),
}

# Marcatori di versione nel nome: attrito tipico dei processi a mano.
# `\b` non separa `rossi_v2`: l'underscore e' un word char. Si usano confini
# espliciti su lettere e cifre, cosi' `_v2`, `-def` e ` finale` valgono uguale.
_EDGE = r"(?<![a-zA-Z0-9])"
_EDGE_END = r"(?![a-zA-Z0-9])"
_VERSION_MARKERS = re.compile(
    _EDGE
    + r"(?:v\d+|versione\s*\d+|def(?:initiv[oa])?|finale?|rev\d*|bozza|copia|"
    + r"ultim[oa]|nuov[oa])"
    + _EDGE_END
    + r"|\(\d+\)|_\d+$",
    re.IGNORECASE,
)
# Date nel nome: 2026-08-10, 10-08-2026, 20260810.
_DATE_IN_NAME = re.compile(r"(?:\d{4}[-_.]?\d{2}[-_.]?\d{2}|\d{2}[-_.]\d{2}[-_.]\d{4})")
_SEPARATORS = re.compile(r"[\s_\-.,()\[\]]+")
_DIGITS = re.compile(r"\d+")


def _posix(path: Path) -> str:
    return path.as_posix()


def _iso_day(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")


def _iso_month(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m")


def type_family(suffix: str) -> str:
    """Famiglia del tipo, non l'estensione grezza."""

    normalized = suffix.casefold()
    for family, suffixes in TYPE_FAMILIES.items():
        if normalized in suffixes:
            return family
    return "altro"


def name_group(name: str) -> str:
    """Gruppo di nomi: il nome senza versioni, date e numeri.

    `Preventivo Rossi v2.docx`, `preventivo_rossi_def.docx` e
    `Preventivo Rossi (1).docx` finiscono nello stesso gruppo: sono tracce
    dello stesso lavoro, non tre lavori diversi."""

    stem = Path(name).stem
    stem = _DATE_IN_NAME.sub(" ", stem)
    stem = _VERSION_MARKERS.sub(" ", stem)
    stem = _DIGITS.sub(" ", stem)
    tokens = [token for token in _SEPARATORS.split(stem) if len(token) > 1]
    return census_rule._normalized(" ".join(tokens))


def work_group(name: str) -> str:
    """Radice del lavoro: il gruppo di nomi senza il soggetto.

    `Fattura 12 Rossi`, `fattura-13-bianchi` e `Fattura 14 Verdi` sono tre
    episodi dello stesso lavoro, non tre lavori diversi. Il gruppo di nomi
    tiene insieme le versioni di un episodio; la radice tiene insieme gli
    episodi di un processo, ed e' su questa che si vede la ripetizione."""

    group = name_group(name)
    if not group:
        return ""
    return group.split(" ", 1)[0]


@dataclass(frozen=True)
class FileRecord:
    """Metadati di un file dentro il perimetro. Nessun contenuto."""

    path: str
    folder: str
    name_group: str
    work_group: str
    type_family: str
    suffix: str
    size_bytes: int
    modified_day: str
    modified_month: str


@dataclass(frozen=True)
class FolderAggregate:
    folder: str
    items: int
    total_bytes: int
    type_families: dict[str, int]
    months: dict[str, int]
    top_name_groups: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class NameGroupAggregate:
    name_group: str
    items: int
    folders: tuple[str, ...]
    type_families: tuple[str, ...]
    days: tuple[str, ...]
    version_variants: int
    sample_paths: tuple[str, ...]


@dataclass(frozen=True)
class WorkGroupAggregate:
    """Aggregato per radice del lavoro: e' qui che si vede la ripetizione."""

    work_group: str
    items: int
    distinct_name_groups: int
    folders: tuple[str, ...]
    type_families: tuple[str, ...]
    days: tuple[str, ...]
    months: tuple[str, ...]
    version_variants: int
    sample_paths: tuple[str, ...]


@dataclass
class Inventory:
    """Uscita della raccolta: aggregati sempre, elenco solo sotto soglia.

    `sensitive_zones` riporta le cartelle da chiedere al proprietario; i file
    che contengono non compaiono da nessuna parte. `excluded_hits` conta le
    esclusioni assolute incontrate senza mai nominarle."""

    roots: tuple[str, ...]
    mode: str
    items_scanned: int
    items_in_perimeter: int
    bytes_in_perimeter: int
    folders: tuple[FolderAggregate, ...]
    name_groups: tuple[NameGroupAggregate, ...]
    work_groups: tuple[WorkGroupAggregate, ...]
    type_families: dict[str, int]
    months: dict[str, int]
    sensitive_zones: tuple[str, ...]
    excluded_hits: int
    outside_hits: int
    technical_skipped: int
    unreadable: tuple[str, ...]
    duration_seconds: float
    within_duration: bool
    files: tuple[FileRecord, ...] = field(default_factory=tuple)
    truncated: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["folders"] = [asdict(item) for item in self.folders]
        data["name_groups"] = [asdict(item) for item in self.name_groups]
        data["work_groups"] = [asdict(item) for item in self.work_groups]
        data["files"] = [asdict(item) for item in self.files]
        return data


def _walk(
    root: Path,
    perimeter: Perimeter,
    *,
    contract_path: Path,
    max_items: int,
) -> tuple[list[FileRecord], dict[str, int], list[str], set[str]]:
    """Percorre una radice in sola lettura.

    Non apre file, non segue collegamenti simbolici (un link puo' uscire dal
    perimetro senza che il percorso lo mostri) e conta cio' che salta."""

    records: list[FileRecord] = []
    counters = {"scanned": 0, "excluded": 0, "outside": 0, "technical": 0}
    unreadable: list[str] = []
    zones: set[str] = set()

    for current, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for dirname in sorted(dirnames):
            if dirname in TECHNICAL_DIRS:
                counters["technical"] += 1
                continue
            child = _posix(current_path / dirname)
            path_class = classify_path(child, perimeter, contract_path=contract_path)
            if path_class == PATH_EXCLUDED:
                counters["excluded"] += 1
                continue
            if path_class == PATH_OUTSIDE:
                counters["outside"] += 1
                continue
            if path_class == PATH_SENSITIVE:
                zone = sensitive_zone(child, is_dir=True, contract_path=contract_path)
                if zone:
                    zones.add(zone)
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs

        for filename in sorted(filenames):
            if filename in NOISE_NAMES:
                continue
            counters["scanned"] += 1
            file_path = current_path / filename
            posix_path = _posix(file_path)
            path_class = classify_path(posix_path, perimeter, contract_path=contract_path)
            if path_class == PATH_EXCLUDED:
                counters["excluded"] += 1
                continue
            if path_class == PATH_OUTSIDE:
                counters["outside"] += 1
                continue
            if path_class == PATH_SENSITIVE:
                zone = sensitive_zone(posix_path, contract_path=contract_path)
                if zone:
                    zones.add(zone)
                continue
            try:
                if file_path.is_symlink():
                    continue
                stat = file_path.stat()
            except OSError:
                unreadable.append(posix_path)
                continue
            records.append(
                FileRecord(
                    path=posix_path,
                    folder=_posix(current_path),
                    name_group=name_group(filename),
                    work_group=work_group(filename),
                    type_family=type_family(file_path.suffix),
                    suffix=file_path.suffix.casefold(),
                    size_bytes=stat.st_size,
                    modified_day=_iso_day(stat.st_mtime),
                    modified_month=_iso_month(stat.st_mtime),
                )
            )
            if len(records) >= max_items:
                return records, counters, unreadable, zones

    return records, counters, unreadable, zones


def _folder_aggregates(records: Sequence[FileRecord]) -> tuple[FolderAggregate, ...]:
    grouped: dict[str, list[FileRecord]] = defaultdict(list)
    for record in records:
        grouped[record.folder].append(record)
    aggregates = []
    for folder in sorted(grouped):
        items = grouped[folder]
        groups = Counter(item.name_group for item in items if item.name_group)
        aggregates.append(
            FolderAggregate(
                folder=folder,
                items=len(items),
                total_bytes=sum(item.size_bytes for item in items),
                type_families=dict(sorted(Counter(item.type_family for item in items).items())),
                months=dict(sorted(Counter(item.modified_month for item in items).items())),
                top_name_groups=tuple(sorted(groups.items(), key=lambda pair: (-pair[1], pair[0]))[:5]),
            )
        )
    return tuple(aggregates)


def _name_group_aggregates(
    records: Sequence[FileRecord], *, max_samples: int
) -> tuple[NameGroupAggregate, ...]:
    grouped: dict[str, list[FileRecord]] = defaultdict(list)
    for record in records:
        if record.name_group:
            grouped[record.name_group].append(record)
    aggregates = []
    for group in sorted(grouped):
        items = sorted(grouped[group], key=lambda item: (item.modified_day, item.path))
        variants = sum(1 for item in items if _VERSION_MARKERS.search(Path(item.path).stem))
        aggregates.append(
            NameGroupAggregate(
                name_group=group,
                items=len(items),
                folders=tuple(sorted({item.folder for item in items})),
                type_families=tuple(sorted({item.type_family for item in items})),
                days=tuple(sorted({item.modified_day for item in items})),
                version_variants=variants,
                sample_paths=tuple(item.path for item in items[:max_samples]),
            )
        )
    return tuple(
        sorted(aggregates, key=lambda item: (-item.items, item.name_group))
    )


def _work_group_aggregates(
    records: Sequence[FileRecord], *, max_samples: int
) -> tuple[WorkGroupAggregate, ...]:
    grouped: dict[str, list[FileRecord]] = defaultdict(list)
    for record in records:
        if record.work_group:
            grouped[record.work_group].append(record)
    aggregates = []
    for group in sorted(grouped):
        items = sorted(grouped[group], key=lambda item: (item.modified_day, item.path))
        variants = sum(1 for item in items if _VERSION_MARKERS.search(Path(item.path).stem))
        aggregates.append(
            WorkGroupAggregate(
                work_group=group,
                items=len(items),
                distinct_name_groups=len({item.name_group for item in items}),
                folders=tuple(sorted({item.folder for item in items})),
                type_families=tuple(sorted({item.type_family for item in items})),
                days=tuple(sorted({item.modified_day for item in items})),
                months=tuple(sorted({item.modified_month for item in items})),
                version_variants=variants,
                sample_paths=tuple(item.path for item in items[:max_samples]),
            )
        )
    return tuple(
        sorted(
            aggregates,
            key=lambda item: (-item.distinct_name_groups, -item.items, item.work_group),
        )
    )


def collect(
    perimeter: Perimeter | dict[str, Any],
    *,
    contract_path: Path = CONTRACT_PATH,
    max_items: int | None = None,
    now: float | None = None,
) -> Inventory:
    """Costruisce l'inventario del perimetro in sola lettura.

    Sopra la soglia del contratto l'elenco file per file non entra nell'uscita:
    restano aggregati e campioni. La durata viene misurata e confrontata con il
    limite dichiarato."""

    started = now if now is not None else datetime.now(tz=timezone.utc).timestamp()
    perimeter_obj = (
        perimeter if isinstance(perimeter, Perimeter) else Perimeter.from_dict(perimeter)
    )
    if not perimeter_obj.roots:
        raise ValueError("perimetro vuoto: dichiarare almeno una cartella autorizzata")

    policy = census_rule._load_policy(contract_path)
    scan = policy["scan_policy"]
    ceiling = max_items if max_items is not None else scan["volume_reference_items"] * 4

    records: list[FileRecord] = []
    counters = Counter()
    unreadable: list[str] = []
    zones: set[str] = set()
    truncated = False

    for raw_root in perimeter_obj.roots:
        root = Path(raw_root)
        if not root.is_dir():
            unreadable.append(_posix(root))
            continue
        found, root_counters, root_unreadable, root_zones = _walk(
            root,
            perimeter_obj,
            contract_path=contract_path,
            max_items=ceiling - len(records),
        )
        records.extend(found)
        counters.update(root_counters)
        unreadable.extend(root_unreadable)
        zones |= root_zones
        if len(records) >= ceiling:
            truncated = True
            break

    records.sort(key=lambda item: item.path)
    plan = plan_scan(len(records), contract_path=contract_path)
    ended = datetime.now(tz=timezone.utc).timestamp() if now is None else started
    duration = max(0.0, ended - started)
    within = duration <= scan["max_duration_minutes"] * 60

    return Inventory(
        roots=tuple(_posix(Path(item)) for item in perimeter_obj.roots),
        mode=plan.mode,
        items_scanned=counters["scanned"],
        items_in_perimeter=len(records),
        bytes_in_perimeter=sum(item.size_bytes for item in records),
        folders=_folder_aggregates(records),
        name_groups=_name_group_aggregates(
            records, max_samples=scan["max_sample_files_per_candidate"]
        ),
        work_groups=_work_group_aggregates(
            records, max_samples=scan["max_sample_files_per_candidate"]
        ),
        type_families=dict(sorted(Counter(item.type_family for item in records).items())),
        months=dict(sorted(Counter(item.modified_month for item in records).items())),
        sensitive_zones=tuple(sorted(zones)),
        excluded_hits=counters["excluded"],
        outside_hits=counters["outside"],
        technical_skipped=counters["technical"],
        unreadable=tuple(sorted(unreadable)),
        duration_seconds=round(duration, 3),
        within_duration=within,
        files=() if plan.mode == SCAN_MODE_AGGREGATES else tuple(records),
        truncated=truncated,
    )


def _cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Raccolta metadati in sola lettura per l'Agente Censitore. "
            "Nessun contenuto viene aperto, nessun file viene scritto."
        )
    )
    parser.add_argument(
        "roots", nargs="+", help="cartelle autorizzate dal proprietario"
    )
    parser.add_argument(
        "--escludi",
        action="append",
        default=[],
        help="cartella o file che il proprietario tiene fuori (ripetibile)",
    )
    parser.add_argument(
        "--fonte-consentita",
        action="append",
        default=[],
        dest="consented",
        help="fonte a consenso inclusa dal proprietario (email, calendario, cronologie)",
    )
    parser.add_argument("--json", action="store_true", help="uscita JSON completa")
    args = parser.parse_args(argv)

    perimeter = Perimeter(
        roots=tuple(args.roots),
        consented_sources=tuple(args.consented),
        extra_exclusions=tuple(args.escludi),
    )
    try:
        inventory = collect(perimeter)
    except (ContractError, ValueError) as exc:
        print(f"CENSIMENTO NON PARTITO: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(inventory.to_dict(), ensure_ascii=False, indent=2))
        return 0

    print(f"Perimetro: {', '.join(inventory.roots)}")
    print(f"Consegna al modello: {inventory.mode}")
    print(
        f"Elementi nel perimetro: {inventory.items_in_perimeter} "
        f"(letti {inventory.items_scanned})"
    )
    print(f"Tipi: {inventory.type_families}")
    print(f"Periodi: {inventory.months}")
    if inventory.sensitive_zones:
        print("Zone sensibili da chiedere al proprietario (non aperte):")
        for zone in inventory.sensitive_zones:
            print(f"  - {zone}")
    print(
        f"Esclusioni assolute incontrate: {inventory.excluded_hits}; "
        f"fuori perimetro: {inventory.outside_hits}; "
        f"ambienti tecnici saltati: {inventory.technical_skipped}"
    )
    print("Lavori piu' ricorrenti (radice):")
    for group in inventory.work_groups[:10]:
        print(
            f"  - {group.work_group}: {group.distinct_name_groups} episodi, "
            f"{group.items} elementi, {len(group.months)} mesi, "
            f"{group.version_variants} varianti di versione"
        )
    print("Gruppi di nomi piu' ricorrenti:")
    for group in inventory.name_groups[:10]:
        print(
            f"  - {group.name_group}: {group.items} elementi, "
            f"{len(group.folders)} cartelle, {len(group.days)} giorni, "
            f"{group.version_variants} varianti di versione"
        )
    print(
        f"Durata: {inventory.duration_seconds}s "
        f"({'entro' if inventory.within_duration else 'OLTRE'} il limite dichiarato)"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - ingresso da riga di comando
    raise SystemExit(_cli())
