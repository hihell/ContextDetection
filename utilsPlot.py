from __future__ import division

__author__ = 'jiusi'

import json
import numpy as np
import matplotlib.pyplot as plt
import utilsData as ud
from scipy.fftpack import fft, ifft, fftfreq
from itertools import combinations

# mesh
MARGIN = .5

def plotLines(list, axles, title=None):
    fig = plt.figure()

    dots = np.array([d['values'] for d in list])

    subplotNum = len(axles)
    subplotIndex = 1

    xAxle = range(0, len(dots))

    if 0 in axles:
        s0 = fig.add_subplot(subplotNum, 1, subplotIndex)
        # s0 = plt.subplot(subplotNum, 1, subplotIndex)
        if title:
            s0.set_title(title)
        s0.plot(xAxle, dots[:, 0], 'r.-')
        s0.set_xlabel('axis: 0')
        s0.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    if 1 in axles:
        s1 = fig.add_subplot(subplotNum, 1, subplotIndex)
        # s1 = plt.subplot(subplotNum, 1, subplotIndex)
        s1.plot(xAxle, dots[:, 1], 'b.-')
        s1.set_xlabel('axis: 1')
        s1.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    if 2 in axles:
        s2 = fig.add_subplot(subplotNum, 1, subplotIndex)
        # s2 = plt.subplot(subplotNum, 1, subplotIndex)
        s2.plot(xAxle, dots[:, 2], 'g.-')
        s2.set_xlabel('axis: 2')
        s2.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    plt.show()


def plotComplexList(complexNumberList):
    xAxle = range(0, len(complexNumberList))

    realList = [ele.real for ele in complexNumberList]
    imagList = [ele.imag for ele in complexNumberList]

    plt.subplot(2, 1, 1)
    plt.plot(xAxle, realList, 'b.')
    plt.axes([0, len(complexNumberList), -20, 20])

    plt.subplot(2, 1, 2)
    plt.plot(xAxle, imagList, 'g.')
    plt.axes([0, len(complexNumberList), -20, 20])

    plt.show()


def plotFTResult(original, result, time, W):
    realList = [ele.real for ele in result]
    imagList = [ele.imag for ele in result]

    print "max(realList):", max(realList)
    print "max(imagList):", max(imagList)

    plt.subplot(3, 1, 1)
    plt.plot(time, original, 'r.-')

    plt.subplot(3, 1, 2)
    plt.plot(W, realList, 'bx')

    plt.subplot(3, 1, 3)
    plt.plot(W, imagList, 'gx')

    plt.show()


def plotFile(filePath):
    f = filePath
    dataList = ud.readFile(f)
    accdata = ud.getDataBySensorType('accelerator', dataList)
    ud.betterPrintData(accdata)
    plotLines(accdata, [0,1,2], title=filePath)


# plotExample()

def plotAllDecisionBoundary(trainData, testData, classifier):
    dimension = range(0, len(trainData[0]))
    foils = [i for i in combinations(dimension, 2)]

    rows = 0
    columns = 2
    if len(foils) % 2 == 0:
        rows = len(foils) / 2
    else:
        rows = len(foils) + 1 / 2

    Z = classifier.predict(trainData)
    Z = np.c_[np.zeros(Z.size), Z]

    for i, foil in enumerate(foils):
        plt.subplot(columns, rows, i + 1)
        plt.subplots_adjust(wspace=0.4, hspace=0.4)


def plotDecisionBoundary(trainData, trainDataClass, testData, classifier, foil, axisNames=None, title=None):

    trainData = np.array(trainData)

    size = 1000
    h = .03
    cm = plt.cm.get_cmap('RdYlBu')

    # boundary of plot
    leftMost = trainData[:, foil[0]].min() -1
    rightMost = trainData[:, foil[0]].max() +1
    downMost = trainData[:, foil[1]].min() -1
    upMost = trainData[:, foil[1]].max() +1


    xx, yy = np.meshgrid(np.arange(leftMost, rightMost, h),
                         np.arange(downMost, upMost, h))

    z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    plt.contourf(xx, yy, z, cmap=cm, alpha=.8)
    plt.scatter(trainData[:, 0], trainData[: ,1], c=trainDataClass,  edgecolors='none', cmap=cm)

    plt.xlabel(axisNames[0])
    plt.ylabel(axisNames[1])

    if(title):
        plt.title(title)

    plt.show()