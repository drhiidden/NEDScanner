import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop, QApplication as QAsyncApplication
from app.ui import MainWindow, WifiTab

async def main():
    app = QAsyncApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.tab_widget.addTab(WifiTab(), "Wi-Fi")
    main_window.show()

    sys.exit(await loop.run_forever()) # Usa await para esperar la finalización del bucle

if __name__ == "__main__":
    # Para asegurar que la aplicación se ejecuta asíncronamente
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
