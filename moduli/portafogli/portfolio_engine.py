#!/usr/bin/env python3
"""Motore deterministico del Sistema Portafogli LeaderAI."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable


PORTFOLIO_FIELDS = {
    "strumento_id",
    "nome",
    "classe",
    "componente",
    "valuta",
    "quantita",
    "prezzo_corrente",
    "cambio_eur",
    "peso_target_pct",
    "prezzo_riferimento",
    "fonte",
    "data_fonte",
    "ammesso",
}

RETURNS_FIELDS = {
    "data",
    "strumento_id",
    "rendimento_mensile_pct",
    "fonte",
    "data_fonte",
}


class ValidationError(ValueError):
    """Errore dati leggibile dall'agente e dal banker."""


@dataclass(frozen=True)
class Holding:
    instrument_id: str
    name: str
    asset_class: str
    component: str
    currency: str
    quantity: float
    current_price: float
    eur_rate: float
    target_pct: float
    reference_price: float | None
    source: str
    source_date: date
    allowed: bool

    @property
    def value_eur(self) -> float:
        return self.quantity * self.current_price * self.eur_rate


def _sniff_dialect(path: Path) -> csv.Dialect:
    sample = path.read_text(encoding="utf-8-sig")[:4096]
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;")
    except csv.Error:
        return csv.excel


def _read_rows(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    if not path.exists():
        raise ValidationError(f"File assente: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, dialect=_sniff_dialect(path))
        fields = {field.strip() for field in (reader.fieldnames or [])}
        rows = []
        for raw in reader:
            row = {(key or "").strip(): (value or "").strip() for key, value in raw.items()}
            if any(row.values()):
                rows.append(row)
    return rows, fields


def _parse_number(value: str, field: str, row_number: int, *, required: bool = True) -> float | None:
    text = value.strip().replace(" ", "").replace("%", "")
    if not text:
        if required:
            raise ValidationError(f"Riga {row_number}: campo {field} vuoto")
        return None
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        number = float(text)
    except ValueError as exc:
        raise ValidationError(f"Riga {row_number}: {field} non numerico ({value!r})") from exc
    if not math.isfinite(number):
        raise ValidationError(f"Riga {row_number}: {field} deve essere finito")
    return number


def _parse_date(value: str, field: str, row_number: int) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(
            f"Riga {row_number}: {field} deve usare AAAA-MM-GG ({value!r})"
        ) from exc
    if parsed > date.today():
        raise ValidationError(f"Riga {row_number}: {field} è nel futuro ({value})")
    return parsed


def _parse_month(value: str, row_number: int) -> str:
    text = value.strip()
    for fmt in ("%Y-%m", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m")
        except ValueError:
            continue
    raise ValidationError(f"Riga {row_number}: data mese non valida ({value!r})")


def _parse_bool(value: str, row_number: int) -> bool:
    normalized = value.strip().lower()
    if normalized in {"si", "sì", "true", "1", "yes"}:
        return True
    if normalized in {"no", "false", "0"}:
        return False
    raise ValidationError(f"Riga {row_number}: ammesso deve essere SI/NO ({value!r})")


def load_portfolio(path: Path) -> list[Holding]:
    rows, fields = _read_rows(path)
    missing = PORTFOLIO_FIELDS - fields
    if missing:
        raise ValidationError(f"Colonne portafoglio mancanti: {', '.join(sorted(missing))}")
    if not rows:
        raise ValidationError("Il portafoglio non contiene righe")

    holdings: list[Holding] = []
    ids: set[str] = set()
    for index, row in enumerate(rows, start=2):
        instrument_id = row["strumento_id"].strip()
        if not instrument_id:
            raise ValidationError(f"Riga {index}: strumento_id vuoto")
        if instrument_id in ids:
            raise ValidationError(f"Riga {index}: strumento_id duplicato ({instrument_id})")
        ids.add(instrument_id)

        component = row["componente"].strip().upper()
        if component not in {"CORE", "SATELLITE"}:
            raise ValidationError(f"Riga {index}: componente deve essere CORE o SATELLITE")

        currency = row["valuta"].strip().upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ValidationError(f"Riga {index}: valuta non valida ({row['valuta']!r})")

        quantity = _parse_number(row["quantita"], "quantita", index)
        current_price = _parse_number(row["prezzo_corrente"], "prezzo_corrente", index)
        eur_rate = _parse_number(row["cambio_eur"], "cambio_eur", index)
        target_pct = _parse_number(row["peso_target_pct"], "peso_target_pct", index)
        reference_price = _parse_number(
            row["prezzo_riferimento"], "prezzo_riferimento", index, required=False
        )
        allowed = _parse_bool(row["ammesso"], index)

        assert quantity is not None
        assert current_price is not None
        assert eur_rate is not None
        assert target_pct is not None
        if quantity < 0 or current_price <= 0 or eur_rate <= 0:
            raise ValidationError(
                f"Riga {index}: quantità >= 0, prezzo e cambio > 0 sono obbligatori"
            )
        if not 0 <= target_pct <= 100:
            raise ValidationError(f"Riga {index}: peso_target_pct fuori intervallo 0-100")
        if target_pct > 0 and not allowed:
            raise ValidationError(
                f"Riga {index}: {instrument_id} ha target positivo ed è fuori universo ammesso"
            )
        if component == "SATELLITE" and reference_price is None:
            raise ValidationError(
                f"Riga {index}: prezzo_riferimento richiesto per il satellite {instrument_id}"
            )
        if reference_price is not None and reference_price <= 0:
            raise ValidationError(f"Riga {index}: prezzo_riferimento deve essere positivo")
        if not row["fonte"].strip():
            raise ValidationError(f"Riga {index}: fonte vuota")

        holdings.append(
            Holding(
                instrument_id=instrument_id,
                name=row["nome"].strip(),
                asset_class=row["classe"].strip(),
                component=component,
                currency=currency,
                quantity=quantity,
                current_price=current_price,
                eur_rate=eur_rate,
                target_pct=target_pct,
                reference_price=reference_price,
                source=row["fonte"].strip(),
                source_date=_parse_date(row["data_fonte"], "data_fonte", index),
                allowed=allowed,
            )
        )

    target_total = sum(item.target_pct for item in holdings)
    if not math.isclose(target_total, 100.0, abs_tol=0.01):
        raise ValidationError(f"La somma dei pesi target è {target_total:.4f}, deve essere 100")
    if sum(item.value_eur for item in holdings) <= 0:
        raise ValidationError("Il valore totale del portafoglio deve essere positivo")
    return holdings


def analyze_portfolio(holdings: list[Holding], alert_threshold_pct: float = 5.0) -> list[dict[str, object]]:
    total = sum(item.value_eur for item in holdings)
    analysis: list[dict[str, object]] = []
    for item in holdings:
        current_pct = item.value_eur / total * 100
        target_value = total * item.target_pct / 100
        movement_pct = None
        alert = ""
        if item.reference_price is not None:
            movement_pct = (item.current_price / item.reference_price - 1) * 100
            if item.component == "SATELLITE" and abs(movement_pct) >= alert_threshold_pct:
                alert = "SOGLIA"
        analysis.append(
            {
                "strumento_id": item.instrument_id,
                "nome": item.name,
                "classe": item.asset_class,
                "componente": item.component,
                "valuta": item.currency,
                "valore_eur": item.value_eur,
                "peso_attuale_pct": current_pct,
                "peso_target_pct": item.target_pct,
                "drift_pct": current_pct - item.target_pct,
                "valore_target_eur": target_value,
                "delta_eur": target_value - item.value_eur,
                "movimento_da_riferimento_pct": movement_pct,
                "alert": alert,
                "fonte": item.source,
                "data_fonte": item.source_date.isoformat(),
            }
        )
    return analysis


ANALYSIS_FIELDS = [
    "strumento_id",
    "nome",
    "classe",
    "componente",
    "valuta",
    "valore_eur",
    "peso_attuale_pct",
    "peso_target_pct",
    "drift_pct",
    "valore_target_eur",
    "delta_eur",
    "movimento_da_riferimento_pct",
    "alert",
    "fonte",
    "data_fonte",
]


def _format_csv_value(field: str, value: object) -> object:
    if isinstance(value, float):
        if "pct" in field:
            return f"{value:.6f}"
        return f"{value:.2f}"
    if value is None:
        return ""
    return value


def _format_eur_it(value: float) -> str:
    return f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _format_num_it(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def _format_date_it(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def write_analysis_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ANALYSIS_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _format_csv_value(field, row[field]) for field in ANALYSIS_FIELDS})


def write_analysis_report(
    path: Path,
    holdings: list[Holding],
    analysis: list[dict[str, object]],
    alert_threshold_pct: float,
) -> None:
    total = sum(item.value_eur for item in holdings)
    oldest_date = min(item.source_date for item in holdings)
    alerts = [row for row in analysis if row["alert"]]
    lines = [
        "# Report calcoli portafoglio",
        "",
        f"- Generato: {_format_date_it(date.today())}",
        f"- Valore totale: EUR {_format_eur_it(total)}",
        f"- Somma target: {_format_num_it(sum(item.target_pct for item in holdings))}%",
        f"- Fonte più datata: {_format_date_it(oldest_date)}",
        f"- Soglia satelliti: ±{_format_num_it(alert_threshold_pct)}%",
        f"- Alert attivi: {len(alerts)}",
        "",
        "## Dettaglio",
        "",
        "| Strumento | Comp. | Attuale % | Target % | Drift p.p. | Delta EUR | Movimento % | Alert |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in analysis:
        movement = row["movimento_da_riferimento_pct"]
        movement_text = "" if movement is None else _format_num_it(float(movement))
        lines.append(
            f"| {row['strumento_id']} | {row['componente']} | "
            f"{_format_num_it(float(row['peso_attuale_pct']))} | "
            f"{_format_num_it(float(row['peso_target_pct']))} | "
            f"{_format_num_it(float(row['drift_pct']))} | "
            f"{_format_eur_it(float(row['delta_eur']))} | "
            f"{movement_text} | {row['alert']} |"
        )
    lines.extend(
        [
            "",
            "## Confine professionale",
            "",
            "Questi sono calcoli tecnici su dati e target dichiarati. Il banker valida "
            "adeguatezza, strumenti, pesi, interventi e comunicazione al cliente.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def load_monthly_returns(path: Path, target_ids: set[str]) -> dict[str, dict[str, float]]:
    rows, fields = _read_rows(path)
    missing = RETURNS_FIELDS - fields
    if missing:
        raise ValidationError(f"Colonne rendimenti mancanti: {', '.join(sorted(missing))}")
    months: dict[str, dict[str, float]] = defaultdict(dict)
    for index, row in enumerate(rows, start=2):
        month = _parse_month(row["data"], index)
        instrument_id = row["strumento_id"].strip()
        if instrument_id not in target_ids:
            continue
        if instrument_id in months[month]:
            raise ValidationError(
                f"Riga {index}: rendimento duplicato per {instrument_id} nel mese {month}"
            )
        if not row["fonte"].strip():
            raise ValidationError(f"Riga {index}: fonte rendimenti vuota")
        _parse_date(row["data_fonte"], "data_fonte", index)
        value = _parse_number(
            row["rendimento_mensile_pct"], "rendimento_mensile_pct", index
        )
        assert value is not None
        if value <= -100:
            raise ValidationError(f"Riga {index}: rendimento mensile <= -100%")
        months[month][instrument_id] = value / 100
    if not months:
        raise ValidationError("Nessun rendimento mensile utile trovato")
    for month, values in sorted(months.items()):
        missing_ids = target_ids - set(values)
        if missing_ids:
            raise ValidationError(
                f"Mese {month}: rendimenti mancanti per {', '.join(sorted(missing_ids))}"
            )
    return dict(sorted(months.items()))


def run_backtest(
    holdings: list[Holding],
    monthly_returns: dict[str, dict[str, float]],
    mode: str,
) -> list[dict[str, float | str]]:
    weights = {
        item.instrument_id: item.target_pct / 100
        for item in holdings
        if item.target_pct > 0
    }
    values = dict(weights)
    cumulative = 1.0
    peak = 1.0
    rows: list[dict[str, float | str]] = []
    for month, returns in monthly_returns.items():
        if mode == "monthly-rebalanced":
            monthly = sum(weights[key] * returns[key] for key in weights)
            cumulative *= 1 + monthly
        elif mode == "buy-and-hold":
            previous = sum(values.values())
            for key in values:
                values[key] *= 1 + returns[key]
            current = sum(values.values())
            monthly = current / previous - 1
            cumulative = current
        else:
            raise ValidationError(f"Modalità backtest sconosciuta: {mode}")
        peak = max(peak, cumulative)
        drawdown = cumulative / peak - 1
        rows.append(
            {
                "data": month,
                "rendimento_mensile_pct": monthly * 100,
                "rendimento_cumulato_pct": (cumulative - 1) * 100,
                "drawdown_pct": drawdown * 100,
            }
        )
    return rows


BACKTEST_FIELDS = [
    "data",
    "rendimento_mensile_pct",
    "rendimento_cumulato_pct",
    "drawdown_pct",
]


def write_backtest_csv(path: Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BACKTEST_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _format_csv_value(field, row[field]) for field in BACKTEST_FIELDS})


def write_backtest_report(path: Path, rows: list[dict[str, float | str]], mode: str) -> None:
    months = len(rows)
    final_cumulative = float(rows[-1]["rendimento_cumulato_pct"]) / 100
    annualized = (1 + final_cumulative) ** (12 / months) - 1
    max_drawdown = min(float(row["drawdown_pct"]) for row in rows)
    lines = [
        "# Report backtest mensile",
        "",
        f"- Periodo: {str(rows[0]['data'])[5:7]}/{str(rows[0]['data'])[:4]} → "
        f"{str(rows[-1]['data'])[5:7]}/{str(rows[-1]['data'])[:4]}",
        f"- Mesi completi: {months}",
        f"- Politica: {mode}",
        f"- Rendimento cumulato: {_format_num_it(final_cumulative * 100)}%",
        f"- Rendimento annualizzato: {_format_num_it(annualized * 100)}%",
        f"- Massimo drawdown mensile: {_format_num_it(max_drawdown)}%",
        "",
        "## Ipotesi",
        "",
        "Il calcolo usa rendimenti mensili delle fonti dichiarate. Costi, fiscalità, "
        "flussi e scostamenti inframensili entrano nel report quando sono disponibili "
        "come dati verificati.",
        "",
        "## Confine professionale",
        "",
        "Il backtest descrive il periodo osservato e supporta la valutazione del banker.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analizza", help="calcola pesi, drift, delta e alert")
    analyze.add_argument("--input", type=Path, required=True)
    analyze.add_argument("--output", type=Path, required=True)
    analyze.add_argument("--report", type=Path, required=True)
    analyze.add_argument("--alert-threshold", type=float, default=5.0)

    backtest = subparsers.add_parser("backtest", help="calcola backtest mensile")
    backtest.add_argument("--portfolio", type=Path, required=True)
    backtest.add_argument("--returns", type=Path, required=True)
    backtest.add_argument("--output", type=Path, required=True)
    backtest.add_argument("--report", type=Path, required=True)
    backtest.add_argument(
        "--mode",
        choices=("monthly-rebalanced", "buy-and-hold"),
        default="monthly-rebalanced",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "analizza":
            holdings = load_portfolio(args.input)
            analysis = analyze_portfolio(holdings, args.alert_threshold)
            write_analysis_csv(args.output, analysis)
            write_analysis_report(args.report, holdings, analysis, args.alert_threshold)
            print(f"PASSA: analisi creata in {args.output} e {args.report}")
        else:
            holdings = load_portfolio(args.portfolio)
            target_ids = {item.instrument_id for item in holdings if item.target_pct > 0}
            monthly_returns = load_monthly_returns(args.returns, target_ids)
            rows = run_backtest(holdings, monthly_returns, args.mode)
            write_backtest_csv(args.output, rows)
            write_backtest_report(args.report, rows, args.mode)
            print(f"PASSA: backtest creato in {args.output} e {args.report}")
    except ValidationError as exc:
        print(f"DA RIPARARE: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
