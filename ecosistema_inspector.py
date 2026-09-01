#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import stat
import subprocess
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

import install_contract


ROOT = Path(__file__).resolve().parent
STANDARD_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
CONTRACT = install_contract.CONTRACT
ORGANIZATION = install_contract.organization_policy(CONTRACT)
ROOM_LIFECYCLE = install_contract.room_lifecycle_policy(CONTRACT)
MARKDOWN_HYGIENE = install_contract.markdown_hygiene_policy(CONTRACT)
CLAUDE_BRIDGE = ROOM_LIFECYCLE.bridge_content
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
}

STANDARD_ECOSYSTEM_PATHS = {
    Path(rule.destination).relative_to("ecosistema").as_posix()
    for rule in install_contract.template_rules(CONTRACT, "both")
    if Path(rule.destination).parts[0] == "ecosistema"
}

ROOM_TEMPLATE_RULES = {
    rule.destination: rule.template
    for rule in install_contract.template_rules(CONTRACT, "both")
    if rule.destination
    in {ROOM_LIFECYCLE.map_template, ROOM_LIFECYCLE.source_template}
}

IGNORED_OS_ENTRIES = {".DS_Store", "Thumbs.db", "desktop.ini"}
IGNORED_ROOM_DIRS = {"__pycache__", "node_modules", ".venv", "venv"}
MEMORY_WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")

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

WINDOWS_RESERVED_NAMES = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}

ROOM_REQUIRED_SECTIONS = ROOM_LIFECYCLE.required_sections
ROOM_REQUIRED_TERMS = ROOM_LIFECYCLE.required_terms
ROOM_FILE_NAMES = {
    name.casefold(): name for name in ROOM_LIFECYCLE.room_required_files
}
ROOM_MAP_FILE = ROOM_FILE_NAMES["agents.md"]
ROOM_BRIDGE_FILE = ROOM_FILE_NAMES["claude.md"]

UNPROVEN_ROOM_RESPONSIBILITY_TERMS = (
    "{{",
    "da definire",
    "da compilare",
    "non applicabile",
)

UNPROVEN_VALUE_TERMS = (
    "{{",
    "da definire",
    "da compilare",
    "da collegare",
)

ROOM_RESPONSIBILITY_GUIDANCE = (
    "descrivere la funzione aziendale riconosciuta dal proprietario, lo stato che "
    "mantiene e le decisioni che governa. elencare script, skill, modelli o output "
    "non dimostra una stanza."
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
    upstream: str
    downstream: str
    sources: str
    outputs: str
    capabilities: str
    map_path: str
    administrator: str
    reports_to: str


@dataclass(frozen=True)
class RootOwned:
    path: str
    classification: str
    usage: str
    registry_path: str


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


def _hidden_from_owner(path: Path) -> bool:
    """Flag di invisibilita' che nasconde il percorso al proprietario.

    macOS/BSD: chflags hidden (st_flags & UF_HIDDEN). Windows: attributo
    Hidden. I dotfile restano fuori: li nasconde la convenzione di sistema,
    non un flag messo sul singolo percorso.
    """
    if path.name.startswith("."):
        return False
    try:
        info = os.stat(path, follow_symlinks=False)
    except OSError:
        return False
    uf_hidden = getattr(stat, "UF_HIDDEN", 0)
    if uf_hidden and getattr(info, "st_flags", 0) & uf_hidden:
        return True
    attr_hidden = getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 0)
    if attr_hidden and getattr(info, "st_file_attributes", 0) & attr_hidden:
        return True
    return False


def _expected_guard_handler(template_name: str) -> dict:
    template = json.loads(
        (ROOT / "templates" / template_name).read_text(encoding="utf-8")
    )
    return template["hooks"]["Stop"][0]["hooks"][0]


def _matches_guard_handler(handler: object, expected: dict) -> bool:
    return (
        isinstance(handler, dict)
        and handler.get("type") == expected.get("type")
        and handler.get("command") == expected.get("command")
    )


def _guardiano_findings(target: Path, mode: str) -> list[Finding]:
    findings: list[Finding] = []
    managed_scripts = {
        ".agent/hooks/guardiano_stanze.sh": "GUARDIANO_STANZE.sh",
        ".agent/hooks/guardiano_stanze_windows.ps1": (
            "GUARDIANO_STANZE_WINDOWS.ps1"
        ),
    }
    for relative, template_name in managed_scripts.items():
        path = target / relative
        if not path.is_file() or path.is_symlink():
            continue
        expected = (ROOT / "templates" / template_name).read_bytes()
        try:
            current = path.read_bytes()
        except OSError:
            current = b""
        if current != expected:
            findings.append(
                Finding(
                    "GUARDIAN_SCRIPT_DRIFT",
                    "BLOCKER",
                    relative,
                    "Il guardiano installato non coincide con il template "
                    "dello standard corrente.",
                )
            )

    configs: list[tuple[str, bool, str]] = []
    if mode in {"codex", "both"}:
        configs.append((".codex/hooks.json", True, "CODEX_HOOKS.json"))
    if mode in {"claude", "both"}:
        configs.append((".claude/settings.json", False, "CLAUDE_SETTINGS.json"))

    for relative, needs_windows, template_name in configs:
        path = target / relative
        if not path.is_file() or path.is_symlink():
            continue
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            config = None
        if not isinstance(config, dict):
            findings.append(
                Finding(
                    "GUARDIAN_CONFIG_INVALID",
                    "BLOCKER",
                    relative,
                    "La configurazione del guardiano non e' un oggetto JSON valido.",
                )
            )
            continue
        if relative.startswith(".claude/") and config.get("disableAllHooks") is True:
            findings.append(
                Finding(
                    "GUARDIAN_HOOK_DISABLED",
                    "BLOCKER",
                    relative,
                    "Gli hook di progetto sono disattivati.",
                )
            )

        hook_map = config.get("hooks")
        stop_groups = hook_map.get("Stop", []) if isinstance(hook_map, dict) else []
        expected_handler = _expected_guard_handler(template_name)
        matching: list[dict] = []
        if isinstance(stop_groups, list):
            for group in stop_groups:
                handlers = group.get("hooks", []) if isinstance(group, dict) else []
                if not isinstance(handlers, list):
                    continue
                for handler in handlers:
                    if _matches_guard_handler(handler, expected_handler):
                        matching.append(handler)

        if not matching:
            findings.append(
                Finding(
                    "GUARDIAN_HOOK_MISSING",
                    "BLOCKER",
                    relative,
                    "Manca l'unico handler Stop del guardiano delle stanze.",
                )
            )
            continue
        if len(matching) > 1:
            findings.append(
                Finding(
                    "GUARDIAN_HOOK_DUPLICATE",
                    "BLOCKER",
                    relative,
                    "Il guardiano e' registrato piu' di una volta.",
                )
            )
        if any(
            any(
                handler.get(key) != value
                for key, value in expected_handler.items()
                if key != "commandWindows"
            )
            for handler in matching
        ):
            findings.append(
                Finding(
                    "GUARDIAN_HOOK_INVALID",
                    "BLOCKER",
                    relative,
                    "Il comando del guardiano esiste ma la configurazione non "
                    "coincide con lo standard corrente.",
                )
            )
        if needs_windows and not any(
            handler.get("commandWindows") == expected_handler.get("commandWindows")
            for handler in matching
        ):
            findings.append(
                Finding(
                    "GUARDIAN_WINDOWS_COMMAND_MISSING",
                    "BLOCKER",
                    relative,
                    "Il ramo Codex non contiene il comando Windows del guardiano.",
                )
            )
    return findings


def _contains_unproven_value(text: str) -> bool:
    normalized = _normalized(text)
    return any(term in normalized for term in UNPROVEN_VALUE_TERMS) or bool(
        re.search(r"\b(?:todo|tbd)\b", normalized)
    )


def _canonical_relative_path(raw: str) -> str | None:
    value = raw.strip().replace("\\", "/")
    if (
        not value
        or value == "."
        or value.startswith("/")
        or re.match(r"^[a-zA-Z]:", value)
    ):
        return None
    parts = [part for part in value.split("/") if part not in {"", "."}]
    if (
        not parts
        or ".." in parts
        or any(
            ":" in part
            or part.rstrip(" .") != part
            or part.split(".", 1)[0].casefold() in WINDOWS_RESERVED_NAMES
            for part in parts
        )
    ):
        return None
    return "/".join(parts)


def _active_markdown(text: str) -> str:
    without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    without_fences = re.sub(
        r"(?ms)^\s*(```|~~~)[^\n]*\n.*?^\s*\1\s*$",
        "",
        without_comments,
    )
    return re.sub(
        r"(?ms)^\s*(```|~~~)[^\n]*\n.*\Z",
        "",
        without_fences,
    )


def _table_cells(line: str) -> list[str]:
    if line.startswith("\t") or len(line) - len(line.lstrip(" ")) >= 4:
        return []
    if not line.lstrip().startswith("|"):
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_block_after_marker(content: str, marker: str) -> list[str]:
    matches = list(
        re.finditer(
            rf"(?m)^[ ]{{0,3}}{re.escape(marker)}[ \t]*$",
            content,
        )
    )
    if len(matches) != 1:
        return []
    section = content[matches[0].end() :]
    section = re.split(r"\n[ ]{0,3}#{2,3}\s", section, maxsplit=1)[0]
    section_lines = section.splitlines()
    while section_lines and not section_lines[0].strip():
        section_lines.pop(0)
    if not section_lines or not section_lines[0].lstrip().startswith("|"):
        return []
    table_lines: list[str] = []
    for line in section_lines:
        if line.lstrip().startswith("|"):
            table_lines.append(line)
        else:
            break
    return table_lines


def _room_from_cell(
    cell: str,
    purpose: str,
    upstream: str,
    downstream: str,
    sources: str,
    outputs: str,
    capabilities: str,
    map_path: str,
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
    canonical_path = _canonical_relative_path(path)
    if canonical_path is None:
        return Room(
            name=name,
            path="",
            purpose=purpose,
            upstream=upstream,
            downstream=downstream,
            sources=sources,
            outputs=outputs,
            capabilities=capabilities,
            map_path=map_path,
            administrator=administrator,
            reports_to=reports_to,
        )
    return Room(
        name=name,
        path=canonical_path,
        purpose=purpose,
        upstream=upstream,
        downstream=downstream,
        sources=sources,
        outputs=outputs,
        capabilities=capabilities,
        map_path=map_path,
        administrator=administrator,
        reports_to=reports_to,
    )


def parse_room_registry(agents_text: str) -> list[Room]:
    agents_text = _active_markdown(agents_text)
    marker = "### Registro delle stanze"
    if not _table_block_after_marker(agents_text, marker):
        return []
    rooms: list[Room] = []
    for line in _table_block_after_marker(agents_text, marker)[2:]:
        cells = _table_cells(line)
        if len(cells) < 2:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        administrator = cells[8].strip("`").strip() if len(cells) > 8 else ""
        reports_to = cells[9].strip("`").strip() if len(cells) > 9 else ""
        map_path = cells[7].strip("`").strip() if len(cells) > 7 else ""
        room = _room_from_cell(
            cells[0],
            cells[1],
            cells[2] if len(cells) > 2 else "",
            cells[3] if len(cells) > 3 else "",
            cells[4] if len(cells) > 4 else "",
            cells[5] if len(cells) > 5 else "",
            cells[6] if len(cells) > 6 else "",
            map_path,
            administrator,
            reports_to,
        )
        if room is not None:
            rooms.append(room)
    return rooms


def parse_root_owned_rows(agents_text: str) -> list[RootOwned]:
    agents_text = _active_markdown(agents_text)
    marker = "### Elementi posseduti direttamente dalla cartella madre"
    if not _table_block_after_marker(agents_text, marker):
        return []
    rows: list[RootOwned] = []
    for line in _table_block_after_marker(agents_text, marker)[2:]:
        cells = _table_cells(line)
        if len(cells) < 2:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        raw = cells[0].strip("`").strip()
        if _normalized(raw) in {"percorso", "da censire"}:
            continue
        canonical_path = _canonical_relative_path(raw)
        rows.append(
            RootOwned(
                path=canonical_path or "",
                classification=cells[1].strip("`").strip(),
                usage=cells[2].strip("`").strip() if len(cells) > 2 else "",
                registry_path=(
                    cells[3].strip("`").strip() if len(cells) > 3 else ""
                ),
            )
        )
    return rows


def parse_root_owned_registry(agents_text: str) -> dict[str, str]:
    return {
        row.path: row.classification for row in parse_root_owned_rows(agents_text)
    }


def _registry_has_entry(content: str, marker: str, expected_path: str) -> bool:
    table = _table_block_after_marker(_active_markdown(content), marker)
    expected = _field_value(expected_path)
    for line in table[2:]:
        cells = _table_cells(line)
        if not cells:
            continue
        raw = cells[0].strip()
        candidates = [raw]
        link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", raw)
        if link:
            candidates.extend(link.groups())
        if any(_field_value(candidate) == expected for candidate in candidates):
            return True
    return False


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


def _frontmatter_list(path: Path, key: str) -> list[str]:
    """Legge una lista semplice dal frontmatter senza dipendere da PyYAML."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    if not lines or lines[0].strip() != "---":
        return []

    values: list[str] = []
    index = 1
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped == "---":
            break
        if not line.startswith((" ", "\t")) and stripped.startswith(f"{key}:"):
            inline = stripped.split(":", 1)[1].strip()
            if inline:
                values.extend(
                    item.strip().strip("\"'")
                    for item in inline.strip("[]").split(",")
                    if item.strip()
                )
                break
            index += 1
            while index < len(lines):
                candidate = lines[index].strip()
                if candidate.startswith("- "):
                    values.append(candidate[2:].strip().strip("\"'"))
                    index += 1
                    continue
                if not candidate:
                    index += 1
                    continue
                break
            break
        index += 1
    return values


def _memory_reference_key(raw: str) -> str | None:
    reference = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if not reference or "/" in reference or reference.startswith(("http:", "https:", "mailto:")):
        return None
    stem = Path(reference).stem
    normalized = _normalized(stem).replace("_", "").replace("-", "")
    if normalized.startswith("feedback"):
        normalized = normalized.removeprefix("feedback")
    return normalized or None


def _memory_merge_reference_findings(target: Path, memory: Path) -> list[Finding]:
    """Una fusione non puo' lasciare wikilink alle voci mandate in archivio."""
    if not memory.is_dir():
        return []

    findings: list[Finding] = []
    replacements: dict[str, Path] = {}
    files = sorted(
        path for path in memory.rglob("*.md") if path.is_file() and not path.is_symlink()
    )
    for path in files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        sources = _frontmatter_list(path, "replaces")
        if re.search(r"\bfusion(?:e|i|ato|ata|ati|ate)?\b", content, flags=re.IGNORECASE) and not sources:
            findings.append(
                Finding(
                    "MEMORY_MERGE_CONTRACT_MISSING",
                    "BLOCKER",
                    path.relative_to(target).as_posix(),
                    "Memoria fusa senza elenco `replaces`: non e' possibile provare "
                    "che tutti i rimandi siano stati aggiornati.",
                )
            )
        for source in sources:
            key = _memory_reference_key(source)
            if key:
                replacements[key] = path

    if not replacements:
        return findings

    for path in files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in MEMORY_WIKILINK_RE.finditer(content):
            reference = match.group(1).strip()
            replacement = replacements.get(_memory_reference_key(reference) or "")
            if replacement is None:
                continue
            findings.append(
                Finding(
                    "MEMORY_MERGE_REFERENCE_STALE",
                    "BLOCKER",
                    path.relative_to(target).as_posix(),
                    "Rimando alla memoria superata `[[%s]]`: puntare a `%s`."
                    % (reference, replacement.relative_to(target).as_posix()),
                )
            )
    return findings


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
    )
    for path, patterns in candidates:
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
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


def _first_markdown_bullet(section: str) -> str:
    for line in section.splitlines():
        match = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return ""


def _markdown_bullets(section: str) -> list[str]:
    return [
        match.group(1).strip()
        for line in section.splitlines()
        if (match := re.match(r"^\s*-\s+(.+?)\s*$", line))
    ]


def _field_value(raw: str) -> str:
    value = raw.strip().strip("`").strip()
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    return re.sub(r"\s+", " ", _normalized(value)).strip()


def _negates_claim(text: str, claims: tuple[str, ...]) -> bool:
    normalized = re.sub(r"[^\w\s]", " ", _normalized(text))
    normalized = re.sub(r"\s+", " ", normalized).strip()
    negation = r"(?:non|nessun[oa]?|senza)"
    denied_verbs = (
        r"(?:esist\w*|avvien\w*|manten\w*|govern\w*|gest\w*|"
        r"applic\w*|riconosc\w*)"
    )
    for claim in claims:
        normalized_claim = re.sub(r"[^\w\s]", " ", _normalized(claim))
        words = [re.escape(word) for word in normalized_claim.split()]
        if not words:
            continue
        claim_pattern = r"\s+".join(words)
        if re.search(
            rf"\b{negation}\b(?:\s+\w+){{0,5}}\s+{claim_pattern}\b",
            normalized,
        ):
            return True
        if re.search(
            rf"\b{claim_pattern}\b(?:\s+\w+){{0,8}}\s+\b{negation}\b"
            rf"(?:\s+\w+){{0,4}}\s+\b{denied_verbs}\b",
            normalized,
        ):
            return True
    return False


def _organization_route_is_negated(text: str) -> bool:
    normalized = re.sub(r"[^\w\s]", " ", _normalized(text))
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return bool(
        re.search(
            r"\briport(?:a|o)\b(?:\s+\w+){0,5}\s+\bnon\b"
            r"(?:\s+\w+){0,3}\s+\b(?:avvien\w*|esist\w*|oper\w*)\b",
            normalized,
        )
    )


def _declared_path_bullets(section: str) -> list[str]:
    declared: list[str] = []
    for value in _markdown_bullets(section):
        match = re.fullmatch(r"`([^`]+)`", value)
        if match:
            declared.append(match.group(1).strip())
    return declared


def _room_operating_source_paths(room_path: Path) -> set[str]:
    """Trova le fonti operative reali, anche se una copia non e' dichiarata."""
    candidates: set[str] = set()
    try:
        paths = tuple(room_path.rglob("*"))
    except OSError:
        return candidates
    for path in paths:
        try:
            relative = path.relative_to(room_path)
            if (
                path.suffix.casefold() != ".md"
                or not path.is_file()
                or _symlink_component(room_path, relative) is not None
            ):
                continue
            content = _active_markdown(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError):
            continue
        title = re.search(r"(?m)^#\s+(.+?)\s*$", content)
        if not title or not _field_value(title.group(1)).endswith(
            "- fonte operativa"
        ):
            continue
        headings = {_normalized(value) for value in _markdown_headings(content)}
        if all(
            _normalized(required) in headings
            for required in ROOM_LIFECYCLE.owner_source_headings
        ):
            candidates.add(relative.as_posix().casefold())
    return candidates


def _business_source_declaration(content: str) -> tuple[str, Path | None]:
    section = _markdown_section(content, ROOM_LIFECYCLE.business_source_section)
    declarations = [
        value
        for value in _markdown_bullets(section)
        if _normalized(value).strip().startswith("non applicabile")
        or re.fullmatch(r"`([^`]+)`", value)
    ]
    if len(declarations) > 1:
        return ("multiple", None)
    value = declarations[0] if declarations else ""
    normalized = _normalized(value).strip()
    if normalized.startswith("non applicabile"):
        reason = normalized.partition(":")[2].strip()
        return ("not_applicable" if reason else "invalid", None)
    match = re.fullmatch(r"`([^`]+)`", value)
    if not match:
        return ("missing", None)
    raw = match.group(1).strip()
    canonical = _canonical_relative_path(raw)
    candidate = Path(canonical) if canonical else None
    if (
        candidate is None
        or candidate.name.casefold() in ROOM_FILE_NAMES
    ):
        return ("invalid", None)
    return ("file", candidate)


def _business_source_file_issue(room_path: Path, candidate: Path) -> str | None:
    if _symlink_component(room_path, candidate) is not None:
        return "symlink"
    source = room_path / candidate
    if not source.is_file():
        return "missing"
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return "unreadable"
    if not text.strip():
        return "empty"
    if _contains_unproven_value(text):
        return "placeholder"
    return None


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

    findings: list[Finding] = []
    room_agents = room_path / ROOM_MAP_FILE
    try:
        map_text = _active_markdown(room_agents.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        map_text = ""
    declaration, source_candidate = _business_source_declaration(map_text)
    if declaration != "file" or source_candidate is None:
        findings.append(
            Finding(
                "BUSINESS_SOURCE_UNDECLARED",
                "BLOCKER",
                room_path.relative_to(target).as_posix(),
                "La stanza genera documenti ma non dichiara una fonte business "
                "editabile esterna al codice.",
            )
        )
    else:
        issue = _business_source_file_issue(room_path, source_candidate)
        issue_details = {
            "symlink": (
                "BUSINESS_SOURCE_SYMLINK",
                "La fonte business deve essere un file locale, non un "
                "collegamento simbolico.",
            ),
            "missing": (
                "BUSINESS_SOURCE_MISSING",
                "La fonte business dichiarata non esiste.",
            ),
            "unreadable": (
                "BUSINESS_SOURCE_UNREADABLE",
                "La fonte business non e' leggibile come testo UTF-8.",
            ),
            "empty": (
                "BUSINESS_SOURCE_EMPTY",
                "La fonte business dichiarata e' vuota.",
            ),
            "placeholder": (
                "BUSINESS_SOURCE_PLACEHOLDER",
                "La fonte business conserva campi non compilati.",
            ),
        }
        if issue:
            code, detail = issue_details[issue]
            findings.append(
                Finding(
                    code,
                    "BLOCKER",
                    f"{room_path.relative_to(target).as_posix()}/"
                    f"{source_candidate.as_posix()}",
                    detail,
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
    section = _markdown_section(content, "responsabilita business")
    if not section:
        return False
    compact = re.sub(r"\s+", " ", _normalized(section)).strip()
    compact = compact.replace(ROOM_RESPONSIBILITY_GUIDANCE, "").strip()
    if not compact:
        return False
    if any(term in compact for term in UNPROVEN_ROOM_RESPONSIBILITY_TERMS):
        return False
    if _negates_claim(compact, ("stato", "decisione", "decisioni")):
        return False
    return "stato" in compact and "decision" in compact


def _markdown_section(content: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\s*(.*?)(?=^##\s|\Z)",
        content,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def _markdown_headings(content: str, level: int = 2) -> tuple[str, ...]:
    marker = "#" * level
    return tuple(
        match.group(1).strip()
        for match in re.finditer(
            rf"(?m)^{re.escape(marker)}\s+(.+?)\s*$",
            content,
        )
    )


def _ecosystem_registry_findings(target: Path) -> list[Finding]:
    registry = target / "ecosistema"
    if registry.is_symlink():
        return [
            Finding(
                "ECOSYSTEM_REGISTRY_SYMLINK",
                "BLOCKER",
                "ecosistema",
                "L'armadio comune deve essere locale alla cartella madre: il "
                "collegamento simbolico non viene attraversato.",
            )
        ]
    if not registry.is_dir():
        return []

    findings: list[Finding] = []
    for path in sorted(registry.rglob("*"), key=lambda item: item.as_posix().casefold()):
        rel = path.relative_to(registry)
        if any(part in IGNORED_OS_ENTRIES for part in rel.parts):
            continue
        rel_text = rel.as_posix()
        if rel_text in STANDARD_ECOSYSTEM_PATHS:
            continue
        if path.is_dir() and any(
            standard.startswith(rel_text.rstrip("/") + "/")
            for standard in STANDARD_ECOSYSTEM_PATHS
        ):
            continue
        if any(
            parent.as_posix() not in STANDARD_ECOSYSTEM_PATHS
            and not any(
                standard.startswith(parent.as_posix().rstrip("/") + "/")
                for standard in STANDARD_ECOSYSTEM_PATHS
            )
            for parent in rel.parents
            if parent != Path(".")
        ):
            continue
        findings.append(
            Finding(
                "ECOSYSTEM_REGISTRY_CONTAMINATED",
                "BLOCKER",
                f"ecosistema/{rel_text}",
                "La cartella ecosistema contiene soltanto registri e calchi "
                "comuni dichiarati dal contratto. Spostare il contenuto nella "
                "stanza proprietaria o classificarlo prima di creare una stanza.",
            )
        )
    for destination, template_name in sorted(ROOM_TEMPLATE_RULES.items()):
        installed = target / destination
        expected = ROOT / "templates" / template_name
        if installed.is_symlink():
            findings.append(
                Finding(
                    "ECOSYSTEM_ROOM_TEMPLATE_SYMLINK",
                    "BLOCKER",
                    destination,
                    "Il calco stanza deve essere un file locale della casa.",
                )
            )
            continue
        try:
            matches = (
                installed.is_file()
                and installed.read_bytes() == expected.read_bytes()
            )
        except OSError:
            matches = False
        if not matches:
            findings.append(
                Finding(
                    "ECOSYSTEM_ROOM_TEMPLATE_DRIFT",
                    "BLOCKER",
                    destination,
                    "Il calco stanza e' vuoto, manomesso o diverso dalla versione "
                    "ufficiale installata.",
                )
            )
    return findings


def _room_prefab_findings(
    target: Path,
    room_path: Path,
    content: str,
    room_name: str,
) -> list[Finding]:
    findings: list[Finding] = []
    room_rel = room_path.relative_to(target).as_posix()
    content = _active_markdown(content)

    if re.search(r"\{\{[^{}]+\}\}", content):
        findings.append(
            Finding(
                "ROOM_MAP_PLACEHOLDER",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "La mappa conserva campi del calco non compilati.",
            )
        )

    source_section = _markdown_section(content, ROOM_LIFECYCLE.owner_source_section)
    source_declarations = _declared_path_bullets(source_section)
    source_raw = source_declarations[0] if source_declarations else ""
    canonical_source = _canonical_relative_path(source_raw)
    source_candidate = Path(canonical_source) if canonical_source else None
    generic_source_stem = _normalized(Path(ROOM_LIFECYCLE.source_template).stem)
    source_valid = bool(
        source_candidate
        and source_candidate.name.casefold() not in ROOM_FILE_NAMES
    )
    physical_sources = _room_operating_source_paths(room_path)
    if len(source_declarations) > 1 or len(physical_sources) > 1:
        findings.append(
            Finding(
                "ROOM_OWNER_SOURCE_MULTIPLE",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "La stanza dichiara piu' di una fonte operativa proprietaria.",
            )
        )
    if not source_valid:
        findings.append(
            Finding(
                "ROOM_OWNER_SOURCE_UNDECLARED",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "La stanza non dichiara una fonte operativa relativa e sicura.",
            )
        )
    else:
        if generic_source_stem in _normalized(source_candidate.stem):
            findings.append(
                Finding(
                    "ROOM_OWNER_SOURCE_GENERIC_NAME",
                    "BLOCKER",
                    f"{room_rel}/{source_candidate.as_posix()}",
                    "La fonte operativa conserva il nome del calco: assegnarle "
                    "un nome legato alla domanda business della stanza.",
                )
            )
        summary_references = [
            _canonical_relative_path(raw)
            for raw in re.findall(
                r"(?im)^\s*-\s*fonte operativa\s*:\s*`([^`]+)`",
                content,
            )
        ]
        if any(reference != canonical_source for reference in summary_references):
            findings.append(
                Finding(
                    "ROOM_OWNER_SOURCE_CONFLICT",
                    "BLOCKER",
                    f"{room_rel}/{ROOM_MAP_FILE}",
                    "I riferimenti alla fonte operativa non coincidono con la "
                    "sezione proprietaria.",
                )
            )
        source_path = room_path / source_candidate
        linked = _symlink_component(room_path, source_candidate)
        if linked is not None or not source_path.is_file():
            findings.append(
                Finding(
                    "ROOM_OWNER_SOURCE_MISSING",
                    "BLOCKER",
                    f"{room_rel}/{source_candidate.as_posix()}",
                    "La fonte operativa dichiarata non esiste come file locale.",
                )
            )
        else:
            try:
                source_raw_text = _active_markdown(
                    source_path.read_text(encoding="utf-8")
                )
            except (OSError, UnicodeError):
                findings.append(
                    Finding(
                        "ROOM_OWNER_SOURCE_UNREADABLE",
                        "BLOCKER",
                        f"{room_rel}/{source_candidate.as_posix()}",
                        "La fonte operativa non e' leggibile come testo UTF-8.",
                    )
                )
            else:
                source_text = _normalized(source_raw_text)
                source_title_match = re.search(
                    r"(?m)^#\s+(.+?)\s*$",
                    source_raw_text,
                )
                source_title = (
                    _field_value(source_title_match.group(1))
                    if source_title_match
                    else ""
                )
                expected_source_title = _field_value(
                    f"{room_name} - fonte operativa"
                )
                if source_title != expected_source_title:
                    findings.append(
                        Finding(
                            "ROOM_OWNER_SOURCE_TITLE_DRIFT",
                            "BLOCKER",
                            f"{room_rel}/{source_candidate.as_posix()}",
                            "Il titolo della fonte operativa non identifica la stanza "
                            "dichiarata nella mappa madre.",
                        )
                    )
                if re.search(r"\{\{[^{}]+\}\}", source_text):
                    findings.append(
                        Finding(
                            "ROOM_OWNER_SOURCE_PLACEHOLDER",
                            "BLOCKER",
                            f"{room_rel}/{source_candidate.as_posix()}",
                            "La fonte operativa conserva campi del calco non compilati.",
                        )
                    )
                headings = _markdown_headings(source_text)
                expected = ROOM_LIFECYCLE.owner_source_headings
                duplicates = [
                    heading for heading in expected if headings.count(heading) > 1
                ]
                if duplicates:
                    findings.append(
                        Finding(
                            "ROOM_OWNER_SOURCE_SECTION_DUPLICATE",
                            "BLOCKER",
                            f"{room_rel}/{source_candidate.as_posix()}",
                            "Sezioni operative duplicate: " + ", ".join(duplicates) + ".",
                        )
                    )
                missing = [heading for heading in expected if heading not in headings]
                empty = [
                    heading
                    for heading in expected
                    if heading in headings and not _markdown_section(source_text, heading)
                ]
                unproven = [
                    heading
                    for heading in expected
                    if heading in headings
                    and _contains_unproven_value(
                        _markdown_section(source_raw_text, heading)
                    )
                ]
                wrong_order = headings[: len(expected)] != expected
                if missing or empty or unproven or wrong_order:
                    details: list[str] = []
                    if missing:
                        details.append("sezioni mancanti: " + ", ".join(missing))
                    if empty:
                        details.append("sezioni vuote: " + ", ".join(empty))
                    if unproven:
                        details.append(
                            "sezioni non compilate: " + ", ".join(unproven)
                        )
                    if wrong_order:
                        details.append("le sezioni operative non sono in testa e in ordine")
                    findings.append(
                        Finding(
                            "ROOM_OWNER_SOURCE_INCOMPLETE",
                            "BLOCKER",
                            f"{room_rel}/{source_candidate.as_posix()}",
                            "; ".join(details).capitalize() + ".",
                        )
                    )

    business_declaration, business_candidate = _business_source_declaration(content)
    if business_declaration in {"missing", "invalid", "multiple"}:
        findings.append(
            Finding(
                "ROOM_BUSINESS_SOURCE_VALUE_MISSING",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "La sezione Fonte business editabile non contiene un valore "
                "compilato o un NON APPLICABILE motivato.",
            )
        )
    elif business_declaration == "file" and business_candidate is not None:
        issue = _business_source_file_issue(room_path, business_candidate)
        issue_codes = {
            "symlink": "ROOM_BUSINESS_SOURCE_SYMLINK",
            "missing": "ROOM_BUSINESS_SOURCE_MISSING",
            "unreadable": "ROOM_BUSINESS_SOURCE_UNREADABLE",
            "empty": "ROOM_BUSINESS_SOURCE_EMPTY",
            "placeholder": "ROOM_BUSINESS_SOURCE_PLACEHOLDER",
        }
        issue_details = {
            "symlink": "La fonte business deve essere un file locale.",
            "missing": "La fonte business dichiarata non esiste.",
            "unreadable": "La fonte business non e' leggibile come testo UTF-8.",
            "empty": "La fonte business dichiarata e' vuota.",
            "placeholder": "La fonte business conserva campi non compilati.",
        }
        if issue:
            findings.append(
                Finding(
                    issue_codes[issue],
                    "BLOCKER",
                    f"{room_rel}/{business_candidate.as_posix()}",
                    issue_details[issue],
                )
            )
        if (
            source_candidate is not None
            and business_candidate.as_posix().casefold()
            == source_candidate.as_posix().casefold()
        ):
            findings.append(
                Finding(
                    "ROOM_SOURCE_ROLE_CONFLICT",
                    "BLOCKER",
                    f"{room_rel}/{business_candidate.as_posix()}",
                    "Fonte operativa e fonte business hanno responsabilita' "
                    "diverse e non possono essere lo stesso file.",
                )
            )

    contents = _markdown_section(content, ROOM_LIFECYCLE.contents_section)
    declared_children: dict[str, str] = {}
    invalid_child_declarations: list[str] = []
    for raw in re.findall(r"`([^`]+)`", contents):
        normalized_path = raw.strip().replace("\\", "/")
        if not normalized_path.endswith("/"):
            continue
        canonical = _canonical_relative_path(normalized_path)
        candidate = Path(canonical) if canonical else None
        if candidate is None or len(candidate.parts) != 1:
            invalid_child_declarations.append(raw)
            continue
        direct_name = candidate.parts[0]
        declared_children[direct_name.casefold()] = direct_name
    if invalid_child_declarations:
        findings.append(
            Finding(
                "ROOM_CHILD_DECLARATION_INVALID",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "Dentro ammette soltanto nomi relativi di sottocartelle dirette.",
            )
        )
    content_values = [
        match.group(1).strip()
        for line in contents.splitlines()
        if (match := re.match(r"^\s*-\s+(.+?)\s*$", line))
    ]
    no_children_declared = any(
        _normalized(value).strip() == "nessuna sottocartella"
        for value in content_values
    )
    if not declared_children and not no_children_declared:
        findings.append(
            Finding(
                "ROOM_CONTENTS_UNDECLARED",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "La sezione Dentro non dichiara sottocartelle reali ne' "
                "l'assenza esplicita di sottocartelle.",
            )
        )
    if declared_children and no_children_declared:
        findings.append(
            Finding(
                "ROOM_CONTENTS_CONFLICT",
                "BLOCKER",
                f"{room_rel}/{ROOM_MAP_FILE}",
                "La sezione Dentro dichiara insieme sottocartelle e la loro assenza.",
            )
        )
    for declared in sorted(declared_children.values(), key=str.casefold):
        child = room_path / declared
        if not child.is_dir() and not child.is_symlink():
            findings.append(
                Finding(
                    "ROOM_CHILD_DECLARED_MISSING",
                    "BLOCKER",
                    f"{room_rel}/{declared}",
                    "La mappa dichiara una sottocartella che non esiste.",
                )
            )

    direct_children = sorted(room_path.iterdir(), key=lambda item: item.name.casefold())
    for child in direct_children:
        if (
            child.name in IGNORED_OS_ENTRIES
            or child.name.casefold() in IGNORED_ROOM_DIRS
        ):
            continue
        if child.is_symlink():
            continue
        if child.is_dir() and child.name.casefold() not in declared_children:
            findings.append(
                Finding(
                    "ROOM_CHILD_UNDECLARED",
                    "BLOCKER",
                    f"{room_rel}/{child.name}",
                    "Sottocartella senza proprietario: dichiararla in Dentro "
                    "oppure ricondurla alla stanza corretta.",
                )
            )

    frontier: list[tuple[Path, int]] = [(room_path, 0)]
    seen_symlinks: set[str] = set()
    seen_unreadable: set[str] = set()
    while frontier:
        parent, depth = frontier.pop(0)
        try:
            children = sorted(parent.iterdir(), key=lambda item: item.name.casefold())
        except OSError:
            rel_text = parent.relative_to(room_path).as_posix()
            if rel_text != "." and rel_text not in seen_unreadable:
                findings.append(
                    Finding(
                        "ROOM_CHILD_UNREADABLE",
                        "BLOCKER",
                        f"{room_rel}/{rel_text}",
                        "La sottocartella non e' leggibile: il collaudo non puo' "
                        "verificare cosa contiene.",
                    )
                )
                seen_unreadable.add(rel_text)
            continue
        for child in children:
            rel = child.relative_to(room_path)
            if any(
                part in IGNORED_OS_ENTRIES
                or part.casefold() in IGNORED_ROOM_DIRS
                for part in rel.parts
            ):
                continue
            rel_text = rel.as_posix()
            if child.is_symlink():
                if rel_text not in seen_symlinks:
                    findings.append(
                        Finding(
                            "ROOM_CHILD_SYMLINK",
                            "BLOCKER",
                            f"{room_rel}/{rel_text}",
                            "Una stanza non puo' delegare il proprio contenuto "
                            "a un collegamento simbolico.",
                        )
                    )
                    seen_symlinks.add(rel_text)
                continue
            if not child.is_dir():
                continue
            child_depth = depth + 1
            if child_depth > ROOM_LIFECYCLE.scan_depth:
                findings.append(
                    Finding(
                        "ROOM_CHILD_TOO_DEEP",
                        "BLOCKER",
                        f"{room_rel}/{rel_text}",
                        "La stanza supera i due livelli ammessi dal contratto.",
                    )
                )
                continue
            if _normalized(child.name) in GENERIC_NAMES:
                findings.append(
                    Finding(
                        "ROOM_CHILD_GENERIC",
                        "BLOCKER",
                        f"{room_rel}/{rel_text}",
                        "Nome generico: assegnare una funzione concreta alla cartella.",
                    )
                )
            if _is_empty_dir(child):
                findings.append(
                    Finding(
                        "ROOM_CHILD_EMPTY",
                        "BLOCKER",
                        f"{room_rel}/{rel_text}",
                        "Cartella vuota: non costituisce contenuto vivo della stanza.",
                    )
                )
            frontier.append((child, child_depth))
    return findings


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


def _root_registry_structure_findings(target: Path, content: str) -> list[Finding]:
    findings: list[Finding] = []
    specifications = (
        (
            "### Registro delle stanze",
            (
                "stanza",
                "scopo",
                "a monte",
                "a valle",
                "fonti",
                "output",
                "capacita'",
                "mappa locale",
                "amministratore",
                "riporta al",
            ),
            "ROOT_ROOM_REGISTRY",
        ),
        (
            "### Elementi posseduti direttamente dalla cartella madre",
            ("percorso", "classe", "uso", "registro di dettaglio"),
            "ROOT_OWNED_REGISTRY",
        ),
    )
    for marker, expected_header, code_prefix in specifications:
        count = len(
            re.findall(
                rf"(?m)^[ ]{{0,3}}{re.escape(marker)}[ \t]*$",
                content,
            )
        )
        if count != 1:
            findings.append(
                Finding(
                    f"{code_prefix}_{'MISSING' if count == 0 else 'DUPLICATE'}",
                    "BLOCKER",
                    "AGENTS.md",
                    "La mappa madre deve contenere una sola sezione "
                    f"`{marker.removeprefix('### ')}`.",
                )
            )
            continue
        table_lines = _table_block_after_marker(content, marker)
        header = tuple(_normalized(cell).strip() for cell in _table_cells(table_lines[0])) if table_lines else ()
        separator_ok = (
            len(table_lines) >= 2
            and len(_table_cells(table_lines[1])) == len(expected_header)
            and all(
                set(cell) <= {"-", ":", " "}
                for cell in _table_cells(table_lines[1])
            )
        )
        malformed_rows = [
            index + 3
            for index, line in enumerate(table_lines[2:])
            if len(_table_cells(line)) != len(expected_header)
        ]
        if header != expected_header or not separator_ok or malformed_rows:
            findings.append(
                Finding(
                    f"{code_prefix}_SCHEMA_INVALID",
                    "BLOCKER",
                    "AGENTS.md",
                    "La tabella della mappa madre non rispetta colonne, "
                    "separatore e righe previsti dal contratto.",
                )
            )
    return findings


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
    agents_text = ""
    if agents_path.is_file() and not agents_path.is_symlink():
        try:
            agents_text = agents_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            findings.append(
                Finding(
                    "ROOT_MAP_UNREADABLE",
                    "BLOCKER",
                    "AGENTS.md",
                    "La mappa madre non e' leggibile come testo UTF-8.",
                )
            )
    active_agents_text = _active_markdown(agents_text)
    normalized_agents = _normalized(active_agents_text)
    findings.extend(_root_registry_structure_findings(target, active_agents_text))
    if (
        _normalized(ORGANIZATION.root_role) not in normalized_agents
        or "governa l'organigramma" not in normalized_agents
        or _negates_claim(
            normalized_agents,
            (ORGANIZATION.root_role, "governa l'organigramma"),
        )
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
        findings.extend(_guardiano_findings(target, requested_mode))
    findings.extend(_ecosystem_registry_findings(target))
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
    if root_bridge.is_file() and not root_bridge.is_symlink():
        try:
            root_bridge_content = root_bridge.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            findings.append(
                Finding(
                    "ROOT_BRIDGE_UNREADABLE",
                    "BLOCKER",
                    "CLAUDE.md",
                    "Il ponte radice non e' leggibile come testo UTF-8.",
                )
            )
        else:
            if root_bridge_content != CLAUDE_BRIDGE:
                findings.append(
                    Finding(
                        "INVALID_ROOT_BRIDGE",
                        "BLOCKER",
                        "CLAUDE.md",
                        "Il ponte deve contenere soltanto @AGENTS.md.",
                    )
                )

    legacy_mission_file = target / "REPORT_FINALE.md"
    if legacy_mission_file.exists() or legacy_mission_file.is_symlink():
        findings.append(
            Finding(
                "LEGACY_MISSION_FILE",
                "BLOCKER",
                "REPORT_FINALE.md",
                "Promuovere i fatti correnti nelle fonti proprietarie e spostare "
                "il file superato nel Cestino.",
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
    required_text_paths: dict[str, Path] = {
        rel: target / rel for rel in required_files
    }
    memory_index = canonical_memory / "MEMORY.md"
    try:
        memory_label = memory_index.relative_to(target).as_posix()
    except ValueError:
        memory_label = str(memory_index)
    required_text_paths[memory_label] = memory_index
    for rel, path in sorted(required_text_paths.items()):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            findings.append(
                Finding(
                    "REQUIRED_TEXT_UNREADABLE",
                    "BLOCKER",
                    rel,
                    "Un file portante dello standard non e' leggibile come "
                    "testo UTF-8.",
                )
            )
    findings.extend(_memory_merge_reference_findings(target, canonical_memory))
    rooms = parse_room_registry(active_agents_text)

    seen_paths: set[str] = set()
    seen_names: set[str] = set()
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
        room_path_key = _normalized(room.path).strip()
        if room_path_key in seen_paths:
            findings.append(
                Finding(
                    "DUPLICATE_ROOM_PATH",
                    "BLOCKER",
                    room.path,
                    "La stessa stanza compare piu' volte nella mappa madre.",
                )
            )
        seen_paths.add(room_path_key)

        if len(Path(room.path).parts) != 1 or room.path.startswith("."):
            findings.append(
                Finding(
                    "ROOM_PATH_NOT_TOP_LEVEL",
                    "BLOCKER",
                    room.path,
                    "Una stanza vive come cartella visibile accanto all'armadio "
                    "ecosistema, non dentro un altro ramo.",
                )
            )
        standard_room_paths = {
            _normalized(name) for name in ROOM_LIFECYCLE.standard_room_paths
        }
        if (
            _normalized(room.path)
            in {_normalized(name) for name in STANDARD_DIRS | ALLOWED_ROOT_FILES}
            and _normalized(room.path) not in standard_room_paths
        ):
            findings.append(
                Finding(
                    "ROOM_STANDARD_COLLISION",
                    "BLOCKER",
                    room.path,
                    "Un elemento del telaio standard non puo' diventare una "
                    "stanza business.",
                )
            )

        room_name_key = _normalized(room.name).strip()
        if (
            room_name_key in {"", "stanza", "da censire"}
            or _contains_unproven_value(room_name_key)
        ):
            findings.append(
                Finding(
                    "ROOM_NAME_UNPROVEN",
                    "BLOCKER",
                    room.path,
                    "La riga della stanza non dichiara un nome business reale.",
                )
            )
        elif room_name_key in seen_names:
            findings.append(
                Finding(
                    "DUPLICATE_ROOM_NAME",
                    "BLOCKER",
                    room.path,
                    "Due stanze dichiarano lo stesso nome business.",
                )
            )
        seen_names.add(room_name_key)

        purpose_key = _normalized(room.purpose).strip()
        if (
            purpose_key in {"", "-", "non applicabile"}
            or _contains_unproven_value(purpose_key)
        ):
            findings.append(
                Finding(
                    "ROOM_PURPOSE_UNPROVEN",
                    "BLOCKER",
                    room.path,
                    "La riga della stanza non dichiara una responsabilita' "
                    "business concreta.",
                )
            )

        registry_fields = {
            "A monte": room.upstream,
            "A valle": room.downstream,
            "Fonti": room.sources,
            "Output": room.outputs,
            "Capacita'": room.capabilities,
        }
        unproven_registry_fields = [
            label
            for label, value in registry_fields.items()
            if (
                not _field_value(value)
                or _field_value(value) in {"-", "non applicabile"}
                or _contains_unproven_value(value)
            )
        ]
        if unproven_registry_fields:
            findings.append(
                Finding(
                    "ROOM_REGISTRY_FIELDS_UNPROVEN",
                    "BLOCKER",
                    room.path,
                    "La riga della stanza conserva campi non compilati: "
                    + ", ".join(unproven_registry_fields)
                    + ".",
                )
            )

        expected_map_path = f"{room.path}/{ROOM_MAP_FILE}"
        actual_map_path = room.map_path.replace("\\", "/").strip("/")
        if actual_map_path != expected_map_path:
            findings.append(
                Finding(
                    "ROOM_MAP_ROUTE_INVALID",
                    "BLOCKER",
                    room.path,
                    "La mappa locale dichiarata deve essere esattamente "
                    f"`{expected_map_path}`.",
                )
            )

        administrator_key = _normalized(room.administrator).strip()
        if (
            not administrator_key
            or "da assegnare" in administrator_key
            or "non applicabile" in administrator_key
            or _contains_unproven_value(administrator_key)
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

        room_agents = room_path / ROOM_MAP_FILE
        room_claude = room_path / ROOM_BRIDGE_FILE
        if room_agents.is_symlink():
            findings.append(
                Finding(
                    "ROOM_MAP_SYMLINK",
                    "BLOCKER",
                    f"{room.path}/{ROOM_MAP_FILE}",
                    "La mappa della stanza deve essere un file locale.",
                )
            )
        elif not room_agents.is_file():
            findings.append(
                Finding(
                    "ROOM_AGENTS_MISSING",
                    "BLOCKER",
                    f"{room.path}/{ROOM_MAP_FILE}",
                    "La stanza non ha la propria mappa locale.",
                )
            )
        else:
            try:
                raw_content = _active_markdown(
                    room_agents.read_text(encoding="utf-8")
                )
            except (OSError, UnicodeError):
                findings.append(
                    Finding(
                        "ROOM_MAP_UNREADABLE",
                        "BLOCKER",
                        f"{room.path}/{ROOM_MAP_FILE}",
                        "La mappa locale non e' leggibile come testo UTF-8.",
                    )
                )
            else:
                content = _normalized(raw_content)
                heading_list = _markdown_headings(content)
                headings = set(heading_list)
                missing_sections = [
                    section
                    for section in ROOM_REQUIRED_SECTIONS
                    if section not in headings
                ]
                empty_sections = [
                    section
                    for section in ROOM_REQUIRED_SECTIONS
                    if section in headings
                    and not _markdown_section(raw_content, section)
                ]
                unproven_sections = [
                    section
                    for section in ROOM_REQUIRED_SECTIONS
                    if section in headings
                    and _contains_unproven_value(
                        _markdown_section(raw_content, section)
                    )
                ]
                organization_section = _normalized(
                    _markdown_section(
                        raw_content,
                        ROOM_LIFECYCLE.required_terms_section,
                    )
                )
                local_title_match = re.search(r"(?m)^#\s+(.+?)\s*$", raw_content)
                local_title = (
                    _normalized(local_title_match.group(1)).strip()
                    if local_title_match
                    else ""
                )
                local_purpose = _normalized(
                    _markdown_section(raw_content, "scopo")
                ).strip()
                if local_title != room_name_key:
                    findings.append(
                        Finding(
                            "ROOM_NAME_DRIFT",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "Il nome della mappa locale non coincide con la riga "
                            "della mappa madre.",
                        )
                    )
                if local_purpose != purpose_key:
                    findings.append(
                        Finding(
                            "ROOM_PURPOSE_DRIFT",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "Lo scopo della mappa locale non coincide con la riga "
                            "della mappa madre.",
                        )
                    )
                local_registry_fields = {
                    "A monte": ("a monte", room.upstream),
                    "A valle": ("a valle", room.downstream),
                    "Fonti": ("fonti", room.sources),
                    "Output": ("output", room.outputs),
                    "Capacita'": ("capacita", room.capabilities),
                }
                drifted_registry_fields: list[str] = []
                for label, (section_name, root_value) in local_registry_fields.items():
                    local_values = _markdown_bullets(
                        _markdown_section(raw_content, section_name)
                    )
                    if (
                        len(local_values) != 1
                        or _field_value(local_values[0]) != _field_value(root_value)
                    ):
                        drifted_registry_fields.append(label)
                if drifted_registry_fields:
                    findings.append(
                        Finding(
                            "ROOM_REGISTRY_FIELD_DRIFT",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "I campi della mappa locale non coincidono con la riga "
                            "madre: "
                            + ", ".join(drifted_registry_fields)
                            + ".",
                        )
                    )
                if room_name_key and room_name_key not in organization_section:
                    findings.append(
                        Finding(
                            "ROOM_ORGANIZATION_NAME_DRIFT",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "L'amministratore locale non identifica la propria stanza.",
                        )
                    )
                missing_terms = [
                    term
                    for term in ROOM_REQUIRED_TERMS
                    if term not in organization_section
                ]
                organization_negated = _negates_claim(
                    organization_section,
                    tuple(ROOM_REQUIRED_TERMS),
                ) or _organization_route_is_negated(organization_section)
                duplicate_sections = [
                    section
                    for section in ROOM_REQUIRED_SECTIONS
                    if heading_list.count(section) > 1
                ]
                if duplicate_sections:
                    findings.append(
                        Finding(
                            "ROOM_MAP_SECTION_DUPLICATE",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "Sezioni contrattuali duplicate: "
                            + ", ".join(duplicate_sections)
                            + ".",
                        )
                    )
                if (
                    missing_sections
                    or empty_sections
                    or unproven_sections
                    or missing_terms
                    or organization_negated
                ):
                    details: list[str] = []
                    if missing_sections:
                        details.append("sezioni mancanti: " + ", ".join(missing_sections))
                    if empty_sections:
                        details.append("sezioni vuote: " + ", ".join(empty_sections))
                    if unproven_sections:
                        details.append(
                            "sezioni non compilate: "
                            + ", ".join(unproven_sections)
                        )
                    if missing_terms:
                        details.append("vincoli mancanti: " + ", ".join(missing_terms))
                    if organization_negated:
                        details.append("l'organigramma nega ruoli o riporto dichiarati")
                    findings.append(
                        Finding(
                            "ROOM_MAP_INCOMPLETE",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "; ".join(details).capitalize() + ".",
                        )
                    )
                if not _room_business_responsibility_is_proven(raw_content):
                    findings.append(
                        Finding(
                            "ROOM_BUSINESS_RESPONSIBILITY_UNPROVEN",
                            "BLOCKER",
                            f"{room.path}/{ROOM_MAP_FILE}",
                            "La mappa non prova una responsabilita' business reale "
                            "con stato e decisioni: script, modelli e output non "
                            "bastano a dimostrare una stanza.",
                        )
                    )
                findings.extend(
                    _room_prefab_findings(
                        target,
                        room_path,
                        raw_content,
                        room.name,
                    )
                )
        if room_claude.is_symlink():
            findings.append(
                Finding(
                    "ROOM_BRIDGE_SYMLINK",
                    "BLOCKER",
                    f"{room.path}/{ROOM_BRIDGE_FILE}",
                    "Il ponte della stanza deve essere un file locale.",
                )
            )
        elif not room_claude.is_file():
            findings.append(
                Finding(
                    "ROOM_CLAUDE_MISSING",
                    "BLOCKER",
                    f"{room.path}/{ROOM_BRIDGE_FILE}",
                    "La stanza non ha il ponte verso AGENTS.md.",
                )
            )
        else:
            try:
                bridge_content = room_claude.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                findings.append(
                    Finding(
                        "ROOM_BRIDGE_UNREADABLE",
                        "BLOCKER",
                        f"{room.path}/{ROOM_BRIDGE_FILE}",
                        "Il ponte non e' leggibile come testo UTF-8.",
                    )
                )
            else:
                if bridge_content != CLAUDE_BRIDGE:
                    findings.append(
                        Finding(
                            "ROOM_CLAUDE_INVALID",
                            "BLOCKER",
                            f"{room.path}/{ROOM_BRIDGE_FILE}",
                            "Il ponte deve contenere soltanto @AGENTS.md.",
                        )
                    )

    root_owned_rows = parse_root_owned_rows(active_agents_text)
    seen_root_owned: set[str] = set()
    for row in root_owned_rows:
        if not row.path:
            findings.append(
                Finding(
                    "ROOT_OWNED_PATH_INVALID",
                    "BLOCKER",
                    "AGENTS.md",
                    "Il registro madre contiene un percorso non relativo o non sicuro.",
                )
            )
            continue
        path_key = _normalized(row.path).strip()
        if path_key in seen_root_owned:
            findings.append(
                Finding(
                    "DUPLICATE_ROOT_OWNED_PATH",
                    "BLOCKER",
                    row.path,
                    "Lo stesso percorso compare piu' volte nel registro della "
                    "cartella madre.",
                )
            )
        seen_root_owned.add(path_key)
    root_owned = {row.path: row for row in root_owned_rows if row.path}
    allowed_classes = {
        _normalized(classification)
        for classification in ROOM_LIFECYCLE.root_owned_classifications
    }
    allowed_registries = set(ROOM_LIFECYCLE.root_owned_registry_paths)
    standard_owned_names = {
        _normalized(name) for name in STANDARD_DIRS | ALLOWED_ROOT_FILES
    }
    room_path_keys = {
        _normalized(room.path).strip() for room in rooms if room.path
    }
    registry_markers = {
        "ecosistema/ASSET.md": "## Registro",
        "ecosistema/FONTI.md": "## Fonti trovate",
    }
    registry_text_cache: dict[str, str | None] = {}
    valid_root_owned_paths: set[str] = set()
    for path, row in sorted(root_owned.items()):
        classification_key = _normalized(row.classification).strip()
        direct_path = len(Path(path).parts) == 1 and not path.startswith(".")
        if not direct_path:
            findings.append(
                Finding(
                    "ROOT_OWNED_PATH_NOT_DIRECT",
                    "BLOCKER",
                    path,
                    "Il registro della cartella madre ammette soltanto elementi "
                    "visibili direttamente nella sua radice.",
                )
            )
        elif _normalized(path) in standard_owned_names:
            findings.append(
                Finding(
                    "ROOT_OWNED_STANDARD_COLLISION",
                    "BLOCKER",
                    path,
                    "Un elemento del telaio standard non puo' ricevere una "
                    "seconda proprieta' business nel registro madre.",
                )
            )
        else:
            valid_root_owned_paths.add(path)
        if _normalized(path).strip() in room_path_keys:
            findings.append(
                Finding(
                    "ROOM_OWNERSHIP_CONFLICT",
                    "BLOCKER",
                    path,
                    "Lo stesso elemento non puo' essere insieme stanza e asset "
                    "posseduto dalla cartella madre.",
                )
            )
        if classification_key == "sospetta":
            findings.append(
                Finding(
                    "ROOT_OWNED_CLASS_UNRESOLVED",
                    "BLOCKER",
                    path,
                    "L'elemento e' ancora classificato come SOSPETTA: va risolto "
                    "prima del collaudo.",
                )
            )
        elif classification_key not in allowed_classes:
            findings.append(
                Finding(
                    "ROOT_OWNED_CLASS_INVALID",
                    "BLOCKER",
                    path,
                    "Classe non ammessa dal contratto: "
                    f"{row.classification or 'vuota'}.",
                )
            )
        usage_key = _normalized(row.usage).strip()
        if (
            not usage_key
            or usage_key in {"-", "non applicabile"}
            or _contains_unproven_value(usage_key)
        ):
            findings.append(
                Finding(
                    "ROOT_OWNED_USAGE_UNPROVEN",
                    "BLOCKER",
                    path,
                    "L'elemento non dichiara un uso business concreto.",
                )
            )
        registry_path = _canonical_relative_path(row.registry_path)
        if registry_path not in allowed_registries:
            findings.append(
                Finding(
                    "ROOT_OWNED_REGISTRY_INVALID",
                    "BLOCKER",
                    path,
                    "Il registro di dettaglio deve essere uno dei registri "
                    "comuni ammessi dal contratto.",
                )
            )
        elif (
            _symlink_component(target, registry_path) is not None
            or not (target / registry_path).is_file()
        ):
            findings.append(
                Finding(
                    "ROOT_OWNED_REGISTRY_MISSING",
                    "BLOCKER",
                    registry_path,
                    "Il registro di dettaglio dichiarato non esiste come file locale.",
                )
            )
        else:
            if registry_path not in registry_text_cache:
                try:
                    registry_text_cache[registry_path] = (
                        target / registry_path
                    ).read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    registry_text_cache[registry_path] = None
            registry_text = registry_text_cache[registry_path]
            if registry_text is None:
                findings.append(
                    Finding(
                        "ROOT_OWNED_REGISTRY_UNREADABLE",
                        "BLOCKER",
                        registry_path,
                        "Il registro di dettaglio non e' leggibile come testo UTF-8.",
                    )
                )
            elif not _registry_has_entry(
                registry_text,
                registry_markers[registry_path],
                path,
            ):
                findings.append(
                    Finding(
                        "ROOT_OWNED_DETAIL_MISSING",
                        "BLOCKER",
                        registry_path,
                        "L'elemento dichiarato nella mappa madre non compare nel "
                        "registro di dettaglio indicato.",
                    )
                )
        linked = _symlink_component(target, path)
        owned_path = target / path
        if linked is not None:
            findings.append(
                Finding(
                    "ROOT_OWNED_PATH_SYMLINK",
                    "BLOCKER",
                    path,
                    "Un elemento posseduto dalla cartella madre deve essere "
                    "locale e non un collegamento simbolico.",
                )
            )
        elif not owned_path.exists():
            findings.append(
                Finding(
                    "ROOT_OWNED_PATH_MISSING",
                    "BLOCKER",
                    path,
                    "La mappa madre dichiara un elemento che non esiste.",
                )
            )
    declared_room_paths = {
        room.path
        for room in rooms
        if room.path
        and len(Path(room.path).parts) == 1
        and not room.path.startswith(".")
    }
    declared_paths = declared_room_paths | valid_root_owned_paths
    declared_top_levels = {Path(path).parts[0] for path in declared_paths}
    for child in sorted(target.iterdir(), key=lambda item: item.name.casefold()):
        if not child.is_dir() or child.name in STANDARD_DIRS:
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
        if not child.is_file() or child.name in IGNORED_OS_ENTRIES:
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

    for child in sorted(target.iterdir(), key=lambda item: item.name.casefold()):
        if child.name in IGNORED_OS_ENTRIES:
            continue
        if _hidden_from_owner(child):
            findings.append(
                Finding(
                    "HIDDEN_FROM_OWNER",
                    "BLOCKER",
                    child.name,
                    "Percorso con flag di invisibilita': il proprietario non lo vede nel Finder/Explorer.",
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
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                findings.append(
                    Finding(
                        "INSPECTOR_SKILL_UNREADABLE",
                        "BLOCKER",
                        rel,
                        "La skill non e' leggibile come testo UTF-8.",
                    )
                )
            else:
                if (
                    "CHECKUP.md" not in content
                    or "ispettore-ecosistema" not in content
                ):
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
            except (OSError, UnicodeError, json.JSONDecodeError):
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
            except (OSError, UnicodeError, json.JSONDecodeError):
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
    asset_registry = ""
    if asset_registry_path.is_file():
        try:
            asset_registry = _normalized(
                asset_registry_path.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError):
            findings.append(
                Finding(
                    "ASSET_REGISTRY_UNREADABLE",
                    "BLOCKER",
                    "ecosistema/ASSET.md",
                    "Il registro asset non e' leggibile come testo UTF-8.",
                )
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
        try:
            issue = _project_control_issue(path)
        except (OSError, UnicodeError):
            findings.append(
                Finding(
                    "PROJECT_CONTROL_UNREADABLE",
                    "BLOCKER",
                    rel.as_posix(),
                    "Il file progetto non e' leggibile come testo UTF-8.",
                )
            )
            continue
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
