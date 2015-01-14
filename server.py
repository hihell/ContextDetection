import os
import sys

BASE_PATH = os.path.dirname(__file__)

import json
import algo.main as algoMain
import algo.utilsData as ud

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
def predict(req):

    d = json.loads(req.body)
    result = {}

    X = d['X']

    y = None
    if 'y' in d:
        y = d['y']

    distinct_id = 'default_distinct_id'
    if 'req_id' in d:
        result['req_id'] = d['req_id']

    pred = []
    if isinstance(X, list):
        pred = algoMain.predict_service(X, clf)
        result['prediction'] = pred.tolist()
        result['responseOk'] = True
    else:
        result['responseOk'] = False
        result['msg'] = 'X must be a array instead of:' + str(X)

    result['X'] = X
    if y:
        result['y'] = d['y']
        rate = ud.getCorrectRate(d['y'], pred)
        result['correct_rate'] = rate


    log(distinct_id, 'predict', result)

    return JsonResponse(result)

def test():
    d = {}
    d['status'] = 'ok'
    return JsonResponse(d)

def log(distinct_id, name, body):
    mp.track(distinct_id=distinct_id, event_name=name, properties=body)


urlpatterns = patterns('',
    url(r'^predict/$', predict),
    url(r'^test/$', test)
)

#load trained classifier
clf = algoMain.loadClassifier()

if __name__ == "__main__":
    execute_from_command_line(sys.argv)

