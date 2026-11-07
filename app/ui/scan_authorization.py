"""Diálogo de autorización de escaneo (human-in-the-loop)."""
from __future__ import annotations

from PyQt6.QtWidgets import QMessageBox, QWidget

from app.core.config import is_demo_mode
from app.core.user_prefs import is_scan_authorized, set_scan_authorized

_ACK_TEXT = (
    "Confirma que solo escanearás redes donde tengas permiso escrito "
    "(propias, laboratorio autorizado o contrato explícito).\n\n"
    "El escaneo no autorizado puede ser ilegal. Ver DISCLAIMER en el repositorio."
)


def ensure_scan_authorized(parent: QWidget | None) -> bool:
    if is_demo_mode() or is_scan_authorized():
        return True
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle("Autorización de escaneo")
    box.setText("Escaneo en red real")
    box.setInformativeText(_ACK_TEXT)
    box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    box.setDefaultButton(QMessageBox.StandardButton.No)
    if box.exec() != QMessageBox.StandardButton.Yes:
        return False
    set_scan_authorized(True)
    window = parent.window() if parent else None
    if window is not None and hasattr(window, "refresh_security_status"):
        window.refresh_security_status()  # type: ignore[attr-defined]
    return True
