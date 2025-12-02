import OpenImageIO as oiio
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap

import numpy as np

class EditorBuffer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor")
        self.label = QLabel()

        buf = oiio.ImageBuf("D:\work\cg\projects\lighting\maya_arnold\studio_small_08_4k.jpeg")
        pixels = buf.get_pixels(0, buf.spec().width, 0, buf.spec().height, 0, 3)
        pixels = (np.clip(pixels, 0, 1) * 255).astype(np.uint8)

        height, width, channels = pixels.shape
        stride = width * channels
        qimage = QImage(pixels.data, width, height, stride, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimage))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


    def add_layer(self):
        pass

    def remove_layer(self):
        pass

def qimage_to_numpy(image_path):

    image = image.convertToFormat(QImage.Format.Format_RGBA8888)
    width = image.width()

    height = image.height()
    ptr = image.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr

#print (qimage_to_numpy("D:\work\cg\projects\lighting\maya_arnold\studio_small_08_4k.jpeg"))
