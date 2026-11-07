#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import asyncio
import logging
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QFile, QTextStream
from qasync import QEventLoop, QApplication as QAsyncApplication
from app.ui.main_window import MainWindow
from app.core.config import is_demo_mode

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.expanduser("~/.nedscaner.log"), encoding='utf-8')
    ]
)
logger = logging.getLogger("NEDScaner")

def load_stylesheet(app):
    """
    Carga la hoja de estilos QSS y la aplica a la aplicación.
    """
    try:
        style_file = QFile("app/ui/styles.qss")
        if not style_file.exists():
            logger.warning("Archivo de estilos no encontrado: app/ui/styles.qss")
            return False
            
        style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stream = QTextStream(style_file)
        stylesheet = stream.readAll()
        app.setStyleSheet(stylesheet)
        style_file.close()
        
        logger.info("Estilos aplicados correctamente")
        return True
    except Exception as e:
        logger.error(f"Error al cargar los estilos: {e}")
        return False

async def _show_demo_notice(main_window: MainWindow) -> None:
    if is_demo_mode():
        QMessageBox.information(
            main_window,
            "Modo demo",
            "NEDSCANNER_DEMO activo: descubrimiento usa red ficticia (sin raw sockets).",
        )
    logger.info("Interfaz de usuario inicializada (demo=%s)", is_demo_mode())


def main() -> int:
    logger.info("Iniciando NEDScaner...")

    app = QAsyncApplication(sys.argv)
    app.setApplicationName("NEDScaner")
    app.setOrganizationName("NEDScaner")

    load_stylesheet(app)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    with loop:
        loop.run_until_complete(_show_demo_notice(main_window))
        return loop.run_forever()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        raise SystemExit(1)
