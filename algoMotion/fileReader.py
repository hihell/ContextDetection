from __future__ import division
from algoMotion import utilsPlot

__author__ = 'jiusi'


import json

import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import fft, fftfreq
from sklearn import svm, cross_validation


def printNorm(list):
    for ele in list:
        x = ele['data'][0]
        y = ele['data'][1]
        z = ele['data'][2]

        print np.linalg.norm([x,y,z])

def readFile(filePath):
    with open(filePath) as f:
        jlist = [line.rstrip() for line in f]
        return [json.loads(j) for j in jlist]


def drawDots(list, axles):
    dots = np.array([d['values'] for d in list])
    subplotNum = len(axles)
    subplotIndex = 1

    xAxle = range(0, len(dots))

    if 0 in axles:
        plt.subplot(subplotNum, 1, subplotIndex)
        plt.plot(xAxle, dots[:,0], 'r.-')
        plt.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    if 1 in axles:
        plt.subplot(subplotNum, 1, subplotIndex)
        plt.plot(xAxle, dots[:,1], 'b.-')
        plt.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    if 2 in axles:
        plt.subplot(subplotNum, 1, subplotIndex)
        plt.plot(xAxle, dots[:,2], 'g.-')
        plt.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    plt.show()


def getListsFromFile(filePath):
    with open(filePath) as json_data:
        d = json.load(json_data)
        json_data.close()

    aList = [ele for ele in d if ele['source'] == 'acc']
    laList = [ele for ele in d if ele['source'] == 'linacc']
    gList = [ele for ele in d if ele['source'] == 'gyro']

    return aList, laList, gList

def getListsFromList(list):
    if 'sensorName' in list[0]:
        key = 'sensorName'
        aList = [ele for ele in list if ele[key] == 'acc']
        laList = [ele for ele in list if ele[key] == 'linacc']
        gList = [ele for ele in list if ele[key] == 'gyro']
        return aList, laList, gList
    elif 'source' in list[0]:
        key = 'source'
        aList = [ele for ele in list if ele[key] == 'accelerometer']
        # old log does not have fused linear acceleration
        gList = [ele for ele in list if ele[key] == 'Gyroscope']
        return aList, None, gList
    else:
        print 'fucked!'


def getXYZ(list):
    if 'data' in list[0]:
        key = 'data'
    elif 'values' in list[0]:
        key = 'values'
    else:
        print "error, list is not correct"

    X = []
    Y = []
    Z = []

    for ele in list:
        X.append(ele[key][0])
        Y.append(ele[key][1])
        Z.append(ele[key][2])

    return X, Y, Z

def checksort(list):
    last = float("-infinity")
    for ele in list:
        if last <= ele['timestamp']:
            last = ele['timestamp']
        else:
            print 'err'
            return

    print 'the list sorted'


def wave():
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

def smooth(signal, gap, density):
    smoothed = []
    for i in range(0, len(signal)-1):
        k = (signal[i + 1] - signal[i]) / gap
        smoothed.append(signal[i])
        for j in range(1, density):
            filler = j/density * gap * k + signal[i]
            smoothed.append(filler)
    return smoothed

def smoothAsIPulse(signal, pulseLen, gapLen):
    smoothed = []
    for i in range(0, len(signal) - 1):
        for p in range(0, pulseLen):
            smoothed.append(signal[i])
        for g in range(0, gapLen):
            smoothed.append(0)
    return smoothed

# signal = [0, 10, 0, 10, 0, 10, 0, 10]


def getFeature(fft_signal, W, size):

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




def readOld(filePath):
    l = readFile(filePath)
    return l[0]

def readNew(filePath):
    return readFile(filePath)

def splitTraniningData(data, pieceNum):
    if len(data) % pieceNum == 0:
        pieceSize = len(data) // pieceNum
    else:
        pieceSize = len(data) // pieceNum + 1

    result = []
    count = 0
    for i in range(0, pieceNum):
        piece = []
        for j in range(0, pieceSize):
            if count < len(data):
                piece.append(data[count])
                count += 1
        result.append(piece)
    return result


def plotFFT(data):
    # ham = np.hamming(len(data))
    #
    # time = np.linspace(start=0, stop=len(data), num=len(data))
    #
    # signal = [h*s for h,s in zip(ham, data)]
    #
    # f_signal = fft(signal)
    #
    # W = fftfreq(len(signal), d=time[1]-time[0])


    # ampls, freqs = getFeature(f_signal, W, 3)
    # print 'ampls:', ampls
    # print 'freqs:', freqs

    time, hammed, W, f_signal = processSignal(data)
    utilsPlot.plotFTResult(hammed, f_signal, time, W)

def processSignal(signal):
    ham = np.hamming(len(signal))
    time = np.linspace(start=0, stop=len(signal), num=len(signal))
    hammed = [h*s for h,s in zip(ham, signal)]
    f_signal = fft(hammed)
    W = fftfreq(len(hammed), d=time[1]-time[0])

    return time, hammed, W, f_signal


def getFeatureFromSignal(signal):
    time, hammed, W, f_signal = processSignal(signal)
    ampls, freqs, rms, var = getFeature(f_signal, W, 3)
    return [freqs[0], ampls[0], rms, var]


sitting = '/Users/jiusi/oldlog/sitting.txt'
sitting_data = readOld(sitting)
#
walking ='/Users/jiusi/walking1211.txt'
walking_data = readNew(walking)

alist, lin, glist = getListsFromList(sitting_data)
x,y,z = getXYZ(alist)

sittingList = np.array(splitTraniningData(x, 10))

d1 = []
for sd in sittingList:
    d1.append(getFeatureFromSignal(sd))
d1 = np.array(d1)

c1 = np.empty(len(sittingList))
c1.fill(0)

alist, lin, glist = getListsFromList(walking_data)
x,y,z = getXYZ(alist)

walkingList = np.array(splitTraniningData(y, 10))
d2 = []
for wd in walkingList:
    d2.append(getFeatureFromSignal(wd))
d2 = np.array(d2)

c2 = np.empty(len(walkingList))
c2.fill(1)

training = np.append(d1, d2, axis=0)
target = np.append(c1, c2, axis=0)

print 'average rms d1:', np.average([ele[2] for ele in d1])
print 'average rms d2:', np.average([ele[2] for ele in d2])

print 'average var d1:', np.average([ele[3] for ele in d1])
print 'average var d2:', np.average([ele[3] for ele in d2])

print 'average top freq d1:', np.average([ele[0] for ele in d1])
print 'average top freq d2:', np.average([ele[0] for ele in d2])

print 'average top freq ampli d1:', np.average([ele[1] for ele in d1])
print 'average top freq ampli d2:', np.average([ele[1] for ele in d2])


# for i in range(0, len(walkingList)):
#     sitting_data = sittingList[i]
#     data = smoothAsIPulse(sitting_data, pulseLen=3, gapLen=20)
#     plotFFT(data)

clf = svm.SVC(kernel='rbf', C=1)

# plotUtils.testColormesh(clfVH, [0,1])

scores = cross_validation.cross_val_score(clf, training, target, cv=5)

print scores