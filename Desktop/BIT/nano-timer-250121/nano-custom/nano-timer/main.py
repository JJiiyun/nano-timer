import sys
from PyQt5.QtWidgets import QApplication

from ui.main_ui import MainUI


app = QApplication(sys.argv)
main_ui = MainUI()
main_ui.show()
app.exec_()