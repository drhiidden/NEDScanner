from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QTableWidget, QTableWidgetItem, QLabel, 
                             QProgressBar, QGroupBox, QHeaderView, QComboBox,
                             QCheckBox, QSpinBox, QFormLayout, QLineEdit, 
                             QSplitter, QTreeWidget, QTreeWidgetItem)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer
import asyncio

class NmapTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scanning = False
        
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Panel superior: configuración de escaneo
        scan_config = QGroupBox("Configuración de Escaneo")
        config_layout = QFormLayout()
        scan_config.setLayout(config_layout)
        
        # Objetivo del escaneo
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Ej: 192.168.1.0/24, example.com, 10.0.0.1-10")
        config_layout.addRow("Objetivo:", self.target_input)
        
        # Tipo de escaneo
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems([
            "Ping (descubrimiento rápido)",
            "Puertos comunes (top 100)",
            "Escaneo completo (1-1000)",
            "Todos los puertos (1-65535)",
            "Personalizado"
        ])
        config_layout.addRow("Tipo de escaneo:", self.scan_type_combo)
        
        # Opciones adicionales
        options_layout = QHBoxLayout()
        
        self.service_version_check = QCheckBox("Detectar versiones")
        self.os_detection_check = QCheckBox("Detectar sistema operativo")
        self.aggressive_scan_check = QCheckBox("Escaneo agresivo (más rápido)")
        
        options_layout.addWidget(self.service_version_check)
        options_layout.addWidget(self.os_detection_check)
        options_layout.addWidget(self.aggressive_scan_check)
        
        config_layout.addRow("Opciones:", options_layout)
        
        # Opciones avanzadas
        self.nmap_args = QLineEdit()
        self.nmap_args.setPlaceholderText("Argumentos adicionales para Nmap")
        config_layout.addRow("Argumentos:", self.nmap_args)
        
        main_layout.addWidget(scan_config)
        
        # Botón de escaneo
        scan_button_layout = QHBoxLayout()
        self.scan_button = QPushButton("Iniciar Escaneo")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setMinimumHeight(40)
        scan_button_layout.addWidget(self.scan_button)
        main_layout.addLayout(scan_button_layout)
        
        # Splitter para resultados
        results_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo: árbol de hosts
        self.hosts_tree = QTreeWidget()
        self.hosts_tree.setHeaderLabels(["Hosts", "Estado"])
        self.hosts_tree.setColumnWidth(0, 250)
        self.hosts_tree.itemSelectionChanged.connect(self.on_host_selected)
        results_splitter.addWidget(self.hosts_tree)
        
        # Panel derecho: detalles del host
        details_widget = QWidget()
        details_layout = QVBoxLayout()
        details_widget.setLayout(details_layout)
        
        # Tabla de puertos
        ports_group = QGroupBox("Puertos")
        ports_layout = QVBoxLayout()
        self.ports_table = QTableWidget(0, 4)
        self.ports_table.setHorizontalHeaderLabels(["Puerto", "Protocolo", "Estado", "Servicio"])
        self.ports_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.ports_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        ports_layout.addWidget(self.ports_table)
        ports_group.setLayout(ports_layout)
        details_layout.addWidget(ports_group)
        
        # Información del host
        host_info_group = QGroupBox("Información del Host")
        host_info_layout = QVBoxLayout()
        self.host_info_text = QTextEdit()
        self.host_info_text.setReadOnly(True)
        host_info_layout.addWidget(self.host_info_text)
        host_info_group.setLayout(host_info_layout)
        details_layout.addWidget(host_info_group)
        
        results_splitter.addWidget(details_widget)
        results_splitter.setSizes([200, 400])
        
        main_layout.addWidget(results_splitter)
        
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
        """Inicia el proceso de escaneo Nmap"""
        if self.scanning:
            return
            
        target = self.target_input.text().strip()
        if not target:
            self.status_label.setText("Error: Especifique un objetivo para el escaneo")
            return
            
        self.scanning = True
        self.scan_button.setEnabled(False)
        self.status_label.setText(f"Escaneando {target}...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        
        # Limpiar resultados anteriores
        self.hosts_tree.clear()
        self.ports_table.setRowCount(0)
        self.host_info_text.clear()
        
        # Simular escaneo (esto se reemplazará con el adaptador real)
        QTimer.singleShot(3000, self.on_scan_complete)
    
    def on_scan_complete(self):
        """Callback cuando el escaneo se completa"""
        self.scanning = False
        self.scan_button.setEnabled(True)
        self.status_label.setText("Escaneo completado")
        self.progress_bar.setVisible(False)
        
        # Simular resultados (esto se reemplazará con datos reales)
        self.populate_sample_data()
    
    def populate_sample_data(self):
        """Llena los resultados con datos de ejemplo"""
        # Datos de ejemplo
        sample_hosts = [
            {
                "ip": "192.168.1.1",
                "hostname": "router.local",
                "status": "up",
                "mac": "AA:BB:CC:DD:EE:FF",
                "vendor": "Cisco",
                "os": "Linux 3.x",
                "ports": [
                    {"port": 22, "protocol": "tcp", "state": "open", "service": "ssh"},
                    {"port": 80, "protocol": "tcp", "state": "open", "service": "http"},
                    {"port": 443, "protocol": "tcp", "state": "open", "service": "https"}
                ]
            },
            {
                "ip": "192.168.1.100",
                "hostname": "desktop.local",
                "status": "up",
                "mac": "11:22:33:44:55:66",
                "vendor": "Dell",
                "os": "Windows 10",
                "ports": [
                    {"port": 135, "protocol": "tcp", "state": "open", "service": "msrpc"},
                    {"port": 445, "protocol": "tcp", "state": "open", "service": "microsoft-ds"},
                    {"port": 3389, "protocol": "tcp", "state": "open", "service": "ms-wbt-server"}
                ]
            },
            {
                "ip": "192.168.1.101",
                "hostname": "",
                "status": "up",
                "mac": "AA:BB:CC:00:11:22",
                "vendor": "Apple",
                "os": "macOS 11",
                "ports": [
                    {"port": 22, "protocol": "tcp", "state": "open", "service": "ssh"}
                ]
            }
        ]
        
        # Llenar el árbol de hosts
        for host in sample_hosts:
            item = QTreeWidgetItem(self.hosts_tree)
            item.setText(0, f"{host['ip']} {f'({host['hostname']})' if host['hostname'] else ''}")
            item.setText(1, host['status'])
            item.setData(0, Qt.ItemDataRole.UserRole, host)  # Guardar datos completos
        
        # Expandir el árbol
        self.hosts_tree.expandAll()
    
    def on_host_selected(self):
        """Maneja la selección de un host en el árbol"""
        selected_items = self.hosts_tree.selectedItems()
        if not selected_items:
            self.ports_table.setRowCount(0)
            self.host_info_text.clear()
            return
        
        # Obtener datos del host seleccionado
        host_data = selected_items[0].data(0, Qt.ItemDataRole.UserRole)
        if not host_data:
            return
            
        # Mostrar puertos
        self.ports_table.setRowCount(0)
        for port_info in host_data["ports"]:
            row = self.ports_table.rowCount()
            self.ports_table.insertRow(row)
            
            self.ports_table.setItem(row, 0, QTableWidgetItem(str(port_info["port"])))
            self.ports_table.setItem(row, 1, QTableWidgetItem(port_info["protocol"]))
            self.ports_table.setItem(row, 2, QTableWidgetItem(port_info["state"]))
            self.ports_table.setItem(row, 3, QTableWidgetItem(port_info["service"]))
        
        # Mostrar información del host
        info_text = f"""IP: {host_data['ip']}
Hostname: {host_data['hostname'] if host_data['hostname'] else 'N/A'}
MAC: {host_data['mac']}
Fabricante: {host_data['vendor']}
Sistema Operativo: {host_data['os']}
Estado: {host_data['status']}
Puertos abiertos: {len([p for p in host_data['ports'] if p['state'] == 'open'])}
"""
        self.host_info_text.setText(info_text)
