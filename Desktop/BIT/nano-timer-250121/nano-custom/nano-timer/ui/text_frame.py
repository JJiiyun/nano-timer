from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout


class TextFrame(QFrame):
    def __init__(self, text, value, unit_text=None, validator=None, readOnly=False):
        super().__init__()
        
        self.value = value
        
        # 프레임 자체의 테두리 제거
        self.setStyleSheet('border: none; background: transparent;')
        
        # Set editor
        self.editor = QLineEdit()
        self.editor.setReadOnly(readOnly)  # readOnly 설정을 먼저 함
        
        if readOnly:  # 읽기 전용일 때의 스타일
            self.editor.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #e0e0e0;
                    border-radius: 3px;
                    padding: 5px;
                    background-color: #f8f9fa;
                    color: #2196F3;
                    font-weight: bold;
                }
            """)
        else:  # 입력 가능한 필드의 스타일
            self.editor.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #cccccc;
                    border-radius: 3px;
                    padding: 5px;
                    background-color: white;
                }
            """)
        
        if validator:
            self.editor.setValidator(validator)
            
        self.editor.setText(value)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # 라벨 스타일
        label = QLabel(f"{text} :")
        label.setStyleSheet('border: none; color: #444444; background: transparent;')
        
        self.layout.addWidget(label)
        self.layout.addWidget(self.editor)
        
        if unit_text:
            unit_label = QLabel(f"{unit_text}")
            unit_label.setStyleSheet('border: none; color: #444444; background: transparent;')
            self.layout.addWidget(unit_label)

        self.setLayout(self.layout)

    def get_text(self):
        return self.editor.text()

    def set_text(self, text):
        self.editor.setText(text)