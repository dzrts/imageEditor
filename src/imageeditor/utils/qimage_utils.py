from __future__ import annotations
import numpy as np
from PySide6.QtGui import QImage

def numpy_to_qimage(arr: np.ndarray) -> QImage:
    h, w, ch = arr.shape
    arr8 = (arr * 255).clip(0,255).astype(np.uint8)
    if ch == 3:
        return QImage(arr8.data, w, h, 3*w, QImage.Format_RGB888).copy()
    elif ch == 4:
        return QImage(arr8.data, w, h, 4*w, QImage.Format_RGBA8888).copy()
    else:
        raise ValueError("Unsupported channel count")
