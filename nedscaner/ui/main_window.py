from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from nedscaner.ui.wifi_tab import WifiTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEDScaner")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.wifi_tab = WifiTab()
        self.tab_widget.addTab(self.wifi_tab, "Wi-Fi Scan")
