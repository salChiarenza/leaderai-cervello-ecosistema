"""Politica condivisa Ispettore/guardiano: archivi di lavoro, mai esenzioni ai segreti.

Componente del controllore del prodotto; il contratto lo installa accanto al guardiano.
Non legge il contenuto dei fascicoli: verifica percorsi e protezione Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import stat
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
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


def maintenance_owner(root: Path, relative: str) -> str:
    """Una sottocartella eredita; infrastruttura comune al controllore della casa."""
    parts = Path(relative).parts
    if parts and parts[0] not in {".", ".."} and not parts[0].startswith("."):
        room = root / parts[0]
        if not room.is_symlink() and (room / "AGENTS.md").is_file():
            return parts[0]
    return "ecosystem-check"


def _local_file(base: Path, raw: str, root: Path) -> Path | None:
    if raw.startswith("@/"):
        base, raw = root, raw[2:]
    if not raw or raw.startswith("/") or any(c in raw for c in "\\:\n\r"):
        return None
    parts = raw.split("/")
    if any(p in {"", ".", ".."} for p in parts):
        return None
    current = base
    for part in parts:
        current = current / part
        if current.is_symlink():
            return None
    return current if current.is_file() else None


def _hook_calls(command: object, script: str, root: Path) -> bool:
    """Accetta l'esecuzione, mai un commento, echo o una sola descrizione."""
    if not isinstance(command, str):
        return False
    try:
        words = shlex.split(command)
    except ValueError:
        return False
    if len(words) < 2 or Path(words[0]).name not in {
        "bash", "python", "python3", "py", "powershell", "pwsh"
    }:
        return False
    # Le configurazioni native usano un percorso tra virgolette con la variabile
    # della casa, oppure la radice Git. Nessuna valutazione del comando qui.
    candidate = words[1]
    return candidate in {
        script, "./" + script, str(root / script),
        "$CLAUDE_PROJECT_DIR/" + script, "${CLAUDE_PROJECT_DIR}/" + script,
        "$CODEX_PROJECT_DIR/" + script, "${CODEX_PROJECT_DIR}/" + script,
        "$(git rev-parse --show-toplevel)/" + script,
    }


def maintenance_findings(root: Path) -> list[tuple[str, str, str]]:
    """Contratto alla nascita + collegamento al controllo; non certifica il business.

    Non esegue comandi delle mappe, non legge segreti e non scrive stato.
    I controlli semantici e le prove di processo spettano all'agente e all'Ispettore.
    """
    issues = []
    try:
        root_text = active_markdown((root / "AGENTS.md").read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return [("MAINTENANCE_ROOT_UNREADABLE", "AGENTS.md", "Mappa madre non leggibile.")]
    declared = re.search(r"(?m)^\s*- Guardiano di chiusura: `([^`]+)`", root_text)
    script = declared[1] if declared else ".agent/hooks/guardiano_stanze.sh"
    guardian = _local_file(root, script, root)
    if guardian is None or not guardian.stat().st_size:
        issues.append(("MAINTENANCE_HOOK_MISSING", script, "Guardiano assente, vuoto o collegato: ripristinare il controllo."))
    mode_match = re.search(r"Modalita' installata: `([^`]+)`", root_text)
    mode = mode_match[1] if mode_match else None
    for engine, rel in (("codex", ".codex/hooks.json"), ("claude", ".claude/settings.json")):
        path = root / rel
        if not path.exists():
            if mode in {engine, "both"}:
                issues.append(("MAINTENANCE_HOOK_UNWIRED", rel, "Configurazione del motore installato assente."))
            continue
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
            groups = config.get("hooks", {}).get("Stop", [])
            linked = not config.get("disableAllHooks", False) and any(
                isinstance(group, dict) and group.get("enabled", True) is not False
                and any(isinstance(h, dict) and h.get("type") == "command"
                    and h.get("enabled", True) is not False
                    and _hook_calls(h.get("command"), script, root)
                    for h in group.get("hooks", []) if isinstance(group.get("hooks"), list))
                for group in groups
            )
        except (OSError, UnicodeError, ValueError, TypeError, AttributeError):
            linked = False
        if not linked:
            issues.append(("MAINTENANCE_HOOK_UNWIRED", rel, "Il guardiano dichiarato non e' collegato a Stop o risulta disabilitato."))
    for room in sorted(root.iterdir()):
        if room.name.startswith(".") or room.is_symlink() or not room.is_dir():
            continue
        path = room / "AGENTS.md"
        if not path.is_file() or path.is_symlink():
            continue
        label = path.relative_to(root).as_posix()
        try:
            text = active_markdown(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            issues.append(("ROOM_MAINTENANCE_MISSING", label, "Mappa non leggibile per la manutenzione."))
            continue
        sections = re.findall(r"(?ms)^## Manutenzione\s*\n(.*?)(?=^## |\Z)", text)
        if len(sections) != 1:
            issues.append(("ROOM_MAINTENANCE_MISSING", label, "Completare una sola sezione Manutenzione: responsabile, eventi, controlli ed esiti."))
            continue
        section = sections[0]
        for field in ("Responsabile", "Quando", "Controlli", "Esiti", "Infrastruttura"):
            values = re.findall(r"(?m)^- " + field + r": (.+)$", section)
            if (len(values) != 1 or len(values[0].strip()) < 4 or "{{" in values[0]
                    or re.match(r"(?i)^(nessuno|da assegnare|da definire|todo|non applicabile)\b", values[0].strip())):
                issues.append(("ROOM_MAINTENANCE_INCOMPLETE", label, "Manutenzione: compilare " + field + "."))
        refs = re.findall(r"(?m)^- Esiti: `([^`]+)`", section)
        source = _local_file(room, refs[0], root) if len(refs) == 1 else None
        if source is None:
            issues.append(("ROOM_MAINTENANCE_EVIDENCE", label, "Manutenzione: Esiti deve puntare alla fonte operativa esistente nella casa."))
        elif room.name != "ecosystem-check":
            # Il controllore e' il bootstrap, non un nuovo processo business.
            # La sua esecuzione e' provata dal collaudo installazione, mai da
            # una ricevuta PASSA precompilata nel template.
            issues.extend(_birth_evidence(root, room, source))
    return issues


def _birth_evidence(root: Path, room: Path, source: Path) -> list[tuple[str, str, str]]:
    label = source.relative_to(root).as_posix()
    try:
        text = active_markdown(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return [("ROOM_BIRTH_PROOF_MISSING", label, "Fonte degli esiti non leggibile.")]
    title = "Prova stanza: " + room.name
    proofs = re.findall(r"(?ms)^## " + re.escape(title) + r"\s*\n(.*?)(?=^## |\Z)", text)
    if len(proofs) != 1:
        return [("ROOM_BIRTH_PROOF_MISSING", label, "Prima di chiudere registra '" + title + "': evento, processo, ingresso, uscita, destinatario e riscontro verificato.")]
    fields = {}
    for name in ("Evento", "Processo", "Ingresso", "Uscita", "Destinatario", "Verifica"):
        values = re.findall(r"(?m)^- " + name + r": (.+)$", proofs[0])
        if len(values) != 1 or len(values[0].strip()) < 4 or re.search(r"(?i){{|da (provare|collaudare|definire)|todo", values[0]):
            return [("ROOM_BIRTH_PROOF_INCOMPLETE", label, "Prova stanza: completare " + name + " con un fatto verificato.")]
        fields[name] = values[0]
    paths = {}
    for name in ("Ingresso", "Uscita", "Destinatario"):
        refs = re.findall(r"`([^`]+)`", fields[name])
        path = _local_file(root, refs[0], root) if len(refs) == 1 else None
        if path is None or ".secrets" in path.parts or path.stat().st_size < 10:
            return [("ROOM_BIRTH_PROOF_FILE", label, "Prova stanza: " + name + " deve citare un file reale non vuoto della casa, con percorso dalla radice.")]
        paths[name] = path
    if paths["Ingresso"] == paths["Uscita"]:
        return [("ROOM_BIRTH_PROOF_CIRCULAR", label, "La prova deve distinguere fonte in ingresso e risultato prodotto.")]
    if len(fields["Processo"]) < 30 or len(fields["Verifica"]) < 30:
        return [("ROOM_BIRTH_PROOF_INCOMPLETE", label, "Descrivere processo e riscontro verificato, non soltanto PASSA.")]
    # Il riscontro semantico non e' inferito dall'esistenza dei file: deve essere
    # riletto dall'Ispettore, mentre il collaudo nativo confronta i dati passati.
    return []


def scan(root: Path, archives=None, errors=None) -> list[str]:
    """Una camminata strutturale, niente processi wc/stat per ogni documento."""
    if archives is None:
        archives, errors = collect(root)
    issues = [f"{path} - {detail}" for _, path, detail in errors]
    issues.extend(f"{path} - {detail}" for _, path, detail in maintenance_findings(root))
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


def record_hook_event(root: Path, payload: object, issues: list[str], script: Path) -> bool:
    """Ultima esecuzione per casa, mai un log che cresce o una prova semantica.

    Solo un evento Stop con sessione e CWD della casa produce la ricevuta.
    Una misura a mano senza evento non puo' fingersi un callback nativo.
    """
    root = root.resolve()
    if not isinstance(payload, dict) or payload.get("hook_event_name") != "Stop":
        return False
    session = payload.get("session_id")
    cwd = payload.get("cwd")
    if not isinstance(session, str) or not session.strip() or not isinstance(cwd, str):
        return False
    if Path(cwd).resolve() != root:
        return False
    folder = root / ".agent"
    if folder.is_symlink() or not folder.is_dir() or script.is_symlink():
        return False
    script = script.resolve()
    record = {
        "evento": "Stop", "sessione": session, "casa": str(root),
        "quando": datetime.now(timezone.utc).isoformat(),
        "guardiano": script.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "motore_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "esito": "PASSA" if not issues else "BLOCCO",
        "rilievi": len(issues),
    }
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=folder, delete=False) as tmp:
        json.dump(record, tmp, ensure_ascii=False)
        tmp.write("\n")
    os.replace(tmp.name, folder / "guardiano-ultimo-evento.json")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--scan", type=Path)
    mode.add_argument("--record-event", type=Path)
    parser.add_argument("--issues", type=Path)
    parser.add_argument("--archive-list", type=Path)
    args = parser.parse_args()
    if args.record_event:
        try:
            payload = json.load(sys.stdin)
            issues = args.issues.read_text(encoding="utf-8").splitlines()
            record_hook_event(args.record_event, payload, issues,
                              args.record_event / ".agent/hooks/guardiano_stanze.sh")
        except (OSError, ValueError, AttributeError):
            raise SystemExit(1)
        raise SystemExit(0)
    archives, errors = collect(args.scan)
    if args.archive_list:
        args.archive_list.write_text("".join(a.path.relative_to(args.scan).as_posix() + "\n" for a in archives), encoding="utf-8")
    for issue in scan(args.scan, archives, errors):
        print(issue)
