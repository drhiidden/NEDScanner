from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEDScaner")
        self.setGeometry(100, 100, 1024, 768)
        self.init_ui()

    def init_ui(self):
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
        Las pestañas se importarán desde sus respectivos módulos.
        """
        # Aquí se añadirán las pestañas una vez implementadas
        pass