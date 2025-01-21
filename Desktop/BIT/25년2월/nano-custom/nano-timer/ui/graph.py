from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt


class GraphFrame(QFrame):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                padding: 10px;
            }
        """)
        
        self.setMinimumHeight(600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 창 크기 조절 시 확장 가능하도록
        
        # 그래프 스타일 설정
        plt.style.use('seaborn-whitegrid')  # 더 깔끔한 그리드 스타일
        self.fig = plt.figure(figsize=(8, 6))
        self.fig.set_facecolor('white')
        
        # 서브플롯 간격 조정
        self.fig.subplots_adjust(left=0.12, right=0.95, bottom=0.1, top=0.95, hspace=0.3)
        
        # 서브플롯 생성
        self.signal_subplot = plt.subplot(2, 1, 1)
        self.impedance_subplot = plt.subplot(2, 1, 2)
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

    def init_subplots(self):
        # Signal subplot 초기화
        self.signal_subplot.clear()
        self.signal_subplot.set_title("Signal", pad=10, fontsize=12, fontweight='bold')
        self.signal_subplot.grid(True, linestyle='--', alpha=0.7)
        self.signal_subplot.set_xlabel("Sample", fontsize=10)
        self.signal_subplot.set_ylabel("Amplitude", fontsize=10)
        
        # Impedance subplot 초기화
        self.impedance_subplot.clear()
        self.impedance_subplot.set_title("Impedance", pad=10, fontsize=12, fontweight='bold')
        self.impedance_subplot.grid(True, linestyle='--', alpha=0.7)
        self.impedance_subplot.set_xlabel("Time (sec)", fontsize=10)
        self.impedance_subplot.set_ylabel("Impedance", fontsize=10)
        
        # 데이터 저장을 위한 리스트 초기화
        self.times = []
        self.impedances = []
        self.signal_data0 = []
        self.signal_data1 = []
        
        self.canvas.draw()

    def update_graph(self, data0, data1, rect, time):
        # 데이터 저장
        self.times.append(time)
        self.impedances.append(abs(rect))
        self.signal_data0 = data0  # 현재 신호 데이터만 저장
        self.signal_data1 = data1
        
        # Signal subplot 업데이트
        self.signal_subplot.clear()
        self.signal_subplot.set_title("Signal", pad=10, fontsize=12, fontweight='bold')
        self.signal_subplot.grid(True, linestyle='--', alpha=0.7)
        self.signal_subplot.plot(self.signal_data0, label='data0', linewidth=1.5)
        self.signal_subplot.plot(self.signal_data1, label='data1', linewidth=1.5)
        self.signal_subplot.legend(frameon=True, loc='upper right')
        self.signal_subplot.set_xlabel("Sample", fontsize=10)
        self.signal_subplot.set_ylabel("Amplitude", fontsize=10)
        
        # Impedance subplot 업데이트 (전체 시간 데이터 표시)
        self.impedance_subplot.clear()
        self.impedance_subplot.set_title("Impedance", pad=10, fontsize=12, fontweight='bold')
        self.impedance_subplot.grid(True, linestyle='--', alpha=0.7)
        self.impedance_subplot.plot(self.times, self.impedances, 'b-', linewidth=1.5)
        self.impedance_subplot.scatter(self.times, self.impedances, color='blue', s=30)
        
        # y축 범위 설정
        if self.impedances:
            max_imp = max(self.impedances)
            self.impedance_subplot.set_ylim([0, max_imp * 1.2])
        
        # x축 범위 설정 (전체 시간 범위 표시)
        if self.times:
            self.impedance_subplot.set_xlim([0, max(self.times) * 1.1])
        
        # 레이블 설정
        self.impedance_subplot.set_xlabel("Time (sec)", fontsize=10)
        self.impedance_subplot.set_ylabel("Impedance", fontsize=10)
        
        self.canvas.draw()

