import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class Results_Window(QDialog):
    def __init__(self, title, parent=None):
        super(Results_Window, self).__init__(parent)
        self.setWindowTitle(title)

        # Setup dialog size and properties
        self.resize(320, 240)

        # Create a QPlainTextEdit widget
        self.textbox = QPlainTextEdit()
        self.textbox.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.textbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textbox.setReadOnly(True)
        font = QFont("Courier")
        self.textbox.setFont(font)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        self.setLayout(layout)

    def set_results_text(self, text):
        self.textbox.setPlainText(text)

