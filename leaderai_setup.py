#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STANDARD_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

GITIGNORE_CONTENT = (ROOT / "templates" / "GITIGNORE.txt").read_text(encoding="utf-8")
SUPPORTED_AGENTS = {"codex", "claude", "both"}
CLAUDE_BRIDGE = "@AGENTS.md\n"
STANDARD_DIRS = ("memory", "logs", "ecosistema", ".codex", ".claude", ".git")
STANDARD_FILES = (
    ".gitignore",
    "AGENTS.md",
    "memory/MEMORY.md",
    "AGENT_CHAT.md",
    ".codex/README.md",
    ".claude/README.md",
    "ecosistema/FONTI.md",
    "ecosistema/ASSET.md",
    "ecosistema/PROCESSI.md",
    "ecosistema/LIMITI.md",
    "logs/install-log.md",
    "REPORT_FINALE.md",
)


@dataclass
class InstallResult:
    target: Path
    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    git_outcome: str = "Git: non ancora valutato."

    def record(self, status: str, path: Path) -> None:
        rel = path.relative_to(self.target).as_posix()
        if status == "created":
            self.created.append(rel)
        elif status == "updated":
            self.updated.append(rel)
        else:
            self.existing.append(rel)


def read_template(name: str, context: dict[str, str]) -> str:
    text = (ROOT / "templates" / name).read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace("{{" + key + "}}", value)
    return text


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
    report_paths = [
        target / "REPORT_FINALE.md",
        target / "logs" / "install-log.md",
    ]
    rendered_outcome = result.git_outcome

    def refresh_outcome(after: str) -> None:
        nonlocal rendered_outcome
        before_text = rendered_outcome.removeprefix("Git: ")
        after_text = after.removeprefix("Git: ")
        for path in report_paths:
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
        final_report_paths = [
            path.relative_to(target).as_posix()
            for path in report_paths
            if path.is_file() and not path.is_symlink()
        ]
        if final_report_paths:
            subprocess.run(
                ["git", "add", "--", *final_report_paths],
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


def build_report(result: InstallResult, agent: str) -> str:
    def section(title: str, items: list[str]) -> str:
        if not items:
            return f"{title}\n- Nessuno\n"
        return title + "\n" + "\n".join(f"- {item}" for item in items) + "\n"

    verdict = "NON PASSA" if result.blockers else (
        "PASSA CON ATTENZIONE" if result.warnings else "PASSA"
    )

    def present(rel: str) -> bool:
        return (result.target / rel).exists() or rel in result.created

    actual_configs: list[str] = []
    if present(".codex/README.md"):
        actual_configs.append("`.codex/README.md` (Codex)")
    if present(".claude/README.md"):
        actual_configs.append("`.claude/README.md` (Claude Code)")
    configs_text = ", ".join(actual_configs) if actual_configs else "nessuna"

    return "\n".join(
        [
            "# Report finale LeaderAI",
            "",
            "STANDARD APPLICATO",
            "- Repo: salChiarenza/leaderai-cervello-ecosistema",
            f"- Versione: {STANDARD_VERSION}",
            "- Accesso: percorso tecnico autorizzato",
            "",
            "FASE 1 - CERVELLO",
            "- File comuni sempre presenti: `AGENTS.md`, `CLAUDE.md` (ponte `@AGENTS.md`).",
            f"- Agente richiesto: {agent}",
            f"- Configurazioni realmente presenti: {configs_text}",
            section("- Creato:", result.created).rstrip(),
            section("- Gia' presente:", result.existing).rstrip(),
            section("- Aggiornato:", result.updated).rstrip(),
            section("- Avvisi:", result.warnings).rstrip(),
            section("- Blocchi:", result.blockers).rstrip(),
            "",
            "GIT",
            f"- {result.git_outcome.removeprefix('Git: ')}",
            "",
            "FASE 2 - ECOSISTEMA",
            "- Stato: predisposto, da collegare alle fonti reali del cliente",
            "- Fonti trovate: da compilare dopo discovery reale in `ecosistema/FONTI.md`",
            "- Asset operativi: da registrare in `ecosistema/ASSET.md` quando nasce una risorsa da usare o rispettare",
            "- Fonti da collegare: cartelle/report clienti, cataloghi, Drive/OneDrive, CRM/gestionale solo se esistono",
            "- Dove scrivere i collegamenti: `ecosistema/FONTI.md` per fonti, `ecosistema/ASSET.md` per asset, `ecosistema/PROCESSI.md` per processi, `ecosistema/LIMITI.md` per vincoli",
            "",
            "ARCHITETTURA ADATTIVA",
            "- Classificazione: da eseguire sul caso reale (`STANZA`, `FONTE`, `OUTPUT`, `CAPACITA`, `INFRASTRUTTURA`, `ARCHIVIO`, `SOSPETTA`).",
            "- Mappa stanze: da compilare nel router `AGENTS.md`; nessun nome business viene imposto dal setup.",
            "- Collegamenti monte/valle: da derivare dai processi reali e collaudare dalla radice.",
            "- Prove di instradamento: due richieste realistiche da eseguire dopo la discovery.",
            "- LEZIONE CANDIDATA: nessuna in questa installazione tecnica; compilare se emerge un errore generalizzabile.",
            "",
            "MAPPA COMUNICAZIONE",
            "- Regola: gli agenti non si parlano direttamente; leggono e scrivono file condivisi.",
            "- Stato e chiusura lavoro: `REPORT_FINALE.md` oppure `logs/install-log.md`.",
            "- Procedure e 'come si fa': file dell'area che le usa, non chat.",
            "- Asset/capacita' nuove: `ecosistema/ASSET.md`.",
            "- Coordinamento temporaneo sullo stesso file: chat solo se serve evitare collisioni, massimo 48 ore.",
            "- Allineamento Claude/Codex: sync dedicato solo se il cliente usa entrambi gli agenti.",
            "",
            "MAPPA MODULI",
            "- Regola: ogni modulo va classificato `NON SERVE`, `DA SCOPRIRE`, `DA COLLAUDARE`, `INSTALLABILE` oppure `ATTIVO`.",
            "- PEC/email certificata: DA SCOPRIRE",
            "- Email e calendario (accesso e prova fonte): DA SCOPRIRE",
            "- Calendario operativo (colori/categorie/eventi test): DA SCOPRIRE",
            "- Drive/OneDrive/cartelle operative: DA SCOPRIRE",
            "- CRM/gestionale/export: DA SCOPRIRE",
            "- Plugin/connettori: DA SCOPRIRE",
            "- Skill per lavori ripetuti: DA SCOPRIRE",
            "- Agenti/ruoli dedicati: DA SCOPRIRE",
            "- Guardiani/hook: DA SCOPRIRE",
            "- Ronde/monitoraggi: DA SCOPRIRE",
            "- Voce/dettatura: DA SCOPRIRE",
            "- Compliance/privacy/AI Act: DA SCOPRIRE",
            "",
            "DECISIONI UMANE",
            *(f"- {item}" for item in (result.decisions or ["Nessuna in questa installazione"])),
            "",
            "VERDETTO",
            f"- {verdict}",
        ]
    )


def _event_key(result: InstallResult, agent: str) -> str:
    payload = {
        "version": STANDARD_VERSION,
        "agent": agent,
        "created": result.created,
        "updated": result.updated,
        "warnings": result.warnings,
        "blockers": result.blockers,
        "git": result.git_outcome,
    }
    raw = json.dumps(payload, ensure_ascii=True, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def ensure_report(
    path: Path,
    result: InstallResult,
    agent: str,
    event_key: str,
    dry_run: bool,
) -> None:
    report = build_report(result, agent).rstrip() + "\n"
    marker = f"<!-- LEADERAI-SETUP-EVENT:{event_key} -->"
    if not path.exists():
        if not dry_run:
            path.write_text(marker + "\n" + report, encoding="utf-8")
        result.record("created", path)
        return
    current = path.read_text(encoding="utf-8")
    if marker in current:
        result.record("existing", path)
        return
    update = (
        "\n\n"
        + marker
        + f"\n## Aggiornamento standard LeaderAI {STANDARD_VERSION}\n\n"
        + report
        + "\nQuesto e' l'esito corrente e supera il verdetto precedente, "
        + "che resta preservato sopra come cronologia.\n"
    )
    if not dry_run:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(update)
    result.record("updated", path)


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


def run_setup(target: Path, client: str, agent: str, force: bool = False, dry_run: bool = False) -> InstallResult:
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
    context = {"client_name": client, "date": today, "agent": agent}
    result = InstallResult(target=target)

    bridge_state = _claude_bridge_state(target / "CLAUDE.md", target / "AGENTS.md")
    if bridge_state in {"invalid", "valid-symlink"} and not force:
        ensure_git_repo(
            target,
            result,
            new_install=False,
            dry_run=dry_run,
        )
        ensure_claude_bridge(
            target / "CLAUDE.md",
            target / "AGENTS.md",
            result,
            force=False,
            dry_run=dry_run,
        )
        event_key = _event_key(result, agent)
        ensure_report(
            target / "REPORT_FINALE.md",
            result,
            agent,
            event_key,
            dry_run,
        )
        ensure_event_log(
            target / "logs" / "install-log.md",
            result,
            client,
            agent,
            event_key,
            stamp,
            dry_run,
        )
        return result

    ensure_dir(target, result, dry_run)
    for dirname in ["memory", "logs", "ecosistema"]:
        ensure_dir(target / dirname, result, dry_run)

    ensure_gitignore(target / ".gitignore", result, dry_run)
    git_ready = ensure_git_repo(
        target,
        result,
        new_install=new_install,
        dry_run=dry_run,
    )

    ensure_text(target / "AGENTS.md", read_template("AGENTS.md", context), result, dry_run)
    ensure_text(
        target / "memory" / "MEMORY.md",
        read_template("MEMORY.md", context),
        result,
        dry_run,
    )
    ensure_text(
        target / "AGENT_CHAT.md",
        read_template("AGENT_CHAT.md", context),
        result,
        dry_run,
    )

    if agent in {"codex", "both"}:
        ensure_dir(target / ".codex", result, dry_run)
        ensure_text(
            target / ".codex" / "README.md",
            read_template("CODEX_README.md", context),
            result,
            dry_run,
        )

    ensure_claude_bridge(
        target / "CLAUDE.md",
        target / "AGENTS.md",
        result,
        force,
        dry_run,
    )

    if agent in {"claude", "both"}:
        ensure_dir(target / ".claude", result, dry_run)
        ensure_text(
            target / ".claude" / "README.md",
            read_template("CLAUDE_README.md", context),
            result,
            dry_run,
        )

    ensure_text(
        target / "ecosistema" / "FONTI.md",
        read_template("FONTI.md", context),
        result,
        dry_run,
    )
    ensure_text(
        target / "ecosistema" / "ASSET.md",
        read_template("ASSET.md", context),
        result,
        dry_run,
    )
    ensure_text(
        target / "ecosistema" / "PROCESSI.md",
        read_template("PROCESSI.md", context),
        result,
        dry_run,
    )
    ensure_text(
        target / "ecosistema" / "LIMITI.md",
        read_template("LIMITI.md", context),
        result,
        dry_run,
    )

    changed_before_report = bool(result.created or result.updated)
    event_needed = new_install or changed_before_report or bool(
        result.warnings or result.blockers
    )
    if event_needed:
        event_key = _event_key(result, agent)
        ensure_report(
            target / "REPORT_FINALE.md",
            result,
            agent,
            event_key,
            dry_run,
        )
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
        for rel in ("REPORT_FINALE.md", "logs/install-log.md"):
            path = target / rel
            if path.exists():
                result.record("existing", path)

    ensure_first_commit(
        target,
        result,
        new_install=new_install,
        git_ready=git_ready,
        dry_run=dry_run,
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
    parser.add_argument("--dry-run", action="store_true", help="Mostra cosa farebbe senza scrivere.")
    parser.add_argument("--quiet", action="store_true", help="Riduce output a una riga.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run_setup(Path(args.target), args.client, args.agent, args.force, args.dry_run)
    except ValueError as exc:
        print(f"DA RIPARARE: {exc}")
        return 2

    if args.quiet:
        print(f"{result.target} | created={len(result.created)} existing={len(result.existing)} updated={len(result.updated)}")
        return 2 if result.blockers else 0

    print(f"Target: {result.target}")
    print(f"Creati: {', '.join(result.created) if result.created else 'nessuno'}")
    print(f"Gia' presenti: {', '.join(result.existing) if result.existing else 'nessuno'}")
    print(f"Aggiornati: {', '.join(result.updated) if result.updated else 'nessuno'}")
    if result.decisions:
        print("Decisioni: " + "; ".join(result.decisions))
    return 2 if result.blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
