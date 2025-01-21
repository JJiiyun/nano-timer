#now fitting the sine function
import numpy as np
import cmath

def lockinSine2Cycle(ref,data,nT):
    N=len(data)
    s0=ref-np.mean(ref)
    M=np.mean(data)
    s1=data-M
    re=np.dot(s0,s1)/N*2
    sft=N/nT/4 #impedance estimation is slightly less than fitting
    sf=np.roll(s0,sft)
    im=np.dot(sf,s1)/N*2
    z=re+1j*im
    ph = np.angle(z)
    A=abs(z)
    return A, ph, M