from PyQt6.QtCore import QDir, QFile, QIODevice
from PyQt6.QtGui import QIcon, QPixmap
import os
import base64

# Iconos codificados en base64 para evitar dependencias de archivos externos
ICONS = {
    "down_arrow": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAGCAYAAAD68A/GAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABLSURBVBhXY/z//z8DKYAJShMEjY2N/6EmwQWRFYErRlGIrBhdMUgMbDQIMEJpOEDWhKwYWTFIDLsirBrQFcMVY9WATTFWDcgKGRgYAIj5FylNtLfJAAAAAElFTkSuQmCC",
    
    "checkmark": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABYSURBVChTY/z//z8DKYARpuHRo0eMyIrMzMwYkMWQNYA0wsD///8ZYOIgDDIFphCZBgFkxTA+TAzFBLIVg/ggNkwMxQSYQmQaBJAVw/gwMbgGYjQwMDAAAI5UFu9DOOk1AAAAAElFTkSuQmCC",
    
    "branch-open": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABfSURBVChTY/z//z8DKYARpuHRo0eMyIrMzMwYkMWQNYA0wsD///8ZYOIgDDIFphCZBgFkxTA+TAzFBLIVg/ggNkwMxQSYQmQaBJAVw/gwMbgGYjQwMDAAAI5UFu9DOOk1AAAAAElFTkSuQmCC",
    
    "branch-closed": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABISURBVChTY/z//z8DKYARpuHRo0eMyIrMzMwYkMWQNYA0wsD///8ZYOIgDDIFphCZBgFkxTA+TAzFBLIVg/ggNkwMxQSYQkYGAIj5FylNtLfJAAAAAElFTkSuQmCC",
    
    "branch-more": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAA1SURBVChTY/z//z8DKYARpuHRo0eMyIrMzMwYkMWQNYA0EgWGlAYmJP9jBcRoYGBgAAA+UBXE+XnABwAAAABJRU5ErkJggg==",
    
    "branch-end": "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAA1SURBVChTY/z//z8DKYARpuHRo0eMyIrMzMwYkMWQNYA0EgWGlAYmJP9jBcRoYGBgAAA+UBXE+XnABwAAAABJRU5ErkJggg==",
    
    "vline": "iVBORw0KGgoAAAANSUhEUgAAAAIAAAAMCAYAAABIvGxUAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYSURBVBhXY/z//z8DAwPD/////2fAAhgZAD6JCrFHbvVcAAAAAElFTkSuQmCC"
}

def save_icons_to_disk():
    """
    Guarda los iconos codificados en base64 como archivos en el sistema de archivos.
    """
    # Crear directorio para los iconos si no existe
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    # Guardar cada icono como archivo
    for icon_name, icon_data in ICONS.items():
        icon_path = os.path.join(icons_dir, f"{icon_name}.png")
        with open(icon_path, "wb") as f:
            f.write(base64.b64decode(icon_data))

def get_icon(name):
    """
    Obtiene un QIcon a partir del nombre del icono.
    """
    if name in ICONS:
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ICONS[name]))
        return QIcon(pixmap)
    return QIcon()

def get_pixmap(name):
    """
    Obtiene un QPixmap a partir del nombre del icono.
    """
    if name in ICONS:
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(ICONS[name]))
        return pixmap
    return QPixmap()

# Inicializar recursos
def init_resources():
    """
    Inicializa los recursos necesarios para la aplicación.
    """
    save_icons_to_disk()
