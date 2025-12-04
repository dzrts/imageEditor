from __future__ import annotations
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PySide6.QtCore import Qt

def ask_jpeg_quality_dialog(parent, current):
    d = QDialog(parent)
    d.setWindowTitle("JPEG Quality")
    layout = QVBoxLayout(d)
    label = QLabel(f"Quality: {current}")
    slider = QSlider(Qt.Horizontal); slider.setRange(1,100); slider.setValue(current)
    slider.valueChanged.connect(lambda v: label.setText(f"Quality: {v}"))
    btns = QHBoxLayout()
    ok = QPushButton("OK"); cancel = QPushButton("Cancel")
    btns.addWidget(ok); btns.addWidget(cancel)
    layout.addWidget(label); layout.addWidget(slider); layout.addLayout(btns)
    result = {"v":None}
    ok.clicked.connect(lambda: (result.__setitem__("v", slider.value()), d.accept()))
    cancel.clicked.connect(d.reject)
    return result["v"] if d.exec() else None
