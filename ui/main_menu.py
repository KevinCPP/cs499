import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QDialog, QTextEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize

from ui.results_menu import Results_Window
from ui.ui_element_factory import UI_Element_Factory

from parser.file_io import file_in
from parser.preprocessor import Preprocessor
from parser.parser import Parser

from parser.document_distance import Sentiment_Analysis

class Main_Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Parser")
        self.uief = UI_Element_Factory()

        self.layout = QVBoxLayout()
        self.title = self.get_title_widget()
        self.layout.addWidget(self.title)
        self.layout.addStretch(1)
       
        self.processor = Preprocessor()
        self.sa = Sentiment_Analysis()
        self.parser = Parser()
        
        self.file_to_parse_name = "HTML file to parse"
        self.file_to_parse = self.uief.make_file_explorer_element(self.file_to_parse_name, "Select which HTML email to parse")
        self.layout.addLayout(self.file_to_parse)

        self.parse_btn = self.uief.make_push_button_element("Parse", None, self.parse)
        self.layout.addWidget(self.parse_btn)

        self.make_graph_btn = self.uief.make_push_button_element("Make Graph", None, self.make_graph)
        self.layout.addWidget(self.make_graph_btn)

        self.quit_btn = self.uief.make_push_button_element("Quit", None, sys.exit)
        self.layout.addWidget(self.quit_btn)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def parse(self):
        self.processor.process(self.uief.getValue(self.file_to_parse_name)) 

    def make_graph(self):
        self.parser.plot_eyesight_age(self.uief.getValue(self.file_to_parse_name))
        
        # sentiment analysis (this is hacky, may want to refactor)

        patients = []
        files = self.uief.getValue(self.file_to_parse_name)
        for file in files:
            if os.path.isfile(file):
                success, text = file_in(file)
                if success:
                    patients += self.parser.get_patients(text)

        # path to negative/positive words
        success, positive = file_in("sentiment/positive.txt")
        if not success:
            print(f"Error: failed to read positive sentiment file")

        success, negative = file_in("sentiment/negative.txt")
        if not success:
            print(f"Error: failed to read negative sentiment file")

        neg_count = 0
        pos_count = 0
        for patient in patients:
            res = self.sa.sentiment_analysis(patient, positive, negative)
            if res[0] >= res[1]:
                pos_count += 1
            else:
                neg_count += 1

        self.rw = Results_Window("sentiment analysis results")
        self.rw.set_results_text(f"Sentiment Analysis\nPositive: {pos_count}\nNegative: {neg_count}")
        self.rw.show()

    def get_title_widget(self) -> QLabel:
        title = QLabel("Email Parser")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(28)  # Increase the font size
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: blue;")  # Set the font color to white
        return title

