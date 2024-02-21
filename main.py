import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QDialog, QTextEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize

from ui.main_menu import * 

def initialize():
    app = QApplication(sys.argv)
    m = Main_Menu()
    m.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    initialize()

