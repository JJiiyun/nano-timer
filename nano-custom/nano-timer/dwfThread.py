import sys
import time
import threading

from dwfNano import dwfImpedance

class dwfThread(threading.Thread):
    def __init__(self, main_ui, period, loop, freq):
        threading.Thread.__init__(self)

        self.main_ui = main_ui
        self.dwfim = main_ui.dwfim

        self.period = period
        self.loop = loop
        self.freq = freq

        self.cur_loop = 0
        self.stop_flag = False  # 스레드 종료 플래그

    def run(self):
        start_time = time.time()

        while self.loop != self.cur_loop:
            if self.stop_flag:  # 종료 플래그 확인
                print("Thread stopped")
                break

            cur_time = time.time()
            elapsed_time = cur_time - start_time

            # GUI 업데이트는 반드시 메인 스레드에서 처리
            self.main_ui.update_elapsed_time(elapsed_time)

            if elapsed_time >= self.period:
                start_time = cur_time
                self.measure_impedance(elapsed_time)
                self.cur_loop += 1

    def measure_impedance(self, elapsed_time):
        # 측정 작업 수행
        data0, data1 = self.dwfim.getScopeData(self.freq)
        zo = self.dwfim.calcImpedance(data0, data1)
        z = -self.main_ui.control_frame.get_ref() * zo

        # GUI 업데이트를 안전하게 메인 스레드에서 수행
        self.main_ui.update_measurements(data0, data1, z, self.cur_loop, elapsed_time)

    def stop(self):
        # 종료 플래그 설정
        self.stop_flag = True
