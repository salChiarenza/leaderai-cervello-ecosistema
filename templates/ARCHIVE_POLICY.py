"""Politica condivisa Ispettore/guardiano: archivi di lavoro, mai esenzioni ai segreti.

Componente del controllore del prodotto; il contratto lo installa accanto al guardiano.
Non legge il contenuto dei fascicoli: verifica percorsi e protezione Git.
"""
from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class Archive:
    path: Path
    signatures: bool = False


def active_markdown(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", text)


def declarations(text: str) -> list[tuple[str, bool]]:
    """Unica sintassi, solo righe effettive della sezione Dentro."""
    text = active_markdown(text)
    section = re.search(r"(?ims)^## Dentro\s*\n(.*?)(?=^## |\Z)", text)
    if not section:
        return []
    result = []
    for line in section[1].splitlines():
        match = re.match(r"^\s*-\s+`([^`]+)`\s*[-—:]\s*ARCHIVIO PROTETTO:\s*(\S.*)$", line, re.I)
        if match:
            result.append((match[1], bool(re.search(r"(?:^|;)\s*FIRME SOTTOSCRITTORI\s*\.?$", match[2], re.I))))
    return result


def safe_relative(raw: str) -> Path | None:
    if not raw or raw.startswith("/") or any(c in raw for c in "\\:*?[]\n\r\t"):
        return None
    parts = raw.rstrip("/").split("/")
    if any(not p or p in {".", "..", "@"} or p.startswith(".") or p.rstrip(" .") != p for p in parts):
        return None
    return Path(*parts)


def inside(path: Path, archives: list[Archive] | tuple[Archive, ...]) -> bool:
    return any(path == a.path or a.path in path.parents for a in archives)


def collect(root: Path) -> tuple[list[Archive], list[tuple[str, str, str]]]:
    archives, issues = [], []
    for room in sorted(root.iterdir()):
        if room.is_symlink() or not room.is_dir() or room.name.startswith("."):
            continue
        map_path = room / "AGENTS.md"
        if map_path.is_symlink() or not map_path.is_file():
            continue
        try:
            rows = declarations(map_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            continue  # la leggibilita' della mappa e' gia' controllata dal chiamante
        seen = set()
        for raw, signatures in rows:
            rel = safe_relative(raw)
            label = f"{room.name}/{raw}"
            errors = []
            if rel is None:
                issues.append(("PROTECTED_ARCHIVE_INVALID", label, "Archivio: percorso relativo locale non valido."))
                continue
            path = room / rel
            if rel.as_posix().casefold() in seen:
                issues.append(("PROTECTED_ARCHIVE_INVALID", label, "Archivio dichiarato piu' volte."))
                continue
            seen.add(rel.as_posix().casefold())
            current = room
            for part in rel.parts:
                current = current / part
                if current.is_symlink():
                    errors.append(("PROTECTED_ARCHIVE_SYMLINK", label, "Archivio collegato: ogni componente deve restare locale."))
                    break
            if not errors and not path.is_dir():
                errors.append(("PROTECTED_ARCHIVE_MISSING", label, "Archivio dichiarato ma assente."))
            entries = [path.relative_to(root).as_posix() + "/"]
            if not errors:
                def walk_error(exc):
                    errors.append(("PROTECTED_ARCHIVE_UNREADABLE", label, "Archivio non interamente leggibile."))
                for parent, dirs, files in os.walk(path, followlinks=False, onerror=walk_error):
                    for name in dirs + files:
                        child = Path(parent) / name
                        if child.is_symlink():
                            errors.append(("PROTECTED_ARCHIVE_SYMLINK", child.relative_to(root).as_posix(), "Collegamento dentro l'archivio: protezione non verificabile."))
                        else:
                            entries.append(child.relative_to(root).as_posix() + ("/" if name in dirs else ""))
                    dirs[:] = [d for d in dirs if not (Path(parent) / d).is_symlink()]
                try:
                    ignored = subprocess.run(["git", "check-ignore", "--no-index", "-z", "--stdin"], cwd=root,
                        input="\0".join(entries).encode("utf-8") + b"\0", capture_output=True, timeout=10)
                    ignored_paths = {p.decode("utf-8") for p in ignored.stdout.split(b"\0") if p}
                    if ignored.returncode not in (0, 1) or not set(entries).issubset(ignored_paths):
                        errors.append(("PROTECTED_ARCHIVE_UNPROTECTED", label, "L'archivio e tutti i suoi elementi devono essere esclusi da Git."))
                    tracked = subprocess.run(["git", "ls-files", "-z", "--", path.relative_to(root).as_posix()], cwd=root, capture_output=True, timeout=10)
                    history = subprocess.run(["git", "log", "--all", "--format=", "--name-only", "--", path.relative_to(root).as_posix()], cwd=root, capture_output=True, timeout=10)
                    if tracked.returncode or history.returncode:
                        errors.append(("PROTECTED_ARCHIVE_UNPROTECTED", label, "Indice o storia Git non verificabili."))
                    elif tracked.stdout or history.stdout.strip():
                        errors.append(("PROTECTED_ARCHIVE_TRACKED", label, "Dati presenti nell'indice o nella storia Git: l'esposizione resta da risolvere."))
                except (OSError, subprocess.TimeoutExpired, UnicodeError):
                    errors.append(("PROTECTED_ARCHIVE_UNPROTECTED", label, "Protezione Git non verificabile."))
            issues.extend(errors)
            if not errors:
                archives.append(Archive(path, signatures))
    return archives, issues


def family_signature(path: Path, archives: list[Archive]) -> bool:
    if path.name != "firma.png" or path.is_symlink():
        return False
    for archive in archives:
        if not archive.signatures or archive.path not in path.parents or path.parent == archive.path:
            continue
        try:
            return any(p.suffix.casefold() == ".pdf" and p.is_file() and not p.is_symlink() for p in path.parent.iterdir())
        except OSError:
            return False
    return False


SKIP_DIRS = {".git", ".agent", ".agents", ".codex", ".claude", ".venv", "venv", "node_modules", "__pycache__", ".secrets", "vendor"}
ROUTERS = {"AGENTS.md", "MEMORY.md", "AGENT_CHAT.md"}


def scan(root: Path, archives=None, errors=None) -> list[str]:
    """Una camminata strutturale, niente processi wc/stat per ogni documento."""
    if archives is None:
        archives, errors = collect(root)
    issues = [f"{path} - {detail}" for _, path, detail in errors]
    cutoff = (datetime.now() - timedelta(days=2)).strftime("%Y%m%d")
    def walk_error(exc):
        issues.append(f"{exc.filename} - percorso non leggibile dal guardiano")
    for parent, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        parent = Path(parent)
        for name in dirs + files:
            path = parent / name
            rel = path.relative_to(root)
            if path.is_symlink():
                continue
            if len(rel.parts) <= 2 and not any(p.startswith(".") for p in rel.parts):
                info = path.stat()
                if (getattr(info, "st_flags", 0) & getattr(stat, "UF_HIDDEN", 0)) or (getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 0)):
                    issues.append(f"{rel.as_posix()} - nascosto al proprietario: togliere il flag (chflags nohidden / attrib -h)")
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not (parent / d).is_symlink() and not inside(parent / d, archives)]
        if parent != root and not files and not dirs and not any(parent.iterdir()):
            issues.append(f"{parent.relative_to(root).as_posix()}/ - cartella vuota")
        for name in files:
            path = parent / name
            if path.is_symlink():
                continue
            rel = path.relative_to(root)
            if re.search(r"(^|[_ .-])(v[0-9]+|finale?|copy|copia|\([0-9]+\))(\.[^.]+)?$", name.lower()):
                issues.append(f"{rel.as_posix()} - possibile copia o versione parallela")
            if path.suffix.lower() != ".md":
                continue
            try:
                data = path.read_bytes()
            except OSError:
                issues.append(f"{rel.as_posix()} - file non leggibile dal guardiano")
                continue
            lines, size = data.count(b"\n"), len(data)
            if name in ROUTERS:
                if lines > 350 or size > 24576:
                    issues.append(f"{rel.as_posix()} - mappa oltre il limite di 350 righe o 24 KiB")
            elif name != "CLAUDE.md" and not re.search(r"_(archivio|storico)_", name) and not {"_archivio", "_storico", "archivio"}.intersection(rel.parts):
                if lines > 800 or size > 81920:
                    issues.append(f"{rel.as_posix()} - documento oltre 800 righe o 80 KiB: archiviare nella stessa stanza")
            if name == "AGENT_CHAT.md":
                stale = 0
                for date in re.findall(r"(?m)^## +(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})", data.decode("utf-8", errors="replace")):
                    stamp = "".join(reversed(date.split("/"))) if "/" in date else date.replace("-", "")
                    stale += stamp < cutoff
                if stale:
                    issues.append(f"{rel.as_posix()} - {stale} note piu' vecchie di 48 ore: promuovi nel file proprietario o in archivio")
    return issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", type=Path, required=True)
    parser.add_argument("--archive-list", type=Path)
    args = parser.parse_args()
    archives, errors = collect(args.scan)
    if args.archive_list:
        args.archive_list.write_text("".join(a.path.relative_to(args.scan).as_posix() + "\n" for a in archives), encoding="utf-8")
    for issue in scan(args.scan, archives, errors):
        print(issue)
