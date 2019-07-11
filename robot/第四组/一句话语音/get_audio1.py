
# coding: utf-8

# In[3]:


import pyaudio
import wave
import RPi.GPIO as GPIO

# In[5]:



def get_audio(filepath):
    #aa = str(input("是否开始录音？   （是/否）"))
    #if aa == str("是") :
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1                # 声道数
    RATE = 16000                # 采样率11025
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
					input_device_index=1,
                    frames_per_buffer=CHUNK)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    print("*"*10, "开始录音：请在2秒内输入语音")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*"*10, "录音结束\n")
    GPIO.output(18, GPIO.LOW)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    '''
    elif aa == str("否"):
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(in_path)
    '''
