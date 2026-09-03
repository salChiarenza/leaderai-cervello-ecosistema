#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import install_contract


ROOT = Path(__file__).resolve().parent
STANDARD_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
CONTRACT = install_contract.CONTRACT

GITIGNORE_CONTENT = (ROOT / "templates" / "GITIGNORE.txt").read_text(encoding="utf-8")
SUPPORTED_AGENTS = set(CONTRACT["supported_agents"])
CLAUDE_BRIDGE = "@AGENTS.md\n"
_ALL_STANDARD_FILES = {
    rule.destination
    for agent_name in SUPPORTED_AGENTS
    for rule in install_contract.template_rules(CONTRACT, agent_name)
}
STANDARD_FILES = tuple(sorted(_ALL_STANDARD_FILES))
STANDARD_DIRS = tuple(
    sorted(
        {
            Path(rel).parts[0]
            for rel in STANDARD_FILES
            if len(Path(rel).parts) > 1
        }
        | {".git"}
    )
)


@dataclass
class InstallResult:
    target: Path
    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    external_effects: list[str] = field(default_factory=list)
    target_verdict: str | None = None
    inspection_codes: list[str] = field(default_factory=list)
    git_outcome: str = "Git: non ancora valutato."

    def record(self, status: str, path: Path) -> None:
        rel = path.relative_to(self.target).as_posix()
        if status == "created":
            self.created.append(rel)
        elif status == "updated":
            self.updated.append(rel)
        elif status == "removed":
            self.removed.append(rel)
        else:
            self.existing.append(rel)


def read_template(name: str, context: dict[str, str]) -> str:
    text = (ROOT / "templates" / name).read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def _installed_version(target: Path) -> str | None:
    agents_path = target / "AGENTS.md"
    if not agents_path.is_file() or agents_path.is_symlink():
        return None
    match = re.search(
        r"Versione standard applicata:\s*`?(\d+\.\d+\.\d+)",
        agents_path.read_text(encoding="utf-8"),
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else None


def _declared_or_detected_agent(target: Path) -> str | None:
    agents_path = target / "AGENTS.md"
    declared = None
    if agents_path.is_file() and not agents_path.is_symlink():
        declared = install_contract.declared_agent(
            agents_path.read_text(encoding="utf-8")
        )
    if declared:
        return declared
    detected = install_contract.detected_agents(CONTRACT, target)
    if detected == {"codex", "claude"}:
        return "both"
    if len(detected) == 1:
        return next(iter(detected))
    return None


def _portable_machine_path(path: Path) -> str:
    resolved = path.expanduser().resolve()
    home = Path.home().resolve()
    try:
        relative = resolved.relative_to(home)
    except ValueError:
        return str(resolved)
    if not relative.parts:
        return "~/"
    return f"~/{relative.as_posix()}"


def _safe_external_file(path: Path) -> None:
    absolute = path.expanduser().absolute()
    if absolute.is_symlink():
        raise ValueError(f"Percorso settings collegato tramite symlink: {absolute}")
    if absolute.exists() and not absolute.is_file():
        raise ValueError(f"Il percorso settings non e' un file: {absolute}")


def _prepare_claude_user_settings(
    target: Path,
    settings_path: Path,
) -> tuple[Path, dict, str, bool]:
    settings_path = settings_path.expanduser().absolute()
    _safe_external_file(settings_path)
    if target == settings_path or target in settings_path.parents:
        raise ValueError(
            "Le user settings Claude non possono vivere dentro la cartella cliente."
        )
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"User settings Claude non sono JSON valido: {settings_path}"
            ) from exc
        if not isinstance(settings, dict):
            raise ValueError("Le user settings Claude devono contenere un oggetto JSON.")
    else:
        settings = {}

    desired_path = (target / "memory").resolve()
    desired_raw = _portable_machine_path(desired_path)
    current_raw = settings.get("autoMemoryDirectory")
    if current_raw is not None:
        if not isinstance(current_raw, str):
            raise ValueError(
                "autoMemoryDirectory esiste ma non e' una stringa: "
                "non viene sovrascritto."
            )
        configured = Path(current_raw).expanduser()
        if not configured.is_absolute():
            raise ValueError(
                "autoMemoryDirectory deve essere assoluto o iniziare con ~/."
            )
        if configured.resolve() != desired_path:
            raise ValueError(
                "autoMemoryDirectory punta a una memoria diversa: confrontare "
                "e unire le memorie prima di migrare il percorso."
            )
    changed = current_raw != desired_raw
    prepared = dict(settings)
    prepared["autoMemoryDirectory"] = desired_raw
    return settings_path, prepared, desired_raw, changed


def ensure_claude_user_settings(
    target: Path,
    settings_path: Path,
    result: InstallResult,
    dry_run: bool,
) -> None:
    path, settings, desired, changed = _prepare_claude_user_settings(
        target,
        settings_path,
    )
    if changed and not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    state = "aggiornate" if changed else "gia' corrette"
    result.external_effects.append(
        f"User settings Claude {state}: {path} -> {desired}"
    )


USER_INSTRUCTIONS = {
    "claude": {"effect": "claude_user_instructions", "label": "Claude Code"},
    "codex": {"effect": "codex_user_instructions", "label": "Codex"},
}


def _user_instructions_spec(agent: str) -> dict:
    return CONTRACT["external_effects"][USER_INSTRUCTIONS[agent]["effect"]]


def _active_user_instructions_path(agent: str, requested: Path) -> Path:
    """File di istruzioni globali che l'agente legge davvero su questa macchina.

    Codex legge `AGENTS.override.md` al posto di `AGENTS.md` quando esiste:
    il blocco va nel file attivo, altrimenti resta invisibile.
    """
    path = requested.expanduser().absolute()
    if agent == "codex" and path.name == "AGENTS.md":
        override = path.with_name("AGENTS.override.md")
        if override.is_file():
            return override
    return path


def merge_marked_block(existing: str, block: str, start: str, end: str) -> str:
    """Inserisce o aggiorna il blocco marcato senza toccare il resto del file."""
    block = block.strip("\n")
    if start in existing and end in existing and existing.index(start) < existing.index(end):
        head, _, rest = existing.partition(start)
        _, _, tail = rest.partition(end)
        merged = head + block + tail
    elif existing.strip():
        merged = existing.rstrip("\n") + "\n\n" + block + "\n"
    else:
        merged = block + "\n"
    if not merged.endswith("\n"):
        merged += "\n"
    return merged


def _prepare_user_instructions(
    agent: str,
    target: Path,
    requested: Path,
    context: dict[str, str],
) -> tuple[Path, str, bool]:
    spec = _user_instructions_spec(agent)
    path = _active_user_instructions_path(agent, requested)
    _safe_external_file(path)
    if target == path or target in path.parents:
        raise ValueError(
            "Le istruzioni globali dell'agente non possono vivere dentro la cartella cliente."
        )
    block = read_template(str(spec["template"]), context).strip("\n")
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            raise ValueError(
                f"Le istruzioni globali non sono testo UTF-8 leggibile: {path}"
            ) from exc
    else:
        existing = ""
    merged = merge_marked_block(
        existing, block, str(spec["block_start"]), str(spec["block_end"])
    )
    return path, merged, merged != existing


def ensure_user_instructions(
    agent: str,
    target: Path,
    requested: Path | None,
    context: dict[str, str],
    result: InstallResult,
    dry_run: bool,
) -> None:
    label = USER_INSTRUCTIONS[agent]["label"]
    if requested is None:
        # Nessun percorso letto su questa macchina: il setup non tocca la home
        # alla cieca. Resta un gesto da collaudare sul computer del cliente.
        result.external_effects.append(
            f"Istruzioni globali {label}: DA COLLAUDARE sulla macchina cliente "
            f"({_user_instructions_spec(agent)['default_path']} non indicato)."
        )
        return
    path, merged, changed = _prepare_user_instructions(agent, target, requested, context)
    if changed and not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(merged, encoding="utf-8")
    state = "aggiornate" if changed else "gia' corrette"
    result.external_effects.append(f"Istruzioni globali {label} {state}: {path}")


def _agent_specific_rules(agent: str) -> list[install_contract.TemplateRule]:
    return [
        install_contract.TemplateRule(
            template=str(raw["template"]),
            destination=str(raw["destination"]),
            strategy=str(raw["strategy"]),
        )
        for raw in CONTRACT["agents"][agent].get("templates", [])
    ]


def _generated_agent_file_is_safe(
    path: Path,
    rule: install_contract.TemplateRule,
    context: dict[str, str],
) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    current = path.read_text(encoding="utf-8")
    expected = read_template(rule.template, context).rstrip() + "\n"
    if current == expected:
        return True
    if rule.strategy == "merge_hooks_json":
        try:
            return json.loads(current) == json.loads(expected)
        except json.JSONDecodeError:
            return False
    if rule.template == "ISPETTORE_SKILL.md":
        return (
            "name: ispettore-ecosistema" in current
            and "Creato da LeaderAI Cervello + Ecosistema il " in current
        )
    return False


def _preflight_agent_transition(
    target: Path,
    requested: str,
    context: dict[str, str],
    migrate_agent: bool,
) -> tuple[str | None, set[str]]:
    current = _declared_or_detected_agent(target)
    detected = install_contract.detected_agents(CONTRACT, target)
    requested_agents = (
        {"codex", "claude"} if requested == "both" else {requested}
    )
    current_agents = (
        {"codex", "claude"}
        if current == "both"
        else ({current} if current else detected)
    )
    remove_agents = current_agents - requested_agents
    crossing = bool(remove_agents) and requested != "both"
    opposite_present = bool(detected - requested_agents) and requested != "both"
    if (crossing or opposite_present) and not migrate_agent:
        raise ValueError(
            "Cambio agente bloccato prima di creare il ramo opposto: usare "
            "--agent both oppure --migrate-agent per una migrazione esplicita."
        )
    if not migrate_agent:
        return current, set()

    remove_agents |= detected - requested_agents
    for old_agent in sorted(remove_agents):
        rules = _agent_specific_rules(old_agent)
        allowed = {rule.destination for rule in rules}
        roots = {Path(rel).parts[0] for rel in allowed}
        for root_name in roots:
            root = target / root_name
            if not root.exists():
                continue
            if root.is_symlink() or not root.is_dir():
                raise ValueError(
                    f"Ramo {old_agent} non migrabile in sicurezza: {root}"
                )
            extras = {
                path.relative_to(target).as_posix()
                for path in root.rglob("*")
                if path.is_file() or path.is_symlink()
            } - allowed
            if extras:
                raise ValueError(
                    f"Ramo {old_agent} contiene dati non standard da preservare: "
                    + ", ".join(sorted(extras))
                )
        for rule in rules:
            path = target / rule.destination
            if path.exists() and not _generated_agent_file_is_safe(
                path,
                rule,
                context,
            ):
                raise ValueError(
                    f"File {old_agent} modificato dal cliente, migrazione fermata: "
                    f"{rule.destination}"
                )
    return current, remove_agents


def _apply_agent_transition(
    target: Path,
    requested: str,
    current: str | None,
    remove_agents: set[str],
    result: InstallResult,
    dry_run: bool,
) -> None:
    for old_agent in sorted(remove_agents):
        for rule in _agent_specific_rules(old_agent):
            path = target / rule.destination
            if not path.exists():
                continue
            if not dry_run:
                path.unlink()
            result.record("removed", path)
        roots = {
            target / Path(rule.destination).parts[0]
            for rule in _agent_specific_rules(old_agent)
        }
        if not dry_run:
            for root in roots:
                if not root.exists():
                    continue
                for directory in sorted(
                    (path for path in root.rglob("*") if path.is_dir()),
                    key=lambda path: len(path.parts),
                    reverse=True,
                ):
                    try:
                        directory.rmdir()
                    except OSError:
                        pass
                try:
                    root.rmdir()
                except OSError:
                    pass
    if current == requested or current is None:
        return
    agents_path = target / "AGENTS.md"
    if not agents_path.is_file() or agents_path.is_symlink():
        return
    text = agents_path.read_text(encoding="utf-8")
    updated = re.sub(
        r"(Modalita' installata:\s*`)(codex|claude|both)(`\.)",
        rf"\g<1>{requested}\g<3>",
        text,
        count=1,
        flags=re.IGNORECASE,
    )
    if updated != text:
        if not dry_run:
            agents_path.write_text(updated, encoding="utf-8")
        result.record("updated", agents_path)


def ensure_dir(path: Path, result: InstallResult, dry_run: bool) -> None:
    if path.is_symlink():
        raise ValueError(f"Directory standard collegata tramite symlink: {path}")
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"Directory standard occupata da un file: {path}")
        if path != result.target:
            result.record("existing", path)
        return
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)
    if path != result.target:
        result.record("created", path)


def ensure_text(path: Path, content: str, result: InstallResult, dry_run: bool) -> None:
    if path.exists() or path.is_symlink():
        result.record("existing", path)
        return
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
    result.record("created", path)


def ensure_managed_text(
    path: Path,
    content: str,
    result: InstallResult,
    dry_run: bool,
) -> None:
    expected = content.rstrip() + "\n"
    if path.exists() or path.is_symlink():
        if path.is_file() and not path.is_symlink():
            try:
                current = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                current = None
            if current == expected:
                result.record("existing", path)
                return
        result.record("existing", path)
        result.blockers.append(
            f"File di controllo LeaderAI modificato o illeggibile: "
            f"{path.relative_to(result.target).as_posix()}."
        )
        return
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8")
    result.record("created", path)


def _managed_guard_commands() -> set[str]:
    commands: set[str] = set()
    for template_name in ("CODEX_HOOKS.json", "CLAUDE_SETTINGS.json"):
        template = json.loads(
            (ROOT / "templates" / template_name).read_text(encoding="utf-8")
        )
        for group in template["hooks"]["Stop"]:
            for handler in group["hooks"]:
                command = handler.get("command")
                if isinstance(command, str):
                    commands.add(command)
    return commands


def _is_managed_guardiano(handler: object) -> bool:
    if not isinstance(handler, dict):
        return False
    return (
        handler.get("type") == "command"
        and handler.get("command") in _managed_guard_commands()
    )


def _load_json_object(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} non e' JSON valido: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} deve contenere un oggetto JSON: {path}")
    return value


def ensure_hooks_json(
    path: Path,
    content: str,
    result: InstallResult,
    dry_run: bool,
) -> None:
    try:
        desired = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Template hook LeaderAI non valido: {path.name}") from exc
    desired_hooks = desired.get("hooks")
    if not isinstance(desired_hooks, dict):
        raise ValueError(f"Template hook LeaderAI privo di hooks: {path.name}")

    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_file():
            result.record("existing", path)
            result.blockers.append(
                f"Configurazione hook non modificabile in sicurezza: "
                f"{path.relative_to(result.target).as_posix()}."
            )
            return
        try:
            current = _load_json_object(path, "Configurazione hook")
        except ValueError as exc:
            result.record("existing", path)
            result.blockers.append(str(exc))
            return
    else:
        current = {}

    merged = copy.deepcopy(current)
    current_hooks = merged.setdefault("hooks", {})
    if not isinstance(current_hooks, dict):
        result.record("existing", path)
        result.blockers.append(
            f"La chiave hooks non e' un oggetto in "
            f"{path.relative_to(result.target).as_posix()}."
        )
        return

    for event_name, desired_groups in desired_hooks.items():
        if not isinstance(desired_groups, list):
            raise ValueError(
                f"Template hook LeaderAI non valido per {event_name}: {path.name}"
            )
        existing_groups = current_hooks.get(event_name, [])
        if not isinstance(existing_groups, list):
            result.record("existing", path)
            result.blockers.append(
                f"L'evento {event_name} non e' una lista in "
                f"{path.relative_to(result.target).as_posix()}."
            )
            return

        cleaned_groups: list[dict] = []
        for group in existing_groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                result.record("existing", path)
                result.blockers.append(
                    f"Gruppo hook {event_name} non riconosciuto in "
                    f"{path.relative_to(result.target).as_posix()}."
                )
                return
            cleaned = copy.deepcopy(group)
            cleaned["hooks"] = [
                handler
                for handler in cleaned["hooks"]
                if not _is_managed_guardiano(handler)
            ]
            if cleaned["hooks"]:
                cleaned_groups.append(cleaned)

        cleaned_groups.extend(copy.deepcopy(desired_groups))
        current_hooks[event_name] = cleaned_groups

    rendered = json.dumps(merged, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.is_file() and path.read_text(encoding="utf-8") == rendered:
        result.record("existing", path)
        return
    status = "updated" if path.exists() else "created"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    result.record(status, path)


def _preflight_managed_rules(
    target: Path,
    rules: list[install_contract.TemplateRule],
    context: dict[str, str],
) -> list[str]:
    scratch = InstallResult(target=target)
    for rule in rules:
        path = target / rule.destination
        if rule.strategy == "managed_text":
            ensure_managed_text(
                path,
                read_template(rule.template, context),
                scratch,
                dry_run=True,
            )
        elif rule.strategy == "merge_hooks_json":
            ensure_hooks_json(
                path,
                read_template(rule.template, context),
                scratch,
                dry_run=True,
            )
    return scratch.blockers


def _claude_bridge_state(path: Path, agents_path: Path) -> str:
    if path.is_symlink():
        try:
            if path.resolve(strict=True) == agents_path.resolve(strict=True):
                return "valid-symlink"
        except (FileNotFoundError, RuntimeError):
            pass
        return "invalid"
    if not path.exists():
        return "missing"
    if path.is_file() and path.read_text(encoding="utf-8") == CLAUDE_BRIDGE:
        return "valid-file"
    return "invalid"


def _assert_safe_backup_family(source: Path) -> None:
    parent = source.parent
    if not parent.exists() or not parent.is_dir():
        return
    base_name = source.name + ".leaderai-backup"
    for candidate in parent.iterdir():
        if candidate.name == base_name or candidate.name.startswith(base_name + "."):
            if candidate.is_symlink():
                raise ValueError(
                    f"Backup LeaderAI collegato tramite symlink: {candidate}"
                )
            if not candidate.is_file():
                raise ValueError(
                    f"Backup LeaderAI occupato da una directory: {candidate}"
                )


def _backup_before_bridge_repair(
    source: Path,
    result: InstallResult,
    dry_run: bool,
) -> None:
    _assert_safe_backup_family(source)
    source_bytes = source.read_bytes()
    base = source.with_name(source.name + ".leaderai-backup")
    index = 1
    while True:
        candidate = base if index == 1 else base.with_name(f"{base.name}.{index}")
        if candidate.exists():
            if candidate.read_bytes() == source_bytes:
                return
            index += 1
            continue
        if not dry_run:
            shutil.copy2(source, candidate)
        result.record("created", candidate)
        return


def ensure_claude_bridge(
    path: Path,
    agents_path: Path,
    result: InstallResult,
    force: bool,
    dry_run: bool,
) -> str:
    state = _claude_bridge_state(path, agents_path)
    if state == "valid-file":
        result.record("existing", path)
        return state
    if state in {"invalid", "valid-symlink"} and not force:
        result.record("existing", path)
        result.blockers.append(
            "CLAUDE.md non e' il ponte regolare Windows-safe verso AGENTS.md. "
            "Rilanciare con --force per sostituire soltanto questo ponte."
        )
        return state
    status = "updated" if state in {"invalid", "valid-symlink"} else "created"
    if not dry_run:
        if path.is_file() and not path.is_symlink():
            _backup_before_bridge_repair(path, result, dry_run=False)
            path.unlink()
        elif path.is_symlink():
            path.unlink()
        elif path.exists():
            result.blockers.append(
                "CLAUDE.md esiste ma non e' un file riparabile automaticamente."
            )
            result.record("existing", path)
            return "invalid"
        path.write_text(CLAUDE_BRIDGE, encoding="utf-8")
    result.record(status, path)
    if state in {"invalid", "valid-symlink"}:
        result.warnings.append(
            "CLAUDE.md convertito nel ponte regolare; AGENTS.md e' rimasto intatto."
        )
        return "repaired"
    return "created"


def _assert_safe_layout(target: Path) -> None:
    root = Path(target.anchor)
    current = root
    for part in target.parts[1:-1]:
        current = current / part
        if current.is_symlink() and current.parent != root:
            raise ValueError(
                f"Directory antenata del target collegata tramite symlink: {current}"
            )
    nearest = target
    while not nearest.exists() and not nearest.is_symlink():
        parent = nearest.parent
        if parent == nearest:
            break
        nearest = parent
    if nearest != target and nearest.is_symlink():
        raise ValueError(
            f"Directory padre del target collegata tramite symlink: {nearest}"
        )
    if target.is_symlink():
        raise ValueError(f"Il target e' un symlink: {target}")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Il target non e' una cartella: {target}")
    _assert_safe_backup_family(target / "CLAUDE.md")
    for dirname in STANDARD_DIRS:
        path = target / dirname
        if path.is_symlink():
            raise ValueError(
                f"Directory standard collegata tramite symlink: {path}. "
                "Il setup si ferma prima di scrivere."
            )
        if path.exists() and not path.is_dir():
            raise ValueError(f"Directory standard occupata da un file: {path}")
    for filename in STANDARD_FILES:
        path = target / filename
        if path.is_symlink():
            if filename == "CLAUDE.md":
                continue
            raise ValueError(
                f"File standard collegato tramite symlink: {path}. "
                "Solo CLAUDE.md puo' essere un ponte verificato."
            )
        if path.exists() and not path.is_file():
            raise ValueError(f"File standard occupato da una directory: {path}")


def _required_gitignore_rules() -> list[str]:
    return [
        line.strip()
        for line in GITIGNORE_CONTENT.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def ensure_gitignore(path: Path, result: InstallResult, dry_run: bool) -> None:
    if path.exists():
        current = path.read_text(encoding="utf-8")
        required = set(_required_gitignore_rules())
        cleaned: list[str] = []
        inside_managed = False
        for line in current.splitlines():
            stripped = line.strip()
            if stripped == "# BEGIN LEADERAI SAFETY RULES":
                inside_managed = True
                continue
            if stripped == "# END LEADERAI SAFETY RULES":
                inside_managed = False
                continue
            if inside_managed:
                continue
            if stripped == "# Regole LeaderAI obbligatorie aggiunte dal setup":
                continue
            if stripped in required:
                continue
            cleaned.append(line)
        base = "\n".join(cleaned).rstrip()
        desired = (
            (base + "\n\n" if base else "")
            + GITIGNORE_CONTENT.rstrip()
            + "\n"
        )
        if current == desired:
            result.record("existing", path)
            return
        if not dry_run:
            path.write_text(desired, encoding="utf-8")
        result.record("updated", path)
        return
    if not dry_run:
        path.write_text(GITIGNORE_CONTENT, encoding="utf-8")
    result.record("created", path)


def ensure_git_repo(
    target: Path,
    result: InstallResult,
    *,
    new_install: bool,
    dry_run: bool,
) -> bool:
    if not new_install:
        if (target / ".git").is_dir():
            result.git_outcome = (
                "Git: repository gia' presente; target vivo, nessun commit automatico."
            )
        else:
            result.git_outcome = (
                "Git: target vivo senza repository; nessuna inizializzazione o commit automatico."
            )
            result.warnings.append(
                "Il target vivo non ha un repository Git; valutare il backup con il cliente."
            )
        return False
    if dry_run:
        result.git_outcome = (
            "Git: nuova installazione, inizializzazione e primo commit pianificati (dry-run)."
        )
        return False
    try:
        subprocess.run(
            ["git", "init"],
            cwd=str(target),
            check=True,
            capture_output=True,
        )
        result.git_outcome = (
            "Git: repository inizializzato; primo commit in preparazione."
        )
        return True
    except FileNotFoundError:
        result.git_outcome = (
            "Git: comando non trovato; repository e primo commit da creare a mano."
        )
        result.warnings.append("Git non disponibile durante la nuova installazione.")
    except subprocess.CalledProcessError:
        result.git_outcome = (
            "Git: inizializzazione fallita; repository e primo commit da completare a mano."
        )
        result.warnings.append("Inizializzazione Git fallita.")
    return False


def ensure_first_commit(
    target: Path,
    result: InstallResult,
    *,
    new_install: bool,
    git_ready: bool,
    dry_run: bool,
) -> None:
    if dry_run or not new_install or not git_ready:
        return
    candidates: list[str] = []
    for rel in dict.fromkeys(result.created + result.updated):
        path = target / rel
        if path.is_file() and not path.is_symlink() and not rel.startswith(".git/"):
            candidates.append(rel)
    if not candidates:
        result.git_outcome = "Git: nessun file LeaderAI da fotografare."
        return
    rendered_log_paths = [target / "logs" / "install-log.md"]
    committed_log_paths = [target / "logs" / "install-log.md"]
    rendered_outcome = result.git_outcome

    def refresh_outcome(after: str) -> None:
        nonlocal rendered_outcome
        before_text = rendered_outcome.removeprefix("Git: ")
        after_text = after.removeprefix("Git: ")
        for path in rendered_log_paths:
            if not path.is_file() or path.is_symlink():
                continue
            current = path.read_text(encoding="utf-8")
            updated = current.replace(before_text, after_text)
            if updated != current:
                path.write_text(updated, encoding="utf-8")
        rendered_outcome = after

    try:
        subprocess.run(
            ["git", "add", "--", *candidates],
            cwd=str(target),
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-c", "user.name=LeaderAI Setup",
                "-c", "user.email=setup@leaderai.local",
                "commit",
                "-m", "Cervello + Ecosistema LeaderAI: installazione iniziale",
            ],
            cwd=str(target),
            check=True,
            capture_output=True,
        )
        result.git_outcome = (
            "Git: repository inizializzato e primo commit creato con soli file LeaderAI."
        )
        refresh_outcome(result.git_outcome)
        final_log_paths = [
            path.relative_to(target).as_posix()
            for path in committed_log_paths
            if path.is_file() and not path.is_symlink()
        ]
        if final_log_paths:
            subprocess.run(
                ["git", "add", "--", *final_log_paths],
                cwd=str(target),
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "-c", "user.name=LeaderAI Setup",
                    "-c", "user.email=setup@leaderai.local",
                    "commit",
                    "--amend",
                    "--no-edit",
                ],
                cwd=str(target),
                check=True,
                capture_output=True,
            )
    except FileNotFoundError:
        result.git_outcome = "Git: comando non trovato; primo commit da fare a mano."
        result.warnings.append("Primo commit Git non creato.")
        refresh_outcome(result.git_outcome)
    except subprocess.CalledProcessError:
        result.git_outcome = "Git: primo commit fallito; completarlo a mano."
        result.warnings.append("Primo commit Git fallito.")
        refresh_outcome(result.git_outcome)


def _event_key(result: InstallResult, agent: str) -> str:
    payload = {
        "version": STANDARD_VERSION,
        "agent": agent,
        "created": result.created,
        "updated": result.updated,
        "removed": result.removed,
        "warnings": result.warnings,
        "blockers": result.blockers,
        "inspection_codes": result.inspection_codes,
        "git": result.git_outcome,
    }
    raw = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def ensure_event_log(
    path: Path,
    result: InstallResult,
    client: str,
    agent: str,
    event_key: str,
    stamp: str,
    dry_run: bool,
) -> None:
    marker = f"<!-- LEADERAI-SETUP-EVENT:{event_key} -->"
    if path.exists() and marker in path.read_text(encoding="utf-8"):
        result.record("existing", path)
        return
    lines = [
        marker,
        f"## {stamp}",
        f"- Client: {client}",
        f"- Agent: {agent}",
        f"- Standard version: {STANDARD_VERSION}",
        f"- Created: {', '.join(result.created) if result.created else 'none'}",
        f"- Updated: {', '.join(result.updated) if result.updated else 'none'}",
        f"- Warnings: {' | '.join(result.warnings) if result.warnings else 'none'}",
        f"- Blockers: {' | '.join(result.blockers) if result.blockers else 'none'}",
        f"- {result.git_outcome}",
    ]
    block = "\n".join(lines).rstrip() + "\n"
    if not path.exists():
        prefix = read_template("INSTALL_LOG.md", {}).rstrip() + "\n\n"
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(prefix + block, encoding="utf-8")
        result.record("created", path)
        return
    if not dry_run:
        with path.open("a", encoding="utf-8") as handle:
            handle.write("\n" + block)
    result.record("updated", path)


def _inspection_event_key(agent: str, inspection) -> str:
    payload = {
        "version": STANDARD_VERSION,
        "agent": agent,
        "installed_version": inspection.installed_version,
        "verdict": inspection.verdict,
        "findings": [
            {
                "code": item.code,
                "severity": item.severity,
                "path": item.path,
            }
            for item in inspection.findings
        ],
    }
    raw = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def _inspect_and_align(
    result: InstallResult,
    agent: str,
    claude_user_settings_path: Path | None,
    claude_user_instructions_path: Path | None = None,
    codex_user_instructions_path: Path | None = None,
):
    import ecosistema_inspector

    inspection = ecosistema_inspector.inspect_ecosystem(
        result.target,
        agent=agent,
        claude_user_settings_path=claude_user_settings_path,
        claude_user_instructions_path=claude_user_instructions_path,
        codex_user_instructions_path=codex_user_instructions_path,
    )
    result.target_verdict = inspection.verdict
    result.inspection_codes = [item.code for item in inspection.findings]
    for item in inspection.findings:
        message = f"Ispettore {item.code} ({item.path}): {item.detail}"
        destination = result.blockers if item.severity == "BLOCKER" else result.warnings
        if message not in destination:
            destination.append(message)
    if result.blockers:
        result.target_verdict = "NON PASSA"
    return inspection


def _finalize_blocked_target(
    result: InstallResult,
    client: str,
    agent: str,
    stamp: str,
    dry_run: bool,
    claude_user_settings_path: Path | None,
    claude_user_instructions_path: Path | None = None,
    codex_user_instructions_path: Path | None = None,
) -> InstallResult:
    if not result.target.is_dir() or dry_run:
        result.target_verdict = "NON PASSA"
        return result
    effects = install_contract.external_effects(CONTRACT, agent)
    if "git_baseline" in effects:
        ensure_git_repo(
            result.target,
            result,
            new_install=False,
            dry_run=dry_run,
        )
    _inspect_and_align(
        result,
        agent,
        claude_user_settings_path,
        claude_user_instructions_path,
        codex_user_instructions_path,
    )
    event_key = _event_key(result, agent)
    ensure_event_log(
        result.target / "logs" / "install-log.md",
        result,
        client,
        agent,
        event_key,
        stamp,
        dry_run,
    )
    return result


def run_setup(
    target: Path,
    client: str,
    agent: str,
    force: bool = False,
    dry_run: bool = False,
    *,
    claude_user_settings_path: Path | None = None,
    claude_user_instructions_path: Path | None = None,
    codex_user_instructions_path: Path | None = None,
    migrate_agent: bool = False,
) -> InstallResult:
    if agent not in SUPPORTED_AGENTS:
        allowed = ", ".join(sorted(SUPPORTED_AGENTS))
        raise ValueError(f"Agente non valido: {agent!r}. Valori ammessi: {allowed}.")

    target = target.expanduser().absolute()
    _assert_safe_layout(target)
    new_install = not target.exists() or not any(target.iterdir())
    if not new_install:
        if not (target / "AGENTS.md").is_file():
            raise ValueError(
                "Target gia' vivo senza Cervello riconosciuto: usa CHECKUP.md per censire "
                "e integrare l'ambiente; lo setup tecnico non impone il telaio a una casa esistente."
            )
    today = dt.datetime.now().strftime("%d/%m/%Y")
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context = {
        "client_name": client,
        "date": today,
        "agent": agent,
        "version": STANDARD_VERSION,
        "house_path": _portable_machine_path(target),
    }
    result = InstallResult(target=target)
    effects = install_contract.external_effects(CONTRACT, agent)
    settings_path = (
        claude_user_settings_path.expanduser().absolute()
        if claude_user_settings_path is not None
        else Path.home() / ".claude" / "settings.json"
    )

    if "claude_user_settings" in effects:
        try:
            _prepare_claude_user_settings(target, settings_path)
        except ValueError as exc:
            result.blockers.append(str(exc))
            return _finalize_blocked_target(
                result,
                client,
                agent,
                stamp,
                dry_run,
                settings_path,
                claude_user_instructions_path,
                codex_user_instructions_path,
            )

    for instructions_agent, instructions_path in (
        ("claude", claude_user_instructions_path),
        ("codex", codex_user_instructions_path),
    ):
        if (
            USER_INSTRUCTIONS[instructions_agent]["effect"] in effects
            and instructions_path is not None
        ):
            try:
                _prepare_user_instructions(
                    instructions_agent, target, instructions_path, context
                )
            except ValueError as exc:
                result.blockers.append(str(exc))
                return _finalize_blocked_target(
                    result,
                    client,
                    agent,
                    stamp,
                    dry_run,
                    settings_path,
                    claude_user_instructions_path,
                    codex_user_instructions_path,
                )

    installed_version = _installed_version(target) if target.exists() else None
    if installed_version is not None and installed_version != STANDARD_VERSION:
        result.blockers.append(
            f"Upgrade bloccato: installata {installed_version}, standard vivo "
            f"{STANDARD_VERSION}. Applicare una migrazione differenziale esplicita."
        )
        return _finalize_blocked_target(
            result,
            client,
            agent,
            stamp,
            dry_run,
            settings_path,
            claude_user_instructions_path,
            codex_user_instructions_path,
        )

    try:
        current_agent, remove_agents = _preflight_agent_transition(
            target,
            agent,
            context,
            migrate_agent,
        )
    except ValueError as exc:
        result.blockers.append(str(exc))
        return _finalize_blocked_target(
            result,
            client,
            agent,
            stamp,
            dry_run,
            settings_path,
            claude_user_instructions_path,
            codex_user_instructions_path,
        )

    rules = install_contract.template_rules(CONTRACT, agent)
    managed_blockers = _preflight_managed_rules(target, rules, context)
    if managed_blockers:
        result.blockers.extend(managed_blockers)
        result.target_verdict = "NON PASSA"
        if target.is_dir() and not dry_run:
            _inspect_and_align(result, agent, settings_path)
        return result

    bridge_state = _claude_bridge_state(target / "CLAUDE.md", target / "AGENTS.md")
    if bridge_state in {"invalid", "valid-symlink"} and not force:
        ensure_claude_bridge(
            target / "CLAUDE.md",
            target / "AGENTS.md",
            result,
            force=False,
            dry_run=dry_run,
        )
        return _finalize_blocked_target(
            result,
            client,
            agent,
            stamp,
            dry_run,
            settings_path,
            claude_user_instructions_path,
            codex_user_instructions_path,
        )

    ensure_dir(target, result, dry_run)
    _apply_agent_transition(
        target,
        agent,
        current_agent,
        remove_agents,
        result,
        dry_run,
    )
    for rule in rules:
        if rule.strategy == "event_log":
            continue
        parent = (target / rule.destination).parent
        if parent != target:
            ensure_dir(parent, result, dry_run)

    gitignore_rule = next(
        rule for rule in rules if rule.strategy == "merge_gitignore"
    )
    ensure_gitignore(target / gitignore_rule.destination, result, dry_run)
    git_ready = False
    if "git_baseline" in effects:
        git_ready = ensure_git_repo(
            target,
            result,
            new_install=new_install,
            dry_run=dry_run,
        )

    for rule in rules:
        path = target / rule.destination
        if rule.strategy in {"merge_gitignore", "event_log"}:
            continue
        if rule.strategy == "claude_bridge":
            ensure_claude_bridge(
                path,
                target / "AGENTS.md",
                result,
                force,
                dry_run,
            )
        elif rule.strategy == "managed_text":
            ensure_managed_text(
                path,
                read_template(rule.template, context),
                result,
                dry_run,
            )
        elif rule.strategy == "merge_hooks_json":
            ensure_hooks_json(
                path,
                read_template(rule.template, context),
                result,
                dry_run,
            )
        else:
            ensure_text(
                path,
                read_template(rule.template, context),
                result,
                dry_run,
            )

    if "claude_user_settings" in effects:
        ensure_claude_user_settings(
            target,
            settings_path,
            result,
            dry_run,
        )

    for instructions_agent, instructions_path in (
        ("claude", claude_user_instructions_path),
        ("codex", codex_user_instructions_path),
    ):
        if USER_INSTRUCTIONS[instructions_agent]["effect"] in effects:
            ensure_user_instructions(
                instructions_agent,
                target,
                instructions_path,
                context,
                result,
                dry_run,
            )

    changes_detected = bool(result.created or result.updated or result.removed)
    external_changed = any("aggiornate" in item for item in result.external_effects)
    event_needed = new_install or changes_detected or bool(
        result.warnings or result.blockers
    ) or external_changed
    if event_needed:
        event_key = _event_key(result, agent)
        ensure_event_log(
            target / "logs" / "install-log.md",
            result,
            client,
            agent,
            event_key,
            stamp,
            dry_run,
        )
    else:
        path = target / "logs" / "install-log.md"
        if path.exists():
            result.record("existing", path)

    ensure_first_commit(
        target,
        result,
        new_install=new_install,
        git_ready=git_ready,
        dry_run=dry_run,
    )

    if dry_run and not target.exists():
        result.target_verdict = "DA COLLAUDARE"
        return result

    _inspect_and_align(
        result,
        agent,
        settings_path,
        claude_user_instructions_path,
        codex_user_instructions_path,
    )

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monta Cervello + Ecosistema LeaderAI in una cartella cliente.")
    parser.add_argument("--target", required=True, help="Cartella cliente da creare o controllare.")
    parser.add_argument("--client", default="Cliente", help="Nome cliente.")
    parser.add_argument("--agent", choices=["codex", "claude", "both"], required=True)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ripara esclusivamente CLAUDE.md; gli altri file cliente restano intatti.",
    )
    parser.add_argument(
        "--claude-user-settings",
        help=(
            "Percorso user settings Claude letto su questa macchina. "
            "Default: ~/.claude/settings.json."
        ),
    )
    parser.add_argument(
        "--claude-user-instructions",
        help=(
            "Percorso delle istruzioni utente Claude Code letto su questa macchina "
            "(di norma ~/.claude/CLAUDE.md). Senza questo valore il setup non tocca la home."
        ),
    )
    parser.add_argument(
        "--codex-user-instructions",
        help=(
            "Percorso dell'AGENTS.md globale di Codex letto su questa macchina "
            "(di norma ~/.codex/AGENTS.md). Senza questo valore il setup non tocca la home."
        ),
    )
    parser.add_argument(
        "--migrate-agent",
        action="store_true",
        help=(
            "Migra esplicitamente codex<->claude rimuovendo soltanto file "
            "LeaderAI riconosciuti; dati non standard bloccano la migrazione."
        ),
    )
    parser.add_argument("--dry-run", action="store_true", help="Mostra cosa farebbe senza scrivere.")
    parser.add_argument("--quiet", action="store_true", help="Riduce output a una riga.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run_setup(
            Path(args.target),
            args.client,
            args.agent,
            args.force,
            args.dry_run,
            claude_user_settings_path=(
                Path(args.claude_user_settings)
                if args.claude_user_settings
                else None
            ),
            claude_user_instructions_path=(
                Path(args.claude_user_instructions)
                if args.claude_user_instructions
                else None
            ),
            codex_user_instructions_path=(
                Path(args.codex_user_instructions)
                if args.codex_user_instructions
                else None
            ),
            migrate_agent=args.migrate_agent,
        )
    except ValueError as exc:
        print(f"DA RIPARARE: {exc}")
        return 2

    if args.quiet:
        print(
            f"{result.target} | verdict={result.target_verdict or 'NON PASSA'} "
            f"created={len(result.created)} existing={len(result.existing)} "
            f"updated={len(result.updated)} removed={len(result.removed)}"
        )
        return 0 if result.target_verdict == "PASSA" else 2

    print(f"Target: {result.target}")
    print(f"Creati: {', '.join(result.created) if result.created else 'nessuno'}")
    print(f"Gia' presenti: {', '.join(result.existing) if result.existing else 'nessuno'}")
    print(f"Aggiornati: {', '.join(result.updated) if result.updated else 'nessuno'}")
    if result.decisions:
        print("Decisioni: " + "; ".join(result.decisions))
    print(f"Verdetto: {result.target_verdict or 'NON PASSA'}")
    return 0 if result.target_verdict == "PASSA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
