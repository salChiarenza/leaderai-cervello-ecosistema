#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent

# Contenuto del .gitignore della cartella madre.
# Tiene FUORI dalla repo i segreti del cliente: la cartella e' un repository git
# e il backup scelto col cliente (GitHub privato o copia su Drive/OneDrive) non
# deve mai contenere token, chiavi o password. Vale sempre, qualunque sia la
# posizione scelta per la cartella madre.
GITIGNORE_CONTENT = """\
# Segreti del cliente: mai nella repo, mai nel backup.
# Su ogni PC i connettori (Gmail, Calendar, Drive, Meta) si ri-autorizzano con login:
# le chiavi restano per-macchina, non viaggiano nel backup.
.secrets/
*.env
.env
*.key
*.pem
*token*
*secret*
*password*
*credential*

# Rumore di sistema
.DS_Store
__pycache__/
.pytest_cache/
"""


@dataclass
class InstallResult:
    target: Path
    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)

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
    if path.exists():
        if path != result.target:
            result.record("existing", path)
        return
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)
    if path != result.target:
        result.record("created", path)


def ensure_text(path: Path, content: str, result: InstallResult, force: bool, dry_run: bool) -> None:
    if path.exists() and not force:
        result.record("existing", path)
        return
    status = "updated" if path.exists() else "created"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
    result.record(status, path)


def append_log(path: Path, lines: Iterable[str], dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line.rstrip() + "\n")


def ensure_gitignore(path: Path, result: InstallResult, dry_run: bool) -> None:
    # Garantisce un .gitignore che esclude i segreti del cliente.
    # Se esiste gia' ma non copre .secrets/, aggiunge le righe mancanti senza
    # toccare il resto: cosi' non sovrascriviamo eventuali regole gia' messe dal cliente.
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if ".secrets/" in current:
            result.record("existing", path)
            return
        if not dry_run:
            with path.open("a", encoding="utf-8") as handle:
                handle.write("\n" + GITIGNORE_CONTENT)
        result.record("updated", path)
        return
    if not dry_run:
        path.write_text(GITIGNORE_CONTENT, encoding="utf-8")
    result.record("created", path)


def ensure_git_repo(target: Path, result: InstallResult, dry_run: bool) -> None:
    # Inizializza la cartella madre come repository git, se non lo e' gia'.
    # E' innocuo e utile in ogni caso: la posizione della cartella (locale o
    # cloud) e il backup (GitHub privato o copia su Drive/OneDrive) si scelgono
    # col cliente, caso per caso. Il repo git serve comunque.
    if (target / ".git").exists():
        result.decisions.append("Git: repository gia' presente nella cartella madre.")
        return
    if dry_run:
        result.decisions.append("Git: 'git init' da eseguire (dry-run).")
        return
    try:
        subprocess.run(
            ["git", "init"],
            cwd=str(target),
            check=True,
            capture_output=True,
        )
        result.decisions.append("Git: repository inizializzato nella cartella madre.")
    except FileNotFoundError:
        result.decisions.append("Git: comando 'git' non trovato, repository da inizializzare a mano.")
    except subprocess.CalledProcessError:
        result.decisions.append("Git: 'git init' fallito, da completare a mano nella cartella madre.")


def build_report(result: InstallResult, agent: str) -> str:
    def section(title: str, items: list[str]) -> str:
        if not items:
            return f"{title}\n- Nessuno\n"
        return title + "\n" + "\n".join(f"- {item}" for item in items) + "\n"

    verdict = "PASSA"
    if result.decisions:
        verdict = "PASSA CON ATTENZIONE"

    if agent == "claude":
        active_agent = "Claude Code"
        active_files = "`CLAUDE.md`, `.claude/README.md`, `AGENTS.md`"
        excluded_agent = "Codex non configurato, salvo richiesta esplicita LeaderAI."
    elif agent == "codex":
        active_agent = "Codex"
        active_files = "`AGENTS.md`, `.codex/README.md`"
        excluded_agent = "Claude Code non configurato, salvo richiesta esplicita LeaderAI."
    else:
        active_agent = "Claude Code + Codex"
        active_files = "`CLAUDE.md`, `.claude/README.md`, `AGENTS.md`, `.codex/README.md`"
        excluded_agent = "Entrambi configurati per richiesta esplicita LeaderAI."

    return "\n".join(
        [
            "# Report finale LeaderAI",
            "",
            "FASE 1 - CERVELLO",
            f"- Agente attivo: {active_agent}",
            f"- Agganci attesi: {active_files}",
            f"- Nota: {excluded_agent}",
            section("- Creato:", result.created).rstrip(),
            section("- Gia' presente:", result.existing).rstrip(),
            section("- Aggiornato:", result.updated).rstrip(),
            "",
            "FASE 2 - ECOSISTEMA",
            "- Stato: predisposto, da collegare alle fonti reali del cliente",
            "- Fonti trovate: da compilare dopo discovery reale in `ecosistema/FONTI.md`",
            "- Asset operativi: da registrare in `ecosistema/ASSET.md` quando nasce una risorsa da usare o rispettare",
            "- Fonti da collegare: cartelle/report clienti, cataloghi, Drive/OneDrive, CRM/gestionale solo se esistono",
            "- Dove scrivere i collegamenti: `ecosistema/FONTI.md` per fonti, `ecosistema/ASSET.md` per asset, `ecosistema/PROCESSI.md` per processi, `ecosistema/LIMITI.md` per vincoli",
            "",
            "MAPPA MODULI",
            "- Regola: ogni modulo va classificato `NON SERVE`, `DA SCOPRIRE`, `DA COLLAUDARE`, `INSTALLABILE` oppure `ATTIVO`.",
            "- PEC/email certificata: DA SCOPRIRE",
            "- Email e calendario: DA SCOPRIRE",
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
            "",
            f"Agente richiesto: {agent}",
        ]
    )


def run_setup(target: Path, client: str, agent: str, force: bool = False, dry_run: bool = False) -> InstallResult:
    target = target.expanduser().resolve()
    today = dt.datetime.now().strftime("%d/%m/%Y")
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context = {"client_name": client, "date": today, "agent": agent}
    result = InstallResult(target=target)

    ensure_dir(target, result, dry_run)
    for dirname in ["memory", "logs", "ecosistema"]:
        ensure_dir(target / dirname, result, dry_run)

    # Cartella madre = repository git con .gitignore che esclude i segreti.
    # La posizione (locale o cloud) e il backup (GitHub o Drive/OneDrive) sono
    # scelti col cliente. Il target arriva da --target, non lo decide lo script.
    ensure_gitignore(target / ".gitignore", result, dry_run)
    ensure_git_repo(target, result, dry_run)

    ensure_text(target / "AGENTS.md", read_template("AGENTS.md", context), result, force, dry_run)
    ensure_text(target / "memory" / "MEMORY.md", read_template("MEMORY.md", context), result, force, dry_run)

    if agent in {"codex", "both"}:
        ensure_dir(target / ".codex", result, dry_run)
        ensure_text(
            target / ".codex" / "README.md",
            "# Codex\n\nCodex deve partire dalla root cliente e leggere `AGENTS.md`.\n",
            result,
            force,
            dry_run,
        )

    if agent in {"claude", "both"}:
        ensure_dir(target / ".claude", result, dry_run)
        ensure_text(
            target / ".claude" / "README.md",
            "# Claude Code\n\nClaude Code deve partire dalla root cliente e leggere `CLAUDE.md` / `AGENTS.md`.\n",
            result,
            force,
            dry_run,
        )
        ensure_text(
            target / "CLAUDE.md",
            "# CLAUDE.md\n\nLeggi `AGENTS.md`: e' la fonte comune del Cervello cliente.\n",
            result,
            force,
            dry_run,
        )

    ensure_text(
        target / "ecosistema" / "FONTI.md",
        "# Fonti\n\nMappa delle fonti vere del cliente.\n\n## Fonti trovate\n\n- Cartella madre: da compilare\n\n## Fonti da collegare\n\n- Cartelle operative: da collegare\n- Report/clienti: da collegare\n- Drive/OneDrive/server: da collegare\n- Email/calendario: da collegare solo se autorizzati\n- CRM/gestionale/fatture: da collegare solo se esiste una fonte reale\n\n## Regola\n\nNon inventare percorsi. Se una fonte non e' presente, lasciare `da collegare`.\n",
        result,
        force,
        dry_run,
    )
    ensure_text(
        target / "ecosistema" / "ASSET.md",
        read_template("ASSET.md", context),
        result,
        force,
        dry_run,
    )
    ensure_text(
        target / "ecosistema" / "PROCESSI.md",
        "# Processi\n\nProcessi osservati o candidati.\n\n## Fase 1 - Cervello\n\n- Verifica lettura istruzioni e memoria\n- Verifica report finale\n\n## Fase 2 - Ecosistema\n\n- Processo: da collegare a una fonte reale\n- Fonte: da collegare\n- Frequenza: da definire\n- Output atteso: da definire\n",
        result,
        force,
        dry_run,
    )
    ensure_text(
        target / "ecosistema" / "LIMITI.md",
        "# Limiti\n\nAzioni che richiedono conferma umana.\n\n## Sempre conferma prima di\n\n- Inviare email\n- Cancellare file\n- Spostare cartelle vive\n- Usare credenziali o dati sensibili\n",
        result,
        force,
        dry_run,
    )

    if agent == "codex":
        result.decisions.append("Claude Code non richiesto: non creato aggancio Claude oltre allo standard comune.")
    elif agent == "claude":
        result.decisions.append("Codex non richiesto: non creato aggancio Codex oltre allo standard comune.")

    ensure_text(target / "logs" / "install-log.md", "# Install log\n", result, False, dry_run)
    ensure_text(target / "REPORT_FINALE.md", build_report(result, agent), result, force, dry_run)

    log_lines = [
        "",
        f"## {stamp}",
        f"- Client: {client}",
        f"- Agent: {agent}",
        f"- Created: {', '.join(result.created) if result.created else 'none'}",
        f"- Existing: {', '.join(result.existing) if result.existing else 'none'}",
        f"- Updated: {', '.join(result.updated) if result.updated else 'none'}",
    ]
    append_log(target / "logs" / "install-log.md", log_lines, dry_run)

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monta Cervello + Ecosistema LeaderAI in una cartella cliente.")
    parser.add_argument("--target", required=True, help="Cartella cliente da creare o controllare.")
    parser.add_argument("--client", default="Cliente", help="Nome cliente.")
    parser.add_argument("--agent", choices=["codex", "claude", "both"], required=True)
    parser.add_argument("--force", action="store_true", help="Sovrascrive i file standard esistenti.")
    parser.add_argument("--dry-run", action="store_true", help="Mostra cosa farebbe senza scrivere.")
    parser.add_argument("--quiet", action="store_true", help="Riduce output a una riga.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_setup(Path(args.target), args.client, args.agent, args.force, args.dry_run)

    if args.quiet:
        print(f"{result.target} | created={len(result.created)} existing={len(result.existing)} updated={len(result.updated)}")
        return 0

    print(f"Target: {result.target}")
    print(f"Creati: {', '.join(result.created) if result.created else 'nessuno'}")
    print(f"Gia' presenti: {', '.join(result.existing) if result.existing else 'nessuno'}")
    print(f"Aggiornati: {', '.join(result.updated) if result.updated else 'nessuno'}")
    if result.decisions:
        print("Decisioni: " + "; ".join(result.decisions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
