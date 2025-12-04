from __future__ import annotations
import traceback
from pathlib import Path

class ErrorHandler:
    def __init__(self, log_dir=None):
        self.log_dir = Path(log_dir) if log_dir else Path.home()/".imageeditor"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir/"error_log.txt"

    def handle(self, exc):
        self._log_exception(exc)
        return self._format_user_message(exc)

    def _log_exception(self, exc):
        with open(self.log_file,"a",encoding="utf8") as f:
            f.write("="*60+"")
            f.write(str(exc)+"")
            f.write(traceback.format_exc()+"")

    def _format_user_message(self, exc):
        msg = str(exc)
        if isinstance(exc, FileNotFoundError): return f"File not found: {msg}"
        if "Unsupported image format" in msg: return f"Unsupported image: {msg}"
        return f"Error: {msg}"

    def safe_call(self, func, *a, **kw):
        try: return func(*a, **kw), None
        except Exception as exc: return None, self.handle(exc)
