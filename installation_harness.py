#!/usr/bin/env python3
"""Collaudo live dell'installazione manuale LeaderAI.

Il collaudo parte da una fotografia locale e immutabile dello standard, avvia
una sessione nuova dell'agente e valuta soltanto effetti osservabili. Il
percorso provato e' quello di ``INSTALLA_CON_AI.md``: niente clone, niente
``leaderai_setup.py`` e nessun codice Python della repo disponibile all'agente.

Il modulo usa soltanto la standard library. Un modello reale viene avviato
esclusivamente dal sottocomando esplicito ``live``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import install_contract


REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_TARGET_NAME = "Casa prova - citta d'Artu"

STANDARD_FILES = (
    "INSTALLA_CON_AI.md",
    "MANIFEST.md",
    "VERSION",
    "install_contract.json",
    "templates/AGENTS.md",
    "templates/AGENT_CHAT.md",
    "templates/ASSET.md",
    "templates/CLAUDE.md",
    "templates/CLAUDE_README.md",
    "templates/CODEX_README.md",
    "templates/FONTI.md",
    "templates/GITIGNORE.txt",
    "templates/INSTALL_LOG.md",
    "templates/ISPETTORE_SKILL.md",
    "templates/LIMITI.md",
    "templates/MEMORY.md",
    "templates/PROCESSI.md",
    "templates/STANZA_AGENTS.md",
    "templates/STANZA_FONTE.md",
)

INSTALL_CONTRACT = install_contract.load_contract(
    REPO_ROOT / "install_contract.json"
)


def _contract_required(mode: str) -> tuple[str, ...]:
    destinations = [
        rule.destination
        for rule in install_contract.template_rules(INSTALL_CONTRACT, mode)
    ]
    required = install_contract.required_paths(INSTALL_CONTRACT, mode)
    return tuple(dict.fromkeys((*destinations, *required)))


MODE_REQUIRED_FILES = {
    mode: _contract_required(mode)
    for mode in INSTALL_CONTRACT["supported_agents"]
}

COMMON_TARGET_FILES = tuple(
    sorted(
        set(MODE_REQUIRED_FILES["codex"])
        & set(MODE_REQUIRED_FILES["claude"])
        & set(MODE_REQUIRED_FILES["both"])
    )
)

MODE_FORBIDDEN_PATHS = {
    mode: tuple(install_contract.forbidden_paths(INSTALL_CONTRACT, mode))
    for mode in INSTALL_CONTRACT["supported_agents"]
}

FORBIDDEN_TARGET_PATHS = (
    "INSTALLA_CON_AI.md",
    "MANIFEST.md",
    "VERSION",
    "leaderai_setup.py",
    "templates",
)

MISSION_TEMPLATE = """\
Questa e' una prova di rilascio autorizzata e isolata dello standard LeaderAI.
Lavora soltanto dentro questa workspace temporanea. Non usare internet e non
toccare impostazioni globali, Desktop, browser, email, account o cartelle
esterne.

Leggi in `standard-snapshot/INSTALLA_CON_AI.md` soltanto la sezione compresa
tra `START_NUCLEO_INSTALLAZIONE` e `END_NUCLEO_INSTALLAZIONE`. Leggi poi
`standard-snapshot/VERSION`, `standard-snapshot/install_contract.json` e i
template dichiarati dal contratto. Applica quel nucleo alla cartella locale vuota
`{target_name}`.

Dati gia' decisi:
- cliente anonimo: Cliente Collaudo;
- azienda: Azienda Collaudo;
- posizione: disco locale, nella cartella indicata sopra;
- modalita': {mode};
- backup remoto: da fare;
- seconda postazione: non serve.

Esegui il nucleo deterministico della procedura manuale:
- usa direttamente i documenti e i template della fotografia in sola lettura;
- per questo target nuovo usa comandi shell meccanici e batch per creare
  directory, copiare template e sostituire placeholder; non riscrivere i file
  uno alla volta;
- la fonte resta intoccabile; dopo la copia rendi scrivibili soltanto i file
  creati nel target, prima di personalizzarli;
- non usare Python, `leaderai_setup.py`, clone, rete o codice scaricato;
- crea e personalizza soltanto il telaio comune e le superfici della modalita';
- inizializza Git locale e crea il primo commit con identita' solo per quel
  comando se la configurazione Git globale manca;
- non inventare stanze, fonti, asset, connettori o percorsi business;
- lascia le prove che richiedono account, browser, impostazioni utente o dati
  reali come `DA COLLAUDARE` o `DA COLLEGARE`, senza fermare il telaio;
- registra in `logs/install-log.md`, con queste chiavi esatte, `default_browser`,
  `desktop_launcher` e `remote_backup`, ciascuna con stato `DA COLLAUDARE` o
  `DA COLLEGARE`;
- registra nello stesso evento del log standard, versione, modalita', prove
  svolte e limiti; la conferma finale resta nel messaggio conclusivo;
- il messaggio del primo commit contiene esattamente `installazione iniziale`.

La fotografia `standard-snapshot/` e' intoccabile. Non copiare dentro il target
la guida, il manifest, VERSION, template, script o codice della repo. Al termine
comunica soltanto l'esito sintetico.
"""


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
class InstallationResult:
    agent: str
    mode: str
    status: str
    return_code: int | None
    timed_out: bool
    executable_found: bool
    oracle_passed: bool
    evidence_dir: str
    workspace_dir: str
    target_dir: str
    duration_seconds: float
    error: str | None = None


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    """Restituisce una fotografia portabile di file, link e directory."""

    files: dict[str, dict[str, Any]] = {}
    directories: list[str] = []
    if not root.exists():
        return {"root": "$ROOT", "directories": [], "files": {}}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            files[relative] = {"kind": "symlink", "target": os.readlink(path)}
        elif path.is_dir():
            directories.append(relative)
        elif path.is_file():
            files[relative] = {
                "kind": "file",
                "sha256": _sha256(path),
                "size": path.stat().st_size,
            }
    return {"root": "$ROOT", "directories": directories, "files": files}


def diff_manifests(
    before: dict[str, Any], after: dict[str, Any]
) -> dict[str, list[str]]:
    before_files = before["files"]
    after_files = after["files"]
    before_paths = set(before_files)
    after_paths = set(after_files)
    shared = before_paths & after_paths
    before_dirs = set(before["directories"])
    after_dirs = set(after["directories"])
    return {
        "added_files": sorted(after_paths - before_paths),
        "removed_files": sorted(before_paths - after_paths),
        "modified_files": sorted(
            path for path in shared if before_files[path] != after_files[path]
        ),
        "added_directories": sorted(after_dirs - before_dirs),
        "removed_directories": sorted(before_dirs - after_dirs),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _copy_standard_snapshot(source_root: Path, snapshot: Path) -> None:
    """Copia soltanto le fonti documentali necessarie e le rende read-only."""

    snapshot.mkdir(parents=True, exist_ok=False)
    for relative in STANDARD_FILES:
        source = source_root / relative
        if not source.is_file():
            raise FileNotFoundError(f"Standard incompleto: manca {relative}")
        destination = snapshot / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)

    for path in sorted(
        snapshot.rglob("*"), key=lambda item: len(item.parts), reverse=True
    ):
        if path.is_file():
            path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif path.is_dir():
            path.chmod(
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IXOTH
            )
    snapshot.chmod(
        stat.S_IRUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )


def _resolve_executable(executable: str) -> str | None:
    candidate = Path(executable).expanduser()
    if candidate.parent != Path("."):
        return str(candidate.resolve()) if candidate.is_file() else None
    return shutil.which(executable)


def _executable_prefix(executable: str) -> list[str]:
    """Permette fake agent Python portabili nei soli test unitari."""

    if Path(executable).suffix.casefold() == ".py":
        return [sys.executable, executable]
    return [executable]


def build_command(
    agent: str,
    executable: str,
    workspace: Path,
    transcript_format: str,
) -> list[str]:
    """Costruisce una sessione nuova confinata nella workspace temporanea."""

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
            str(workspace),
            "--json",
            "-",
        ]
    if agent == "claude":
        output_format = "stream-json" if transcript_format == "jsonl" else "json"
        # Il live parte solo su comando esplicito, dentro una workspace
        # temporanea usa-e-getta. Il bypass evita richieste interattive sui
        # file `.claude/` e su Git che renderebbero il gate non ripetibile.
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
            "Read,Write,Edit,Glob,Grep,Bash",
            "--permission-mode",
            "bypassPermissions",
            "--output-format",
            output_format,
        ]
        if transcript_format == "jsonl":
            command.append("--verbose")
        return command
    raise ValueError(f"Agente non supportato: {agent}")


def redact_command(
    command: Sequence[str], workspace: Path, target: Path
) -> list[str]:
    redacted: list[str] = []
    for item in command:
        cleaned = item.replace(str(target), "$TARGET")
        cleaned = cleaned.replace(str(workspace), "$WORKSPACE")
        redacted.append(cleaned)
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
    workspace: Path,
    prompt: str,
    timeout_seconds: float,
) -> ProcessOutcome:
    started = _utc_now()
    try:
        completed = subprocess.run(
            list(command),
            cwd=workspace,
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
    return records or [{"type": "empty"}]


def write_transcript(
    evidence_dir: Path, stdout: str, transcript_format: str
) -> Path:
    if transcript_format == "jsonl":
        path = evidence_dir / "transcript.jsonl"
        path.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                for record in _parse_json_lines(stdout)
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
    _write_json(path, payload)
    return path


def _run_git(target: Path, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(target), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def inspect_git(target: Path) -> dict[str, Any]:
    """Raccoglie prove Git senza cambiare il target."""

    evidence: dict[str, Any] = {
        "available": False,
        "is_repository": False,
        "commit_count": 0,
        "log": "",
        "status": "",
        "remotes": "",
        "ignored_safety_paths": [],
        "error": None,
    }
    try:
        inside = _run_git(target, ["rev-parse", "--is-inside-work-tree"])
    except FileNotFoundError as exc:
        evidence["error"] = str(exc)
        return evidence

    evidence["available"] = True
    evidence["is_repository"] = (
        inside.returncode == 0 and inside.stdout.strip() == "true"
    )
    if not evidence["is_repository"]:
        evidence["error"] = inside.stderr.strip() or "Non e' un repository Git"
        return evidence

    count = _run_git(target, ["rev-list", "--count", "HEAD"])
    if count.returncode == 0:
        try:
            evidence["commit_count"] = int(count.stdout.strip())
        except ValueError:
            evidence["commit_count"] = 0
    log = _run_git(target, ["log", "--format=%H %s"])
    evidence["log"] = log.stdout
    status_result = _run_git(target, ["status", "--porcelain=v1"])
    evidence["status"] = status_result.stdout
    remotes = _run_git(target, ["remote", "-v"])
    evidence["remotes"] = remotes.stdout
    safety_paths = (
        ".secrets/prova.txt",
        "prova.env",
        "api-token-prova.txt",
        "client-secret-prova.txt",
        "client-password-prova.txt",
        "client-credential-prova.txt",
    )
    ignored: list[str] = []
    for relative in safety_paths:
        result = _run_git(target, ["check-ignore", "--quiet", "--", relative])
        if result.returncode == 0:
            ignored.append(relative)
    evidence["ignored_safety_paths"] = ignored
    return evidence


def _check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"name": name, "passed": passed, "detail": detail}


def _read_text(target: Path, relative: str) -> str:
    path = target / relative
    if not path.is_file() or path.is_symlink():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _log_mode(install_log: str) -> str | None:
    match = re.search(
        r"(?im)^\s*(?:(?:-|\*)\s+)?(?:\*\*)?"
        r"(?:agent|modalit(?:a'?|à))"
        r"(?:\s+(?:scelta|installata|attiva))?(?:\*\*)?\s*:\s*(?:\*\*)?\s*"
        r"`?(codex|claude|both)`?(?=\s|[.;,(]|$)",
        install_log,
    )
    return match.group(1).casefold() if match else None


def evaluate_oracle(
    *,
    target: Path,
    snapshot: Path,
    mode: str,
    snapshot_before: dict[str, Any],
    snapshot_after: dict[str, Any],
    target_before: dict[str, Any],
    target_after: dict[str, Any],
    git_evidence: dict[str, Any],
) -> dict[str, Any]:
    """Verifica parita' manuale, modalita', Git, versione e log tecnico."""

    version = (snapshot / "VERSION").read_text(encoding="utf-8").strip()
    present_files = set(target_after["files"])
    present_dirs = set(target_after["directories"])

    common_missing = sorted(set(COMMON_TARGET_FILES) - present_files)
    mode_missing = sorted(set(MODE_REQUIRED_FILES[mode]) - present_files)
    forbidden_present = sorted(
        relative
        for relative in (*MODE_FORBIDDEN_PATHS[mode], *FORBIDDEN_TARGET_PATHS)
        if relative in present_files
        or relative in present_dirs
        or any(path.startswith(relative.rstrip("/") + "/") for path in present_files)
    )

    agents = _read_text(target, "AGENTS.md")
    install_log = _read_text(target, "logs/install-log.md")
    bridge = _read_text(target, "CLAUDE.md")
    gitignore = _read_text(target, ".gitignore")

    install_log_folded = install_log.casefold()
    declared_mode = install_contract.declared_agent(agents)
    logged_mode = _log_mode(install_log)
    version_ok = (
        version in agents
        and version in install_log
        and declared_mode == mode
        and logged_mode == mode
    )
    deferred_checks_recorded = (
        "da collaudare" in install_log_folded
        or "da collegare" in install_log_folded
    )
    environment_checks_recorded = all(
        re.search(
            rf"{re.escape(check)}.{{0,120}}\bda\s+(?:collaudare|collegare)\b",
            install_log_folded,
            flags=re.DOTALL,
        )
        for check in install_contract.environment_checks(INSTALL_CONTRACT)
    )

    required_ignore_rules = [
        line.strip()
        for line in (snapshot / "templates/GITIGNORE.txt")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    ignore_missing = sorted(
        rule for rule in required_ignore_rules if rule not in gitignore.splitlines()
    )
    expected_ignored = {
        ".secrets/prova.txt",
        "prova.env",
        "api-token-prova.txt",
        "client-secret-prova.txt",
        "client-password-prova.txt",
        "client-credential-prova.txt",
    }
    ignored_observed = set(git_evidence["ignored_safety_paths"])
    git_ok = (
        git_evidence["available"]
        and git_evidence["is_repository"]
        and git_evidence["commit_count"] >= 1
        and "installazione iniziale" in git_evidence["log"].casefold()
        and not git_evidence["status"].strip()
        and not git_evidence["remotes"].strip()
        and expected_ignored <= ignored_observed
    )

    generated_with_placeholders = sorted(
        relative
        for relative in (
            "AGENTS.md",
            "AGENT_CHAT.md",
            "memory/MEMORY.md",
        )
        if "{{" in _read_text(target, relative)
    )
    ecosystem_allowed_files = {
        relative
        for relative in MODE_REQUIRED_FILES[mode]
        if Path(relative).parts and Path(relative).parts[0] == "ecosistema"
    }
    ecosystem_allowed_dirs = {"ecosistema"}
    for relative in ecosystem_allowed_files:
        parent = Path(relative).parent
        while parent != Path("."):
            ecosystem_allowed_dirs.add(parent.as_posix())
            parent = parent.parent
    ecosystem_observed = {
        relative
        for relative in (*present_files, *present_dirs)
        if Path(relative).parts and Path(relative).parts[0] == "ecosistema"
    }
    unexpected_ecosystem_entries = sorted(
        ecosystem_observed - ecosystem_allowed_files - ecosystem_allowed_dirs
    )
    room_template_issues: list[str] = []
    room_policy = install_contract.room_lifecycle_policy(INSTALL_CONTRACT)
    room_template_destinations = {
        room_policy.map_template,
        room_policy.source_template,
    }
    for rule in install_contract.template_rules(INSTALL_CONTRACT, mode):
        if rule.destination not in room_template_destinations:
            continue
        installed = target / rule.destination
        expected = snapshot / "templates" / rule.template
        if installed.is_symlink():
            room_template_issues.append(f"{rule.destination}:symlink")
            continue
        try:
            matches = (
                installed.is_file()
                and installed.read_bytes() == expected.read_bytes()
            )
        except OSError:
            matches = False
        if not matches:
            room_template_issues.append(f"{rule.destination}:contenuto")
    python_files = sorted(
        relative for relative in present_files if relative.casefold().endswith(".py")
    )
    clone_markers = sorted(
        relative
        for relative in present_dirs
        if relative.endswith(".git/modules") or "/.git/modules/" in relative
    )
    allowed_root_names = {
        Path(relative).parts[0]
        for relative in MODE_REQUIRED_FILES[mode]
    } | {".git"}
    observed_root_names = {
        Path(relative).parts[0]
        for relative in (*present_files, *present_dirs)
        if Path(relative).parts
    }
    unexpected_root_entries = sorted(observed_root_names - allowed_root_names)
    snapshot_diff = diff_manifests(snapshot_before, snapshot_after)
    target_diff = diff_manifests(target_before, target_after)

    checks = [
        _check(
            "fotografia_standard_completa",
            set(STANDARD_FILES) <= set(snapshot_before["files"]),
            f"file={len(snapshot_before['files'])}",
        ),
        _check(
            "fotografia_standard_immutata",
            snapshot_before == snapshot_after,
            json.dumps(snapshot_diff, ensure_ascii=False, sort_keys=True),
        ),
        _check(
            "telaio_comune_completo",
            not common_missing,
            f"mancanti={common_missing}",
        ),
        _check(
            "modalita_esatta",
            not mode_missing and not forbidden_present,
            f"modalita={mode}; mancanti={mode_missing}; vietati={forbidden_present}",
        ),
        _check(
            "ponte_claude_canonico",
            bridge == "@AGENTS.md\n",
            repr(bridge),
        ),
        _check(
            "versione_e_log_coerenti",
            version_ok
            and deferred_checks_recorded
            and environment_checks_recorded,
            (
                f"versione={version}; modalita_mappa={declared_mode}; "
                f"modalita_log={logged_mode}; "
                f"prove_differite={deferred_checks_recorded}; "
                f"controlli_ambiente={environment_checks_recorded}"
            ),
        ),
        _check(
            "git_locale_pronto_e_segreti_ignorati",
            git_ok and not ignore_missing,
            (
                f"repo={git_evidence['is_repository']}; "
                f"commit={git_evidence['commit_count']}; "
                f"pulito={not bool(git_evidence['status'].strip())}; "
                f"remoti={bool(git_evidence['remotes'].strip())}; "
                f"regole_mancanti={ignore_missing}"
            ),
        ),
        _check(
            "installazione_manual_senza_setup_clone_o_codice",
            not python_files
            and not clone_markers
            and not forbidden_present
            and not unexpected_root_entries,
            (
                f"python={python_files}; clone={clone_markers}; "
                f"copie_standard={forbidden_present}; "
                f"root_inattese={unexpected_root_entries}"
            ),
        ),
        _check(
            "nessun_placeholder_cliente_nel_core",
            not generated_with_placeholders,
            f"file={generated_with_placeholders}",
        ),
        _check(
            "armadio_comune_ermetico",
            not unexpected_ecosystem_entries,
            f"elementi_inattesi={unexpected_ecosystem_entries}",
        ),
        _check(
            "calchi_stanza_integri",
            not room_template_issues,
            f"problemi={room_template_issues}",
        ),
        _check(
            "log_installazione_presente",
            bool(install_log.strip()) and version in install_log,
            f"logs/install-log.md; versione={version}",
        ),
        _check(
            "target_partito_vuoto_ed_evidenze_osservabili",
            not target_before["files"]
            and bool(target_diff["added_files"])
            and "logs/install-log.md" in target_diff["added_files"],
            json.dumps(target_diff, ensure_ascii=False, sort_keys=True),
        ),
    ]
    return {
        "mode": mode,
        "version": version,
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }


def _ensure_separate_paths(target: Path, evidence: Path) -> None:
    target = target.resolve()
    evidence = evidence.resolve()
    if (
        target == evidence
        or target in evidence.parents
        or evidence in target.parents
    ):
        raise ValueError("Target ed evidenze devono vivere in directory separate")


def run_installation(
    *,
    agent: str,
    mode: str,
    executable: str | None,
    source_root: Path,
    evidence_dir: Path,
    timeout_seconds: float,
    transcript_format: str,
    workspace_dir: Path | None = None,
    target_name: str = DEFAULT_TARGET_NAME,
) -> InstallationResult:
    """Esegue una installazione manuale in una workspace usa-e-getta."""

    if agent not in ("codex", "claude"):
        raise ValueError(f"Agente non supportato: {agent}")
    if mode not in MODE_REQUIRED_FILES:
        raise ValueError(f"Modalita' non supportata: {mode}")
    if not target_name or target_name in (".", ".."):
        raise ValueError("Nome target non valido")
    if Path(target_name).is_absolute() or len(Path(target_name).parts) != 1:
        raise ValueError("Il target deve essere un solo nome relativo")

    evidence_dir = evidence_dir.expanduser().resolve()
    evidence_dir.mkdir(parents=True, exist_ok=False)
    temporary_workspace: tempfile.TemporaryDirectory[str] | None = None
    if workspace_dir is None:
        temporary_workspace = tempfile.TemporaryDirectory(
            prefix="leaderai-manual-install-"
        )
        workspace = Path(temporary_workspace.name)
    else:
        workspace = workspace_dir.expanduser().resolve()
        workspace.mkdir(parents=True, exist_ok=False)

    snapshot = workspace / "standard-snapshot"
    target = workspace / target_name
    target.mkdir(parents=True, exist_ok=False)
    _ensure_separate_paths(target, evidence_dir)

    try:
        _copy_standard_snapshot(source_root.expanduser().resolve(), snapshot)
        snapshot_before = build_manifest(snapshot)
        target_before = build_manifest(target)
        _write_json(evidence_dir / "standard-manifest-pre.json", snapshot_before)
        _write_json(evidence_dir / "target-manifest-pre.json", target_before)

        prompt = MISSION_TEMPLATE.format(target_name=target.name, mode=mode)
        (evidence_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

        chosen = executable or agent
        resolved = _resolve_executable(chosen)
        command_executable = resolved or chosen
        command = build_command(
            agent, command_executable, workspace, transcript_format
        )
        _write_json(
            evidence_dir / "command.json",
            {
                "agent": agent,
                "mode": mode,
                "argv": redact_command(command, workspace, target),
                "cwd": "$WORKSPACE",
                "target": "$WORKSPACE/" + target.name,
                "snapshot": "$WORKSPACE/standard-snapshot",
                "prompt_transport": "stdin",
                "environment_recorded": False,
                "network_allowed_by_mission": False,
            },
        )

        outcome = execute_agent(command, workspace, prompt, timeout_seconds)
        (evidence_dir / "stdout.raw").write_text(outcome.stdout, encoding="utf-8")
        (evidence_dir / "stderr.txt").write_text(outcome.stderr, encoding="utf-8")
        write_transcript(evidence_dir, outcome.stdout, transcript_format)

        snapshot_after = build_manifest(snapshot)
        target_after = build_manifest(target)
        git_evidence = inspect_git(target)
        oracle = evaluate_oracle(
            target=target,
            snapshot=snapshot,
            mode=mode,
            snapshot_before=snapshot_before,
            snapshot_after=snapshot_after,
            target_before=target_before,
            target_after=target_after,
            git_evidence=git_evidence,
        )
        _write_json(evidence_dir / "standard-manifest-post.json", snapshot_after)
        _write_json(evidence_dir / "standard-diff.json", diff_manifests(
            snapshot_before, snapshot_after
        ))
        _write_json(evidence_dir / "target-manifest-post.json", target_after)
        _write_json(
            evidence_dir / "target-diff.json",
            diff_manifests(target_before, target_after),
        )
        _write_json(evidence_dir / "git.json", git_evidence)
        _write_json(evidence_dir / "oracle.json", oracle)

        for relative, evidence_name in (
            ("logs/install-log.md", "observed-install-log.md"),
            ("AGENTS.md", "observed-agents.md"),
        ):
            source = target / relative
            if source.is_file() and not source.is_symlink():
                shutil.copyfile(source, evidence_dir / evidence_name)

        if outcome.state != "COMPLETED":
            status = outcome.state
        elif oracle["passed"]:
            status = "PASS"
        else:
            status = "ORACLE_FAIL"

        result = InstallationResult(
            agent=agent,
            mode=mode,
            status=status,
            return_code=outcome.return_code,
            timed_out=outcome.state == "TIMEOUT",
            executable_found=outcome.state != "EXECUTABLE_MISSING",
            oracle_passed=bool(oracle["passed"]),
            evidence_dir=str(evidence_dir),
            workspace_dir=(
                "$TEMPORARY_WORKSPACE"
                if temporary_workspace is not None
                else str(workspace)
            ),
            target_dir=(
                "$TEMPORARY_TARGET"
                if temporary_workspace is not None
                else str(target)
            ),
            duration_seconds=outcome.duration_seconds,
            error=outcome.error,
        )
        _write_json(evidence_dir / "result.json", asdict(result))
        return result
    finally:
        if temporary_workspace is not None:
            temporary_workspace.cleanup()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Collaudo dell'installazione manuale LeaderAI. Nessun modello "
            "viene avviato senza il sottocomando esplicito 'live'."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    describe = subparsers.add_parser(
        "describe", help="Mostra il contratto senza avviare agenti"
    )
    describe.set_defaults(action="describe")

    live = subparsers.add_parser(
        "live", help="Avvia una sessione reale e valuta l'installazione"
    )
    live.add_argument("--agent", choices=("codex", "claude"), required=True)
    live.add_argument("--mode", choices=("codex", "claude", "both"))
    live.add_argument("--executable")
    live.add_argument("--source-root", type=Path, default=REPO_ROOT)
    live.add_argument(
        "--evidence-dir",
        type=Path,
        help="Directory esterna da creare per le prove",
    )
    live.add_argument("--timeout", type=float, default=600.0)
    live.add_argument(
        "--transcript-format", choices=("json", "jsonl"), default="jsonl"
    )
    live.set_defaults(action="live")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.action == "describe":
        print(
            json.dumps(
                {
                    "standard_files": list(STANDARD_FILES),
                    "common_target_files": list(COMMON_TARGET_FILES),
                    "mode_required_files": MODE_REQUIRED_FILES,
                    "live_by_default": False,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    if args.timeout <= 0:
        parser.error("--timeout deve essere maggiore di zero")
    mode = args.mode or args.agent
    if args.evidence_dir is None:
        evidence_dir = Path(
            tempfile.mkdtemp(prefix="leaderai-install-evidence-parent-")
        ) / f"{_utc_now().strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    else:
        evidence_dir = args.evidence_dir

    try:
        result = run_installation(
            agent=args.agent,
            mode=mode,
            executable=args.executable,
            source_root=args.source_root,
            evidence_dir=evidence_dir,
            timeout_seconds=args.timeout,
            transcript_format=args.transcript_format,
        )
    except (FileNotFoundError, FileExistsError, ValueError, OSError) as exc:
        print(f"ERRORE HARNESS: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
