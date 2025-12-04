from __future__ import annotations
from pathlib import Path
from PySide6.QtGui import QImage
from core.pipeline import ImagePipeline
from services.project_manager import ProjectManager
from services.settings import SettingsManager
from services.error_handler import ErrorHandler
from utils.qimage_utils import numpy_to_qimage

class AppController:
    def __init__(self, settings: SettingsManager, project_manager: ProjectManager, error_handler: ErrorHandler):
        self.settings = settings
        self.project_manager = project_manager
        self.error_handler = error_handler
        self.pipeline = ImagePipeline()

    def load_image_for_preview(self, path):
        result, err = self.error_handler.safe_call(self.pipeline.load_only, path)
        if err: return None, err
        return numpy_to_qimage(result.data), None

    def composite_preview(self, fg, bg):
        if not bg: return self.load_image_for_preview(fg)
        result, err = self.error_handler.safe_call(
            self.pipeline.composite_only, fg, bg,
            self.settings.settings.placement_mode
        )
        if err: return None, err
        return numpy_to_qimage(result.data), None

    def export_composited_image(self, fg, bg, out_dir):
        out = self.project_manager.make_output_path(out_dir, fg, suffix="_export")
        saved, err = self.error_handler.safe_call(
            self.pipeline.process, fg, bg, out,
            self.settings.settings.jpeg_quality,
            self.settings.settings.placement_mode
        )
        if err: return None, err
        self.settings.update_last_folders(Path(fg).parent, out_dir)
        return saved, None

    def set_default_background(self, p): self.settings.set_default_background(p)
    def set_jpeg_quality(self, v): self.settings.settings.jpeg_quality=int(v); self.settings.save()
    def set_placement_mode(self, m): self.settings.settings.placement_mode=m; self.settings.save()
