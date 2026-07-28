#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


CLAUDE_BRIDGE = "@AGENTS.md\n"
ROOT = Path(__file__).resolve().parent
STANDARD_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

REQUIRED_FILES = (
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "memory/MEMORY.md",
    "AGENT_CHAT.md",
    "logs/install-log.md",
    "ecosistema/FONTI.md",
    "ecosistema/ASSET.md",
    "ecosistema/PROCESSI.md",
    "ecosistema/LIMITI.md",
    "ecosistema/STANZA_AGENTS.md",
)

STANDARD_DIRS = {
    "memory",
    "logs",
    "ecosistema",
    ".codex",
    ".claude",
    ".agents",
    ".git",
    ".secrets",
}

ALLOWED_ROOT_FILES = {
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "AGENT_CHAT.md",
    "REPORT_FINALE.md",
}

GENERIC_NAMES = {
    "documenti",
    "documents",
    "docs",
    "output",
    "outputs",
    "export",
    "exports",
    "varie",
    "misc",
    "temp",
    "tmp",
    "nuova cartella",
    "new folder",
}

ROOM_REQUIRED_TERMS = (
    "stato corrente e prossimo passo",
    "scopo",
    "responsabilita business",
    "dentro",
    "fonti",
    "output",
    "capacita",
    "a monte",
    "a valle",
    "dove scrivere",
    "fonte business editabile",
)

UNPROVEN_ROOM_RESPONSIBILITY_TERMS = (
    "{{",
    "da definire",
    "da compilare",
    "non applicabile",
)

CREDENTIAL_NAME_TERMS = {
    "password",
    "passwd",
    "credential",
    "credenzial",
    "secret",
    "segreto",
    "token",
}

COMMUNICATION_CONFIG_TERMS = {
    "posta",
    "mail",
    "email",
    "smtp",
    "pec",
    "oauth",
    "auth",
}

SENSITIVE_ASSET_FAMILIES = {
    "firma": {"firma", "signature"},
    "timbro": {"timbro", "stamp"},
    "sigillo": {"sigillo", "seal"},
}

SOURCE_CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx"}
DOCUMENT_GENERATOR_HINTS = {
    "docx",
    "document",
    "pdf",
    "reportlab",
    "scheda",
    "stampa",
    "weasyprint",
}


@dataclass(frozen=True)
class Room:
    name: str
    path: str
    purpose: str


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    detail: str


@dataclass
class Inspection:
    target: str
    rooms: list[Room]
    findings: list[Finding]
    standard_version: str = STANDARD_VERSION
    installed_version: str | None = None

    @property
    def verdict(self) -> str:
        if any(item.severity == "BLOCKER" for item in self.findings):
            return "NON PASSA"
        if self.findings:
            return "PASSA CON ATTENZIONE"
        return "PASSA"

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "verdict": self.verdict,
            "standard_version": self.standard_version,
            "installed_version": self.installed_version,
            "rooms": [asdict(room) for room in self.rooms],
            "findings": [asdict(item) for item in self.findings],
        }


def _normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _table_cells(line: str) -> list[str]:
    if not line.lstrip().startswith("|"):
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _room_from_cell(cell: str, purpose: str) -> Room | None:
    link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", cell)
    if link:
        name, path = link.groups()
    else:
        value = cell.strip("`").strip()
        if not value or _normalized(value) in {"stanza", "da censire"}:
            return None
        name = value
        path = value
    path = path.replace("\\", "/").strip("/")
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return Room(name=name, path="", purpose=purpose)
    return Room(name=name, path=path, purpose=purpose)


def parse_room_registry(agents_text: str) -> list[Room]:
    marker = "### Registro delle stanze"
    if marker not in agents_text:
        return []
    section = agents_text.split(marker, 1)[1]
    section = re.split(r"\n##\s", section, maxsplit=1)[0]
    rooms: list[Room] = []
    for line in section.splitlines():
        cells = _table_cells(line)
        if len(cells) < 2:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        room = _room_from_cell(cells[0], cells[1])
        if room is not None:
            rooms.append(room)
    return rooms


def _is_empty_dir(path: Path) -> bool:
    try:
        return not any(path.iterdir())
    except OSError:
        return False


def _active_agents(target: Path, requested: str) -> set[str]:
    if requested != "auto":
        return {"codex", "claude"} if requested == "both" else {requested}
    active: set[str] = set()
    if (target / ".codex" / "README.md").is_file():
        active.add("codex")
    if (target / ".claude" / "README.md").is_file():
        active.add("claude")
    return active


def _extract_installed_version(target: Path) -> str | None:
    candidates = (
        (
            target / "AGENTS.md",
            (
                r"Versione standard applicata:\s*`?(\d+\.\d+\.\d+)",
                r"standard\s+(\d+\.\d+\.\d+)",
            ),
        ),
        (
            target / "logs" / "install-log.md",
            (r"Standard version:\s*(\d+\.\d+\.\d+)",),
        ),
        (
            target / "REPORT_FINALE.md",
            (
                r"Versione:\s*(\d+\.\d+\.\d+)",
                r"standard\s+(\d+\.\d+\.\d+)",
            ),
        ),
    )
    for path, patterns in candidates:
        if not path.is_file() or path.is_symlink():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(1)
    return None


def _git_path_state(target: Path, rel: str) -> tuple[bool, bool]:
    if not (target / ".git").is_dir():
        return False, False
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", rel],
            cwd=str(target),
            capture_output=True,
            text=True,
            check=False,
        ).returncode == 0
        history = bool(
            subprocess.run(
                ["git", "log", "--all", "--format=%H", "--", rel],
                cwd=str(target),
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
        )
    except OSError:
        return False, False
    return tracked, history


def _git_history_paths(target: Path) -> set[str]:
    if not (target / ".git").is_dir():
        return set()
    try:
        output = subprocess.run(
            ["git", "log", "--all", "--name-only", "--pretty=format:"],
            cwd=str(target),
            capture_output=True,
            text=True,
            check=False,
        ).stdout
    except OSError:
        return set()
    return {
        line.strip().replace("\\", "/")
        for line in output.splitlines()
        if line.strip()
    }


def _iter_files(target: Path, *, include_protected: bool = False):
    for path in target.rglob("*"):
        try:
            rel = path.relative_to(target)
        except ValueError:
            continue
        if ".git" in rel.parts:
            continue
        if not include_protected and ".secrets" in rel.parts:
            continue
        if path.is_symlink() or not path.is_file():
            continue
        yield rel, path


def _is_credential_candidate(rel: Path) -> bool:
    normalized = _normalized(rel.as_posix())
    name = _normalized(rel.name)
    if any(term in normalized for term in CREDENTIAL_NAME_TERMS):
        return True
    config_suffix = rel.suffix.casefold() in {".json", ".yaml", ".yml", ".toml", ".ini"}
    return (
        config_suffix
        and "config" in name
        and any(term in normalized for term in COMMUNICATION_CONFIG_TERMS)
    )


def _sensitive_asset_term(rel: Path) -> str | None:
    normalized = _normalized(rel.name)
    for family, aliases in SENSITIVE_ASSET_FAMILIES.items():
        if any(alias in normalized for alias in aliases):
            return family
    return None


def _hardcoded_business_string(path: Path, text: str) -> bool:
    if path.suffix.casefold() == ".py":
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return False
        strings = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        ]
    else:
        strings = re.findall(r"""(?s)(?:"([^"\n]{60,})"|'([^'\n]{60,})')""", text)
        strings = [left or right for left, right in strings]
    for value in strings:
        compact = " ".join(value.split())
        if len(compact) >= 60 and len(compact.split()) >= 8:
            return True
    return False


def _business_source_findings(target: Path, room_path: Path) -> list[Finding]:
    generator_files: list[tuple[Path, str]] = []
    for rel, path in _iter_files(room_path):
        if rel.suffix.casefold() not in SOURCE_CODE_SUFFIXES:
            continue
        if _is_credential_candidate(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        signal = _normalized(rel.as_posix() + "\n" + text)
        if any(hint in signal for hint in DOCUMENT_GENERATOR_HINTS):
            generator_files.append((path, text))
    if not generator_files:
        return []

    room_agents = room_path / "AGENTS.md"
    map_text = (
        _normalized(room_agents.read_text(encoding="utf-8"))
        if room_agents.is_file()
        else ""
    )
    source_section = ""
    match = re.search(
        r"(?ms)^##\s+fonte business editabile\s*$\s*(.*?)(?=^##\s|\Z)",
        map_text,
    )
    if match:
        source_section = match.group(1).strip()
    source_declared = bool(source_section) and not any(
        token in source_section
        for token in (
            "{{",
            "da definire",
            "nessuna",
            "non dichiarata",
            "non applicabile",
        )
    )

    findings: list[Finding] = []
    if not source_declared:
        findings.append(
            Finding(
                "BUSINESS_SOURCE_UNDECLARED",
                "BLOCKER",
                room_path.relative_to(target).as_posix(),
                "La stanza genera documenti ma non dichiara una fonte business "
                "editabile esterna al codice.",
            )
        )
    for path, text in generator_files:
        if _hardcoded_business_string(path, text):
            findings.append(
                Finding(
                    "BUSINESS_CONTENT_HARDCODED_RISK",
                    "BLOCKER",
                    path.relative_to(target).as_posix(),
                    "Il generatore contiene testo umano esteso nel codice: "
                    "portarlo nella fonte business dichiarata e mantenere PDF/Word "
                    "come derivati.",
                )
            )
    return findings


def _room_business_responsibility_is_proven(content: str) -> bool:
    match = re.search(
        r"(?ms)^##\s+responsabilita business\s*$\s*(.*?)(?=^##\s|\Z)",
        content,
    )
    if not match:
        return False
    section = match.group(1).strip()
    if not section:
        return False
    return not any(term in section for term in UNPROVEN_ROOM_RESPONSIBILITY_TERMS)


def _project_control_issue(path: Path) -> str | None:
    text = _normalized(path.read_text(encoding="utf-8"))
    headings = [
        (match.start(), match.group(1).strip())
        for match in re.finditer(r"(?m)^#{1,4}\s+(.+)$", text)
    ]
    if not headings:
        return "Mancano intestazioni per stato corrente, prossimo passo e scadenze."

    def heading_position(term: str) -> int | None:
        return next((position for position, title in headings if term in title), None)

    state = heading_position("stato corrente")
    next_step = heading_position("prossimo")
    deadlines = heading_position("scaden")
    diary = heading_position("diario")
    missing = [
        label
        for label, position in (
            ("stato corrente", state),
            ("prossimo passo", next_step),
            ("scadenze", deadlines),
        )
        if position is None
    ]
    if missing:
        return "Sezioni mancanti in testa: " + ", ".join(missing) + "."
    if diary is not None and any(
        position is not None and position > diary
        for position in (state, next_step, deadlines)
    ):
        return "Stato, prossimo passo e scadenze devono precedere il diario."
    return None


def inspect_ecosystem(target: Path, agent: str = "auto") -> Inspection:
    target = target.expanduser().resolve()
    findings: list[Finding] = []
    if not target.is_dir():
        return Inspection(
            target=str(target),
            rooms=[],
            findings=[
                Finding(
                    "TARGET_NOT_FOUND",
                    "BLOCKER",
                    ".",
                    "La cartella viva non esiste o non e' una directory.",
                )
            ],
        )

    installed_version = _extract_installed_version(target)
    if installed_version is None:
        findings.append(
            Finding(
                "INSTALLED_VERSION_UNKNOWN",
                "BLOCKER",
                "AGENTS.md",
                "Versione installata non trovata: il checkup non puo' "
                f"confrontarla con VERSION corrente {STANDARD_VERSION}.",
            )
        )
    elif installed_version != STANDARD_VERSION:
        findings.append(
            Finding(
                "STANDARD_VERSION_OUTDATED",
                "BLOCKER",
                "AGENTS.md",
                f"Installata {installed_version}; standard vivo letto da "
                f"VERSION {STANDARD_VERSION}. Applicare le differenze e "
                "ripetere il checkup.",
            )
        )

    for rel in REQUIRED_FILES:
        path = target / rel
        if not path.is_file():
            findings.append(
                Finding(
                    "MISSING_STANDARD_FILE",
                    "BLOCKER",
                    rel,
                    "File obbligatorio dello standard assente.",
                )
            )

    root_bridge = target / "CLAUDE.md"
    if root_bridge.is_file() and root_bridge.read_text(encoding="utf-8") != CLAUDE_BRIDGE:
        findings.append(
            Finding(
                "INVALID_ROOT_BRIDGE",
                "BLOCKER",
                "CLAUDE.md",
                "Il ponte deve contenere soltanto @AGENTS.md.",
            )
        )

    report_path = target / "REPORT_FINALE.md"
    if report_path.is_file():
        report = report_path.read_text(encoding="utf-8")
        normalized_report = _normalized(report)
        if "valido al:" not in normalized_report or "stato missione:" not in normalized_report:
            findings.append(
                Finding(
                    "STALE_REPORT",
                    "BLOCKER",
                    "REPORT_FINALE.md",
                    "Report senza data di validita' o stato missione: non puo' "
                    "essere usato come stato corrente.",
                )
            )
        tracked, _history = _git_path_state(target, "REPORT_FINALE.md")
        if tracked:
            findings.append(
                Finding(
                    "TEMP_REPORT_IN_GIT",
                    "BLOCKER",
                    "REPORT_FINALE.md",
                    "L'output temporaneo e' ancora tracciato in Git: promuovere "
                    "i fatti nelle fonti proprietarie e rimuoverlo dall'indice.",
                )
            )

    agents_path = target / "AGENTS.md"
    agents_text = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
    rooms = parse_room_registry(agents_text)

    seen_paths: set[str] = set()
    purposes: dict[str, str] = {}
    for room in rooms:
        if not room.path:
            findings.append(
                Finding(
                    "INVALID_ROOM_PATH",
                    "BLOCKER",
                    room.name,
                    "Il percorso della stanza non e' relativo e sicuro.",
                )
            )
            continue
        if room.path in seen_paths:
            findings.append(
                Finding(
                    "DUPLICATE_ROOM_PATH",
                    "BLOCKER",
                    room.path,
                    "La stessa stanza compare piu' volte nella mappa madre.",
                )
            )
        seen_paths.add(room.path)

        purpose_key = _normalized(room.purpose).strip()
        if purpose_key and purpose_key not in {"-", "da definire dal lavoro reale"}:
            if purpose_key in purposes:
                findings.append(
                    Finding(
                        "DUPLICATE_ROOM_PURPOSE",
                        "BLOCKER",
                        room.path,
                        f"Funzione gia' dichiarata dalla stanza {purposes[purpose_key]}.",
                    )
                )
            else:
                purposes[purpose_key] = room.path

        room_path = target / room.path
        if not room_path.is_dir():
            findings.append(
                Finding(
                    "ROOM_PATH_MISSING",
                    "BLOCKER",
                    room.path,
                    "La mappa madre dichiara una stanza che non esiste.",
                )
            )
            continue

        room_agents = room_path / "AGENTS.md"
        room_claude = room_path / "CLAUDE.md"
        if not room_agents.is_file():
            findings.append(
                Finding(
                    "ROOM_AGENTS_MISSING",
                    "BLOCKER",
                    f"{room.path}/AGENTS.md",
                    "La stanza non ha la propria mappa locale.",
                )
            )
        else:
            content = _normalized(room_agents.read_text(encoding="utf-8"))
            missing_terms = [term for term in ROOM_REQUIRED_TERMS if term not in content]
            if missing_terms:
                findings.append(
                    Finding(
                        "ROOM_MAP_INCOMPLETE",
                        "BLOCKER",
                        f"{room.path}/AGENTS.md",
                        "Sezioni mancanti: " + ", ".join(missing_terms) + ".",
                    )
                )
            elif not _room_business_responsibility_is_proven(content):
                findings.append(
                    Finding(
                        "ROOM_BUSINESS_RESPONSIBILITY_UNPROVEN",
                        "BLOCKER",
                        f"{room.path}/AGENTS.md",
                        "La mappa non prova una responsabilita' business reale "
                        "con stato e decisioni: script, modelli e output non "
                        "bastano a dimostrare una stanza.",
                    )
                )
        if not room_claude.is_file():
            findings.append(
                Finding(
                    "ROOM_CLAUDE_MISSING",
                    "BLOCKER",
                    f"{room.path}/CLAUDE.md",
                    "La stanza non ha il ponte verso AGENTS.md.",
                )
            )
        elif room_claude.read_text(encoding="utf-8") != CLAUDE_BRIDGE:
            findings.append(
                Finding(
                    "ROOM_CLAUDE_INVALID",
                    "BLOCKER",
                    f"{room.path}/CLAUDE.md",
                    "Il ponte deve contenere soltanto @AGENTS.md.",
                )
            )

    declared_top_levels = {Path(room.path).parts[0] for room in rooms if room.path}
    for child in sorted(target.iterdir(), key=lambda item: item.name.casefold()):
        if not child.is_dir() or child.name in STANDARD_DIRS or child.name.startswith("."):
            continue
        if child.name not in declared_top_levels:
            findings.append(
                Finding(
                    "UNCLASSIFIED_DIR",
                    "BLOCKER",
                    child.name,
                    "Cartella visibile senza classe, proprietario o collegamento nella mappa madre.",
                )
            )
        if _normalized(child.name) in GENERIC_NAMES:
            findings.append(
                Finding(
                    "GENERIC_DIR",
                    "BLOCKER",
                    child.name,
                    "Nome generico: classificare i contenuti e portarli nella stanza proprietaria.",
                )
            )
        if _is_empty_dir(child):
            findings.append(
                Finding(
                    "EMPTY_DIR",
                    "BLOCKER",
                    child.name,
                    "Cartella vuota: non costituisce una stanza viva.",
                )
            )
        findings.extend(_business_source_findings(target, child))

    for child in sorted(target.iterdir(), key=lambda item: item.name.casefold()):
        if not child.is_file() or child.name.startswith("."):
            continue
        if child.name in ALLOWED_ROOT_FILES or ".leaderai-backup" in child.name:
            continue
        findings.append(
            Finding(
                "UNOWNED_ROOT_FILE",
                "BLOCKER",
                child.name,
                "File sciolto nella home senza stanza proprietaria.",
            )
        )

    active_agents = _active_agents(target, agent)
    if not active_agents:
        findings.append(
            Finding(
                "ACTIVE_AGENT_UNKNOWN",
                "BLOCKER",
                ".",
                "Impossibile determinare l'agente attivo.",
            )
        )
    skill_paths = {
        "codex": ".agents/skills/ispettore-ecosistema/SKILL.md",
        "claude": ".claude/skills/ispettore-ecosistema/SKILL.md",
    }
    for active_agent in sorted(active_agents):
        rel = skill_paths[active_agent]
        path = target / rel
        if not path.is_file():
            findings.append(
                Finding(
                    "INSPECTOR_SKILL_MISSING",
                    "BLOCKER",
                    rel,
                    f"Ispettore non richiamabile da {active_agent}.",
                )
            )
        else:
            content = path.read_text(encoding="utf-8")
            if "CHECKUP.md" not in content or "ispettore-ecosistema" not in content:
                findings.append(
                    Finding(
                        "INSPECTOR_SKILL_INVALID",
                        "BLOCKER",
                        rel,
                        "La skill non punta alla procedura unica CHECKUP.md.",
                    )
                )

    if "claude" in active_agents:
        settings_path = target / ".claude" / "settings.local.json"
        desired_memory = (target / "memory").resolve()
        if not settings_path.is_file():
            findings.append(
                Finding(
                    "CLAUDE_MEMORY_ROUTE_MISSING",
                    "BLOCKER",
                    ".claude/settings.local.json",
                    "Claude Code non punta auto memory alla memory/ della casa; "
                    "verificare /memory e riconciliare l'eventuale memoria esterna.",
                )
            )
        else:
            try:
                settings = json.loads(settings_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                settings = None
            raw_memory = (
                settings.get("autoMemoryDirectory")
                if isinstance(settings, dict)
                else None
            )
            if not isinstance(raw_memory, str):
                findings.append(
                    Finding(
                        "CLAUDE_MEMORY_ROUTE_INVALID",
                        "BLOCKER",
                        ".claude/settings.local.json",
                        "autoMemoryDirectory assente o non valido.",
                    )
                )
            else:
                configured = Path(raw_memory).expanduser()
                if not configured.is_absolute():
                    findings.append(
                        Finding(
                            "CLAUDE_MEMORY_ROUTE_INVALID",
                            "BLOCKER",
                            ".claude/settings.local.json",
                            "autoMemoryDirectory deve essere assoluto o iniziare con ~/.",
                        )
                    )
                elif configured.resolve() != desired_memory:
                    findings.append(
                        Finding(
                            "CLAUDE_MEMORY_DIVERGED",
                            "BLOCKER",
                            ".claude/settings.local.json",
                            "Auto memory punta fuori dalla memory/ della casa: "
                            "confrontare e unire le due memorie prima di cambiare il percorso.",
                        )
                    )

    current_credential_paths: set[str] = set()
    for rel, _path in _iter_files(target):
        if _is_credential_candidate(rel):
            current_credential_paths.add(rel.as_posix())
            tracked, history = _git_path_state(target, rel.as_posix())
            if tracked or history:
                findings.append(
                    Finding(
                        "CREDENTIAL_EXPOSURE_NOT_EXCLUDED",
                        "BLOCKER",
                        rel.as_posix(),
                        "Configurazione credenziali fuori .secrets/ e presente "
                        "nell'indice o nella history Git: non leggere il "
                        "contenuto; bloccare l'uso e proporre rotazione.",
                    )
                )
            else:
                findings.append(
                    Finding(
                        "CREDENTIAL_FILE_OUTSIDE_SECRETS",
                        "BLOCKER",
                        rel.as_posix(),
                        "Configurazione credenziali fuori .secrets/. La history "
                        "del percorso non mostra commit; spostare e riprovare.",
                    )
                )

    for historical_path in sorted(_git_history_paths(target)):
        rel = Path(historical_path)
        if (
            historical_path in current_credential_paths
            or ".secrets" in rel.parts
            or not _is_credential_candidate(rel)
        ):
            continue
        findings.append(
            Finding(
                "CREDENTIAL_EXPOSURE_NOT_EXCLUDED",
                "BLOCKER",
                historical_path,
                "Configurazione credenziali non piu' presente ma visibile nella "
                "history Git: non leggere il contenuto; bloccare l'uso e "
                "proporre rotazione finche' l'esposizione non e' esclusa.",
            )
        )

    asset_registry_path = target / "ecosistema" / "ASSET.md"
    asset_registry = (
        _normalized(asset_registry_path.read_text(encoding="utf-8"))
        if asset_registry_path.is_file()
        else ""
    )
    registered_sensitive_assets = {
        family
        for line in asset_registry.splitlines()
        if line.lstrip().startswith("|")
        for family, aliases in SENSITIVE_ASSET_FAMILIES.items()
        if any(alias in line for alias in aliases)
    }
    for rel, _path in _iter_files(target, include_protected=True):
        term = _sensitive_asset_term(rel)
        if term is None:
            continue
        if ".secrets" not in rel.parts:
            findings.append(
                Finding(
                    "SENSITIVE_ASSET_OUTSIDE_PROTECTED",
                    "BLOCKER",
                    rel.as_posix(),
                    "Firma, timbro o sigillo fuori dalla casa protetta e fuori "
                    "Git richiesta dallo standard.",
                )
            )
        if term not in registered_sensitive_assets:
            findings.append(
                Finding(
                    "SENSITIVE_ASSET_UNREGISTERED",
                    "BLOCKER",
                    rel.as_posix(),
                    "Asset ad alto rischio non registrato in ASSET.md con "
                    "metadati, limiti e conferma umana.",
                )
            )

    for rel, path in _iter_files(target):
        if rel.name.casefold() != "progetto.md":
            continue
        issue = _project_control_issue(path)
        if issue:
            findings.append(
                Finding(
                    "PROJECT_CONTROL_OUT_OF_ORDER",
                    "BLOCKER",
                    rel.as_posix(),
                    issue,
                )
            )

    return Inspection(
        target=str(target),
        rooms=rooms,
        findings=findings,
        installed_version=installed_version,
    )


def _markdown(inspection: Inspection) -> str:
    lines = [
        "# Ispettore Ecosistema",
        "",
        f"- Cartella viva: `{inspection.target}`",
        f"- Standard vivo: `{inspection.standard_version}`",
        f"- Versione installata: `{inspection.installed_version or 'NON TROVATA'}`",
        f"- Verdetto: **{inspection.verdict}**",
        "",
        "| Gravita | Codice | Percorso | Evidenza |",
        "|---|---|---|---|",
    ]
    if not inspection.findings:
        lines.append("| - | OK | - | Nessuno scostamento meccanico |")
    else:
        for item in inspection.findings:
            detail = item.detail.replace("|", "/")
            lines.append(
                f"| {item.severity} | {item.code} | `{item.path}` | {detail} |"
            )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Controllo strutturale in sola lettura del Cervello + Ecosistema."
    )
    parser.add_argument("--target", required=True, help="Cartella viva da ispezionare.")
    parser.add_argument(
        "--agent",
        choices=("auto", "codex", "claude", "both"),
        default="auto",
    )
    parser.add_argument("--json", action="store_true", help="Emette JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inspection = inspect_ecosystem(Path(args.target), args.agent)
    if args.json:
        print(json.dumps(inspection.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_markdown(inspection), end="")
    return 0 if inspection.verdict == "PASSA" else 1


if __name__ == "__main__":
    raise SystemExit(main())
