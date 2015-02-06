__author__ = 'jiusi'

GRAN_SAMPLE = 100
N_FOLD = 5

STAT_DICT = {'Sitting':0, 'Driving':1, 'Riding':2, 'Walking':3, 'Running': 4}
STAT_NAME = ['Sitting', 'Driving', 'Riding', 'Walking', 'Running']

STAT_CLASS_MAP = {0:0, 1:0, 2:1, 3:1, 4:1}
STAT_CLASS_NAME = {'Inactive':0, 'Active':1}

STAT_CODE = [0, 1, 2, 3, 4]

CLASSIFIER_VH_PATH = 'clfVH/clf.pkl'
CLASSIFIER_SS_L1_PATH = 'clfSS_L1/clf.pkl'
CLASSIFIER_SS_L2A_PATH = 'clfSS_L2A/clf.pkl'
CLASSIFIER_SS_L2I_PATH = 'clfSS_L2I/clf.pkl'

# mesh
MARGIN = .5

# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white
statusColors = ['b', 'g', 'r', 'y', 'm']
statusMarkers =['+', 'x', 'o', '.', '<']

FEATURES_SERVICE = range(0,6)