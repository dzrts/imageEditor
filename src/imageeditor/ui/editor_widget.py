from __future__ import annotations
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect

class EditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._image = None

    def set_image(self, img):
        self._image = img; self.update()

    def clear(self): self._image=None; self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(30,30,30))
        if not self._image: return
        r = self._scaled_rect(self._image)
        p.drawImage(r, self._image)

    def _scaled_rect(self, img):
        ww, wh = self.width(), self.height()
        iw, ih = img.width(), img.height()
        wr, ir = ww/wh, iw/ih
        if ir > wr:
            sw, sh = ww, int(ww/ir)
        else:
            sh, sw = wh, int(wh*ir)
        x, y = (ww-sw)//2, (wh-sh)//2
        return QRect(x,y,sw,sh)
