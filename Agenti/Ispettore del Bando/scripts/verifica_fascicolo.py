#!/usr/bin/env python3
"""Valuta una pratica da un manifesto di prove e genera report e ricevuta.

Il programma non interpreta il bando e non invia nulla: rende deterministici
quadratura, integrita delle evidenze e vocabolario del verdetto. Il giudizio sui
documenti resta all'agente, che deve leggerli prima di compilare il manifesto.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


STATI = {"PROVATO", "BLOCCO", "IN_ATTESA_ESTERNA", "PASSAGGIO_UMANO"}
GESTI_UMANI = {
    "accesso",
    "2fa",
    "firma",
    "dichiarazione",
    "pagamento",
    "invio-finale",
    "scelta-titolare",
}
ID_GESTI_UMANI = {
    "accesso": "accesso",
    "2fa": "2fa",
    "firma": "firma-titolare",
    "dichiarazione": "dichiarazione-titolare",
    "pagamento": "pagamento",
    "invio-finale": "invio-finale",
    "scelta-titolare": "scelta-titolare",
}
GESTI_PER_FASE = {
    "preparazione": {"accesso", "2fa", "dichiarazione", "scelta-titolare"},
    "firma": {"accesso", "2fa", "firma"},
    "pagamento": {"accesso", "2fa", "pagamento"},
    "invio": {"accesso", "2fa", "invio-finale"},
    "presentata": set(),
}
TESTI_GESTI_UMANI = {
    "accesso": "Il titolare esegue l'accesso collegato a `{path}`.",
    "2fa": "Il titolare completa la verifica 2FA collegata a `{path}`.",
    "firma": "Il titolare applica la firma digitale al file `{path}`.",
    "dichiarazione": "Il titolare conferma la dichiarazione nel file `{path}`.",
    "pagamento": "Il titolare autorizza il pagamento descritto nel file `{path}`.",
    "invio-finale": "Il titolare autorizza e compie l'invio finale del riepilogo `{path}`.",
    "scelta-titolare": "Il titolare registra la propria scelta nel documento `{path}`.",
}
VINCOLI_OGGETTO_UMANO = {
    "firma": (
        "output_finale",
        "da_firmare_evidenza",
        "firma-titolare: oggetto diverso dall'output finale da firmare.",
    ),
    "pagamento": (
        "pagamento",
        "avviso_evidenza",
        "pagamento: oggetto diverso dall'avviso di pagamento verificato.",
    ),
    "invio-finale": (
        "output_finale",
        "riepilogo_invio_evidenza",
        "invio-finale: oggetto diverso dal riepilogo finale verificato.",
    ),
}
CONTROLLI_PREPARATORI_UMANI = {
    "accesso": "accesso-preparato",
    "2fa": "2fa-preparata",
    "dichiarazione": "dichiarazione-da-confermare",
    "scelta-titolare": "scelta-da-compiere",
}


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def _normalized_identifier(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value)).strip().casefold()


def _inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _parse_aware_datetime(value: Any) -> dt.datetime | None:
    try:
        parsed = dt.datetime.fromisoformat(str(value).strip())
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _aware_datetime(value: Any) -> bool:
    return _parse_aware_datetime(value) is not None


def _money_decimal(value: Any, *, allow_zero: bool = False) -> Decimal | None:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    if not amount.is_finite():
        return None
    minimum_ok = amount >= 0 if allow_zero else amount > 0
    if not minimum_ok or amount.as_tuple().exponent < -2:
        return None
    return amount


def _source_date_valid(value: Any) -> bool:
    text = str(value).strip()
    try:
        checked_date = dt.date.fromisoformat(text)
    except ValueError:
        checked_at = _parse_aware_datetime(text)
        if checked_at is None:
            return False
        return checked_at.astimezone(dt.timezone.utc) <= (
            dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)
        )
    return checked_date <= dt.date.today()


def _structured_human_action(
    control: dict[str, Any],
    category: str,
    valid_evidence: set[str],
    evidence_by_id: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    control_id = str(control.get("id", "")).strip()
    if str(control.get("azione", "")).strip():
        return (
            "",
            f"{control_id}: PASSAGGIO_UMANO deve usare campi strutturati, non azione libera.",
        )
    evidence_id = str(control.get("oggetto_evidenza", "")).strip()
    refs = set(control.get("evidenze", []))
    if evidence_id not in valid_evidence or evidence_id not in refs:
        return "", f"{control_id}: gesto umano senza oggetto_evidenza integro."
    evidence_path = str(evidence_by_id.get(evidence_id, {}).get("path", "")).strip()
    if not evidence_path:
        return "", f"{control_id}: gesto umano senza oggetto_evidenza integro."
    return TESTI_GESTI_UMANI[category].format(path=evidence_path), ""


def _valid_evidence(manifest: dict[str, Any], root: Path) -> tuple[set[str], list[str]]:
    valid: set[str] = set()
    errors: list[str] = []
    seen: set[str] = set()
    for item in manifest.get("evidenze", []):
        evidence_id = str(item.get("id", "")).strip()
        relative = str(item.get("path", "")).strip()
        expected_hash = str(item.get("sha256", "")).strip().lower()
        label = evidence_id or relative or "evidenza-senza-id"
        if not evidence_id or evidence_id in seen:
            errors.append(f"{label}: identificativo assente o duplicato")
            continue
        seen.add(evidence_id)
        candidate = root / relative
        if not relative or not _inside(root, candidate):
            errors.append(f"{label}: percorso non valido")
            continue
        if not candidate.is_file():
            errors.append(f"{label}: file assente")
            continue
        if len(expected_hash) != 64:
            errors.append(f"{label}: impronta SHA-256 assente o non valida")
            continue
        actual_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"{label}: impronta SHA-256 diversa")
            continue
        valid.add(evidence_id)
    return valid, errors


def _document_inventory(label: str, root: Path) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    relative_root = Path("spese") / label
    directory = root / relative_root
    if not directory.is_dir():
        return set(), [f"Inventario {label}: cartella canonica assente: {relative_root}."]
    if directory.is_symlink():
        return set(), [f"Inventario {label}: la cartella canonica e un collegamento simbolico."]
    files: set[str] = set()
    for candidate in directory.rglob("*"):
        if candidate.is_symlink():
            errors.append(
                f"Inventario {label}: collegamento simbolico non ammesso: "
                f"{candidate.relative_to(root)}."
            )
        elif candidate.is_file():
            if not _inside(root, candidate):
                errors.append(f"Inventario {label}: file fuori pratica: {candidate}.")
            else:
                files.add(str(candidate.resolve()))
    return files, errors


def _expense_blocks(
    spese: dict[str, Any],
    valid_evidence: set[str],
    official_source_evidence: set[str],
    evidence_by_id: dict[str, dict[str, Any]],
    root: Path,
    controls_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    blocks: list[str] = []
    requested = spese.get("richieste", True)
    if not isinstance(requested, bool):
        return ["Spese: campo richieste non valido."]
    if requested is False:
        control = controls_by_id.get("spese-non-richieste")
        evidence_id = str(spese.get("fonte_non_richieste_evidenza", "")).strip()
        refs = set(control.get("evidenze", [])) if control else set()
        if not (
            control
            and control.get("stato") == "PROVATO"
            and evidence_id
            and evidence_id in valid_evidence
            and evidence_id in official_source_evidence
            and evidence_id in refs
        ):
            blocks.append("Spese dichiarate non richieste senza prova sulla fonte ufficiale.")
        return blocks
    invoice_inventory, invoice_inventory_errors = _document_inventory("fatture", root)
    payment_inventory, payment_inventory_errors = _document_inventory("pagamenti", root)
    blocks.extend(invoice_inventory_errors)
    blocks.extend(payment_inventory_errors)
    count_fields = (
        "fatture_attese",
        "fatture_trovate",
        "pagamenti_trovati",
        "coppie_verificate",
        "coppie_irrisolte",
    )
    counts: dict[str, int] = {}
    for field in count_fields:
        value = spese.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blocks.append(f"Spese: campo {field} assente o non valido.")
        else:
            counts[field] = value
    if len(counts) == len(count_fields):
        expected = counts["fatture_attese"]
        verified = counts["coppie_verificate"]
        unresolved = counts["coppie_irrisolte"]
        if (
            expected == 0
            or counts["fatture_trovate"] != expected
            or counts["pagamenti_trovati"] != expected
            or verified != expected
            or unresolved != 0
        ):
            blocks.append(
                f"Quadratura spese incompleta: {verified}/{expected} coppie verificate, "
                f"{unresolved} irrisolte dichiarate."
            )
    for field in ("totale_ammesso_eur", "totale_escluso_eur"):
        if _money_decimal(spese.get(field), allow_zero=True) is None:
            blocks.append(f"Spese: campo {field} assente o non valido.")
    refs = spese.get("evidenze", [])
    if not refs or any(ref not in valid_evidence for ref in refs):
        blocks.append("Quadratura spese priva di evidenza integra.")
    index_relative = str(spese.get("indice_csv", "")).strip()
    index_path = root / index_relative
    if not index_relative or not _inside(root, index_path) or not index_path.is_file():
        blocks.append("Prospetto spese CSV assente o fuori dalla cartella della pratica.")
        return blocks
    index_resolved = index_path.resolve()
    index_is_integral_evidence = any(
        ref in valid_evidence
        and bool(str(evidence_by_id.get(ref, {}).get("path", "")).strip())
        and (root / str(evidence_by_id[ref]["path"])).resolve() == index_resolved
        for ref in refs
    )
    if not index_is_integral_evidence:
        blocks.append(
            "Il prospetto indicato da indice_csv non coincide con un'evidenza integra delle spese."
        )

    required_columns = (
        "coppia_id",
        "fattura_path",
        "fattura_sha256",
        "pagamento_path",
        "pagamento_sha256",
        "fornitore_id",
        "numero_fattura",
        "data_fattura",
        "data_pagamento",
        "riferimento_pagamento",
        "importo_eur",
        "stato",
        "attesa_controllo_id",
    )
    with index_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing_columns = [column for column in required_columns if column not in (reader.fieldnames or [])]
        if missing_columns:
            blocks.append(f"Prospetto spese: colonne mancanti: {', '.join(missing_columns)}.")
            return blocks
        rows = list(reader)

    pair_ids: set[str] = set()
    invoice_paths: set[str] = set()
    payment_paths: set[str] = set()
    invoice_hashes: set[str] = set()
    payment_hashes: set[str] = set()
    invoice_keys: set[tuple[str, str, str]] = set()
    payment_references: set[str] = set()
    admitted = Decimal("0.00")
    excluded = Decimal("0.00")
    for line_number, row in enumerate(rows, 2):
        pair_id = row["coppia_id"].strip()
        if not pair_id:
            blocks.append(f"Prospetto spese: coppia_id assente alla riga {line_number}.")
        elif pair_id in pair_ids:
            blocks.append(f"Prospetto spese: coppia_id duplicato alla riga {line_number}: {pair_id}.")
        pair_ids.add(pair_id)

        for kind, path_field, hash_field, seen, seen_hashes in (
            ("fattura", "fattura_path", "fattura_sha256", invoice_paths, invoice_hashes),
            (
                "pagamento",
                "pagamento_path",
                "pagamento_sha256",
                payment_paths,
                payment_hashes,
            ),
        ):
            relative = row[path_field].strip()
            expected_hash = row[hash_field].strip().lower()
            candidate = root / relative
            resolved = str(candidate.resolve())
            if not relative or not _inside(root, candidate) or not candidate.is_file():
                blocks.append(f"Prospetto spese: {kind} assente o fuori pratica alla riga {line_number}.")
            elif resolved in seen:
                blocks.append(f"Prospetto spese: {kind} duplicato alla riga {line_number}: {relative}.")
            elif len(expected_hash) != 64:
                blocks.append(f"Prospetto spese: SHA-256 {kind} non valido alla riga {line_number}.")
            elif expected_hash in seen_hashes:
                blocks.append(f"Prospetto spese: SHA-256 {kind} duplicato alla riga {line_number}.")
            elif hashlib.sha256(candidate.read_bytes()).hexdigest() != expected_hash:
                blocks.append(f"Prospetto spese: SHA-256 {kind} diverso alla riga {line_number}.")
            seen.add(resolved)
            if len(expected_hash) == 64:
                seen_hashes.add(expected_hash)

        supplier_id = _normalized_identifier(row["fornitore_id"])
        invoice_number = _normalized_identifier(row["numero_fattura"])
        invoice_date = row["data_fattura"].strip()
        payment_reference = _normalized_identifier(row["riferimento_pagamento"])
        if not supplier_id:
            blocks.append(f"Prospetto spese: fornitore_id assente alla riga {line_number}.")
        if not invoice_number:
            blocks.append(f"Prospetto spese: numero_fattura assente alla riga {line_number}.")
        invoice_key = (supplier_id, invoice_number, invoice_date)
        if all(invoice_key):
            if invoice_key in invoice_keys:
                blocks.append(f"Prospetto spese: chiave fattura duplicata alla riga {line_number}.")
            invoice_keys.add(invoice_key)
        if not payment_reference:
            blocks.append(f"Prospetto spese: riferimento_pagamento assente alla riga {line_number}.")
        elif payment_reference in payment_references:
            blocks.append(f"Prospetto spese: riferimento_pagamento duplicato alla riga {line_number}.")
        payment_references.add(payment_reference)

        for date_field in ("data_fattura", "data_pagamento"):
            try:
                dt.date.fromisoformat(row[date_field].strip())
            except ValueError:
                blocks.append(f"Prospetto spese: {date_field} non valida alla riga {line_number}.")
        amount = _money_decimal(row["importo_eur"].strip())
        if amount is None:
            blocks.append(f"Prospetto spese: importo_eur non valido alla riga {line_number}.")
            amount = Decimal("0.00")
        state = row["stato"].strip()
        if state == "AMMESSA":
            admitted += amount
        elif state == "ESCLUSA":
            excluded += amount
        elif state == "IN_ATTESA":
            wait_id = row["attesa_controllo_id"].strip()
            wait_control = controls_by_id.get(wait_id)
            if not wait_id or not wait_control or wait_control.get("stato") != "IN_ATTESA_ESTERNA":
                blocks.append(
                    f"Prospetto spese: attesa senza controllo esterno valido alla riga {line_number}."
                )
        else:
            blocks.append(f"Prospetto spese: stato non valido alla riga {line_number}: {state}.")

    if len(rows) != counts.get("fatture_attese", -1):
        blocks.append(
            f"Prospetto spese: {len(rows)} righe reali contro {counts.get('fatture_attese', 0)} attese."
        )
    if invoice_hashes.intersection(payment_hashes):
        blocks.append("Prospetto spese: stesso contenuto usato come fattura e pagamento.")
    if invoice_inventory != invoice_paths:
        blocks.append(
            f"Inventario fatture: {len(invoice_inventory)} file presenti, "
            f"{len(invoice_paths)} indicizzati."
        )
    if payment_inventory != payment_paths:
        blocks.append(
            f"Inventario pagamenti: {len(payment_inventory)} file presenti, "
            f"{len(payment_paths)} indicizzati."
        )
    try:
        declared_admitted = Decimal(str(spese.get("totale_ammesso_eur")))
        if declared_admitted != admitted:
            blocks.append(
                f"Totale ammesso dichiarato EUR {declared_admitted:.2f}, "
                f"calcolato dal prospetto EUR {admitted:.2f}."
            )
        declared_excluded = Decimal(str(spese.get("totale_escluso_eur")))
        if declared_excluded != excluded:
            blocks.append(
                f"Totale escluso dichiarato EUR {declared_excluded:.2f}, "
                f"calcolato dal prospetto EUR {excluded:.2f}."
            )
    except (InvalidOperation, TypeError, ValueError):
        pass
    return blocks


def _signature_validation_blocks(
    manifest: dict[str, Any], valid_evidence: set[str], controls_by_id: dict[str, dict[str, Any]]
) -> list[str]:
    control = controls_by_id.get("validazione-firma-digitale")
    metadata = manifest.get("validazione_firma", {})
    if not control or control.get("stato") != "PROVATO":
        return ["Validazione della firma digitale assente prima del pagamento o invio finale."]
    refs = set(control.get("evidenze", []))
    signed_id = str(metadata.get("file_firmato_evidenza", "")).strip()
    receipt_id = str(metadata.get("ricevuta_evidenza", "")).strip()
    original_id = str(metadata.get("originale_evidenza", "")).strip()
    original_hash = str(metadata.get("originale_sha256", "")).strip().lower()
    evidence_by_id = {
        str(item.get("id", "")).strip(): item for item in manifest.get("evidenze", [])
    }
    expected_original_id = str(
        manifest.get("output_finale", {}).get("da_firmare_evidenza", "")
    ).strip()
    expected_original_hash = str(
        evidence_by_id.get(expected_original_id, {}).get("sha256", "")
    ).strip().lower()
    if not (
        expected_original_id
        and original_id == expected_original_id
        and original_id in valid_evidence
        and original_id in refs
        and len(expected_original_hash) == 64
        and original_hash == expected_original_hash
    ):
        return ["Validazione firma digitale non riferita all'output finale originale."]
    role_ids = {original_id, signed_id, receipt_id}
    role_hashes = {
        str(evidence_by_id.get(role_id, {}).get("sha256", "")).strip().lower()
        for role_id in role_ids
    }
    if len(role_ids) != 3 or len(role_hashes) != 3 or "" in role_hashes:
        return [
            "Originale, file firmato e ricevuta di validazione devono essere distinti."
        ]
    signed_path = str(evidence_by_id.get(signed_id, {}).get("path", "")).lower()
    required = {
        "formato": metadata.get("formato") == "CAdES",
        "estensione": signed_path.endswith(".p7m"),
        "firmatario": bool(metadata.get("firmatario_atteso"))
        and metadata.get("firmatario_atteso") == metadata.get("firmatario_verificato"),
        "file": signed_id in valid_evidence and signed_id in refs,
        "ricevuta": receipt_id in valid_evidence and receipt_id in refs,
        "strumento": bool(str(metadata.get("strumento", "")).strip()),
        "data": _aware_datetime(metadata.get("verificata_il")),
        "esito": metadata.get("esito") == "VALIDA",
    }
    missing = [name for name, ok in required.items() if not ok]
    if missing:
        return [f"Validazione firma digitale incompleta: {', '.join(missing)}."]
    return []


def _signature_exemption_blocks(
    manifest: dict[str, Any],
    valid_evidence: set[str],
    official_source_evidence: set[str],
    controls_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    control = controls_by_id.get("firma-non-richiesta")
    metadata = manifest.get("validazione_firma", {})
    evidence_id = str(metadata.get("fonte_non_richiesta_evidenza", "")).strip()
    refs = set(control.get("evidenze", [])) if control else set()
    if not (
        control
        and control.get("stato") == "PROVATO"
        and evidence_id
        and evidence_id in valid_evidence
        and evidence_id in official_source_evidence
        and evidence_id in refs
    ):
        return ["Firma dichiarata non richiesta senza prova sulla fonte ufficiale."]
    return []


def _payment_blocks(
    manifest: dict[str, Any],
    phase: str,
    valid_evidence: set[str],
    official_source_evidence: set[str],
    controls_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    if phase not in {"pagamento", "invio", "presentata"}:
        return []
    payment = manifest.get("pagamento", {})
    requested = payment.get("richiesto", True)
    if not isinstance(requested, bool):
        return ["Pagamento: campo richiesto non valido."]
    if requested is False:
        control = controls_by_id.get("pagamento-non-richiesto")
        evidence_id = str(payment.get("fonte_non_richiesto_evidenza", "")).strip()
        refs = set(control.get("evidenze", [])) if control else set()
        if not (
            control
            and control.get("stato") == "PROVATO"
            and evidence_id
            and evidence_id in valid_evidence
            and evidence_id in official_source_evidence
            and evidence_id in refs
        ):
            return ["Pagamento dichiarato non richiesto senza prova sulla fonte ufficiale."]
        if phase == "pagamento":
            return ["Fase pagamento usata anche se la fonte ufficiale non lo richiede."]
        return []
    notice_id = str(payment.get("avviso_evidenza", "")).strip()
    notice_hash = str(payment.get("avviso_sha256", "")).strip().lower()
    evidence_by_id = {
        str(item.get("id", "")).strip(): item for item in manifest.get("evidenze", [])
    }
    recorded_notice_hash = str(
        evidence_by_id.get(notice_id, {}).get("sha256", "")
    ).strip().lower()
    expected_amount = _money_decimal(payment.get("importo_atteso_eur"))
    expected_reference = _normalized_identifier(payment.get("riferimento_atteso", ""))
    notice_control = controls_by_id.get("avviso-pagamento")
    notice_refs = set(notice_control.get("evidenze", [])) if notice_control else set()
    notice_proven = bool(
        notice_control
        and notice_control.get("stato") == "PROVATO"
        and notice_id
        and notice_id in valid_evidence
        and notice_id in notice_refs
        and len(recorded_notice_hash) == 64
        and notice_hash == recorded_notice_hash
        and expected_amount is not None
        and expected_reference
    )
    reserved_notice_ids = {
        str(manifest.get("validazione_firma", {}).get("originale_evidenza", "")).strip(),
        str(manifest.get("validazione_firma", {}).get("file_firmato_evidenza", "")).strip(),
        str(manifest.get("validazione_firma", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("output_finale", {}).get("riepilogo_invio_evidenza", "")).strip(),
        str(manifest.get("presentazione", {}).get("ricevuta_evidenza", "")).strip(),
    }
    reserved_notice_ids.discard("")
    reserved_notice_hashes = {
        str(evidence_by_id.get(role_id, {}).get("sha256", "")).strip().lower()
        for role_id in reserved_notice_ids
    }
    reserved_notice_hashes.discard("")
    notice_overlaps = bool(
        notice_id
        and (notice_id in reserved_notice_ids or recorded_notice_hash in reserved_notice_hashes)
    )
    if phase == "pagamento":
        human_control = controls_by_id.get("pagamento")
        human_refs = set(human_control.get("evidenze", [])) if human_control else set()
        if not (
            notice_proven
            and human_control
            and human_control.get("stato") == "PASSAGGIO_UMANO"
            and notice_id in human_refs
        ):
            return ["Avviso di pagamento incompleto prima del gesto del titolare."]
        if notice_overlaps:
            return ["Avviso di pagamento sovrapposto a un altro artefatto della pratica."]
        return []
    if not notice_id:
        return ["Pagamento non provato prima dell'invio finale."]
    if not notice_proven:
        return ["Pagamento completato non riferito all'avviso originale."]
    if notice_overlaps:
        return ["Avviso di pagamento sovrapposto a un altro artefatto della pratica."]
    control = controls_by_id.get("pagamento-completato")
    receipt_id = str(payment.get("ricevuta_evidenza", "")).strip()
    refs = set(control.get("evidenze", [])) if control else set()
    recorded_receipt_hash = str(
        evidence_by_id.get(receipt_id, {}).get("sha256", "")
    ).strip().lower()
    paid_amount = _money_decimal(payment.get("importo_eur"))
    amount_is_valid = paid_amount is not None
    if not (
        control
        and control.get("stato") == "PROVATO"
        and receipt_id
        and receipt_id in valid_evidence
        and receipt_id in refs
        and amount_is_valid
        and str(payment.get("riferimento", "")).strip()
        and _aware_datetime(payment.get("eseguito_il"))
    ):
        return ["Pagamento non provato prima dell'invio finale."]
    if notice_id == receipt_id or (
        recorded_notice_hash and recorded_notice_hash == recorded_receipt_hash
    ):
        return ["Avviso e ricevuta di pagamento devono essere evidenze distinte."]
    paid_reference = _normalized_identifier(payment.get("riferimento", ""))
    if not (
        notice_id
        and notice_id in valid_evidence
        and notice_id in refs
        and len(recorded_notice_hash) == 64
        and notice_hash == recorded_notice_hash
        and expected_amount is not None
        and paid_amount == expected_amount
        and expected_reference
        and paid_reference == expected_reference
    ):
        return ["Pagamento completato non riferito all'avviso originale."]
    return []


def _chronology_blocks(manifest: dict[str, Any], phase: str) -> list[str]:
    if phase not in {"pagamento", "invio", "presentata"}:
        return []
    signature_time = None
    if manifest.get("validazione_firma", {}).get("richiesta", True) is not False:
        signature_time = _parse_aware_datetime(
            manifest.get("validazione_firma", {}).get("verificata_il")
        )
    payment_time = None
    if manifest.get("pagamento", {}).get("richiesto", True) is not False:
        payment_time = _parse_aware_datetime(manifest.get("pagamento", {}).get("eseguito_il"))
    presentation_time = None
    if phase == "presentata":
        presentation_time = _parse_aware_datetime(
            manifest.get("presentazione", {}).get("presentata_il")
        )
    now_limit = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)
    if any(
        event_time and event_time.astimezone(dt.timezone.utc) > now_limit
        for event_time in (signature_time, payment_time, presentation_time)
    ):
        return ["Cronologia futura impossibile per una fase dichiarata completata."]
    if signature_time and payment_time and signature_time > payment_time:
        return ["Cronologia impossibile tra firma, pagamento e presentazione."]
    if presentation_time and any(
        event_time and event_time > presentation_time
        for event_time in (signature_time, payment_time)
    ):
        return ["Cronologia impossibile tra firma, pagamento e presentazione."]
    return []


def _receipt_role_blocks(manifest: dict[str, Any]) -> list[str]:
    evidence_by_id = {
        str(item.get("id", "")).strip(): item for item in manifest.get("evidenze", [])
    }
    receipt_ids = [
        str(manifest.get("validazione_firma", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("pagamento", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("presentazione", {}).get("ricevuta_evidenza", "")).strip(),
    ]
    receipt_ids = [receipt_id for receipt_id in receipt_ids if receipt_id]
    receipt_hashes = [
        str(evidence_by_id.get(receipt_id, {}).get("sha256", "")).strip().lower()
        for receipt_id in receipt_ids
    ]
    known_hashes = [receipt_hash for receipt_hash in receipt_hashes if receipt_hash]
    if len(receipt_ids) != len(set(receipt_ids)) or len(known_hashes) != len(set(known_hashes)):
        return ["Le ricevute di firma, pagamento e protocollo devono essere distinte."]
    return []


def _critical_artifact_role_blocks(manifest: dict[str, Any]) -> list[str]:
    evidence_by_id = {
        str(item.get("id", "")).strip(): item for item in manifest.get("evidenze", [])
    }
    role_ids = [
        str(manifest.get("validazione_firma", {}).get("originale_evidenza", "")).strip(),
        str(manifest.get("validazione_firma", {}).get("file_firmato_evidenza", "")).strip(),
        str(manifest.get("validazione_firma", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("pagamento", {}).get("avviso_evidenza", "")).strip(),
        str(manifest.get("pagamento", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("output_finale", {}).get("riepilogo_invio_evidenza", "")).strip(),
        str(manifest.get("presentazione", {}).get("ricevuta_evidenza", "")).strip(),
    ]
    role_ids = [role_id for role_id in role_ids if role_id]
    role_hashes = [
        str(evidence_by_id.get(role_id, {}).get("sha256", "")).strip().lower()
        for role_id in role_ids
    ]
    known_hashes = [role_hash for role_hash in role_hashes if role_hash]
    if len(role_ids) != len(set(role_ids)) or len(known_hashes) != len(set(known_hashes)):
        return ["Gli artefatti critici della pratica devono avere ruoli distinti."]
    return []


def _final_summary_blocks(
    manifest: dict[str, Any],
    phase: str,
    valid_evidence: set[str],
    controls_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    if phase not in {"invio", "presentata"}:
        return []
    evidence_by_id = {
        str(item.get("id", "")).strip(): item for item in manifest.get("evidenze", [])
    }
    summary_id = str(
        manifest.get("output_finale", {}).get("riepilogo_invio_evidenza", "")
    ).strip()
    control = controls_by_id.get("riepilogo-finale")
    refs = set(control.get("evidenze", [])) if control else set()
    if not (
        control
        and control.get("stato") == "PROVATO"
        and summary_id
        and summary_id in valid_evidence
        and summary_id in refs
    ):
        return ["Riepilogo finale non provato prima dell'invio."]
    summary_hash = str(evidence_by_id.get(summary_id, {}).get("sha256", "")).strip().lower()
    reserved_ids = {
        str(manifest.get("validazione_firma", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("pagamento", {}).get("avviso_evidenza", "")).strip(),
        str(manifest.get("pagamento", {}).get("ricevuta_evidenza", "")).strip(),
        str(manifest.get("presentazione", {}).get("ricevuta_evidenza", "")).strip(),
    }
    reserved_ids.discard("")
    reserved_hashes = {
        str(evidence_by_id.get(role_id, {}).get("sha256", "")).strip().lower()
        for role_id in reserved_ids
    }
    reserved_hashes.discard("")
    if summary_id in reserved_ids or summary_hash in reserved_hashes:
        return ["Riepilogo finale sovrapposto ad avvisi o ricevute."]
    return []


def _signable_output_blocks(
    manifest: dict[str, Any],
    phase: str,
    signature_required: bool,
    valid_evidence: set[str],
    controls_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    if not signature_required or phase not in {"firma", "pagamento", "invio", "presentata"}:
        return []
    original_id = str(
        manifest.get("output_finale", {}).get("da_firmare_evidenza", "")
    ).strip()
    control = controls_by_id.get("output-da-firmare")
    refs = set(control.get("evidenze", [])) if control else set()
    if not (
        control
        and control.get("stato") == "PROVATO"
        and original_id
        and original_id in valid_evidence
        and original_id in refs
    ):
        return ["Output da firmare non provato prima del gesto del titolare."]
    return []


def valuta(manifest: dict[str, Any], root: Path) -> dict[str, Any]:
    root = root.resolve()
    valid_evidence, evidence_errors = _valid_evidence(manifest, root)
    evidence_by_id = {
        str(item.get("id", "")).strip(): item for item in manifest.get("evidenze", [])
    }
    blocks = list(evidence_errors)
    waits: list[str] = []
    human: list[str] = []
    human_entries: list[tuple[str, str]] = []
    human_objects: list[tuple[str, str]] = []
    proven: list[str] = []
    controls_by_id: dict[str, dict[str, Any]] = {}
    official_source_evidence: set[str] = set()
    if manifest.get("schema_version") != 1:
        blocks.append("Versione schema non supportata: usare 1.")
    practice = manifest.get("pratica", {})
    missing_practice_fields = [
        field
        for field in ("nome", "ente", "edizione")
        if not str(practice.get(field, "")).strip()
    ]
    if missing_practice_fields:
        blocks.append(f"Identita pratica incompleta: {', '.join(missing_practice_fields)}.")
    phase = str(practice.get("fase", "")).strip().lower()
    if phase not in GESTI_PER_FASE:
        blocks.append(
            "Fase pratica non valida: usare preparazione, firma, pagamento, invio o presentata."
        )
    declared_human_controls = 0

    sources = manifest.get("fonti_ufficiali", [])
    if not sources:
        blocks.append("Mancano le fonti ufficiali verificate.")
    for source in sources:
        name = str(source.get("nome", "")).strip()
        url = str(source.get("url", "")).strip()
        parsed_url = urlparse(url)
        state = source.get("stato")
        evidence_id = str(source.get("evidenza_id", "")).strip()
        if (
            not name
            or parsed_url.scheme != "https"
            or not parsed_url.hostname
            or not _source_date_valid(source.get("verificata_il"))
            or state != "PROVATO"
            or evidence_id not in valid_evidence
        ):
            blocks.append(f"Fonte non provata: {name or 'fonte senza nome'}.")
        else:
            official_source_evidence.add(evidence_id)

    controls = manifest.get("controlli", [])
    if not controls:
        blocks.append("La matrice dei controlli e vuota.")
    seen_controls: set[str] = set()
    for control in controls:
        control_id = str(control.get("id", "")).strip()
        label = str(control.get("voce", control_id or "controllo senza nome")).strip()
        state = control.get("stato")
        action = str(control.get("azione", "")).strip()
        refs = control.get("evidenze", [])
        if not control_id or control_id in seen_controls:
            blocks.append(f"Controllo con identificativo assente o duplicato: {label}.")
            continue
        seen_controls.add(control_id)
        controls_by_id[control_id] = control
        if state not in STATI:
            blocks.append(f"{control_id}: stato non valido.")
        elif state == "PROVATO":
            if not refs or any(ref not in valid_evidence for ref in refs):
                blocks.append(f"{control_id}: dichiarato PROVATO senza evidenza integra.")
            else:
                proven.append(label)
        elif state == "BLOCCO":
            blocks.append(action or f"Risolvere: {label}.")
        elif state == "IN_ATTESA_ESTERNA":
            waits.append(action or f"Attendere prova esterna: {label}.")
        elif state == "PASSAGGIO_UMANO":
            declared_human_controls += 1
            category = str(control.get("categoria_umana", "")).strip()
            if category not in GESTI_UMANI:
                blocks.append(f"{control_id}: '{category}' non e un gesto riservato al titolare")
            elif control_id != ID_GESTI_UMANI[category]:
                blocks.append(f"{control_id}: identificativo non canonico per {category}.")
            elif category not in GESTI_PER_FASE.get(phase, set()):
                blocks.append(f"{control_id}: gesto {category} non ammesso nella fase {phase}.")
            else:
                binding = VINCOLI_OGGETTO_UMANO.get(category)
                if binding:
                    section, field, message = binding
                    expected_id = str(manifest.get(section, {}).get(field, "")).strip()
                    actual_id = str(control.get("oggetto_evidenza", "")).strip()
                    if not expected_id or actual_id != expected_id:
                        blocks.append(message)
                        continue
                human_action, human_error = _structured_human_action(
                    control, category, valid_evidence, evidence_by_id
                )
                if human_error:
                    blocks.append(human_error)
                else:
                    human.append(human_action)
                    human_entries.append((category, human_action))
                    human_objects.append(
                        (category, str(control.get("oggetto_evidenza", "")).strip())
                    )

    if declared_human_controls > 1:
        blocks.append("Piu di un gesto umano dichiarato nella stessa fase.")
    for category, object_id in human_objects:
        preparatory_id = CONTROLLI_PREPARATORI_UMANI.get(category)
        if not preparatory_id:
            continue
        preparatory = controls_by_id.get(preparatory_id)
        preparatory_refs = set(preparatory.get("evidenze", [])) if preparatory else set()
        if not (
            preparatory
            and preparatory.get("stato") == "PROVATO"
            and object_id in valid_evidence
            and object_id in preparatory_refs
        ):
            blocks.append(f"{ID_GESTI_UMANI[category]}: preparazione non provata sullo stesso oggetto.")
            continue
        if category == "scelta-titolare":
            choice = manifest.get("scelta_titolare", {})
            options = choice.get("opzioni", [])
            normalized_options = (
                [
                    unicodedata.normalize("NFKC", str(option)).strip().casefold()
                    for option in options
                ]
                if isinstance(options, list)
                else []
            )
            if not (
                choice.get("evidenza_id") == object_id
                and str(choice.get("domanda", "")).strip()
                and 2 <= len(normalized_options) <= 5
                and all(normalized_options)
                and len(set(normalized_options)) == len(normalized_options)
            ):
                blocks.append("scelta-titolare: domanda o opzioni non valide.")

    blocks.extend(
        _expense_blocks(
            manifest.get("spese", {}),
            valid_evidence,
            official_source_evidence,
            evidence_by_id,
            root,
            controls_by_id,
        )
    )
    if (
        phase in GESTI_PER_FASE
        and phase != "presentata"
        and declared_human_controls == 0
        and not blocks
        and not waits
    ):
        blocks.append(f"Fase {phase} senza l'unico gesto umano corrente.")
    signature_setting = manifest.get("validazione_firma", {}).get("richiesta", True)
    if not isinstance(signature_setting, bool):
        blocks.append("Validazione firma: campo richiesta non valido.")
    signature_required = signature_setting is not False
    blocks.extend(
        _signable_output_blocks(
            manifest,
            phase,
            signature_required,
            valid_evidence,
            controls_by_id,
        )
    )
    if phase in {"pagamento", "invio", "presentata"}:
        if signature_required:
            blocks.extend(_signature_validation_blocks(manifest, valid_evidence, controls_by_id))
        else:
            blocks.extend(
                _signature_exemption_blocks(
                    manifest,
                    valid_evidence,
                    official_source_evidence,
                    controls_by_id,
                )
            )
    blocks.extend(
        _payment_blocks(
            manifest,
            phase,
            valid_evidence,
            official_source_evidence,
            controls_by_id,
        )
    )
    blocks.extend(_chronology_blocks(manifest, phase))
    blocks.extend(_receipt_role_blocks(manifest))
    blocks.extend(_critical_artifact_role_blocks(manifest))
    blocks.extend(_final_summary_blocks(manifest, phase, valid_evidence, controls_by_id))
    final_receipt = controls_by_id.get("ricevuta-protocollo")
    receipt_refs = set(final_receipt.get("evidenze", [])) if final_receipt else set()
    receipt_proven = bool(
        final_receipt
        and final_receipt.get("stato") == "PROVATO"
        and receipt_refs
        and receipt_refs.issubset(valid_evidence)
    )
    presentation = manifest.get("presentazione", {})
    presentation_receipt_id = str(presentation.get("ricevuta_evidenza", "")).strip()
    expected_summary_id = str(
        manifest.get("output_finale", {}).get("riepilogo_invio_evidenza", "")
    ).strip()
    declared_summary_id = str(presentation.get("riepilogo_evidenza", "")).strip()
    declared_summary_hash = str(presentation.get("riepilogo_sha256", "")).strip().lower()
    expected_summary_hash = str(
        evidence_by_id.get(expected_summary_id, {}).get("sha256", "")
    ).strip().lower()
    presentation_receipt_hash = str(
        evidence_by_id.get(presentation_receipt_id, {}).get("sha256", "")
    ).strip().lower()
    expected_practice_id = str(presentation.get("pratica_id_atteso", "")).strip()
    receipt_practice_id = str(presentation.get("pratica_id_ricevuta", "")).strip()
    date_is_valid = _aware_datetime(presentation.get("presentata_il"))
    presentation_metadata_proven = bool(
        presentation_receipt_id
        and presentation_receipt_id in receipt_refs
        and presentation_receipt_id in valid_evidence
        and str(presentation.get("numero_protocollo", "")).strip()
        and str(presentation.get("portale", "")).strip()
        and date_is_valid
    )
    presentation_continuity_proven = bool(
        expected_summary_id
        and declared_summary_id == expected_summary_id
        and expected_summary_id in valid_evidence
        and expected_summary_id in receipt_refs
        and len(expected_summary_hash) == 64
        and declared_summary_hash == expected_summary_hash
        and expected_practice_id
        and receipt_practice_id == expected_practice_id
    )
    presentation_roles_distinct = bool(
        expected_summary_id
        and presentation_receipt_id
        and expected_summary_id != presentation_receipt_id
        and expected_summary_hash
        and presentation_receipt_hash
        and expected_summary_hash != presentation_receipt_hash
    )
    if phase == "presentata":
        if not receipt_proven:
            blocks.append("Fase PRESENTATA senza ricevuta o protocollo finale provato.")
        if not presentation_metadata_proven:
            blocks.append("Fase PRESENTATA senza metadati completi della presentazione finale.")
        if not presentation_continuity_proven:
            blocks.append("Ricevuta finale non riferita al riepilogo inviato.")
        if not presentation_roles_distinct:
            blocks.append("Riepilogo inviato e ricevuta finale devono essere evidenze distinte.")
        if declared_human_controls:
            blocks.append("Fase PRESENTATA con gesti umani ancora pendenti.")
    blocks = _unique(blocks)
    waits = _unique(waits)
    human = _unique(human)
    if blocks:
        verdict = "BLOCCATO"
    elif waits:
        verdict = "IN ATTESA"
    else:
        verdict = "PRONTO"
    ordered_human = human_entries
    next_human = ordered_human[0][1] if ordered_human and verdict == "PRONTO" else ""
    later_human = [action for _, action in ordered_human if action != next_human]
    return {
        "verdetto": verdict,
        "blocchi": blocks,
        "attese_esterne": waits,
        "passaggi_umani": human,
        "prossimo_passaggio_umano": next_human,
        "passaggi_umani_successivi": later_human,
        "fase_confermata": (
            "PRESENTATA"
            if phase == "presentata"
            and receipt_proven
            and presentation_metadata_proven
            and presentation_continuity_proven
            and presentation_roles_distinct
            and not human_entries
            and not blocks
            else ""
        ),
        "voci_provate": proven,
        "evidenze_valide": sorted(valid_evidence),
        "evidenze_non_valide": evidence_errors,
    }


def _numbered(items: list[str], empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def render_report(manifest: dict[str, Any], result: dict[str, Any]) -> str:
    practice = manifest.get("pratica", {})
    expenses = manifest.get("spese", {})
    expense_line = "Non previste o non ancora applicabili."
    if expenses.get("richieste"):
        expense_line = (
            f"{expenses.get('coppie_verificate', 0)}/{expenses.get('fatture_attese', 0)} coppie; "
            f"ammesso EUR {expenses.get('totale_ammesso_eur', '0.00')}; "
            f"escluso EUR {expenses.get('totale_escluso_eur', '0.00')}."
        )
    return (
        "# Ispettore del Bando\n\n"
        f"**Verdetto: {result['verdetto']}**\n\n"
        "## Situazione in breve\n\n"
        f"- Pratica: {practice.get('nome', 'non indicata')}\n"
        f"- Ente: {practice.get('ente', 'non indicato')}\n"
        f"- Edizione: {practice.get('edizione', 'non indicata')}\n"
        f"- Fase: {practice.get('fase', 'non indicata')}\n"
        f"- Evidenze integre: {len(result['evidenze_valide'])}\n"
        f"- Controlli provati: {len(result['voci_provate'])}\n"
        f"- Spese: {expense_line}\n\n"
        "## Blocchi da risolvere\n\n"
        f"{_numbered(result['blocchi'], 'Nessuno.')}\n\n"
        "## In attesa da soggetti esterni\n\n"
        f"{_numbered(result['attese_esterne'], 'Nessuna.')}\n\n"
        "## Serve al titolare\n\n"
        f"{_numbered([result['prossimo_passaggio_umano']] if result['prossimo_passaggio_umano'] else [], 'Nessun gesto in questa fase.')}\n\n"
        "## Confine del verdetto\n\n"
        "`PRONTO` significa pronto al successivo gesto umano indicato. Non significa "
        "presentato: la presentazione esiste soltanto con ricevuta o protocollo finale "
        "scaricato e verificato.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--ricevuta", type=Path, required=True)
    args = parser.parse_args()

    raw = args.manifest.read_bytes()
    manifest = json.loads(raw.decode("utf-8"))
    result = valuta(manifest, args.root)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.ricevuta.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(manifest, result), encoding="utf-8")
    receipt = {
        "esito": "ISPETTORE_BANDO_OK" if result["verdetto"] == "PRONTO" else "ISPETTORE_BANDO_STOP",
        "verdetto": result["verdetto"],
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "generata_il": dt.datetime.now(dt.timezone.utc).isoformat(),
        "report": str(args.report),
        "blocchi": result["blocchi"],
        "attese_esterne": result["attese_esterne"],
        "passaggi_umani": result["passaggi_umani"],
        "prossimo_passaggio_umano": result["prossimo_passaggio_umano"],
        "passaggi_umani_successivi": result["passaggi_umani_successivi"],
    }
    args.ricevuta.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = receipt["esito"]
    print(f"{prefix}: {result['verdetto']}")
    return 0 if result["verdetto"] == "PRONTO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
