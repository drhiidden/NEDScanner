"""Ayuda contextual por pestaña (texto estático, sin LLM)."""
from __future__ import annotations

from PyQt6.QtWidgets import QMessageBox, QWidget

HELP_BY_TAB: dict[str, tuple[str, str]] = {
    "wifi": (
        "Wi‑Fi",
        "Lista redes visibles con NetworkManager. Útil para inventario doméstico.\n\n"
        "• Modo demo: datos ficticios sin nmcli real.\n"
        "• Tras el escaneo, revisa Aprendizaje con tu última sesión.",
    ),
    "nmap": (
        "Escaneo de red",
        "Escaneo de puertos/servicios con Nmap. Define un objetivo (IP, rango o host) "
        "solo en redes autorizadas.\n\n"
        "Si aparece bloqueo, confirma autorización en Configuración → Seguridad "
        "o usa `python main.py --demo`.",
    ),
    "discovery": (
        "Descubrimiento rápido",
        "Combina ARP, ICMP, mDNS y LLMNR para ver hosts activos sin un Nmap completo.\n\n"
        "Hosts no presentes en tu inventario de confianza se marcan como desconocidos.",
    ),
    "results": (
        "Resultados",
        "Historial de la sesión actual (no persiste al cerrar la app). "
        "Exporta desde aquí si necesitas conservar un informe.",
    ),
    "learning": (
        "Aprendizaje",
        "Lee una lección y compárala con el panel «Tu último escaneo». "
        "Pulsa «Ir a la práctica» para saltar a la pestaña indicada.",
    ),
    "settings": (
        "Configuración",
        "Seguridad: autorización de escaneo real. Herramientas: timeout de Nmap. "
        "Inventario: dispositivos que declaras conocidos.",
    ),
}

_TAB_KEYS = (
    ("wifi", "Wi‑Fi"),
    ("nmap", "Escaneo de Red"),
    ("discovery", "Descubrimiento Rápido"),
    ("results", "Resultados"),
    ("learning", "Aprendizaje"),
    ("settings", "Configuración"),
)


def tab_key_from_index(index: int) -> str | None:
    if 0 <= index < len(_TAB_KEYS):
        return _TAB_KEYS[index][0]
    return None


def show_tab_help(parent: QWidget | None, tab_key: str) -> None:
    title, body = HELP_BY_TAB.get(
        tab_key,
        ("Ayuda", "Selecciona una pestaña para ver consejos contextuales."),
    )
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Information)
    box.setWindowTitle(f"Ayuda — {title}")
    box.setText(title)
    box.setInformativeText(body)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    box.exec()