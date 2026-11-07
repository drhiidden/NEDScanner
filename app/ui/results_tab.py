from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QDate, Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.known_inventory import is_host_known, unknown_hosts_from_payload
from app.core.safe_io import safe_export_path
from app.core.scan_history import ScanRecord, delete_record, get_record, list_records

_KIND_LABEL = {
    "wifi": "Wi-Fi",
    "nmap": "Nmap",
    "discovery": "Descubrimiento",
}


class ResultsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._rows: dict[int, int] = {}  # table row -> record id
        self.init_ui()
        self.reload_from_history()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        alerts_group = QGroupBox("Dispositivos desconocidos (último descubrimiento)")
        alerts_layout = QVBoxLayout()
        self.alerts_label = QLabel("Sin descubrimientos en esta sesión.")
        self.alerts_label.setWordWrap(True)
        alerts_layout.addWidget(self.alerts_label)
        alerts_group.setLayout(alerts_layout)
        main_layout.addWidget(alerts_group)

        filters_group = QGroupBox("Filtros y Búsqueda")
        filters_layout = QHBoxLayout()
        filters_group.setLayout(filters_layout)

        type_layout = QFormLayout()
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems(["Todos", "Wi-Fi", "Nmap", "Descubrimiento"])
        type_layout.addRow("Tipo:", self.scan_type_combo)
        filters_layout.addLayout(type_layout)

        date_layout = QFormLayout()
        self.date_from = QDateEdit(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        date_layout.addRow("Desde:", self.date_from)
        date_layout.addRow("Hasta:", self.date_to)
        filters_layout.addLayout(date_layout)

        search_layout = QFormLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por IP, MAC, hostname...")
        search_layout.addRow("Buscar:", self.search_input)
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_results)
        search_layout.addRow(self.search_button)
        filters_layout.addLayout(search_layout)

        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.reload_from_history)
        filters_layout.addWidget(self.refresh_button)

        main_layout.addWidget(filters_group)

        scans_group = QGroupBox("Historial de escaneos (sesión actual)")
        scans_layout = QVBoxLayout()

        self.scans_table = QTableWidget(0, 5)
        self.scans_table.setHorizontalHeaderLabels(["ID", "Tipo", "Fecha", "Objetivo", "Resultados"])
        self.scans_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.scans_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.scans_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.scans_table.itemSelectionChanged.connect(self.on_scan_selected)
        scans_layout.addWidget(self.scans_table)

        actions_layout = QHBoxLayout()
        self.export_button = QPushButton("Exportar JSON")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_scan)
        self.delete_button = QPushButton("Quitar del historial")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_scan)
        self.compare_button = QPushButton("Comparar (2 descubrimientos)")
        self.compare_button.setEnabled(False)
        self.compare_button.clicked.connect(self.compare_scans)
        actions_layout.addWidget(self.export_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addWidget(self.compare_button)
        scans_layout.addLayout(actions_layout)
        scans_group.setLayout(scans_layout)
        main_layout.addWidget(scans_group)

        preview_group = QGroupBox("Vista previa")
        preview_layout = QVBoxLayout()
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)

    def reload_from_history(self) -> None:
        self.scans_table.setRowCount(0)
        self._rows.clear()
        for rec in list_records():
            row = self.scans_table.rowCount()
            self.scans_table.insertRow(row)
            label = _KIND_LABEL.get(rec.kind, rec.kind)
            when = rec.at.astimezone().strftime("%Y-%m-%d %H:%M")
            rid = f"{rec.id:03d}"
            self.scans_table.setItem(row, 0, QTableWidgetItem(rid))
            self.scans_table.setItem(row, 1, QTableWidgetItem(label))
            self.scans_table.setItem(row, 2, QTableWidgetItem(when))
            self.scans_table.setItem(row, 3, QTableWidgetItem(rec.target))
            self.scans_table.setItem(row, 4, QTableWidgetItem(rec.summary))
            self.scans_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, rec.id)
            self._rows[row] = rec.id
        self._update_alerts()
        self.preview_text.clear()
        self.on_scan_selected()

    def _update_alerts(self) -> None:
        latest: ScanRecord | None = None
        for rec in reversed(list_records()):
            if rec.kind == "discovery":
                latest = rec
                break
        if not latest:
            self.alerts_label.setText(
                "Sin descubrimientos en esta sesión. "
                "Inventario conocido: ~/.nedscaner/known-devices.json"
            )
            return
        unknowns = unknown_hosts_from_payload(latest.payload)
        if not unknowns:
            self.alerts_label.setText(
                f"Último descubrimiento ({latest.target}): todos los hosts coinciden con el inventario conocido."
            )
            return
        lines = [f"⚠ {len(unknowns)} dispositivo(s) no están en tu inventario:"]
        for u in unknowns[:12]:
            lines.append(
                f"  • {u.get('ip', '?')}  MAC {u.get('mac', '—')}  "
                f"{u.get('hostname') or '(sin nombre)'}"
            )
        if len(unknowns) > 12:
            lines.append(f"  … y {len(unknowns) - 12} más")
        lines.append("Marca como conocidos en Descubrimiento o en Configuración → Inventario.")
        self.alerts_label.setText("\n".join(lines))

    def _selected_record_id(self) -> int | None:
        items = self.scans_table.selectedItems()
        if not items:
            return None
        row = self.scans_table.row(items[0])
        item = self.scans_table.item(row, 0)
        if not item:
            return None
        rid = item.data(Qt.ItemDataRole.UserRole)
        return int(rid) if rid is not None else None

    @pyqtSlot()
    def search_results(self):
        search_text = self.search_input.text().lower()
        scan_type = self.scan_type_combo.currentText()
        d0 = self.date_from.date()
        d1 = self.date_to.date()

        for row in range(self.scans_table.rowCount()):
            hide = False
            tipo = self.scans_table.item(row, 1).text()
            if scan_type != "Todos" and tipo != scan_type:
                hide = True
            fecha_txt = self.scans_table.item(row, 2).text()
            try:
                when = datetime.strptime(fecha_txt, "%Y-%m-%d %H:%M").date()
                if when < d0.toPyDate() or when > d1.toPyDate():
                    hide = True
            except ValueError:
                pass
            if search_text and not any(
                search_text in self.scans_table.item(row, col).text().lower()
                for col in range(self.scans_table.columnCount())
            ):
                hide = True
            self.scans_table.setRowHidden(row, hide)

    def on_scan_selected(self):
        has = self._selected_record_id() is not None
        self.export_button.setEnabled(has)
        self.delete_button.setEnabled(has)

        selected_rows = {self.scans_table.row(i) for i in self.scans_table.selectedItems()}
        can_compare = False
        if len(selected_rows) == 2:
            kinds = {self.scans_table.item(r, 1).text() for r in selected_rows}
            can_compare = kinds == {"Descubrimiento"}
        self.compare_button.setEnabled(can_compare)

        rid = self._selected_record_id()
        if rid is None:
            self.preview_text.clear()
            return
        rec = get_record(rid)
        if rec:
            self.preview_text.setText(self._format_preview(rec))

    def _format_preview(self, rec: ScanRecord) -> str:
        header = (
            f"ID: {rec.id:03d}\n"
            f"Tipo: {_KIND_LABEL.get(rec.kind, rec.kind)}\n"
            f"Fecha: {rec.at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"Objetivo: {rec.target}\n"
            f"Resumen: {rec.summary}\n\n"
        )
        if rec.kind == "discovery":
            body = "Hosts:\n"
            for h in rec.payload:
                trust = (
                    "conocido"
                    if is_host_known(h.get("ip"), h.get("mac"), h.get("hostname"))
                    else "desconocido"
                )
                body += (
                    f"- {h.get('ip')} ({h.get('mac', '—')}) "
                    f"{h.get('hostname') or ''} [{trust}]\n"
                )
            return header + body
        if rec.kind == "wifi":
            body = "Redes:\n"
            for w in rec.payload:
                body += (
                    f"- {w.get('ssid')} {w.get('bssid')} "
                    f"ch {w.get('channel')} {w.get('signal_dbm')} dBm {w.get('security')}\n"
                )
            return header + body
        if rec.kind == "nmap":
            body = "Hosts:\n"
            for h in rec.payload:
                body += f"- {h.get('ip')} ({h.get('hostname') or '—'}) "
                ports = h.get("ports") or []
                open_ports = [p for p in ports if p.get("state") == "open"]
                body += f"{len(open_ports)} puertos abiertos\n"
            return header + body
        return header + json.dumps(rec.payload, indent=2, ensure_ascii=False)

    def export_scan(self):
        rid = self._selected_record_id()
        if rid is None:
            return
        rec = get_record(rid)
        if not rec:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar escaneo",
            str(Path.home() / f"nedscanner-scan-{rid:03d}.json"),
            "JSON (*.json)",
        )
        if not path:
            return
        try:
            dest = safe_export_path(path)
        except ValueError as exc:
            self.preview_text.append(f"\nExportación rechazada: {exc}")
            return
        blob = {
            "id": rec.id,
            "kind": rec.kind,
            "target": rec.target,
            "summary": rec.summary,
            "at": rec.at.isoformat(),
            "payload": rec.payload,
        }
        dest.write_text(json.dumps(blob, indent=2, ensure_ascii=False), encoding="utf-8")
        self.preview_text.append(f"\nExportado: {dest}")

    def delete_scan(self):
        rid = self._selected_record_id()
        if rid is None:
            return
        if delete_record(rid):
            self.reload_from_history()

    def compare_scans(self):
        selected_rows = sorted({self.scans_table.row(i) for i in self.scans_table.selectedItems()})
        if len(selected_rows) != 2:
            return
        id1 = int(self.scans_table.item(selected_rows[0], 0).data(Qt.ItemDataRole.UserRole))
        id2 = int(self.scans_table.item(selected_rows[1], 0).data(Qt.ItemDataRole.UserRole))
        r1, r2 = get_record(id1), get_record(id2)
        if not r1 or not r2 or r1.kind != "discovery" or r2.kind != "discovery":
            return

        def ips(rec: ScanRecord) -> set[str]:
            return {str(h.get("ip")) for h in rec.payload if h.get("ip")}

        def by_ip(rec: ScanRecord) -> dict[str, dict]:
            return {str(h.get("ip")): h for h in rec.payload if h.get("ip")}

        older, newer = (r1, r2) if r1.at <= r2.at else (r2, r1)
        i_old, i_new = ips(older), ips(newer)
        new_ips = i_new - i_old
        gone = i_old - i_new
        b_old, b_new = by_ip(older), by_ip(newer)

        lines = [f"Comparando descubrimiento #{older.id} → #{newer.id}", ""]
        if new_ips:
            lines.append("Nuevos (no estaban en el anterior):")
            for ip in sorted(new_ips):
                h = b_new[ip]
                unk = (
                    " ⚠ DESCONOCIDO"
                    if not is_host_known(h.get("ip"), h.get("mac"), h.get("hostname"))
                    else ""
                )
                lines.append(f"  + {ip} {h.get('mac', '—')}{unk}")
        else:
            lines.append("Sin IPs nuevas.")
        if gone:
            lines.append("\nYa no aparecen:")
            for ip in sorted(gone):
                lines.append(f"  - {ip}")
        mac_changes = []
        for ip in i_old & i_new:
            m1 = (b_old[ip].get("mac") or "").lower()
            m2 = (b_new[ip].get("mac") or "").lower()
            if m1 and m2 and m1 != m2:
                mac_changes.append(f"  ! {ip}: MAC {m1} → {m2}")
        if mac_changes:
            lines.append("\nCambio de MAC (posible suplantación o DHCP):")
            lines.extend(mac_changes)
        self.preview_text.setText("\n".join(lines))
