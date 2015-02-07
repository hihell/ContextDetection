__author__ = 'jiusi'

import parameters as param
import numpy as np

import xmlReader
import scipy.io.wavfile as wave


def getData(dataSetDict):
    classDict, fileDict = xmlReader.readXML(param.xmlPath)

    print "total data base files:", len(fileDict)

    fileNames = [name for name in dataSetDict]
    fileIDs = range(0, len(fileNames))

    fileNameIDMap = {}
    for name, id in zip(fileNames, fileIDs):
        fileNameIDMap[name] = id

    fileGroupedSig = []
    fileGroupedL2 = []
    rate = 0

    print "total train files:", len(fileNames)

    for name in fileNames:
        filePath = param.audioRoot + fileDict[name]['fileNameLeft']
        rate, sig = wave.read(filePath)
        fileGroupedSig.append(sig)
        L2Code = dataSetDict[name]['L2']
        fileGroupedL2.append(L2Code)


    return rate, fileGroupedSig, fileGroupedL2


def sigToFrames(rate, sig, frameTime):
    frameSize = rate * frameTime
    trimmed = sig[0:(len(sig) - len(sig) % frameSize)]
    trimmed = np.array(trimmed)
    frames = trimmed.reshape(len(trimmed) / frameSize, frameSize)

    return frames

