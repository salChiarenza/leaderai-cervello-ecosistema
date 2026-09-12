"""Collaudo espansione su agenti reali; avvio esplicito, dati simulati, casa temporanea.

python3 -m tests.room_growth_live --agent codex --evidence-dir /percorcorso/prove
Ripetere per claude prima del rilascio che modifica la nascita dei reparti.
"""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
import shutil
import shlex
import subprocess
import tempfile
from datetime import date, timedelta
from pathlib import Path

import installation_harness as runtime
from templates import ARCHIVE_POLICY as policy
from tests import test_ecosistema_inspector as fixtures


def quotes_reconciled(text):
    expected = {"PRATICA-A": (Decimal(100), Decimal(100), Decimal(0)),
                "PRATICA-B": (Decimal(200), Decimal(0), Decimal(200))}
    found = {}
    for line in text.splitlines():
        cells = [x.strip().strip("*` ") for x in line.strip().strip("|").split("|")]
        if not line.lstrip().startswith("|") or not cells or cells[0] not in expected:
            continue
        try:
            values = tuple(Decimal(x.replace("€", "").replace("euro", "").replace(",", ".").strip()) for x in cells[1:4])
        except InvalidOperation:
            return False
        if values != expected[cells[0]]:
            return False
        found[cells[0]] = values
    return found == expected


def notes_reconciled(room, before_paths, original_date):
    """La soglia verde non basta: il caso duplicato resta nella stessa fonte."""
    paths = {p.relative_to(room).as_posix() for p in room.rglob("*.md")}
    notes = room / "appunti.md"
    text = notes.read_text() if notes.is_file() else ""
    dates = {original_date, date.fromisoformat(original_date).strftime("%d/%m/%Y")}
    return {
        "manutenzione_senza_nuovi_file_md": paths == before_paths,
        "appunti_informazione_conservata": "Appunto operativo datato da conservare." in text
            and any(day in text for day in dates) and "801" in text,
        "appunti_duplicati_accorpati": text.count("Appunto operativo datato da conservare.") == 1
            and len(text.splitlines()) < 100,
    }



def native_session_matches(agent, transcript, receipt):
    """Incrocia il callback con la sessione osservata e i suoi comandi.

    Il JSON del guardiano non e una firma della piattaforma. Nella prova
    isolata il chiamante conserva transcript e ricevuta, rimossa prima del giro.
    Comandi del modello capaci di simulare la ricevuta invalidano questa prova.
    """
    sessions, commands = set(), []
    for line in transcript.splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if item.get("type") == "thread.started":
            sessions.add(item.get("thread_id"))
        if agent == "claude" and item.get("session_id"):
            sessions.add(item["session_id"])
        event = item.get("item", {})
        if event.get("type") and event["type"] not in {"command_execution", "agent_message", "reasoning", "error", "todo_list"}:
            return False
        if event.get("type") == "command_execution":
            commands.append(event.get("command", ""))
        for block in item.get("message", {}).get("content", []):
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            if block.get("name") == "Bash":
                commands.append(block.get("input", {}).get("command", ""))
            elif block.get("name") not in {"Read", "Glob", "Grep"}:
                return False
    for command in commands:
        try:
            words = shlex.split(command)
            if words and Path(words[0]).name in {"bash", "zsh", "sh"} and len(words) == 3 and words[1] in {"-c", "-lc"}:
                command = words[2]
                words = shlex.split(command)
        except ValueError:
            return False
        if not words or words[0] not in {"cat", "pwd", "rg", "head", "tail", "wc", "ls", "stat"}:
            return False
        if any(token in command for token in (">", "<", ";", "&", "|", "\n", "$", "`", "--pre", "--exec")):
            return False
    return bool(receipt.get("sessione")) and receipt.get("sessione") in sessions


def run_growth(agent, evidence_dir, timeout=300):
    evidence_dir = Path(evidence_dir).resolve()
    evidence_dir.mkdir(parents=True, exist_ok=False)
    checks = {}
    with tempfile.TemporaryDirectory(prefix="leaderai-crescita-") as tmp:
        fixture = fixtures.EcosistemaInspectorTest()
        root = fixture.make_target(tmp, agent=agent)
        fixture.create_valid_room(root)
        fixture.add_room_to_registry(root)
        state = root / "app-iscrizioni/STATO_ISCRIZIONI.md"
        state.write_text(state.read_text() + "\n## Quote da incassare\n\n| Pratica | Dovuto | Incassato | Residuo |\n|---|---|---|---|\n| PRATICA-A | 100 | 0 | 100 |\n| PRATICA-B | 200 | 0 | 200 |\n")
        log = root / "logs/install-log.md"
        log.write_text(log.read_text() + "\nPERCORSO GUIDATO CHIUSO: casa anonima di collaudo.\n")
        protected = {}
        for base in (".agents/skills", ".claude/skills"):
            for path in (root / base).rglob("SKILL.md"):
                protected[path.relative_to(root).as_posix()] = path.read_bytes()

        config_path = root / (".codex/hooks.json" if agent == "codex" else ".claude/settings.json")
        expected_guard = (root / ".agent/hooks/guardiano_stanze.sh").read_bytes()
        callback = root / ".agent/guardiano-ultimo-evento.json"

        def turn(name, prompt):
            command = runtime.build_command(agent, agent, root, "jsonl")
            if agent == "codex":
                # Solo questa invocazione nella casa usa-e-getta. Fonti del
                # guardiano controllate prima del bypass, nessuna trust globale.
                if (root / ".agent/hooks/guardiano_stanze.sh").read_bytes() != expected_guard:
                    checks[name + "_runtime"] = False
                    return None
                config = json.loads(config_path.read_text())
                groups = config.get("hooks", {}).get("Stop", [])
                # --ignore-user-config esclude anche il caricamento dei ganci
                # su questa CLI. Carica la configurazione della fixture come
                # override nativo: nessun hook globale della casa di Sal.
                # Non e una prova della fiducia persistente della piattaforma.
                for group in groups:
                    for hook in group.get("hooks", []):
                        if not policy._hook_calls(hook.get("command"), ".agent/hooks/guardiano_stanze.sh", root):
                            raise ValueError("Hook di collaudo non previsto")
                def toml(value):
                    if isinstance(value, dict):
                        return "{" + ",".join(json.dumps(k) + "=" + toml(v) for k, v in value.items()) + "}"
                    if isinstance(value, list):
                        return "[" + ",".join(toml(v) for v in value) + "]"
                    return json.dumps(value)
                command[2:2] = ["--add-dir", str(root / ".codex"), "--dangerously-bypass-hook-trust", "--enable", "hooks", "-c",
                    "hooks.Stop=" + toml(groups)]
            result = runtime.execute_agent(command, root, prompt, timeout)
            (evidence_dir / (name + ".prompt.txt")).write_text(prompt)
            (evidence_dir / (name + ".jsonl")).write_text(result.stdout)
            (evidence_dir / (name + ".stderr.txt")).write_text(result.stderr)
            checks[name + "_runtime"] = result.state == "COMPLETED" and result.return_code == 0
            return result

        turn("nascita", "Crea il reparto amministrazione per gestire gli incassi e comunicarli al reparto Iscrizioni. "
             "Inizia riconciliando questo estratto simulato: movimento BANCA-001, quota PRATICA-A, accredito di 100 euro. "
             "Conserva il risultato nel reparto nuovo e aggiorna lo stato delle quote nel reparto Iscrizioni. "
             "La PRATICA-B non e stata pagata. Usa solo questi dati simulati e i file della casa.")
        room = root / "amministrazione"
        checks["stanza_con_manutenzione"] = room.is_dir() and not policy.maintenance_findings(root)
        guard = subprocess.run(["bash", str(root / ".agent/hooks/guardiano_stanze.sh")],
            input='{"hook_event_name":"Stop"}', cwd=root, text=True, capture_output=True)
        checks["guardiano_nascita"] = guard.returncode == 0
        (evidence_dir / "guardiano-nascita.txt").write_text(guard.stdout + guard.stderr)
        current = state.read_text()
        # Il dato deve passare nella fonte proprietaria esistente, senza cambiare
        # la pratica non pagata. Un racconto nel messaggio finale non basta.
        (evidence_dir / "iscrizioni-dopo-nascita.md").write_text(current)
        checks["passaggio_iscrizioni"] = quotes_reconciled(current)
        texts = "\n".join(p.read_text(errors="replace") for p in room.rglob("*.md")) if room.is_dir() else ""
        checks["riconciliazione_in_reparto"] = "BANCA-001" in texts and "PRATICA-A" in texts
        if room.is_dir():
            turn("sottocartella", "Nel reparto amministrazione organizza gli estratti in una sottocartella banca e conserva li la fonte simulata di questa riconciliazione.")
            checks["sottocartella_eredita"] = (room / "banca").is_dir() and policy.maintenance_owner(root, "amministrazione/banca/estratto.csv") == "amministrazione"
            checks["nessun_agente_aggiunto"] = all((root / p).read_bytes() == data for p, data in protected.items()) and set(protected) == {
                p.relative_to(root).as_posix() for base in (".agents/skills", ".claude/skills") for p in (root / base).rglob("SKILL.md")}
            big = room / "appunti.md"
            history_date = (date.today() - timedelta(days=14)).isoformat()
            big.write_text("# Appunti\n\n## " + history_date + " — Prova storica\n\n" + "Appunto operativo datato da conservare.\n" * 801)
            before_notes_paths = {p.relative_to(room).as_posix() for p in room.rglob("*.md")}
            config = json.loads(config_path.read_text())
            config["hooks"]["Stop"] = []
            config_path.write_text(json.dumps(config, indent=2))
            measured = policy.scan(root)
            (evidence_dir / "difetti-iniettati.txt").write_text("\n".join(measured))
            checks["misura_due_difetti"] = any("appunti.md" in x for x in measured) and any(config_path.name in x for x in measured)
            turn("manutenzione", "Esegui la manutenzione della casa e registra gli esiti nelle fonti previste.")
            checks.update(notes_reconciled(room, before_notes_paths, history_date))
            evidence_text = "\n".join(p.read_text(errors="replace") for p in root.rglob("*.md")
                if p.name not in {"AGENTS.md", "SKILL.md", "CLAUDE.md", "appunti.md"} and ".git" not in p.parts)
            checks["difetto_md_preso_in_carico"] = "appunti.md" in evidence_text
            checks["difetto_gancio_preso_in_carico"] = config_path.name in evidence_text
            checks["gancio_ripristinato"] = not any(x[0].startswith("MAINTENANCE_HOOK") for x in policy.maintenance_findings(root))
            # Verifica di una consegna nativa Stop, distinta da lanciare lo script.
            callback.unlink(missing_ok=True)
            probe = turn("prova_stop", "Concludi questa prova tecnica rispondendo soltanto Prova completata, senza usare strumenti e senza modificare file.")
            native = json.loads(callback.read_text()) if callback.is_file() else {}
            checks["callback_stop_nativa"] = native.get("esito") == "PASSA" and native.get("guardiano") == ".agent/hooks/guardiano_stanze.sh" and native.get("sha256") == hashlib.sha256(expected_guard).hexdigest() and native.get("motore_sha256") == hashlib.sha256((root / ".agent/hooks/archive_policy.py").read_bytes()).hexdigest()
            checks["evento_incrocato_con_sessione"] = bool(probe) and native_session_matches(agent, probe.stdout, native)
            if callback.is_file():
                (evidence_dir / "stop-nativo.json").write_bytes(callback.read_bytes())
            checks["contratto_finale"] = not policy.maintenance_findings(root)
        # Artefatti anonimi e riscontri rileggibili anche dopo la rimozione della casa.
        for folder in ("amministrazione", "app-iscrizioni", "ecosystem-check"):
            if (root / folder).is_dir():
                shutil.copytree(root / folder, evidence_dir / folder)
        (evidence_dir / "mappa-madre.md").write_bytes((root / "AGENTS.md").read_bytes())
        report = {"agent": agent, "checks": checks, "passed": bool(checks) and all(checks.values()),
                  "prova": "sessioni native; riconciliazione simulata, nessun accesso bancario",
                  "state_sha256": hashlib.sha256(current.encode()).hexdigest(),
                  "hook_configuration_mode": "fixture JSON via override nativo isolato" if agent == "codex" else "configurazione progetto nativa",
                  "limite": "La fiducia del cliente nei ganci e un permesso della sua piattaforma; va verificata all installazione."}
        (evidence_dir / "report.json").write_text(json.dumps(report, indent=2))
        return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=["codex", "claude"], required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()
    result = run_growth(args.agent, args.evidence_dir, args.timeout)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
