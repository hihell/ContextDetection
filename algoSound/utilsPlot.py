__author__ = 'jiusi'

import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

import utilsData as ud
import parameters as param

from sklearn import mixture
from librosa.feature import mfcc

from utils import utils


def plotMFCCs(filePathList):
    rates = []
    sigs = []
    for filePath in filePathList:
        rate, sig = ud.getDataFromPath(filePath)
        rates.append(rate)
        sigs.append(sig)

    mfccValueList = []
    mfccDeltaList = []
    for rate, sig in zip(rates, sigs):
        mfccValue = mfcc(y=sig, sr=rate, n_mfcc=param.N_MFCC)
        mfccDelta = librosa.feature.delta(mfccValue)
        mfccValueList.append(mfccValue)
        mfccDeltaList.append(mfccDelta)

    unitHeight = 10
    figHeight = 10 * (len(filePathList) * 2)
    figSize = (figHeight, unitHeight)
    print figSize

    plt.figure(figsize=figSize)

    for i, tu in enumerate(zip(mfccValueList, mfccDeltaList)):
        mfccValue = tu[0]
        mfccDelta = tu[1]

        fileName = utils.path_leaf(filePathList[i])

        a = len(filePathList) * 2
        b = 1
        c = i * 2 + 1
        print a, b, c
        plt.subplot(a, b, c)
        librosa.display.specshow(mfccValue)
        plt.ylabel('mfcc:' + fileName)
        plt.colorbar()

        print a, b, c+1
        plt.subplot(a, b, c+1)
        librosa.display.specshow(mfccDelta)
        plt.ylabel('mfcc delta')
        plt.colorbar()

    plt.tight_layout()
    plt.show()

quite_smarti = '/Users/jiusi/Desktop/smarti_ref.wav'
quite_iphone = '/Users/jiusi/Desktop/iphone_ref.m4a'

plotMFCCs([quite_smarti, quite_iphone])
