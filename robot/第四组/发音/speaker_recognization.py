
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


def output():
	path='/home/pi/au/output/'
	#source = "development_set/"
	#modelpath = "speaker_models/"
	#test_file = "development_set_test.txt"
	#file_paths = open(test_file, 'r')
	in_path=path+'input.wav'


	# In[3]:


	gmm_files = [path+'speaker_models/wangziwei.gmm',path+'speaker_models/wuqiurun.gmm']
	#print(gmm_files)


	# In[4]:


	models = [cPickle.load(open(fname, 'rb')) for fname in gmm_files]


	# In[28]:


	#sec=1
	#while (sec==1):
	get_audio(in_path)
	sr, audio = read(in_path)
	id=0
	mfcc_feat = mfcc.mfcc(audio, sr, 0.025, 0.01,20, appendEnergy=True)
	mfcc_feat = preprocessing.scale(mfcc_feat)
	rows, cols = mfcc_feat.shape
	#print(rows)
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
	loser = 1- winner
	dif=log_likelihood[winner]-log_likelihood[loser]
	if winner==0 and dif>500:
		print('wangziwei')
		id_u=1
	elif winner==1 and dif>500:
		print('wuqiurun')
		id_u=2
	elif dif<=500:
		print('unknown')
		id_u=0
	if id_u==1:
		play_audio(path+'welcome.wav')
		play_audio(path+'wzw.wav')
	if id_u==2:
		play_audio(path+'welcome.wav')
		play_audio(path+'wqr.wav')
	if id_u==0:
		play_audio(path+'unknown.wav')
	return
