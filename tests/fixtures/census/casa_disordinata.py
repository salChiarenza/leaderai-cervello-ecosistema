"""Casa finta volutamente disordinata per il collaudo del Censitore.

Requisito del piano (correzione 1 della revisione Claude): la promessa non si
prova soltanto su LeaderAI, che e' gia' strutturata. Questa casa non ha
registri, non ha procedure e non ha mappe: ha Desktop e Download mescolati,
nomi ambigui, file omonimi in cartelle diverse, rumore di sistema, un episodio
duplicato in due posti, una cartella segreta, una cartella personale e due
processi sepolti nelle tracce.

Attesi del collaudo:

- due processi reali emergono (preventivo al cliente, fattura dopo il lavoro);
- l'episodio duplicato non diventa due processi;
- il rumore non diventa un processo;
- la cartella segreta non viene mai aperta ne' nominata;
- la cartella personale viene segnalata come zona, non aperta.

La casa si costruisce a runtime in una cartella temporanea: niente file finti
versionati nella repo e nessuna dipendenza dalla macchina.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

# (percorso relativo, giorno di modifica, contenuto finto)
# Il contenuto non viene mai letto dal collector: serve solo a dare una taglia
# credibile ai file.
CASA: tuple[tuple[str, str, str], ...] = (
    # --- Processo 1: preventivo al cliente, sparso fra Desktop e Download ---
    ("Scrivania/Preventivo Rossi.docx", "2026-07-10", "bozza preventivo"),
    ("Scrivania/preventivo_rossi_v2.docx", "2026-07-11", "seconda versione"),
    ("Scrivania/Preventivo Rossi def.docx", "2026-07-11", "versione definitiva"),
    ("Scaricati/Preventivo Bianchi.pdf", "2026-08-02", "preventivo inviato"),
    ("Scaricati/preventivo bianchi (1).pdf", "2026-08-02", "stesso file riscaricato"),
    ("Scrivania/Preventivo Verdi v3.docx", "2026-08-20", "terzo cliente"),
    # --- Processo 2: fattura dopo il lavoro ---
    ("Scrivania/Fattura 12 Rossi.pdf", "2026-07-20", "fattura emessa"),
    ("Scaricati/fattura-13-bianchi.pdf", "2026-08-15", "fattura emessa"),
    ("Scaricati/Fattura 14 Verdi.pdf", "2026-08-28", "fattura emessa"),
    # --- Omonimia: stesso nome, cartelle diverse, lavori diversi ---
    ("Scrivania/note.txt", "2026-06-01", "appunti sparsi"),
    ("Scaricati/note.txt", "2026-08-30", "altri appunti"),
    # --- Rumore: nessuna ripetizione, nessun processo ---
    ("Scrivania/IMG_4412.jpg", "2026-05-14", "foto"),
    ("Scrivania/schermata 2026-06-02.png", "2026-06-02", "screenshot"),
    ("Scaricati/manuale-stampante.pdf", "2026-04-03", "manuale scaricato"),
    ("Scaricati/setup_app.zip", "2026-04-03", "installer"),
    # --- Rumore di sistema: mai contato ---
    ("Scrivania/.DS_Store", "2026-08-30", "rumore"),
    ("Scaricati/.DS_Store", "2026-08-30", "rumore"),
    # --- Ambiente tecnico: saltato in blocco ---
    ("Scaricati/progetto/node_modules/pacchetto/index.js", "2026-07-01", "libreria"),
    ("Scaricati/progetto/node_modules/pacchetto/LICENSE", "2026-07-01", "licenza"),
    ("Scaricati/progetto/__pycache__/modulo.pyc", "2026-07-01", "cache"),
    # --- Segreti: esclusione assoluta, mai aperti ne' nominati ---
    ("Scrivania/.secrets/gestionale.env", "2026-03-01", "TOKEN=xxx"),
    ("Scrivania/password_banca.txt", "2026-03-01", "segreto"),
    ("Scaricati/api_key_fornitore.json", "2026-03-02", "chiave"),
    # --- Zona personale dentro il perimetro: segnalata, mai aperta ---
    ("Scrivania/Personale/referto_medico.pdf", "2026-02-10", "documento sanitario"),
    ("Scrivania/Personale/cedolino marzo.pdf", "2026-03-10", "busta paga"),
    # --- Fuori perimetro: esiste sul disco ma non si tocca ---
    ("Documenti/relazione.docx", "2026-08-01", "fuori dal perimetro"),
)

# Cartelle autorizzate dal proprietario (le altre restano fuori).
ROOTS = ("Scrivania", "Scaricati")


def _timestamp(day: str) -> float:
    return datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()


def build(base: Path) -> Path:
    """Crea la casa disordinata sotto ``base`` e ne restituisce la radice."""

    home = base / "casa-disordinata"
    for relative, day, content in CASA:
        target = home / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        stamp = _timestamp(day)
        os.utime(target, (stamp, stamp))
    return home


def perimeter_roots(home: Path) -> tuple[str, ...]:
    return tuple((home / name).as_posix() for name in ROOTS)
