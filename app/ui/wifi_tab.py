from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt6.QtCore import pyqtSlot
from ..adapters.nmcli_adapter import simulate_wifi_scan
import asyncio
from qasync import QEventLoop

class WifiTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.scan_button = QPushButton("Scan Wi-Fi")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.setLayout(layout)

    @pyqtSlot()
    def start_scan(self):
        self.results_text.setText("Escaneando Wi-Fi... por favor espera.")
        # Ejecutar la operación asíncrona en un hilo separado o con qasync
        loop = asyncio.get_event_loop()
        loop.create_task(self._run_scan_task())

    async def _run_scan_task(self):
        try:
            result = await simulate_wifi_scan()
            self.results_text.append(result)
        except Exception as e:
            self.results_text.append(f"Error durante el escaneo: {e}")
