__author__ = 'jiusi'

import utilsData as ud
import utilsPlot as up
import trainer as tr
import featureGenerator as fg
from sklearn import svm, tree
from sklearn.cross_validation import cross_val_score
import numpy as np

GRAN_SAMPLE = 50
N_FOLD = 5

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

        features = fg.getFullFeatures(verticalAmplitude=verA, horizontalMagnitude=horM)
        trainData.append(features)

    score = cross_val_score(classifier, trainData, y, cv=N_FOLD)
    print score
    classifier.fit(trainData, y)

    return classifier

def predict(filePaths, classifier):

    if not (isinstance(filePaths, list) or isinstance(filePaths, np.ndarray)):
        filePaths = [filePaths]

    buckets, y = ud.processFile(filePaths, GRAN_SAMPLE)

    predictData = []
    tags = []

    for bucket in buckets:
        regu = fg.regularizeSignal(bucket)
        verA = regu['verticalAmplitude']
        horM = regu['horizontalMagnitude']

        features = fg.getFullFeatures(verA, horM)
        predictData.append(features)
        tags.append(ud.STAT_CODE[bucket[0]['status']])

    prediction = classifier.predict(predictData)
    print "pred:", prediction
    print "tags:", np.array(tags)
    return prediction

clf_tree = tree.DecisionTreeClassifier()
clf_svm = svm.SVC(kernel='linear', C=1)

trainData = './data/train.txt'
walking = './data/walking.txt'
sitting = './data/sitting'
running = './data/somerunning.txt'

clf = train(trainData, clf_svm)
# clf = train(trainData, clf_tree)

predict(walking, clf)
predict(sitting, clf)
predict(running, clf)
# predict(trainData, clf)