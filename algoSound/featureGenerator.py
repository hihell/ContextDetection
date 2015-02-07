__author__ = 'jiusi'


from librosa.feature import mfcc as mfccAlgo
from librosa.feature import delta as mfccDelta

import parameters as param
import utilsData as ud

import numpy as np

# NOTE! librosa treat vector list differently than NDArray
# The MFCC passed to function is in NDArray's convention
# Need to transpose it before passing to librosa functions

def sigToMFCC(rate, sig, n_mfcc=param.N_MFCC):
    return mfccAlgo(y=sig, sr=rate, n_mfcc=n_mfcc).T

def mfccToMFCCDelta(mfccVectorList, order=1):
    mfccVectorList = mfccVectorList.T
    return mfccDelta(mfccVectorList, order=order).T

def getXy(rate, fileGroupedSig, fileGroupedY, frameTime, featureSchema):
    X = []
    y = []
    for i, fileSig in enumerate(fileGroupedSig):
        frames = ud.sigToFrames(rate, fileSig, frameTime)
        for frame in frames:
            tag = fileGroupedY[i]
            mfcc = sigToMFCC(rate, frame)
            feature = np.array(mfcc)

            if 'mfccDelta' in featureSchema:
                mfccDelta = mfccToMFCCDelta(feature)
                feature = np.append(feature, mfccDelta, axis=1)
            if 'mfccDelta2' in featureSchema:
                mfccDelta2 = mfccToMFCCDelta(mfcc, order=2)
                feature = np.append(feature, mfccDelta2, axis=1)

            X.extend(feature)
            y.extend([tag for j in range(0, feature.shape[0])])

    return X, y

def getFeatureFrameSize(rate, frameTime):
    testFrame = np.zeros(rate * frameTime)
    mfcc = sigToMFCC(rate, testFrame)
    return mfcc.shape[0]
