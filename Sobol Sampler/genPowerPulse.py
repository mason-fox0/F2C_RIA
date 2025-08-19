#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 13:01:13 2023

@author: mfox48
"""

import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt

def main():
    cal_g = 150
    pw = 30E-3 #sec
    fuelDensity = 10431.5 #kg/m^3 
    l = 0.1 #m
    r = 4.096e-3 #m
    V = math.pi * l * r**2
    
    pwr_tuple = genPowerCurve(cal_g, pw, V, fuelDensity, 250)
    time_unzip, pwr_unzip = zip(*pwr_tuple)

    for i, time in enumerate(time_unzip):
        simtime = round(time,5)
        pwr = round(pwr_unzip[i],2) 
        print(str(simtime) + ',' + str(pwr))

def genPowerCurve(cal_g:float, pulseWidth:float, volume:float, fuelDens:float, numPts:int):
    mass_kg = volume * fuelDens 
    empirical_correction_factor = 1.0296 #correction factor -- ordered and integrated power off by 2.96 pct consistently
    cal = cal_g * mass_kg * 1000 * empirical_correction_factor    #cal/test capsule
    joules = (cal * 4.184) # bison_correction_factor     #convert to Joules = Watts*sec
    pw = pulseWidth        
    
    timeList = list(np.linspace(0, 8*pw, numPts)) #8 pulsewidths captures enough of the curve
    
    pwr = powerPulse(pw, joules, timeList, fuelDens)
    pwr = [p/volume for p in pwr] #divide by volume

    timeList = [time + 10 for time in timeList]
    #make sure transient doesn't start before 10 sec 
    timeList.insert(0,9.99)
    timeList.insert(0,0.0)
    pwr.insert(0,0.0)
    pwr.insert(0,0.0)
    
    #make power generation go to zero after transient 
    timeList.append(timeList[-1]+0.1)
    pwr.append(0.0)

    t_pwr = tuple(zip(timeList, pwr))
    return(t_pwr) 

def powerPulse(pulseWidth:float, integral:float, time:list, fuelDens:float) -> tuple:
    #pulseWidth -- seconds
    #integral -- Joules
    #time -- list of time statepoints
    #fuelDens -- kg/m^3

    k = pulseWidth / ((2*math.acosh(math.sqrt(2))))
    amp = integral/(2*k)
    pulse = []
    timeLast = time[-1]

    for t in time:
        pulse.append(amp*(1/math.cosh((t-(timeLast/2))/k))**2)
    return pulse
    
if __name__ == '__main__':
    main()
