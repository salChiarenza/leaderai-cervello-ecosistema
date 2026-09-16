#!/usr/bin/env python3
"""
Copia di sicurezza della casa (Cervello + Ecosistema LeaderAI).

La casa NON e' un registro git: la sua copia di sicurezza e' un archivio zip
datato in una cartella scelta dal proprietario (per esempio dentro iCloud
Drive, Google Drive o OneDrive). La fa la routine giornaliera delle 07:45 e,
la prima volta, l'installazione. Si tengono le ultime copie, le altre si
cancellano da sole.

Restano fuori dalla copia: `.secrets/`, `.git/` residui, file che sembrano
segreti (token, chiavi, password, credenziali, .env, impostazioni locali),
rumore di sistema e gli archivi dichiarati `ARCHIVIO PROTETTO` nelle mappe
delle stanze.

Uso:
  python3 .agent/hooks/backup_casa.py                       # una copia adesso
  python3 .agent/hooks/backup_casa.py --imposta "<cartella>" # sceglie la cartella e fa la prima copia
  python3 .agent/hooks/backup_casa.py --stato               # dove va e quando e' stata fatta l'ultima
Cartella madre: `--casa <percorso>`; altrimenti CLAUDE_PROJECT_DIR o la cartella
che contiene questo file (due livelli sopra).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

CONFIG = Path(".agent") / "backup_casa.json"
LOG = Path("logs") / "backup-log.md"
CONSERVA = 7
SEGRETI = re.compile(
    r"(?:^|/)(?:\.secrets/|\.env$|[^/]*\.env$|[^/]*\.key$|[^/]*\.pem$|"
    r"[^/]*token[^/]*|[^/]*secret[^/]*|[^/]*password[^/]*|[^/]*credential[^/]*|"
    r"settings\.local\.json$)",
    re.IGNORECASE,
)
RUMORE = {".DS_Store", "__pycache__", ".pytest_cache", ".git"}
ARCHIVIO = re.compile(r"^-\s+`([^`]+)`\s+[—-]+\s+ARCHIVIO PROTETTO", re.MULTILINE)


def casa_da(argomento: str | None) -> Path:
    if argomento:
        return Path(argomento).expanduser().resolve()
    per_env = os.environ.get("CLAUDE_PROJECT_DIR")
    if per_env:
        return Path(per_env).resolve()
    return Path(__file__).resolve().parents[2]


def archivi_protetti(casa: Path) -> set[Path]:
    """Gli archivi dichiarati nelle mappe delle stanze: restano fuori dalla copia."""
    trovati: set[Path] = set()
    for mappa in casa.glob("*/AGENTS.md"):
        try:
            testo = mappa.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for rel in ARCHIVIO.findall(testo):
            trovati.add((mappa.parent / rel.strip("/")).resolve())
    return trovati


def leggi_config(casa: Path) -> dict:
    try:
        return json.loads((casa / CONFIG).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def scrivi_config(casa: Path, cartella: Path, conserva: int) -> None:
    (casa / CONFIG).parent.mkdir(parents=True, exist_ok=True)
    (casa / CONFIG).write_text(
        json.dumps({"cartella": str(cartella), "conserva": conserva}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def copia(casa: Path, cartella: Path, conserva: int) -> Path:
    cartella.mkdir(parents=True, exist_ok=True)
    esclusi = archivi_protetti(casa)
    quando = datetime.now()
    nome = f"Cervello-{casa.name}-{quando.strftime('%Y-%m-%d-%H%M')}.zip"
    destinazione = cartella / nome
    conteggio = 0
    with zipfile.ZipFile(destinazione, "w", zipfile.ZIP_DEFLATED) as zf:
        for radice, cartelle, file in os.walk(casa, followlinks=False):
            radice_p = Path(radice)
            cartelle[:] = [
                d for d in cartelle
                if d not in RUMORE
                and not (radice_p / d).is_symlink()
                and (radice_p / d).resolve() not in esclusi
                and (radice_p / d).resolve() != cartella.resolve()
                and not SEGRETI.search((radice_p / d).relative_to(casa).as_posix() + "/")
            ]
            for f in file:
                p = radice_p / f
                rel = p.relative_to(casa).as_posix()
                if f in RUMORE or p.is_symlink() or SEGRETI.search(rel):
                    continue
                zf.write(p, rel)
                conteggio += 1
    vecchie = sorted(cartella.glob(f"Cervello-{casa.name}-*.zip"))
    for vecchia in vecchie[:-conserva] if conserva > 0 else []:
        try:
            vecchia.unlink()
        except OSError:
            pass
    (casa / LOG).parent.mkdir(parents=True, exist_ok=True)
    with (casa / LOG).open("a", encoding="utf-8") as log:
        if log.tell() == 0:
            log.write("# Copie di sicurezza della casa\n\n")
        log.write(f"- {quando.strftime('%d/%m/%Y %H:%M')} — {conteggio} file in `{destinazione}`\n")
    return destinazione


def ultima_copia(cartella: Path, casa: Path) -> Path | None:
    copie = sorted(cartella.glob(f"Cervello-{casa.name}-*.zip")) if cartella.is_dir() else []
    return copie[-1] if copie else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Copia di sicurezza della casa LeaderAI")
    ap.add_argument("--casa", help="cartella madre (default: questa casa)")
    ap.add_argument("--imposta", help="cartella dove tenere le copie; fa subito la prima copia")
    ap.add_argument("--conserva", type=int, default=None, help=f"quante copie tenere (default {CONSERVA})")
    ap.add_argument("--stato", action="store_true", help="mostra cartella e ultima copia, senza copiare")
    args = ap.parse_args(argv)
    casa = casa_da(args.casa)
    if not (casa / "AGENTS.md").is_file():
        print(f"BACKUP NON FATTO: {casa} non sembra una casa LeaderAI (manca AGENTS.md)")
        return 1
    config = leggi_config(casa)
    if args.imposta:
        cartella = Path(args.imposta).expanduser().resolve()
        conserva = args.conserva or int(config.get("conserva", CONSERVA))
        scrivi_config(casa, cartella, conserva)
        config = {"cartella": str(cartella), "conserva": conserva}
    if not config.get("cartella"):
        print("BACKUP: cartella della copia di sicurezza non ancora scelta. "
              "Usa: python3 .agent/hooks/backup_casa.py --imposta \"<cartella>\"")
        return 0
    cartella = Path(config["cartella"]).expanduser()
    conserva = args.conserva or int(config.get("conserva", CONSERVA))
    if args.stato:
        ultima = ultima_copia(cartella, casa)
        print(f"BACKUP: cartella {cartella}; ultima copia: {ultima.name if ultima else 'nessuna'}")
        return 0
    try:
        destinazione = copia(casa, cartella, conserva)
    except OSError as errore:
        print(f"BACKUP NON FATTO: {errore}")
        return 1
    print(f"BACKUP OK: {destinazione}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
