"""
Main application
Controller for data and ui
exec imports the ui and the data and manages the app
"""
import logging
import os.path
import sys
from PySide6.QtWidgets import QApplication

from ui import mainui, editorui
from utils.mainutils import exr_to_jpeg

class Manager:
    def __init__(self):
        self.directory = "D:\work\cg\projects\lighting\maya_arnold"
        self.extensions = ["exr"]

    def _setup_btn_connections(self):
        self.window.btn_convert.clicked.connect(self.action_convert)
        self.window.btn_edit.clicked.connect(self.action_edit)

    def action_convert(self):
        selected_items = self.window.list_widget.selectedItems()
        for sel in selected_items:
            filename = sel.text()
            if os.path.splitext(filename)[1] == ".exr":
                widget_selection = self.window.list_widget.selectedItems()
                filepath = os.path.join(self.directory, filename)
                if not os.path.exists(filepath):
                    logging.error("File does not exist")
                    continue
                new_filename = filename.replace(".exr", ".jpeg")
                new_filepath = os.path.join(self.directory, new_filename)
                exr_to_jpeg(filepath, new_filepath)
                logging.warning(f"Created {new_filename} at {new_filepath}")
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
        self.window = mainui.MainWindow(self, self.directory, self.extensions)
        self.window.populate_list_widget(self.directory)
        self._setup_btn_connections()
        self.window.resize(500, 400)
        self.window.show()


        sys.exit(app.exec())



