from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QStatusBar, QLabel, QToolBar, QMenu
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction

from app.ui.wifi_tab import WifiTab
from app.ui.nmap_tab import NmapTab
from app.ui.discovery_tab import DiscoveryTab
from app.ui.results_tab import ResultsTab
from app.ui.settings_tab import SettingsTab
from app.ui.icon_provider import IconProvider

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEDScaner")
        self.setGeometry(100, 100, 1024, 768)
        self.init_ui()

    def init_ui(self):
        # Crear barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
        
        # Crear barra de herramientas
        self.toolbar = QToolBar("Herramientas Principales")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)
        
        # Acciones para la barra de herramientas
        self.action_scan_wifi = QAction(IconProvider.get_icon("wifi"), "Escanear Wi-Fi", self)
        self.action_scan_wifi.setStatusTip("Iniciar un escaneo de redes Wi-Fi")
        self.action_scan_wifi.triggered.connect(self.start_wifi_scan)
        self.toolbar.addAction(self.action_scan_wifi)
        
        self.action_scan_network = QAction(IconProvider.get_icon("network"), "Escanear Red", self)
        self.action_scan_network.setStatusTip("Iniciar un escaneo de red con Nmap")
        self.action_scan_network.triggered.connect(self.start_network_scan)
        self.toolbar.addAction(self.action_scan_network)
        
        self.action_quick_discovery = QAction(IconProvider.get_icon("discovery"), "Descubrimiento Rápido", self)
        self.action_quick_discovery.setStatusTip("Iniciar un descubrimiento rápido de dispositivos")
        self.action_quick_discovery.triggered.connect(self.start_quick_discovery)
        self.toolbar.addAction(self.action_quick_discovery)
        
        self.toolbar.addSeparator()
        
        self.action_view_results = QAction(IconProvider.get_icon("results"), "Ver Resultados", self)
        self.action_view_results.setStatusTip("Ver historial de escaneos")
        self.action_view_results.triggered.connect(self.show_results)
        self.toolbar.addAction(self.action_view_results)
        
        self.action_settings = QAction(IconProvider.get_icon("settings"), "Configuración", self)
        self.action_settings.setStatusTip("Abrir configuración")
        self.action_settings.triggered.connect(self.show_settings)
        self.toolbar.addAction(self.action_settings)
        
        # Crear menú
        self.menu_bar = self.menuBar()
        
        # Menú Archivo
        file_menu = self.menu_bar.addMenu("&Archivo")
        
        action_exit = QAction(IconProvider.get_icon("exit"), "&Salir", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.setStatusTip("Salir de la aplicación")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)
        
        # Menú Escaneo
        scan_menu = self.menu_bar.addMenu("&Escaneo")
        
        scan_menu.addAction(self.action_scan_wifi)
        scan_menu.addAction(self.action_scan_network)
        scan_menu.addAction(self.action_quick_discovery)
        
        # Menú Ver
        view_menu = self.menu_bar.addMenu("&Ver")
        view_menu.addAction(self.action_view_results)
        
        # Menú Herramientas
        tools_menu = self.menu_bar.addMenu("&Herramientas")
        tools_menu.addAction(self.action_settings)
        
        # Menú Ayuda
        help_menu = self.menu_bar.addMenu("A&yuda")
        
        action_about = QAction(IconProvider.get_icon("about"), "&Acerca de", self)
        action_about.setStatusTip("Mostrar información sobre la aplicación")
        action_about.triggered.connect(self.show_about)
        help_menu.addAction(action_about)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Widget de pestañas
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Inicializar pestañas
        self.init_tabs()
        
    def init_tabs(self):
        """
        Inicializa todas las pestañas de la aplicación.
        """
        # Pestaña Wi-Fi
        self.wifi_tab = WifiTab()
        self.tab_widget.addTab(self.wifi_tab, IconProvider.get_icon("wifi"), "Wi-Fi")
        
        # Pestaña Nmap
        self.nmap_tab = NmapTab()
        self.tab_widget.addTab(self.nmap_tab, IconProvider.get_icon("network"), "Escaneo de Red")
        
        # Pestaña Descubrimiento
        self.discovery_tab = DiscoveryTab()
        self.tab_widget.addTab(self.discovery_tab, IconProvider.get_icon("discovery"), "Descubrimiento Rápido")
        
        # Pestaña Resultados
        self.results_tab = ResultsTab()
        self.tab_widget.addTab(self.results_tab, IconProvider.get_icon("results"), "Resultados")
        
        # Pestaña Configuración
        self.settings_tab = SettingsTab()
        self.tab_widget.addTab(self.settings_tab, IconProvider.get_icon("settings"), "Configuración")
    
    def start_wifi_scan(self):
        """Inicia un escaneo Wi-Fi desde la barra de herramientas"""
        self.tab_widget.setCurrentWidget(self.wifi_tab)
        self.wifi_tab.start_scan()
        self.status_bar.showMessage("Escaneando redes Wi-Fi...")
    
    def start_network_scan(self):
        """Inicia un escaneo de red desde la barra de herramientas"""
        self.tab_widget.setCurrentWidget(self.nmap_tab)
        # No iniciamos automáticamente porque necesitamos un objetivo
        self.status_bar.showMessage("Por favor, especifique un objetivo para el escaneo de red")
    
    def start_quick_discovery(self):
        """Inicia un descubrimiento rápido desde la barra de herramientas"""
        self.tab_widget.setCurrentWidget(self.discovery_tab)
        # No iniciamos automáticamente porque necesitamos un objetivo
        self.status_bar.showMessage("Por favor, especifique un objetivo para el descubrimiento rápido")
    
    def show_results(self):
        """Muestra la pestaña de resultados"""
        self.tab_widget.setCurrentWidget(self.results_tab)
        self.status_bar.showMessage("Mostrando historial de escaneos")
    
    def show_settings(self):
        """Muestra la pestaña de configuración"""
        self.tab_widget.setCurrentWidget(self.settings_tab)
        self.status_bar.showMessage("Configuración")
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        # Aquí se implementaría un diálogo de "Acerca de"
        self.status_bar.showMessage("NEDScaner - Aplicación para detección y visualización de redes Linux")