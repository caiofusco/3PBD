from __future__ import annotations

import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any


class CsvValidationError(ValueError):
    pass


def read_csv_bytes(content: bytes) -> list[dict[str, str | None]]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise CsvValidationError("CSV sem cabecalho.")

    rows: list[dict[str, str | None]] = []
    for line_number, raw_row in enumerate(reader, start=2):
        row: dict[str, str | None] = {}
        for key, value in raw_row.items():
            if key is None:
                continue
            normalized_key = key.strip().lower()
            normalized_value = value.strip() if isinstance(value, str) else value
            row[normalized_key] = normalized_value or None
        row["__line_number"] = str(line_number)
        rows.append(row)
    return rows


def required(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if value in (None, ""):
        line = row.get("__line_number", "?")
        raise CsvValidationError(f"Campo obrigatorio ausente: {key}. Linha: {line}.")
    return str(value)


def optional(row: dict[str, Any], key: str) -> str | None:
    value = row.get(key)
    if value in (None, ""):
        return None
    return str(value)


def parse_int(value: str | None, field_name: str) -> int:
    if value in (None, ""):
        raise CsvValidationError(f"Campo numerico obrigatorio ausente: {field_name}.")
    try:
        return int(str(value))
    except ValueError as exc:
        raise CsvValidationError(f"Valor inteiro invalido em {field_name}: {value!r}.") from exc


def parse_decimal(value: str | None, field_name: str) -> Decimal:
    if value in (None, ""):
        raise CsvValidationError(f"Campo decimal obrigatorio ausente: {field_name}.")
    normalized = str(value).replace(".", "").replace(",", ".") if "," in str(value) else str(value)
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise CsvValidationError(f"Valor decimal invalido em {field_name}: {value!r}.") from exc


def parse_datetime(value: str | None, field_name: str) -> datetime | None:
    if value in (None, ""):
        return None
    normalized = str(value).replace("Z", "").strip()
    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue
    raise CsvValidationError(f"Data invalida em {field_name}: {value!r}.")
