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

import install_contract


CLAUDE_BRIDGE = "@AGENTS.md\n"
ROOT = Path(__file__).resolve().parent
STANDARD_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
CONTRACT = install_contract.CONTRACT
ORGANIZATION = install_contract.organization_policy(CONTRACT)
MARKDOWN_HYGIENE = install_contract.markdown_hygiene_policy(CONTRACT)
GITIGNORE_REQUIRED_RULES = tuple(
    line.strip()
    for line in (ROOT / "templates" / "GITIGNORE.txt")
    .read_text(encoding="utf-8")
    .splitlines()
    if line.strip() and not line.lstrip().startswith("#")
)

REQUIRED_FILES = tuple(CONTRACT["common"]["required"])

STANDARD_DIRS = {
    Path(rel).parts[0]
    for agent_name in CONTRACT["supported_agents"]
    for rel in (
        install_contract.required_paths(CONTRACT, agent_name)
        + [
            rule.destination
            for rule in install_contract.template_rules(CONTRACT, agent_name)
        ]
    )
    if len(Path(rel).parts) > 1
} | {".git", ".secrets"}

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
    "amministratore del settore",
    "boss dell'ecosistema",
    "riporta al boss",
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
    administrator: str
    reports_to: str


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


def _room_from_cell(
    cell: str,
    purpose: str,
    administrator: str,
    reports_to: str,
) -> Room | None:
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
        return Room(
            name=name,
            path="",
            purpose=purpose,
            administrator=administrator,
            reports_to=reports_to,
        )
    return Room(
        name=name,
        path=path,
        purpose=purpose,
        administrator=administrator,
        reports_to=reports_to,
    )


def parse_room_registry(agents_text: str) -> list[Room]:
    marker = "### Registro delle stanze"
    if marker not in agents_text:
        return []
    section = agents_text.split(marker, 1)[1]
    section = re.split(r"\n#{2,3}\s", section, maxsplit=1)[0]
    rooms: list[Room] = []
    for line in section.splitlines():
        cells = _table_cells(line)
        if len(cells) < 2:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        administrator = cells[8].strip("`").strip() if len(cells) > 8 else ""
        reports_to = cells[9].strip("`").strip() if len(cells) > 9 else ""
        room = _room_from_cell(cells[0], cells[1], administrator, reports_to)
        if room is not None:
            rooms.append(room)
    return rooms


def parse_root_owned_registry(agents_text: str) -> set[str]:
    marker = "### Elementi posseduti direttamente dalla cartella madre"
    if marker not in agents_text:
        return set()
    section = agents_text.split(marker, 1)[1]
    section = re.split(r"\n#{2,3}\s", section, maxsplit=1)[0]
    paths: set[str] = set()
    for line in section.splitlines():
        cells = _table_cells(line)
        if len(cells) < 2:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        raw = cells[0].strip("`").strip().replace("\\", "/").strip("/")
        if _normalized(raw) in {"percorso", "da censire"}:
            continue
        candidate = Path(raw)
        if raw and not candidate.is_absolute() and ".." not in candidate.parts:
            paths.add(raw)
    return paths


def _canonical_memory_path(target: Path, agents_text: str) -> Path:
    match = re.search(
        r"Memoria canonica:\s*`([^`]+)`",
        agents_text,
        flags=re.IGNORECASE,
    )
    if not match:
        return (target / "memory").resolve()
    raw = match.group(1).strip().replace("\\", "/")
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = target / candidate
    return candidate.resolve()


def _is_empty_dir(path: Path) -> bool:
    try:
        return not any(path.iterdir())
    except OSError:
        return False


def _symlink_component(target: Path, relative: str | Path) -> Path | None:
    current = target
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            return current
    return None


def _active_agents(target: Path, requested: str) -> set[str]:
    if requested != "auto":
        return {"codex", "claude"} if requested == "both" else {requested}
    return install_contract.detected_agents(CONTRACT, target)


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


def _is_inside_home(path: Path) -> bool:
    """Il percorso sta dentro la home dell'utente corrente?

    Serve a riconoscere i percorsi che inchiodano il segmento utente: sono
    quelli che, replicati su un'altra postazione del cliente, puntano a una
    cartella inesistente e rompono la memoria in silenzio.
    """
    try:
        home = Path.home().resolve()
    except (OSError, RuntimeError):
        return False
    try:
        resolved = path.expanduser().resolve()
    except (OSError, RuntimeError):
        return False
    return resolved == home or home in resolved.parents


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


def _markdown_hygiene_findings(target: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel, path in _iter_files(target):
        if rel.suffix.casefold() != ".md":
            continue
        try:
            size = path.stat().st_size
            lines = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            continue

        is_router = rel.name.casefold() in MARKDOWN_HYGIENE.router_names
        max_lines = (
            MARKDOWN_HYGIENE.router_max_lines
            if is_router
            else MARKDOWN_HYGIENE.document_review_lines
        )
        max_bytes = (
            MARKDOWN_HYGIENE.router_max_bytes
            if is_router
            else MARKDOWN_HYGIENE.document_review_bytes
        )
        if lines <= max_lines and size <= max_bytes:
            continue

        if is_router:
            findings.append(
                Finding(
                    "MARKDOWN_ROUTER_TOO_LARGE",
                    "BLOCKER",
                    rel.as_posix(),
                    f"Mappa o indice troppo grande ({lines} righe, {size} byte; "
                    f"limite {max_lines} righe/{max_bytes} byte): spostare i "
                    "dettagli nelle fonti proprietarie gia' esistenti e lasciare "
                    "qui soltanto indice, regole di ingresso e collegamenti.",
                )
            )
        else:
            findings.append(
                Finding(
                    "MARKDOWN_DOCUMENT_REVIEW",
                    "ATTENZIONE",
                    rel.as_posix(),
                    f"Documento esteso ({lines} righe, {size} byte; soglia di "
                    f"revisione {max_lines} righe/{max_bytes} byte): verificare "
                    "che risponda a una sola domanda e non duplichi una fonte viva.",
                )
            )
    return findings


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


def inspect_ecosystem(
    target: Path,
    agent: str = "auto",
    claude_user_settings_path: Path | None = None,
) -> Inspection:
    requested_target = target.expanduser()
    if requested_target.is_symlink():
        return Inspection(
            target=str(requested_target),
            rooms=[],
            findings=[
                Finding(
                    "TARGET_SYMLINK",
                    "BLOCKER",
                    ".",
                    "La cartella madre non puo' essere un collegamento simbolico.",
                )
            ],
        )
    target = requested_target.resolve()
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

    agents_path = target / "AGENTS.md"
    agents_text = (
        agents_path.read_text(encoding="utf-8")
        if agents_path.is_file() and not agents_path.is_symlink()
        else ""
    )
    normalized_agents = _normalized(agents_text)
    if (
        _normalized(ORGANIZATION.root_role) not in normalized_agents
        or "governa l'organigramma" not in normalized_agents
    ):
        findings.append(
            Finding(
                "ECOSYSTEM_BOSS_MISSING",
                "BLOCKER",
                "AGENTS.md",
                "La mappa madre non dichiara il Boss dell'Ecosistema che "
                "governa l'organigramma e coordina gli amministratori di settore.",
            )
        )
    declared_mode = install_contract.declared_agent(agents_text)
    detected_agents = install_contract.detected_agents(CONTRACT, target)
    detected_mode = (
        "both"
        if detected_agents == {"codex", "claude"}
        else (next(iter(detected_agents)) if len(detected_agents) == 1 else None)
    )
    requested_mode = agent if agent != "auto" else (declared_mode or detected_mode)
    if requested_mode is None:
        findings.append(
            Finding(
                "ACTIVE_AGENT_UNKNOWN",
                "BLOCKER",
                "AGENTS.md",
                "Modalita' agente non dichiarata e nessun ramo agente riconoscibile.",
            )
        )
    elif declared_mode is not None and agent != "auto" and declared_mode != agent:
        findings.append(
            Finding(
                "AGENT_MODE_MISMATCH",
                "BLOCKER",
                "AGENTS.md",
                f"La casa dichiara {declared_mode}, ma il controllo richiede {agent}. "
                "Usare both o una migrazione esplicita.",
            )
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

    required_files = (
        install_contract.required_paths(CONTRACT, requested_mode)
        if requested_mode is not None
        else list(REQUIRED_FILES)
    )
    for rel in required_files:
        path = target / rel
        linked = _symlink_component(target, rel)
        if linked is not None:
            findings.append(
                Finding(
                    "STANDARD_PATH_SYMLINK",
                    "BLOCKER",
                    rel,
                    "Un file o un suo antenato e' un symlink: lo standard deve "
                    "vivere dentro la cartella madre.",
                )
            )
            continue
        if not path.is_file():
            findings.append(
                Finding(
                    "MISSING_STANDARD_FILE",
                    "BLOCKER",
                    rel,
                    "File obbligatorio dello standard assente.",
                )
            )
    if requested_mode is not None:
        for rel in install_contract.forbidden_paths(CONTRACT, requested_mode):
            path = target / rel
            if path.exists() or path.is_symlink():
                findings.append(
                    Finding(
                        "FORBIDDEN_STANDARD_FILE",
                        "BLOCKER",
                        rel,
                        f"Il file appartiene a un ramo vietato in modalita' "
                        f"{requested_mode}. Usare both o una migrazione esplicita.",
                    )
                )

    if (
        requested_mode is None
        or "git_baseline"
        in install_contract.external_effects(CONTRACT, requested_mode)
    ):
        gitignore_path = target / ".gitignore"
        if gitignore_path.is_file() and not gitignore_path.is_symlink():
            gitignore_lines = {
                line.strip()
                for line in gitignore_path.read_text(
                    encoding="utf-8", errors="replace"
                ).splitlines()
            }
            missing_ignore_rules = sorted(
                set(GITIGNORE_REQUIRED_RULES) - gitignore_lines
            )
            if missing_ignore_rules:
                findings.append(
                    Finding(
                        "GITIGNORE_RULES_MISSING",
                        "BLOCKER",
                        ".gitignore",
                        "Regole di sicurezza mancanti: "
                        + ", ".join(missing_ignore_rules),
                    )
                )

        git_dir = target / ".git"
        if git_dir.is_symlink():
            findings.append(
                Finding(
                    "GIT_REPOSITORY_SYMLINK",
                    "BLOCKER",
                    ".git",
                    "La baseline Git deve appartenere alla cartella madre.",
                )
            )
        elif not git_dir.is_dir():
            findings.append(
                Finding(
                    "GIT_REPOSITORY_MISSING",
                    "BLOCKER",
                    ".git",
                    "La casa non ha ancora una baseline Git verificabile.",
                )
            )
        else:
            try:
                head = subprocess.run(
                    ["git", "rev-parse", "--verify", "HEAD"],
                    cwd=str(target),
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError:
                head = None
            if head is None or head.returncode != 0:
                findings.append(
                    Finding(
                        "GIT_BASELINE_MISSING",
                        "BLOCKER",
                        ".git",
                        "Repository presente senza primo commit verificabile.",
                    )
                )

            safety_paths = (
                "REPORT_FINALE.md",
                ".secrets/prova.txt",
                "prova.env",
                "api-token-prova.txt",
                "client-secret-prova.txt",
                "client-password-prova.txt",
                "client-credential-prova.txt",
            )
            ineffective = []
            for relative in safety_paths:
                try:
                    ignored = subprocess.run(
                        ["git", "check-ignore", "--quiet", "--", relative],
                        cwd=str(target),
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                except OSError:
                    ignored = None
                if ignored is None or ignored.returncode != 0:
                    ineffective.append(relative)
            if ineffective:
                findings.append(
                    Finding(
                        "GITIGNORE_INEFFECTIVE",
                        "BLOCKER",
                        ".gitignore",
                        "Le esclusioni non proteggono: "
                        + ", ".join(ineffective),
                    )
                )

    root_bridge = target / "CLAUDE.md"
    if (
        root_bridge.is_file()
        and not root_bridge.is_symlink()
        and root_bridge.read_text(encoding="utf-8") != CLAUDE_BRIDGE
    ):
        findings.append(
            Finding(
                "INVALID_ROOT_BRIDGE",
                "BLOCKER",
                "CLAUDE.md",
                "Il ponte deve contenere soltanto @AGENTS.md.",
            )
        )

    report_path = target / "REPORT_FINALE.md"
    if report_path.is_symlink():
        findings.append(
            Finding(
                "TEMP_REPORT_SYMLINK",
                "BLOCKER",
                "REPORT_FINALE.md",
                "Il report temporaneo deve essere un file locale.",
            )
        )
    elif report_path.is_file():
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

    canonical_memory = _canonical_memory_path(target, agents_text)
    if not (canonical_memory / "MEMORY.md").is_file():
        findings.append(
            Finding(
                "MISSING_CANONICAL_MEMORY_INDEX",
                "BLOCKER",
                str(canonical_memory / "MEMORY.md"),
                "La memoria canonica dichiarata nella mappa madre non contiene MEMORY.md.",
            )
        )
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

        administrator_key = _normalized(room.administrator).strip()
        if (
            not administrator_key
            or "da assegnare" in administrator_key
            or _normalized(ORGANIZATION.sector_role) not in administrator_key
        ):
            findings.append(
                Finding(
                    "ROOM_ADMINISTRATOR_MISSING",
                    "BLOCKER",
                    room.path,
                    "Il ramo non dichiara il proprio Amministratore di settore.",
                )
            )
        if _normalized(room.reports_to).strip() != _normalized(
            ORGANIZATION.default_reports_to
        ):
            findings.append(
                Finding(
                    "ROOM_BOSS_ROUTE_MISSING",
                    "BLOCKER",
                    room.path,
                    "L'amministratore del ramo non riporta al Boss "
                    "dell'Ecosistema nella mappa madre.",
                )
            )

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
        linked = _symlink_component(target, room.path)
        if linked is not None:
            findings.append(
                Finding(
                    "ROOM_PATH_SYMLINK",
                    "BLOCKER",
                    room.path,
                    "La stanza o un suo antenato e' un symlink fuori dal "
                    "contratto della cartella madre.",
                )
            )
            continue
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
        if room_agents.is_symlink():
            findings.append(
                Finding(
                    "ROOM_MAP_SYMLINK",
                    "BLOCKER",
                    f"{room.path}/AGENTS.md",
                    "La mappa della stanza deve essere un file locale.",
                )
            )
        elif not room_agents.is_file():
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
        if room_claude.is_symlink():
            findings.append(
                Finding(
                    "ROOM_BRIDGE_SYMLINK",
                    "BLOCKER",
                    f"{room.path}/CLAUDE.md",
                    "Il ponte della stanza deve essere un file locale.",
                )
            )
        elif not room_claude.is_file():
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

    root_owned = parse_root_owned_registry(agents_text)
    declared_paths = {room.path for room in rooms if room.path} | root_owned
    declared_top_levels = {Path(path).parts[0] for path in declared_paths}
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
                    "Nome generico: classificare i contenuti e portarli alla cartella madre o alla stanza proprietaria.",
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
        if (
            child.name in ALLOWED_ROOT_FILES
            or child.name in root_owned
            or ".leaderai-backup" in child.name
        ):
            continue
        findings.append(
            Finding(
                "UNOWNED_ROOT_FILE",
                "BLOCKER",
                child.name,
                "File sciolto nella home senza proprietario dichiarato.",
            )
        )

    active_agents = _active_agents(
        target,
        requested_mode if requested_mode is not None else "auto",
    )
    if not active_agents:
        # Il finding e' gia' emesso sopra con la fonte della modalita'.
        pass
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
        project_settings_paths = (
            target / ".claude" / "settings.json",
            target / ".claude" / "settings.local.json",
        )
        for project_settings_path in project_settings_paths:
            if not project_settings_path.is_file():
                continue
            try:
                project_settings = json.loads(
                    project_settings_path.read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError):
                project_settings = None
            if isinstance(project_settings, dict) and "autoMemoryDirectory" in project_settings:
                findings.append(
                    Finding(
                        "CLAUDE_MEMORY_SCOPE_INVALID",
                        "BLOCKER",
                        project_settings_path.relative_to(target).as_posix(),
                        "autoMemoryDirectory non e' accettato nelle settings "
                        "project/local: spostare la chiave nelle user settings.",
                    )
                )

        settings_path = (
            claude_user_settings_path.expanduser()
            if claude_user_settings_path is not None
            else Path.home() / ".claude" / "settings.json"
        )
        desired_memory = canonical_memory
        settings_label = (
            str(settings_path)
            if claude_user_settings_path is not None
            else "~/.claude/settings.json"
        )
        if not settings_path.is_file():
            findings.append(
                Finding(
                    "CLAUDE_MEMORY_ROUTE_MISSING",
                    "BLOCKER",
                    settings_label,
                    "Claude Code non punta auto memory alla memoria canonica della casa; "
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
                        settings_label,
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
                            settings_label,
                            "autoMemoryDirectory deve essere assoluto o iniziare con ~/.",
                        )
                    )
                elif configured.resolve() != desired_memory:
                    findings.append(
                        Finding(
                            "CLAUDE_MEMORY_DIVERGED",
                            "BLOCKER",
                            settings_label,
                            "Auto memory punta fuori dalla memoria canonica della casa: "
                            "confrontare e unire le due memorie prima di cambiare il percorso.",
                        )
                    )
                elif not raw_memory.startswith("~/") and _is_inside_home(configured):
                    # Forma non portabile: il percorso e' corretto su QUESTO computer,
                    # ma inchioda il segmento utente della home locale. Su un'altra
                    # postazione dello stesso cliente punterebbe a una cartella
                    # inesistente e la memoria si romperebbe senza errori visibili.
                    findings.append(
                        Finding(
                            "CLAUDE_MEMORY_NOT_PORTABLE",
                            "ATTENZIONE",
                            settings_label,
                            "autoMemoryDirectory inchioda il nome utente di questo "
                            "computer: riscriverlo nella forma portabile ~/ prima di "
                            "replicarlo su un'altra postazione del cliente.",
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

    findings.extend(_markdown_hygiene_findings(target))

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
    parser.add_argument(
        "--claude-user-settings",
        help=(
            "Percorso user settings Claude letto su questa macchina. "
            "Default: ~/.claude/settings.json."
        ),
    )
    parser.add_argument("--json", action="store_true", help="Emette JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inspection = inspect_ecosystem(
        Path(args.target),
        args.agent,
        claude_user_settings_path=(
            Path(args.claude_user_settings)
            if args.claude_user_settings
            else None
        ),
    )
    if args.json:
        print(json.dumps(inspection.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_markdown(inspection), end="")
    return 0 if inspection.verdict == "PASSA" else 1


if __name__ == "__main__":
    raise SystemExit(main())
