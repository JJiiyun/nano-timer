import sys

import time

import threading

import pandas as pd

import os



from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout



from ui.control import ControlFrame

from ui.measure import MeasureFrame

from ui.start import StartFrame

from ui.graph import GraphFrame



from dwfNano import dwfImpedance



# main_ui.py (수정된 ImpedanceThread)
class ImpedanceThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            freq = self.parent.control_frame.get_freq() * 1000
            ref = self.parent.control_frame.get_ref()
            # Duration은 분 단위 -> 초로 변환
            duration_minutes = self.parent.control_frame.get_duration()
            total_duration = duration_minutes * 60

            sampling_interval = 0.01  # 0.01초마다 측정

            sample_count = 0
            start_time = time.time()
            last_measure_time = start_time

            self.parent.start_frame.set_el_time("0.00")

            while True:
                if self.parent.stop_flag:
                    print("Stop requested")
                    break

                current_time = time.time()
                elapsed_time = current_time - start_time

                if elapsed_time >= total_duration:
                    print("Timer duration reached")
                    break

                if (current_time - last_measure_time) >= sampling_interval:
                    sample_count += 1
                    # 균일한 샘플 시간 (예: 0.01, 0.02, 0.03, ...)
                    sample_time = sample_count * sampling_interval
                    data0, data1, z = self.measure(freq, ref, sample_time)
                    last_measure_time = current_time
                    self.save_data(data0, data1, z, sample_time)

                # 실제 경과시간은 타이머 표시용으로 사용
                self.parent.start_frame.set_el_time(f"{elapsed_time:.2f}")
                self.msleep(1)
        except Exception as e:
            print(f"Error in run: {e}")
        finally:
            pass

    def measure(self, freq, ref, measure_time):
        try:
            data0, data1 = self.parent.dwfim.getScopeData(freq)
            zo = self.parent.dwfim.calcImpedance(data0, data1)
            z = -ref * zo

            self.parent.measure_frame.set_real(f"{z.real:.3f}")
            self.parent.measure_frame.set_imag(f"{z.imag:.3f}")
            self.parent.measure_frame.set_abs(f"{abs(z):.3f}")

            # 그래프 업데이트 시 x축 값은 균일한 sample_time으로 전달
            self.parent.graph_frame.update_graph(data0, data1, z, measure_time)

            return data0, data1, z

        except Exception as e:
            print(f"Error in measure: {e}")
            return None, None, None

    def save_data(self, data0, data1, z, time_value):
        try:
            new_data = pd.DataFrame({
                'Time(sec)': [time_value],
                'real': [round(z.real, 3)],
                'imag': [round(z.imag, 3)],
                'abs': [round(abs(z), 3)]
            })

            if not hasattr(self.parent, 'data'):
                self.parent.data = new_data
            else:
                self.parent.data = pd.concat([self.parent.data, new_data], ignore_index=True)
        except Exception as e:
            print(f"Error in save_data: {e}")







from PyQt5.QtCore import pyqtSlot, pyqtSignal



class MainUI(QWidget):

    update_signal = pyqtSignal(float, int, object)  # GUI 업데이트를 위한 Signal



    def __init__(self):

        super().__init__()

        

        self.dwfim = dwfImpedance()

        self.dwf_thread = ImpedanceThread(self)



        self.initUI()

        

    def initUI(self):

        self.setWindowTitle("NanoDrop-timer")

        self.setGeometry(100, 100, 1000, 850)

        self.setMinimumSize(1000, 850)

        

        # Frame definition with spacing

        self.graph_frame = GraphFrame()

        self.control_frame = ControlFrame()

        self.measure_frame = MeasureFrame()

        self.start_frame = StartFrame()

        

        # Connect start button event

        self.start_frame.start_btn.clicked.connect(self.startButtonEvent)



        # Main layout

        main_layout = QVBoxLayout()

        main_layout.setSpacing(10)

        main_layout.setContentsMargins(10, 10, 10, 10)

        

        # Graph area

        main_layout.addWidget(self.graph_frame, stretch=1)

        

        # Control area

        control_layout = QHBoxLayout()

        control_layout.setSpacing(10)

        

        control_layout.addWidget(self.control_frame, stretch=4)

        control_layout.addWidget(self.measure_frame, stretch=3)

        control_layout.addWidget(self.start_frame, stretch=3)

        

        main_layout.addLayout(control_layout)

        

        self.setLayout(main_layout)



        self.cur_loop = 0

        self.stop_flag = False





    def startButtonEvent(self):

        start_btn = self.start_frame.start_btn



        if start_btn.isChecked():

            # Start 버튼이 눌렸을 때

            self.stop_flag = False

            self.control_frame.set_disabled_all(True)

            

            # 그래프 초기화는 Start 버튼 눌렀을 때만

            self.graph_frame.init_subplots()

            

            # 데이터프레임 초기화 (필요한 컬럼만)

            self.data = pd.DataFrame(columns=['Time(sec)', 'real', 'imag', 'abs'])

            

            # UI 업데이트

            start_btn.setText("Stop")

            start_btn.setProperty("state", "stop")

            start_btn.style().unpolish(start_btn)

            start_btn.style().polish(start_btn)

            

            # 새로운 쓰레드 생성 및 시작

            self.dwf_thread = ImpedanceThread(self)

            self.dwf_thread.finished.connect(self.on_measurement_finished)

            self.dwf_thread.start()



        else:

            # Stop 버튼이 눌렸을 때

            self.stop_flag = True

            start_btn.setDisabled(True)  # 버튼 비활성화 (측정 완료될 때까지)



    def on_measurement_finished(self):

        # 데이터 저장

        if hasattr(self, 'data') and not self.data.empty:

            try:

                # 현재 스크립트의 디렉토리 경로를 기준으로 data 폴더 경로 설정

                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

                data_dir = os.path.join(current_dir, "data")

                

                # data 디렉토리가 없으면 생성

                if not os.path.exists(data_dir):

                    os.makedirs(data_dir)



                # CSV 파일로 저장

                filename = os.path.join(data_dir, f"{self.control_frame.get_filename()}.csv")

                self.data.to_csv(filename, index=False, encoding='utf-8-sig')

                print(f"Data saved to {filename}")

                

            except Exception as e:

                print(f"Error saving data: {e}")



        # UI 초기화

        self.reset_ui()



    def reset_ui(self):

        # 측정값 초기화

        self.measure_frame.reset_all()

        

        # 타이머 초기화

        self.start_frame.set_el_time("0.00")


        # 그래프 초기화하지 않음 (Start 버튼 눌렀을 때만 초기화)

        # self.graph_frame.init_subplots()  # 이 줄 제거

        

        # 입력 필드 활성화

        self.control_frame.set_disabled_all(False)

        

        # Start 버튼 초기화

        start_btn = self.start_frame.start_btn

        start_btn.setText("Start")

        start_btn.setProperty("state", "start")

        start_btn.style().unpolish(start_btn)

        start_btn.style().polish(start_btn)

        start_btn.setChecked(False)

        start_btn.setEnabled(True)

        

        # 플래그 초기화

        self.stop_flag = False



    def start(self):

        self.dwf_thread.start()


