from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QTableWidget, QTableWidgetItem, QLabel, 
                             QProgressBar, QGroupBox, QHeaderView, QComboBox,
                             QCheckBox, QSpinBox, QFormLayout, QLineEdit, 
                             QRadioButton, QButtonGroup, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer
import asyncio

class DiscoveryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scanning = False
        
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Panel superior: configuración de descubrimiento
        config_group = QGroupBox("Configuración de Descubrimiento Rápido")
        config_layout = QVBoxLayout()
        config_group.setLayout(config_layout)
        
        # Objetivo del escaneo
        target_layout = QFormLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Ej: 192.168.1.0/24")
        target_layout.addRow("Objetivo:", self.target_input)
        config_layout.addLayout(target_layout)
        
        # Métodos de descubrimiento
        methods_group = QGroupBox("Métodos de Descubrimiento")
        methods_layout = QGridLayout()
        
        # Crear opciones de métodos
        self.arp_check = QCheckBox("ARP Ping (solo LAN)")
        self.arp_check.setChecked(True)
        self.icmp_check = QCheckBox("ICMP Echo (ping)")
        self.tcp_check = QCheckBox("TCP SYN (puerto 80)")
        self.udp_check = QCheckBox("UDP (puerto 53)")
        self.mdns_check = QCheckBox("mDNS Discovery")
        self.llmnr_check = QCheckBox("LLMNR Discovery")
        
        # Organizar en grid
        methods_layout.addWidget(self.arp_check, 0, 0)
        methods_layout.addWidget(self.icmp_check, 0, 1)
        methods_layout.addWidget(self.tcp_check, 1, 0)
        methods_layout.addWidget(self.udp_check, 1, 1)
        methods_layout.addWidget(self.mdns_check, 2, 0)
        methods_layout.addWidget(self.llmnr_check, 2, 1)
        
        methods_group.setLayout(methods_layout)
        config_layout.addWidget(methods_group)
        
        # Opciones avanzadas
        advanced_layout = QFormLayout()
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 30)
        self.timeout_spin.setValue(5)
        self.timeout_spin.setSuffix(" s")
        advanced_layout.addRow("Timeout:", self.timeout_spin)
        
        self.retries_spin = QSpinBox()
        self.retries_spin.setRange(0, 5)
        self.retries_spin.setValue(2)
        advanced_layout.addRow("Reintentos:", self.retries_spin)
        
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 100)
        self.threads_spin.setValue(10)
        advanced_layout.addRow("Hilos:", self.threads_spin)
        
        config_layout.addLayout(advanced_layout)
        
        main_layout.addWidget(config_group)
        
        # Botón de escaneo
        scan_button_layout = QHBoxLayout()
        self.scan_button = QPushButton("Iniciar Descubrimiento")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setMinimumHeight(40)
        scan_button_layout.addWidget(self.scan_button)
        main_layout.addLayout(scan_button_layout)
        
        # Tabla de resultados
        results_group = QGroupBox("Dispositivos Descubiertos")
        results_layout = QVBoxLayout()
        
        self.results_table = QTableWidget(0, 4)
        self.results_table.setHorizontalHeaderLabels(["IP", "MAC", "Hostname", "Método"])
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        results_layout.addWidget(self.results_table)
        
        # Acciones para los resultados
        actions_layout = QHBoxLayout()
        
        self.export_button = QPushButton("Exportar Resultados")
        self.export_button.setEnabled(False)
        
        self.nmap_scan_button = QPushButton("Escanear con Nmap")
        self.nmap_scan_button.setEnabled(False)
        self.nmap_scan_button.clicked.connect(self.scan_with_nmap)
        
        actions_layout.addWidget(self.export_button)
        actions_layout.addWidget(self.nmap_scan_button)
        
        results_layout.addLayout(actions_layout)
        results_group.setLayout(results_layout)
        
        main_layout.addWidget(results_group)
        
        # Barra de estado
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Listo")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(status_layout)
    
    @pyqtSlot()
    def start_scan(self):
        """Inicia el proceso de descubrimiento rápido"""
        if self.scanning:
            return
            
        target = self.target_input.text().strip()
        if not target:
            self.status_label.setText("Error: Especifique un objetivo para el descubrimiento")
            return
        
        # Verificar que al menos un método esté seleccionado
        if not any([
            self.arp_check.isChecked(),
            self.icmp_check.isChecked(),
            self.tcp_check.isChecked(),
            self.udp_check.isChecked(),
            self.mdns_check.isChecked(),
            self.llmnr_check.isChecked()
        ]):
            self.status_label.setText("Error: Seleccione al menos un método de descubrimiento")
            return
            
        self.scanning = True
        self.scan_button.setEnabled(False)
        self.status_label.setText(f"Descubriendo dispositivos en {target}...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        
        # Limpiar resultados anteriores
        self.results_table.setRowCount(0)
        self.export_button.setEnabled(False)
        self.nmap_scan_button.setEnabled(False)
        
        # Simular escaneo (esto se reemplazará con el adaptador real)
        QTimer.singleShot(2000, self.on_scan_complete)
    
    def on_scan_complete(self):
        """Callback cuando el descubrimiento se completa"""
        self.scanning = False
        self.scan_button.setEnabled(True)
        self.status_label.setText("Descubrimiento completado")
        self.progress_bar.setVisible(False)
        
        # Simular resultados (esto se reemplazará con datos reales)
        self.populate_sample_data()
        
        # Habilitar botones de acción si hay resultados
        if self.results_table.rowCount() > 0:
            self.export_button.setEnabled(True)
            self.nmap_scan_button.setEnabled(True)
    
    def populate_sample_data(self):
        """Llena la tabla con datos de ejemplo"""
        # Datos de ejemplo
        sample_devices = [
            {"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF", "hostname": "router.local", "method": "ARP"},
            {"ip": "192.168.1.100", "mac": "11:22:33:44:55:66", "hostname": "desktop.local", "method": "ARP, ICMP"},
            {"ip": "192.168.1.101", "mac": "AA:BB:CC:00:11:22", "hostname": "laptop.local", "method": "mDNS"},
            {"ip": "192.168.1.102", "mac": "AA:BB:CC:00:22:33", "hostname": "", "method": "TCP SYN"},
            {"ip": "192.168.1.200", "mac": "00:11:22:33:44:55", "hostname": "printer.local", "method": "LLMNR"}
        ]
        
        for device in sample_devices:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            self.results_table.setItem(row, 0, QTableWidgetItem(device["ip"]))
            self.results_table.setItem(row, 1, QTableWidgetItem(device["mac"]))
            self.results_table.setItem(row, 2, QTableWidgetItem(device["hostname"]))
            self.results_table.setItem(row, 3, QTableWidgetItem(device["method"]))
    
    def scan_with_nmap(self):
        """Envía los dispositivos seleccionados a la pestaña de Nmap"""
        # Aquí se implementaría la lógica para pasar los dispositivos seleccionados
        # a la pestaña de Nmap para un escaneo más detallado
        selected_items = self.results_table.selectedItems()
        if not selected_items:
            return
            
        # Obtener las filas seleccionadas (únicas)
        selected_rows = set()
        for item in selected_items:
            selected_rows.add(self.results_table.row(item))
            
        # Obtener las IPs de las filas seleccionadas
        selected_ips = []
        for row in selected_rows:
            ip = self.results_table.item(row, 0).text()
            selected_ips.append(ip)
            
        # Mostrar mensaje de depuración (en producción, esto pasaría los datos a la pestaña Nmap)
        self.status_label.setText(f"Enviando a Nmap: {', '.join(selected_ips)}")
