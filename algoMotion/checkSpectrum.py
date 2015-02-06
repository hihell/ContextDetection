from __future__ import division
from algoMotion import utilsPlot

__author__ = 'jiusi'

import numpy as np

from scipy.fftpack import fft, fftfreq


def rectangleWave():
    time = np.linspace(0, 100, 100)
    signal = []
    stepLen = 10
    j = 0
    for i in range(0, len(time)):
        if j < stepLen / 2:
            signal.append(0)
        elif j >= stepLen / 2 and j < stepLen:
            signal.append(10)
        elif j == stepLen:
            j = 0
            signal.append(0)
        j+=1
    return time, signal

def highFreqWave():
    time = np.linspace(0,100, 1000)
    signal = []
    last = 0
    for i in range(0, len(time)):
        signal.append(last)
        if last == 10:
            last = 0
        else:
            last = 10
    return time, signal

def pulse():
    time = np.linspace(0, 100, 1000)
    signal = []
    stepLen = 20
    pulseLen = 20
    j = 0
    for i in range(0, len(time)):
        if j < stepLen:
            signal.append(0)
        elif j >= stepLen and j < stepLen+pulseLen:
            signal.append(10)
        elif j == stepLen+pulseLen:
            j = 0
            signal.append(0)
        j+=1
    return time, signal


def smooth(signal, gap, density):
    smoothed = []
    for i in range(0, len(signal)-1):
        k = (signal[i + 1] - signal[i]) / gap
        smoothed.append(signal[i])
        for j in range(1, density):
            filler = j/density * gap * k + signal[i]
            smoothed.append(filler)
    return smoothed

# time, signal = rectangleWave()
# time, signal = highFreqWave()
time, signal = pulse()

fftsignal = fft(signal)
print fftsignal

realsignal = np.array([ele.real for ele in fftsignal])
imagsignal = np.array([ele.imag for ele in fftsignal])

W = fftfreq(len(signal), d=time[1]-time[0])
print W

# plt.plot(W, fftsignal)
# plt.show()

indexes, freqs = fg.getSpectrumFeature(realsignal, W, 3)
print 'real'
print 'indexes:', indexes
print 'freqs:', freqs

indexes, freqs = fg.getSpectrumFeature(imagsignal, W, 3)
print 'imag'
print 'indexes:', indexes
print 'freqs:', freqs

utilsPlot.plotFTResult(signal, fftsignal, time, W)


