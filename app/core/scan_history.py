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
    id: int = 0


_HISTORY: list[ScanRecord] = []
_next_id = 1


def append_record(record: ScanRecord) -> int:
    global _next_id
    record.id = _next_id
    _next_id += 1
    _HISTORY.append(record)
    return record.id


def list_records() -> list[ScanRecord]:
    return list(_HISTORY)


def get_record(record_id: int) -> ScanRecord | None:
    for rec in _HISTORY:
        if rec.id == record_id:
            return rec
    return None


def delete_record(record_id: int) -> bool:
    for i, rec in enumerate(_HISTORY):
        if rec.id == record_id:
            del _HISTORY[i]
            return True
    return False


def clear_history() -> None:
    _HISTORY.clear()
