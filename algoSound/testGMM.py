__author__ = 'jiusi'


import numpy as np
from sklearn import mixture
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

from sklearn import cross_validation

import parameters as param
import featureGenerator as fg

from utils import utils

import utilsData

def getTags(fileGroupedX, fileGroupedY):
    tagList = []
    for i, feature in enumerate(fileGroupedX):
        tagList.extend([fileGroupedY[i] for j in range(0, len(feature))])

    return tagList

def trainKNN(X, y):
    knn = KNeighborsClassifier()
    knn.fit(X, y)

    scores = cross_validation.cross_val_score(knn, X, y, cv=5)
    print "knn 5 fold score:", scores

    return knn

def trainGMM(X, n_components):
    g = mixture.GMM(n_components=n_components)
    g.fit(X)
    # print 'np.round(g.weights_, 2):', np.round(g.weights_, 2)
    # print 'np.round(g.means_, 2):', np.round(g.means_, 2)
    # print 'np.round(g.covars_, 2):', np.round(g.covars_, 2)
    return g

def trainTestClfs(rate, fileGroupedSig, fileGroupedY, frameTime, saveWhom):
    noDeltaX, y = fg.getXy(rate, fileGroupedSig, fileGroupedY, frameTime, [])
    withDeltaX, y = fg.getXy(rate, fileGroupedSig, fileGroupedY, frameTime, ['mfccDelta'])
    withDelta2X, y = fg.getXy(rate, fileGroupedSig, fileGroupedY,  frameTime, ['mfccDelta', 'mfccDelta2'])
    print 'feature retrieved'

    knnNoDelta = KNeighborsClassifier()
    knnWithDelta = KNeighborsClassifier()
    knnWithDelta2 = KNeighborsClassifier()

    gmmNoDelta = mixture.GMM(n_components=param.N_COMPONENTS)
    gmmWithDelta = mixture.GMM(n_components=param.N_COMPONENTS)
    gmmWithDelta2 = mixture.GMM(n_components=param.N_COMPONENTS)


    if param.CLF_KNN_MFCC['name'] in saveWhom:
        knnNoDelta.fit(noDeltaX, y)
        utils.saveClassifier(knnNoDelta, param.CLF_KNN_MFCC['path'])
        print 'clf trained for feature contains only mfcc finished'

        kNDScore = cross_validation.cross_val_score(knnNoDelta, X=noDeltaX, y=y, cv=param.K_FOLD)
        print 'with only mfcc:', kNDScore


    if param.CLF_KNN_MFCC_DELTA['name'] in saveWhom:
        knnWithDelta.fit(withDeltaX, y)
        utils.saveClassifier(knnWithDelta, param.CLF_KNN_MFCC_DELTA['path'])
        print 'clf trained for feature contains mfcc and mfcc delta finished'

        kDScore = cross_validation.cross_val_score(knnWithDelta, X=withDeltaX, y=y, cv=param.K_FOLD)
        print 'with mfcc, mfcc delta', kDScore


    if param.CLF_KNN_MFCC_DELTA2['name'] in saveWhom:
        knnWithDelta2.fit(withDelta2X, y)
        utils.saveClassifier(knnWithDelta2, param.CLF_KNN_MFCC_DELTA2['path'])
        print 'clf trained for feature contains mfcc mfcc delta and mfcc delta 2nd order finished'

        kD2Score = cross_validation.cross_val_score(knnWithDelta2, X=withDelta2X, y=y, cv=param.K_FOLD)
        print 'with mfcc, mfcc delta and mfcc delta 2nd order', kD2Score


    if param.CLF_GMM_MFCC['name'] in saveWhom:
        gmmNoDelta.fit(noDeltaX)
        utils.saveClassifier(gmmNoDelta, param.CLF_GMM_MFCC['path'])
        print 'GMM clf trained for mfcc only'

    if param.CLF_GMM_MFCC_DELTA['name'] in saveWhom:
        gmmWithDelta.fit(withDeltaX)
        utils.saveClassifier(gmmWithDelta, param.CLF_GMM_MFCC_DELTA['path'])
        print 'GMM clf trained for mfcc and mfcc delta'

    if param.CLF_GMM_MFCC_DELTA2['name'] in saveWhom:
        gmmWithDelta2.fit(withDelta2X)
        utils.saveClassifier(gmmWithDelta2, param.CLF_GMM_MFCC_DELTA2['path'])
        print 'GMM clf trained for mfcc mfcc delta and mfcc delta 2nd order'

# def compareClf(gmm, knn, rate, fileGroupedSig, fileGroupedL2, frameTime):
#     gmmList = testClf(gmm, rate, fileGroupedSig, frameTime)
#     knnList = testClf(knn, rate, fileGroupedSig, frameTime)
#
#     for i, tu in enumerate(zip(gmmList, knnList)):
#         tag = param.L2ContextIdNameMap[fileGroupedL2[i]]
#         gmmPred = tu[0]
#         knnPred = tu[1]
#
#         print "L2:", tag
#         print "gmm:", gmmPred
#         print "knn:", knnPred
#


def refinePrediction(predictionList, frameSize):
    predictionList = np.array(predictionList)
    frameGrouped = predictionList.reshape(predictionList.size/frameSize, frameSize)
    merged = []
    for predictionCluster in frameGrouped:
        classMap = {}
        for p in predictionCluster:
            if p in classMap:
                classMap[p] += 1
            else:
                classMap[p] = 1

        maxProbabilityClass = max(classMap, key=lambda i: classMap[i])
        merged.append(maxProbabilityClass)
    return merged

#
# def train(save=False):
#     trainRate, trainSigList, y = utilsData.getData(param.fileContextMap)
#     print 'train data retrieved'
#
#     mfccList = []
#     for trainSig in trainSigList:
#         mfcc = fg.sigToMFCC(trainRate, trainSig)
#         mfccList.append(mfcc)
#
#     knn = trainKNN(mfccList, y)
#
#     mfccs = []
#     for mfcc in mfccList:
#         mfccs.extend(mfcc)
#
#     gmm = trainGMM(mfccs, n_components=param.N_COMPONENTS)
#
#     print 'gmm trained'
#
#     if(save):
#         utils.saveClassifier(gmm, param.CLF_GMM_TEST)
#         utils.saveClassifier(knn, param.CLF_KNN_TEST)
#         print 'gmm saved to:', param.CLF_GMM_TEST, param.CLF_KNN_TEST
#     else:
#         print 'save param is false, will not save classifier'
#
#     return gmm, knn
#
#
#
#
# def test(gmm=None, knn=None):
#     if not gmm:
#         gmm = utils.loadClassifier(param.CLF_GMM_TEST)
#
#     if not knn:
#         knn = utils.loadClassifier(param.CLF_KNN_TEST)
#
#     trainRate, trainSigList, L2s = utilsData.getData(param.testSet)
#     # compareClf(gmm, knn, trainRate, trainSigList, L2s, frameTime=10)
#     # print testClf(gmm, trainRate, trainSigList, frameTime=10)
#

# gmm, knn = train(save=True)
# test(gmm, knn)
