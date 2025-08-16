#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import asyncio
import logging
import os
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop, QApplication as QAsyncApplication
from app.ui.main_window import MainWindow

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

async def main():
    """
    Función principal que inicia la aplicación NEDScaner.
    Configura el bucle de eventos asíncrono y muestra la ventana principal.
    """
    logger.info("Iniciando NEDScaner...")
    
    # Crear la aplicación Qt
    app = QAsyncApplication(sys.argv)
    app.setApplicationName("NEDScaner")
    app.setOrganizationName("NEDScaner")
    
    # Configurar el bucle de eventos
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Crear y mostrar la ventana principal
    main_window = MainWindow()
    main_window.show()
    
    logger.info("Interfaz de usuario inicializada")
    
    # Ejecutar el bucle de eventos
    try:
        await loop.run_forever()
    except Exception as e:
        logger.error(f"Error en el bucle de eventos: {e}")
    finally:
        logger.info("Cerrando NEDScaner")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)