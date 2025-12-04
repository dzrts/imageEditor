from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

SETTINGS_FILENAME = "imageeditor_settings.json"

@dataclass
class AppSettings:
    jpeg_quality: int = 95
    default_background: Optional[str] = None
    last_input_folder: Optional[str] = None
    last_output_folder: Optional[str] = None
    placement_mode: str = "center"

    def to_dict(self): return self.__dict__
    @staticmethod
    def from_dict(d): return AppSettings(**d)

class SettingsManager:
    def __init__(self, config_dir=None):
        self.config_dir = Path(config_dir) if config_dir else Path.home()/".imageeditor"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings_path = self.config_dir/SETTINGS_FILENAME
        self.settings = AppSettings()

    def load(self):
        if self.settings_path.exists():
            try: self.settings = AppSettings.from_dict(json.loads(self.settings_path.read_text()))
            except: pass

    def save(self): self.settings_path.write_text(json.dumps(self.settings.to_dict(), indent=4))

    def update_last_folders(self, inp, out):
        self.settings.last_input_folder = str(inp)
        self.settings.last_output_folder = str(out)
        self.save()

    def set_default_background(self, p):
        self.settings.default_background = str(p)
        self.save()
