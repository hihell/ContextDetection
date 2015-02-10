__author__ = 'jiusi'

import os

import parameters as param
import numpy as np

import audioDBReader
import scipy.io.wavfile as wave

from pydub import AudioSegment

def getData(dataSetDict):
    classDict, fileDict = audioDBReader.readJson(param.jsonPath)

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

        rate, sig = getDataFromPath(filePath)

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


def printAudioParams(audioPath, format):
    a = AudioSegment.from_file(audioPath, format)
    print a

def getDataFromPath(filePath):
    fileName, extension = os.path.splitext(filePath)
    print 'name:', fileName, ' ext:', extension

    if extension.lower() == 'mp3':
        wavPath = fileName + '.wav'
        mp3 = AudioSegment.from_mp3(filePath)
        mp3.export(wavPath, format='wav')
        filePath = wavPath
    elif extension.lower() == '.m4a':
        wavPath = fileName + '.wav'
        m4a = AudioSegment.from_file(filePath, 'm4a')
        m4a.export(wavPath, format='wav')
        filePath = wavPath

    print filePath
    rate, sig = wave.read(filePath)
    return rate, sig