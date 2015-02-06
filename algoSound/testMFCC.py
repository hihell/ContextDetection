__author__ = 'jiusi'

import numpy as np
from sklearn import mixture
import matplotlib.pyplot as plt
from librosa.feature import mfcc
import librosa

import scipy.io.wavfile as wave

# rate = 24000

# obs = np.concatenate((np.random.randn(100000, 1),
#                       10 + np.random.randn(300000, 1)))

soundPath = '/Users/jiusi/Desktop/audioSamples/Rec_003.wav'
forrest = '/Users/jiusi/dares_g1.1/dares_g1/left/forrest_1.wav'
livingRoom = '/Users/jiusi/dares_g1.1/dares_g1/left/living_room_1.wav'
study = '/Users/jiusi/dares_g1.1/dares_g1/left/study_1.wav'


rate,sig = wave.read(study)

mfccValue = mfcc(y=sig, sr=rate, n_mfcc=13)
delta_mfcc  = librosa.feature.delta(mfccValue)
delta2_mfcc = librosa.feature.delta(mfccValue, order=2)

# plt.plot()
#
# fig = plt.figure()
# signalSub = fig.addSubPlot()
# signalSub.plot(range(0, len(obs)), obs)

# mfccSub = fig.addSubPlot()
# mfccSub.plot(range(0, len(mfccValue)), mfccValue)


# How do they look?  We'll show each in its own subplot
plt.figure(figsize=(12, 6))

plt.subplot(2,1,1)
librosa.display.specshow(mfccValue)
plt.ylabel('MFCC')
plt.colorbar()

plt.subplot(2,1,2)
librosa.display.specshow(delta_mfcc)
plt.ylabel('MFCC-$\Delta$')
plt.colorbar()

# plt.subplot(3,1,3)
# librosa.display.specshow(delta2_mfcc, sr=sr, hop_length=64, x_axis='time')
# plt.ylabel('MFCC-$\Delta^2$')
# plt.colorbar()

plt.tight_layout()
plt.show()

# For future use, we'll stack these together into one matrix
# M = np.vstack([mfcc, delta_mfcc, delta2_mfcc])