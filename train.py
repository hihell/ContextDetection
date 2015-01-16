__author__ = 'jiusi'

import algo.main as algoMain
import algo.parameters as param
from sklearn import svm
from sklearn.qda import QDA

from sklearn.neighbors import KNeighborsClassifier

# clf_tree = tree.DecisionTreeClassifier()
clf_knnVH = KNeighborsClassifier(n_neighbors=len(param.STAT_CODE), weights='distance')
# 1st layer class, determine active/inactive
knnL1 = KNeighborsClassifier(weights='distance')
svmLinL1 = svm.SVC(kernel='linear')
# active class: walking, bicycling, running
knnL2Active = KNeighborsClassifier(weights='distance')
svmLinL2Active = svm.SVC(kernel='linear')
# inactive class: sitting, driving
knnL2Inactive = KNeighborsClassifier(weights='distance')
svmLinL2Inactive = svm.SVC(kernel='linear')

# clf_svm_rbf = svm.SVC(kernel='rbf', C=100)
clf_svm_lin = svm.SVC(kernel='linear', C=5)

# merge = './data/merge.txt'
#
# trainData2 = './data/train2.txt'
# trainData3 = './data/train3.txt'
# trainData4 = './data/train4.txt'
# trainData5 = './data/train5.txt'
trainData6 = '../data/train6.txt'
# driving = './data/train_driving.txt'
# driving1 = './data/train_driving1.txt'
#
walking = '../data/walking.txt'
# sitting = './data/sitting'
# running = './data/somerunning.txt'
daiyue = '../data/daiyue.txt.rfn'
# daiyue1 = './data/daiyue1.txt'
daiyue_r = '/Users/jiusi/Downloads/daiyue1229_riding.log'
# john = './data/john.txt'
hengyang = '../data/hengyang.txt.rfn'
# jiusi_w = '/Users/jiusi/Downloads/jiusi0112_walking.txt'
jiusi_s = '/Users/jiusi/Downloads/jiusi0112_sitting.txt'
#
# clf = algo.main.train(trainData6, clf_svm_lin)

featureList = [0,1]

# clf = algoMain.loadClassifier('../clf/clf.pkl')
# clf_knnVH, clf_knnSS = algoMain.trainVH(trainData6, clf_knnVH, clf_knnSS, featureList)
algoMain.trainSS(trainData6,
                 clf1=svmLinL1,
                 clf2Active=svmLinL2Active,
                 clf2Inactive=svmLinL2Inactive)

algoMain.predict_testSS(hengyang,
                        clf1=svmLinL1,
                        clf2Active=svmLinL2Active,
                        clf2Inactive=svmLinL2Inactive,
                        tagged=True)

# # clf = train(trainData, clf_tree)
# # clf = train(trainData6, clf_svm_lin)
#
# predict_test(daiyue_r, clf_svm_lin, tagged=True)
#
# # predict(hengyang, clf_svm_lin, tagged=True)
# # predict(john, clf_svm)
# # predict(hengyang, clf_svm)
# # predict(daiyue, clf_svm_lin, tagged=True)
# # predict(sitting, clf)
# # predict(running, clf)
# # predict(trainData, clf)