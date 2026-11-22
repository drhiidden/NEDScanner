"""Tutorial primer arranque (QWizard) — Fase 3 ADR-002."""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QLabel,
    QVBoxLayout,
    QWizard,
    QWizardPage,
)

from app.core.config import is_demo_mode
from app.core.user_prefs import set_onboarding_complete, set_scan_authorized


class _WelcomePage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Bienvenido a NEDScanner")
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "Inventario visual de tu red en Linux: descubrimiento, Nmap, Wi‑Fi "
                "y lecciones en la pestaña Aprendizaje."
            )
        )
        layout.addWidget(
            QLabel(
                "Este asistente tarda menos de un minuto. "
                "Solo escanea redes propias o con permiso escrito."
            )
        )


class _EthicsPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Uso responsable")
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "El escaneo no autorizado puede ser ilegal. Los autores no se "
                "responsabilizan del mal uso."
            )
        )
        self._ack = QCheckBox("Entiendo y solo usaré redes autorizadas")
        layout.addWidget(self._ack)
        self.registerField("ethics_ack*", self._ack)

    def validatePage(self) -> bool:
        return self._ack.isChecked()


class _ModePage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Modo demo o red real")
        layout = QVBoxLayout(self)
        if is_demo_mode():
            layout.addWidget(
                QLabel(
                    "Estás en modo demo (sin sockets privilegiados). "
                    "Ideal para leer lecciones y probar la interfaz."
                )
            )
        else:
            layout.addWidget(
                QLabel(
                    "Sin flag demo, los escaneos pueden necesitar permisos de red. "
                    "Para practicar sin root: `python main.py --demo`."
                )
            )
        layout.addWidget(
            QLabel(
                "Recomendación: Descubrimiento en demo → pestaña Aprendizaje → "
                "luego autoriza escaneo real si lo necesitas."
            )
        )


class _AuthorizePage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Autorización (opcional)")
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "Puedes activar ahora la autorización para escaneos reales, "
                "o hacerlo más tarde en Configuración → Seguridad."
            )
        )
        self._auth = QCheckBox("Confirmo permiso para escanear mis redes autorizadas")
        layout.addWidget(self._auth)
        self.registerField("scan_auth", self._auth)

    def validatePage(self) -> bool:
        if self._auth.isChecked() and not is_demo_mode():
            set_scan_authorized(True)
        return True


class _FinishPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Listo")
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "Pulsa Finalizar. Se abrirá la pestaña Aprendizaje; "
                "puedes repetir el tutorial desde Ayuda si lo necesitas."
            )
        )


class FirstRunWizard(QWizard):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Primeros pasos — NEDScanner")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setOption(QWizard.WizardOption.HaveHelpButton, False)
        self.setPixmap(QWizard.WizardPixmap.LogoPixmap, Qt.GlobalColor.transparent)

        self.addPage(_WelcomePage())
        self.addPage(_EthicsPage())
        self.addPage(_ModePage())
        self.addPage(_AuthorizePage())
        self.addPage(_FinishPage())

    def accept(self) -> None:
        set_onboarding_complete(True)
        super().accept()


def should_offer_onboarding() -> bool:
    from app.core.user_prefs import is_onboarding_complete

    return not is_onboarding_complete()


def run_first_run_wizard(parent) -> bool:
    """Muestra el asistente. Devuelve True si el usuario finalizó (Accept)."""
    wizard = FirstRunWizard(parent)
    return wizard.exec() == QWizard.DialogCode.Accepted