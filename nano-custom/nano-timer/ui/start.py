from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont

from ui.text_frame import TextFrame

class StartFrame(QFrame):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton#start_btn {
                min-height: 35px;
                min-width: 150px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 3px;
            }
            QPushButton#start_btn[state="start"] {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#start_btn[state="start"]:hover {
                background-color: #45a049;
            }
            QPushButton#start_btn[state="start"]:disabled {
                background-color: #cccccc;
            }
            QPushButton#start_btn[state="stop"] {
                background-color: #f44336;
                color: white;
            }
            QPushButton#start_btn[state="stop"]:hover {
                background-color: #d32f2f;
            }
            QPushButton#start_btn[state="stop"]:disabled {
                background-color: #cccccc;
            }
            QPushButton#start_btn:pressed {
                margin: 1px;
            }
        """)
        
        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setProperty("state", "start")
        self.start_btn.setCheckable(True)
        self.start_btn.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.frames = {
            'el_time': (TextFrame('Elapsed', "", unit_text="s", readOnly=True), (1,0,1,1))
        }
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        for frame, _ in self.frames.values():
            info_layout.addWidget(frame)
        
        layout.addLayout(info_layout)
        self.setLayout(layout)

    def set_el_time(self, text):
        print(text)
        self.frames['el_time'][0].set_text(text)
