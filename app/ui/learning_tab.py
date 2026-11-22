"""Pestaña Aprendizaje — lecciones docs/learn + contexto del último escaneo."""
from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from app.core.learning_catalog import Lesson, list_lessons, load_lesson_text
from app.core.scan_context_for_learning import format_practice_context


class LearningTab(QWidget):
    practice_requested = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._lessons: list[Lesson] = []
        self._current: Lesson | None = None
        self._build_ui()
        self.reload_catalog()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        intro = QLabel(
            "Lee un concepto y compáralo con tu red (solo redes propias o autorizadas)."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        splitter = QSplitter()
        layout.addWidget(splitter)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("Lecciones"))
        self.lesson_list = QListWidget()
        self.lesson_list.currentRowChanged.connect(self._on_lesson_selected)
        left_layout.addWidget(self.lesson_list)
        splitter.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        self.lesson_view = QTextBrowser()
        self.lesson_view.setOpenExternalLinks(True)
        right_layout.addWidget(self.lesson_view, stretch=3)

        right_layout.addWidget(QLabel("Tu último escaneo (esta sesión)"))
        self.context_view = QTextBrowser()
        self.context_view.setMaximumHeight(180)
        right_layout.addWidget(self.context_view, stretch=1)

        btn_row = QHBoxLayout()
        self.practice_button = QPushButton("Ir a la práctica")
        self.practice_button.clicked.connect(self._emit_practice)
        self.refresh_button = QPushButton("Actualizar datos")
        self.refresh_button.clicked.connect(self.refresh_context)
        btn_row.addWidget(self.practice_button)
        btn_row.addWidget(self.refresh_button)
        btn_row.addStretch()
        right_layout.addLayout(btn_row)

        splitter.addWidget(right)
        splitter.setSizes([220, 700])

    def reload_catalog(self) -> None:
        self.lesson_list.clear()
        self._lessons = list_lessons()
        for lesson in self._lessons:
            item = QListWidgetItem(lesson.title)
            self.lesson_list.addItem(item)
        if self._lessons:
            self.lesson_list.setCurrentRow(0)
        else:
            self.lesson_view.setMarkdown(
                "*No hay lecciones en `docs/learn/`. Consulta el README del proyecto.*"
            )

    def _on_lesson_selected(self, row: int) -> None:
        if row < 0 or row >= len(self._lessons):
            return
        self._current = self._lessons[row]
        text = load_lesson_text(self._current.rel_path)
        self.lesson_view.setMarkdown(text)
        self.refresh_context()

    def refresh_context(self) -> None:
        self.context_view.setMarkdown(format_practice_context(self._current))

    def _emit_practice(self) -> None:
        if self._current:
            self.practice_requested.emit(self._current.practice_kind)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self.refresh_context()