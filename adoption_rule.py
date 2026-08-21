"""Regola deterministica dell'adozione osservata (Passo 1-quinquies).

Il checkup misura *come si lavora davvero* dentro il Cervello. Il controllo
testuale prova soltanto che le etichette siano scritte nel documento: passa
anche se l'agente conta tre volte lo stesso gesto o scrive un giudizio d'uso su
tracce povere. Questa regola chiude quel buco con una funzione deterministica e
testabile, la stessa che il rapporto deve rispettare a mano.

Confine di prodotto: qui si misura l'uso (quali gesti entrano nelle giornate).
La misura della spesa e del consumo appartiene al prodotto `Il Consigliere`.

Fonte macchina obbligatoria: verdetti e tracce ammesse vivono SOLO in
``install_contract.json -> inspection_policies -> adoption_observation``. Se il
contratto manca, non e' JSON valido o la policy e' incompleta, la regola fallisce
in modo visibile (``ContractError``): nessun default locale silenzioso.
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
# I valori canonici vivono nel contratto macchina; qui restano solo i nomi con
# cui il codice li riferisce.
VERDICT_TRACES_ABSENT = "TRACCE ASSENTI"
VERDICT_PARTIAL_ONE_STATION = "OSSERVAZIONE PARZIALE - UNA POSTAZIONE"
VERDICT_OBSERVED = "ADOZIONE OSSERVATA"

# I tre verdetti che la policy deve sempre dichiarare per essere completa.
REQUIRED_VERDICTS = frozenset(
    {VERDICT_TRACES_ABSENT, VERDICT_PARTIAL_ONE_STATION, VERDICT_OBSERVED}
)


class ContractError(RuntimeError):
    """Il contratto macchina manca, e' malformato o la policy e' incompleta.

    Errore visibile: la regola non deve mai proseguire con default locali."""


def normalize_gesture(raw: str) -> str:
    """Normalizza un testo: minuscole, spazi collassati, bordi puliti.

    Lo stesso gesto scritto in Git, in chat e nel diario collassa cosi' su una
    sola forma, altrimenti il conteggio si gonfia (difetto gia' visto sul campo
    a luglio sul conteggio consumi di un cliente)."""

    return re.sub(r"\s+", " ", str(raw).strip().lower())


@dataclass(frozen=True)
class Episode:
    """Una traccia di un episodio conservata dalla macchina.

    ``episode`` e' l'identita' deterministica dell'episodio: piu' tracce dello
    stesso episodio (il commit, la nota in chat, la riga di diario) portano lo
    stesso valore e collassano su uno. Due episodi diversi portano identita'
    diverse e restano distinti anche con lo stesso gesto nello stesso giorno.

    Quando ``episode`` non e' dichiarato, l'identita' si ricava in modo
    deterministico dalla coppia (gesto normalizzato, data): stesso gesto in
    giorni diversi resta distinto; per separare due episodi con lo stesso gesto
    nello stesso giorno serve un ``episode`` esplicito."""

    gesture: str
    source: str
    machine: str = ""
    date: str = ""
    episode: str = ""

    def key(self) -> str:
        explicit = normalize_gesture(self.episode)
        if explicit:
            return explicit
        return f"{normalize_gesture(self.gesture)}@{str(self.date).strip()}"


@dataclass(frozen=True)
class AdoptionOutcome:
    verdict: str
    unique_gestures: tuple[str, ...]
    unique_count: int
    duplicates_collapsed: int
    machines_observed: tuple[str, ...]
    traces_read: bool
    note: str


def _load_policy(contract_path: Path = CONTRACT_PATH) -> dict:
    """Legge e valida la policy dal contratto macchina, unica fonte.

    Fallisce in modo visibile se il file manca, non e' JSON valido, non contiene
    la policy o la policy e' incompleta. Nessun default locale."""

    if not contract_path.exists():
        raise ContractError(f"contratto macchina mancante: {contract_path}")

    try:
        data = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(
            f"contratto macchina illeggibile o JSON non valido ({contract_path}): {exc}"
        ) from exc

    try:
        policy = data["inspection_policies"]["adoption_observation"]
    except (KeyError, TypeError) as exc:
        raise ContractError(
            "policy adoption_observation assente dal contratto macchina"
        ) from exc

    if not isinstance(policy, dict):
        raise ContractError("policy adoption_observation malformata: non e' un oggetto")

    verdicts = policy.get("verdicts")
    if not isinstance(verdicts, list) or REQUIRED_VERDICTS - set(verdicts):
        mancanti = sorted(REQUIRED_VERDICTS - set(verdicts or []))
        raise ContractError(
            f"policy adoption_observation incompleta: verdetti mancanti {mancanti}"
        )

    sources = policy.get("dedup_sources")
    if not isinstance(sources, list) or not sources:
        raise ContractError(
            "policy adoption_observation incompleta: dedup_sources assente o vuota"
        )

    # Set canonico delle tracce (Passo 1-quinquies): NON e' una seconda lista
    # Python, e' dichiarato dal contratto stesso nel glossario. Cosi' la fonte
    # macchina resta unica e la corrispondenza si valida in modo esplicito.
    glossario = policy.get("dedup_sources_glossario")
    if not isinstance(glossario, dict) or not glossario:
        raise ContractError(
            "policy adoption_observation incompleta: dedup_sources_glossario "
            "assente o vuoto (dichiara le tracce canoniche del Passo 1-quinquies)"
        )

    mancanti = set(glossario) - set(sources)
    if mancanti:
        raise ContractError(
            "policy adoption_observation incompleta: dedup_sources non copre le "
            f"tracce canoniche del Passo 1-quinquies, mancano {sorted(mancanti)}"
        )

    return policy


def classify_adoption(
    episodes: Iterable[Any],
    *,
    traces_read: bool,
    house_shared: bool = False,
    machines_in_house: Iterable[str] | None = None,
    contract_path: Path = CONTRACT_PATH,
) -> AdoptionOutcome:
    """Classifica l'adozione osservata in modo deterministico.

    - Le tracce dello stesso episodio (stessa identita') contano uno.
    - Due episodi distinti contano due anche con lo stesso gesto e nello stesso
      giorno.
    - Con tracce insufficienti l'esito e' ``TRACCE ASSENTI``: mai un giudizio di
      mancato uso.
    - Se la casa e' condivisa fra piu' postazioni ma le tracce arrivano da una
      sola macchina, l'esito e' ``OSSERVAZIONE PARZIALE - UNA POSTAZIONE``.

    Verdetti e tracce ammesse arrivano dal contratto macchina; se manca o e'
    incompleto, la funzione solleva ``ContractError`` senza default locali.
    """

    policy = _load_policy(contract_path)
    verdicts = set(policy["verdicts"])
    valid_sources = set(policy["dedup_sources"])

    parsed: list[Episode] = []
    for raw in episodes or []:
        episode = raw if isinstance(raw, Episode) else Episode(**raw)
        if episode.source not in valid_sources:
            raise ValueError(
                f"traccia non ammessa: {episode.source!r} "
                f"(ammesse: {sorted(valid_sources)})"
            )
        parsed.append(episode)

    # Deduplica per identita' di episodio, mantenendo l'ordine di prima apparizione.
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
        note = f"{unique_count} episodi distinti osservati"

    if verdict not in verdicts:  # pragma: no cover - guardia sul contratto
        raise ContractError(f"verdetto fuori contratto macchina: {verdict!r}")

    return AdoptionOutcome(
        verdict=verdict,
        unique_gestures=unique_gestures,
        unique_count=unique_count,
        duplicates_collapsed=duplicates_collapsed,
        machines_observed=machines_observed,
        traces_read=bool(traces_read),
        note=note,
    )
