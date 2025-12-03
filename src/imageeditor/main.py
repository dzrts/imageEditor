import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
# import os
# import OpenImageIO as oiio
# from PySide6.QtWidgets import QApplication
from .apps import manager
from .ui import mainui

# Initialize main classes
app = QApplication([])
view = mainui.MainWindow()
manager = manager.Manager(view)

# Run program
manager.setup_view()
view.show()
app.exec()