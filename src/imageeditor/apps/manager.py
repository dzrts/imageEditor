"""
Main application
Controller for data and ui
exec imports the ui and the data and manages the app
"""
import logging
import os.path

from ui import editorui
from utils.mainutils import exr_to_jpeg

class Manager(object):
    def __init__(self, view):
        #self.directory = "U:\14_RENDU\s14\s14p0013\Valid_DA\v004\exr"
        self.directory = "D:\work\cg\projects\lighting\maya_arnold"
        self.extensions = ["exr"]
        self.view = view

    def _setup_btn_connections(self):
        self.view.btn_convert.clicked.connect(self.action_convert)
        self.view.btn_edit.clicked.connect(self._action_edit)
        self.view.btn_select_folder.clicked.connect(self._action_select_directory)

    def _action_select_directory(self):
        self.directory = self.view.select_directory()

    def _action_edit(self):
        selected_items = self.view.list_widget.selectedItems()
        if len(selected_items) == 0:
            logging.error("No item selected, cannot edit")
            return None
        first_selected_filename = selected_items[0].text()

        if len(self.view.editor_windows) == 1:
            logging.error("Edit already opened")
            return None
        editor = editorui.EditorBuffer(os.path.join(self.directory, first_selected_filename))
        self.view.editor_windows.append(editor)
        editor.show()

    def _editorCloseEvent(self):
        editor = self.view.editor_windows[0]
        event = editor.event

        def _closeEvent(editor, event):
            print('toto')

    def action_convert(self):
        selected_items = self.view.list_widget.selectedItems()
        if len(selected_items) == 0:
            logging.error("No item selected, cannot convert")
            return None
        for sel in selected_items:
            filename = sel.text()
            fileext = os.path.splitext(filename)[1][1:]
            if fileext in self.extensions:
                widget_selection = self.view.list_widget.selectedItems()
                filepath = os.path.join(self.directory, filename)
                print(filepath)
                if not os.path.exists(filepath):
                    logging.error("File does not exist")
                    continue
                new_filename = filename.replace(".exr", ".jpeg")
                new_filepath = os.path.join(self.directory, new_filename)
                print(new_filepath)
                exr_to_jpeg(filepath, new_filepath)
                logging.warning(f"Created {new_filename} at {new_filepath}")
            elif fileext == "jpeg":
                print(f"{filename} skipped. already converted to jpeg")
            else:
                print(f"{filename} ignored. Only Jpeg is allowed.")

    def setup_view(self):
        self.view.directory = self.directory
        self.view.extensions = self.extensions

        self.view.populate_list_widget(self.directory)
        self._setup_btn_connections()
        self.view.resize(500, 400)






