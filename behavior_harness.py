#!/usr/bin/env python3
"""Collaudo comportamentale live del Cervello LeaderAI.

Il modulo usa soltanto la standard library. I test unitari possono passare un
eseguibile finto; una sessione con un modello reale parte esclusivamente dal
sottocomando esplicito ``live``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "behavior" / "anonymous_house"
GENERIC_ROOT_DIRS = frozenset(
    {
        "documenti",
        "docs",
        "export",
        "exports",
        "misc",
        "output",
        "outputs",
        "varie",
    }
)

HARNESS_INSTRUCTION = """\
Sei entrato in una nuova sessione nella cartella madre operativa di un cliente
anonimo. Orientati leggendo la mappa madre e le mappe locali. Usa soltanto i
fatti presenti nella casa, considera gli archivi come materiale storico e non
modificare alcuna fonte. Crea solo l'output richiesto, nella stanza che ne e'
proprietaria. Non usare internet e non chiedere indicazioni tecniche al
cliente. Al termine comunica in modo conciso cosa hai prodotto.
"""


@dataclass(frozen=True)
class Scenario:
    """Contratto osservabile di una missione business."""

    name: str
    business_prompt: str
    owner_dir: str
    expected_output: str
    canonical_source: str
    required_markers: tuple[str, ...]
    historical_markers: tuple[str, ...]
    foreign_markers: tuple[str, ...]
    include_harness_instruction: bool = True

    @property
    def prompt(self) -> str:
        if not self.include_harness_instruction:
            return self.business_prompt.strip() + "\n"
        return (
            f"{HARNESS_INSTRUCTION.rstrip()}\n\n"
            f"Missione business:\n{self.business_prompt.strip()}\n"
        )


SCENARIOS: dict[str, Scenario] = {
    "relazioni_scheda": Scenario(
        name="relazioni_scheda",
        business_prompt=(
            "Cliente Aurora incontrera' il responsabile. Prepara una scheda "
            "operativa aggiornata per il prossimo incontro usando i fatti "
            "correnti della relazione. Deve essere pronta all'uso, chiara e "
            "breve."
        ),
        owner_dir="relazioni",
        expected_output="relazioni/output/scheda-operativa.md",
        canonical_source="relazioni/fonti/cliente-aurora.md",
        required_markers=(
            "REL-2026-017",
            "Laboratorio operativo di 45 minuti",
            "03/08/2026",
        ),
        historical_markers=(
            "Corso registrato introduttivo",
            "prospecting",
        ),
        foreign_markers=(
            "ORD-042",
            "Giulia R.",
            "07/08/2026",
        ),
    ),
    "operazioni_consegna": Scenario(
        name="operazioni_consegna",
        business_prompt=(
            "La consegna ORD-042 va preparata per il coordinamento del mattino. "
            "Produci il piano di consegna aggiornato usando lo stato corrente "
            "della casa, con responsabile, scadenza, blocco e prossima azione."
        ),
        owner_dir="operazioni",
        expected_output="operazioni/output/piano-consegna.md",
        canonical_source="operazioni/fonti/ordine-042.md",
        required_markers=(
            "ORD-042",
            "Giulia R.",
            "07/08/2026",
            "approvazione legale della clausola privacy",
        ),
        historical_markers=(
            "Marco T.",
            "01/08/2026",
            "Nessun blocco",
        ),
        foreign_markers=(
            "REL-2026-017",
            "Cliente Aurora",
            "Laboratorio operativo di 45 minuti",
        ),
    ),
    "brand_identity": Scenario(
        name="brand_identity",
        business_prompt="Crea la Brand Identity",
        owner_dir="identita",
        expected_output="identita/output/brand-identity.md",
        canonical_source="identita/fonti/brand-verificato.md",
        required_markers=(
            "AVORIO-37",
            "Accoglienza sartoriale senza pressione",
            "Noce caldo",
            "Champagne opaco",
        ),
        historical_markers=(
            "Lusso irraggiungibile",
            "ORO-99",
        ),
        foreign_markers=(
            "REL-2026-017",
            "ORD-042",
        ),
        include_harness_instruction=False,
    ),
}


@dataclass
class ProcessOutcome:
    state: str
    return_code: int | None
    stdout: str
    stderr: str
    duration_seconds: float
    executable: str
    error: str | None = None


@dataclass
class ScenarioResult:
    scenario: str
    agent: str
    status: str
    return_code: int | None
    timed_out: bool
    executable_found: bool
    oracle_passed: bool
    evidence_dir: str
    target_dir: str
    duration_seconds: float
    error: str | None = None


@dataclass(frozen=True)
class InstructionVariant:
    """Una sola variazione controllata del contesto di progetto."""

    block_id: str
    instruction_path: str
    current_text: str
    lighter_text: str
    candidate_action: str
    protected: bool = False
    supporting_cases: int = 1


@dataclass
class ContextMetrics:
    run_status: str
    outcome_observed: bool
    correct_sources: bool
    correct_routing: bool
    completed: bool
    human_correction_requests: int
    duration_seconds: float
    input_tokens: int | None
    output_tokens: int | None
    safety_preserved: bool


@dataclass
class ContextComparisonResult:
    block_id: str
    scenario: str
    agent: str
    classification: str
    full: ContextMetrics
    lighter: ContextMetrics
    evidence_dir: str
    reason: str


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    """Descrive file, link e directory senza leggere contenuti nelle evidenze."""

    files: dict[str, dict[str, Any]] = {}
    directories: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            files[relative] = {
                "kind": "symlink",
                "target": os.readlink(path),
            }
        elif path.is_dir():
            directories.append(relative)
        elif path.is_file():
            files[relative] = {
                "kind": "file",
                "sha256": _sha256(path),
                "size": path.stat().st_size,
            }
    return {"root": "$TARGET", "directories": directories, "files": files}


def diff_manifests(
    before: dict[str, Any], after: dict[str, Any]
) -> dict[str, list[str]]:
    before_files = before["files"]
    after_files = after["files"]
    before_paths = set(before_files)
    after_paths = set(after_files)
    shared_paths = before_paths & after_paths
    before_dirs = set(before["directories"])
    after_dirs = set(after["directories"])
    return {
        "added_files": sorted(after_paths - before_paths),
        "removed_files": sorted(before_paths - after_paths),
        "modified_files": sorted(
            path
            for path in shared_paths
            if before_files[path] != after_files[path]
        ),
        "added_directories": sorted(after_dirs - before_dirs),
        "removed_directories": sorted(before_dirs - after_dirs),
    }


def _check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "detail": detail}


def evaluate_oracle(
    target: Path,
    scenario: Scenario,
    before: dict[str, Any],
    after: dict[str, Any],
    changes: dict[str, list[str]],
) -> dict[str, Any]:
    """Valuta soltanto effetti osservabili sul filesystem."""

    expected = target / scenario.expected_output
    output_exists = expected.is_file()
    output_text = expected.read_text(encoding="utf-8") if output_exists else ""
    folded = output_text.casefold()
    required_missing = [
        marker
        for marker in scenario.required_markers
        if marker.casefold() not in folded
    ]
    historical_present = [
        marker
        for marker in scenario.historical_markers
        if marker.casefold() in folded
    ]
    foreign_present = [
        marker
        for marker in scenario.foreign_markers
        if marker.casefold() in folded
    ]

    expected_path = Path(scenario.expected_output)
    owner_path = Path(scenario.owner_dir)
    owner_is_correct = (
        expected_path != owner_path
        and owner_path in expected_path.parents
        and expected_path.parent.name == "output"
    )

    allowed_files = {scenario.expected_output}
    unexpected_files = sorted(set(changes["added_files"]) - allowed_files)

    allowed_directories = {
        parent.as_posix()
        for parent in expected_path.parents
        if parent != Path(".") and owner_path in (parent, *parent.parents)
    }
    unexpected_directories = sorted(
        set(changes["added_directories"]) - allowed_directories
    )

    generic_root_present = sorted(
        name
        for name in GENERIC_ROOT_DIRS
        if (target / name).exists()
    )
    initial_sources_unchanged = not (
        changes["modified_files"]
        or changes["removed_files"]
        or changes["removed_directories"]
    )
    canonical_recorded = scenario.canonical_source in before["files"]

    checks = [
        _check(
            "output_nel_percorso_proprietario",
            output_exists and owner_is_correct,
            scenario.expected_output,
        ),
        _check(
            "contenuto_derivato_dalla_fonte_canonica",
            canonical_recorded and not required_missing and not foreign_present,
            (
                f"fonte={scenario.canonical_source}; "
                f"marker_mancanti={required_missing}; "
                f"marker_di_altre_stanze={foreign_present}"
            ),
        ),
        _check(
            "doppione_storico_non_usato",
            not historical_present,
            f"marker_storici_presenti={historical_present}",
        ),
        _check(
            "nessun_output_in_root_o_cartelle_generiche",
            not generic_root_present
            and not unexpected_files
            and not unexpected_directories,
            (
                f"root_generiche={generic_root_present}; "
                f"file_inattesi={unexpected_files}; "
                f"directory_inattese={unexpected_directories}"
            ),
        ),
        _check(
            "fonti_standard_inalterate",
            initial_sources_unchanged,
            (
                f"modificati={changes['modified_files']}; "
                f"rimossi={changes['removed_files']}; "
                f"directory_rimosse={changes['removed_directories']}"
            ),
        ),
    ]
    return {
        "scenario": scenario.name,
        "passed": all(item["passed"] for item in checks),
        "checks": checks,
    }


def _resolve_executable(executable: str) -> str | None:
    candidate = Path(executable).expanduser()
    if candidate.parent != Path("."):
        return str(candidate.resolve()) if candidate.is_file() else None
    return shutil.which(executable)


def _executable_prefix(executable: str) -> list[str]:
    """Avvia i finti agenti Python in modo portabile anche su Windows."""

    if Path(executable).suffix.casefold() == ".py":
        return [sys.executable, executable]
    return [executable]


def build_command(
    agent: str,
    executable: str,
    target: Path,
    transcript_format: str,
) -> list[str]:
    """Costruisce una sessione nuova senza riprese o directory aggiuntive."""

    prefix = _executable_prefix(executable)
    if agent == "codex":
        return [
            *prefix,
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--cd",
            str(target),
            "--json",
            "-",
        ]
    if agent == "claude":
        output_format = "stream-json" if transcript_format == "jsonl" else "json"
        command = [
            *prefix,
            "--print",
            "--no-session-persistence",
            "--no-chrome",
            "--disable-slash-commands",
            "--setting-sources",
            "project",
            "--strict-mcp-config",
            "--mcp-config",
            '{"mcpServers":{}}',
            "--tools",
            "Read,Write,Edit,Glob,Grep",
            "--permission-mode",
            "acceptEdits",
            "--output-format",
            output_format,
        ]
        if output_format == "stream-json":
            command.append("--verbose")
        return command
    raise ValueError(f"Agente non supportato: {agent}")


def redact_command(command: Sequence[str], target: Path) -> list[str]:
    """Rimuove percorsi macchina e non include mai prompt o ambiente."""

    redacted: list[str] = []
    target_text = str(target)
    for index, item in enumerate(command):
        if index == 0:
            redacted.append(Path(item).name)
        else:
            redacted.append(item.replace(target_text, "$TARGET"))
    redacted.append("<PROMPT via stdin>")
    return redacted


def _text_from_timeout(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def execute_agent(
    command: Sequence[str],
    target: Path,
    prompt: str,
    timeout_seconds: float,
) -> ProcessOutcome:
    started = _utc_now()
    try:
        completed = subprocess.run(
            list(command),
            cwd=target,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except FileNotFoundError as exc:
        duration = (_utc_now() - started).total_seconds()
        return ProcessOutcome(
            state="EXECUTABLE_MISSING",
            return_code=None,
            stdout="",
            stderr="",
            duration_seconds=duration,
            executable=Path(command[0]).name,
            error=str(exc),
        )
    except subprocess.TimeoutExpired as exc:
        duration = (_utc_now() - started).total_seconds()
        return ProcessOutcome(
            state="TIMEOUT",
            return_code=None,
            stdout=_text_from_timeout(exc.stdout),
            stderr=_text_from_timeout(exc.stderr),
            duration_seconds=duration,
            executable=Path(command[0]).name,
            error=f"Timeout dopo {timeout_seconds:g} secondi",
        )

    duration = (_utc_now() - started).total_seconds()
    output = f"{completed.stdout}\n{completed.stderr}".casefold()
    auth_markers = (
        "authentication_failed",
        "authentication required",
        "not logged in",
        "please log in",
        "unauthorized",
        "login required",
    )
    if completed.returncode == 0:
        state = "COMPLETED"
    elif any(marker in output for marker in auth_markers):
        state = "AUTH_FAILURE"
    else:
        state = "RETURN_CODE_ERROR"
    return ProcessOutcome(
        state=state,
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        duration_seconds=duration,
        executable=Path(command[0]).name,
        error=None if completed.returncode == 0 else "Processo terminato con errore",
    )


def _parse_json_lines(stdout: str) -> list[Any]:
    records: list[Any] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append({"type": "unparsed", "raw": line})
    if not records:
        records.append({"type": "empty"})
    return records


def write_transcript(
    evidence_dir: Path, stdout: str, transcript_format: str
) -> Path:
    """Salva sempre un transcript sintatticamente valido."""

    if transcript_format == "jsonl":
        records = _parse_json_lines(stdout)
        path = evidence_dir / "transcript.jsonl"
        path.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                for record in records
            ),
            encoding="utf-8",
        )
        return path

    path = evidence_dir / "transcript.json"
    try:
        payload: Any = json.loads(stdout) if stdout.strip() else {"type": "empty"}
    except json.JSONDecodeError:
        records = _parse_json_lines(stdout)
        payload = records[0] if len(records) == 1 else records
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _oracle_checks(evidence_dir: Path) -> dict[str, bool]:
    oracle = json.loads((evidence_dir / "oracle.json").read_text(encoding="utf-8"))
    return {item["name"]: bool(item["passed"]) for item in oracle["checks"]}


def _usage_from_transcript(raw: str) -> tuple[int | None, int | None]:
    """Legge i contatori quando l'agente li espone; altrimenti restituisce N/D."""

    values: dict[str, list[int]] = {"input": [], "output": []}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                folded = key.casefold()
                if isinstance(item, int) and folded in {
                    "input_tokens",
                    "input_token_count",
                }:
                    values["input"].append(item)
                elif isinstance(item, int) and folded in {
                    "output_tokens",
                    "output_token_count",
                }:
                    values["output"].append(item)
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    for record in _parse_json_lines(raw):
        visit(record)
    return (
        max(values["input"]) if values["input"] else None,
        max(values["output"]) if values["output"] else None,
    )


def _human_correction_requests(raw: str) -> int:
    folded = raw.casefold()
    markers = (
        "mi serve",
        "fornisci",
        "dimmi",
        "puoi indicare",
        "devi indicare",
        "ho bisogno che",
        "chiedo conferma",
    )
    return sum(folded.count(marker) for marker in markers) + folded.count("?")


def _context_metrics(evidence_dir: Path, result: ScenarioResult) -> ContextMetrics:
    checks = _oracle_checks(evidence_dir)
    raw = (evidence_dir / "stdout.raw").read_text(encoding="utf-8")
    input_tokens, output_tokens = _usage_from_transcript(raw)
    return ContextMetrics(
        run_status=result.status,
        outcome_observed=result.oracle_passed,
        correct_sources=(
            checks.get("contenuto_derivato_dalla_fonte_canonica", False)
            and checks.get("doppione_storico_non_usato", False)
        ),
        correct_routing=(
            checks.get("output_nel_percorso_proprietario", False)
            and checks.get("nessun_output_in_root_o_cartelle_generiche", False)
        ),
        completed=(evidence_dir / "observed-output.md").is_file(),
        human_correction_requests=_human_correction_requests(raw),
        duration_seconds=result.duration_seconds,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        safety_preserved=checks.get("fonti_standard_inalterate", False),
    )


CLASSIFICATIONS = {
    "keep": "MANTIENI",
    "compact": "ACCORPA",
    "move": "SPOSTA NELLA PROCEDURA/SKILL GIUSTA",
    "rewrite": "RISCRIVI",
    "remove": "CANDIDATA ALLA RIMOZIONE",
}


def classify_instruction_variant(
    variant: InstructionVariant,
    full: ContextMetrics,
    lighter: ContextMetrics,
) -> tuple[str, str]:
    """Classifica senza trasformare l'esperimento in una cancellazione."""

    invalid_statuses = {
        "EXECUTABLE_MISSING",
        "AUTH_FAILURE",
        "TIMEOUT",
        "RETURN_CODE_ERROR",
    }
    if full.run_status != "PASS":
        return (
            "DA COLLAUDARE",
            "Il contesto attuale non ha prodotto una base valida.",
        )
    if lighter.run_status in invalid_statuses:
        return (
            "DA COLLAUDARE",
            "La sessione alleggerita ha avuto un errore tecnico e non misura l'istruzione.",
        )

    full_core = (
        full.outcome_observed,
        full.correct_sources,
        full.correct_routing,
        full.completed,
        full.safety_preserved,
    )
    lighter_core = (
        lighter.outcome_observed,
        lighter.correct_sources,
        lighter.correct_routing,
        lighter.completed,
        lighter.safety_preserved,
    )
    if variant.protected and variant.candidate_action == "remove":
        return (
            "MANTIENI",
            "Blocco protetto: sicurezza, privacy, autorizzazione e integrita non si eliminano automaticamente.",
        )
    if variant.candidate_action == "remove" and variant.supporting_cases < 2:
        return (
            "MANTIENI",
            "Un solo caso non basta: ripetere su almeno un secondo compito prima di candidare la rimozione.",
        )
    if any(before and not after for before, after in zip(full_core, lighter_core)):
        return (
            "MANTIENI",
            "Il contesto alleggerito peggiora almeno un esito osservabile.",
        )
    if lighter.human_correction_requests > full.human_correction_requests:
        return "MANTIENI", "Il contesto alleggerito richiede piu correzioni o dati umani."
    if not lighter.outcome_observed:
        return "MANTIENI", "La variante alleggerita non completa correttamente la missione."
    classification = CLASSIFICATIONS[variant.candidate_action]
    return classification, "La variante alleggerita mantiene gli esiti senza regressioni osservate."


def _safe_instruction_path(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("Il file istruzioni deve essere relativo alla fixture")
    unresolved = root / candidate
    if unresolved.is_symlink():
        raise ValueError(f"Il file istruzioni non puo essere un symlink: {relative}")
    resolved = unresolved.resolve()
    if root.resolve() not in resolved.parents:
        raise ValueError("Il file istruzioni esce dalla fixture")
    if not resolved.is_file():
        raise ValueError(f"File istruzioni non valido: {relative}")
    return resolved


def run_context_comparison(
    *,
    scenario: Scenario,
    variant: InstructionVariant,
    agent: str,
    executable: str,
    fixture: Path,
    evidence_dir: Path,
    timeout_seconds: float,
    transcript_format: str,
) -> ContextComparisonResult:
    """Confronta due sessioni pulite variando un solo blocco di istruzioni."""

    if variant.candidate_action not in CLASSIFICATIONS:
        raise ValueError(f"Azione candidata non supportata: {variant.candidate_action}")
    if variant.supporting_cases < 1:
        raise ValueError("I casi di supporto devono essere almeno uno")
    evidence_dir.mkdir(parents=True, exist_ok=False)
    evaluation_scenario = replace(scenario, include_harness_instruction=False)
    with tempfile.TemporaryDirectory(prefix="leaderai-context-audit-") as tmp:
        root = Path(tmp)
        lighter_fixture = root / "fixture-lighter"
        shutil.copytree(fixture, lighter_fixture)
        instruction_file = _safe_instruction_path(
            lighter_fixture,
            variant.instruction_path,
        )
        current = instruction_file.read_text(encoding="utf-8")
        occurrences = current.count(variant.current_text)
        if occurrences != 1:
            raise ValueError(
                f"Il blocco {variant.block_id} deve comparire una sola volta; trovato {occurrences}"
            )
        instruction_file.write_text(
            current.replace(variant.current_text, variant.lighter_text, 1),
            encoding="utf-8",
        )
        full_result = run_scenario(
            scenario=evaluation_scenario,
            agent=agent,
            executable=executable,
            fixture=fixture,
            evidence_dir=evidence_dir / "full",
            timeout_seconds=timeout_seconds,
            transcript_format=transcript_format,
            target_dir=root / "target-full",
        )
        lighter_result = run_scenario(
            scenario=evaluation_scenario,
            agent=agent,
            executable=executable,
            fixture=lighter_fixture,
            evidence_dir=evidence_dir / "lighter",
            timeout_seconds=timeout_seconds,
            transcript_format=transcript_format,
            target_dir=root / "target-lighter",
        )
    full_metrics = _context_metrics(evidence_dir / "full", full_result)
    lighter_metrics = _context_metrics(evidence_dir / "lighter", lighter_result)
    classification, reason = classify_instruction_variant(
        variant,
        full_metrics,
        lighter_metrics,
    )
    comparison = ContextComparisonResult(
        block_id=variant.block_id,
        scenario=scenario.name,
        agent=agent,
        classification=classification,
        full=full_metrics,
        lighter=lighter_metrics,
        evidence_dir=str(evidence_dir.resolve()),
        reason=reason,
    )
    _write_json(evidence_dir / "comparison.json", asdict(comparison))
    return comparison


def _validate_fixture(fixture: Path) -> None:
    if not fixture.is_dir():
        raise FileNotFoundError(f"Fixture non trovata: {fixture}")
    for relative in ("AGENTS.md", "CLAUDE.md"):
        if not (fixture / relative).is_file():
            raise ValueError(f"Fixture incompleta: manca {relative}")


def _ensure_separate_paths(target: Path, evidence: Path) -> None:
    resolved_target = target.resolve()
    resolved_evidence = evidence.resolve()
    if (
        resolved_evidence == resolved_target
        or resolved_evidence in resolved_target.parents
        or resolved_target in resolved_evidence.parents
    ):
        raise ValueError("Target ed evidenze devono vivere in directory separate")


def run_scenario(
    *,
    scenario: Scenario,
    agent: str,
    executable: str,
    fixture: Path,
    evidence_dir: Path,
    timeout_seconds: float,
    transcript_format: str,
    target_dir: Path | None = None,
) -> ScenarioResult:
    """Esegue una missione su una copia nuova e salva prove indipendenti."""

    _validate_fixture(fixture)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    temporary_root: tempfile.TemporaryDirectory[str] | None = None
    if target_dir is None:
        temporary_root = tempfile.TemporaryDirectory(
            prefix=f"leaderai-behavior-{scenario.name}-"
        )
        target = Path(temporary_root.name) / "anonymous-house"
    else:
        target = target_dir
    _ensure_separate_paths(target, evidence_dir)
    if target.exists():
        raise FileExistsError(f"Il target di prova esiste gia': {target}")

    try:
        shutil.copytree(fixture, target)
        before = build_manifest(target)
        _write_json(evidence_dir / "manifest-pre.json", before)
        (evidence_dir / "prompt.txt").write_text(scenario.prompt, encoding="utf-8")

        resolved_executable = _resolve_executable(executable)
        command_executable = resolved_executable or executable
        command = build_command(
            agent,
            command_executable,
            target,
            transcript_format,
        )
        _write_json(
            evidence_dir / "command.json",
            {
                "agent": agent,
                "argv": redact_command(command, target),
                "cwd": "$TARGET",
                "prompt_transport": "stdin",
                "environment_recorded": False,
                "workspace_scope": "$TARGET only; no additional directories",
            },
        )

        outcome = execute_agent(
            command,
            target,
            scenario.prompt,
            timeout_seconds,
        )
        (evidence_dir / "stdout.raw").write_text(
            outcome.stdout, encoding="utf-8"
        )
        (evidence_dir / "stderr.txt").write_text(
            outcome.stderr, encoding="utf-8"
        )
        write_transcript(evidence_dir, outcome.stdout, transcript_format)

        after = build_manifest(target)
        changes = diff_manifests(before, after)
        oracle = evaluate_oracle(target, scenario, before, after, changes)
        _write_json(evidence_dir / "manifest-post.json", after)
        _write_json(evidence_dir / "diff.json", changes)
        _write_json(evidence_dir / "oracle.json", oracle)

        expected_output = target / scenario.expected_output
        if expected_output.is_file():
            shutil.copyfile(expected_output, evidence_dir / "observed-output.md")

        if outcome.state != "COMPLETED":
            status = outcome.state
        elif oracle["passed"]:
            status = "PASS"
        else:
            status = "ORACLE_FAIL"

        result = ScenarioResult(
            scenario=scenario.name,
            agent=agent,
            status=status,
            return_code=outcome.return_code,
            timed_out=outcome.state == "TIMEOUT",
            executable_found=outcome.state != "EXECUTABLE_MISSING",
            oracle_passed=bool(oracle["passed"]),
            evidence_dir=str(evidence_dir.resolve()),
            target_dir="$TEMPORARY_TARGET" if temporary_root else str(target.resolve()),
            duration_seconds=outcome.duration_seconds,
            error=outcome.error,
        )
        _write_json(evidence_dir / "result.json", asdict(result))
        return result
    finally:
        if temporary_root is not None:
            temporary_root.cleanup()


def _scenario_selection(values: Iterable[str]) -> list[Scenario]:
    names = list(values)
    if not names or "all" in names:
        return list(SCENARIOS.values())
    unique_names = list(dict.fromkeys(names))
    return [SCENARIOS[name] for name in unique_names]


def run_harness(
    *,
    agent: str,
    scenario_names: Iterable[str],
    executable: str | None,
    fixture: Path,
    evidence_base: Path | None,
    timeout_seconds: float,
    transcript_format: str,
) -> tuple[Path, list[ScenarioResult]]:
    """Esegue uno o piu' scenari e restituisce la cartella prove."""

    run_id = f"{_utc_now().strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    if evidence_base is None:
        evidence_root = Path(
            tempfile.mkdtemp(prefix="leaderai-behavior-evidence-")
        )
    else:
        evidence_root = evidence_base.expanduser().resolve() / run_id
        evidence_root.mkdir(parents=True, exist_ok=False)

    selected = _scenario_selection(scenario_names)
    chosen_executable = executable or agent
    results = [
        run_scenario(
            scenario=scenario,
            agent=agent,
            executable=chosen_executable,
            fixture=fixture,
            evidence_dir=evidence_root / scenario.name,
            timeout_seconds=timeout_seconds,
            transcript_format=transcript_format,
        )
        for scenario in selected
    ]
    summary = {
        "run_id": run_id,
        "agent": agent,
        "passed": all(result.status == "PASS" for result in results),
        "scenarios": [asdict(result) for result in results],
    }
    _write_json(evidence_root / "summary.json", summary)
    return evidence_root, results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Collaudo comportamentale LeaderAI. Nessun modello viene avviato "
            "senza il sottocomando esplicito 'live'."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser(
        "list", help="Elenca le missioni senza eseguirle"
    )
    list_parser.set_defaults(action="list")

    live = subparsers.add_parser(
        "live", help="Avvia nuove sessioni reali e valuta gli effetti"
    )
    live.add_argument("--agent", choices=("codex", "claude"), required=True)
    live.add_argument(
        "--scenario",
        action="append",
        choices=("all", *SCENARIOS.keys()),
        default=[],
        help="Ripetibile; se omesso esegue tutti gli scenari",
    )
    live.add_argument(
        "--executable",
        help="Eseguibile alternativo; utile per collaudi locali controllati",
    )
    live.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Casa anonima sorgente da copiare",
    )
    live.add_argument(
        "--evidence-dir",
        type=Path,
        help="Directory esterna in cui creare il pacchetto prove",
    )
    live.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="Timeout per scenario in secondi (default: 300)",
    )
    live.add_argument(
        "--transcript-format",
        choices=("json", "jsonl"),
        default="jsonl",
    )
    live.set_defaults(action="live")

    compare = subparsers.add_parser(
        "compare-context",
        help="Confronta contesto completo e alleggerito in due sessioni nuove",
    )
    compare.add_argument("--agent", choices=("codex", "claude"), required=True)
    compare.add_argument("--scenario", choices=tuple(SCENARIOS), required=True)
    compare.add_argument("--block-id", required=True)
    compare.add_argument("--instruction-file", required=True)
    compare.add_argument("--current-block-file", type=Path, required=True)
    compare.add_argument("--lighter-block-file", type=Path, required=True)
    compare.add_argument(
        "--candidate-action",
        choices=tuple(CLASSIFICATIONS),
        required=True,
    )
    compare.add_argument("--protected", action="store_true")
    compare.add_argument("--supporting-cases", type=int, default=1)
    compare.add_argument("--executable")
    compare.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    compare.add_argument("--evidence-dir", type=Path, required=True)
    compare.add_argument("--timeout", type=float, default=300.0)
    compare.add_argument(
        "--transcript-format",
        choices=("json", "jsonl"),
        default="jsonl",
    )
    compare.set_defaults(action="compare-context")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.action == "list":
        payload = [
            {
                "name": scenario.name,
                "missione": scenario.business_prompt,
                "output_atteso": scenario.expected_output,
            }
            for scenario in SCENARIOS.values()
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.action == "compare-context":
        if args.timeout <= 0:
            parser.error("--timeout deve essere maggiore di zero")
        variant = InstructionVariant(
            block_id=args.block_id,
            instruction_path=args.instruction_file,
            current_text=args.current_block_file.read_text(encoding="utf-8"),
            lighter_text=args.lighter_block_file.read_text(encoding="utf-8"),
            candidate_action=args.candidate_action,
            protected=args.protected,
            supporting_cases=args.supporting_cases,
        )
        result = run_context_comparison(
            scenario=SCENARIOS[args.scenario],
            variant=variant,
            agent=args.agent,
            executable=args.executable or args.agent,
            fixture=args.fixture.expanduser().resolve(),
            evidence_dir=args.evidence_dir.expanduser().resolve(),
            timeout_seconds=args.timeout,
            transcript_format=args.transcript_format,
        )
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        valid_lighter_states = {"PASS", "ORACLE_FAIL"}
        return 0 if (
            result.full.run_status == "PASS"
            and result.lighter.run_status in valid_lighter_states
        ) else 1

    if args.timeout <= 0:
        parser.error("--timeout deve essere maggiore di zero")
    evidence_root, results = run_harness(
        agent=args.agent,
        scenario_names=args.scenario,
        executable=args.executable,
        fixture=args.fixture.expanduser().resolve(),
        evidence_base=args.evidence_dir,
        timeout_seconds=args.timeout,
        transcript_format=args.transcript_format,
    )
    summary = {
        "passed": all(result.status == "PASS" for result in results),
        "evidence_dir": str(evidence_root),
        "results": [asdict(result) for result in results],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
