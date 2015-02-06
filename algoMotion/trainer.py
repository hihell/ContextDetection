__author__ = 'jiusi'

import time

from sklearn.externals import joblib

# joblib.dump(clfVH, 'my_model.pkl', compress=9)

from sklearn import cross_validation

def train(trainList, targetList, classifier, savePath):
    scores = cross_validation.cross_val_score(classifier, trainList, trainList, cv=5)

    if savePath == None:
        joblib.dump(classifier, savePath, compress=9)
    else:
        joblib.dump(classifier, time.time() + '.pkl', compress=9)

    print scores
    return scores, classifier
