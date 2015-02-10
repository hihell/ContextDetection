__author__ = 'jiusi'

from algoSound import utilsData, testGMM
import algoSound.parameters as param


rate, fileGroupedSig, fileGroupedY = utilsData.getData(param.fileContextMap)
print 'data retrieved'

gmmList = [param.CLF_GMM_MFCC['name'], param.CLF_GMM_MFCC_DELTA['name'], param.CLF_GMM_MFCC_DELTA2['name']]
knnList = [param.CLF_KNN_MFCC['name'], param.CLF_KNN_MFCC_DELTA['name'], param.CLF_KNN_MFCC_DELTA2['name']]

testGMM.trainTestClfs(rate, fileGroupedSig, fileGroupedY, param.FRAME_IN_SEC, gmmList)