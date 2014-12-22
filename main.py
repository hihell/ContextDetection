__author__ = 'jiusi'

import utilsData as ud
import trainer as tr
import featureGenerator as fg
from sklearn import svm, tree
from sklearn.cross_validation import cross_val_score

GRAN_SAMPLE = 50
N_FOLD = 5

def train(filePath, classifier):

    buckets, y = ud.processFile(filePath, GRAN_SAMPLE)
    trainData = []

    for bucket in buckets:
        # accList = ud.getDataByDataType('accelerator', bucket)
        print len(bucket)
        regu = fg.regularizeSignal(bucket)
        verA = regu['verticalAmplitude']
        horM = regu['horizontalMagnitude']

        features = fg.getFullFeatures(verticalAmplitude=verA, horizontalMagnitude=horM)
        trainData.append(features)

    score = cross_val_score(classifier, trainData, y, cv=N_FOLD)
    print score
    classifier.fit(trainData, y)

    return classifier

def predict(filePath, classifier):
    buckets, y = ud.processFile(filePath, GRAN_SAMPLE)

    predictData = []

    for bucket in buckets:
        print len(bucket)
        regu = fg.regularizeSignal(bucket)
        verA = regu['verticalAmplitude']
        horM = regu['horizontalMagnitude']

        features = fg.getFullFeatures(verA, horM)
        predictData.append(features)

    prediction = classifier.predict(predictData)
    print prediction
    return prediction

clf_tree = tree.DecisionTreeClassifier()
clf_svm = svm.SVC(kernel='linear', C=1)

data1 = '/Users/jiusi/try.txt'
data2 = '/Users/jiusi/walkingandsitting1221.txt' # dirty one
data3 = '/Users/jiusi/walking12130.txt'
data4 = '/Users/jiusi/shouldsmall.txt'
data5 = '/Users/jiusi/doutui.txt'

# clf = train(data1, clf_svm)
clf = train(data1, clf_svm)
predict(data5, clf)