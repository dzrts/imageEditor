from __future__ import annotations
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from ui.editor_widget import EditorWidget
from ui.controllers import AppController
from ui.dialogs import ask_jpeg_quality_dialog

class MainWindow(QMainWindow):
    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("ImageEditor")
        self._foreground_path = None
        self._background_path = None
        self._create_ui()

    def _create_ui(self):
        central = QWidget(); layout = QVBoxLayout(central)
        self.editor = EditorWidget(); layout.addWidget(self.editor)
        btns = QHBoxLayout(); layout.addLayout(btns)
        self.btn_fg = QPushButton("Open Foreground")
        self.btn_bg = QPushButton("Open Background")
        self.btn_export = QPushButton("Export")
        btns.addWidget(self.btn_fg); btns.addWidget(self.btn_bg); btns.addWidget(self.btn_export)
        self.btn_fg.clicked.connect(self._open_foreground)
        self.btn_bg.clicked.connect(self._open_background)
        self.btn_export.clicked.connect(self._export)
        self.setCentralWidget(central)

    def _open_foreground(self):
        path,_ = QFileDialog.getOpenFileName(self,"Open Foreground")
        if path: self._foreground_path = Path(path); self._update_preview()

    def _open_background(self):
        path,_ = QFileDialog.getOpenFileName(self,"Open Background")
        if path:
            self._background_path = Path(path)
            self.controller.set_default_background(self._background_path)
            self._update_preview()

    def _update_preview(self):
        if not self._foreground_path: return
        if self._background_path:
            qimg, err = self.controller.composite_preview(self._foreground_path, self._background_path)
        else:
            qimg, err = self.controller.load_image_for_preview(self._foreground_path)
        if err: QMessageBox.critical(self,"Error",err); return
        self.editor.set_image(qimg)

    def _export(self):
        if not self._foreground_path:
            QMessageBox.critical(self,"Error","No foreground selected")
            return
        out = QFileDialog.getExistingDirectory(self,"Choose Output")
        if not out: return
        saved, err = self.controller.export_composited_image(self._foreground_path,self._background_path,out)
        if err: QMessageBox.critical(self,"Error",err); return
        QMessageBox.information(self,"Export",f"Saved:{saved}")
