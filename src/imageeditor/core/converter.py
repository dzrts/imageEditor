from __future__ import annotations
import numpy as np
from pathlib import Path
import cv2
from .model import ImageModel

class ImageConverter:
    @staticmethod
    def to_srgb(array: np.ndarray) -> np.ndarray:
        array = np.clip(array, 0.0, None)
        srgb = np.where(
            array <= 0.0031308,
            array * 12.92,
            1.055 * np.power(array, 1.0 / 2.4) - 0.055,
        )
        return np.clip(srgb, 0.0, 1.0)

    @staticmethod
    def convert_to_jpeg(image: ImageModel, output_path: str | Path, quality: int = 95) -> Path:
        output_path = Path(output_path).with_suffix(".jpg")
        srgb = ImageConverter.to_srgb(image.data)
        srgb_u8 = (srgb * 255).clip(0, 255).astype(np.uint8)
        if image.channels == 3:
            bgr = cv2.cvtColor(srgb_u8, cv2.COLOR_RGB2BGR)
        else:
            bgr = cv2.cvtColor(srgb_u8, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(str(output_path), bgr, [cv2.IMWRITE_JPEG_QUALITY, quality])
        return output_path
