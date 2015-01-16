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


def smoothAsPulse(signal, pulseLen, gapLen):
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


def getVHFullFeatures(verticalAmplitude, horizontalMagnitude):
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
#           0      1     2     3     4      5     6

def getSomeFeatures(verticalAmplitude, horizontalMagnitude, featureList):
    fl = getVHFullFeatures(verticalAmplitude, horizontalMagnitude)
    return [fl[i] for i in featureList]

def getFeatureByVH(VH, featureList):
    X = []
    for vh in VH:
        x = getSomeFeatures(
            verticalAmplitude=vh[0],
            horizontalMagnitude=vh[1],
            featureList=featureList
            )
        X.append(x)
    return X

def getFeatureBySS(SS):
    X = []
    for ss in SS:
        x = getSSFullFeatures(ss)
        X.append(x)
    return X

def getSSFullFeatures(sqrWindow):
    winSize = len(sqrWindow)

    sqrWindow = np.array(sqrWindow)

    mean = np.average(sqrWindow)
    std = np.std(sqrWindow)
    min = np.min(sqrWindow)
    max = np.max(sqrWindow)
    p10 = np.percentile(sqrWindow, 10)
    p25 = np.percentile(sqrWindow, 25)
    p50 = np.percentile(sqrWindow, 50)
    p75 = np.percentile(sqrWindow, 75)
    p90 = np.percentile(sqrWindow, 90)

    sorted = np.sort(sqrWindow)

    i5 = int(winSize * .05)
    sb5 = sum(sorted[:i5])
    ssb5 = sum(sorted[:i5] ** 2)

    i10 = int(winSize * .1)
    sb10 = sum(sorted[:i10])
    ssb10 = sum(sorted[:i10] ** 2)

    i25 = int(winSize * .25)
    sb25 = sum(sorted[:i25])
    ssb25 = sum(sorted[:i25] ** 2)

    i75 = int(winSize * .75)
    sa75 = sum(sorted[i75:])
    ssa75 = sum(sorted[i75:] ** 2)

    i90 = int(winSize * .9)
    sa90 = sum(sorted[i90:])
    ssa90 = sum(sorted[i90:] ** 2)

    i95 = int(winSize * .95)
    sa95 = sum(sorted[i95:])
    ssa95 = sum(sorted[i95:] ** 2)

    return [
        mean,
        std,
        min,
        max,
        p10,
        p25,
        p50,
        p75,
        p90,
        sb5, ssb5,
        sb10,ssb10,
        sb25, ssb25,
        sa75, ssa75,
        sa90, ssa90,
        sa95, ssa95
    ]



def accToVH(buckets):
    VH = []
    for bucket in buckets:
        regu = regularizeSignal(bucket)
        verA = regu['verticalAmplitude']
        horM = regu['horizontalMagnitude']

        VH.append([verA, horM])

    return VH

def accToSqrSum(buckets):

    ssBuckets = []
    for bucket in buckets:
        ssBucket = []
        for data in bucket:
            acc = data['values']
            sqrSum = np.sqrt(np.dot(acc, acc))
            ssBucket.append(sqrSum)
        ssBuckets.append(ssBucket)
    return ssBuckets