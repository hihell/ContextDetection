from __future__ import division

__author__ = 'jiusi'

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pltColors
import utilsData as ud
from scipy.fftpack import fft, ifft, fftfreq
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from itertools import combinations


# mesh
MARGIN = .5

# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white
statusColors = ['b', 'g', 'r', 'y', 'm']
statusMarkers =['+', 'x', 'o', 'd', '<']



# Data manipulation:

def make_segments(x, y):
    '''
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    '''

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    return segments


# Interface to LineCollection:

def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0):
    '''
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    '''

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc


def plotAccLines(list, axles, title=None):
    dots = np.array([d['values'] for d in list])
    plotLines(dots, axles, title)


def plotVH(VH, y, title=None):

    if not isinstance(VH, np.ndarray):
        VH = np.array(VH)

    VH = np.insert(VH, 2, range(0, len(y)), axis=1)

    fig = plt.figure()

    s0 = fig.add_subplot(2, 1, 1)
    s0.set_xlabel('vertical amplitude')
    s0.set_title(title)
    s1 = fig.add_subplot(2, 1, 2)
    s1.set_xlabel('horizontal magnitude')

    for statusCode in np.unique(y):
        bucket = []

        for vh, code in zip(VH, y):
            if code == statusCode:
                bucket.append(vh)
        bucket = np.array(bucket)
        label = ud.getStatusByCode(statusCode)
        color = statusColors[statusCode]
        marker = statusMarkers[statusCode]

        s0.scatter(bucket[:, 2], bucket[:, 0], c=color, label=label, marker=marker)
        s1.scatter(bucket[:, 2], bucket[:, 1], c=color, label=label, marker=marker)

    s0.legend(loc='upper right')
    fig.show()


def plotLines(dots, axles, title=None, color=None):
    fig = plt.figure()

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
    accdata = ud.getDataBySensorType('accelerometer', dataList)
    ud.betterPrintData(accdata)
    plotAccLines(accdata, [0,1,2], title=filePath)


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



def plotDecisionBoundary(X, y, clf, foil, axisNames=None, title=None):

    X = np.array(X)

    size = 1000
    h = .03
    cm = plt.cm.get_cmap('RdYlBu')

    # boundary of plot
    leftMost = X[:, foil[0]].min() -1
    rightMost = X[:, foil[0]].max() +1
    downMost = X[:, foil[1]].min() -1
    upMost = X[:, foil[1]].max() +1

    xx, yy = np.meshgrid(np.arange(leftMost, rightMost, h),
                         np.arange(downMost, upMost, h))

    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    plt.contourf(xx, yy, z, cmap=cm, alpha=.8)

    # plt.scatter(trainData[:, 0], trainData[:, 1], c=trainDataClass, label=trainDataClass, cmap=cm)
    # plt.legend(loc='upper right')
    labels = np.unique(y)
    for label in labels:
        status = ud.getStatusByCode(label)
        color = statusColors[label]
        marker = statusMarkers[label]

        bucket = []
        for data, dataLabel in zip(X, y):
            if dataLabel == label:
                bucket.append(data)
        bucket = np.array(bucket)

        plt.scatter(bucket[:, 0],
                    bucket[:, 1],
                    c = color,
                    label = status,
                    marker=marker
                    )

    plt.legend(loc = 'upper left')

    plt.xlabel(axisNames[0])
    plt.ylabel(axisNames[1])


    if(title):
        plt.title(title)

    plt.show()

