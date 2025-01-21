import sys
from PyQt5 import QtGui, uic, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
#from PyQt4.QtGui import *
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt

import dwfNano as dw
import numpy as np
from ctypes import *
import fitSine as fs
import cmath as cm


class Form(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi('dnaDrop.ui',self)
        self.ui.show()
        f = open('initdata.txt')
        lines = f.readlines()
        self.ui.edtFreq.setText(lines[0])
        self.ui.edtRef.setText(lines[1])
        f.close()
    
    def measureBtnClicked(self):
        fr = int(self.ui.edtFreq.text())
        ref = float(self.ui.edtRef.text())
        freq = fr*1000
        zo=dw.measureImpedance(freq)
        z=-ref*zo
        self.ui.edtReal.setText('%0.4f'%z.real)
        self.ui.edtImag.setText('%0.4f'%z.imag)
        self.ui.edtAbs.setText('%0.4f'%abs(z))
    
    def graphBtnClicked(self):
        fr = int(self.ui.edtFreq.text())
        freq = fr*1000
        d0, d1 = dw.getScopeData(freq)
        plt.plot(d0)
        plt.plot(d1)
        plt.show()
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    font=QtGui.QFont('Times New Roman', 12) #, QFont.Bold)
    app.setFont(font)

    w = Form()
    sys.exit(app.exec_())
