
# coding: utf-8

# In[1]:


import os
import time
import threading
import ali_speech
import pyaudio
import wave
import jieba
from ali_speech.callbacks import SpeechRecognizerCallback
from ali_speech.constant import ASRFormat
from ali_speech.constant import ASRSampleRate
from get_audio1 import get_audio
from word_devide import jieba_devide
from find_command import find_cmd
from control import  control

import sys
sys.path.append('/home/pi/')
import CAM as CAM
# In[16]:


input_filename = "input1.wav"               # 麦克风采集的语音输入
input_filepath = "/home/pi/au/"              # 输入文件的path
in_path = input_filepath + input_filename


class MyCallback(SpeechRecognizerCallback):
    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """
    sen=''

    def __init__(self, name='input'):
        self._name = name
    def on_started(self, message):
        print('MyCallback.OnRecognitionStarted: %s' % message)
    def on_result_changed(self, message):
        print('MyCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s' % (
            self._name, message['header']['task_id'], message['payload']['result']))
    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: file: %s, task_id:%s, result:%s' % (
            self._name, message['header']['task_id'], message['payload']['result']))
        MyCallback.sen=message['payload']['result']
    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed: %s' % message)
    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')
def process(client, appkey, token):
    audio_name = '/home/pi/au/input1.wav'
    callback = MyCallback(audio_name)
    recognizer = client.create_recognizer(callback)
    recognizer.set_appkey(appkey)
    recognizer.set_token(token)
    recognizer.set_format(ASRFormat.PCM)
    recognizer.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    recognizer.set_enable_intermediate_result(False)
    recognizer.set_enable_punctuation_prediction(True)
    recognizer.set_enable_inverse_text_normalization(True)
    try:
        ret = recognizer.start()
        if ret < 0:
            return ret
        print('sending audio...')
        with open(audio_name, 'rb') as f:
            audio = f.read(3200)
            while audio:
                ret = recognizer.send(audio)
                if ret < 0:
                    break
                audio = f.read(3200)
        recognizer.stop()
    except Exception as e:
        print(e)
    finally:
        recognizer.close()
    return MyCallback.sen
def process_multithread(client, appkey, token, number):
    thread_list = []
    for i in range(0, number):
        thread = threading.Thread(target=process, args=(client, appkey, token))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
def au_control():
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')
    appkey = '8qMtpb3T6XdGvxAt'
    token = 'b502dcb93b96459199a485741d195d84'
    sec=1
    i=0
    while (sec==1):
        if_control = CAM.get()
        if(if_control != 1):
          continue
        get_audio(in_path)
        sentence_result=process(client, appkey, token)
        if sentence_result =='':
            sentence_result='错误'
        #word_list=jieba_devide(sentence_result)
        #cmd=find_cmd(word_list)
        elif '小车' in sentence_result:
            cmd = find_cmd(sentence_result)
            print('onesense:')
            print(cmd)
            control(cmd)
       # time.sleep(1)#具体延迟看stm32的反应速度
        #在此处开始调用串口传递函数传参cmd
    return 0

