import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QSize

from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QDialog, QTextEdit
from PySide2.QtGui import QFont, QCloseEvent
from PySide2.QtCore import Qt, QSize
import ui.main_menu as Main_Menu

from ui.ui_element_factory import UI_Element_Factory

from parser.preprocessor import Preprocessor

class Email_Parser(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_menu = Main_Menu
        self.setWindowTitle("Email Parser")
        self.uief = UI_Element_Factory()


        self.layout = QVBoxLayout()
        self.title = self.get_title_widget()
        self.layout.addWidget(self.title)
        self.layout.addStretch(1)
        
        self.processor = Preprocessor()
        
        self.file_to_parse_name = "HTML file to parse"
        self.file_to_parse = self.uief.make_file_explorer_element(self.file_to_parse_name, "Select which HTML email to parse")
        self.layout.addLayout(self.file_to_parse)

        self.parse_btn = self.uief.make_push_button_element("Parse", None, self.parse)
        self.layout.addWidget(self.parse_btn)

        self.rtn_main_menu_btn = self.uief.make_push_button_element("Return to main menu", None, self.return_to_main_menu)
        self.layout.addWidget(self.rtn_main_menu_btn)

        self.quit_btn = self.uief.make_push_button_element("Quit", None, sys.exit)
        self.layout.addWidget(self.quit_btn)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def return_to_main_menu(self):
    # Show the main menu window
        if self.parent():
            self.parent().show()
        # Optionally, close this window
        self.close()
    
    # Open the main menu if the current window is closed
    # by any means other than quitting the application
    def closeEvent(self, event: QCloseEvent):
        parent = self.parent()
        if parent is not None:
            parent.show()  # Show the main window again
        super().closeEvent(event)

    def parse(self):
        self.processor.process(self.uief.getValue(self.file_to_parse_name)) 

    def get_title_widget(self) -> QLabel:
        title = QLabel("Email Parser")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(28)  # Increase the font size
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: black;")  # Set the font color to black
        return title


