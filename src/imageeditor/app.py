from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.controllers import AppController
from services.project_manager import ProjectManager
from services.settings import SettingsManager
from services.error_handler import ErrorHandler

def load_stylesheet(path: str | Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def create_app() -> QApplication:
    app = QApplication([])
    print("toto")
    settings = SettingsManager(); settings.load()
    project_manager = ProjectManager()
    error_handler = ErrorHandler()
    controller = AppController(settings=settings, project_manager=project_manager, error_handler=error_handler)
    style_path = Path(__file__).parent / "ui" / "resources" / "style.qss"
    qss = load_stylesheet(style_path)
    if qss: app.setStyleSheet(qss)
    window = MainWindow(controller)
    window.show()
    return app
