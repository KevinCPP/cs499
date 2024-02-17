import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from ui.email_parser import Email_Parser

class Main_Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.resize(250, 50)
        
        self.layout = QVBoxLayout()

        # Create buttons
        self.censor_emails_btn = QPushButton("Censor Emails")
        self.analyze_emails_btn = QPushButton("Analyze Emails")
        self.settings_btn = QPushButton("Settings")
        self.quit_btn = QPushButton("Quit")

        # Add buttons to layout
        self.layout.addWidget(self.censor_emails_btn)
        self.layout.addWidget(self.analyze_emails_btn)
        self.layout.addWidget(self.settings_btn)
        self.layout.addWidget(self.quit_btn)

        # Connect buttons to their functionalities
        self.censor_emails_btn.clicked.connect(self.open_censor_emails)
        self.quit_btn.clicked.connect(sys.exit)

        # Set central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def open_censor_emails(self):
        self.hide()
        self.censor_emails_window = Email_Parser(self)
        self.censor_emails_window.show()
