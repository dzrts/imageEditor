from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QScrollArea
from PySide6.QtGui import QPixmap, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt

from utils import uiutils

class EditorBuffer(QWidget):
    def __init__(self, exr_path=None):
        super().__init__()

        self.setWindowTitle("Editor")
        self.scale_factor = 1.0  # facteur de zoom initial

        self.qimage = uiutils.import_exr_as_q_image(exr_path)

        self.label = QLabel()
        self.qimage = self.qimage.scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.original_pixmap = QPixmap.fromImage(self.qimage)
        self.label.setPixmap(self.original_pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        # QScrollArea
        self.scroll = NoWheelScrollArea()
        self.scroll.setWidgetResizable(False)  # permet à l'image de suivre la taille du scroll area
        self.scroll.setAlignment(Qt.AlignCenter)  # <-- centrer quand l'image est plus petite
        self.scroll.setWidget(self.label)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.resize(800, 600)

    def wheelEvent(self, event: QWheelEvent):
        """Zoom avec la molette."""
        angle = event.angleDelta().y()
        factor = 1.1 if angle > 0 else 0.9  # zoom in/out
        self.scale_factor *= factor

        # Zoom limit
        self.scale_factor = max(0.1, min(self.scale_factor, 10.0))

        # Position du curseur relative au scroll area
        cursor_pos = self.scroll.viewport().mapFromGlobal(event.globalPosition().toPoint())
        h_scroll = self.scroll.horizontalScrollBar()
        v_scroll = self.scroll.verticalScrollBar()
        rel_x = (h_scroll.value() + cursor_pos.x()) / self.label.width()
        rel_y = (v_scroll.value() + cursor_pos.y()) / self.label.height()

        # Reformat pixmap
        size = self.original_pixmap.size() * self.scale_factor
        scaled_pixmap = self.original_pixmap.scaled(
            size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)
        self.label.resize(scaled_pixmap.size())

        # Ajuster les scrollbars pour que le curseur reste sur le même point
        h_scroll.setValue(int(rel_x * self.label.width() - cursor_pos.x()))
        v_scroll.setValue(int(rel_y * self.label.height() - cursor_pos.y()))

        event.accept()

    # Start pan
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._panning = True
            self._pan_start = event.position().toPoint()  # position initiale
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            event.accept()

    # Pan
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._panning:
            delta = event.position().toPoint() - self._pan_start
            self._pan_start = event.position().toPoint()

            # Move scrollbar
            h_scroll = self.scroll.horizontalScrollBar()
            v_scroll = self.scroll.verticalScrollBar()
            h_scroll.setValue(h_scroll.value() - delta.x())
            v_scroll.setValue(v_scroll.value() - delta.y())
            event.accept()

    # End pan
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._panning = False
            QApplication.restoreOverrideCursor()
            event.accept()

    def add_layer(self):
        pass

    def remove_layer(self):
        pass

class NoWheelScrollArea(QScrollArea):
    def wheelEvent(self, event):
        event.ignore()   # <-- Désactive le scroll à la molette

#print (qimage_to_numpy("D:\work\cg\projects\lighting\maya_arnold\studio_small_08_4k.jpeg"))
