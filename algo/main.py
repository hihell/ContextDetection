from __future__ import division


__author__ = 'jiusi'

import utilsData as ud
import utilsPlot as up
import parameters as param
import featureGenerator as fg

from sklearn import svm, tree
from sklearn.cross_validation import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import pickle

featureList = range(0, 6)
featureNames = ['meanV', 'stdV', 'p75V', 'iqrV', 'meanH', 'stdH', 'coore[0]']

def loadClassifier(clfPath=param.CLASSIFIER_PATH):
    clf = joblib.load(clfPath)
    print 'classifier recovered from:', clfPath
    return clf

def saveClassifier(clf):
    s = joblib.dump(clf, param.CLASSIFIER_PATH)
    print 'classifier saved at:', s

def train(filePath, classifier):

    buckets, y = ud.processFile(filePath, param.GRAN_SAMPLE)
    trainData = []

    vhList = ud.processAccelerationData(buckets)

    for vh in vhList:
        verA = vh['verticalAmplitude']
        horM = vh['horizontalMagnitude']

        # features = fg.getFullFeatures(verticalAmplitude=verA, horizontalMagnitude=horM)
        features = fg.getSomeFeatures(verA, horM, featureList)

        trainData.append(features)

    score = cross_val_score(classifier, trainData, y, cv=param.N_FOLD)
    print score
    classifier.fit(trainData, y)

    fn = [featureNames[i] for i in featureList]
    up.plotDecisionBoundary(X=trainData, y=y,
                            clf=classifier,
                            foil=[0,1], axisNames = fn,
                            title=filePath)

    saveClassifier(classifier)
    return classifier

def predict_service(X, classifier):
    pred = classifier.predict(X)
    return pred

def predict_test(filePath, features, classifier, tagged=False):

    ud.printDataLabels(filePath)

    buckets, y = ud.processFile(filePath, param.GRAN_SAMPLE)

    VH = fg.getVHByBuckets(buckets)
    X = fg.getFeatureByVH(VH, featureList)

    print "X:", X

    # up.plotVH(VH, y=y, title=filePath)

    pred = classifier.predict(X)

    up.plotConfusionMatrix(y, pred)

    if tagged:
        print "prediction correct rate:", ud.getCorrectRate(y, pred)

    fn = [featureNames[i] for i in featureList]
    # up.plotDecisionBoundary(X,
    #                         pred,
    #                         classifier,
    #                         foil=[0,1],
    #                         axisNames=fn,
    #                         title=filePath)

    return pred
