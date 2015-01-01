from __future__ import division

__author__ = 'jiusi'

import utilsData as ud
import utilsPlot as up
import trainer as tr
import featureGenerator as fg
from sklearn import svm, tree
from sklearn.cross_validation import cross_val_score
import numpy as np


GRAN_SAMPLE = 50
N_FOLD = 8

# featureList = [0,1]
featureList = range(0, 2)
featureNames = ['meanV', 'stdV', 'p75V', 'iqrV', 'meanH', 'stdH', 'coore[0]']

def train(filePaths, classifier):
    if not (isinstance(filePaths, list) or isinstance(filePaths, np.ndarray)):
        filePaths = [filePaths]

    buckets, y = ud.processFile(filePaths, GRAN_SAMPLE)
    trainData = []

    for bucket in buckets:
        # accList = ud.getDataByDataType('accelerator', bucket)

        regu = fg.regularizeSignal(bucket)
        verA = regu['verticalAmplitude']
        horM = regu['horizontalMagnitude']

        # features = fg.getFullFeatures(verticalAmplitude=verA, horizontalMagnitude=horM)
        features = fg.getSomeFeatures(verA, horM, featureList)

        trainData.append(features)

    score = cross_val_score(classifier, trainData, y, cv=N_FOLD)
    print score
    classifier.fit(trainData, y)

    # fn = [featureNames[i] for i in featureList]
    # up.plotDecisionBoundary(trainData, trainDataClass=y,
    #                         testData=None, classifier=classifier,
    #                         foil=[0,1], axisNames = fn,
    #                         title=filePaths)

    return classifier

def predict(filePaths, classifier, tagged=False):

    if not (isinstance(filePaths, list) or isinstance(filePaths, np.ndarray)):
        filePaths = [filePaths]

    buckets, y = ud.processFile(filePaths, GRAN_SAMPLE)

    predictData = []
    tags = []

    for bucket in buckets:
        regu = fg.regularizeSignal(bucket)
        verA = regu['verticalAmplitude']
        horM = regu['horizontalMagnitude']

        # features = fg.getFullFeatures(verA, horM)
        features = fg.getSomeFeatures(verA, horM, featureList)
        predictData.append(features)
        tags.append(ud.STAT_CODE[bucket[0]['status']])

    prediction = classifier.predict(predictData)
    print "pred:", prediction
    print "tags:", np.array(tags)

    if tagged:
        correctCount = 0
        for p, t in zip(prediction, tags):
            if p == t:
                correctCount += 1
        print "prediction correct rate:", correctCount / len(prediction)
    return prediction

clf_tree = tree.DecisionTreeClassifier()
clf_svm_rbf = svm.SVC(kernel='rbf', C=2)
clf_svm_lin = svm.SVC(kernel='linear', C=2)

# trainData = './data/train1.txt'
trainData = './data/train2.txt'
driving = './data/train_driving.txt'
driving1 = './data/train_driving1.txt'

walking = './data/walking.txt'
sitting = './data/sitting'
running = './data/somerunning.txt'
daiyue = './data/daiyue.txt'
daiyue1 = './data/daiyue1.txt'
john = './data/john.txt'
hengyang = './data/hengyang.txt'
smarT1 = '/Users/jiusi/walking1230.txt'

# clf = train(driving1, clf_tree)
# clf = train(trainData, clf_tree)
clf = train(trainData, clf_svm_lin)

predict(hengyang, clf_svm_lin, tagged=True)
# predict(john, clf_svm)
# predict(hengyang, clf_svm)
predict(daiyue, clf_svm_lin, tagged=True)
# predict(sitting, clf)
# predict(running, clf)
# predict(trainData, clf)