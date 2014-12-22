from __future__ import division

__author__ = 'jiusi'

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq
from itertools import combinations


def plotLines(list, axles):
    dots = np.array([d['values'] for d in list])

    subplotNum = len(axles)
    subplotIndex = 1

    xAxle = range(0, len(dots))

    if 0 in axles:
        plt.subplot(subplotNum, 1, subplotIndex)
        plt.plot(xAxle, dots[:, 0], 'r.-')
        plt.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    if 1 in axles:
        plt.subplot(subplotNum, 1, subplotIndex)
        plt.plot(xAxle, dots[:, 1], 'b.-')
        plt.axis([0, len(dots), -20, 20])
        subplotIndex += 1

    if 2 in axles:
        plt.subplot(subplotNum, 1, subplotIndex)
        plt.plot(xAxle, dots[:, 2], 'g.-')
        plt.axis([0, len(dots), -20, 20])
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


def plotClassResult(dataSet, clf, classes):
    print 'dimension:', dataSet[0][0].size
    print 'results will be projected to 2 dimensional plane'




    # dimension = range(0, len(dataSet[0]))
    # foils = [i for i in combinations(dimension, 2)]
    #
    # rows = 0
    # columns = 2
    # if len(foils) % 2 == 0:
    #     rows = len(foils) / 2
    # else:
    #     rows = len(foils) + 1 / 2
    #
    # Z = clf.predict(dataSet)
    # Z = np.c_[np.zeros(Z.size), Z]
    #
    #
    # for i, foil in enumerate(foils):
    #     plt.subplot(columns, rows, i + 1)
    #     plt.subplots_adjust(wspace=0.4, hspace=0.4)
    #


def testColormesh(clf, classes):
    size = 1000
    h = .2
    cm = plt.cm.RdBu

    dataSet = []
    for i in range(0, size):
        dataSet.append([np.random.uniform(-20, 20), np.random.uniform(-20, 20)])
    dataSet = np.array(dataSet)
    # dataSet.reshape(size/2, 2)

    Z = clf.predict(dataSet)

    plt.scatter(dataSet[:, 0], dataSet[: ,1], c=Z,  edgecolors='none', cmap=plt.cm.Accent)

    xx, yy = np.meshgrid(np.arange(-20, 20, h),
                         np.arange(-20, 20, h))

    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    plt.contourf(xx, yy, z, cmap=cm, alpha=.8)

    plt.show()

