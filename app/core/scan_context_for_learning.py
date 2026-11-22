"""Resumen del último escaneo para enlazar con lecciones (sin exportar fuera de la UI)."""
from __future__ import annotations

from typing import Any

from app.core.learning_catalog import Lesson
from app.core.scan_history import ScanRecord, list_records


def last_record(kind: str | None = None) -> ScanRecord | None:
    records = list_records()
    if not records:
        return None
    if kind:
        for rec in reversed(records):
            if rec.kind == kind:
                return rec
        return None
    return records[-1]


def _sample_ports(payload: list[dict[str, Any]], limit: int = 8) -> list[str]:
    lines: list[str] = []
    for host in payload[:3]:
        ip = host.get("ip", "?")
        ports = host.get("ports") or []
        for p in ports[:5]:
            port = p.get("port", "?")
            svc = p.get("service") or p.get("state") or ""
            lines.append(f"{ip}:{port} {svc}".strip())
        if len(lines) >= limit:
            break
    return lines[:limit]


def format_practice_context(lesson: Lesson | None) -> str:
    if lesson is None:
        return "Selecciona una lección."
    rec = last_record(lesson.practice_kind)
    if rec is None:
        return (
            f"**Sin escaneos de tipo «{lesson.practice_kind}» en esta sesión.**\n\n"
            f"{lesson.practice_hint}\n\n"
            "Modo demo: `python main.py --demo` si no tienes permisos de red."
        )

    lines = [
        f"**Último escaneo ({rec.kind})** — objetivo: `{rec.target}`",
        f"Resumen: {rec.summary}",
        "",
    ]

    if rec.kind == "discovery" and rec.payload:
        hosts = [h.get("ip", "?") for h in rec.payload[:12]]
        lines.append("Hosts vistos: " + ", ".join(hosts))
        if len(rec.payload) > 12:
            lines.append(f"(+{len(rec.payload) - 12} más)")
    elif rec.kind == "nmap" and rec.payload:
        ports = _sample_ports(rec.payload)
        if ports:
            lines.append("Puertos (muestra):")
            lines.extend(f"- `{p}`" for p in ports)
        else:
            lines.append("Sin puertos en el payload del último Nmap.")
    elif rec.kind == "wifi" and rec.payload:
        nets = [w.get("ssid") or w.get("bssid") or "?" for w in rec.payload[:8]]
        lines.append("Redes Wi‑Fi (muestra): " + ", ".join(str(n) for n in nets))

    lines.extend(["", lesson.practice_hint])
    return "\n".join(lines)