from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ImageModel:
    path: Path
    data: np.ndarray
    width: int
    height: int
    channels: int

    @classmethod
    def from_numpy(cls, path: str | Path, array: np.ndarray) -> "ImageModel":
        h, w = array.shape[:2]
        channels = array.shape[2] if array.ndim == 3 else 1
        return cls(path=Path(path), data=array, width=w, height=h, channels=channels)

    def clone(self) -> "ImageModel":
        return ImageModel(path=self.path, data=self.data.copy(),
                          width=self.width, height=self.height,
                          channels=self.channels)
