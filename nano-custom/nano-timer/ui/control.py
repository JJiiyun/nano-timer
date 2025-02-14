from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QWidget, QGridLayout, QVBoxLayout, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator

from ui.text_frame import TextFrame

class ControlFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 3px;
                margin-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 3px;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                background-color: white;
                min-width: 150px;
            }
        """)

        # 메인 레이아웃
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # 상단 입력 필드 레이아웃 (그리드)
        input_layout = QGridLayout()
        input_layout.setSpacing(10)

        # 각 입력 필드 생성 (Loop와 Period 삭제, Duration 추가)
        self.freq_frame = TextFrame('Freq', "1000", unit_text="KHz", validator=QDoubleValidator())
        self.ref_frame = TextFrame('Ref', "10", unit_text="kOhm", validator=QDoubleValidator())
        self.duration_frame = TextFrame('Duration', "30", unit_text="min", validator=QDoubleValidator())

        input_layout.addWidget(self.freq_frame, 0, 0)
        input_layout.addWidget(self.ref_frame, 0, 1)
        # Duration 필드는 1행 전체(2열)로 배치
        input_layout.addWidget(self.duration_frame, 1, 0, 1, 2)

        # 파일명 입력 필드
        self.filename_frame = TextFrame('Filename', "default", unit_text=".csv")

        # 레이아웃 조립
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.filename_frame)
        
        self.setLayout(self.layout)

        # frames dictionary (불필요한 항목 제거)
        self.frames = {
            'freq': (self.freq_frame, None),
            'ref': (self.ref_frame, None),
            'duration': (self.duration_frame, None),
        }

    # Get functions
    def get_freq(self):
        return float(self.freq_frame.get_text())

    def get_ref(self):
        return float(self.ref_frame.get_text())

    def get_duration(self):
        return float(self.duration_frame.get_text())

    def get_filename(self):
        return self.filename_frame.get_text()

    # 전체 값을 dictionary로 반환
    def get_all2dict(self):
        return {
            'freq'      : self.get_freq(),
            'ref'       : self.get_ref(),
            'duration'  : self.get_duration(),
            'filename'  : self.get_filename(),
        }

    # 모든 입력 필드 비활성화
    def set_disabled_all(self, flag):
        for frame, _ in self.frames.values():
            frame.editor.setDisabled(flag)
        self.filename_frame.editor.setDisabled(flag)
