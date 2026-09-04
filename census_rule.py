"""Regola deterministica dell'Agente Censitore dei processi (Passo 2).

Il Censitore legge in sola lettura il lavoro presente nel computer e propone
processi candidati con prove e livello di certezza. Questo modulo e' la parte
testabile di quella promessa: decide che cosa e' `OSSERVATO`, `DEDUCIBILE` o
`DA CONFERMARE`, quali percorsi si possono aprire, quando due tracce sono lo
stesso episodio, quando l'inventario va aggregato e se un rapporto e' pulito.

Confine: qui non si legge il disco e non si interpreta il contenuto dei file.
La raccolta dei metadati e la skill che guida l'agente (fase 2 del piano)
consegnano a queste funzioni i dati gia' raccolti e ne rispettano il verdetto.

Fonte macchina obbligatoria: ogni parametro vive SOLO in
``install_contract.json -> inspection_policies -> process_census``. Se il
contratto manca o e' incompleto la regola fallisce in modo visibile
(``ContractError``): nessun default locale silenzioso.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from adoption_rule import normalize_gesture


ROOT = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "install_contract.json"

# Livelli di certezza: i valori canonici vivono nel contratto macchina; qui
# restano solo i nomi con cui il codice li riferisce.
CERTAINTY_OBSERVED = "OSSERVATO"
CERTAINTY_DEDUCIBLE = "DEDUCIBILE"
CERTAINTY_TO_CONFIRM = "DA CONFERMARE"
REQUIRED_LEVELS = frozenset(
    {CERTAINTY_OBSERVED, CERTAINTY_DEDUCIBLE, CERTAINTY_TO_CONFIRM}
)

# Classi di percorso.
PATH_ALLOWED = "AMMESSO"
PATH_OUTSIDE = "FUORI PERIMETRO"
PATH_EXCLUDED = "ESCLUSO"
PATH_SENSITIVE = "ZONA SENSIBILE"
REQUIRED_PATH_CLASSES = frozenset(
    {PATH_ALLOWED, PATH_OUTSIDE, PATH_EXCLUDED, PATH_SENSITIVE}
)

# Modalita' di scansione consegnata al modello.
SCAN_MODE_LIST = "ELENCO"
SCAN_MODE_AGGREGATES = "AGGREGATI"

# Pattern che non devono mai comparire in un rapporto: IBAN italiani, chiavi
# in stile `sk-...` e stringhe lunghe alfanumeriche tipiche dei token.
_IBAN_PATTERN = re.compile(r"\bIT\d{2}[A-Z]\d{10}[0-9A-Z]{12}\b")
_KEY_PREFIX_PATTERN = re.compile(r"\b(?:sk|pk|ghp|xox[abp])[-_][A-Za-z0-9_\-]{12,}")
_TOKEN_LIKE_PATTERN = re.compile(r"(?<![A-Za-z0-9/._-])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9/._-])")


class ContractError(RuntimeError):
    """Il contratto macchina manca, e' malformato o la policy e' incompleta."""


class PerimeterViolation(ValueError):
    """Una prova punta fuori dal perimetro, su un percorso escluso, su una fonte
    non ammessa o su una fonte che richiede consenso non concesso."""


class CertaintyAmbiguity(ValueError):
    """La certezza dichiarata dall'agente non coincide con quella calcolata."""


def _normalized(text: str) -> str:
    """Minuscole, senza accenti, spazi collassati: stessa forma per confronti."""

    decomposed = unicodedata.normalize("NFKD", str(text))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", stripped.casefold().strip())


def _norm_path(raw: str) -> str:
    value = str(raw).strip().replace("\\", "/")
    value = re.sub(r"/+", "/", value)
    return value.rstrip("/") if len(value) > 1 else value


def _path_parts(raw: str) -> tuple[str, ...]:
    return tuple(part for part in _norm_path(raw).split("/") if part)


def _load_policy(contract_path: Path = CONTRACT_PATH) -> dict[str, Any]:
    """Legge e valida la policy dal contratto macchina, unica fonte."""

    if not contract_path.exists():
        raise ContractError(f"contratto macchina mancante: {contract_path}")
    try:
        data = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(
            f"contratto macchina illeggibile o JSON non valido ({contract_path}): {exc}"
        ) from exc
    try:
        policy = data["inspection_policies"]["process_census"]
    except (KeyError, TypeError) as exc:
        raise ContractError("policy process_census assente dal contratto macchina") from exc
    if not isinstance(policy, dict):
        raise ContractError("policy process_census malformata: non e' un oggetto")

    def _list(name: str) -> list[str]:
        value = policy.get(name)
        if not isinstance(value, list) or not value:
            raise ContractError(f"policy process_census incompleta: {name} assente o vuota")
        return value

    levels = set(_list("certainty_levels"))
    if REQUIRED_LEVELS - levels:
        raise ContractError(
            "policy process_census incompleta: livelli di certezza mancanti "
            f"{sorted(REQUIRED_LEVELS - levels)}"
        )
    classes = set(_list("path_classes"))
    if REQUIRED_PATH_CLASSES - classes:
        raise ContractError(
            "policy process_census incompleta: classi di percorso mancanti "
            f"{sorted(REQUIRED_PATH_CLASSES - classes)}"
        )
    sources = _list("allowed_sources")
    glossario = policy.get("allowed_sources_glossario")
    if not isinstance(glossario, dict) or set(glossario) != set(sources):
        raise ContractError(
            "policy process_census incompleta: allowed_sources_glossario non "
            "coincide con allowed_sources"
        )
    if set(_list("consent_required_sources")) - set(sources):
        raise ContractError(
            "policy process_census incoerente: fonte a consenso non ammessa"
        )
    for name in (
        "always_excluded_dirs",
        "always_excluded_terms",
        "sensitive_zone_terms",
        "table_columns",
        "forbidden_actions",
        "output_registries",
        "priority_criteria",
        "owner_decisions",
    ):
        _list(name)
    if len(policy["table_columns"]) != 10:
        raise ContractError("policy process_census incoerente: la tabella ha dieci colonne")
    if policy.get("read_only") is not True:
        raise ContractError("policy process_census incoerente: read_only deve essere true")
    scan = policy.get("scan_policy")
    if not isinstance(scan, dict):
        raise ContractError("policy process_census incompleta: scan_policy assente")
    for name in (
        "aggregate_threshold_items",
        "volume_reference_items",
        "max_sample_files_per_candidate",
        "max_duration_minutes",
    ):
        value = scan.get(name)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ContractError(f"policy process_census incoerente: scan_policy.{name}")
    if scan["aggregate_threshold_items"] >= scan["volume_reference_items"]:
        raise ContractError(
            "policy process_census incoerente: soglia aggregati sopra il volume di riferimento"
        )
    if not isinstance(scan.get("aggregation_axes"), list) or not scan["aggregation_axes"]:
        raise ContractError("policy process_census incompleta: aggregation_axes")
    return policy


# ---------------------------------------------------------------------------
# Perimetro e percorsi
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Perimeter:
    """Perimetro approvato dal proprietario prima della lettura.

    ``roots`` sono le cartelle autorizzate; ``consented_sources`` le fonti a
    consenso (email, calendario, cronologie) che il proprietario ha incluso;
    ``extra_exclusions`` cartelle o file che il proprietario tiene fuori anche
    dentro le radici autorizzate."""

    roots: tuple[str, ...]
    consented_sources: tuple[str, ...] = ()
    extra_exclusions: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Perimeter":
        return cls(
            roots=tuple(str(item) for item in raw.get("roots", [])),
            consented_sources=tuple(
                str(item) for item in raw.get("consented_sources", [])
            ),
            extra_exclusions=tuple(
                str(item) for item in raw.get("extra_exclusions", [])
            ),
        )

    def contains(self, path: str) -> bool:
        target = _normalized(_norm_path(path))
        for root in self.roots:
            base = _normalized(_norm_path(root))
            if not base:
                continue
            if target == base or target.startswith(base.rstrip("/") + "/"):
                return True
        return False

    def excluded_by_owner(self, path: str) -> bool:
        target = _normalized(_norm_path(path))
        for item in self.extra_exclusions:
            base = _normalized(_norm_path(item))
            if base and (target == base or target.startswith(base.rstrip("/") + "/")):
                return True
        return False


def _matches_excluded(path: str, policy: dict[str, Any]) -> bool:
    parts = _path_parts(path)
    excluded_dirs = {_normalized(item) for item in policy["always_excluded_dirs"]}
    if any(_normalized(part) in excluded_dirs for part in parts):
        return True
    haystack = _normalized(_norm_path(path))
    terms = [_normalized(term) for term in policy["always_excluded_terms"]]
    return any(term in haystack for term in terms)


def sensitive_zone(
    path: str,
    *,
    is_dir: bool = False,
    contract_path: Path = CONTRACT_PATH,
) -> str:
    """Restituisce la zona sensibile che contiene ``path`` oppure ``""``.

    La zona e' sempre una cartella: la piu' esterna che porta un tratto
    sensibile. Se il tratto sta soltanto nel nome di un file, la zona e' la
    cartella che lo contiene, cosi' il nome del file non viene mai restituito.
    Con ``is_dir`` la cartella che porta il tratto e' essa stessa la zona."""

    policy = _load_policy(contract_path)
    terms = [_normalized(term) for term in policy["sensitive_zone_terms"]]
    parts = _path_parts(path)
    if not parts:
        return ""
    for index, part in enumerate(parts):
        if any(term in _normalized(part) for term in terms):
            last = index == len(parts) - 1
            if last and not is_dir and index > 0:
                return "/".join(parts[:index])
            return "/".join(parts[: index + 1])
    return ""


def classify_path(
    path: str,
    perimeter: Perimeter,
    *,
    contract_path: Path = CONTRACT_PATH,
) -> str:
    """Classifica un percorso prima di ogni lettura.

    Ordine fisso: le esclusioni assolute vincono sempre, poi il perimetro, poi
    la zona sensibile dentro il perimetro. Solo ``AMMESSO`` puo' essere aperto
    o citato come prova."""

    policy = _load_policy(contract_path)
    if _matches_excluded(path, policy) or perimeter.excluded_by_owner(path):
        return PATH_EXCLUDED
    if not perimeter.contains(path):
        return PATH_OUTSIDE
    if sensitive_zone(path, contract_path=contract_path):
        return PATH_SENSITIVE
    return PATH_ALLOWED


# ---------------------------------------------------------------------------
# Prove, tracce e candidati
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Evidence:
    """Puntatore a una prova: percorso o fonte, mai una copia del contenuto.

    ``direct`` e' vero quando l'agente ha letto la prova nel perimetro;
    ``step`` collega la prova a un passaggio della sequenza (facoltativo)."""

    path: str
    source: str
    date: str = ""
    note: str = ""
    direct: bool = True
    step: str = ""


@dataclass(frozen=True)
class Trace:
    """Una traccia di un episodio (stessa identita' dell'adozione osservata).

    ``episode`` esplicito vince; altrimenti la coppia (soggetto normalizzato,
    data). Tracce dello stesso episodio collassano su uno."""

    subject: str
    date: str = ""
    source: str = ""
    path: str = ""
    episode: str = ""

    def key(self) -> str:
        explicit = normalize_gesture(self.episode)
        if explicit:
            return explicit
        return f"{normalize_gesture(self.subject)}@{str(self.date).strip()}"


@dataclass(frozen=True)
class Candidate:
    """Un processo candidato proposto dal Censitore."""

    name: str
    trigger: str = ""
    sequence: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    output: str = ""
    frequency: str = ""
    friction: str = ""
    evidence: tuple[Evidence, ...] = ()
    traces: tuple[Trace, ...] = ()
    inferred_links: tuple[str, ...] = ()
    declared_certainty: str = ""
    risk: str = "basso"
    owner_decision: str = "in attesa"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Candidate":
        return cls(
            name=str(raw.get("name", "")).strip(),
            trigger=str(raw.get("trigger", "")).strip(),
            sequence=tuple(str(item) for item in raw.get("sequence", [])),
            sources=tuple(str(item) for item in raw.get("sources", [])),
            output=str(raw.get("output", "")).strip(),
            frequency=str(raw.get("frequency", "")).strip(),
            friction=str(raw.get("friction", "")).strip(),
            evidence=tuple(
                item if isinstance(item, Evidence) else Evidence(**item)
                for item in raw.get("evidence", [])
            ),
            traces=tuple(
                item if isinstance(item, Trace) else Trace(**item)
                for item in raw.get("traces", [])
            ),
            inferred_links=tuple(str(item) for item in raw.get("inferred_links", [])),
            declared_certainty=str(raw.get("declared_certainty", "")).strip(),
            risk=str(raw.get("risk", "basso")).strip() or "basso",
            owner_decision=str(raw.get("owner_decision", "in attesa")).strip()
            or "in attesa",
        )

    def episode_keys(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(trace.key() for trace in self.traces))


def validate_evidence(
    evidence: Evidence,
    perimeter: Perimeter,
    *,
    contract_path: Path = CONTRACT_PATH,
) -> None:
    """Una prova e' accettata solo se fonte ammessa, consenso presente e
    percorso ``AMMESSO``. Altrimenti ``PerimeterViolation``: la prova non entra
    nel rapporto e il percorso non viene citato."""

    policy = _load_policy(contract_path)
    if evidence.source not in policy["allowed_sources"]:
        raise PerimeterViolation(
            f"fonte non ammessa: {evidence.source!r} "
            f"(ammesse: {sorted(policy['allowed_sources'])})"
        )
    if (
        evidence.source in policy["consent_required_sources"]
        and evidence.source not in perimeter.consented_sources
    ):
        raise PerimeterViolation(
            f"fonte {evidence.source!r} non inclusa nel perimetro dal proprietario"
        )
    if evidence.source in policy["consent_required_sources"] and not evidence.path:
        return
    path_class = classify_path(evidence.path, perimeter, contract_path=contract_path)
    if path_class != PATH_ALLOWED:
        raise PerimeterViolation(f"prova su percorso {path_class}: non si apre e non si cita")


@dataclass(frozen=True)
class CertaintyOutcome:
    level: str
    direct_count: int
    indirect_count: int
    inferred_links: tuple[str, ...]
    uncovered_steps: tuple[str, ...]
    reason: str


def classify_certainty(
    candidate: Candidate,
    perimeter: Perimeter,
    *,
    contract_path: Path = CONTRACT_PATH,
) -> CertaintyOutcome:
    """Calcola la certezza di un candidato in modo deterministico.

    - nessuna prova diretta → ``DA CONFERMARE``;
    - prove dirette ma almeno un anello dedotto o un passaggio senza prova
      diretta → ``DEDUCIBILE``;
    - ogni passaggio provato e nessun anello dedotto → ``OSSERVATO``.

    Una certezza dichiarata diversa da quella calcolata solleva
    ``CertaintyAmbiguity``: una deduzione non diventa mai fatto perche' appare
    plausibile, e un fatto provato non viene declassato a sensazione."""

    policy = _load_policy(contract_path)
    for evidence in candidate.evidence:
        validate_evidence(evidence, perimeter, contract_path=contract_path)

    direct = [item for item in candidate.evidence if item.direct]
    indirect = [item for item in candidate.evidence if not item.direct]

    uncovered: tuple[str, ...] = ()
    if candidate.sequence and any(item.step for item in direct):
        covered = {_normalized(item.step) for item in direct if item.step}
        uncovered = tuple(
            step for step in candidate.sequence if _normalized(step) not in covered
        )

    if not direct:
        level = CERTAINTY_TO_CONFIRM
        reason = "nessuna prova diretta: tracce insufficienti, indicare la traccia che servirebbe"
    elif candidate.inferred_links or uncovered:
        level = CERTAINTY_DEDUCIBLE
        reason = (
            f"{len(direct)} prove dirette; anelli dedotti {len(candidate.inferred_links)}, "
            f"passaggi senza prova {len(uncovered)}"
        )
    else:
        level = CERTAINTY_OBSERVED
        reason = f"{len(direct)} prove dirette, ogni passaggio provato, nessun anello dedotto"

    if level not in policy["certainty_levels"]:  # pragma: no cover - guardia
        raise ContractError(f"livello fuori contratto macchina: {level!r}")

    declared = candidate.declared_certainty.strip().upper()
    if declared and declared != level:
        raise CertaintyAmbiguity(
            f"{candidate.name!r}: dichiarato {declared}, calcolato {level} ({reason})"
        )

    return CertaintyOutcome(
        level=level,
        direct_count=len(direct),
        indirect_count=len(indirect),
        inferred_links=tuple(candidate.inferred_links),
        uncovered_steps=uncovered,
        reason=reason,
    )


def dedupe_traces(traces: Iterable[Trace]) -> tuple[tuple[str, ...], int]:
    """Tracce dello stesso episodio contano uno. Ritorna (chiavi, collassate)."""

    items = [item if isinstance(item, Trace) else Trace(**item) for item in traces]
    keys = tuple(dict.fromkeys(item.key() for item in items))
    return keys, len(items) - len(keys)


def dedupe_candidates(
    candidates: Iterable[Candidate],
) -> tuple[list[Candidate], list[tuple[str, str]]]:
    """Due candidati con lo stesso nome normalizzato o con lo stesso insieme di
    episodi sono lo stesso processo: resta il primo, il secondo e' registrato
    come fusione ``(tenuto, fuso)``. Due processi con episodi diversi restano
    due anche se condividono un soggetto."""

    kept: list[Candidate] = []
    merged: list[tuple[str, str]] = []
    for candidate in candidates:
        name_key = _normalized(candidate.name)
        keys = frozenset(candidate.episode_keys())
        duplicate = None
        for existing in kept:
            same_name = _normalized(existing.name) == name_key
            same_episodes = bool(keys) and frozenset(existing.episode_keys()) == keys
            if same_name or same_episodes:
                duplicate = existing
                break
        if duplicate is None:
            kept.append(candidate)
        else:
            merged.append((duplicate.name, candidate.name))
    return kept, merged


# ---------------------------------------------------------------------------
# Volume, priorita', rapporto
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ScanPlan:
    mode: str
    item_count: int
    aggregate_threshold_items: int
    volume_reference_items: int
    max_sample_files_per_candidate: int
    aggregation_axes: tuple[str, ...]
    max_duration_minutes: int
    within_duration: bool


def plan_scan(
    item_count: int,
    *,
    elapsed_minutes: float | None = None,
    contract_path: Path = CONTRACT_PATH,
) -> ScanPlan:
    """Decide se il modello riceve l'elenco o soltanto aggregati e campioni."""

    policy = _load_policy(contract_path)
    scan = policy["scan_policy"]
    if not isinstance(item_count, int) or item_count < 0:
        raise ValueError("item_count deve essere un intero non negativo")
    mode = (
        SCAN_MODE_AGGREGATES
        if item_count > scan["aggregate_threshold_items"]
        else SCAN_MODE_LIST
    )
    within = elapsed_minutes is None or elapsed_minutes <= scan["max_duration_minutes"]
    return ScanPlan(
        mode=mode,
        item_count=item_count,
        aggregate_threshold_items=scan["aggregate_threshold_items"],
        volume_reference_items=scan["volume_reference_items"],
        max_sample_files_per_candidate=scan["max_sample_files_per_candidate"],
        aggregation_axes=tuple(scan["aggregation_axes"]),
        max_duration_minutes=scan["max_duration_minutes"],
        within_duration=within,
    )


_RISK_RANK = {"basso": 0, "medio": 1, "alto": 2}


def priority_key(candidate: Candidate) -> tuple[int, int, int, int, str]:
    """Chiave d'ordine: ripetizione, attrito, chiarezza dell'output, rischio.

    Nessuna ora, costo o ritorno economico entra nella chiave: il contratto li
    vieta e la funzione non ha campi per riceverli."""

    repetition = len(candidate.episode_keys())
    friction = 1 if candidate.friction.strip() else 0
    clear_output = 1 if candidate.output.strip() else 0
    risk = _RISK_RANK.get(_normalized(candidate.risk), 1)
    return (-repetition, -friction, -clear_output, risk, _normalized(candidate.name))


def prioritize(candidates: Iterable[Candidate]) -> list[Candidate]:
    return sorted(candidates, key=priority_key)


def report_is_clean(
    text: str, *, contract_path: Path = CONTRACT_PATH
) -> tuple[bool, tuple[str, ...]]:
    """Il rapporto non contiene credenziali, IBAN, chiavi o termini esclusi."""

    policy = _load_policy(contract_path)
    findings: list[str] = []
    haystack = _normalized(text)
    for term in policy["always_excluded_terms"]:
        if _normalized(term) in haystack:
            findings.append(f"termine escluso: {term}")
    for part in policy["always_excluded_dirs"]:
        if re.search(rf"(?<![\w-]){re.escape(_normalized(part))}(?![\w-])", haystack):
            findings.append(f"cartella esclusa: {part}")
    if _IBAN_PATTERN.search(text):
        findings.append("pattern IBAN")
    if _KEY_PREFIX_PATTERN.search(text):
        findings.append("pattern chiave API")
    for match in _TOKEN_LIKE_PATTERN.finditer(text):
        token = match.group(0)
        if any(ch.isdigit() for ch in token) and any(ch.isalpha() for ch in token):
            findings.append("stringa simile a un token")
            break
    return (not findings, tuple(findings))


def _cell(value: str) -> str:
    return re.sub(r"\s+", " ", str(value)).replace("|", "/").strip() or "-"


def render_row(
    candidate: Candidate,
    outcome: CertaintyOutcome,
    *,
    contract_path: Path = CONTRACT_PATH,
) -> str:
    """Riga della tabella unica di `ecosistema/PROCESSI.md`, colonne dal contratto.

    La colonna `prova` porta soltanto puntatori (percorso o fonte e data), mai
    contenuto."""

    policy = _load_policy(contract_path)
    proofs = "; ".join(
        f"{item.path or item.source}" + (f" ({item.date})" if item.date else "")
        for item in candidate.evidence
    )
    values = {
        "processo candidato": candidate.name,
        "innesco": candidate.trigger,
        "sequenza": " -> ".join(candidate.sequence),
        "fonti/strumenti": ", ".join(candidate.sources),
        "output": candidate.output,
        "frequenza osservata": candidate.frequency,
        "attrito": candidate.friction,
        "prova": proofs,
        "certezza": outcome.level,
        "stato": candidate.owner_decision,
    }
    missing = [column for column in policy["table_columns"] if column not in values]
    if missing:  # pragma: no cover - guardia sul contratto
        raise ContractError(f"colonne del contratto senza valore: {missing}")
    return "| " + " | ".join(_cell(values[column]) for column in policy["table_columns"]) + " |"


@dataclass(frozen=True)
class CensusOutcome:
    candidates: tuple[Candidate, ...]
    levels: tuple[str, ...]
    rows: tuple[str, ...]
    merged: tuple[tuple[str, str], ...]
    certain_count: int
    traces_read: bool
    note: str
    sensitive_zones: tuple[str, ...] = field(default_factory=tuple)


def run_census(
    candidates: Iterable[Any],
    perimeter: Perimeter | dict[str, Any],
    *,
    traces_read: bool = True,
    observed_paths: Iterable[str] = (),
    contract_path: Path = CONTRACT_PATH,
) -> CensusOutcome:
    """Esegue la parte deterministica del censimento su candidati gia' raccolti.

    - deduplica i candidati (stesso episodio = un processo);
    - valida ogni prova contro perimetro ed esclusioni;
    - calcola la certezza e ordina per priorita';
    - con tracce non lette nessun processo viene dichiarato certo;
    - i percorsi osservati in zona sensibile vengono riportati come zona, mai
      come file.

    Lo stesso ingresso produce sempre la stessa uscita: e' la base della
    parita' Claude/Codex."""

    perimeter_obj = (
        perimeter if isinstance(perimeter, Perimeter) else Perimeter.from_dict(perimeter)
    )
    parsed = [
        item if isinstance(item, Candidate) else Candidate.from_dict(item)
        for item in candidates or []
    ]
    kept, merged = dedupe_candidates(parsed)

    zones = tuple(
        dict.fromkeys(
            zone
            for zone in (
                sensitive_zone(path, contract_path=contract_path)
                for path in observed_paths
                if classify_path(path, perimeter_obj, contract_path=contract_path)
                == PATH_SENSITIVE
            )
            if zone
        )
    )

    if not traces_read:
        outcomes = [
            CertaintyOutcome(
                level=CERTAINTY_TO_CONFIRM,
                direct_count=0,
                indirect_count=len(candidate.evidence),
                inferred_links=tuple(candidate.inferred_links),
                uncovered_steps=tuple(candidate.sequence),
                reason="tracce non lette: nessun processo dichiarato certo",
            )
            for candidate in kept
        ]
    else:
        outcomes = [
            classify_certainty(candidate, perimeter_obj, contract_path=contract_path)
            for candidate in kept
        ]

    ordered = sorted(zip(kept, outcomes), key=lambda pair: priority_key(pair[0]))
    rows = tuple(
        render_row(candidate, outcome, contract_path=contract_path)
        for candidate, outcome in ordered
    )
    levels = tuple(outcome.level for _, outcome in ordered)
    certain = sum(1 for level in levels if level == CERTAINTY_OBSERVED)
    if not kept:
        note = "nessun candidato: tracce assenti o perimetro vuoto"
    elif not traces_read:
        note = "tracce non lette: tutti i candidati restano DA CONFERMARE"
    else:
        note = f"{len(kept)} candidati, {certain} osservati, {len(merged)} fusioni"

    return CensusOutcome(
        candidates=tuple(candidate for candidate, _ in ordered),
        levels=levels,
        rows=rows,
        merged=tuple(merged),
        certain_count=certain,
        traces_read=bool(traces_read),
        note=note,
        sensitive_zones=zones,
    )
