#!/usr/bin/env python3
"""Monta il Sistema Portafogli in una cartella Cervello + Ecosistema esistente."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


MODULE_NAME = "Sistema Portafogli Core-Satellite"
ROOM_NAME = "Costruzione Portafogli"
SOURCE = Path(__file__).resolve().parent


@dataclass
class InstallResult:
    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)


MANAGED_FILES = {
    "AGENTS.md": "CLIENTE_AGENTS.md",
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


def _copy_if_missing(source: Path, destination: Path, result: InstallResult) -> None:
    if destination.exists():
        result.existing.append(str(destination))
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    result.created.append(str(destination))


def _update_managed(source: Path, destination: Path, result: InstallResult) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_bytes() == source.read_bytes():
        result.existing.append(str(destination))
        return
    if destination.exists():
        backup = destination.with_suffix(destination.suffix + ".leaderai-backup")
        if not backup.exists():
            shutil.copy2(destination, backup)
            result.created.append(str(backup))
        shutil.copy2(source, destination)
        result.updated.append(str(destination))
    else:
        shutil.copy2(source, destination)
        result.created.append(str(destination))


def _append_once(path: Path, marker: str, block: str, result: InstallResult) -> None:
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if marker in content:
        result.existing.append(str(path))
        return
    separator = "" if content.endswith("\n") else "\n"
    path.write_text(content + separator + "\n" + block.rstrip() + "\n", encoding="utf-8")
    result.updated.append(str(path))


def install(target: Path, update_managed: bool = False) -> InstallResult:
    target = target.expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise ValueError(f"Cartella target assente: {target}")
    if not (target / "AGENTS.md").exists() and not (target / "CLAUDE.md").exists():
        raise ValueError(
            "La cartella target non mostra un Cervello installato: AGENTS.md/CLAUDE.md assenti"
        )

    result = InstallResult()
    room = target / ROOM_NAME
    room.mkdir(parents=True, exist_ok=True)

    for destination_name, source_name in MANAGED_FILES.items():
        source = SOURCE / source_name
        destination = room / destination_name
        if update_managed:
            _update_managed(source, destination, result)
        else:
            _copy_if_missing(source, destination, result)

    for destination_name, source_name in CUSTOM_FILES.items():
        _copy_if_missing(SOURCE / source_name, room / destination_name, result)

    claude_map = room / "CLAUDE.md"
    if not claude_map.exists():
        shutil.copy2(room / "AGENTS.md", claude_map)
        result.created.append(str(claude_map))
    else:
        result.existing.append(str(claude_map))

    skill_destination = target / ".claude" / "skills" / "gestisci-portafoglio" / "SKILL.md"
    if update_managed:
        _update_managed(SOURCE / "SKILL.md", skill_destination, result)
    else:
        _copy_if_missing(SOURCE / "SKILL.md", skill_destination, result)

    asset_block = (
        "| Sistema Portafogli Core-Satellite | `Costruzione Portafogli/` | "
        "costruzione, analisi, backtest, monitoraggio e report | "
        "INSTALLATO - DA VALIDARE SU CASO REALE | modulo LeaderAI versionato |"
    )
    _append_once(
        target / "ecosistema" / "ASSET.md",
        "Sistema Portafogli Core-Satellite",
        asset_block,
        result,
    )

    process_block = """## Sistema Portafogli Core-Satellite

- Casa: `Costruzione Portafogli/`
- Contratto: `Costruzione Portafogli/AGENTS.md`
- Processo: `Costruzione Portafogli/PROCESSO.md`
- Calcoli: `Costruzione Portafogli/portfolio_engine.py`
- Orchestrazione Claude: `.claude/skills/gestisci-portafoglio/SKILL.md`
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
        "--update-managed",
        action="store_true",
        help="aggiorna file tecnici/versionati creando un backup una tantum",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = install(args.target, args.update_managed)
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
