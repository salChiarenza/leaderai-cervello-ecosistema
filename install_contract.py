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
    "claude_bridge",
    "event_log",
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


def _safe_relative(raw: str, label: str) -> str:
    path = Path(raw)
    if not raw or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} non e' un percorso relativo sicuro: {raw!r}")
    return path.as_posix()


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
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
    markdown_hygiene_policy(data)
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
            if rule.destination in seen:
                continue
            rules.append(rule)
            seen.add(rule.destination)
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


CONTRACT = load_contract()
