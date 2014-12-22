__author__ = 'jiusi'

from sklearn.externals import joblib
import time
import featureGenerator as fg
# joblib.dump(clf, 'my_model.pkl', compress=9)

import numpy as np
import matplotlib.pyplot as plt

import utilsPlot

from scipy.fftpack import fft, fftfreq
from sklearn import svm, cross_validation

def train(trainList, targetList, classifier, savePath):
    scores = cross_validation.cross_val_score(classifier, trainList, trainList, cv=5)

    if savePath == None:
        joblib.dump(classifier, savePath, compress=9)
    else:
        joblib.dump(classifier, time.time() + '.pkl', compress=9)

    print scores
    return scores, classifier
