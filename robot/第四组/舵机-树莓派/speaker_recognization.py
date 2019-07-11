
# coding: utf-8

# In[24]:


import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
import warnings
import time
from sklearn.mixture import GMM
from sklearn import preprocessing
import python_speech_features as mfcc
from get_audio import get_audio
from play_audio import play_audio

def recognization():
    in_path='input.wav'

    gmm_files = ['speaker_models/wangziwei.gmm','speaker_models/wuqiurun.gmm','speaker_models/baiyunpeng.gmm']

    models = [cPickle.load(open(fname, 'rb')) for fname in gmm_files]

    get_audio(in_path)
    sr, audio = read("input.wav")
    id_u=0
    mfcc_feat = mfcc.mfcc(audio, sr, 0.025, 0.01,20, appendEnergy=True)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    rows, cols = mfcc_feat.shape
    deltas = np.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i + j > rows - 1:
                second = rows - 1
            else:
                second = i + j
            if i - j < 0:
                first = 0
            else:
                first = i-j
            index.append((second, first))
            j += 1
        deltas[i] = (mfcc_feat[index[0][0]] - mfcc_feat[index[0][1]] + (2 * (mfcc_feat[index[1][0]] - mfcc_feat[index[1][1]]))) / 10
    vector = np.hstack((mfcc_feat, deltas))

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        scores = np.array(gmm.score(vector))
        #print(scores.shape)
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)
    if winner == 0:
        dif_1 = log_likelihood[winner] - log_likelihood[1]
        dif_2 = log_likelihood[winner] - log_likelihood[2]
    if winner == 1:
        dif_1 = log_likelihood[winner] - log_likelihood[0]
        dif_2 = log_likelihood[winner] - log_likelihood[2]
    if winner == 2:
        dif_1 = log_likelihood[winner] - log_likelihood[0]
        dif_2 = log_likelihood[winner] - log_likelihood[1]
    if winner == 0 and dif_1 > 650 and dif_2 > 650:
        print('wangziwei')
        id_u = 1
    elif winner == 1 and dif_1 > 650 and dif_2 > 650:
        print('wuqiurun')
        id_u = 2
    elif winner == 2 and dif_1 > 650 and dif_2 > 650:
        print('baiyunpeng')
        id_u = 3
    elif dif_1 <= 650 and dif_2 <= 650:
        print('unknown')
        id_u = 0
    return id_u
