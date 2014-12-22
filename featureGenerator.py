__author__ = 'jiusi'

import numpy as np
from scipy.fftpack import fft, fftfreq

def getSpectrumFeature(fft_signal, W, dimension):
    indexes = fft_signal.argsort()[-dimension:][::-1]
    freqs = []
    for i in range(0, len(fft_signal)):
        if i in indexes:
            freqs.append(W[i])
    return indexes, freqs


def smoothAsIPulse(signal, pulseLen, gapLen):
    smoothed = []
    for i in range(0, len(signal) - 1):
        for p in range(0, pulseLen):
            smoothed.append(signal[i])
        for g in range(0, gapLen):
            smoothed.append(0)
    return smoothed


def processSignal(rawSensorData):
    # apply hamming window to original data
    ham = np.hamming(len(rawSensorData))
    time = np.linspace(start=0, stop=len(rawSensorData), num=len(rawSensorData))
    hammed = [h*s for h,s in zip(ham, rawSensorData)]

    # do Fourier Transform to processed data
    f_signal = fft(hammed)
    W = fftfreq(len(hammed), d=time[1]-time[0])

    return time, hammed, W, f_signal


def fftFeature(fft_signal, W, size):
    realList = np.array([ele.real for ele in fft_signal])
    imagList = np.array([ele.imag for ele in fft_signal])

    indexes = imagList.argsort()[-size:][::-1]
    freqs = []
    for i in range(0, len(fft_signal)):
        if i in indexes:
            freqs.append(W[i])

    ampls = [imagList[i] for i in indexes]

    rms = np.sqrt(np.mean(np.square(freqs)))
    var = np.var(freqs)
    return ampls, freqs, rms, var


def getMean(accData):
    values = np.array([ele['values'] for ele in accData])

    mx = np.average(values[:,0])
    my = np.average(values[:,1])
    mz = np.average(values[:,2])

    return np.array([mx, my, mz])

def getDirection(accData):
    mean = getMean(accData)
    return np.array(mean / np.linalg.norm(mean))

def regularizeSignal(accData):
    result = {}
    direction = getDirection(accData)
    regularized = []
    horizontalMagnitude = []
    verticalAmplitude = []

    values = np.array([ele['values'] for ele in accData])

    for a in values:

        amplitude = np.inner(a, direction)
        p = amplitude * direction
        regularized.append(p)

        h = a - p
        magnitude = np.linalg.norm(h)

        horizontalMagnitude.append(magnitude)
        verticalAmplitude.append(amplitude)


    result['regularized'] = regularized
    result['verticalAmplitude'] = verticalAmplitude
    result['horizontalMagnitude'] = horizontalMagnitude
    return result


def getFullFeatures(verticalAmplitude, horizontalMagnitude):
    meanV = np.average(verticalAmplitude)
    stdV = np.std(verticalAmplitude)
    p75V = np.percentile(verticalAmplitude, 75)
    p25V = np.percentile(verticalAmplitude, 25)
    iqrV = p75V - p25V
    meanH = np.average(horizontalMagnitude)
    stdH = np.std(horizontalMagnitude)
    coore = np.correlate(verticalAmplitude, horizontalMagnitude)
    if len(verticalAmplitude) != len(horizontalMagnitude):
        print 'warning, verticalAmplitude is not at the same length as horizontalMagnitude'

    return [meanV, stdV, p75V, iqrV, meanH, stdH, coore[0]]

