__author__ = 'jiusi'

# import pyaudio
# import wave
import sys

from librosa.feature import mfcc as mfccL

import numpy as np
import operator

import scipy.io.wavfile as wave
from sklearn import mixture

import matplotlib.pyplot as plt

CHUNK = 1024

GANU = 1

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

rate,sig = wave.read(sys.argv[1])

g = mixture.GMM(n_components=5)

obsTrain = mfccL(y=sig, sr=rate, n_mfcc=13)
print 'fit result:', g.fit(obsTrain.T)

frameSize = rate * GANU

trimmed = sig[0:(len(sig) - len(sig)%frameSize)]
trimmed = np.array(trimmed)

print 'frame count:', len(trimmed) / frameSize

frames = trimmed.reshape(len(trimmed) / frameSize, frameSize)

print 'frames shape:', frames.shape

mfccList = np.array([])
mfccSize = 0
for frame in frames:
    mfcc = mfccL(y=frame, sr=rate, n_mfcc=13)
    mfccSize = mfcc.shape[1]
    if mfccList.size == 0:
        mfccList = np.array(mfcc)
    else:
        mfccList = np.append(mfccList, mfcc, axis=1)


obs = mfccList.T
# plt.plot(obs[:1],obs[:0])
print 'obs.shape:', obs.shape


predictionList = []
bucket = []
prediction = g.predict(obs)

print "prediction[0]:", prediction[0]

for i, p in enumerate(prediction):
    if i % mfccSize == 0 and len(bucket) != 0:
        predictionList.append(bucket)
        bucket = []
    bucket.append(p)

mergedPrediction = []

print "predictionList[2]:", predictionList[2]

for predictionCluster in predictionList:
    classMap = {}
    for p in predictionCluster:
        if p in classMap:
            classMap[p] += 1
        else:
            classMap[p] = 1

    maxProbabilityClass = max(classMap.iteritems(), key=operator.itemgetter(1))[0]
    mergedPrediction.append(maxProbabilityClass)

print mergedPrediction

# instantiate PyAudio (1)
# p = pyaudio.PyAudio()
#
# # open stream (2)
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframeratde(),
#                 output=True)
#
# # read data
# data = wf.readframes(CHUNK)
#
# # play stream (3)
# while data != '':
#     stream.write(data)
#     data = wf.readframes(CHUNK)
#
# # stop stream (4)
# stream.stop_stream() g
# stream.close()
#
# # close PyAudio (5)
# p.terminate()