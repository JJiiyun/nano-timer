from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QDoubleValidator

from ui.text_frame import TextFrame

class MeasureFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
        """)

        self.frames = {
            'real'  : (TextFrame('Real', "", readOnly=True), (0,0,1,1)),
            'imag'  : (TextFrame('Imag', "", readOnly=True), (0,1,1,1)),
            'abs'   : (TextFrame('Abs', "", readOnly=True), (1,0,1,2)),
        }

        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)

        for frame, position in self.frames.values():
            self.layout.addWidget(frame, position[0], position[1], position[2], position[3])

        self.setLayout(self.layout)

    # Get functions
    def get_real(self):
        return float(self.frames['real'][0].get_text())
        
    def get_imag(self):
        return float(self.frames['imag'][0].get_text())

    def get_abs(self):
        return float(self.frames['abs'][0].get_text())

    def get_all2dict(self):
        return {
            'real'      : self.get_real(),
            'imag'       : self.get_imag(),
            'abs'      : self.get_abs(),
        }

    # Set functions
    def set_real(self, text):
        self.frames['real'][0].set_text(text)
        
    def set_imag(self, text):
        self.frames['imag'][0].set_text(text)

    def set_abs(self, text):
        self.frames['abs'][0].set_text(text)

    # Get functions
    def get_real(self):
        return self.frames['real'][0].get_text()

    # Util functions
    def reset_all(self):
        for frame, _ in self.frames.values():
            frame.editor.setText("")