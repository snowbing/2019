import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc


def calculate_delta(array):
    first=0
    rows, cols = mfcc_feat.shape
    print(rows)
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
                first = i - j
            index.append((second, first))
            j += 1
        deltas[i] = (mfcc_feat[index[0][0]] - mfcc_feat[index[0][1]] + (2 * (mfcc_feat[index[1][0]] - mfcc_feat[index[1][1]]))) / 10
    return deltas


def extract_features(audio, rate):
    mfcc_feat = mfcc.mfcc(audio, rate, 0.025, 0.01,20, appendEnergy=True)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)
    combined = np.hstack((mfcc_feat, delta))
    return combined