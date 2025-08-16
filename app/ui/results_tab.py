from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QTableWidget, QTableWidgetItem, QLabel, 
                             QProgressBar, QGroupBox, QHeaderView, QComboBox,
                             QCheckBox, QSpinBox, QFormLayout, QLineEdit, 
                             QSplitter, QTreeWidget, QTreeWidgetItem, QTabWidget,
                             QDateEdit, QCalendarWidget, QDialog, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer, QDateTime
import asyncio

class ResultsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Panel superior: filtros y búsqueda
        filters_group = QGroupBox("Filtros y Búsqueda")
        filters_layout = QHBoxLayout()
        filters_group.setLayout(filters_layout)
        
        # Filtro por tipo
        type_layout = QFormLayout()
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems(["Todos", "Wi-Fi", "Nmap", "Descubrimiento Rápido"])
        type_layout.addRow("Tipo:", self.scan_type_combo)
        filters_layout.addLayout(type_layout)
        
        # Filtro por fecha
        date_layout = QFormLayout()
        self.date_from = QDateEdit(QDateTime.currentDateTime().date().addDays(-30))
        self.date_from.setCalendarPopup(True)
        self.date_to = QDateEdit(QDateTime.currentDateTime().date())
        self.date_to.setCalendarPopup(True)
        
        date_layout.addRow("Desde:", self.date_from)
        date_layout.addRow("Hasta:", self.date_to)
        filters_layout.addLayout(date_layout)
        
        # Búsqueda por texto
        search_layout = QFormLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por IP, MAC, hostname...")
        search_layout.addRow("Buscar:", self.search_input)
        
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_results)
        search_layout.addRow(self.search_button)
        
        filters_layout.addLayout(search_layout)
        
        main_layout.addWidget(filters_group)
        
        # Tabla de escaneos
        scans_group = QGroupBox("Historial de Escaneos")
        scans_layout = QVBoxLayout()
        
        self.scans_table = QTableWidget(0, 5)
        self.scans_table.setHorizontalHeaderLabels(["ID", "Tipo", "Fecha", "Objetivo", "Resultados"])
        self.scans_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.scans_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.scans_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.scans_table.itemSelectionChanged.connect(self.on_scan_selected)
        
        scans_layout.addWidget(self.scans_table)
        
        # Acciones para los escaneos
        actions_layout = QHBoxLayout()
        
        self.view_button = QPushButton("Ver Detalles")
        self.view_button.setEnabled(False)
        self.view_button.clicked.connect(self.view_scan_details)
        
        self.export_button = QPushButton("Exportar")
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_scan)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_scan)
        
        self.compare_button = QPushButton("Comparar")
        self.compare_button.setEnabled(False)
        self.compare_button.clicked.connect(self.compare_scans)
        
        actions_layout.addWidget(self.view_button)
        actions_layout.addWidget(self.export_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addWidget(self.compare_button)
        
        scans_layout.addLayout(actions_layout)
        scans_group.setLayout(scans_layout)
        
        main_layout.addWidget(scans_group)
        
        # Panel de vista previa
        preview_group = QGroupBox("Vista Previa")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # Cargar datos de ejemplo
        self.populate_sample_data()
    
    def populate_sample_data(self):
        """Llena la tabla con datos de ejemplo"""
        # Datos de ejemplo
        sample_scans = [
            {"id": "001", "type": "Wi-Fi", "date": "2023-08-15 10:30", "target": "wlan0", "results": "3 redes encontradas"},
            {"id": "002", "type": "Nmap", "date": "2023-08-15 10:45", "target": "192.168.1.0/24", "results": "5 hosts, 12 puertos abiertos"},
            {"id": "003", "type": "Descubrimiento", "date": "2023-08-15 11:00", "target": "192.168.1.0/24", "results": "4 dispositivos"},
            {"id": "004", "type": "Wi-Fi", "date": "2023-08-16 09:15", "target": "wlan0", "results": "5 redes encontradas"},
            {"id": "005", "type": "Nmap", "date": "2023-08-16 14:20", "target": "10.0.0.0/24", "results": "2 hosts, 3 puertos abiertos"}
        ]
        
        for scan in sample_scans:
            row = self.scans_table.rowCount()
            self.scans_table.insertRow(row)
            
            self.scans_table.setItem(row, 0, QTableWidgetItem(scan["id"]))
            self.scans_table.setItem(row, 1, QTableWidgetItem(scan["type"]))
            self.scans_table.setItem(row, 2, QTableWidgetItem(scan["date"]))
            self.scans_table.setItem(row, 3, QTableWidgetItem(scan["target"]))
            self.scans_table.setItem(row, 4, QTableWidgetItem(scan["results"]))
    
    @pyqtSlot()
    def search_results(self):
        """Busca en los resultados según los filtros"""
        search_text = self.search_input.text().lower()
        scan_type = self.scan_type_combo.currentText()
        
        # Aquí iría la lógica real de búsqueda en la base de datos
        # Por ahora, solo simulamos un filtrado básico en los datos de ejemplo
        
        for row in range(self.scans_table.rowCount()):
            hide_row = False
            
            # Filtrar por tipo
            if scan_type != "Todos" and self.scans_table.item(row, 1).text() != scan_type:
                hide_row = True
                
            # Filtrar por texto
            if search_text and not any(
                search_text in self.scans_table.item(row, col).text().lower() 
                for col in range(self.scans_table.columnCount())
            ):
                hide_row = True
                
            self.scans_table.setRowHidden(row, hide_row)
    
    def on_scan_selected(self):
        """Maneja la selección de un escaneo en la tabla"""
        selected_items = self.scans_table.selectedItems()
        has_selection = len(selected_items) > 0
        
        self.view_button.setEnabled(has_selection)
        self.export_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        
        # Habilitar botón de comparar solo si hay exactamente 2 filas seleccionadas
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(self.scans_table.row(item))
        self.compare_button.setEnabled(len(selected_rows) == 2)
        
        # Mostrar vista previa del primer escaneo seleccionado
        if has_selection:
            row = self.scans_table.row(selected_items[0])
            scan_id = self.scans_table.item(row, 0).text()
            scan_type = self.scans_table.item(row, 1).text()
            scan_date = self.scans_table.item(row, 2).text()
            scan_target = self.scans_table.item(row, 3).text()
            
            # Generar vista previa según el tipo de escaneo
            if scan_type == "Wi-Fi":
                preview = f"""ID de Escaneo: {scan_id}
Tipo: {scan_type}
Fecha: {scan_date}
Interfaz: {scan_target}

Redes Encontradas:
- Red-Hogar (AA:BB:CC:DD:EE:FF) - Canal 1 - Señal: -45 dBm - WPA2
- Oficina-5G (11:22:33:44:55:66) - Canal 36 - Señal: -60 dBm - WPA2-Enterprise
- Invitados (AA:BB:CC:00:11:22) - Canal 11 - Señal: -72 dBm - Abierta
"""
            elif scan_type == "Nmap":
                preview = f"""ID de Escaneo: {scan_id}
Tipo: {scan_type}
Fecha: {scan_date}
Objetivo: {scan_target}

Hosts Encontrados:
- 192.168.1.1 (router.local) - 3 puertos abiertos
  * 22/tcp - ssh
  * 80/tcp - http
  * 443/tcp - https
- 192.168.1.100 (desktop.local) - 3 puertos abiertos
  * 135/tcp - msrpc
  * 445/tcp - microsoft-ds
  * 3389/tcp - ms-wbt-server
"""
            else:  # Descubrimiento
                preview = f"""ID de Escaneo: {scan_id}
Tipo: {scan_type}
Fecha: {scan_date}
Objetivo: {scan_target}

Dispositivos Encontrados:
- 192.168.1.1 (AA:BB:CC:DD:EE:FF) - router.local - ARP
- 192.168.1.100 (11:22:33:44:55:66) - desktop.local - ARP, ICMP
- 192.168.1.101 (AA:BB:CC:00:11:22) - laptop.local - mDNS
- 192.168.1.102 (AA:BB:CC:00:22:33) - [sin nombre] - TCP SYN
"""
            
            self.preview_text.setText(preview)
        else:
            self.preview_text.clear()
    
    def view_scan_details(self):
        """Muestra los detalles completos de un escaneo"""
        selected_items = self.scans_table.selectedItems()
        if not selected_items:
            return
            
        row = self.scans_table.row(selected_items[0])
        scan_id = self.scans_table.item(row, 0).text()
        scan_type = self.scans_table.item(row, 1).text()
        
        # Aquí se implementaría la lógica para mostrar los detalles completos
        # Por ahora, solo mostramos un mensaje en la vista previa
        self.preview_text.append("\n[Mostrando detalles completos del escaneo...]")
    
    def export_scan(self):
        """Exporta los resultados del escaneo"""
        selected_items = self.scans_table.selectedItems()
        if not selected_items:
            return
            
        row = self.scans_table.row(selected_items[0])
        scan_id = self.scans_table.item(row, 0).text()
        
        # Simular diálogo de exportación
        self.preview_text.append("\n[Exportando resultados del escaneo...]")
        
        # Aquí se implementaría un QFileDialog.getSaveFileName() y la lógica de exportación
    
    def delete_scan(self):
        """Elimina un escaneo del historial"""
        selected_items = self.scans_table.selectedItems()
        if not selected_items:
            return
            
        # Obtener filas únicas seleccionadas
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(self.scans_table.row(item))
            
        # Eliminar filas en orden inverso para evitar problemas de índices
        for row in sorted(selected_rows, reverse=True):
            self.scans_table.removeRow(row)
            
        # Limpiar vista previa si no quedan selecciones
        if not self.scans_table.selectedItems():
            self.preview_text.clear()
    
    def compare_scans(self):
        """Compara dos escaneos seleccionados"""
        selected_items = self.scans_table.selectedItems()
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(self.scans_table.row(item))
            
        if len(selected_rows) != 2:
            return
            
        # Obtener IDs de los escaneos
        rows = sorted(selected_rows)
        scan_id1 = self.scans_table.item(rows[0], 0).text()
        scan_id2 = self.scans_table.item(rows[1], 0).text()
        
        # Mostrar comparación simulada
        self.preview_text.setText(f"""Comparando escaneos {scan_id1} y {scan_id2}:

Nuevos dispositivos en {scan_id2}:
- 192.168.1.105 (00:11:22:33:44:66) - nuevo-dispositivo.local

Dispositivos que ya no están presentes en {scan_id2}:
- 192.168.1.102 (AA:BB:CC:00:22:33)

Cambios en puertos:
- 192.168.1.1: Nuevo puerto abierto 22/tcp (ssh)
- 192.168.1.100: Puerto cerrado 3389/tcp (ms-wbt-server)

Cambios en redes Wi-Fi:
- Nueva red "Visitantes" (Canal 6)
- "Red-Hogar" cambió de canal 1 a canal 3
""")
