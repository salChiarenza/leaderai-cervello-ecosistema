from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CONTRACT_PATH = ROOT / "install_contract.json"
VALID_STRATEGIES = {
    "create",
    "merge_gitignore",
    "merge_hooks_json",
    "managed_text",
    "claude_bridge",
    "event_log",
}

CANONICAL_ROOM_CLASSIFICATIONS = (
    "STANZA",
    "FONTE",
    "OUTPUT",
    "CAPACITA",
    "INFRASTRUTTURA",
    "ARCHIVIO",
    "SOSPETTA",
)

CANONICAL_ROOT_OWNED_CLASSIFICATIONS = (
    "FONTE",
    "OUTPUT",
    "CAPACITA",
    "INFRASTRUTTURA",
    "ARCHIVIO",
)

CANONICAL_ROOT_OWNED_REGISTRIES = (
    "ecosistema/ASSET.md",
    "ecosistema/FONTI.md",
)

CANONICAL_STANDARD_ROOM_PATHS = ("ecosystem-check",)

CANONICAL_ROOM_REQUIRED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
)

CANONICAL_ROOM_MAP_TEMPLATE = "ecosistema/STANZA_AGENTS.md"
CANONICAL_ROOM_SOURCE_TEMPLATE = "ecosistema/STANZA_FONTE.md"

CANONICAL_ROOM_SECTIONS = (
    "stato corrente e prossimo passo",
    "scopo",
    "responsabilita business",
    "organigramma",
    "dentro",
    "fonti",
    "output",
    "fonte operativa",
    "fonte business editabile",
    "capacita",
    "a monte",
    "a valle",
    "dove scrivere",
    "regole",
)

CANONICAL_ROOM_TERMS = (
    "amministratore del settore",
    "boss dell'ecosistema",
    "riporta al boss",
)

CANONICAL_OWNER_SOURCE_HEADINGS = (
    "stato corrente",
    "prossimo passo",
    "decisioni",
    "scadenze",
)

WINDOWS_RESERVED_NAMES = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


@dataclass(frozen=True)
class TemplateRule:
    template: str
    destination: str
    strategy: str


@dataclass(frozen=True)
class OfficialSource:
    id: str
    url: str
    role: str
    comparison: str


@dataclass(frozen=True)
class MarkdownHygienePolicy:
    router_names: tuple[str, ...]
    router_max_lines: int
    router_max_bytes: int
    document_review_lines: int
    document_review_bytes: int


@dataclass(frozen=True)
class OrganizationPolicy:
    root_role: str
    sector_role: str
    default_reports_to: str


@dataclass(frozen=True)
class RoomLifecyclePolicy:
    classifications: tuple[str, ...]
    root_owned_classifications: tuple[str, ...]
    root_owned_registry_paths: tuple[str, ...]
    room_required_files: tuple[str, ...]
    bridge_content: str
    map_template: str
    source_template: str
    required_sections: tuple[str, ...]
    required_terms: tuple[str, ...]
    required_terms_section: str
    owner_source_section: str
    business_source_section: str
    owner_source_headings: tuple[str, ...]
    contents_section: str
    scan_depth: int
    standard_room_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProcessCensusPolicy:
    """Contratto dell'Agente Censitore dei processi (Passo 2 - Censimento).

    Il dettaglio vive in ``install_contract.json -> inspection_policies ->
    process_census``; qui restano i campi che il codice e i test riferiscono.
    La regola deterministica e' ``census_rule.py``."""

    agent_name: str
    skill_name: str
    phase_served: int
    next_phase: int
    trigger_commands: tuple[str, ...]
    read_only: bool
    forbidden_actions: tuple[str, ...]
    certainty_levels: tuple[str, ...]
    path_classes: tuple[str, ...]
    allowed_sources: tuple[str, ...]
    consent_required_sources: tuple[str, ...]
    always_excluded_dirs: tuple[str, ...]
    always_excluded_terms: tuple[str, ...]
    sensitive_zone_terms: tuple[str, ...]
    aggregate_threshold_items: int
    volume_reference_items: int
    max_sample_files_per_candidate: int
    max_duration_minutes: int
    aggregation_axes: tuple[str, ...]
    table_columns: tuple[str, ...]
    card_fields: tuple[str, ...]
    owner_decisions: tuple[str, ...]
    priority_criteria: tuple[str, ...]
    output_registries: tuple[str, ...]
    room_status_after_census: str


def _safe_relative(raw: str, label: str) -> str:
    value = raw.strip()
    parts = value.split("/") if value else []
    if (
        not value
        or value != raw
        or "\\" in value
        or value.startswith("/")
        or re.match(r"^[a-zA-Z]:", value)
        or any(part in {"", ".", ".."} for part in parts)
        or any(
            ":" in part
            or part.rstrip(" .") != part
            or part.split(".", 1)[0].casefold() in WINDOWS_RESERVED_NAMES
            for part in parts
        )
    ):
        raise ValueError(f"{label} non e' un percorso relativo sicuro: {raw!r}")
    return "/".join(parts)


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Contratto installazione non leggibile: {path}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Schema install_contract.json non supportato.")
    supported = data.get("supported_agents")
    if supported != ["codex", "claude", "both"]:
        raise ValueError("supported_agents deve dichiarare codex, claude e both.")
    if not isinstance(data.get("common"), dict) or not isinstance(
        data.get("agents"), dict
    ):
        raise ValueError("Contratto privo delle sezioni common/agents.")
    official_sources(data)
    organization_policy(data)
    room_lifecycle_policy(data)
    markdown_hygiene_policy(data)
    process_census_policy(data)
    for agent in supported:
        if not isinstance(data["agents"].get(agent), dict):
            raise ValueError(f"Contratto agente mancante: {agent}.")
        for rel in required_paths(data, agent) + forbidden_paths(data, agent):
            _safe_relative(rel, f"Percorso {agent}")
    destinations: set[str] = set()
    for rule in template_rules(data, "both"):
        _safe_relative(rule.template, "Template")
        destination = _safe_relative(rule.destination, "Destinazione")
        if rule.strategy not in VALID_STRATEGIES:
            raise ValueError(f"Strategia template non supportata: {rule.strategy}.")
        if destination in destinations:
            raise ValueError(f"Destinazione template duplicata: {destination}.")
        destinations.add(destination)
        if not (ROOT / "templates" / rule.template).is_file():
            raise ValueError(f"Template dichiarato ma assente: {rule.template}.")
    environment_checks(data)
    semantic_requirements(data)
    return data


def _agent_parts(contract: dict[str, Any], agent: str) -> list[dict[str, Any]]:
    supported = contract["supported_agents"]
    if agent not in supported:
        raise ValueError(f"Agente non valido nel contratto: {agent!r}.")
    common = contract["common"]
    selected = contract["agents"][agent]
    parts = [common]
    for included in selected.get("includes", []):
        if included not in supported or included == "both":
            raise ValueError(f"Include agente non valido per {agent}: {included!r}.")
        parts.append(contract["agents"][included])
    parts.append(selected)
    return parts


def template_rules(
    contract: dict[str, Any],
    agent: str,
) -> list[TemplateRule]:
    rules: list[TemplateRule] = []
    seen: set[str] = set()
    for part in _agent_parts(contract, agent):
        for raw in part.get("templates", []):
            if not isinstance(raw, dict):
                raise ValueError("Regola template non valida nel contratto.")
            rule = TemplateRule(
                template=str(raw.get("template", "")),
                destination=str(raw.get("destination", "")),
                strategy=str(raw.get("strategy", "")),
            )
            destination_key = rule.destination.replace("\\", "/").casefold()
            if destination_key in seen:
                raise ValueError(
                    f"Destinazione template duplicata: {rule.destination}."
                )
            rules.append(rule)
            seen.add(destination_key)
    return rules


def required_paths(contract: dict[str, Any], agent: str) -> list[str]:
    paths: list[str] = []
    for part in _agent_parts(contract, agent):
        for raw in part.get("required", []):
            rel = str(raw)
            if rel not in paths:
                paths.append(rel)
    return paths


def forbidden_paths(contract: dict[str, Any], agent: str) -> list[str]:
    paths: list[str] = []
    # `both` eredita i file obbligatori dei due agenti, non i loro divieti
    # reciproci. I divieti sono quindi sempre quelli comuni + quelli dichiarati
    # direttamente dalla modalita' richiesta.
    for part in (contract["common"], contract["agents"][agent]):
        for raw in part.get("forbidden", []):
            rel = str(raw)
            if rel not in paths:
                paths.append(rel)
    return paths


def external_effects(contract: dict[str, Any], agent: str) -> set[str]:
    effects: set[str] = set()
    for part in _agent_parts(contract, agent):
        effects.update(str(value) for value in part.get("external_effects", []))
    unknown = effects - set(contract.get("external_effects", {}))
    if unknown:
        raise ValueError(
            "Effetti esterni non descritti: " + ", ".join(sorted(unknown))
        )
    return effects


def environment_checks(contract: dict[str, Any]) -> set[str]:
    checks = {
        str(value)
        for value in contract["common"].get("environment_checks", [])
    }
    unknown = checks - set(contract.get("environment_checks", {}))
    if unknown:
        raise ValueError(
            "Controlli ambiente non descritti: " + ", ".join(sorted(unknown))
        )
    return checks


def semantic_requirements(contract: dict[str, Any]) -> set[str]:
    requirements = {
        str(value)
        for value in contract["common"].get("semantic_requirements", [])
    }
    unknown = requirements - set(contract.get("semantic_requirements", {}))
    if unknown:
        raise ValueError(
            "Requisiti semantici non descritti: "
            + ", ".join(sorted(unknown))
        )
    return requirements


def official_sources(contract: dict[str, Any]) -> list[OfficialSource]:
    raw_sources = contract.get("official_sources")
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValueError("Contratto privo delle fonti ufficiali vive.")

    sources: list[OfficialSource] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for raw in raw_sources:
        if not isinstance(raw, dict):
            raise ValueError("Fonte ufficiale non valida nel contratto.")
        source = OfficialSource(
            id=str(raw.get("id", "")).strip(),
            url=str(raw.get("url", "")).strip(),
            role=str(raw.get("role", "")).strip(),
            comparison=str(raw.get("comparison", "")).strip(),
        )
        if not all((source.id, source.url, source.role, source.comparison)):
            raise ValueError("Fonte ufficiale incompleta nel contratto.")
        if not source.url.startswith("https://"):
            raise ValueError(f"URL ufficiale non HTTPS: {source.url!r}.")
        if source.id in seen_ids or source.url in seen_urls:
            raise ValueError(f"Fonte ufficiale duplicata: {source.id!r}.")
        sources.append(source)
        seen_ids.add(source.id)
        seen_urls.add(source.url)
    return sources


def markdown_hygiene_policy(contract: dict[str, Any]) -> MarkdownHygienePolicy:
    policies = contract.get("inspection_policies")
    if not isinstance(policies, dict):
        raise ValueError("Contratto privo delle policy di ispezione.")
    raw = policies.get("markdown_hygiene")
    if not isinstance(raw, dict):
        raise ValueError("Contratto privo della policy igiene Markdown.")

    names = raw.get("router_names")
    if (
        not isinstance(names, list)
        or not names
        or any(not isinstance(name, str) or not name.endswith(".md") for name in names)
    ):
        raise ValueError("router_names deve contenere nomi Markdown validi.")
    normalized_names = tuple(name.casefold() for name in names)
    if len(set(normalized_names)) != len(normalized_names):
        raise ValueError("router_names contiene duplicati.")

    limit_names = (
        "router_max_lines",
        "router_max_bytes",
        "document_review_lines",
        "document_review_bytes",
    )
    limits = {name: raw.get(name) for name in limit_names}
    if any(not isinstance(value, int) or value <= 0 for value in limits.values()):
        raise ValueError("Le soglie Markdown devono essere interi positivi.")
    if limits["router_max_lines"] >= limits["document_review_lines"]:
        raise ValueError("La soglia righe dei router deve essere piu' stretta.")
    if limits["router_max_bytes"] >= limits["document_review_bytes"]:
        raise ValueError("La soglia byte dei router deve essere piu' stretta.")

    return MarkdownHygienePolicy(
        router_names=normalized_names,
        router_max_lines=limits["router_max_lines"],
        router_max_bytes=limits["router_max_bytes"],
        document_review_lines=limits["document_review_lines"],
        document_review_bytes=limits["document_review_bytes"],
    )


def organization_policy(contract: dict[str, Any]) -> OrganizationPolicy:
    policies = contract.get("inspection_policies")
    if not isinstance(policies, dict):
        raise ValueError("Contratto privo delle policy di ispezione.")
    raw = policies.get("organization_chart")
    if not isinstance(raw, dict):
        raise ValueError("Contratto privo della policy organigramma.")
    policy = OrganizationPolicy(
        root_role=str(raw.get("root_role", "")).strip(),
        sector_role=str(raw.get("sector_role", "")).strip(),
        default_reports_to=str(raw.get("default_reports_to", "")).strip(),
    )
    if not all((policy.root_role, policy.sector_role, policy.default_reports_to)):
        raise ValueError("Policy organigramma incompleta.")
    if policy.default_reports_to != policy.root_role:
        raise ValueError("Ogni settore deve riportare al ruolo radice.")
    return policy


def room_lifecycle_policy(contract: dict[str, Any]) -> RoomLifecyclePolicy:
    policies = contract.get("inspection_policies")
    if not isinstance(policies, dict):
        raise ValueError("Contratto privo delle policy di ispezione.")
    raw = policies.get("room_lifecycle")
    if not isinstance(raw, dict):
        raise ValueError("Contratto privo della policy ciclo di vita stanze.")

    classifications = raw.get("classifications")
    root_owned_classifications = raw.get("root_owned_classifications")
    root_owned_registry_paths = raw.get("root_owned_registry_paths")
    standard_room_paths = raw.get("standard_room_paths")
    required_files = raw.get("room_required_files")
    required_sections = raw.get("required_sections")
    required_terms = raw.get("required_terms")
    source_headings = raw.get("owner_source_headings")
    lists = {
        "classifications": classifications,
        "root_owned_classifications": root_owned_classifications,
        "root_owned_registry_paths": root_owned_registry_paths,
        "standard_room_paths": standard_room_paths,
        "room_required_files": required_files,
        "required_sections": required_sections,
        "required_terms": required_terms,
        "owner_source_headings": source_headings,
    }
    for label, values in lists.items():
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(value, str) or not value.strip() for value in values)
        ):
            raise ValueError(f"Policy stanze: {label} non valido.")
        normalized = [value.casefold().strip() for value in values]
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Policy stanze: {label} contiene duplicati.")

    for rel in required_files:
        _safe_relative(rel, "File obbligatorio stanza")
    if tuple(value.strip() for value in required_files) != CANONICAL_ROOM_REQUIRED_FILES:
        raise ValueError(
            "Policy stanze: i file obbligatori canonici non possono cambiare."
        )
    normalized_classifications = {
        value.casefold().strip() for value in classifications
    }
    if tuple(value.strip() for value in classifications) != CANONICAL_ROOM_CLASSIFICATIONS:
        raise ValueError(
            "Policy stanze: l'insieme e l'ordine delle classi canoniche non "
            "possono cambiare."
        )
    if (
        tuple(value.strip() for value in root_owned_classifications)
        != CANONICAL_ROOT_OWNED_CLASSIFICATIONS
    ):
        raise ValueError(
            "Policy stanze: le classi della cartella madre non possono cambiare."
        )
    normalized_registry_paths = tuple(
        _safe_relative(value, "Registro elementi cartella madre")
        for value in root_owned_registry_paths
    )
    if normalized_registry_paths != CANONICAL_ROOT_OWNED_REGISTRIES:
        raise ValueError(
            "Policy stanze: i registri canonici della cartella madre non possono "
            "cambiare."
        )
    normalized_standard_rooms = tuple(
        _safe_relative(value, "Stanza standard") for value in standard_room_paths
    )
    if normalized_standard_rooms != CANONICAL_STANDARD_ROOM_PATHS:
        raise ValueError(
            "Policy stanze: le stanze standard canoniche non possono cambiare."
        )
    map_template = _safe_relative(str(raw.get("map_template", "")), "Calco mappa stanza")
    source_template = _safe_relative(
        str(raw.get("source_template", "")), "Calco fonte stanza"
    )
    if (
        map_template != CANONICAL_ROOM_MAP_TEMPLATE
        or source_template != CANONICAL_ROOM_SOURCE_TEMPLATE
    ):
        raise ValueError("Policy stanze: i due calchi canonici non possono cambiare.")
    installed_destinations = {
        rule.destination for rule in template_rules(contract, "both")
    }
    if not set(normalized_registry_paths) <= installed_destinations:
        raise ValueError(
            "Policy stanze: i registri della cartella madre devono essere "
            "installati dal contratto."
        )
    for room_path in normalized_standard_rooms:
        for filename in CANONICAL_ROOM_REQUIRED_FILES:
            required = f"{room_path}/{filename}"
            if required not in installed_destinations:
                raise ValueError(
                    f"Stanza standard incompleta nel contratto: {required}."
                )
    for rel in (map_template, source_template):
        if rel not in installed_destinations:
            raise ValueError(f"Calco stanza non installato dal contratto: {rel}.")

    bridge_content = raw.get("bridge_content")
    if bridge_content != "@AGENTS.md\n":
        raise ValueError("Il ponte stanza deve essere esattamente @AGENTS.md.")
    scalar_fields = {
        "required_terms_section": raw.get("required_terms_section"),
        "owner_source_section": raw.get("owner_source_section"),
        "business_source_section": raw.get("business_source_section"),
        "contents_section": raw.get("contents_section"),
    }
    if any(not isinstance(value, str) or not value.strip() for value in scalar_fields.values()):
        raise ValueError("Policy stanze: nomi sezione incompleti.")
    normalized_required_sections = tuple(
        value.casefold().strip() for value in required_sections
    )
    if normalized_required_sections != CANONICAL_ROOM_SECTIONS:
        raise ValueError(
            "Policy stanze: sezioni e ordine canonici non possono cambiare."
        )
    normalized_required_terms = tuple(
        value.casefold().strip() for value in required_terms
    )
    if normalized_required_terms != CANONICAL_ROOM_TERMS:
        raise ValueError("Policy stanze: i termini canonici non possono cambiare.")
    normalized_source_headings = tuple(
        value.casefold().strip() for value in source_headings
    )
    if normalized_source_headings != CANONICAL_OWNER_SOURCE_HEADINGS:
        raise ValueError(
            "Policy stanze: le sezioni della fonte operativa non possono cambiare."
        )
    expected_scalar_fields = {
        "required_terms_section": "organigramma",
        "owner_source_section": "fonte operativa",
        "business_source_section": "fonte business editabile",
        "contents_section": "dentro",
    }
    normalized_scalar_fields = {
        name: str(value).casefold().strip()
        for name, value in scalar_fields.items()
    }
    if normalized_scalar_fields != expected_scalar_fields:
        raise ValueError(
            "Policy stanze: l'instradamento canonico delle sezioni non puo' cambiare."
        )
    scan_depth = raw.get("scan_depth")
    if (
        isinstance(scan_depth, bool)
        or not isinstance(scan_depth, int)
        or scan_depth != 2
    ):
        raise ValueError("Policy stanze: scan_depth deve essere esattamente 2.")

    return RoomLifecyclePolicy(
        classifications=tuple(value.strip() for value in classifications),
        root_owned_classifications=tuple(
            value.strip() for value in root_owned_classifications
        ),
        root_owned_registry_paths=normalized_registry_paths,
        room_required_files=tuple(value.strip() for value in required_files),
        bridge_content=bridge_content,
        map_template=map_template,
        source_template=source_template,
        required_sections=normalized_required_sections,
        required_terms=normalized_required_terms,
        required_terms_section=str(
            scalar_fields["required_terms_section"]
        ).casefold().strip(),
        owner_source_section=str(scalar_fields["owner_source_section"]).casefold().strip(),
        business_source_section=str(
            scalar_fields["business_source_section"]
        ).casefold().strip(),
        owner_source_headings=normalized_source_headings,
        contents_section=str(scalar_fields["contents_section"]).casefold().strip(),
        scan_depth=scan_depth,
        standard_room_paths=normalized_standard_rooms,
    )


def declared_agent(agents_text: str) -> str | None:
    match = re.search(
        r"Modalita' installata:\s*`(codex|claude|both)`",
        agents_text,
        flags=re.IGNORECASE,
    )
    return match.group(1).casefold() if match else None


def detected_agents(contract: dict[str, Any], target: Path) -> set[str]:
    active: set[str] = set()
    for agent in ("codex", "claude"):
        agent_required = set(contract["agents"][agent].get("required", []))
        if any((target / rel).exists() for rel in agent_required):
            active.add(agent)
    return active


def _string_tuple(raw: Any, label: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(raw, list) or any(
        not isinstance(item, str) or not item.strip() for item in raw
    ):
        raise ValueError(f"{label} deve essere una lista di testi non vuoti.")
    values = tuple(item.strip() for item in raw)
    if not values and not allow_empty:
        raise ValueError(f"{label} non puo' essere vuota.")
    if len(set(values)) != len(values):
        raise ValueError(f"{label} contiene duplicati.")
    return values


def _positive_int(raw: Any, label: str) -> int:
    if not isinstance(raw, int) or isinstance(raw, bool) or raw <= 0:
        raise ValueError(f"{label} deve essere un intero positivo.")
    return raw


def process_census_policy(contract: dict[str, Any]) -> ProcessCensusPolicy:
    """Legge e valida il contratto dell'Agente Censitore (Passo 2).

    Nessun default locale: un campo mancante o incoerente blocca il contratto,
    cosi' l'agente non censisce mai con regole implicite."""

    policies = contract.get("inspection_policies")
    if not isinstance(policies, dict):
        raise ValueError("Contratto privo delle policy di ispezione.")
    raw = policies.get("process_census")
    if not isinstance(raw, dict):
        raise ValueError("Contratto privo della policy process_census.")

    agent_name = str(raw.get("agent_name", "")).strip()
    skill_name = str(raw.get("skill_name", "")).strip()
    if not agent_name or not skill_name:
        raise ValueError("process_census richiede agent_name e skill_name.")
    phase_served = _positive_int(raw.get("phase_served"), "phase_served")
    next_phase = _positive_int(raw.get("next_phase"), "next_phase")
    if next_phase != phase_served + 1:
        raise ValueError("Il Censitore consegna soltanto al passo successivo.")
    if raw.get("read_only") is not True:
        raise ValueError("Il Censitore deve dichiarare read_only true.")

    certainty_levels = _string_tuple(raw.get("certainty_levels"), "certainty_levels")
    rules = raw.get("certainty_rules")
    if not isinstance(rules, dict) or set(rules) != set(certainty_levels):
        raise ValueError(
            "certainty_rules deve descrivere esattamente ogni livello di certezza."
        )
    allowed_sources = _string_tuple(raw.get("allowed_sources"), "allowed_sources")
    glossario = raw.get("allowed_sources_glossario")
    if not isinstance(glossario, dict) or set(glossario) != set(allowed_sources):
        raise ValueError(
            "allowed_sources_glossario deve descrivere esattamente ogni fonte ammessa."
        )
    consent_sources = _string_tuple(
        raw.get("consent_required_sources"), "consent_required_sources"
    )
    if set(consent_sources) - set(allowed_sources):
        raise ValueError("consent_required_sources deve essere dentro allowed_sources.")

    scan = raw.get("scan_policy")
    if not isinstance(scan, dict):
        raise ValueError("process_census richiede scan_policy.")
    if scan.get("structure_before_content") is not True:
        raise ValueError("scan_policy deve leggere la struttura prima del contenuto.")
    if scan.get("content_only_for_candidates_in_perimeter") is not True:
        raise ValueError(
            "scan_policy deve aprire contenuti solo per candidati nel perimetro."
        )
    threshold = _positive_int(
        scan.get("aggregate_threshold_items"), "aggregate_threshold_items"
    )
    reference = _positive_int(
        scan.get("volume_reference_items"), "volume_reference_items"
    )
    if threshold >= reference:
        raise ValueError(
            "La soglia degli aggregati deve stare sotto il volume di riferimento."
        )

    table_columns = _string_tuple(raw.get("table_columns"), "table_columns")
    if len(table_columns) != 10:
        raise ValueError("La tabella del censimento ha dieci colonne fisse.")
    if "certezza" not in table_columns or "prova" not in table_columns:
        raise ValueError("La tabella del censimento deve portare prova e certezza.")
    owner_decisions = _string_tuple(raw.get("owner_decisions"), "owner_decisions")
    priority_criteria = _string_tuple(raw.get("priority_criteria"), "priority_criteria")
    forbidden_estimates = _string_tuple(
        raw.get("priority_forbidden_estimates"), "priority_forbidden_estimates"
    )
    if set(priority_criteria) & set(forbidden_estimates):
        raise ValueError("La priorita' non puo' usare stime vietate.")
    registries = _string_tuple(raw.get("output_registries"), "output_registries")
    for registry in registries:
        _safe_relative(registry, "Registro del censimento")
    room_status = str(raw.get("room_status_after_census", "")).strip()
    if not room_status:
        raise ValueError("process_census richiede room_status_after_census.")

    return ProcessCensusPolicy(
        agent_name=agent_name,
        skill_name=skill_name,
        phase_served=phase_served,
        next_phase=next_phase,
        trigger_commands=_string_tuple(raw.get("trigger_commands"), "trigger_commands"),
        read_only=True,
        forbidden_actions=_string_tuple(raw.get("forbidden_actions"), "forbidden_actions"),
        certainty_levels=certainty_levels,
        path_classes=_string_tuple(raw.get("path_classes"), "path_classes"),
        allowed_sources=allowed_sources,
        consent_required_sources=consent_sources,
        always_excluded_dirs=_string_tuple(
            raw.get("always_excluded_dirs"), "always_excluded_dirs"
        ),
        always_excluded_terms=_string_tuple(
            raw.get("always_excluded_terms"), "always_excluded_terms"
        ),
        sensitive_zone_terms=_string_tuple(
            raw.get("sensitive_zone_terms"), "sensitive_zone_terms"
        ),
        aggregate_threshold_items=threshold,
        volume_reference_items=reference,
        max_sample_files_per_candidate=_positive_int(
            scan.get("max_sample_files_per_candidate"), "max_sample_files_per_candidate"
        ),
        max_duration_minutes=_positive_int(
            scan.get("max_duration_minutes"), "max_duration_minutes"
        ),
        aggregation_axes=_string_tuple(scan.get("aggregation_axes"), "aggregation_axes"),
        table_columns=table_columns,
        card_fields=_string_tuple(raw.get("card_fields"), "card_fields"),
        owner_decisions=owner_decisions,
        priority_criteria=priority_criteria,
        output_registries=registries,
        room_status_after_census=room_status,
    )


CONTRACT = load_contract()