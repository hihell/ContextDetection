__author__ = 'jiusi'

import numpy as np
from sklearn import mixture
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.externals import joblib
from sklearn import cross_validation

import xmlReader
import parameters as param

from librosa.feature import mfcc as mfccL

import scipy.io.wavfile as wave

def getData(dataSetDict):
    classDict, fileDict = xmlReader.readXML(param.xmlPath)

    print "total data base files:", len(fileDict)

    fileNames = [name for name in dataSetDict]
    fileIDs = range(0, len(fileNames))

    fileNameIDMap = {}
    for name, id in zip(fileNames, fileIDs):
        fileNameIDMap[name] = id

    trainSigList = []
    L2s = []
    trainRate = 0
    root = "/Users/jiusi/dares_g1.1/dares_g1/"

    print "total train files:", len(fileNames)

    for name in fileNames:
        filePath = root + fileDict[name]['fileNameLeft']
        rate, sig = wave.read(filePath)
        trainSigList.append(sig)
        L2Code = dataSetDict[name]['L2']
        L2s.append(L2Code)
        trainRate = rate

    return trainRate, trainSigList, L2s



def sigToMFCC(rate, sig, n_mfcc):
    return mfccL(y=sig, sr=rate, n_mfcc=n_mfcc)

def trainKNN(X, y):
    k = KNeighborsClassifier()

    mfccList = []
    tagList = []
    for i, mfccs in enumerate(X):
        mfccList.extend(mfccs)
        tagList.extend([y[i] for j in range(0, len(mfccs))])

    k.fit(mfccList, tagList)

    scores = cross_validation.cross_val_score(k, mfccList, tagList, cv=5)
    print "knn 5 fold score:", scores

    return k

def trainGMM(obs, n_components):
    g = mixture.GMM(n_components=n_components)
    g.fit(obs)
    # print 'np.round(g.weights_, 2):', np.round(g.weights_, 2)
    # print 'np.round(g.means_, 2):', np.round(g.means_, 2)
    # print 'np.round(g.covars_, 2):', np.round(g.covars_, 2)
    return g


def sigToFrames(rate, sig, frameTime):
    frameSize = rate * frameTime
    trimmed = sig[0:(len(sig) - len(sig) % frameSize)]
    trimmed = np.array(trimmed)
    frames = trimmed.reshape(len(trimmed) / frameSize, frameSize)

    return frames

def testClf(clf, rate, sigList, frameTime):
    predList = []
    for sig in sigList:
        frames = sigToFrames(rate, sig, frameTime)
        mfccList = np.array([])
        mfccSize = 0

        for frame in frames:
            obs = mfccL(y=frame, sr=rate, n_mfcc=13).T
            mfccSize = obs.shape[0]
            if mfccList.size == 0:
                mfccList = np.array(obs)
            else:
                mfccList = np.append(mfccList, obs, axis=0)

        # print 'mfccList.shape:', mfccList.shape

        frameList = []
        bucket = []

        pred = clf.predict(mfccList)

        for i, p in enumerate(pred):
            if i % mfccSize == 0 and len(bucket) != 0:
                frameList.append(bucket)
                bucket = []
            bucket.append(p)

        mergedPred = mergePrediction(frameList)
        predList.append(mergedPred)

    return predList

def compareClf(gmm, knn, rate, sigList, L2s, frameTime):
    gmmList = testClf(gmm, rate, sigList, frameTime)
    knnList = testClf(knn, rate, sigList, frameTime)

    for i, tu in enumerate(zip(gmmList, knnList)):
        tag = param.L2ContextIdNameMap[L2s[i]]
        gmmPred = tu[0]
        knnPred = tu[1]

        print "L2:", tag
        print "gmm:", gmmPred
        print "knn:", knnPred


def mergePrediction(frameList):
    merged = []
    for predictionCluster in frameList:
        classMap = {}
        for p in predictionCluster:
            if p in classMap:
                classMap[p] += 1
            else:
                classMap[p] = 1

        maxProbabilityClass = max(classMap, key=lambda i: classMap[i])
        merged.append(maxProbabilityClass)
    return merged

def saveClassifier(clf, savePath):
    s = joblib.dump(clf, savePath)
    print 'classifier saved at:', s

def loadClassifier(clfPath):
    clf = joblib.load(clfPath)
    print 'classifier recovered from:', clfPath
    return clf


def train(save=False):
    trainRate, trainSigList, y = getData(param.fileContextMap)
    print 'train data retrieved'

    mfccList = []
    for trainSig in trainSigList:
        mfcc = mfccL(y=trainSig, sr=trainRate, n_mfcc=param.N_MFCC)
        mfccList.append(mfcc.T)

    knn = trainKNN(mfccList, y)

    mfccs = []
    for mfcc in mfccList:
        mfccs.extend(mfcc)

    gmm = trainGMM(mfccs, n_components=param.N_COMPONENTS)

    print 'gmm trained'

    if(save):
        saveClassifier(gmm, param.CLF_GMM_TEST)
        saveClassifier(knn, param.CLF_KNN_TEST)
        print 'gmm saved to:', param.CLF_GMM_TEST, param.CLF_KNN_TEST
    else:
        print 'save param is false, will not save classifier'

    return gmm, knn




def test(gmm=None, knn=None):
    if not gmm:
        gmm = loadClassifier(param.CLF_GMM_TEST)

    if not knn:
        knn = loadClassifier(param.CLF_KNN_TEST)

    trainRate, trainSigList, L2s = getData(param.testSet)
    compareClf(gmm, knn, trainRate, trainSigList, L2s, frameTime=10)
    # print testClf(gmm, trainRate, trainSigList, frameTime=10)


gmm, knn = train(save=True)
# test(gmm, knn)