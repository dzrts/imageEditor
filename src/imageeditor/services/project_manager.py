from __future__ import annotations
from pathlib import Path

class ProjectManager:
    IMAGE_EXTENSIONS = {".exr",".hdr",".tif",".tiff",".jpg",".jpeg",".png",".bmp"}

    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else None

    def resolve(self, path): 
        p = Path(path)
        return p if p.is_absolute() or not self.base_dir else self.base_dir/p

    def list_images(self, directory):
        d = self.resolve(directory)
        if not d.exists(): raise FileNotFoundError(d)
        return sorted([p for p in d.iterdir()
                       if p.suffix.lower() in self.IMAGE_EXTENSIONS])
    def ensure_output_dir(self, d):
        d = self.resolve(d); d.mkdir(parents=True, exist_ok=True); return d

    def make_output_path(self, out_dir, src, suffix="_converted", ext=".jpg"):
        out_dir = self.ensure_output_dir(out_dir)
        src = Path(src)
        return out_dir / f"{src.stem}{suffix}{ext}"
