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

ab = np.zeros(20)

class Form(QDialog):
    def __init__(self, parent=None):
        global noE,ab
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi('dnaDropStats.ui',self)
        self.ui.show()
        f = open('initdata.txt')
        lines = f.readlines()
        self.ui.edtFreq.setText(lines[0])
        self.ui.edtRef.setText(lines[1])
        f.close()
        noE = 0
    
    def saveBtnClicked(self):
        global noE, ab, m, s, ms, ss
        f = open('record.txt','w')
        for i in range(noE):
            f.write('%0.4f\n'%(ab[i]))
        f.close()
        msg = QMessageBox()
        msg.setInformativeText('data are saved!')
        msg.exec_()

    def displayStats(self):
        global noE, ab, m, s, ms, ss
        if noE > 1:
            m = np.mean(ab[:noE])
            s = np.std(ab[:noE])
            cv = s/m*100
            self.ui.edtMean.setText('%0.4f'%m)
            self.ui.edtStd.setText('%0.4f'%s)
            self.ui.edtCv.setText('%0.4f'%(s/m*100))
            if noE > 4:
               sidx = np.argsort(abs(ab-m))
               sab=[ab[i] for i in sidx[:noE-2]]
               ms = np.mean(sab)
               ss = np.std(sab)
               scv = ss/ms*100            
               self.ui.edtSmean.setText('%0.4f'%ms)
               self.ui.edtSstd.setText('%0.4f'%ss)
               self.ui.edtScv.setText('%0.4f'%scv)
            else: 
               self.ui.edtSmean.clear()
               self.ui.edtSstd.clear()
               self.ui.edtScv.clear()
               ms = ss = scv = 0
               ss = 0
               scv = 0
        else:
            self.ui.edtMean.clear()
            self.ui.edtStd.clear()
            self.ui.edtCv.clear()
            m = 0
            s = 0
            cv = 0
            

    def cancelBtnClicked(self):
        global noE,ab
        ab[noE]=0
        noE = noE-1
        self.ui.edtExp.undo()
        self.ui.edtReal.undo()
        self.ui.edtImag.undo()
        self.ui.edtAbs.undo()
        self.displayStats()
        
    def measureBtnClicked(self):
        global noE,ab
        fr = int(self.ui.edtFreq.text())
        ref = float(self.ui.edtRef.text())
        freq = fr*1000
        noE = noE+1
        if ( noE > 15 ):
            msg = QMessageBox()
            msg.setInformativeText('max. exp. < 15')
            msg.exec_()
            noE = 15
        zo=dw.measureImpedance(freq)
        z=-ref*zo
        #z = noE*noE #for test
        ab[noE-1] = abs(z)
        self.ui.edtExp.append('%d'%(noE))
        self.ui.edtReal.append('%0.4f'%z.real)
        self.ui.edtImag.append('%0.4f'%z.imag)
        self.ui.edtAbs.append('%0.4f'%abs(z))
        self.displayStats()
    
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
