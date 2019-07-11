
#GPIO 18 -- 开门标志(绿)
#GPIO GND
#GPIO 23  -- 检测到有车到来(蓝)
#GPIO 24  -- 开启声纹识别 (黄)
#GND
#GPIO 25  -- 滚出去(红)
import os
import cv2
from speaker_recognization import recognization
import serial #导入模块
import RPi.GPIO as GPIO
import time

car_total=['辽BXFNB1','辽B88888']
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)	
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.LOW)


import sys,os
import base64
import time
import json

from urllib.parse import urlparse
import client
import request
import constant
import traceback
import urllib.request
import base64

def get_img_base64(img_file):
    with open(img_file, 'rb') as infile:
        s = infile.read()
        return base64.b64encode(s) 


def predict(url, appcode, img_base64, kv_config, old_format):
        if not old_format:
            param = {}
            param['image'] = img_base64
            if kv_config is not None:
                param['configure'] = json.dumps(kv_config)
            param['image']=param['image'].decode()
            body = json.dumps(param).encode()
        else:
            param = {}
            pic = {}
            pic['dataType'] = 50
            pic['dataValue'] = img_base64
            param['image'] = pic
    
            if kv_config is not None:
                conf = {}
                conf['dataType'] = 50
                conf['dataValue'] = json.dumps(kv_config) 
                param['configure'] = conf

    
            inputs = { "inputs" : [param]}
            body = json.dumps(inputs)


        headers = {'Authorization' : 'APPCODE %s' % appcode}
        request = urllib.request.Request(url = url, headers = headers, data = body)
        try:
            response = urllib.request.urlopen(request, timeout = 10)
            return response.code, response.headers, response.read()
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read()


def plate_recognization():
    cap=cv2.VideoCapture(0)
    print('开始录像!')
    time.sleep(1)
    ret,img = cap.read()
    cap.release()
    time.sleep(1)
    cv2.imwrite("test.png", img,[int(cv2.IMWRITE_JPEG_QUALITY), 5])
    appcode = '40ec9a83677a4bea9ba85b45e7fc1d23'
    url = 'https://ocrcp.market.alicloudapi.com/rest/160601/ocr/ocr_vehicle_plate.json'
    img_file = 'test.png'
    #如果输入带有inputs, 设置为True，否则设为False
    is_old_format = False
    config = {'multi_crop': False}
    #如果没有configure字段，config设为None
    #config = None

    img_base64data = get_img_base64(img_file)
    stat, header, content = predict( url, appcode, img_base64data, config, is_old_format)
    if stat != 200:
        print ('Http status code: ', stat)
        print ('Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else '')
        print ('Error msg in body: ', content)
        return 'xxxxxx'
    if is_old_format:
        result_str = json.loads(content)['outputs'][0]['outputValue']['dataValue']
    else:
        result_str = content
    #print (result_str)
    result = json.loads(result_str)
    if result['success']:
      car=result['plates'][0]['txt']
      print(car)
      return car
    else:
      print(car)
      return 'xxxxxx'
    
	
def get_distance():
	#1 -- 有车
	#0 -- 没车
	ser = serial.Serial("/dev/ttyAMA0",9600)
	d=int(ser.read().decode())
	print(d)
	if d:
		GPIO.output(23, GPIO.HIGH)
	else :
		GPIO.output(23, GPIO.LOW)
	return d
	
	
def opendoor():
	GPIO.output(18, GPIO.HIGH)

	ser = serial.Serial("/dev/ttyAMA0",9600)
	for i in range(8):
		ch=b'1\n'
		time.sleep(0.2)
		ser.write(ch)
	d=get_distance()
	while(d):
		time.sleep(1)
		d=get_distance()
	for i in range(6):
		ch=b'2\n'
		time.sleep(0.2)
		ser.write(ch)
	GPIO.output(18, GPIO.LOW)

	return 0
	
	
	
while 1:
	if_car = 0
    #while 1:
    #    portx='COM4'
    #    bps=9600
    #    timex=1#超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    #   ser=serial.Serial(portx,bps,timeout=timex)
    #    if_car=ser.read()#读一个字节 十六进制的读取
    #   ser.close()#关闭串口
	#	print(if_car)
    #    if if_car !=0:
    #        break
	if get_distance() == 0:
		continue
		a=1
	if_car = plate_recognization()
	if if_car in car_total:
		print ('车牌已识别')
		opendoor()
	else:
		print('车牌未识别,请输入语音!')
		GPIO.output(24, GPIO.HIGH)
		if_door=recognization()
		GPIO.output(24, GPIO.LOW)
		if if_door !=0:
			opendoor()
		else:
			print('我不认识你,请出去!')
			GPIO.output(25, GPIO.HIGH)
			while get_distance():
				continue
			GPIO.output(25, GPIO.LOW)
			
		

