import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QSize

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QDialog, QTextEdit
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, QSize

from ui.main_menu import Main_Menu 

def initialize():
    app = QApplication(sys.argv)
    m = Main_Menu()
    m.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    initialize()

