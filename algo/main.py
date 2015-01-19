from __future__ import division


__author__ = 'jiusi'

import utilsData as ud
import utilsPlot as up
import parameters as param
import featureGenerator as fg

import numpy as np

from sklearn import svm, tree
from sklearn.cross_validation import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import pickle

featureNames = ['meanV', 'stdV', 'p75V', 'iqrV', 'meanH', 'stdH', 'coore[0]']

activeCode = param.STAT_CLASS_NAME['Active']
inactiveCode = param.STAT_CLASS_NAME['Inactive']


def loadClassifier(clfPath):
    clf = joblib.load(clfPath)
    print 'classifier recovered from:', clfPath
    return clf

def saveClassifier(clf, savePath):
    s = joblib.dump(clf, savePath)
    print 'classifier saved at:', s

def trainVH(filePath, clf, featureList=range(0,7), save=False):

    buckets, y, drop = ud.processFile(filePath, param.GRAN_SAMPLE)

    VH = fg.accToVH(buckets)
    X = fg.getFeatureByVH(VH, featureList)

    scoreVH = cross_val_score(clf, X, y, cv=param.N_FOLD)
    print scoreVH
    clf.fit(X, y)

    fn = [featureNames[i] for i in featureList]
    up.plotDecisionBoundary(X=X, y=y,
                            clf=clf,
                            foil=[0,1], axisNames = fn,
                            title=filePath)
    if save:
        saveClassifier(clf, param.CLASSIFIER_VH_PATH)
    return clf

def trainSS(filePath, clf1, clf2Active, clf2Inactive, save=False):
    buckets, y2, y1 = ud.processFile(filePath, param.GRAN_SAMPLE)
    SS = fg.accToSqrSum(buckets)
    X = fg.getFeatureBySS(SS)

    # train 1st layer classifier
    scoreL1 = cross_val_score(clf1, X, y1, cv=param.N_FOLD)
    print 'score layer 1:', scoreL1
    clf1.fit(X, y1)

    # split data by it's general activity level (active / inactive)
    activeData = []
    aL2 = []
    inactiveData = []
    iL2 = []
    for data, l1, l2 in zip(X, y1, y2):
        if l1 == inactiveCode:
            inactiveData.append(data)
            iL2.append(l2)
        elif l1 == activeCode:
            activeData.append(data)
            aL2.append(l2)

    # train 2nd layer classifiers
    scoreAL2 = cross_val_score(clf2Active, activeData, aL2, cv=param.N_FOLD)
    scoreIL2 = cross_val_score(clf2Inactive, inactiveData, iL2, cv=param.N_FOLD)

    print 'score active data:', scoreAL2
    print 'score inactive data:', scoreIL2

    clf2Active.fit(activeData, aL2)
    clf2Inactive.fit(inactiveData, iL2)

    if save:
        saveClassifier(clf1, param.CLASSIFIER_SS_L1_PATH)
        saveClassifier(clf2Active, param.CLASSIFIER_SS_L2A_PATH)
        saveClassifier(clf2Inactive, param.CLASSIFIER_SS_L2I_PATH)

    return clf1, clf2Active, clf2Inactive

def predict_feature_service(X, clfVH):
    # TODO change this to clfVH tree
    pred = clfVH.predict(X)
    return pred

def predict_raw_service(rawData, clfDict, clfType):
    buckets = ud.processRawData(rawData, param.GRAN_SAMPLE)

    print "len(buckets):", len(buckets)

    result = {}

    if 'VH' in clfType:
        clf = clfDict['VH']

        VH = fg.accToVH(buckets)
        X = fg.getFeatureByVH(VH, param.FEATURES_SERVICE)

        result['predVH'] = clf.predict(X).tolist()

    if 'SS' in clfType:
        clf1 = clfDict['SSClf1']
        clf2Active = clfDict['SSClf2Active']
        clf2Inactive = clfDict['SSClf2Inactive']

        SS = fg.accToSqrSum(buckets)
        X  = fg.getFeatureBySS(SS)

        result['predSS'] = predictSS(X, clf1, clf2Active, clf2Inactive)

    return result

def predict_testVH(filePath, clf, featureList=range(0,7), tagged=False):

    ud.printDataLabels(filePath)

    buckets, y, drop = ud.processFile(filePath, param.GRAN_SAMPLE)

    VH = fg.accToVH(buckets)
    X = fg.getFeatureByVH(VH, featureList)

    print "X:", X

    predVH = clf.predict(X)

    if tagged:
        up.plotConfusionMatrix(y, predVH)
        print "VH prediction correct rate:", ud.getCorrectRate(y, predVH)

    fn = [featureNames[i] for i in featureList]
    up.plotDecisionBoundary(X,
                            predVH,
                            clf,
                            foil=[0,1],
                            axisNames=fn,
                            title=filePath)

    return predVH

def predict_testSS(filePath, clf1, clf2Active, clf2Inactive, tagged=False):
    ud.printDataLabels(filePath)

    buckets, y2, y1 = ud.processFile(filePath, param.GRAN_SAMPLE)

    SS = fg.accToSqrSum(buckets)
    X = fg.getFeatureBySS(SS)

    p = predictSS(X, clf1, clf2Active, clf2Inactive)

    if tagged:
        up.plotConfusionMatrixSS(y2, p)

    return p

def predictSS(X, clf1, clf2Active, clf2Inactive):
    X = np.array(X)

    p1 = clf1.predict(X)

    actIndexes = []
    inaIndexes = []

    # setup true tag for confusion matrix
    for i, (data, l1) in enumerate(zip(X, p1)):
        if l1 == inactiveCode:
            inaIndexes.append(i)
        elif l1 == activeCode:
            actIndexes.append(i)

    p2Active, p2Inactive = [], []
    activeData = X[actIndexes]
    inactiveData = X[inaIndexes]
    if len(actIndexes) > 0:
        p2Active = clf2Active.predict(activeData)
    if len(inaIndexes) > 0:
        p2Inactive = clf2Inactive.predict(inactiveData)

    pIndex = np.concatenate((actIndexes,inaIndexes), axis=0)
    pred = np.concatenate((p2Active, p2Inactive), axis=0)

    zipped = zip(pIndex, pred)
    zipped.sort(key = lambda t:t[0])

    p = [prediction for index, prediction in zipped]

    return p