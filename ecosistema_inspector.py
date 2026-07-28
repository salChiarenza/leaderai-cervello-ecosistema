#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


CLAUDE_BRIDGE = "@AGENTS.md\n"

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
    "REPORT_FINALE.md",
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
    "scopo",
    "dentro",
    "fonti",
    "output",
    "capacita",
    "a monte",
    "a valle",
    "dove scrivere",
)


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

    return Inspection(target=str(target), rooms=rooms, findings=findings)


def _markdown(inspection: Inspection) -> str:
    lines = [
        "# Ispettore Ecosistema",
        "",
        f"- Cartella viva: `{inspection.target}`",
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
