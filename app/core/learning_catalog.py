"""Catálogo de lecciones en docs/learn/ (Fase 2 — ADR Tooling-002)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Lesson:
    title: str
    rel_path: str
    practice_kind: str
    practice_hint: str


LESSONS: tuple[Lesson, ...] = (
    Lesson(
        title="TCP/IP y modelo OSI",
        rel_path="01-fundamentos-redes/tcp-ip-modelo-osi.md",
        practice_kind="discovery",
        practice_hint="Pestaña Descubrimiento — observa qué hosts responden en tu rango.",
    ),
    Lesson(
        title="Puertos y servicios",
        rel_path="01-fundamentos-redes/puertos-servicios.md",
        practice_kind="nmap",
        practice_hint="Pestaña Escaneo de Red — compara puertos abiertos con la tabla del apunte.",
    ),
    Lesson(
        title="Reconocimiento pasivo",
        rel_path="03-reconocimiento/reconocimiento-pasivo.md",
        practice_kind="discovery",
        practice_hint="Inventario Conocido/Desconocido tras un descubrimiento.",
    ),
    Lesson(
        title="Escaneo de puertos",
        rel_path="04-escaneo-redes/escaneo-puertos.md",
        practice_kind="nmap",
        practice_hint="Ejecuta un escaneo y revisa el historial en Resultados.",
    ),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def learn_dir() -> Path:
    return repo_root() / "docs" / "learn"


def list_lessons() -> list[Lesson]:
    base = learn_dir()
    out: list[Lesson] = []
    for lesson in LESSONS:
        if (base / lesson.rel_path).is_file():
            out.append(lesson)
    return out


def load_lesson_text(rel_path: str) -> str:
    path = learn_dir() / rel_path
    if not path.is_file():
        return f"*No se encontró la lección:* `{rel_path}`"
    return path.read_text(encoding="utf-8", errors="replace")