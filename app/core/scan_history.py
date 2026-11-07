"""Historial en memoria de la sesión (sin persistencia en disco)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ScanRecord:
    kind: str
    target: str
    summary: str
    payload: list[dict[str, Any]] = field(default_factory=list)
    at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


_HISTORY: list[ScanRecord] = []


def append_record(record: ScanRecord) -> None:
    _HISTORY.append(record)


def list_records() -> list[ScanRecord]:
    return list(_HISTORY)
