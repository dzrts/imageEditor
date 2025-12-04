from __future__ import annotations
from pathlib import Path
from typing import Optional
from .loader import ImageLoader
from .compositor import ImageCompositor
from .converter import ImageConverter
from .model import ImageModel

class ImagePipeline:
    def __init__(self):
        self.loader = ImageLoader()
        self.compositor = ImageCompositor()
        self.converter = ImageConverter()

    def process(self, fg_path, bg_path, output_path, jpeg_quality=95, placement="center") -> Path:
        fg = self.loader.load(fg_path)
        if bg_path:
            bg = self.loader.load(bg_path)
            result = self.compositor.composite(fg, bg, placement)
        else:
            result = fg.clone()
        return self.converter.convert_to_jpeg(result, output_path, quality=jpeg_quality)

    def load_only(self, path): return self.loader.load(path)

    def composite_only(self, fg, bg, placement="center"):
        fg = self.loader.load(fg)
        bg = self.loader.load(bg)
        return self.compositor.composite(fg, bg, placement)
