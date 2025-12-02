import os, logging

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QFileDialog, QLineEdit
)
from PySide6.QtCore import Qt
from utils import mainutils


class MainWindow(QMainWindow):
    def __init__(self, manager=None):
        super().__init__()
        if not manager:
            logging.debug("No manager assigned to application")

        self.setWindowTitle("File lister")

        self.current_folder = None
        self._all_files = []  # liste complète pour filtrage

        # Widgets
        self.btn_select_folder = QPushButton("Chose a directory")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")

        self.list_widget = QListWidget()

        self.btn_convert = QPushButton("Convert")
        self.btn_edit = QPushButton("Edit")
        # Actions buttons layout
        action_btn_layout = QHBoxLayout()
        action_btn_layout.addWidget(self.btn_convert)
        action_btn_layout.addWidget(self.btn_edit)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.btn_select_folder)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.list_widget)
        layout.addLayout(action_btn_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connections
        self.btn_select_folder.clicked.connect(self._select_directory)
        self.search_bar.textChanged.connect(self._filter_files)


    def _select_directory(self,directory=None):
        """

        :param directory:
        :return:
        """
        directory = QFileDialog.getExistingDirectory(
            self,
            "Choisir un dossier",
            "",
            QFileDialog.ShowDirsOnly
        )

        if directory:
            self.list_widget.clear()

            self._files = mainutils.listAllFiles(directory)
            for f in self._files:
                if os.path.isfile(f):
                    filename = os.path.basename(f)
                    self.list_widget.addItem(filename)

    def _load_files(self, folder):
        self._all_files = []
        for f in os.listdir(folder):
            fullpath = os.path.join(folder, f)
            if os.path.isfile(fullpath):
                self._all_files.append(f)
        self._update_list(self._all_files)

    def _update_list(self, files):
        self.list_widget.clear()
        for f in files:
            self.list_widget.addItem(f)

    def _filter_files(self):
        if not self._all_files:
            return

        query = self.search_bar.text().lower()
        if not query:
            self._update_list(self._all_files)
            return
        print(query)
        print(f.lower())
        filtered = [f for f in self._all_files if query in f.lower()]
        self._update_list(filtered)

