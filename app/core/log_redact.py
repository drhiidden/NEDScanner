"""Reducción de detalle en logs (sin PII ni volcados largos)."""

from __future__ import annotations


def redact_for_log(value: str, *, max_len: int = 64) -> str:
    """Recorta y normaliza texto de log; evita newlines y cadenas enormes."""
    v = (value or "").strip().replace("\n", " ").replace("\r", " ")
    if len(v) <= max_len:
        return v
    return f"{v[: max_len - 3]}..."


def redact_subprocess_stderr(raw: bytes, *, max_len: int = 120) -> str:
    """Resumen de stderr de herramientas externas (nmcli, nmap)."""
    if not raw:
        return "(vacío)"
    text = raw.decode(errors="replace").strip()
    return redact_for_log(text, max_len=max_len)
