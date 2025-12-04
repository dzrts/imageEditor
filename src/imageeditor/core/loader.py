from __future__ import annotations
import numpy as np
from pathlib import Path
import OpenImageIO as oiio
import cv2
from .model import ImageModel

class ImageLoader:
    SUPPORTED_OIIO_EXT = {".exr", ".hdr", ".tif", ".tiff"}
    SUPPORTED_OPENCV_EXT = {".jpg", ".jpeg", ".png", ".bmp"}

    @staticmethod
    def load(path: str | Path) -> ImageModel:
        path = Path(path)
        ext = path.suffix.lower()
        if not path.exists(): raise FileNotFoundError(f"Image not found: {path}")
        if ext in ImageLoader.SUPPORTED_OIIO_EXT: return ImageLoader._load_with_oiio(path)
        if ext in ImageLoader.SUPPORTED_OPENCV_EXT: return ImageLoader._load_with_opencv(path)
        raise ValueError(f"Unsupported image format: {ext}")

    @staticmethod
    def _load_with_oiio(path: Path) -> ImageModel:
        inp = oiio.ImageInput.open(str(path))
        if not inp: raise RuntimeError(f"OIIO failed to open image: {path}")
        try:
            spec = inp.spec()
            w, h, ch = spec.width, spec.height, spec.nchannels
            pixels = inp.read_image("float")
            if pixels is None: raise RuntimeError(f"OIIO failed to read pixel data: {path}")
            arr = np.array(pixels, dtype=np.float32).reshape((h, w, ch))
            if ch == 1:
                arr = np.repeat(arr, 3, axis=2)
                ch = 3
            return ImageModel(path=path, data=arr, width=w, height=h, channels=ch)
        finally:
            inp.close()

    @staticmethod
    def _load_with_opencv(path: Path) -> ImageModel:
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if img is None: raise RuntimeError(f"OpenCV failed to load image: {path}")
        if img.ndim == 3: img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        h, w = img.shape[:2]
        ch = img.shape[2] if img.ndim == 3 else 1
        return ImageModel(path=path, data=img, width=w, height=h, channels=ch)
