"""Gate unico per test deterministici e rilascio live.

Uso:

``python3 -m tests.gate --quick``
    Esegue tutta la suite deterministica. Zero test o test saltati falliscono.

``python3 -m tests.gate --release --agents codex,claude``
    Esegue prima la suite deterministica, poi i collaudi comportamentali e
    d'installazione manuale su sessioni reali di entrambi gli agenti.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence, TextIO


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RELEASE_AGENTS = ("codex", "claude")


@dataclass
class QuickResult:
    status: str
    tests_run: int
    failures: int
    errors: int
    skipped: int
    successful: bool


def _utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def discover_suite(
    *,
    start_dir: Path = REPO_ROOT / "tests",
    top_level_dir: Path = REPO_ROOT,
) -> unittest.TestSuite:
    """Scopre in modo esplicito tutti i ``test_*.py`` della repo."""

    return unittest.defaultTestLoader.discover(
        start_dir=str(start_dir),
        pattern="test_*.py",
        top_level_dir=str(top_level_dir),
    )


def run_quick(
    *,
    stream: TextIO | None = None,
    verbosity: int = 1,
    suite: unittest.TestSuite | None = None,
) -> QuickResult:
    """Esegue la suite e considera zero test o skip un gate fallito."""

    selected = suite if suite is not None else discover_suite()
    runner = unittest.TextTestRunner(
        stream=stream or sys.stderr,
        verbosity=verbosity,
    )
    result = runner.run(selected)
    skipped = len(result.skipped)
    successful = (
        result.testsRun > 0
        and result.wasSuccessful()
        and skipped == 0
    )
    if result.testsRun == 0:
        status = "ZERO_TESTS"
    elif skipped:
        status = "SKIPPED_TESTS"
    elif result.wasSuccessful():
        status = "PASS"
    else:
        status = "TEST_FAILURE"
    return QuickResult(
        status=status,
        tests_run=result.testsRun,
        failures=len(result.failures),
        errors=len(result.errors),
        skipped=skipped,
        successful=successful,
    )


def parse_agents(raw: str) -> tuple[str, ...]:
    agents = tuple(
        dict.fromkeys(part.strip().casefold() for part in raw.split(",") if part.strip())
    )
    unknown = sorted(set(agents) - set(REQUIRED_RELEASE_AGENTS))
    if unknown:
        raise ValueError(f"Agenti non supportati: {', '.join(unknown)}")
    missing = sorted(set(REQUIRED_RELEASE_AGENTS) - set(agents))
    if missing:
        raise ValueError(
            "Un rilascio richiede entrambi gli agenti; mancanti: "
            + ", ".join(missing)
        )
    return agents


def _live_entry(
    *,
    kind: str,
    agent: str,
    status: str,
    evidence_dir: str,
    detail: dict[str, Any],
) -> dict[str, Any]:
    return {
        "kind": kind,
        "agent": agent,
        "status": status,
        "passed": status == "PASS",
        "evidence_dir": evidence_dir,
        "detail": detail,
    }


def run_release_live(
    *,
    agents: Sequence[str],
    evidence_root: Path,
    timeout_seconds: float,
    executables: dict[str, str | None] | None = None,
) -> list[dict[str, Any]]:
    """Esegue i due harness live; ogni stato diverso da PASS resta bloccante."""

    import behavior_harness
    import installation_harness

    overrides = executables or {}
    entries: list[dict[str, Any]] = []
    for agent in agents:
        try:
            behavior_evidence, behavior_results = behavior_harness.run_harness(
                agent=agent,
                scenario_names=("all",),
                executable=overrides.get(agent),
                fixture=behavior_harness.DEFAULT_FIXTURE,
                evidence_base=evidence_root / "behavior" / agent,
                timeout_seconds=timeout_seconds,
                transcript_format="jsonl",
            )
            statuses = [result.status for result in behavior_results]
            behavior_status = (
                "PASS"
                if behavior_results
                and all(status == "PASS" for status in statuses)
                else (
                    "ZERO_SCENARIOS"
                    if not behavior_results
                    else next(status for status in statuses if status != "PASS")
                )
            )
            entries.append(
                _live_entry(
                    kind="behavior",
                    agent=agent,
                    status=behavior_status,
                    evidence_dir=str(behavior_evidence),
                    detail={
                        "scenario_count": len(behavior_results),
                        "statuses": statuses,
                    },
                )
            )
        except Exception as exc:  # pragma: no cover - difesa del gate live
            entries.append(
                _live_entry(
                    kind="behavior",
                    agent=agent,
                    status="HARNESS_ERROR",
                    evidence_dir=str(evidence_root / "behavior" / agent),
                    detail={"error": str(exc)},
                )
            )

        install_evidence = evidence_root / "installation" / agent
        try:
            install_result = installation_harness.run_installation(
                agent=agent,
                mode=agent,
                executable=overrides.get(agent),
                source_root=REPO_ROOT,
                evidence_dir=install_evidence,
                timeout_seconds=timeout_seconds,
                transcript_format="jsonl",
            )
            entries.append(
                _live_entry(
                    kind="manual_installation",
                    agent=agent,
                    status=install_result.status,
                    evidence_dir=install_result.evidence_dir,
                    detail=asdict(install_result),
                )
            )
        except Exception as exc:  # pragma: no cover - difesa del gate live
            entries.append(
                _live_entry(
                    kind="manual_installation",
                    agent=agent,
                    status="HARNESS_ERROR",
                    evidence_dir=str(install_evidence),
                    detail={"error": str(exc)},
                )
            )
    return entries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gate di rilascio LeaderAI: nessun live implicito."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--quick",
        action="store_true",
        help="Esegue soltanto i test deterministici",
    )
    mode.add_argument(
        "--release",
        action="store_true",
        help="Esegue test deterministici e collaudi live completi",
    )
    parser.add_argument(
        "--agents",
        help="Per --release deve essere codex,claude",
    )
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--codex-executable")
    parser.add_argument("--claude-executable")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout deve essere maggiore di zero")
    if args.quick and args.agents:
        parser.error("--agents si usa soltanto con --release")
    if args.release and not args.agents:
        parser.error("--release richiede --agents codex,claude")

    agents: tuple[str, ...] = ()
    if args.release:
        try:
            agents = parse_agents(args.agents)
        except ValueError as exc:
            parser.error(str(exc))

    quick = run_quick(verbosity=1 + args.verbose)
    print(json.dumps(asdict(quick), ensure_ascii=False, indent=2))
    if not quick.successful:
        return 1
    if args.quick:
        return 0

    if args.evidence_dir is None:
        evidence_root = Path(
            tempfile.mkdtemp(prefix="leaderai-release-evidence-")
        )
    else:
        evidence_root = (
            args.evidence_dir.expanduser().resolve()
            / f"{_utc_stamp()}-{uuid.uuid4().hex[:8]}"
        )
        evidence_root.mkdir(parents=True, exist_ok=False)

    entries = run_release_live(
        agents=agents,
        evidence_root=evidence_root,
        timeout_seconds=args.timeout,
        executables={
            "codex": args.codex_executable,
            "claude": args.claude_executable,
        },
    )
    passed = (
        len(entries) == len(REQUIRED_RELEASE_AGENTS) * 2
        and all(entry["status"] == "PASS" for entry in entries)
    )
    summary = {
        "mode": "release",
        "passed": passed,
        "quick": asdict(quick),
        "agents": list(agents),
        "evidence_root": str(evidence_root),
        "live": entries,
    }
    _write_json(evidence_root / "release-summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
