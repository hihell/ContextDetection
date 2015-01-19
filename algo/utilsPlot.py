from __future__ import division
from algo import utilsData as ud

__author__ = 'jiusi'

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from itertools import combinations

import parameters as param
import featureGenerator as fg

# Data manipulation:

activeCode = param.STAT_CLASS_NAME['Active']
inactiveCode = param.STAT_CLASS_NAME['Inactive']

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
        color = param.statusColors[statusCode]
        marker = param.statusMarkers[statusCode]

        s0.scatter(bucket[:, 2], bucket[:, 0], c=color, label=label, marker='.', edgecolors='none')
        s1.scatter(bucket[:, 2], bucket[:, 1], c=color, label=label, marker='.', edgecolors='none')

    s0.legend(loc='upper right')
    fig.show()


def plotVHComparisonByStatus(filePaths, statusCode, GRAN_SAMPLE):

    VH = []
    vhTags = []

    separation = 0

    for filePath in filePaths:

        buckets, y = ud.processFile(filePath, GRAN_SAMPLE)
        buckets = [data for data, tag in zip(buckets, y) if tag == statusCode]

        for bucket in buckets:
            regu = fg.regularizeSignal(bucket)
            verA = regu['verticalAmplitude']
            horM = regu['horizontalMagnitude']

            tag = param.STAT_DICT[bucket[0]['status']]

            for v, h in zip(verA, horM):
                VH.append([v, h])
                vhTags.append(tag)

        if separation == 0:
            print 'separation:', separation
            separation = len(VH)

    VH = np.array(VH)
    vhTags = np.array(vhTags)

    fig = plt.figure()

    s0 = fig.add_subplot(2, 1, 1)
    s0.set_xlabel('vertical amplitude')
    s0.set_title('|'.join(filePaths) + ' status:' + ud.getStatusByCode(statusCode))
    s1 = fig.add_subplot(2, 1, 2)
    s1.set_xlabel('horizontal magnitude')

    xAxle = range(0, len(vhTags))

    s0.scatter(
        xAxle,
        VH[:, 0],
        c=param.statusColors[statusCode],
        marker='.',
        edgecolors='none')

    s0.axvline(x=separation)

    s1.scatter(
        xAxle,
        VH[:, 1],
        c=param.statusColors[statusCode],
        marker='.',
        edgecolors='none')

    s1.axvline(x=separation)

    plt.show()


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


def plotFile(filePath, sensor='accelerometer', status=None):
    f = filePath
    dataList = ud.readFile(f)
    accdata = ud.getDataBySensorType(sensor, dataList)
    print ud.getDataListStatus(accdata)

    if status:
        accdata = [data for data in accdata if data['status'] == status]

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

    if len(X[0]) > 2:
        print 'data dimension larger than 2, abort plot decision boundary'
        return

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
        color = param.statusColors[label]
        marker = param.statusMarkers[label]

        bucket = []
        for data, dataLabel in zip(X, y):
            if dataLabel == label:
                bucket.append(data)
        bucket = np.array(bucket)

        plt.scatter(bucket[:, 0],
                    bucket[:, 1],
                    c = color,
                    label = status,
                    marker='o',
                    edgecolors='none'
                    )

    plt.legend(loc = 'upper left')

    plt.xlabel(axisNames[0])
    plt.ylabel(axisNames[1])


    if(title):
        plt.title(title)

    plt.show()

def plotConfusionMatrix(cm):

    print param.STAT_DICT
    print(cm)

    plt.matshow(cm)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def plotConfusionMatrix(trueTag, predTag, title):
    cm = np.zeros(shape=(len(param.STAT_CODE), len(param.STAT_CODE)))
    for i, j in zip(trueTag, predTag):
        cm[i][j] += 1

    print cm

    fig = plt.figure()
    fig.suptitle(title)
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm, interpolation='nearest')
    fig.colorbar(cax)

    ax.set_xlabel('predict status')
    ax.set_ylabel('true status')
    ax.set_xticklabels(['']+param.STAT_NAME)
    ax.set_yticklabels(['']+param.STAT_NAME)

    plt.show()

def plotConfusionMatrixSS(y, p):
    plotConfusionMatrix(y, p, 'total prediction')

    y1 = [param.STAT_CLASS_MAP[i] for i in y if i in param.STAT_CLASS_MAP]
    p1 = [param.STAT_CLASS_MAP[i] for i in p if i in param.STAT_CLASS_MAP]

    print "layer 1 prediction correct rate:", ud.getCorrectRate(y1, p1)
    plotConfusionMatrix(y1, p1, 'layer1 prediction')

    y2a = []
    p2a = []
    y2in = []
    p2in = []
    for trueTag, pred in zip(y, p):
        if param.STAT_CLASS_MAP[trueTag] == activeCode:
            y2a.append(trueTag)
            p2a.append(pred)
        elif param.STAT_CLASS_MAP[trueTag] == inactiveCode:
            y2in.append(trueTag)
            p2in.append(pred)


    if len(y2a) > 0:
        print "layer 2 a active prediction correct rate:", ud.getCorrectRate(y2a, p2a)
        plotConfusionMatrix(y2a, p2a, 'layer 2 active prediction')

    if len(y2in) > 0:
        print "layer 2 a inactive prediction correct rate:", ud.getCorrectRate(y2in, p2in)
        plotConfusionMatrix(y2in, p2in, 'layer 2 inactive prediction')




