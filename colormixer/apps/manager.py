"""
Main application
Controller for data and ui
exec imports the ui and the data and manages the app
"""
import os.path
import sys
from PySide6.QtWidgets import QApplication

from ui import mainui, editorui
from utils.mainutils import exr_to_jpeg

class Manager:
    def __init__(self):
        pass

    def _setup_btn_connections(self):
        self.window.btn_convert.clicked.connect(self.action_convert)
        self.window.btn_edit.clicked.connect(self.action_edit)

    def action_convert(self):
        selected_items = self.window.list_widget.selectedItems()
        for item in selected_items:
            filename = item.text()
            print(filename)
            print(os.path.splitext(filename)[1])
            if os.path.splitext(filename)[1] == ".exr":
                exr_to_jpeg()
            elif os.path.splitext(filename)[1] == ".jpeg":
                print(f"{filename} skipped. already converted to jpeg")
            else:
                print(f"{filename} ignored. Only Jpeg is allowed.")


    def action_edit(self):
        editor = editorui.EditorBuffer()
        editor.show()
        editor.add_layer()

    def exec(self):
        """
        :return:
        """
        # Launch app and display window
        app = QApplication(sys.argv)
        self.window = mainui.MainWindow(self)
        self._setup_btn_connections()
        self.window.resize(500, 400)
        self.window.show()
        sys.exit(app.exec())
