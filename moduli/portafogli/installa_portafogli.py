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


@dataclass
class InstallResult:
    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)


MANAGED_FILES = {
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


def _resolve_room(target: Path, room_path: str | Path) -> Path:
    relative = Path(room_path)
    if relative.is_absolute() or not relative.parts or relative == Path("."):
        raise ValueError("La stanza deve essere un percorso relativo alla cartella madre")
    room = (target / relative).resolve()
    if not room.is_relative_to(target):
        raise ValueError("La stanza deve restare dentro la cartella madre")
    return room


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
        backup = destination.with_suffix(destination.suffix + ".leaderai-backup")
        if not backup.exists():
            shutil.copy2(destination, backup)
            result.created.append(str(backup))
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
    target = target.expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise ValueError(f"Cartella target assente: {target}")
    if not (target / "AGENTS.md").exists():
        raise ValueError(
            "La cartella target non mostra il router del Cervello: AGENTS.md assente; "
            "esegui prima CHECKUP.md"
        )
    if skill_name:
        _validate_skill_name(skill_name)
        if not (target / "CLAUDE.md").exists() and not (target / ".claude").exists():
            raise ValueError(
                "Una skill Claude richiede un Cervello Claude gia' attivo; "
                "ometti --skill-name o completa prima il checkup"
            )

    result = InstallResult()
    room = _resolve_room(target, room_path)
    if room.exists() and not room.is_dir():
        raise ValueError(f"La stanza scelta non e' una cartella: {room}")
    if not room.exists():
        if not create_room:
            raise ValueError(
                "La stanza scelta non esiste. Prima censisci l'ambiente; "
                "creala solo dopo approvazione e rilancia con --create-room"
            )
        room.mkdir(parents=True)
        result.created.append(str(room))

    room_rel = room.relative_to(target).as_posix()

    root_map_block = f"""## Stanza collegata: {room_rel}

- Funzione: Sistema Portafogli Core-Satellite.
- Mappa locale: `{room_rel}/AGENTS.md`.
- Fonti e output: dichiarati nella stanza e nei registri `ecosistema/`.
- A monte / a valle: compilare dai processi reali del proprietario.
"""
    _append_once(
        target / "AGENTS.md",
        f"## Stanza collegata: {room_rel}",
        root_map_block,
        result,
    )

    room_map = room / "AGENTS.md"
    if room_map.exists():
        module_map = f"""## Sistema Portafogli Core-Satellite

Questa stanza possiede la capacita' Portafogli LeaderAI.

- Processo: `{room_rel}/PROCESSO.md`
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

    if (target / "CLAUDE.md").exists() or (target / ".claude").exists():
        claude_map = room / "CLAUDE.md"
        if not claude_map.exists():
            claude_map.write_text("# CLAUDE.md\n\n@AGENTS.md\n", encoding="utf-8")
            result.created.append(str(claude_map))
        else:
            result.existing.append(str(claude_map))

    skill_reference = "nessuna nuova skill; riusare una capacita' equivalente se esiste"
    if skill_name:
        skill_destination = target / ".claude" / "skills" / skill_name / "SKILL.md"
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
