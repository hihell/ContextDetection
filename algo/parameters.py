__author__ = 'jiusi'

GRAN_SAMPLE = 100
N_FOLD = 8

STAT_DICT = {'Sitting':0, 'Driving':1, 'Riding':2, 'Walking':3, 'Running': 4}
STAT_NAME = ['Sitting', 'Driving', 'Riding', 'Walking', 'Running']

STAT_CLASS_MAP = {0:0, 1:0, 2:1, 3:1, 4:1}
STAT_CLASS_NAME = {'Inactive':0, 'Active':1}

STAT_CODE = [0, 1, 2, 3, 4]

CLASSIFIER_PATH = 'clf/clf.pkl'

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
