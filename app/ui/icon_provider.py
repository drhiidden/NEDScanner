from PyQt6.QtWidgets import QStyle, QApplication
from PyQt6.QtGui import QIcon
import os

class IconProvider:
    """
    Proveedor de iconos para la aplicación NEDScaner.
    Utiliza iconos del sistema Qt para garantizar compatibilidad.
    """
    
    @staticmethod
    def get_icon(icon_type):
        """
        Obtiene un icono del sistema Qt.
        
        Args:
            icon_type: Nombre del icono a obtener.
            
        Returns:
            QIcon: Icono solicitado.
        """
        app = QApplication.instance()
        if not app:
            return QIcon()
            
        style = app.style()
        
        # Mapeo de nombres de iconos a QStyle::StandardPixmap
        icon_map = {
            "scan": QStyle.StandardPixmap.SP_FileDialogContentsView,
            "network": QStyle.StandardPixmap.SP_DriveNetIcon,
            "discovery": QStyle.StandardPixmap.SP_FileDialogInfoView,
            "settings": QStyle.StandardPixmap.SP_FileDialogDetailedView,
            "results": QStyle.StandardPixmap.SP_FileDialogListView,
            "wifi": QStyle.StandardPixmap.SP_ComputerIcon,
            "refresh": QStyle.StandardPixmap.SP_BrowserReload,
            "save": QStyle.StandardPixmap.SP_DialogSaveButton,
            "open": QStyle.StandardPixmap.SP_DialogOpenButton,
            "exit": QStyle.StandardPixmap.SP_DialogCloseButton,
            "help": QStyle.StandardPixmap.SP_DialogHelpButton,
            "about": QStyle.StandardPixmap.SP_MessageBoxInformation,
            "warning": QStyle.StandardPixmap.SP_MessageBoxWarning,
            "error": QStyle.StandardPixmap.SP_MessageBoxCritical,
            "success": QStyle.StandardPixmap.SP_DialogApplyButton,
            "cancel": QStyle.StandardPixmap.SP_DialogCancelButton,
            "add": QStyle.StandardPixmap.SP_FileDialogNewFolder,
            "delete": QStyle.StandardPixmap.SP_TrashIcon,
            "edit": QStyle.StandardPixmap.SP_FileDialogContentsView,
        }
        
        if icon_type in icon_map:
            return style.standardIcon(icon_map[icon_type])
        
        # Si no se encuentra el icono, devolver un icono por defecto
        return style.standardIcon(QStyle.StandardPixmap.SP_TitleBarMenuButton)
