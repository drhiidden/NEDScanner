"""Estilos UI compartidos (inventario de confianza)."""
from __future__ import annotations

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidget

UNKNOWN_ROW = QColor(255, 140, 60)


def highlight_row_if_unknown(table: QTableWidget, row: int, *, unknown: bool, columns: int) -> None:
    if not unknown:
        return
    for col in range(columns):
        item = table.item(row, col)
        if item:
            item.setBackground(UNKNOWN_ROW)
