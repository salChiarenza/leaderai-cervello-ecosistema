#!/usr/bin/env python3
"""Monta il Sistema Portafogli in una cartella Cervello + Ecosistema esistente."""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


MODULE_NAME = "Sistema Portafogli Core-Satellite"
SOURCE = Path(__file__).resolve().parent
REPO_ROOT = SOURCE.parents[1]
TEMPLATES = REPO_ROOT / "templates"
ROOM_TABLE_HEADER = (
    "| Stanza | Scopo | A monte | A valle | Fonti | Output | Capacita' | "
    "Mappa locale | Amministratore | Riporta al |"
)
ROOM_TABLE_SEPARATOR = "|---|---|---|---|---|---|---|---|---|---|"
CLAUDE_BRIDGE = "@AGENTS.md\n"


@dataclass
class InstallResult:
    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)


MANAGED_FILES = {
    "VERIFICA_FINANZIARIA.md": "VERIFICA_FINANZIARIA.md",
    "PROCESSO.md": "PROCESSO.md",
    "SCHEMA_DATI.md": "SCHEMA_DATI.md",
    "portfolio_engine.py": "portfolio_engine.py",
    "SCHEDA_CLIENTE_MODELLO.md": "SCHEDA_CLIENTE_MODELLO.md",
    "REPORT_INTERNO_MODELLO.md": "REPORT_INTERNO_MODELLO.md",
    "REPORT_CLIENTE_MODELLO.md": "REPORT_CLIENTE_MODELLO.md",
    "DATI_PORTAFOGLIO_MODELLO.csv": "DATI_PORTAFOGLIO_MODELLO.csv",
    "RENDIMENTI_MENSILI_MODELLO.csv": "RENDIMENTI_MENSILI_MODELLO.csv",
    "VERSION": "VERSION",
}

CUSTOM_FILES = {
    "METODO.md": "METODO.template.md",
    "FONTI.md": "FONTI.template.md",
    "CORE.md": "CORE.template.md",
}


def _assert_regular_or_missing(path: Path, label: str) -> None:
    if path.is_symlink():
        raise ValueError(f"{label} collegato tramite symlink: {path}")
    if path.exists() and not path.is_file():
        raise ValueError(f"{label} occupato da una directory: {path}")


def _assert_safe_backup(path: Path) -> None:
    _assert_regular_or_missing(path, "Backup LeaderAI")


def _assert_safe_backup_family(source: Path) -> None:
    parent = source.parent
    if not parent.exists() or not parent.is_dir():
        return
    base_name = source.name + ".leaderai-backup"
    for candidate in parent.iterdir():
        if candidate.name == base_name or candidate.name.startswith(base_name + "."):
            _assert_safe_backup(candidate)


def _backup_before_overwrite(source: Path, result: InstallResult) -> None:
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
        shutil.copy2(source, candidate)
        result.created.append(str(candidate))
        return


def _copy_if_missing(source: Path, destination: Path, result: InstallResult) -> None:
    _assert_regular_or_missing(destination, "File destinazione")
    if destination.exists():
        result.existing.append(str(destination))
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    result.created.append(str(destination))


def _update_managed(source: Path, destination: Path, result: InstallResult) -> None:
    _assert_regular_or_missing(destination, "File gestito")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_bytes() == source.read_bytes():
        result.existing.append(str(destination))
        return
    if destination.exists():
        _backup_before_overwrite(destination, result)
        shutil.copy2(source, destination)
        result.updated.append(str(destination))
    else:
        shutil.copy2(source, destination)
        result.created.append(str(destination))


def _append_once(path: Path, marker: str, block: str, result: InstallResult) -> None:
    _assert_regular_or_missing(path, "Registro")
    if not path.exists():
        raise ValueError(f"Registro da aggiornare assente: {path}; esegui CHECKUP.md")
    content = path.read_text(encoding="utf-8")
    if marker in content:
        result.existing.append(str(path))
        return
    separator = "" if content.endswith("\n") else "\n"
    path.write_text(content + separator + "\n" + block.rstrip() + "\n", encoding="utf-8")
    result.updated.append(str(path))


def _register_room(path: Path, room_rel: str, result: InstallResult) -> None:
    _assert_regular_or_missing(path, "Mappa madre")
    content = path.read_text(encoding="utf-8")
    map_pointer = f"`{room_rel}/AGENTS.md`"
    row = (
        f"| `{room_rel}/` | Sistema Portafogli Core-Satellite | Da compilare | "
        f"Da compilare | `{room_rel}/FONTI.md` | Analisi, dossier e report | "
        f"Sistema Portafogli | {map_pointer} | Amministratore di settore "
        f"{room_rel} | Boss dell'Ecosistema |"
    )
    section = "### Registro delle stanze"
    if section not in content:
        block = f"""{section}

{ROOM_TABLE_HEADER}
{ROOM_TABLE_SEPARATOR}
{row}

Ogni stanza deve essere raggiungibile da questa tabella. I collegamenti a monte
e a valle si compilano soltanto dai processi reali del proprietario.
"""
        _append_once(path, section, block, result)
        return

    lines = content.splitlines()
    try:
        header_index = lines.index(ROOM_TABLE_HEADER)
        if lines[header_index + 1] != ROOM_TABLE_SEPARATOR:
            raise ValueError
    except (ValueError, IndexError) as exc:
        raise ValueError(
            "Il Registro delle stanze esiste ma non segue il formato canonico; "
            "riparalo con CHECKUP.md prima di installare il modulo"
        ) from exc

    table_end = header_index + 2
    while table_end < len(lines) and lines[table_end].startswith("|"):
        table_end += 1
    if any(map_pointer in line for line in lines[header_index + 2 : table_end]):
        result.existing.append(str(path))
        return
    table_rows = [
        line
        for line in lines[header_index + 2 : table_end]
        if not line.startswith("| Da censire |")
    ]
    lines[header_index + 2 : table_end] = table_rows + [row]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    result.updated.append(str(path))


def _resolve_room(target: Path, room_path: str | Path) -> Path:
    relative = Path(room_path)
    if (
        relative.is_absolute()
        or not relative.parts
        or relative == Path(".")
        or ".." in relative.parts
    ):
        raise ValueError("La stanza deve essere un percorso relativo alla cartella madre")
    room = target / relative
    current = target
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(
                f"La stanza o una sua directory padre e' un symlink: {current}"
            )
    return room


def _bridge_state(path: Path, agents_path: Path) -> str:
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


def _ensure_bridge(path: Path, agents_path: Path, result: InstallResult) -> None:
    state = _bridge_state(path, agents_path)
    if state == "valid-file":
        result.existing.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if state in {"invalid", "valid-symlink"}:
        if path.is_symlink():
            path.unlink()
        elif path.is_file():
            _backup_before_overwrite(path, result)
            path.unlink()
        else:
            raise ValueError(f"Ponte CLAUDE non riparabile automaticamente: {path}")
        status = result.updated
    else:
        status = result.created
    path.write_text(CLAUDE_BRIDGE, encoding="utf-8")
    status.append(str(path))


def _assert_safe_target(target: Path) -> None:
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
        raise ValueError(f"La cartella target e' un symlink: {target}")
    for rel in ("ecosistema", "logs", ".claude", ".claude/skills"):
        path = target / rel
        if path.is_symlink():
            raise ValueError(f"Directory operativa collegata tramite symlink: {path}")
        if path.exists() and not path.is_dir():
            raise ValueError(f"Directory operativa occupata da un file: {path}")
    for rel in (
        "AGENTS.md",
        "ecosistema/ASSET.md",
        "ecosistema/PROCESSI.md",
        "logs/install-log.md",
    ):
        path = target / rel
        if path.is_symlink():
            raise ValueError(f"File operativo collegato tramite symlink: {path}")
        if path.exists() and not path.is_file():
            raise ValueError(f"File operativo occupato da una directory: {path}")


def _assert_no_symlink_components(base: Path, destination: Path) -> None:
    relative = destination.relative_to(base)
    current = base
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(
                f"Percorso destinazione collegato tramite symlink: {current}"
            )


def _validate_skill_name(skill_name: str) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name):
        raise ValueError(
            "Il nome skill deve usare minuscole, numeri e trattini (es. portafogli-azimut)"
        )


def _install_skill(
    destination: Path,
    skill_name: str,
    result: InstallResult,
    update_managed: bool,
) -> None:
    _assert_regular_or_missing(destination, "Skill Claude")
    content = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
    content = re.sub(r"(?m)^name: .+$", f"name: {skill_name}", content, count=1)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not update_managed:
        result.existing.append(str(destination))
        return
    if destination.exists() and destination.read_text(encoding="utf-8") == content:
        result.existing.append(str(destination))
        return
    if destination.exists():
        _backup_before_overwrite(destination, result)
        destination.write_text(content, encoding="utf-8")
        result.updated.append(str(destination))
        return
    destination.write_text(content, encoding="utf-8")
    result.created.append(str(destination))


def install(
    target: Path,
    room_path: str | Path,
    *,
    skill_name: str | None = None,
    create_room: bool = False,
    update_managed: bool = False,
) -> InstallResult:
    target = target.expanduser().absolute()
    _assert_safe_target(target)
    if not target.exists() or not target.is_dir():
        raise ValueError(f"Cartella target assente: {target}")
    if not (target / "AGENTS.md").exists():
        raise ValueError(
            "La cartella target non mostra il router del Cervello: AGENTS.md assente; "
            "esegui prima CHECKUP.md"
        )
    if skill_name:
        _validate_skill_name(skill_name)
        claude_readme = target / ".claude" / "README.md"
        if not claude_readme.is_file() or claude_readme.is_symlink():
            raise ValueError(
                "Una skill Claude richiede `.claude/README.md`: il solo ponte "
                "CLAUDE.md non attiva Claude; "
                "ometti --skill-name o completa prima il checkup"
            )

    room = _resolve_room(target, room_path)
    if room.exists() and not room.is_dir():
        raise ValueError(f"La stanza scelta non e' una cartella: {room}")

    room_destinations = [
        room / "AGENTS.md",
        room / "CLAUDE.md",
        *(room / name for name in MANAGED_FILES),
        *(room / name for name in CUSTOM_FILES),
    ]
    for destination in room_destinations:
        _assert_regular_or_missing(destination, "File della stanza")
    _assert_safe_backup_family(target / "CLAUDE.md")
    _assert_safe_backup_family(room / "CLAUDE.md")
    for destination in [room / name for name in MANAGED_FILES]:
        _assert_safe_backup_family(destination)

    skill_destination: Path | None = None
    if skill_name:
        skill_destination = target / ".claude" / "skills" / skill_name / "SKILL.md"
        _assert_no_symlink_components(target, skill_destination)
        _assert_regular_or_missing(skill_destination, "Skill Claude")
        _assert_safe_backup_family(skill_destination)

    result = InstallResult()
    _ensure_bridge(target / "CLAUDE.md", target / "AGENTS.md", result)
    if not room.exists():
        if not create_room:
            raise ValueError(
                "La stanza scelta non esiste. Prima censisci l'ambiente; "
                "creala solo dopo approvazione e rilancia con --create-room"
            )
        room.mkdir(parents=True)
        result.created.append(str(room))

    room_rel = room.relative_to(target).as_posix()

    _copy_if_missing(TEMPLATES / "ASSET.md", target / "ecosistema" / "ASSET.md", result)
    _copy_if_missing(
        TEMPLATES / "PROCESSI.md", target / "ecosistema" / "PROCESSI.md", result
    )
    _register_room(target / "AGENTS.md", room_rel, result)

    room_map = room / "AGENTS.md"
    if room_map.exists():
        module_map = f"""## Sistema Portafogli Core-Satellite

Questa stanza possiede la capacita' Portafogli LeaderAI.

- Processo: `{room_rel}/PROCESSO.md`
- Verifica finanziaria: `{room_rel}/VERIFICA_FINANZIARIA.md`
- Fonti: `{room_rel}/FONTI.md`
- Metodo professionale: `{room_rel}/METODO.md`
- Motore numerico: `{room_rel}/portfolio_engine.py`
- Collegamenti a monte e a valle: mantenere nella mappa della stanza e nel
  registro processi della cartella madre.
"""
        _append_once(room_map, "## Sistema Portafogli Core-Satellite", module_map, result)
    else:
        _copy_if_missing(SOURCE / "CLIENTE_AGENTS.md", room_map, result)

    for destination_name, source_name in MANAGED_FILES.items():
        source = SOURCE / source_name
        destination = room / destination_name
        if update_managed:
            _update_managed(source, destination, result)
        else:
            _copy_if_missing(source, destination, result)

    for destination_name, source_name in CUSTOM_FILES.items():
        _copy_if_missing(SOURCE / source_name, room / destination_name, result)

    _ensure_bridge(room / "CLAUDE.md", room / "AGENTS.md", result)

    skill_reference = "nessuna nuova skill; riusare una capacita' equivalente se esiste"
    if skill_name and skill_destination is not None:
        _install_skill(skill_destination, skill_name, result, update_managed)
        skill_reference = f"`.claude/skills/{skill_name}/SKILL.md`"

    asset_block = f"""## Sistema Portafogli Core-Satellite

- Tipo: `CAPACITA`
- Stanza proprietaria: `{room_rel}/`
- Uso: costruzione, analisi, backtest, monitoraggio e report.
- Orchestrazione: {skill_reference}.
- Stato: `INSTALLATO - DA VALIDARE SU CASO REALE`.
- Prova: modulo LeaderAI versionato; collaudo fittizio e caso reale da registrare.
"""
    _append_once(
        target / "ecosistema" / "ASSET.md",
        "Sistema Portafogli Core-Satellite",
        asset_block,
        result,
    )

    process_block = f"""## Sistema Portafogli Core-Satellite

- Stanza proprietaria: `{room_rel}/`
- Contratto: `{room_rel}/AGENTS.md`
- Processo: `{room_rel}/PROCESSO.md`
- Verifica finanziaria: `{room_rel}/VERIFICA_FINANZIARIA.md`
- Calcoli: `{room_rel}/portfolio_engine.py`
- Orchestrazione: {skill_reference}
- A monte / a valle: compilare dai processi reali del proprietario.
- Stato iniziale: installato, da configurare sulle fonti reali e validare col banker.
"""
    _append_once(
        target / "ecosistema" / "PROCESSI.md",
        "## Sistema Portafogli Core-Satellite",
        process_block,
        result,
    )

    timestamp = datetime.now().astimezone().strftime("%d/%m/%Y %H:%M %z")
    version = (SOURCE / "VERSION").read_text(encoding="utf-8").strip()
    log_block = (
        f"\n## {timestamp} — {MODULE_NAME}\n\n"
        f"- Versione: `{version}`\n"
        f"- Cartella: `{room}`\n"
        f"- Creati: {len(result.created)}\n"
        f"- Aggiornati: {len(result.updated)}\n"
        f"- Preservati: {len(result.existing)}\n"
        "- Prossimo gate: compilare fonti/metodo/Core e collaudare su caso fittizio.\n"
    )
    log_path = target / "logs" / "install-log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(log_block)
    result.updated.append(str(log_path))
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument(
        "--room",
        required=True,
        help="percorso relativo della stanza proprietaria scelto dopo il censimento",
    )
    parser.add_argument(
        "--create-room",
        action="store_true",
        help="crea la stanza indicata; usarlo solo dopo approvazione strutturale",
    )
    parser.add_argument(
        "--skill-name",
        help="installa una nuova skill Claude col nome scelto; omettere per riusare l'esistente",
    )
    parser.add_argument(
        "--update-managed",
        action="store_true",
        help="aggiorna file tecnici/versionati creando un backup una tantum",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = install(
            args.target,
            args.room,
            skill_name=args.skill_name,
            create_room=args.create_room,
            update_managed=args.update_managed,
        )
    except ValueError as exc:
        print(f"DA RIPARARE: {exc}")
        return 2
    print(f"PASSA: {MODULE_NAME}")
    print(f"Creati: {len(result.created)}")
    print(f"Aggiornati: {len(result.updated)}")
    print(f"Preservati: {len(result.existing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
