__author__ = 'jiusi'

xmlPath = '/Users/jiusi/dares_g1.1/dares_g1.1_noxmlns.xml'
audioRoot = '/Users/jiusi/dares_g1.1/dares_g1/'
CLF_GMM = 'clfGMM/clf.pkl'
CLF_KNN = 'clfKNN/clf.pkl'

CLF_GMM_TEST = '../clfGMM/clf.pkl'
CLF_KNN_TEST = '../clfKNN/clf.pkl'

N_MFCC = 13
N_COMPONENTS = 30
N_NEIGHBORS = 3

K_FOLD = 5

FRAME_IN_SEC = 10

fileContextMap = {
    "busy_street_1": {"L1":0, "L2":0},
    "busy_street_2": {"L1":0, "L2":0},
    "busy_street_3": {"L1":0, "L2":0},
    "busy_street_4": {"L1":0, "L2":0},
    "busy_street_5": {"L1":0, "L2":0},
    "busy_street_6": {"L1":0, "L2":0},
    "busy_street_7": {"L1":0, "L2":0},
    "busy_street_8": {"L1":0, "L2":0},
    "busy_street_9": {"L1":0, "L2":0},
    "quiet_street_1": {"L1":0, "L2":1},
    "quiet_street_2": {"L1":0, "L2":1},
    "quiet_street_3": {"L1":0, "L2":1},
    "quiet_street_4": {"L1":0, "L2":1},
    "bus_station_1": {"L1":0, "L2":2},
    "bus_stop_1": {"L1":0, "L2":2},
    "bus_stop_2": {"L1":0, "L2":2},
    "bus_stop_3": {"L1":0, "L2":2},

    "living_room_1":{"L1":1,"L2":3},
    "living_room_10":{"L1":1,"L2":3},
    "living_room_11":{"L1":1,"L2":3},
    "living_room_12":{"L1":1,"L2":3},
    "living_room_13":{"L1":1,"L2":3},
    "living_room_14":{"L1":1,"L2":3},
    "living_room_15":{"L1":1,"L2":3},
    "living_room_16":{"L1":1,"L2":3},
    "living_room_17":{"L1":1,"L2":3},
    "living_room_18":{"L1":1,"L2":3},
    "living_room_19":{"L1":1,"L2":3},
    "living_room_2":{"L1":1,"L2":3},
    "living_room_20":{"L1":1,"L2":3},
    "living_room_21":{"L1":1,"L2":3},
    "living_room_22":{"L1":1,"L2":3},
    "living_room_23":{"L1":1,"L2":3},
    "living_room_24":{"L1":1,"L2":3},
    "living_room_25":{"L1":1,"L2":3},
    "living_room_26":{"L1":1,"L2":3},
    "living_room_27":{"L1":1,"L2":3},
    "living_room_28":{"L1":1,"L2":3},
    "living_room_3":{"L1":1,"L2":3},
    "living_room_4":{"L1":1,"L2":3},
    "living_room_5":{"L1":1,"L2":3},
    "living_room_6":{"L1":1,"L2":3},
    "living_room_7":{"L1":1,"L2":3},
    "living_room_8":{"L1":1,"L2":3},
    "living_room_9":{"L1":1,"L2":3},
    "kitchen_1":{"L1":1, "L2":4},
    "kitchen_2":{"L1":1, "L2":4},
    "kitchen_3":{"L1":1, "L2":4},
    "kitchen_4":{"L1":1, "L2":4},
    "kitchen_5":{"L1":1, "L2":4},
    "kitchen_6":{"L1":1, "L2":4},
    "kitchen_7":{"L1":1, "L2":4},
    "kitchen_8":{"L1":1, "L2":4},
    "kitchen_9":{"L1":1, "L2":4},
    "hallway_1":{"L1":1, "L2":5},
    "hallway_2":{"L1":1, "L2":5},
    "hallway_4":{"L1":1, "L2":5},
    "hallway_5":{"L1":1, "L2":5},
    "bedroom_1":{"L1":1, "L2":6},
    "bedroom_2":{"L1":1, "L2":6},
    "bedroom_3":{"L1":1, "L2":6},
    "flat_1":{"L1":1, "L2":7},
    "flat_10":{"L1":1, "L2":7},
    "flat_11":{"L1":1, "L2":7},
    "flat_12":{"L1":1, "L2":7},
    "flat_13":{"L1":1, "L2":7},
    "flat_2":{"L1":1, "L2":7},
    "flat_3":{"L1":1, "L2":7},
    "flat_4":{"L1":1, "L2":7},
    "flat_5":{"L1":1, "L2":7},
    "flat_6":{"L1":1, "L2":7},
    "flat_7":{"L1":1, "L2":7},
    "flat_8":{"L1":1, "L2":7},
    "flat_9":{"L1":1, "L2":7},

    "forrest_1":{"L1":2, "L2":8},
    "forrest_2":{"L1":2, "L2":8},
    "forrest_4":{"L1":2, "L2":8},
    "forrest_5":{"L1":2, "L2":8},

    "train_station_1":{"L1":3, "L2":9},

    "supermarket_1":{"L1":4, "L2":10},
    "supermarket_2":{"L1":4, "L2":10},
    "supermarket_3":{"L1":4, "L2":10},
    "supermarket_4":{"L1":4, "L2":10},
    "supermarket_5":{"L1":4, "L2":10},
    "supermarket_6":{"L1":4, "L2":10},
    "shop_1":{"L1":4, "L2":11},
    "shop_2":{"L1":4, "L2":11},

    "study_1":{"L1":5, "L2":12},
    "study_10":{"L1":5, "L2":12},
    "study_11":{"L1":5, "L2":12},
    "study_12":{"L1":5, "L2":12},
    "study_13":{"L1":5, "L2":12},
    "study_2":{"L1":5, "L2":12},
    "study_3":{"L1":5, "L2":12},
    "study_4":{"L1":5, "L2":12},
    "study_5":{"L1":5, "L2":12},
    "study_6":{"L1":5, "L2":12},
    "study_7":{"L1":5, "L2":12},
    "study_8":{"L1":5, "L2":12},
    "study_9":{"L1":5, "L2":12}
}


testSet = {
    "busy_street_5": {"L1":0, "L2":0},
    "living_room_24":{"L1":1,"L2":3},
}

L1ContextIdNameMap = {
    0:"outside",
    1:"home",
    2:"wild",
    3:"reverberant places",
    4:"public area",
    5:"quite inside"
}

L2ContextIdNameMap = {
    0:"busy street",
    1:"quite street",
    2:"bus stop",
    3:"living room",
    4:"kitchen",
    5:"hallway",
    6:"bedroom",
    7:"flat",
    8:"forrest",
    9:"train station",
    10:"supermarket",
    11:"shop",
    12:"study quite office",
}