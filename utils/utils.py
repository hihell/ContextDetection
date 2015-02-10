__author__ = 'jiusi'
from sklearn.externals import joblib
import ntpath

def loadClassifier(clfPath):
    clf = joblib.load(clfPath)
    print 'classifier recovered from:', clfPath
    return clf

def saveClassifier(clf, savePath):
    s = joblib.dump(clf, savePath)
    print 'classifier saved at:', s

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)