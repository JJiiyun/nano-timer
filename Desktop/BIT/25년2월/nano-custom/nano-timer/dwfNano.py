"""
NanoDropper library
"""
from ctypes import * # C로 작성한 .so, .dll을 이용할 수 있도록 해주는 라이브러리.
import time
import threading
import cmath as cm
import numpy as np


from dwfconstants import *
import fitSine as fs

dwf = cdll.dwf # waveform 사용

#declare ctype variables; 
hdwf = c_int()
sts = c_byte()

class dwfImpedance:
    def __init__(self):
        self._dwf_init()

        self.rg0Samples = (c_double*self.buf_len)()
        self.rg1Samples = (c_double*self.buf_len)()



    def _dwf_init(self):
        # Open device
        dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

        if hdwf.value == hdwfNone.value:
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            print(szerr.value)
            print("failed to open device(AD2 connecting required.)")
            quit()

        self._set_power_supply(V=5)

        self._set_function_generator(amplitude=1, offset=0)

        self._set_analog_input(T=1024, nT=2)

        self._set_digital_output(mask=0x001F)
    
    

    def _set_power_supply(self, V=5):
        # enable positive supply
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(True)) 
        # set voltage
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(V)) 
        # enable negative
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(0), c_double(True)) 
        # set voltage to
        dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(1), c_double(-V))
        # master enable
        dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))


    def _set_function_generator(self, amplitude=1, offset=0):
        # enable just one channel
        dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(True))

        # configure enabled channels
        dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcSine)
        dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(amplitude)) #1V amplitude
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(offset))  #0V offset
        time.sleep(1) # needed time sleep 1 sec

    def _set_analog_input(self, T=1024, nT=2):
        self.T, self.nT = T, nT
        self.buf_len = T*nT

        dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(2*self.buf_len)) 
        dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
        dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(0.5))
        dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))
        dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(0.5))

        #set up trigger
        dwf.FDwfAnalogInTriggerAutoTimeoutSet(hdwf, c_double(0)) #disable auto trigger
        dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcDetectorAnalogIn) #one of the analog in channels
        dwf.FDwfAnalogInTriggerTypeSet(hdwf, trigtypeEdge)
        dwf.FDwfAnalogInTriggerChannelSet(hdwf, c_int(0)) # first channel
        dwf.FDwfAnalogInTriggerLevelSet(hdwf, c_double(0)) # 0V
        dwf.FDwfAnalogInTriggerConditionSet(hdwf, trigcondRisingPositive) 

    def _set_digital_output(self,mask=0x001F):
        dwf.FDwfDigitalIOOutputEnableSet(hdwf, c_int(mask))

    def portSel(self, channel):
        port = channel*2+1
        dwf.FDwfDigitalIOOutputSet(hdwf, c_int(port))

    def getScopeData(self, fr):
        dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(fr))
        # now enable function generator and wait stabilization
        dwf.FDwfAnalogOutConfigure(hdwf,c_int(0), c_bool(True))
        time.sleep(0.5)
        af = c_double()
        dwf.FDwfAnalogOutNodeFrequencyGet(hdwf, c_int(0), AnalogOutNodeCarrier, byref(af))
        #sampling frequency calculation, set 2*period less than self.buf_len
        vlen = self.buf_len+1
        tT = self.T+1
        while vlen > self.buf_len:
            tT = tT-1
            sf = af.value*tT
            asf = c_double()
            dwf.FDwfAnalogInFrequencySet(hdwf, c_double(sf))
            dwf.FDwfAnalogInFrequencyGet(hdwf, byref(asf))
            vlen = int(2*asf.value/af.value)
        #begin acquisition and wait for completion
        dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(True))
        sts = c_byte()
        while True:
            dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value :
                    break
            time.sleep(0.1)
        #get data
        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), self.rg0Samples, self.buf_len)
        dwf.FDwfAnalogInStatusData(hdwf, c_int(1), self.rg1Samples, self.buf_len)

        data0=list(self.rg0Samples[1:vlen])
        data1=list(self.rg1Samples[1:vlen])
        return data0, data1

    def calcImpedance(self, data0, data1):
        R0, T0, M0 = fs.sineFit2Cycle(data0, self.nT)
        R1, T1, M1 = fs.sineFit2Cycle(data1, self.nT)

        if R0 < 0:
            R0 = -R0
            T0 = T0-np.pi
        if R1 < 0:
            R1 = -R1
            T1 = T1-np.pi

        g = R1/R0
        p = T1-T0
        if p > np.pi:
            p -= np.pi*2
                
        z = cm.rect(g,p)
        return z