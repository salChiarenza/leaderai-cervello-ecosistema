"""Regola deterministica dell'adozione osservata (Passo 1-quinquies).

Il checkup misura *come si lavora davvero* dentro il Cervello. Il controllo
testuale prova soltanto che le etichette siano scritte nel documento: passa
anche se l'agente conta tre volte lo stesso gesto o scrive un giudizio d'uso su
tracce povere. Questa regola chiude quel buco con una funzione deterministica e
testabile, la stessa che il rapporto deve rispettare a mano.

Confine di prodotto: qui si misura l'uso (quali gesti entrano nelle giornate).
La misura della spesa e del consumo appartiene al prodotto `Il Consigliere`.

I verdetti sono la fonte unica in
``install_contract.json -> inspection_policies -> adoption_observation``.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "install_contract.json"

# Verdetti dell'adozione osservata. Restano separati dal VERDETTO CONFORMITA'
# del gate tecnico: la casa puo' passare mentre l'uso resta non misurabile.
VERDICT_TRACES_ABSENT = "TRACCE ASSENTI"
VERDICT_PARTIAL_ONE_STATION = "OSSERVAZIONE PARZIALE - UNA POSTAZIONE"
VERDICT_OBSERVED = "ADOZIONE OSSERVATA"

# Le tre tracce che ammettono la deduplicazione dello stesso episodio.
VALID_SOURCES = frozenset({"git", "chat", "diario"})


def normalize_gesture(raw: str) -> str:
    """Chiave di un episodio: minuscole, spazi collassati, bordi puliti.

    Lo stesso gesto scritto in Git, in chat e nel diario deve collassare su una
    sola chiave, altrimenti il conteggio si gonfia (difetto gia' visto sul campo
    a luglio sul conteggio consumi di un cliente)."""

    return re.sub(r"\s+", " ", str(raw).strip().lower())


@dataclass(frozen=True)
class Episode:
    """Un gesto osservato in una traccia della macchina."""

    gesture: str
    source: str
    machine: str = ""
    date: str = ""

    def key(self) -> str:
        return normalize_gesture(self.gesture)


@dataclass(frozen=True)
class AdoptionOutcome:
    verdict: str
    unique_gestures: tuple[str, ...]
    unique_count: int
    duplicates_collapsed: int
    machines_observed: tuple[str, ...]
    traces_read: bool
    note: str


def _load_verdicts() -> set[str]:
    """Legge i verdetti dal contratto macchina; se manca, usa i default locali.

    La lettura del contratto e' la prova che la regola e la sua etichetta vivono
    in una sola fonte."""

    try:
        data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        policy = data["inspection_policies"]["adoption_observation"]
        return set(policy["verdicts"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return {VERDICT_TRACES_ABSENT, VERDICT_PARTIAL_ONE_STATION, VERDICT_OBSERVED}


def classify_adoption(
    episodes: Iterable[Any],
    *,
    traces_read: bool,
    house_shared: bool = False,
    machines_in_house: Iterable[str] | None = None,
) -> AdoptionOutcome:
    """Classifica l'adozione osservata in modo deterministico.

    - Ogni episodio presente in Git, chat e diario sullo stesso gesto conta uno.
    - Con tracce insufficienti l'esito e' ``TRACCE ASSENTI``: mai un giudizio di
      mancato uso.
    - Se la casa e' condivisa fra piu' postazioni ma le tracce arrivano da una
      sola macchina, l'esito e' ``OSSERVAZIONE PARZIALE - UNA POSTAZIONE``.
    """

    parsed: list[Episode] = []
    for raw in episodes or []:
        episode = raw if isinstance(raw, Episode) else Episode(**raw)
        if episode.source not in VALID_SOURCES:
            raise ValueError(
                f"traccia non ammessa: {episode.source!r} "
                f"(ammesse: {sorted(VALID_SOURCES)})"
            )
        parsed.append(episode)

    # Deduplica per episodio, mantenendo l'ordine di prima apparizione.
    seen: dict[str, str] = {}
    for episode in parsed:
        seen.setdefault(episode.key(), episode.gesture.strip())
    unique_gestures = tuple(seen.values())
    unique_count = len(unique_gestures)
    duplicates_collapsed = len(parsed) - unique_count

    machines_observed = tuple(
        dict.fromkeys(e.machine for e in parsed if e.machine)
    )
    house = tuple(dict.fromkeys(machines_in_house or []))

    verdicts = _load_verdicts()

    # Tracce insufficienti: nessun giudizio d'uso, si dichiara solo cosa manca.
    if not traces_read or not parsed:
        verdict = VERDICT_TRACES_ABSENT
        note = "tracce assenti o troppo povere: indicare la traccia che servirebbe"
    # Casa su piu' postazioni ma tracce da una sola: osservazione parziale.
    elif (house_shared or len(house) > 1) and len(machines_observed) <= 1:
        verdict = VERDICT_PARTIAL_ONE_STATION
        stazione = machines_observed[0] if machines_observed else "sconosciuta"
        note = (
            f"casa condivisa fra {max(len(house), 2)} postazioni; tracce dalla "
            f"sola macchina {stazione}"
        )
    else:
        verdict = VERDICT_OBSERVED
        note = f"{unique_count} gesti distinti osservati"

    if verdict not in verdicts:  # pragma: no cover - guardia sul contratto
        raise ValueError(f"verdetto fuori contratto macchina: {verdict!r}")

    return AdoptionOutcome(
        verdict=verdict,
        unique_gestures=unique_gestures,
        unique_count=unique_count,
        duplicates_collapsed=duplicates_collapsed,
        machines_observed=machines_observed,
        traces_read=bool(traces_read),
        note=note,
    )
