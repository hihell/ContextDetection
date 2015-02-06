import os
import sys

from algoMotion import main as algoMain


BASE_PATH = os.path.dirname(__file__)

import json
import algoMotion.utilsData as ud
import algoMotion.parameters as param

from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel
mp = Mixpanel('ccd6520fac580540b4a003e6ffa8e2e1')

settings.configure(
    DEBUG=True,
    SECRET_KEY='placerandomsecretkeyhere',
    ROOT_URLCONF=sys.modules[__name__],
    TEMPLATE_DIRS=(
        os.path.join(BASE_PATH, 'templates'),
    ),
)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predictByFeature(req):

    d = json.loads(req.body)
    result = {}

    X = d['X']

    distinct_id = 'default_distinct_id'
    if 'req_id' in d:
        result['req_id'] = d['req_id']

    pred = []
    if isinstance(X, list):
        pred = algoMain.predict_feature_service(X, clfVH)
        result['pred'] = pred.tolist()
        result['responseOk'] = True
    else:
        result['responseOk'] = False
        result['msg'] = 'X must be a array instead of:' + str(X)

    logFeaturePrediction(distinct_id, 'predictFeature', d, pred)

    return JsonResponse(result)

@csrf_exempt
def predictByRawData(req):

    d = json.loads(req.body)
    result = {}


    distinct_id = 'default_distinct_id'
    if 'req_id' in d:
        result['req_id'] = d['req_id']

    rawData = None
    X = None
    if 'rawData' in d and isinstance(d['rawData'], list):
        rawData = d['rawData']
        clfType = ['SS']
        if 'clfType' in d:
            clfType = d['clfType']

        clfDict = {}
        clfDict['VH'] = clfVH
        clfDict['SSClf1'] = clfSS_L1
        clfDict['SSClf2Active'] = clfSS_L2A
        clfDict['SSClf2Inactive'] = clfSS_L2I

        X, y2, result = algoMain.predict_raw_service(rawData, clfDict=clfDict, clfType=clfType)
        result['responseOk'] = True
    else:
        result['responseOk'] = False
        result['msg'] = 'rawData don not exit or not an array'

    logRawPrediction(distinct_id, 'predictRawData', rawData, X, result, y2)

    return JsonResponse(result)


def test():
    d = {}
    d['status'] = 'ok'
    return JsonResponse(d)

def logFeaturePrediction(distinct_id, name, reqBody, prediction):
    logProperties = {}

    logProperties['X'] = reqBody['X']
    logProperties['prediction'] = prediction.tolist()
    if 'y' in reqBody:
        logProperties['y'] = reqBody['y']
        rate = ud.getCorrectRate(reqBody['y'], prediction)
        logProperties['correct_rate'] = rate

    mp.track(distinct_id, name, logProperties)

def logRawPrediction(distinct_id, name, rawData, X, result, y=None):
    logProperties = {}

    logProperties['rawData'] = rawData
    logProperties['X'] = X

    logProperties['predVH'] = result['predVH']
    logProperties['predSS'] = result['predSS']

    if y:
        logProperties['y'] = y
        rateVH = ud.getCorrectRate(y, result['predVH'])
        rateSS = ud.getCorrectRate(y, result['predSS'])
        logProperties['correct_rate_VH'] = rateVH
        logProperties['correct_rate_SS'] = rateSS

    mp.track(distinct_id, name, logProperties)


urlpatterns = patterns('',
    url(r'^predictByFeature/$', predictByFeature),
    url(r'^predictByRawData/$', predictByRawData),
    url(r'^test/$', test)
)

#load trained classifiers
clfVH = algoMain.loadClassifier(param.CLASSIFIER_VH_PATH)
clfSS_L1 = algoMain.loadClassifier(param.CLASSIFIER_SS_L1_PATH)
clfSS_L2A = algoMain.loadClassifier(param.CLASSIFIER_SS_L2A_PATH)
clfSS_L2I = algoMain.loadClassifier(param.CLASSIFIER_SS_L2I_PATH)


if __name__ == "__main__":
    execute_from_command_line(sys.argv)

