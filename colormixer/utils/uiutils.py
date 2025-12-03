import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import logging, cv2
from PySide6.QtGui import QImage

def import_exr_as_q_image(exr_path=None):

    if not exr_path:
        logging.error("Exr file not found")
        return None

    # Lire le fichier EXR avec OpenCV
    img = cv2.imread(exr_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)  # float32

    if img is None:
        raise FileNotFoundError(exr_path)

    # Normaliser pour l'affichage 0-255
    img_norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    img_uint8 = img_norm.astype('uint8')

    # Convertir BGR -> RGB
    img_rgb = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2RGB)

    # Convertir en QImage
    h, w, ch = img_rgb.shape
    qimage = QImage(img_rgb.data, w, h, ch * w, QImage.Format_RGB888)

    return qimage
