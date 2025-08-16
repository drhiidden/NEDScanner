# NEDScaner

## Descripción

NEDScaner es una aplicación GUI desarrollada con PyQt6 para la detección y visualización de redes Linux, adhiriéndose a la arquitectura HCP.

## Configuración y Ejecución

Sigue estos pasos para configurar y ejecutar la aplicación:

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd NEDScaner
    ```

2.  **Crear y Activar un Entorno Virtual (Opcional pero Recomendado):**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    Navega al directorio raíz del proyecto (`NEDScaner/`) e instala las dependencias usando `pip`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la Aplicación:**
    Una vez instaladas las dependencias, puedes ejecutar la aplicación desde el directorio `NEDScaner/`:
    ```bash
    python nedscaner/main.py
    ```

## Uso

-   Abre la aplicación.
-   Ve a la pestaña "Wi-Fi Scan".
-   Haz clic en el botón "Scan Wi-Fi" para iniciar un escaneo simulado de redes. Los resultados aparecerán en el área de texto.
