"""
NanoDropper library
"""
from ctypes import *
from dwfconstants import *
import math
import cmath as cm
import time
import numpy as np
import sys

import fitSine as fs
import lockinSine as ls

#if sys.platform.startswith("win"):
dwf = cdll.dwf

#declare ctype variables
hdwf = c_int()
sts = c_byte()

#open device
print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    print("failed to open device")
    quit()

print("Power supply enable")
# enable positive supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(0), c_double(True)) 
# set voltage to 5 V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(0), c_int(1), c_double(5)) 
# enable negative supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(0), c_double(True)) 
# set voltage to -5 V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, c_int(1), c_int(1), c_double(-5)) 
# master enable
dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))

print("Function generator enable")
# enable just one channel
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(True))

# configure enabled channels
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcSine)
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(1)) #1V amplitude
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(0))  #0V offset
time.sleep(1)

T=1024
nT = 2 #number of cycles in data buffer
BUFLEN = T*nT

dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(2*BUFLEN)) 
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

rg0Samples = (c_double*BUFLEN)() # buffer for source channel
rg1Samples = (c_double*BUFLEN)() # buffer for destination channel

# enable output/mask on 8 LSB IO pins, from DIO 0 to 7
dwf.FDwfDigitalIOOutputEnableSet(hdwf, c_int(0x001F))

print( "Ready to use: measureImpedance, getScopeData, portSel ... ")

def portSel(channel):
    port = channel*2+1
    print(port)
    dwf.FDwfDigitalIOOutputSet(hdwf, c_int(port))   

def measureImpedance(freq): 
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(freq))
    # now enable function generator and wait stabilization
    dwf.FDwfAnalogOutConfigure(hdwf,c_int(0), c_bool(True))
    time.sleep(0.5)
    af = c_double()
    dwf.FDwfAnalogOutNodeFrequencyGet(hdwf, c_int(0), AnalogOutNodeCarrier, byref(af))
    #sampling frequency calculation, set 2*period less than BUFLEN
    vlen = BUFLEN+1
    tT = T+1
    while vlen > BUFLEN:
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

    # now disable function generator
    dwf.FDwfAnalogOutConfigure(hdwf,c_int(0), c_bool(False))

    #get data
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rg0Samples, BUFLEN)
    dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg1Samples, BUFLEN)

    #sine matching
    data0=list(rg0Samples[1:vlen])
    data1=list(rg1Samples[1:vlen])
    R0, T0, M0 = fs.sineFit2Cycle(data0,nT)
    R1, T1, M1 = fs.sineFit2Cycle(data1,nT)

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
    print(z)
    return z

def getScopeData(fr):
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(fr))
    # now enable function generator and wait stabilization
    dwf.FDwfAnalogOutConfigure(hdwf,c_int(0), c_bool(True))
    time.sleep(0.5)
    af = c_double()
    dwf.FDwfAnalogOutNodeFrequencyGet(hdwf, c_int(0), AnalogOutNodeCarrier, byref(af))
    #sampling frequency calculation, set 2*period less than BUFLEN
    vlen = BUFLEN+1
    tT = T+1
    while vlen > BUFLEN:
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
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rg0Samples, BUFLEN)
    dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg1Samples, BUFLEN)

    data0=list(rg0Samples[1:vlen])
    data1=list(rg1Samples[1:vlen])
    return data0, data1