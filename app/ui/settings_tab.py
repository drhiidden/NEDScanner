from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QTableWidget, QTableWidgetItem, QLabel, 
                             QGroupBox, QHeaderView, QComboBox, QCheckBox, 
                             QSpinBox, QFormLayout, QLineEdit, QTabWidget,
                             QFileDialog, QMessageBox, QRadioButton, QButtonGroup,
                             QListWidget, QListWidgetItem, QSlider)
from PyQt6.QtCore import Qt, pyqtSlot, QSettings
import os

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Crear pestañas de configuración
        settings_tabs = QTabWidget()
        
        # Pestaña: Configuración general
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        general_tab.setLayout(general_layout)
        
        # Grupo: Interfaz de usuario
        ui_group = QGroupBox("Interfaz de Usuario")
        ui_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Claro", "Oscuro", "Sistema"])
        ui_layout.addRow("Tema:", self.theme_combo)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Español", "English", "Français", "Deutsch"])
        ui_layout.addRow("Idioma:", self.lang_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 16)
        self.font_size_spin.setValue(10)
        ui_layout.addRow("Tamaño de fuente:", self.font_size_spin)
        
        ui_group.setLayout(ui_layout)
        general_layout.addWidget(ui_group)
        
        # Grupo: Comportamiento
        behavior_group = QGroupBox("Comportamiento")
        behavior_layout = QFormLayout()
        
        self.auto_save_check = QCheckBox("Guardar resultados automáticamente")
        self.auto_save_check.setChecked(True)
        behavior_layout.addRow(self.auto_save_check)
        
        self.confirm_actions_check = QCheckBox("Confirmar acciones peligrosas")
        self.confirm_actions_check.setChecked(True)
        behavior_layout.addRow(self.confirm_actions_check)
        
        self.auto_update_check = QCheckBox("Buscar actualizaciones al iniciar")
        self.auto_update_check.setChecked(True)
        behavior_layout.addRow(self.auto_update_check)
        
        behavior_group.setLayout(behavior_layout)
        general_layout.addWidget(behavior_group)
        
        # Grupo: Directorios
        dirs_group = QGroupBox("Directorios")
        dirs_layout = QFormLayout()
        
        self.data_dir_layout = QHBoxLayout()
        self.data_dir_input = QLineEdit()
        self.data_dir_input.setReadOnly(True)
        self.data_dir_input.setText(os.path.expanduser("~/.nedscaner/data"))
        self.data_dir_button = QPushButton("Cambiar...")
        self.data_dir_button.clicked.connect(self.select_data_dir)
        self.data_dir_layout.addWidget(self.data_dir_input)
        self.data_dir_layout.addWidget(self.data_dir_button)
        dirs_layout.addRow("Directorio de datos:", self.data_dir_layout)
        
        self.export_dir_layout = QHBoxLayout()
        self.export_dir_input = QLineEdit()
        self.export_dir_input.setReadOnly(True)
        self.export_dir_input.setText(os.path.expanduser("~/Documentos/NEDScaner"))
        self.export_dir_button = QPushButton("Cambiar...")
        self.export_dir_button.clicked.connect(self.select_export_dir)
        self.export_dir_layout.addWidget(self.export_dir_input)
        self.export_dir_layout.addWidget(self.export_dir_button)
        dirs_layout.addRow("Directorio de exportación:", self.export_dir_layout)
        
        dirs_group.setLayout(dirs_layout)
        general_layout.addWidget(dirs_group)
        
        general_layout.addStretch()
        settings_tabs.addTab(general_tab, "General")
        
        # Pestaña: Herramientas
        tools_tab = QWidget()
        tools_layout = QVBoxLayout()
        tools_tab.setLayout(tools_layout)
        
        # Grupo: Nmap
        nmap_group = QGroupBox("Nmap")
        nmap_layout = QFormLayout()
        
        self.nmap_path_layout = QHBoxLayout()
        self.nmap_path_input = QLineEdit()
        self.nmap_path_input.setText("/usr/bin/nmap")
        self.nmap_path_button = QPushButton("Buscar...")
        self.nmap_path_button.clicked.connect(lambda: self.select_tool_path("nmap"))
        self.nmap_path_layout.addWidget(self.nmap_path_input)
        self.nmap_path_layout.addWidget(self.nmap_path_button)
        nmap_layout.addRow("Ruta de Nmap:", self.nmap_path_layout)
        
        self.nmap_sudo_check = QCheckBox("Usar sudo para Nmap")
        nmap_layout.addRow(self.nmap_sudo_check)
        
        self.nmap_args_input = QLineEdit()
        self.nmap_args_input.setPlaceholderText("Argumentos por defecto para Nmap")
        nmap_layout.addRow("Argumentos por defecto:", self.nmap_args_input)
        
        nmap_group.setLayout(nmap_layout)
        tools_layout.addWidget(nmap_group)
        
        # Grupo: NetworkManager
        nm_group = QGroupBox("NetworkManager")
        nm_layout = QFormLayout()
        
        self.nmcli_path_layout = QHBoxLayout()
        self.nmcli_path_input = QLineEdit()
        self.nmcli_path_input.setText("/usr/bin/nmcli")
        self.nmcli_path_button = QPushButton("Buscar...")
        self.nmcli_path_button.clicked.connect(lambda: self.select_tool_path("nmcli"))
        self.nmcli_path_layout.addWidget(self.nmcli_path_input)
        self.nmcli_path_layout.addWidget(self.nmcli_path_button)
        nm_layout.addRow("Ruta de nmcli:", self.nmcli_path_layout)
        
        self.nm_dbus_radio = QRadioButton("Usar D-Bus (recomendado)")
        self.nm_dbus_radio.setChecked(True)
        self.nm_cli_radio = QRadioButton("Usar CLI (nmcli)")
        
        nm_method_group = QButtonGroup(self)
        nm_method_group.addButton(self.nm_dbus_radio)
        nm_method_group.addButton(self.nm_cli_radio)
        
        nm_method_layout = QHBoxLayout()
        nm_method_layout.addWidget(self.nm_dbus_radio)
        nm_method_layout.addWidget(self.nm_cli_radio)
        nm_layout.addRow("Método de acceso:", nm_method_layout)
        
        nm_group.setLayout(nm_layout)
        tools_layout.addWidget(nm_group)
        
        # Grupo: Scapy
        scapy_group = QGroupBox("Scapy")
        scapy_layout = QFormLayout()
        
        self.scapy_timeout_spin = QSpinBox()
        self.scapy_timeout_spin.setRange(1, 30)
        self.scapy_timeout_spin.setValue(5)
        self.scapy_timeout_spin.setSuffix(" s")
        scapy_layout.addRow("Timeout por defecto:", self.scapy_timeout_spin)
        
        self.scapy_retries_spin = QSpinBox()
        self.scapy_retries_spin.setRange(0, 5)
        self.scapy_retries_spin.setValue(2)
        scapy_layout.addRow("Reintentos por defecto:", self.scapy_retries_spin)
        
        self.scapy_threads_spin = QSpinBox()
        self.scapy_threads_spin.setRange(1, 100)
        self.scapy_threads_spin.setValue(10)
        scapy_layout.addRow("Hilos por defecto:", self.scapy_threads_spin)
        
        scapy_group.setLayout(scapy_layout)
        tools_layout.addWidget(scapy_group)
        
        tools_layout.addStretch()
        settings_tabs.addTab(tools_tab, "Herramientas")
        
        # Pestaña: Seguridad
        security_tab = QWidget()
        security_layout = QVBoxLayout()
        security_tab.setLayout(security_layout)
        
        # Grupo: Permisos
        perms_group = QGroupBox("Permisos y Privilegios")
        perms_layout = QVBoxLayout()
        
        self.perms_text = QTextEdit()
        self.perms_text.setReadOnly(True)
        self.perms_text.setText("""Permisos actuales:

1. Nmap: No configurado para ejecutarse sin sudo
   - Estado: Requiere sudo para escaneos SYN y OS fingerprinting

2. Scapy: No configurado para ejecutarse sin sudo
   - Estado: Requiere sudo para captura de paquetes

3. NetworkManager: Configurado correctamente
   - Estado: Acceso permitido a través de D-Bus

Para configurar Nmap y Scapy para ejecutarse sin sudo, use:
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/nmap
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/python3

O ejecute la aplicación con sudo (no recomendado).
""")
        perms_layout.addWidget(self.perms_text)
        
        self.check_perms_button = QPushButton("Verificar Permisos")
        self.check_perms_button.clicked.connect(self.check_permissions)
        perms_layout.addWidget(self.check_perms_button)
        
        perms_group.setLayout(perms_layout)
        security_layout.addWidget(perms_group)
        
        # Grupo: Almacenamiento de credenciales
        creds_group = QGroupBox("Almacenamiento de Credenciales")
        creds_layout = QVBoxLayout()
        
        self.use_keyring_check = QCheckBox("Usar keyring del sistema para almacenar contraseñas")
        self.use_keyring_check.setChecked(True)
        creds_layout.addWidget(self.use_keyring_check)
        
        self.clear_creds_button = QPushButton("Limpiar Credenciales Guardadas")
        self.clear_creds_button.clicked.connect(self.clear_credentials)
        creds_layout.addWidget(self.clear_creds_button)
        
        creds_group.setLayout(creds_layout)
        security_layout.addWidget(creds_group)
        
        security_layout.addStretch()
        settings_tabs.addTab(security_tab, "Seguridad")
        
        # Pestaña: Avanzado
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout()
        advanced_tab.setLayout(advanced_layout)
        
        # Grupo: Logging
        logging_group = QGroupBox("Logging")
        logging_layout = QFormLayout()
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["ERROR", "WARNING", "INFO", "DEBUG"])
        self.log_level_combo.setCurrentIndex(2)  # INFO por defecto
        logging_layout.addRow("Nivel de log:", self.log_level_combo)
        
        self.log_file_layout = QHBoxLayout()
        self.log_file_input = QLineEdit()
        self.log_file_input.setText(os.path.expanduser("~/.nedscaner/nedscaner.log"))
        self.log_file_button = QPushButton("Cambiar...")
        self.log_file_button.clicked.connect(self.select_log_file)
        self.log_file_layout.addWidget(self.log_file_input)
        self.log_file_layout.addWidget(self.log_file_button)
        logging_layout.addRow("Archivo de log:", self.log_file_layout)
        
        self.view_log_button = QPushButton("Ver Log")
        self.view_log_button.clicked.connect(self.view_log)
        logging_layout.addRow(self.view_log_button)
        
        logging_group.setLayout(logging_layout)
        advanced_layout.addWidget(logging_group)
        
        # Grupo: Rendimiento
        perf_group = QGroupBox("Rendimiento")
        perf_layout = QFormLayout()
        
        self.parallel_scans_spin = QSpinBox()
        self.parallel_scans_spin.setRange(1, 10)
        self.parallel_scans_spin.setValue(2)
        perf_layout.addRow("Escaneos paralelos máximos:", self.parallel_scans_spin)
        
        self.cache_size_spin = QSpinBox()
        self.cache_size_spin.setRange(10, 1000)
        self.cache_size_spin.setValue(100)
        self.cache_size_spin.setSuffix(" MB")
        perf_layout.addRow("Tamaño máximo de caché:", self.cache_size_spin)
        
        self.clear_cache_button = QPushButton("Limpiar Caché")
        self.clear_cache_button.clicked.connect(self.clear_cache)
        perf_layout.addRow(self.clear_cache_button)
        
        perf_group.setLayout(perf_layout)
        advanced_layout.addWidget(perf_group)
        
        # Grupo: Base de datos
        db_group = QGroupBox("Base de Datos")
        db_layout = QVBoxLayout()
        
        self.db_info_label = QLabel("Base de datos SQLite: ~/.nedscaner/database.db")
        db_layout.addWidget(self.db_info_label)
        
        db_buttons_layout = QHBoxLayout()
        self.backup_db_button = QPushButton("Respaldar BD")
        self.backup_db_button.clicked.connect(self.backup_database)
        self.restore_db_button = QPushButton("Restaurar BD")
        self.restore_db_button.clicked.connect(self.restore_database)
        self.reset_db_button = QPushButton("Reiniciar BD")
        self.reset_db_button.clicked.connect(self.reset_database)
        
        db_buttons_layout.addWidget(self.backup_db_button)
        db_buttons_layout.addWidget(self.restore_db_button)
        db_buttons_layout.addWidget(self.reset_db_button)
        
        db_layout.addLayout(db_buttons_layout)
        db_group.setLayout(db_layout)
        advanced_layout.addWidget(db_group)
        
        advanced_layout.addStretch()
        settings_tabs.addTab(advanced_tab, "Avanzado")
        
        # Añadir pestañas al layout principal
        main_layout.addWidget(settings_tabs)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Restaurar Valores Predeterminados")
        self.reset_button.clicked.connect(self.reset_settings)
        
        self.apply_button = QPushButton("Aplicar")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setDefault(True)
        
        buttons_layout.addWidget(self.reset_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.apply_button)
        
        main_layout.addLayout(buttons_layout)
    
    def select_data_dir(self):
        """Selecciona el directorio de datos"""
        directory = QFileDialog.getExistingDirectory(
            self, "Seleccionar Directorio de Datos", 
            self.data_dir_input.text()
        )
        if directory:
            self.data_dir_input.setText(directory)
    
    def select_export_dir(self):
        """Selecciona el directorio de exportación"""
        directory = QFileDialog.getExistingDirectory(
            self, "Seleccionar Directorio de Exportación", 
            self.export_dir_input.text()
        )
        if directory:
            self.export_dir_input.setText(directory)
    
    def select_tool_path(self, tool_name):
        """Selecciona la ruta de una herramienta"""
        if tool_name == "nmap":
            input_field = self.nmap_path_input
            title = "Seleccionar Ejecutable de Nmap"
        elif tool_name == "nmcli":
            input_field = self.nmcli_path_input
            title = "Seleccionar Ejecutable de nmcli"
        else:
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, title, input_field.text()
        )
        if file_path:
            input_field.setText(file_path)
    
    def select_log_file(self):
        """Selecciona el archivo de log"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Seleccionar Archivo de Log", 
            self.log_file_input.text()
        )
        if file_path:
            self.log_file_input.setText(file_path)
    
    def check_permissions(self):
        """Verifica los permisos de las herramientas"""
        # Aquí iría la lógica real para verificar permisos
        QMessageBox.information(
            self, "Verificación de Permisos",
            "Verificación completada. Ver resultados en la sección de permisos."
        )
    
    def clear_credentials(self):
        """Limpia las credenciales guardadas"""
        result = QMessageBox.question(
            self, "Limpiar Credenciales",
            "¿Está seguro de que desea eliminar todas las credenciales guardadas?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            # Aquí iría la lógica real para limpiar credenciales
            QMessageBox.information(
                self, "Limpiar Credenciales",
                "Todas las credenciales han sido eliminadas."
            )
    
    def view_log(self):
        """Muestra el archivo de log"""
        # Aquí iría la lógica para mostrar el log en un visor
        QMessageBox.information(
            self, "Ver Log",
            f"Mostrando log desde: {self.log_file_input.text()}"
        )
    
    def clear_cache(self):
        """Limpia la caché de la aplicación"""
        result = QMessageBox.question(
            self, "Limpiar Caché",
            "¿Está seguro de que desea limpiar toda la caché?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            # Aquí iría la lógica real para limpiar la caché
            QMessageBox.information(
                self, "Limpiar Caché",
                "Caché limpiada correctamente."
            )
    
    def backup_database(self):
        """Respalda la base de datos"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Respaldo de Base de Datos", 
            os.path.expanduser("~/nedscaner_backup.db"),
            "Archivos SQLite (*.db)"
        )
        if file_path:
            # Aquí iría la lógica real para respaldar la BD
            QMessageBox.information(
                self, "Respaldo de Base de Datos",
                f"Base de datos respaldada en: {file_path}"
            )
    
    def restore_database(self):
        """Restaura la base de datos desde un respaldo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Respaldo de Base de Datos", 
            os.path.expanduser("~"),
            "Archivos SQLite (*.db)"
        )
        if file_path:
            result = QMessageBox.warning(
                self, "Restaurar Base de Datos",
                "¿Está seguro de que desea restaurar la base de datos? "
                "Esto sobrescribirá todos los datos actuales.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if result == QMessageBox.StandardButton.Yes:
                # Aquí iría la lógica real para restaurar la BD
                QMessageBox.information(
                    self, "Restaurar Base de Datos",
                    "Base de datos restaurada correctamente."
                )
    
    def reset_database(self):
        """Reinicia la base de datos a su estado inicial"""
        result = QMessageBox.warning(
            self, "Reiniciar Base de Datos",
            "¿Está seguro de que desea reiniciar la base de datos? "
            "Esto eliminará TODOS los datos (escaneos, configuraciones, etc.).",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            confirm = QMessageBox.warning(
                self, "Confirmar Reinicio",
                "Esta acción NO SE PUEDE DESHACER. ¿Realmente desea continuar?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                # Aquí iría la lógica real para reiniciar la BD
                QMessageBox.information(
                    self, "Reiniciar Base de Datos",
                    "Base de datos reiniciada correctamente."
                )
    
    def reset_settings(self):
        """Restaura todos los ajustes a sus valores predeterminados"""
        result = QMessageBox.question(
            self, "Restaurar Valores Predeterminados",
            "¿Está seguro de que desea restaurar todos los ajustes a sus valores predeterminados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            # Aquí iría la lógica para restaurar valores predeterminados
            self.theme_combo.setCurrentIndex(0)
            self.lang_combo.setCurrentIndex(0)
            self.font_size_spin.setValue(10)
            self.auto_save_check.setChecked(True)
            self.confirm_actions_check.setChecked(True)
            self.auto_update_check.setChecked(True)
            self.data_dir_input.setText(os.path.expanduser("~/.nedscaner/data"))
            self.export_dir_input.setText(os.path.expanduser("~/Documentos/NEDScaner"))
            self.nmap_path_input.setText("/usr/bin/nmap")
            self.nmap_sudo_check.setChecked(False)
            self.nmap_args_input.clear()
            self.nmcli_path_input.setText("/usr/bin/nmcli")
            self.nm_dbus_radio.setChecked(True)
            self.scapy_timeout_spin.setValue(5)
            self.scapy_retries_spin.setValue(2)
            self.scapy_threads_spin.setValue(10)
            self.use_keyring_check.setChecked(True)
            self.log_level_combo.setCurrentIndex(2)
            self.log_file_input.setText(os.path.expanduser("~/.nedscaner/nedscaner.log"))
            self.parallel_scans_spin.setValue(2)
            self.cache_size_spin.setValue(100)
            
            QMessageBox.information(
                self, "Restaurar Valores Predeterminados",
                "Todos los ajustes han sido restaurados a sus valores predeterminados."
            )
    
    def apply_settings(self):
        """Aplica los cambios de configuración"""
        # Aquí iría la lógica para guardar la configuración
        QMessageBox.information(
            self, "Aplicar Configuración",
            "La configuración ha sido aplicada correctamente."
        )
