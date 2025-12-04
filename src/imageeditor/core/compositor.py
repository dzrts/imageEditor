from __future__ import annotations
import numpy as np
import cv2
from pathlib import Path
from .model import ImageModel

class ImageCompositor:
    @staticmethod
    def resize_background(bg: np.ndarray, target_w: int, target_h: int) -> np.ndarray:
        h, w = bg.shape[:2]
        scale = max(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)
        resized = cv2.resize(bg, (nw, nh), interpolation=cv2.INTER_AREA)
        x0 = (nw - target_w) // 2
        y0 = (nh - target_h) // 2
        return resized[y0:y0+target_h, x0:x0+target_w]

    @staticmethod
    def ensure_rgba(arr: np.ndarray) -> np.ndarray:
        if arr.shape[2] == 4: return arr
        if arr.shape[2] == 3:
            alpha = np.ones((arr.shape[0], arr.shape[1], 1), dtype=arr.dtype)
            return np.concatenate([arr, alpha], axis=2)
        raise ValueError("Unsupported channel count.")

    @staticmethod
    def alpha_blend(fg, bg):
        fg_rgb, fg_a = fg[..., :3], fg[..., 3:4]
        bg_rgb, bg_a = bg[..., :3], bg[..., 3:4]
        out_a = fg_a + bg_a * (1 - fg_a)
        out_rgb = (fg_rgb * fg_a + bg_rgb * bg_a * (1 - fg_a)) / np.clip(out_a, 1e-6, None)
        return np.concatenate([out_rgb, out_a], axis=2)

    @staticmethod
    def composite(fg: ImageModel, bg: ImageModel, mode="center") -> ImageModel:
        canvas_w, canvas_h = bg.width, bg.height
        bg_arr = ImageCompositor.resize_background(bg.data, canvas_w, canvas_h)
        fg_arr = fg.data
        fg_h, fg_w = fg_arr.shape[:2]
        bg_arr = ImageCompositor.ensure_rgba(bg_arr)
        fg_arr = ImageCompositor.ensure_rgba(fg_arr)
        output = bg_arr.copy()
        if mode == "center":
            x = (canvas_w - fg_w) // 2
            y = (canvas_h - fg_h) // 2
        region = output[y:y+fg_h, x:x+fg_w]
        output[y:y+fg_h, x:x+fg_w] = ImageCompositor.alpha_blend(fg_arr, region)
        return ImageModel.from_numpy("composited", output)
